from datetime import datetime, timezone

from ninja import NinjaAPI, Schema

from django.db import transaction
from django.shortcuts import get_object_or_404

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema
from incursions.models.waitlist import CharacterRoles, Role


class RoleSchema(Schema):
    name: str
    description: str


class CommanderSchema(Schema):
    character: CharacterSchema
    role: RoleSchema
    granted_by: CharacterSchema | None
    granted_at: datetime


class CommanderFiltersSchema(Schema):
    name: str
    member_count: int


class CommanderListSchema(Schema):
    commanders: list[CommanderSchema]
    filters: list[CommanderFiltersSchema]


class RequestPayload(Schema):
    character_id: int
    role: str


logger = get_extension_logger(__name__)
api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    CommandersAPIEndpoints(api)


class CommandersAPIEndpoints:

    tags = ["Commanders"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/commanders", response={200: CommanderListSchema, 403: dict}, tags=self.tags)
        def list_commanders(request):
            if not request.user.has_perm("incursions.view_commanders"):
                logger.warning(f"User {request.user} denied access to commander list")
                return 403, {"error": "Permission denied"}

            commanders = CharacterRoles.objects.select_related("character", "role", "granted_by")
            filters = Role.objects.only("pk", "name")
            logger.info(f"User {request.user} fetched {commanders.count()} commanders and {filters.count()} filters")
            return 200, CommanderListSchema(commanders=list(commanders), filters=list(filters))

        @api.post("/commanders", response={200: dict, 400: dict, 403: dict, 404: dict}, tags=self.tags)
        def assign_commander(request, payload: RequestPayload):
            if not request.user.has_perm("incursions.manage_commanders"):
                logger.warning(f"User {request.user} denied assigning commander role")
                return 403, {"error": "Permission denied"}

            if CharacterRoles.objects.filter(character__character_id=payload.character_id).exists():
                logger.warning(f"Character {payload.character_id} already has a commander role")
                return 400, {"error": "Character already has a role"}

            role = get_object_or_404(Role, name=payload.role)
            character = get_object_or_404(EveCharacter, character_id=payload.character_id)
            issuer = get_main_character_from_user(request.user)

            if role.power > CharacterRoles.objects.get(character=issuer).role.power:
                logger.warning(f"User {request.user} attempted to assign higher power role")
                return 403, {"error": "Permission denied, You don't have the power to assign this role"}

            with transaction.atomic():
                commander = CharacterRoles.objects.create(
                    character=character,
                    role=role,
                    granted_by=issuer,
                    granted_at=datetime.now(timezone.utc)
                )

            logger.info(f"Assigned commander role {role.name} to character {character.pk} by user {request.user}")
            return 200, {"status": "Commander assigned", "id": commander.pk}

        @api.get("/commanders/roles", response={200: list[str], 403: dict}, tags=self.tags)
        def assignable_roles(request):
            if not request.user.has_perm("incursions.view_commanders"):
                logger.warning(f"User {request.user} denied access to roles list")
                return 403, {"error": "Permission denied"}

            roles = list(Role.objects.only("name").values_list("name", flat=True))
            logger.info(f"User {request.user} fetched {len(roles)} assignable roles")
            return 200, roles

        @api.get("/commanders/{character_id}", response={200: str, 403: dict}, tags=self.tags)
        def lookup_commander(request, character_id: int):
            if not request.user.has_perm("incursions.view_commanders"):
                logger.warning(f"User {request.user} denied lookup for character {character_id}")
                return 403, {"error": "Permission denied"}

            character_role = get_object_or_404(CharacterRoles.objects.select_related("role"), character__character_id=character_id)
            logger.info(f"User {request.user} looked up role {character_role.role.name} for character {character_id}")
            return 200, character_role.role.name

        @api.delete("/commanders/{character_id}", response={200: dict, 403: dict, 404: dict}, tags=self.tags)
        def revoke_commander(request, character_id: int):
            if not request.user.has_perm("incursions.manage_commanders"):
                logger.warning(f"User {request.user} denied revoke for character {character_id}")
                return 403, {"error": "Permission denied"}

            try:
                commander = CharacterRoles.objects.select_related("role").get(character__character_id=character_id)
            except CharacterRoles.DoesNotExist:
                logger.error(f"Commander role not found for character {character_id}")
                return 404, {"error": "Commander role not found"}

            issuer = get_main_character_from_user(request.user)
            if commander.role.power > CharacterRoles.objects.get(character=issuer).role.power:
                logger.warning(f"User {request.user} lacks permission to revoke role from character {character_id}")
                return 403, {"error": "Permission denied, You don't have the power to revoke this role"}

            deleted, _ = CharacterRoles.objects.filter(character__character_id=character_id).delete()
            logger.info(f"Commander role revoked for character {character_id} by user {request.user}")
            return 200, {"status": "Commander role revoked"}
