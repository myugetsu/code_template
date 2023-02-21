from unittest.mock import Mock, patch
from app import create_app
from flask_test_helpers import FlackTestCase
import requests

from app.utils.service import get_users, get_user
from tests.mocks import get_free_port, start_mock_server


class TestMockServer(FlackTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_request_users_response(self):
        mock_users_url = "http://localhost:{port}/users".format(
            port=self.mock_server_port
        )

        users_response_list = [
            {
                "id": 1,
                "name": "Leanne Graham",
                "username": "Bret",
                "email": "Sincere@april.biz",
                "address": {
                    "street": "Kulas Light",
                    "suite": "Apt. 556",
                    "city": "Gwenborough",
                    "zipcode": "92998-3874",
                    "geo": {"lat": "-37.3159", "lng": "81.1496"},
                },
                "phone": "1-770-736-8031 x56442",
                "website": "hildegard.org",
                "company": {
                    "name": "Romaguera-Crona",
                    "catchPhrase": "Multi-layered client-server neural-net",
                    "bs": "harness real-time e-markets",
                },
            },
            {
                "id": 2,
                "name": "Ervin Howell",
                "username": "Antonette",
                "email": "Shanna@melissa.tv",
                "address": {
                    "street": "Victor Plains",
                    "suite": "Suite 879",
                    "city": "Wisokyburgh",
                    "zipcode": "90566-7771",
                    "geo": {"lat": "-43.9509", "lng": "-34.4618"},
                },
                "phone": "010-692-6593 x09125",
                "website": "anastasia.net",
                "company": {
                    "name": "Deckow-Crist",
                    "catchPhrase": "Proactive didactic contingency",
                    "bs": "synergize scalable supply-chains",
                },
            },
        ]

        # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
        with patch.dict("app.utils.service.__dict__", {"USERS_URL": mock_users_url}):
            response = get_users()

        self.assertDictContainsSubset(
            {"Content-Type": "application/json; charset=utf-8"}, response.headers
        )
        self.assertTrue(response.ok)
        self.assertListEqual(response.json(), users_response_list)

    def test_request_user_response(self):
        mock_user_url = "http://localhost:{port}/users/1".format(
            port=self.mock_server_port
        )

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
                "geo": {"lat": "-37.3159", "lng": "81.1496"},
            },
            "phone": "1-770-736-8031 x56442",
            "website": "hildegard.org",
            "company": {
                "name": "Romaguera-Crona",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets",
            },
        }
        # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
        with patch.dict("app.utils.service.__dict__", {"USER_URL": mock_user_url}):
            response = get_user(1)

        self.assertDictContainsSubset(
            {"Content-Type": "application/json; charset=utf-8"}, response.headers
        )

        self.assertTrue(response.ok)
        self.assertTrue(response.json(), user_response)
