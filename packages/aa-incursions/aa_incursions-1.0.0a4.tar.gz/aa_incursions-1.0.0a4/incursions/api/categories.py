from ninja import NinjaAPI, Schema

from allianceauth.services.hooks import get_extension_logger

from incursions.models.waitlist import WaitlistCategory


class CategorySchema(Schema):
    id: int
    name: str


api = NinjaAPI()


logger = get_extension_logger(__name__)


def setup(api: NinjaAPI) -> None:
    CategoriesAPIEndpoints(api)


class CategoriesAPIEndpoints:

    tags = ["Categories"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/categories", response={200: list[CategorySchema], 403: dict}, tags=self.tags)
        def list_categories(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            return 200, [CategorySchema.from_orm(cat) for cat in WaitlistCategory.objects.all()]
