from unittest import skipIf
from unittest.mock import Mock, patch
from app import create_app
from flask_test_helpers import FlackTestCase
from app.utils.service import get_todos, get_uncompleted_todos
import requests
from app.utils.constants import SKIP_TAGS


class TestIntegration(FlackTestCase):
    @skipIf("real" in SKIP_TAGS, "Skipping tests that hit the real API server.")
    def test_integration_contract(self):
        # Call the service to hit the actual API.
        actual = get_todos()
        actual_keys = actual.json().pop().keys()

        # Call the service to hit the mocked API.
        with patch("app.utils.service.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = [
                {"userId": 1, "id": 1, "title": "Make the bed", "completed": False}
            ]

            mocked = get_todos()
            mocked_keys = mocked.json().pop().keys()

        # An object from the actual API and an object from the mocked API should have
        # the same data structure.
        self.assertListEqual(list(actual_keys), list(mocked_keys))


class TestToDo(FlackTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_get_patcher = patch("app.utils.service.requests.get")
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_get_patcher.stop()

    def test_getting_todos_when_response_is_ok(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value.ok = True

        todos = [{"userId": 1, "id": 1,
                  "title": "Make the bed", "completed": False}]

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.json.return_value = todos

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertListEqual(response.json(), todos)

    def test_getting_todos_when_response_is_not_ok(self):
        # Configure the mock to not return a response with an OK status code.
        self.mock_get.return_value.ok = False

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the response contains an error, I should get no todos.
        self.assertIsNone(response)


class TestUncompletedTodos(FlackTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_get_todos_patcher = patch("app.utils.service.get_todos")
        cls.mock_get_todos = cls.mock_get_todos_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_get_todos_patcher.stop()

    def test_getting_uncompleted_todos_when_todos_is_not_none(self):
        todo1 = {"userId": 1, "id": 1,
                 "title": "Make the bed", "completed": False}
        todo2 = {"userId": 2, "id": 2,
                 "title": "Walk the dog", "completed": True}

        # Configure mock to return a response with a JSON-serialized list of todos.
        self.mock_get_todos.return_value = Mock()
        self.mock_get_todos.return_value.json.return_value = [todo1, todo2]

        # Call the service, which will get a list of todos filtered on completed.
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called.
        self.assertTrue(self.mock_get_todos.called)

        # Confirm that the expected filtered list of todos was returned.
        self.assertListEqual(uncompleted_todos, [todo1])

    def test_getting_uncompleted_todos_when_todos_is_none(self):
        # Configure mock to return None.
        self.mock_get_todos.return_value = None

        # Call the service, which will return an empty list.
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called.
        self.assertTrue(self.mock_get_todos.called)

        # Confirm that an empty list was returned.
        self.assertListEqual(uncompleted_todos, [])
