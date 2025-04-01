import json
import logging
import traceback

from mcp import stdio_server

from classes.tools import SpecimenSearch, IndexLotsSearch
from natural_history_museum_mcp import nhm_api
from mcp.server import Server
from mcp.types import Tool, TextContent

from natural_history_museum_mcp.constants import NhmTools, DEFAULT_LIMIT, DEFAULT_OFFSET

logger = logging.getLogger("NaturalHistoryMuseumMCPServer")
logger.setLevel(logging.INFO)



def search_specimens(search_term: str, limit: int=DEFAULT_LIMIT, offset=DEFAULT_OFFSET) -> str:
    logger.info(f"Starting specimen search for {search_term} with limit {limit}")
    nhm_api_result = nhm_api.get_resource_by_search_term(NhmTools.SPECIMEN_SEARCH, search_term, limit, offset)

    return json.dumps(nhm_api_result)

def search_index_lots(search_term: str, limit: int=DEFAULT_LIMIT, offset=DEFAULT_OFFSET) -> str:
    logger.info(f"Starting index lots search for {search_term} with limit {limit}")
    nhm_api_result = nhm_api.get_resource_by_search_term(NhmTools.INDEX_LOTS_SEARCH, search_term, limit, offset)

    return json.dumps(nhm_api_result)

async def serve():
    server = Server("nhm-api")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=NhmTools.SPECIMEN_SEARCH,
                description="Specimen search results from Natural History Museum",
                inputSchema=SpecimenSearch.model_json_schema(),
            ),
            Tool(
                name=NhmTools.INDEX_LOTS_SEARCH,
                description="Index lots search results from Natural History Museum",
                inputSchema=IndexLotsSearch.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:

        try:
            match name:
                case NhmTools.SPECIMEN_SEARCH:
                    search_term = arguments["search_term"]
                    limit = arguments["limit"] if "limit" in arguments else DEFAULT_LIMIT
                    offset = arguments["offset"] if "offset" in arguments else DEFAULT_OFFSET
                    result = search_specimens(search_term, limit=limit, offset=offset)
                    return [TextContent(
                        type="text",
                        text=result,
                    )]
                case NhmTools.INDEX_LOTS_SEARCH:
                    search_term = arguments["search_term"]
                    limit = arguments["limit"] if "limit" in arguments else DEFAULT_LIMIT
                    offset = arguments["offset"] if "offset" in arguments else DEFAULT_OFFSET
                    result = search_index_lots(search_term, limit=limit, offset=offset)
                    return [TextContent(
                        type="text",
                        text=result,
                    )]
                case _:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}, please specify a tool from the provided tools list"
                    )]
        except Exception as e:
            logger.error(traceback.print_exc())
            return [TextContent(
                type="text",
                text=f"Tool encountered an error {e}. Please report this to the github page."
            )]


    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)