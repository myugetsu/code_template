from unittest import skipIf
from unittest.mock import Mock, patch
from app import create_app
from flask_test_helpers import FlackTestCase
from app.utils.service import get_users, get_user
import requests
from app.utils.constants import SKIP_TAGS


class TestRealServer(FlackTestCase):
    @skipIf('real' in SKIP_TAGS, 'Skipping tests that hit the real API server.')
    def test_request_response(self):
        response = get_users()

        self.assertDictContainsSubset(
            {'Content-Type': 'application/json; charset=utf-8'}, response.headers)
        self.assertTrue(response.ok)
        self.assertIsInstance(response.json(), list)

    @skipIf('real' in SKIP_TAGS, 'Skipping tests that hit the real API server.')
    def test_request_user_response(self):
        response = get_user(1)

        user_response = {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {
                    "street": "Kulas Light",
                    "suite": "Apt. 556",
                    "city": "Gwenborough",
                    "zipcode": "92998-3874",
                    "geo": {
                              "lat": "-37.3159",
                              "lng": "81.1496"
                    }
            },
            "phone": "1-770-736-8031 x56442",
            "website": "hildegard.org",
            "company": {
                "name": "Romaguera-Crona",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets"
            }
        }

        self.assertDictContainsSubset(
            {'Content-Type': 'application/json; charset=utf-8'}, response.headers)
        self.assertTrue(response.ok)
        self.assertEqual(response.json(), user_response)
