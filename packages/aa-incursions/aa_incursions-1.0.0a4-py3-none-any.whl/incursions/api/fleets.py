from corptools.models import EveItemType
from ninja import NinjaAPI, Schema

from django.http import Http404

from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema, HullSchema
from incursions.models.waitlist import (
    ActiveFleet, Fleet, FleetSquad, WaitlistCategory,
)
from incursions.providers import kick_all_fleet_members


class FleetStatusFleetSchema(Schema):
    id: int
    boss: CharacterSchema


class FleetStatusResponse(Schema):
    fleets : list[FleetStatusFleetSchema]


class FleetInfoSquadSchema(Schema):
    id: int
    name: str


class FleetInfoWingSchema(Schema):
    id: int
    name: str
    squads: list[FleetInfoSquadSchema]


class FleetInfoResponse(Schema):
    fleet_id: int
    wings: list[FleetInfoWingSchema]


class FleetMemberSchema(Schema):
    id: int
    name: str | None = None
    ship: HullSchema
    role: str


class FleetCompSquadMembersSchema(Schema):
    id: int
    name: str
    members: list[FleetMemberSchema]


class FleetCompWingSchema(Schema):
    id: int
    name: str
    squads: list[FleetCompSquadMembersSchema]
    member: FleetMemberSchema | None = None


class FleetCompResponse(Schema):
    wings: list[FleetCompWingSchema]
    id: int
    member: FleetMemberSchema | None = None


class FleetMembersMemberSchema(Schema):
    id: int
    name: str | None = None
    ship: HullSchema
    wl_category: str | None = None
    category: str | None = None
    role: str


class FleetMembersResponse(Schema):
    members: list[FleetMembersMemberSchema]


class RegisterRequest(Schema):
    character_id: int
    fleet_id: int
    assignments: dict[str, tuple[int, int]]


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    FleetAPIEndpoints(api)


class FleetAPIEndpoints:

    tags = ["Fleets"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/status", response={200: FleetStatusResponse, 403: dict}, tags=self.tags)
        def fleet_status(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            fleets = ActiveFleet.get_solo().fleet

            return FleetStatusResponse(fleets=fleets)

        @api.get("/info", response={200: FleetInfoResponse, 403: dict}, tags=self.tags)
        def fleet_info(request, boss_character_id: int):
            if not request.user.has_perm("incursions.waitlist_manage_waitlist"):
                return 403, {"error": "Permission denied"}

            fleet = ActiveFleet.get_solo().fleet
            fleet_wings = fleet.get_fleet_wings()

            wings: list[FleetInfoWingSchema] = []
            for wing in fleet_wings:
                wing.append(FleetInfoWingSchema(
                    id=wing.id,
                    name=wing.name,
                    squads=[FleetInfoSquadSchema(id=squad.id, name=squad.name) for squad in wing.squads]
                ))

            return FleetInfoResponse(fleet_id=fleet.pk, wings=wings)

        @api.get("/fleetcomp", response=FleetCompResponse, tags=self.tags)
        def fleet_composition(request, boss_character_id: int):
            if not request.user.has_perm("incursions.waitlist_fleet_view"):
                return 403, {"error": "Permission denied"}

            fleet = ActiveFleet.get_solo().fleet
            fleet_members = fleet.get_fleet_members()
            fleet_wings = fleet.get_fleet_wings()

            wings: list[FleetCompWingSchema] = []
            for wing in fleet_wings:
                squads: list[FleetMemberSchema] = []
                for fleet_member in fleet_members:
                    if fleet_member.wing_id == wing.id:
                        squads.append(FleetMemberSchema(
                            id=fleet_member.squad_id,
                            name=EveCharacter.objects.get(id=fleet_member.id).character_name,
                            ship=HullSchema(id=fleet_member.ship_type_id, name=EveItemType.objects.get(id=fleet_member.ship_type_id)),
                            role=fleet_member.role_name
                        ))
                wings.append(FleetCompWingSchema(id=wing.id, name=wing.name, squads=squads))

            return FleetCompResponse(wings=wings, id=fleet.pk)

        @api.get("/fleet/members/{character_id}", response=FleetMembersResponse, tags=self.tags)
        def fleet_members(request, character_id: int):
            if not request.user.has_perm("incursions.waitlist_fleet_view"):
                return 403, {"error": "Permission denied"}

            try:
                fleet = Fleet.objects.filter(boss_id=character_id).get()
            except Fleet.DoesNotExist:
                return Http404("Fleet not found")

            fleet_members = fleet.get_fleet_members()
            wings = fleet.get_fleet_wings()

            wing_array = {}
            for wing in wings:  # We have to build a lil cute lookup table here off the ESI data, since its not indexed on ID
                wing_array.update((wing.id, wing.name))

            members: list[FleetMembersMemberSchema] = []

            for fleet_member in fleet_members:
                member = FleetMembersMemberSchema(
                    id=fleet_member.character_id,
                    name=fleet_member.character_name,
                    ship=HullSchema(id=fleet_member.ship_type_id, name=EveItemType.objects.get(id=fleet_member.ship_type_id).name),
                    wl_category=FleetSquad.objects.get(squad_id=fleet_member.squad_id).category,
                    category=f"{wing_array[fleet_member.wing_id]} - {fleet_member.squad_name}",  # from ESI wing/squad name
                    role=fleet_member.role,
                )
                members.append(member)

            return FleetMembersResponse(members=members)

        @api.post("/register", tags=self.tags)
        def register_fleet(request, body: RegisterRequest):
            if not request.user.has_perm("incursions.waitlist_manage_waitlist"):
                return 403, {"error": "Permission denied"}

            fleet, created = Fleet.objects.get_or_create(
                pk=body.fleet_id,
                defaults={"boss": EveCharacter.objects.get(id=body.character_id)},
            )

            active_fleet = ActiveFleet.get_solo()
            active_fleet.fleet = fleet
            fleet.save()

            for category, (wing_id, squad_id) in body.assignments.items():
                FleetSquad.objects.update_or_create(
                    fleet=fleet,
                    category=WaitlistCategory.objects.get(name=category),
                    defaults={
                        "wing_id": wing_id,
                        "squad_id": squad_id,
                    },
                )

            return "OK"

        @api.post("/close", tags=self.tags)
        def close_fleet(request, boss_character_id: int):
            if not request.user.has_perm("incursions.waitlist_manage_waitlist"):
                return 403, {"error": "Permission denied"}

            fleet = ActiveFleet.get_solo().fleet
            count = kick_all_fleet_members(boss_character_id=fleet.boss.character_id, fleet_id=fleet.pk)
            return f"Kicked {count} Fleet Members"
