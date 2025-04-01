import unittest
import urllib
from unittest.mock import patch

from pyportal.constants import resources, URLs
from requests import Response
from starlette.status import HTTP_409_CONFLICT, HTTP_200_OK

from natural_history_museum_mcp import nhm_api
from natural_history_museum_mcp.constants import NhmTools
from natural_history_museum_mcp.nhm_api import data_object, get_resource_by_search_term


class NhmApiTests(unittest.TestCase):

    def test_data_object_returns_correct_shape(self):
        records = [1, 2, 3]
        message = "Test message"
        success = True

        result = data_object(records, message, success)

        expected_result = {
            "records": records,
            "message": message,
            "success": success,
            "number_of_records": len(records)
        }

        self.assertEqual(result, expected_result)

    def test_handle_response_returns_correctly_if_status_code_not_ok(self):
        failed_response: Response = Response()
        failed_response.status_code = HTTP_409_CONFLICT # An error code the NHM API can return

        result = nhm_api.handle_response(failed_response)

        expected_result_records = []
        expected_result_success = False

        self.assertEqual(result["records"], expected_result_records)
        self.assertEqual(result["success"], expected_result_success)

    def test_handle_response_returns_correctly_if_status_code_ok(self):
        successful_response: Response = Response()
        successful_response.status_code = HTTP_200_OK
        successful_response.json = lambda: {"result": {"records": [1, 2, 3]}}

        result = nhm_api.handle_response(successful_response)

        expected_result_records = [1, 2, 3]
        expected_result_success = True
        self.assertEqual(result["records"], expected_result_records)
        self.assertEqual(result["success"], expected_result_success)

    def test_get_resource_id_match_statement(self):
        expected_resource_id = resources.specimens
        index_lot_resource_id = resources.indexlots

        specimen_result = nhm_api.get_resource_id(NhmTools.SPECIMEN_SEARCH)

        self.assertEqual(specimen_result, expected_resource_id)

        index_lots_result = nhm_api.get_resource_id(NhmTools.INDEX_LOTS_SEARCH)

        self.assertEqual(index_lots_result, index_lot_resource_id)

    @patch("requests.get")
    @patch("natural_history_museum_mcp.nhm_api.handle_response")
    def test_get_resource_by_search_term_calls_requests_get_with_correct_params(self, mock_handle_response, mock_requests_get):
        resource_type = NhmTools.SPECIMEN_SEARCH
        search_term = "my term"
        limit = 10
        offset = 0

        mock_handle_response.return_value = {}
        base_url = f"{URLs.base_url}/action/datastore_search"
        result = get_resource_by_search_term(resource_type, search_term, limit, offset)

        mock_requests_get.assert_called_with(base_url, params={
            "resource_id": resources.specimens,
            "search_term": urllib.parse.quote(search_term),
            "limit": limit,
            "offset": offset
        })


if __name__ == '__main__':
    unittest.main()
