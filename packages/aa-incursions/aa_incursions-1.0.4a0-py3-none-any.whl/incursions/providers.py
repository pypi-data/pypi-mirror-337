from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi import __version__ as esi__version__
from esi.clients import EsiClientProvider
from esi.models import Token

from . import __version__

logger = get_extension_logger(__name__)

APP_INFO_TEXT = f"aa-incursions/{__version__} allianceauth/{aa__version__} django-esi/{esi__version__}"

"""
Swagger spec operations:
get_incursions
"""

esi = EsiClientProvider(app_info_text=APP_INFO_TEXT)


def get_incursions_incursions():
    operation = esi.client.Incursions.get_incursions()
    operation.request_config.also_return_response = True
    incursions, response = operation.results()
    return incursions, response


def get_fleet_wings(boss_character_id: int, fleet_id: int):
    required_scopes = ['esi-fleets.read_fleet.v1']
    token = Token.get_token(boss_character_id, required_scopes)

    result = esi.client.Fleets.get_fleets_fleet_id_wings(
        fleet_id=fleet_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_fleet_members(boss_character_id: int, fleet_id: int):
    required_scopes = ['esi-fleets.read_fleet.v1']
    token = Token.get_token(boss_character_id, required_scopes)

    result = esi.client.Fleets.get_fleets_fleet_id_members(
        fleet_id=fleet_id,
        token=token.valid_access_token()
    ).results()
    return result


def kick_fleet_member(boss_character_id:int, fleet_id:int, character_id:int):
    required_scopes = ['esi-fleets.write_fleet.v1']

    token = Token.get_token(boss_character_id, required_scopes)

    result = esi.client.Fleets.delete_fleets_fleet_id_members_member_id(
        fleet_id=fleet_id,
        member_id=character_id,
        token=token.valid_access_token()
    ).results()
    return result


def kick_all_fleet_members(boss_character_id:int, fleet_id:int) -> int:
    '''
    Helper function to kick all fleet members
    get_fleet_members() -> kick_fleet_member()
    '''
    fleet_members = get_fleet_members(boss_character_id, fleet_id)

    count = fleet_members.count()
    for fleet_member in fleet_members:
        kick_fleet_member(boss_character_id, fleet_id, fleet_member['character_id'])

    return count


def search_esi(character_id:int, search_string:str, search_categories:str, strict:bool = False):
    required_scopes = ['esi-search.search_structures.v1']
    token = Token.get_token(character_id, required_scopes)

    operation = esi.client.Search.get_search(
        character_id=character_id,
        categories=search_categories,
        search=search_string,
        strict=strict,
        token=token.valid_access_token()
    )
    operation.request_config.also_return_response = True
    result, response = operation.results()
    return result, response


def open_window_information(character_id:int, target_id:int):
    required_scopes = ['esi-ui.open_window.v1']
    token = Token.get_token(character_id, required_scopes)

    operation = esi.client.UserInterface.post_ui_openwindow_information(
        character_id=character_id,
        target_id=target_id,
        token=token.valid_access_token(),
    )
    operation.request_config.also_return_response = True
    result, response = operation.results()
    return result, response


def get_character_implants(character_id:int):
    required_scopes = ['esi-clones.read_implants.v1']
    token = Token.get_token(character_id, required_scopes)

    operation = esi.client.Clones.get_characters_character_id_implants(
        character_id=character_id,
        token=token.valid_access_token()
    )
    operation.request_config.also_return_response = True
    result, response = operation.results()
    return result, response


def invite_to_fleet(boss_character_id:int, fleet_id:int, character_id:int, squad_id:int | None, wing_id:int | None, role: str = "squad_member"):
    required_scopes = ['esi-fleets.write_fleet.v1']
    token = Token.get_token(boss_character_id, required_scopes)

    operation = esi.client.Fleets.post_fleets_fleet_id_members(
        fleet_id=fleet_id,
        invitation={"character_id": character_id, "role": role},
        squad_id=squad_id if squad_id else 0,
        wing_id=wing_id if wing_id else 0,
        token=token.valid_access_token()
    )
    operation.request_config.also_return_response = True
    result, response = operation.results()
    return result, response
