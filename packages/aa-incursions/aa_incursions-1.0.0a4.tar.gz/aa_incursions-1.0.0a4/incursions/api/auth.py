from ninja import NinjaAPI, Schema

from allianceauth.framework.api.user import (
    get_all_characters_from_user, get_main_character_from_user,
)
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema


class WhoamiResponse(Schema):
    account_id: int
    access: list[str]
    characters: list[CharacterSchema]


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    AuthAPIEndpoints(api)


class AuthAPIEndpoints:

    tags = ["Auth"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/auth/whoami", response={200: WhoamiResponse, 404: dict}, tags=self.tags)
        def whoami(request):
            user = request.user

            try:
                main_character = get_main_character_from_user(user)
            except Exception:
                return 404, {"error": "User has no Main Character Set"}

            access_levels: list[str] = []
            for perm in user.get_all_permissions():
                if perm.startswith("incursions."):
                    access_levels.append(perm)

            return 200, WhoamiResponse(account_id=main_character.character_id, access=access_levels, characters=[CharacterSchema.from_orm(alt) for alt in get_all_characters_from_user(user)])

        @api.get("/auth/logout", tags=self.tags)
        def logout(request) -> dict:
            # DEPRECATE THIS
            return {"status": "Logged out"}

        @api.get("/auth/login_url", tags=self.tags)
        def login_url(request, alt: bool = False, fc: bool = False) -> dict:
            state = "alt" if alt else "normal"
            scopes = ["publicData", "skills.read_skills", "clones.read_implants"]
            if fc:
                scopes.extend(["fleets.read_fleet", "fleets.write_fleet", "ui.open_window", "search"])

            return {
                "login_url": f"https://login.eveonline.com/v2/oauth/authorize?response_type=code&redirect_uri=YOUR_REDIRECT_URI&client_id=YOUR_CLIENT_ID&scope={' '.join(scopes)}&state={state}"
            }
