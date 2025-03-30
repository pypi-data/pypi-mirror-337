from ninja import NinjaAPI, Schema

from allianceauth.services.hooks import get_extension_logger

from incursions.models.waitlist import (
    ApprovedFitting, WaitlistCategory, WaitlistCategoryRule,
)


class DNAFittingSchema(Schema):
    name: str
    dna: str
    tier: str
    implant_set: str


class FittingNoteSchema(Schema):
    name: str
    description: str


class FittingResponse(Schema):
    fittingdata: list[DNAFittingSchema] | None
    notes: list[FittingNoteSchema] | None
    logi_rules: list[int] | None  # Im hoping to deprecate this entirely, its dumb


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    FittingsAPIEndpoints(api)


class FittingsAPIEndpoints:

    tags = ["Fittings"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/fittings", response={200: FittingResponse, 403: dict, 404: dict}, tags=self.tags)
        def fittings(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            fittings = ApprovedFitting.objects.all()

            logi_category, _ = WaitlistCategory.objects.get_or_create(name="LOGI")  # Fuck you, have a logi category even if you dont want it

            return FittingResponse(
                fittingdata=fittings,
                notes=fittings,
                logi_rules=WaitlistCategoryRule.objects.filter(waitlist_category=logi_category).values_list("ship__type_id", flat=True)
            )
