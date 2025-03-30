from datetime import datetime, timezone

from ninja import NinjaAPI, Schema

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

# Hey Ariel, A commander is just a Character with Roles ++


class CommandersAPIEndpoints:

    tags = ["Commanders"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/commanders", response={200: CommanderListSchema, 403: dict}, tags=self.tags)
        def list_commanders(request):
            if not request.user.has_perm("incursions.view_commanders"):
                return 403, {"error": "Permission denied"}

            return 200, CommanderListSchema(commanders=CharacterRoles.objects.all(), filters=Role.objects.all())

        @api.post("/commanders", response={200: dict, 400:dict, 403: dict, 404: dict}, tags=self.tags)
        def assign_commander(request, payload: RequestPayload):
            if not request.user.has_perm("incursions.manage_commanders"):
                return 403, {"error": "Permission denied"}

            character = get_object_or_404(EveCharacter, character_id=payload.character_id)
            if CharacterRoles.objects.filter(character=character).exists():
                return 400, {"error": "Character already has a role"}

            role = get_object_or_404(Role, name=payload.role)
            if role.power > CharacterRoles.objects.get(character=get_main_character_from_user(request.user)).role.power:
                return 403, {"error": "Permission denied, You dont have the power to assign this role"}

            commander = CharacterRoles.objects.create(
                character=character,
                role=role,
                granted_by=get_main_character_from_user(request.user),
                granted_at=datetime.now(timezone.utc)
            )
            return 200, {"status": "Commander assigned", "id": commander.pk}

        @api.get("/commanders/roles", response={200: list[str], 403: dict}, tags=self.tags)
        def assignable_roles(request):
            if not request.user.has_perm("incursions.view_commanders"):
                return 403, {"error": "Permission denied"}

            return 200, list(Role.objects.all().values_list("name", flat=True))

        @api.get("/commanders/{character_id}", response={200: str, 403: dict}, tags=self.tags)
        def lookup_commander(request, character_id: int):
            if not request.user.has_perm("incursions.view_commanders"):
                return 403, {"error": "Permission denied"}

            character = get_object_or_404(EveCharacter, character_id=character_id)
            character_role = get_object_or_404(CharacterRoles, character=character)

            return 200, character_role.role.name

        @api.delete("/commanders/{character_id}", response={200: dict, 403: dict, 404: dict}, tags=self.tags)
        def revoke_commander(request, character_id: int):
            if not request.user.has_perm("incursions.manage_commanders"):
                return 403, {"error": "Permission denied"}

            character = get_object_or_404(EveCharacter, character_id=character_id)
            commander = get_object_or_404(CharacterRoles, character=character)

            if commander.role.power > CharacterRoles.objects.get(character=get_main_character_from_user(request.user)).role.power:
                return 403, {"error": "Permission denied, You dont have the power to rovoke this role"}

            try:
                deleted, _ = CharacterRoles.objects.filter(character_id=character_id).delete()
            except CharacterRoles.DoesNotExist:
                return 404, {"error": "Commander role not found"}

            return 200, {"status": "Commander role revoked"}
