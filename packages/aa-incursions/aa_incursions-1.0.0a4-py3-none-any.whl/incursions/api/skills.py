from corptools.models import CharacterAudit, EveItemGroup, EveItemType, Skill
from ninja import NinjaAPI, Schema

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_all_characters_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.models.waitlist import ApprovedSkills

SKILL_GROUP_GUNNERY = 255
SKILL_GROUP_MISSILES = 256
SKILL_GROUP_SPACESHIP_COMMAND = 257
SKILL_GROUP_ARMOR = 1210
SKILL_GROUP_RIGGING = 269
SKILL_GROUP_SHIELDS = 1209
SKILL_GROUP_DRONES = 273
SKILL_GROUP_NEURAL_ENHANCEMENT = 1220

EVECATEGORY_SKILLS = 16

RELEVANT_SKILL_GROUPS = [SKILL_GROUP_ARMOR, SKILL_GROUP_DRONES, SKILL_GROUP_GUNNERY, SKILL_GROUP_MISSILES, SKILL_GROUP_NEURAL_ENHANCEMENT, SKILL_GROUP_RIGGING, SKILL_GROUP_SHIELDS, SKILL_GROUP_SPACESHIP_COMMAND]


class SkillTierSchema(Schema):
    min: int | None
    elite: int | None
    gold: int | None


class SkillsResponse(Schema):
    current: dict[int, int]
    ids: dict[str, int]
    categories: dict[str, list[int]]
    requirements: dict[str, dict[int, SkillTierSchema]]


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    SkillsAPIEndpoints(api)


class SkillsAPIEndpoints:

    tags = ["Skills"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/skills/{character_id}", response={200: SkillsResponse, 403: dict}, tags=self.tags)
        def list_skills(request: HttpRequest, character_id: int):
            character = get_object_or_404(EveCharacter, character_id=character_id)
            if not (character in get_all_characters_from_user(request.user) or request.user.has_perm("incursions.skills_view")):
                return 403, {"error": "Permission denied"}

            character_audit = get_object_or_404(CharacterAudit, character=character)
            skills = Skill.objects.filter(character=character_audit, skill_name__group_id__in=RELEVANT_SKILL_GROUPS).select_related("skill_name")

            requirements = {}
            for hullskills in ApprovedSkills.objects.all():

                requirements.update({hullskills.hull.name: {x.skill.type_id: SkillTierSchema.from_orm(x) for x in hullskills.skill_checks.all()}})

            return SkillsResponse(
                current={skill.skill_name.type_id: skill.trained_skill_level for skill in skills},
                ids={skill.name: skill.type_id for skill in EveItemType.objects.filter(group__category_id=EVECATEGORY_SKILLS)},
                categories={group.name: list(EveItemType.objects.filter(group=group).values_list("type_id", flat=True)) for group in EveItemGroup.objects.filter(group_id__in=RELEVANT_SKILL_GROUPS)},
                requirements=requirements,
            )
