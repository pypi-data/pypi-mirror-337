import msgpack
from ninja import NinjaAPI

from django.shortcuts import redirect

from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions import app_settings
from incursions.api.helpers.sse import SSEClient

logger = get_extension_logger(__name__)
api = NinjaAPI()

VERSION_BYTE = b'\xBA'


def setup(api: NinjaAPI) -> None:
    SSEAPIEndpoints(api)


class SSEAPIEndpoints:

    tags = ["SSE"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/sse/stream", tags=self.tags)
        def sse_stream(request):
            if not request.user.has_perm("incursions.basic_waitlist"):
                return {"error": "Permission denied"}

            topics = ["announcements", "waitlist", f"account;{get_main_character_from_user(request.user).character_id}"]
            if request.user.is_authenticated and request.user.has_perm("waitlist_fleet_view"):
                topics.append("fleet_comp")

            payload_dict = {"topics": topics}
            payload_bytes: bytes = msgpack.packb(payload_dict, use_bin_type=True)

            token = SSEClient(app_settings.SSE_SITE_URL, app_settings.SSE_SECRET).branca_encode(payload=payload_bytes)

            sse_url = f"{app_settings.SSE_SITE_URL}/events?token={token}"
            return redirect(sse_url)
