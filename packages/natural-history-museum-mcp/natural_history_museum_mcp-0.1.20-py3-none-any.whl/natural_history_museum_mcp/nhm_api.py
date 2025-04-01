import urllib.parse

from pyportal.constants import resources, URLs
import requests
from requests import Response
import logging

from natural_history_museum_mcp.constants import NhmTools

logger = logging.getLogger("NaturalHistoryMuseumAPI")
logger.setLevel(logging.DEBUG)


# Data contract
def data_object(records: list, msg: str | None, success: bool) -> dict:
    return {
        "records": records,
        "message": msg,
        "success": success,
        "number_of_records": len(records)
    }


def handle_response(response: Response) -> dict:
    if not response.ok:
        logger.error(response.reason)
        return data_object([],
                               f"Request to natural history museum API failed with status code {response.status_code}",
                               False)

    data = response.json()

    records = data["result"]["records"]

    if len(records) == 0:
        return data_object([], "Received OK from natural history museum API, but received no records. Try searching a different collection to find some records.", True)


    return data_object(records, None, True)

def get_resource_id(resource_type: NhmTools) -> str | None:
    match resource_type:
        case NhmTools.SPECIMEN_SEARCH:
            resource_id = resources.specimens
        case NhmTools.INDEX_LOTS_SEARCH:
            resource_id = resources.indexlots
        case _:
            resource_id = None

    return resource_id


def get_resource_by_search_term(resource_type: NhmTools, search_term: str, limit: int, offset: int) -> dict:

    resource_id = get_resource_id(resource_type)

    if resource_id is None:
        return data_object([], "Please provide a valid resource type.", False)

    url: str = f"{URLs.base_url}/action/datastore_search"
    params = {
        "resource_id": resource_id,
        "search_term": urllib.parse.quote(search_term),
        "limit": limit,
        "offset": offset
    }

    response = requests.get(url, params=params)

    return handle_response(response)
