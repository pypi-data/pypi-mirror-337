import json
from datetime import datetime

from corptools.models import EveItemType
from ninja import NinjaAPI, Schema

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.evecharacter import (
    get_main_character_from_evecharacter,
)
from allianceauth.framework.api.user import (
    get_all_characters_from_user, get_main_character_from_user,
)

from incursions.api.helpers.fittings import FittingParser
from incursions.api.helpers.sse import SSEClient, SSEEvent
from incursions.api.schema import CharacterSchema, HullSchema
from incursions.app_settings import SSE_SECRET, SSE_SITE_URL
from incursions.models.waitlist import (
    ActiveFleet, Fitting, FleetSquad, ImplantSet, Waitlist, WaitlistCategory,
    WaitlistCategoryRule, WaitlistEntry, WaitlistEntryFit,
)
from incursions.providers import get_character_implants, invite_to_fleet


class WaitlistEntryFitSchema(Schema):
    id: int
    approved: bool
    category: str
    dna: str
    hull: HullSchema | None = None
    character: CharacterSchema | None = None
    hours_in_fleet: int | None = None
    review_comment: str | None = None
    implants: list[int] | None = None
    fit_analysis: dict | None = None
    is_alt: bool
    messagexup: str | None = None
    tags: list[str] = []


class WaitlistEntrySchema(Schema):
    id: int
    character: CharacterSchema | None = None
    joined_at: datetime
    can_remove: bool
    fits: list[WaitlistEntryFitSchema]


class WaitlistResponse(Schema):
    open: bool
    waitlist: list[WaitlistEntrySchema] | None = None
    categories: list[str]


class XupRequest(Schema):
    waitlist_id: int
    character_id: int
    eft: str
    is_alt: bool
    messagexup: str


class RemoveXRequest(Schema):
    id: int


class RemoveFitRequest(Schema):
    id: int


class InviteRequest(Schema):
    id: int
    character_id: int


class ApproveRequest(Schema):
    id: int


class RejectRequest(Schema):
    id: int
    review_comment: str


class SetOpenRequest(Schema):
    open: bool
    waitlist_id: int


class EmptyWaitlistRequest(Schema):
    waitlist_id: int


class WaitlistUpdateSchema(Schema):
    waitlist_id: int


sse_client = SSEClient(SSE_SITE_URL, SSE_SECRET)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    WaitlistAPIEndpoints(api)


class WaitlistAPIEndpoints:

    tags = ["Waitlist"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/waitlist", response={200: WaitlistResponse, 403: dict, 404: dict}, tags=self.tags)
        def get_waitlist(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            waitlist = Waitlist.get_solo()
            request_main_character = get_main_character_from_user(request.user)

            # Permissions Fuckery
            # These flow downwards mostly, so if you have the top one, you have the bottom ones, done to avoid excessive OR statements later
            # Major Perms
            context_manager: bool = request.user.has_perm("incursions.waitlist_manage_waitlist")  # Manage Waitlist
            context_wl_approver: bool = context_manager or request.user.has_perm("incursions.waitlist_manage_waitlist_approve_fits")  # Approve Fits
            # Minor Perms
            context_implants: bool = context_wl_approver or request.user.has_perm("incursions.waitlist_implants_view")  # Implants
            context_stats: bool = context_wl_approver or request.user.has_perm("incursions.waitlist_stats_view")  # Stats
            # Minor-er Perms
            context_quantity: bool = context_wl_approver or request.user.has_perm("incursions.waitlist_context_a")  # Number of Pilots
            context_hull: bool = context_wl_approver or request.user.has_perm("incursions.waitlist_context_b")  # Ship Types
            context_time: bool = context_wl_approver or request.user.has_perm("incursions.waitlist_context_c")  # Time in Waitlist
            context_name: bool = context_wl_approver or request.user.has_perm("incursions.waitlist_context_d")  # Pilot Names

            if not waitlist.is_open:
                return WaitlistResponse(open=False, waitlist=None, categories=list(WaitlistCategory.objects.values_list("name", flat=True)))

            waitlist_entries = (WaitlistEntry.objects.filter(waitlist=waitlist).select_related("main_character").order_by("pk"))

            response_waitlist: list[WaitlistEntrySchema] = []

            for waitlist_entry in waitlist_entries:
                fits_data: list[WaitlistEntryFitSchema] = []
                is_self: bool = True if request_main_character == waitlist_entry.main_character else False
                for wl_fit in WaitlistEntryFit.objects.filter(waitlist_entry=waitlist_entry).select_related("fit", "fit__ship", "character", "category").order_by("pk"):

                    # ARIEL refactor fit checker to handle a list of fits, that way we can check a boxer immediately

                    if wl_fit.implant_set and wl_fit.implant_set.implants:
                        implants_list = json.loads(wl_fit.implant_set.implants)
                    else:
                        implants_list: list[str] = []

                    try:
                        fit_analysis_data = json.loads(wl_fit.fit_analysis)  # Can we redo this to just be comma seperated please ARIEL
                    except Exception:
                        fit_analysis_data = None

                    fits_data.append(WaitlistEntryFitSchema(
                        id=wl_fit.pk,
                        approved=wl_fit.approved,
                        category=wl_fit.category.name,
                        hull=HullSchema(
                            id=wl_fit.fit.ship.type_id if is_self or context_wl_approver or context_hull else 0,
                            name=wl_fit.fit.ship.name if is_self or context_wl_approver or context_hull else "Hidden",
                        ),
                        character=CharacterSchema(
                            character_name=wl_fit.character.character_name if is_self or context_name else "Hidden",
                            character_id=wl_fit.character.character_id if is_self or context_name else 0
                        ),
                        hours_in_fleet=wl_fit.cached_time_in_fleet // 3600 if context_stats else 0,
                        review_comment=wl_fit.review_comment if is_self or context_wl_approver else None,
                        dna=wl_fit.fit.dna if is_self or context_wl_approver else "",
                        implants=implants_list if is_self or context_wl_approver or context_implants else [],
                        fit_analysis=fit_analysis_data if is_self or context_wl_approver or context_implants else None,
                        is_alt=wl_fit.is_alt if is_self or context_wl_approver or context_quantity else False,
                        messagexup=wl_fit.messagexup if is_self or context_wl_approver else None,
                        tags=[tag for tag in wl_fit.tags.split(",") if tag],
                    ))

                    # End fits

                response_waitlist.append(WaitlistEntrySchema(
                    id=waitlist_entry.pk,
                    character=CharacterSchema(
                        character_name=waitlist_entry.main_character.character_name if is_self or context_name else "Hidden",
                        character_id=waitlist_entry.main_character.character_id if is_self or context_name else 0
                    ),
                    joined_at=waitlist_entry.joined_at if is_self or context_time else now(),
                    can_remove=True if is_self or context_wl_approver else False,
                    fits=fits_data
                ))

            return WaitlistResponse(open=True, waitlist=response_waitlist, categories=list(WaitlistCategory.objects.values_list("name", flat=True)))

        @api.post("/waitlist/xup", response={200: dict, 403: dict, 404: dict}, tags=self.tags)
        def xup(request, payload: XupRequest):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return 403, {"error": "Permission denied"}

            waitlist = get_object_or_404(Waitlist, id=payload.waitlist_id)
            character = get_object_or_404(EveCharacter, character_id=payload.character_id)

            fitting_parser = FittingParser.from_eft(payload.eft)

            # ARIEL refactor fit checker to handle a list of fits, that way we can check a boxer immediately

            fitting, _ = Fitting.objects.get_or_create(
                dna=fitting_parser.to_dna(),
                ship=EveItemType.objects.get_or_create_from_esi(fitting_parser.hull)[0]
            )
            implant_set, _ = ImplantSet.objects.get_or_create(
                implants=list(get_character_implants(character.character_id)[0])
            )
            try:
                waitlist_category = WaitlistCategoryRule.objects.get(ship=fitting.ship).waitlist_category
            except WaitlistCategoryRule.DoesNotExist:
                # Its possible someone hasn't set up a category rule for this ship yet
                # It's also possible they never loaded out preset Categories
                waitlist_category, _ = WaitlistCategory.objects.get_or_create(name="Other")

            waitlist_entry, _ = WaitlistEntry.objects.get_or_create(
                main_character=character,
                waitlist=waitlist,
                defaults={
                    "joined_at": now(),
                }
            )

            new_fit = WaitlistEntryFit.objects.create(
                character=character,
                waitlist=waitlist,
                fit=fitting,
                implant_set=implant_set,
                approved=False,
                tags="",
                category=waitlist_category,
                cached_time_in_fleet=0,
                is_alt=payload.is_alt,
                messagexup=payload.messagexup
            )

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=waitlist.pk).model_dump())])

            # ARIEL refactor into multiple fleets
            sse_client.submit([SSEEvent.new(
                topic=f"account;{get_main_character_from_evecharacter(ActiveFleet.get_solo().fleet.boss.character_id).character_id}",
                event="message",
                data="New x-up in waitlist",
            )])
            return 200, {"status": "X-up recorded", "fit_id": new_fit.pk}

        @api.post("/waitlist/remove_x", response={200: dict, 403: dict}, tags=self.tags)
        def remove_x(request, payload: RemoveXRequest):
            waitlist_entry = get_object_or_404(WaitlistEntry, id=payload.id)
            waitlist = get_object_or_404(Waitlist, id=waitlist_entry.waitlist.pk)

            if not (waitlist_entry.main_character is get_main_character_from_user(request.user) or request.user.has_perm("incursions.manage_waitlist")):
                return 403, {"error": "Permission denied"}

            waitlist_entry.delete()

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=waitlist.pk).model_dump())])
            return 200, {"status": "Waitlist X-Up removed"}

        @api.post("/waitlist/remove_fit", response={200: dict, 403: dict}, tags=self.tags)
        def remove_fit(request, payload: RemoveFitRequest):
            entry = get_object_or_404(WaitlistEntryFit, id=payload.id)
            waitlist_entry = get_object_or_404(WaitlistEntry, id=entry.waitlist_entry.pk)
            waitlist = get_object_or_404(Waitlist, id=waitlist_entry.waitlist.pk)

            if not (entry.character in get_all_characters_from_user(request.user) or request.user.has_perm("incursions.manage_waitlist")):
                return 403, {"error": "Permission denied"}

            entry.delete()

            if WaitlistEntryFit.objects.filter(waitlist=waitlist_entry).count() == 0:
                # The User has no more fits on the waitlist, so we can remove them from the waitlist
                waitlist_entry.delete()

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=waitlist.pk).model_dump())])
            return 200, {"status": "Waitlist X-Up Fit removed"}

        @api.post("/waitlist/invite", tags=self.tags)
        def invite(request, payload: InviteRequest):
            if not request.user.has_perm("incursions.manage_waitlist"):
                return 403, {"error": "Permission denied"}

            active_fleet = ActiveFleet.get_solo()
            waitlist_entry_fit = get_object_or_404(WaitlistEntryFit, pk=payload.id)

            for waitlist_category in WaitlistCategory.objects.all():
                if waitlist_category.name == waitlist_entry_fit.category:
                    squad_id = FleetSquad.objects.get(fleet=active_fleet.fleet, name=waitlist_category.name).squad_id
                    wing_id = FleetSquad.objects.get(fleet=active_fleet.fleet, name=waitlist_category.name).wing_id

            invite_to_fleet(
                boss_character_id=active_fleet.fleet.boss.character_id,
                fleet_id=active_fleet.fleet.pk,
                character_id=payload.character_id,
                squad_id=squad_id if squad_id else None,
                wing_id=wing_id if wing_id else None,
                role="squad_member"
            )

            sse_client.submit([SSEEvent.new(
                topic=f"account;{get_main_character_from_evecharacter(waitlist_entry_fit.character).character_id}",
                event="wakeup",
                data=f"{active_fleet.fleet.boss.character_name} has invited your {waitlist_entry_fit.fit.ship.name} to fleet.",
            )])

            return {"status": f"Character {payload.character_id} invited to waitlist entry {payload.id}"}

        @api.post("/waitlist/approve", tags=self.tags)
        def approve_fit(request, payload: ApproveRequest):
            if not (request.user.has_perm("incursions.manage_waitlist") or request.user.has_perm("incursions.waitlist_manage_waitlist_approve_fits")):
                return 403, {"error": "Permission denied"}

            fit = get_object_or_404(WaitlistEntryFit, id=payload.id)
            fit.approved = True
            fit.save()

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=fit.waitlist_entry.pk).model_dump())])
            return {"status": f"Fit {fit.pk} approved"}

        @api.post("/waitlist/reject", tags=self.tags)
        def reject_fit(request, payload: RejectRequest):
            if not (request.user.has_perm("incursions.manage_waitlist") or request.user.has_perm("incursions.waitlist_manage_waitlist_approve_fits")):
                return 403, {"error": "Permission denied"}

            fit = get_object_or_404(WaitlistEntryFit, id=payload.id)
            fit.approved = False
            fit.review_comment = payload.review_comment
            fit.save()

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=fit.waitlist_entry.pk).model_dump())])
            return 200, {"status": f"Fit {fit.pk} rejected"}

        @api.post("/waitlist/set_open", tags=self.tags)
        def set_open(request, payload: SetOpenRequest):
            if not request.user.has_perm("incursions.manage_waitlist"):
                return 403, {"error": "Permission denied"}

            w = get_object_or_404(Waitlist, id=payload.waitlist_id)
            w.is_open = payload.open
            w.save()

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="open", data=WaitlistUpdateSchema(waitlist_id=w.pk).model_dump())])
            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=w.pk).model_dump())])
            return 200, {"status": "OK"}

        @api.post("/waitlist/empty", tags=self.tags)
        def empty_waitlist(request, payload: EmptyWaitlistRequest):
            if not request.user.has_perm("incursions.manage_waitlist"):
                return 403, {"error": "Permission denied"}

            w = get_object_or_404(Waitlist, id=payload.waitlist_id)
            WaitlistEntryFit.objects.filter(waitlist=w).delete()

            sse_client.submit([SSEEvent.new_json(topic="waitlist", event="waitlist_update", data=WaitlistUpdateSchema(waitlist_id=w.pk).model_dump())])
            return 200, {"status": "OK"}
