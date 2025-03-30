from corptools.models import EveItemType
from ninja import NinjaAPI, Schema

from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema, HullSchema
from incursions.api.skills import EVECATEGORY_SKILLS, RELEVANT_SKILL_GROUPS
from incursions.models.waitlist import (
    FittingHistory, FleetActivity, SkillHistory,
)

api = NinjaAPI()


class ActivityEntrySchema(Schema):
    hull: HullSchema
    logged_at: int
    time_in_fleet: int


class ActivitySummaryEntrySchema(Schema):
    hull: HullSchema
    time_in_fleet: int


class ActivityResponse(Schema):
    activity: list[ActivityEntrySchema]
    summary: list[ActivitySummaryEntrySchema]


class FleetCompEntrySchema(Schema):
    hull: HullSchema
    character: CharacterSchema
    logged_at: int
    time_in_fleet: int
    is_boss: bool


class FleetCompResponse(Schema):
    fleets: dict[int, list[FleetCompEntrySchema]]


class XupHistoryLineSchema(Schema):
    logged_at: int
    dna: str
    implants: list[int]
    hull: HullSchema


class XupHistorySchema(Schema):
    xups: list[XupHistoryLineSchema]


class SkillHistoryResponseLineSchema(Schema):
    skill_id: int
    old_level: int
    new_level: int
    logged_at: int
    name: str


class SkillHistoryResponse(Schema):
    history: list[SkillHistoryResponseLineSchema]
    ids: dict[str, int]


logger = get_extension_logger(__name__)


def setup(api: NinjaAPI) -> None:
    HistoryAPIEndpoints(api)


class HistoryAPIEndpoints:

    tags = ["History"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/api/history/fleet", response=ActivityResponse, tags=self.tags)
        def fleet_history(request, character_id: int):
            if not request.user.has_perm("incursions.waitlist_history_view"):
                return 403, {"error": "Permission denied"}

            activities = FleetActivity.objects.filter(character_id=character_id).order_by("-first_seen")
            time_by_hull: dict[int, int] = {}
            activity_entries: list[ActivityEntrySchema] = []

            for act in activities:
                time_in_fleet = act.last_seen - act.first_seen
                hull_id = act.ship.type_id  # Assuming "hull" is an integer field on FleetActivity.
                time_by_hull[hull_id] = time_by_hull.get(hull_id, 0) + time_in_fleet

                activity_entries.append(ActivityEntrySchema(
                    hull=HullSchema(id=hull_id, name=EveItemType.objects.get(id=hull_id).name),
                    logged_at=act.first_seen,
                    time_in_fleet=time_in_fleet,
                ))

            summary_entries: list[ActivitySummaryEntrySchema] = []
            for hull_id, total_time in time_by_hull.items():
                summary_entries.append(ActivitySummaryEntrySchema(
                    hull=HullSchema(id=hull_id, name=EveItemType.objects.get(id=hull_id).name),
                    time_in_fleet=total_time,
                ))
            summary_entries.sort(key=lambda s: s.time_in_fleet, reverse=True)

            return {
                "activity": activity_entries,
                "summary": summary_entries,
            }

        @api.get("/api/history/fleet-comp", response=FleetCompResponse, tags=self.tags)
        def fleet_comp(request, time: int):
            if not request.user.has_perm("incursions.waitlist_history_view"):
                return 403, {"error": "Permission denied"}

            comp_entries = FleetActivity.objects.select_related("character").filter(
                first_seen__lte=time,
                last_seen__gte=time,
            )

            fleets: dict[int, list[FleetCompEntrySchema]] = {}
            for entry in comp_entries:
                fleet_id = entry.fleet_id  # Adjust field name if necessary.
                fleet_entry = FleetCompEntrySchema(
                    hull=HullSchema.from_orm(entry.ship),
                    character=CharacterSchema.from_orm(entry.character),
                    logged_at=entry.first_seen,
                    time_in_fleet=entry.last_seen - entry.first_seen,
                    is_boss=True if entry.fleet.boss == entry.character else False,
                )
                fleets.setdefault(fleet_id, []).append(fleet_entry)

            return {"fleets": fleets}

        @api.get("/api/history/xup", response=XupHistorySchema, tags=self.tags)
        def xup_history(request, character_id: int):
            if not request.user.has_perm("incursions.waitlist_history_view"):
                return 403, {"error": "Permission denied"}

            xup_lines: list[XupHistoryLineSchema] = []
            for xup in FittingHistory.objects.filter(character_id=character_id).order_by("-id"):
                try:
                    implants_list = [int(i) for i in xup.implant_set.implants.split(':') if i]
                except Exception:
                    implants_list: list[int] = []
                hull_schema = HullSchema().from_orm(xup.fit.ship)
                xup_lines.append(XupHistoryLineSchema(
                    logged_at=xup.logged_at,
                    dna=xup.fit.dna,
                    implants=implants_list,
                    hull=hull_schema,
                ))

            return {"xups": xup_lines}

        @api.get("/api/history/skills", response=SkillHistoryResponse, tags=self.tags)
        def skill_history(request, character_id: int):
            if not request.user.has_perm("incursions.waitlist_history_view"):
                return 403, {"error": "Permission denied"}

            history_list: list[SkillHistoryResponseLineSchema] = []
            for skill in SkillHistory.objects.filter(character_id=character_id).order_by("-id"):
                if skill.skill.group.category.category_id in RELEVANT_SKILL_GROUPS:
                    history_list.append(SkillHistoryResponseLineSchema(
                        skill_id=skill.skill.type_id,
                        old_level=skill.old_level,
                        new_level=skill.new_level,
                        logged_at=skill.logged_at,
                        name=skill.skill.name,
                    ))

            return {
                "history": history_list,
                "ids": {skill.name: skill.type_id for skill in EveItemType.objects.filter(group__category_id=EVECATEGORY_SKILLS)},
            }
