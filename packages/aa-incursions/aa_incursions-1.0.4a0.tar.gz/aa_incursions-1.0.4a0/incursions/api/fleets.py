from corptools.models import EveItemType
from ninja import NinjaAPI, Schema

from django.db import transaction
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
    fleets: list[FleetStatusFleetSchema]


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
    wings: list[FleetCompWingSchema] | None
    id: int | None
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
                logger.warning(f"User {request.user} denied access to fleet status")
                return 403, {"error": "Permission denied"}

            fleet = ActiveFleet.get_solo().fleet
            logger.info(f"User {request.user} retrieved active fleet {fleet.pk}")
            return FleetStatusResponse(fleets=[fleet])

        @api.get("/info", response={200: FleetInfoResponse, 403: dict}, tags=self.tags)
        def fleet_info(request, boss_character_id: int):
            if not request.user.has_perm("incursions.waitlist_manage_waitlist"):
                logger.warning(f"User {request.user} denied access to fleet info")
                return 403, {"error": "Permission denied"}

            fleet = ActiveFleet.get_solo().fleet
            fleet_wings = fleet.get_fleet_wings()
            wings = [
                FleetInfoWingSchema(
                    id=wing.id,
                    name=wing.name,
                    squads=[FleetInfoSquadSchema(id=s.id, name=s.name) for s in wing.squads],
                )
                for wing in fleet_wings
            ]
            logger.info(f"Fleet info fetched for fleet {fleet.pk} by user {request.user}")
            return FleetInfoResponse(fleet_id=fleet.pk, wings=wings)

        @api.get("/fleetcomp", response=FleetCompResponse, tags=self.tags)
        def fleet_composition(request, boss_character_id: int):
            if not request.user.has_perm("incursions.waitlist_fleet_view"):
                logger.warning(f"User {request.user} denied access to fleet composition")
                return 403, {"error": "Permission denied"}

            active = ActiveFleet.get_solo()
            if not active:
                logger.info(f"No active fleet found for {request.user}")
                return FleetCompResponse(wings=[], id=None)

            fleet = active.fleet
            fleet_members = fleet.get_fleet_members()
            fleet_wings = fleet.get_fleet_wings()
            wings: list[FleetCompWingSchema] = []

            for wing in fleet_wings:
                squads: list[FleetMemberSchema] = []
                for fm in fleet_members:
                    if fm.wing_id == wing.id:
                        try:
                            character = EveCharacter.objects.only("character_name").get(pk=fm.character_id)
                            ship = EveItemType.objects.only("name").get(pk=fm.ship_type_id)
                        except (EveCharacter.DoesNotExist, EveItemType.DoesNotExist):
                            continue
                        squads.append(FleetMemberSchema(
                            id=fm.squad_id,
                            name=character.character_name,
                            ship=HullSchema(id=ship.pk, name=ship.name),
                            role=fm.role_name,
                        ))
                wings.append(FleetCompWingSchema(id=wing.id, name=wing.name, squads=squads))

            logger.info(f"Fleet composition fetched for fleet {fleet.pk} by user {request.user}")
            return FleetCompResponse(wings=wings, id=fleet.pk)

        @api.get("/fleet/members/{character_id}", response=FleetMembersResponse, tags=self.tags)
        def fleet_members(request, character_id: int):
            if not request.user.has_perm("incursions.waitlist_fleet_view"):
                logger.warning(f"User {request.user} denied access to fleet members for character {character_id}")
                return 403, {"error": "Permission denied"}

            try:
                fleet = Fleet.objects.select_related("boss").get(boss__character_id=character_id)
            except Fleet.DoesNotExist:
                logger.error(f"Fleet not found for character {character_id}")
                raise Http404("Fleet not found")

            fleet_members = fleet.get_fleet_members()
            wings = {w.id: w.name for w in fleet.get_fleet_wings()}
            members: list[FleetMembersMemberSchema] = []

            for fm in fleet_members:
                try:
                    char = EveCharacter.objects.only("character_name").get(pk=fm.character_id)
                    ship = EveItemType.objects.only("name").get(pk=fm.ship_type_id)
                    category = FleetSquad.objects.only("category").get(squad_id=fm.squad_id)
                except (EveCharacter.DoesNotExist, EveItemType.DoesNotExist, FleetSquad.DoesNotExist):
                    continue

                members.append(FleetMembersMemberSchema(
                    id=fm.character_id,
                    name=char.character_name,
                    ship=HullSchema(id=ship.pk, name=ship.name),
                    wl_category=category.category.name,
                    category=f"{wings.get(fm.wing_id)} - {fm.squad_name}",
                    role=fm.role,
                ))

            logger.info(f"Fleet members listed for fleet {fleet.pk} by user {request.user}")
            return FleetMembersResponse(members=members)

        @api.post("/register", tags=self.tags)
        def register_fleet(request, body: RegisterRequest):
            if not request.user.has_perm("incursions.waitlist_manage_waitlist"):
                logger.warning(f"User {request.user} denied fleet registration")
                return 403, {"error": "Permission denied"}

            with transaction.atomic():
                fleet, _ = Fleet.objects.select_for_update().get_or_create(
                    pk=body.fleet_id,
                    defaults={"boss": EveCharacter.objects.get(pk=body.character_id)},
                )

                active_fleet = ActiveFleet.get_solo()
                active_fleet.fleet = fleet
                active_fleet.save(update_fields=["fleet"])

                for category, (wing_id, squad_id) in body.assignments.items():
                    cat = WaitlistCategory.objects.get(name=category)
                    FleetSquad.objects.update_or_create(
                        fleet=fleet,
                        category=cat,
                        defaults={"wing_id": wing_id, "squad_id": squad_id},
                    )

            logger.info(f"Fleet {fleet.pk} registered and squads assigned by user {request.user}")
            return "OK"

        @api.post("/close", tags=self.tags)
        def close_fleet(request, boss_character_id: int):
            if not request.user.has_perm("incursions.waitlist_manage_waitlist"):
                logger.warning(f"User {request.user} denied closing fleet")
                return 403, {"error": "Permission denied"}

            fleet = ActiveFleet.get_solo().fleet
            count = kick_all_fleet_members(boss_character_id=fleet.boss.character_id, fleet_id=fleet.pk)
            logger.info(f"User {request.user} closed fleet {fleet.pk} and kicked {count} members")
            return f"Kicked {count} Fleet Members"
