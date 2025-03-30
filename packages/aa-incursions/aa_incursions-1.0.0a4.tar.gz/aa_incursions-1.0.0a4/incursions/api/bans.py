from datetime import datetime, timezone

from ninja import NinjaAPI, Schema

from django.shortcuts import get_object_or_404

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import (
    AllianceSchema, CharacterSchema, CorporationSchema,
)
from incursions.models.waitlist import Ban


class PublicBanSchema(Schema):
    id: int
    entity_name: str
    entity_type: str
    entity_character: CharacterSchema | None
    entity_corporation: CorporationSchema | None
    entity_alliance: AllianceSchema | None
    issued_at: datetime
    issued_by: CharacterSchema | None
    public_reason: str | None
    revoked_at: datetime | None
    revoked_by: CharacterSchema | None


class BanSchema(Schema):
    id: int
    entity_name: str
    entity_type: str
    entity_character: CharacterSchema | None
    entity_corporation: CorporationSchema | None
    entity_alliance: AllianceSchema | None
    issued_at: datetime
    issued_by: CharacterSchema | None
    reason: str
    public_reason: str | None
    revoked_at: datetime | None
    revoked_by: CharacterSchema | None


class UpdateBanSchema(Schema):
    id: int
    entity_type: str
    entity_character: CharacterSchema | None
    entity_corporation: CorporationSchema | None
    entity_alliance: AllianceSchema | None
    reason: str
    public_reason: str | None
    revoked_at: datetime | None


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    BansAPIEndpoints(api)


class BansAPIEndpoints:

    tags = ["Bans"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/bans", response={200: list[BanSchema], 403: dict}, tags=self.tags)
        def list_bans(request):
            if not request.user.has_perm("incursions.view_bans"):
                return 403, {"error": "Permission denied"}

            return 200, Ban.objects.filter(revoked_at__isnull=True)

        @api.post("/bans", response={200: dict, 403: dict}, tags=self.tags)
        def create_ban(request, payload: UpdateBanSchema):
            if not request.user.has_perm("incursions.manage_bans"):
                return 403, {"error": "Permission denied"}

            Ban.objects.create(
                pk=payload.id,
                entity_type=payload.entity_type,
                issued_at=datetime.now(timezone.utc),
                issued_by=get_main_character_from_user(request.user),
                entity_character=payload.entity_character,
                entity_corporation=payload.entity_corporation,
                entity_alliance=payload.entity_alliance,
                reason=payload.reason,
                public_reason=payload.public_reason,
                revoked_at=payload.revoked_at,
                revoked_by=get_main_character_from_user(request.user) if payload.revoked_at is not None else None
            )
            return 200, {"status": "Ban created"}

        @api.get("/bans/{character_id}", response={200: list[BanSchema], 403: dict, 404: dict}, tags=self.tags)
        def character_history(request, character_id: int):
            if not request.user.has_perm("incursions.view_bans"):
                return 403, {"error": "Permission denied"}

            try:
                character = get_object_or_404(EveCharacter, character_id=character_id)
                bans = Ban.objects.filter(entity_character=character, entity_type="Character")
            except EveCharacter.DoesNotExist:
                return 404, {"error": "Character not found"}
            except Ban.DoesNotExist:
                return 404, {"error": "Ban not found"}

            return [BanSchema.from_orm(ban) for ban in bans]

        @api.patch("/bans/{ban_id}", response={200: dict, 403: dict, 404: dict}, tags=self.tags)
        def update_ban(request, ban_id: int, payload: BanSchema):
            if not request.user.has_perm("incursions.manage_bans"):
                return 403, {"error": "Permission denied"}

            try:
                ban = Ban.objects.get(id=ban_id)
            except Ban.DoesNotExist:
                return 404, {"error": "Ban not found"}

            ban.reason = payload.reason
            ban.public_reason = payload.public_reason
            ban.revoked_at = payload.revoked_at
            ban.revoked_by = get_main_character_from_user(request.user) if payload.revoked_at is not None else None
            ban.issued_by = get_main_character_from_user(request.user)
            ban.issued_at = datetime.now(timezone.utc)
            ban.save()

            return 200, {"status": "Ban updated"}

        @api.delete("/bans/{ban_id}", response={200: dict, 403: dict, 404: dict}, tags=self.tags)
        def revoke_ban(request, ban_id: int)  :
            if not request.user.has_perm("incursions.manage_bans"):
                return 403, {"error": "Permission denied"}

            try:
                ban = Ban.objects.get(id=ban_id)
            except Ban.DoesNotExist:
                return 404, {"error": "Ban not found"}

            ban.revoked_at = datetime.now(timezone.utc)
            ban.revoked_by = get_main_character_from_user(request.user)
            ban.save()
            return 200, {"status": "Ban revoked"}
