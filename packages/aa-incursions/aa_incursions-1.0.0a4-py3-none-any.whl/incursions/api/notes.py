from datetime import datetime

from ninja import NinjaAPI, Schema

from django.utils.timezone import now

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.api.schema import CharacterSchema
from incursions.models.waitlist import CharacterNote


class NoteSchema(Schema):
    character: CharacterSchema
    note: str
    author: CharacterSchema | None
    logged_at: datetime


class NotesSchema(Schema):
    notes: list[NoteSchema] | None


class AddNoteSchema(Schema):
    character_id: int
    note: str


logger = get_extension_logger(__name__)

api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    NotesAPIEndpoints(api)


class NotesAPIEndpoints:

    tags = ["Notes"]

    def __init__(self, api: NinjaAPI) -> None:

        # These endpoints were fucky, the client expects an emtpy list if no notes are found
        # and not a 404 error, so we return an empty list instead of a 404

        @api.get("/notes", response={200: NotesSchema, 403: dict}, tags=self.tags)
        def list_notes(request, character_id: int):
            if not request.user.has_perm("incursions.notes_view"):
                return 403, {"error": "Permission denied"}

            try:
                character = EveCharacter.objects.get(character_id=character_id)
                notes = CharacterNote.objects.filter(character=character)
            except EveCharacter.DoesNotExist:
                return NotesSchema(notes=[])
            except CharacterNote.DoesNotExist:
                return NotesSchema(notes=[])

            return NotesSchema(notes=notes)

        @api.post("/notes/add", tags=self.tags)
        def add_note(request, payload: AddNoteSchema):
            if not request.user.has_perm("incursions.notes_manage"):
                return 403, {"error": "Permission denied"}

            try:
                character = EveCharacter.objects.get(character_id=payload.character_id)
                note = CharacterNote(
                    character=character,
                    note=payload.note,
                    author=get_main_character_from_user(request.user),
                    logged_at=now()
                )
                note.save()
            except EveCharacter.DoesNotExist:
                return {"status": "Character not found"}
            except CharacterNote.DoesNotExist:
                return {"status": "Note not found"}

            return {"status": "OK"}
