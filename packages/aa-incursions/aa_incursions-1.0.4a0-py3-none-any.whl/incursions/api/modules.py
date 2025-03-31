from corptools.models import EveItemType
from corptools.task_helpers.update_tasks import process_bulk_types_from_esi
from ninja import NinjaAPI, Schema

from allianceauth.services.hooks import get_extension_logger

from incursions.models.waitlist import ApprovedFitting


class ModuleSchema(Schema):
    name: str
    category: str
    slot: str | None


class ModuleInfoRequest(Schema):
    ids: list[int]


logger = get_extension_logger(__name__)
api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    ModulesAPIEndpoints(api)


class ModulesAPIEndpoints:

    tags = ["Modules"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.post("/module/info", response={200: dict[int, ModuleSchema], 403: dict}, tags=self.tags)
        def module_info(request, payload: ModuleInfoRequest):
            if not request.user.has_perm("incursions.basic_waitlist"):
                logger.warning(f"User {request.user} denied access to module info")
                return 403, {"error": "Permission denied"}

            logger.debug(f"Fetching module info for {len(payload.ids)} type IDs")
            process_bulk_types_from_esi(payload.ids)
            types = EveItemType.objects.select_related("group__category").filter(type_id__in=payload.ids)

            response = {
                type.type_id: ModuleSchema(
                    name=type.name,
                    category=type.group.category.name,
                    slot=None
                ) for type in types
            }
            logger.info(f"Returning module info for {len(response)} items to user {request.user}")
            return response

        @api.get("/module/preload", response={200: dict[int, ModuleSchema], 403: dict}, tags=self.tags)
        def preload(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                logger.warning(f"User {request.user} denied access to module preload")
                return 403, {"error": "Permission denied"}

            type_ids: list[int] = []
            for fit in ApprovedFitting.objects.only("dna"):
                for x in fit.dna.split(":"):
                    if x:
                        try:
                            type_ids.append(int(x.split(";")[0]))
                        except ValueError:
                            continue

            logger.debug(f"Preloading module info for {len(type_ids)} extracted type IDs")
            process_bulk_types_from_esi(type_ids)
            types = EveItemType.objects.select_related("group__category").filter(type_id__in=type_ids)

            response = {
                type.type_id: ModuleSchema(
                    name=type.name,
                    category=type.group.category.name if type.group and type.group.category else None,
                    slot=None
                ) for type in types
            }
            logger.info(f"Returning preloaded module info for {len(response)} items to user {request.user}")
            return response
