from enum import Enum

from ninja import Field, NinjaAPI, Schema

from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import HullSchema


class SkillLevelEnum(str, Enum):
    I = "I"  # noqa: E741
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"


class BaseSkillPlanLevel(Schema):
    type: str


class FitLevel(Schema):
    type: str = "fit"
    hull: str
    fit: str


class SkillsLevel(Schema):
    type: str = "skills"
    from_: str = Field(..., alias="from")
    tier: str


class SkillLevelEntry(Schema):
    type: str = "skill"
    from_: str = Field(..., alias="from")
    level: SkillLevelEnum


class TankLevel(Schema):
    type: str = "tank"
    from_: str = Field(..., alias="from")


class SkillPlanSchema(Schema):
    name: str
    description: str
    alpha: bool = False
    plan: list[FitLevel | SkillsLevel | SkillLevelEntry | TankLevel] = Field(..., discriminator="type")


class SkillPlansResponsePlanSchema(Schema):
    source: str
    levels: list[tuple[int, int]]
    ships: list[HullSchema]


class SkillPlansResponse(Schema):
    plans: list[SkillPlansResponsePlanSchema]


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    SkillPlansAPIEndpoints(api)


class SkillPlansAPIEndpoints:

    tags = ["Skill Plans"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/skills/plans", response={200: SkillPlansResponse, 403: dict}, tags=self.tags)
        def get_skill_plans(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            plans: list[SkillPlansResponsePlanSchema] = []
            plans.append(SkillPlansResponsePlanSchema(
                source=None,
                level=None,
                ships=None,
            ))

            return SkillPlansResponse(plans=plans)
