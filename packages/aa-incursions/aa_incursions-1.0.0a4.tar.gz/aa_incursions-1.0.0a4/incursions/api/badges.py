from datetime import datetime

from ninja import NinjaAPI, Schema

from allianceauth.authentication.admin import User
from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema
from incursions.models.waitlist import Badge, CharacterBadges


class BadgeSchema(Schema):
    id: int
    name: str
    member_count: int
    exclude_badge_id: int | None


class CharacterBadgesSchema(Schema):
    badge: BadgeSchema
    character: CharacterSchema
    granted_by: CharacterSchema | None
    granted_at: datetime


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    BadgesAPIEndpoints(api)


class BadgesAPIEndpoints:

    tags = ["Badges"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/badges", response={200: list[BadgeSchema], 403: dict}, tags=self.tags)
        def list_badges(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            return 200, Badge.objects.all()

        @api.get("/badges/{badge_id}/members", response={200: list[CharacterBadgesSchema], 403: dict, 404: dict}, tags=self.tags)
        def get_badge_members(request, badge_id: int):
            if not request.user.has_perm("incursions.manage_badges"):
                return 403, {"error": "Permission denied"}

            try:
                characters = CharacterBadges.objects.filter(badge_id=badge_id).select_related("character", "granted_by")
            except Badge.DoesNotExist:
                return 404, {"error": "Badge not found"}

            return 200, characters

        @api.post("/badges/{badge_id}/members", response={200: dict, 403: dict, 404: dict} ,tags=self.tags)
        def assign_badge(request, badge_id: int, character_id: int):
            if not request.user.has_perm("incursions.manage_badges"):
                return 403, {"error": "Permission denied"}

            try:
                character = EveCharacter.objects.filter(character_id=character_id).get()
            except EveCharacter.DoesNotExist:
                return 404, {"error": "EveCharacter not found"}

            try:
                badge = Badge.objects.filter(id=badge_id).get()
            except Badge.DoesNotExist:
                return 404, {"error": "Badge not found"}

            if CharacterBadges.objects.filter(character=character, badge=badge).exists():
                return 400, {"error": "EveCharacter already has this badge"}

            CharacterBadges.objects.create(badge=badge, character=character, granted_by=get_main_character_from_user(request.user))
            return 200, {"status": "Badge assigned"}

        @api.delete("/badges/{badge_id}/members/{character_id}", response={200: dict, 403: dict, 404: dict}, tags=self.tags)
        def revoke_badge(request, badge_id: int, character_id: int):
            if not request.user.has_perm("incursions.manage_badges"):
                return 403, {"error": "Permission denied"}

            try:
                character = EveCharacter.objects.filter(character_id=character_id).get()
            except User.DoesNotExist:
                return 404, {"error": "User not found"}

            try:
                badge = Badge.objects.filter(id=badge_id).get()
            except Badge.DoesNotExist:
                return 404, {"error": "Badge not found"}

            if not CharacterBadges.objects.filter(character=character, badge=badge).exists():
                return 404, {"error": "Badge assignment not found"}

            deleted, _ = CharacterBadges.objects.filter(character=character, badge_id=badge_id).delete()
            return 200, {"status": "Badge revoked"}
