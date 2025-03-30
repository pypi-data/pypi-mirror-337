from ninja import NinjaAPI, Schema

from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema
from incursions.providers import search_esi


class SearchResponse(Schema):
    query: str
    results: list[CharacterSchema]


class EsiSearchRequest(Schema):
    search: str
    category: str = "character"
    strict: bool = False


class EsiSearchResponse(Schema):
    character: list[int] | None = None
    corporation: list[int] | None = None
    alliance: list[int] | None = None


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    SearchAPIEndpoints(api)


class SearchAPIEndpoints:

    tags = ["Search"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/search", response={200: SearchResponse, 403: dict}, tags=self.tags)
        def query(request, query: str):
            if not request.user.has_perm("incursions.waitlist_search"):
                return 403, {"error": "Permission denied"}

            return SearchResponse(query=query, results=list(EveCharacter.objects.filter(character_name__icontains=query)))

        @api.post("/search", response={200: list[int], 403: dict}, tags=self.tags)
        def esi_search(request, payload: EsiSearchRequest):
            if not request.user.has_perm("incursions.waitlist_esi_search"):
                return 403, {"error": "Permission denied"}

            if payload.category == "character":
                result, _ = search_esi(request.user.main_character.character_id, payload.search, payload.category, payload.strict)

                return [x for x in result[payload.category]]
