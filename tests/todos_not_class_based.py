from unittest.mock import Mock, patch
from app import create_app
from flask_test_helpers import FlackTestCase
from app.utils.service import get_todos, get_uncompleted_todos
import requests


class TestCase(FlackTestCase):

    @patch('app.utils.service.requests.get')
    def test_request_response(self, mock_get):
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertIsNotNone(response)

    @patch('app.utils.service.requests.get')
    def test_getting_todos_when_response_is_ok(self, mock_get):
        todos = [{
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }]

        # Configure the mock to return a response with an OK status code. Also, the mock should have
        # a `json()` method that returns a list of todos.
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = todos

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertListEqual(response.json(), todos)

    @patch('app.utils.service.requests.get')
    def test_getting_todos_when_response_is_not_ok(self, mock_get):
        # Configure the mock to not return a response with an OK status code.
        mock_get.return_value.ok = False

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the response contains an error, I should get no todos.
        self.assertIsNone(response)

    @patch('app.utils.service.get_todos')
    def test_getting_uncompleted_todos_when_todos_is_not_none(self, mock_get_todos):
        todo1 = {
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }
        todo2 = {
            'userId': 1,
            'id': 2,
            'title': 'Walk the dog',
            'completed': True
        }

        # Configure mock to return a response with a JSON-serialized list of todos.
        mock_get_todos.return_value = Mock()
        mock_get_todos.return_value.json.return_value = [todo1, todo2]

        # Call the service, which will get a list of todos filtered on completed.
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called.
        self.assertTrue(mock_get_todos.called)

        # Confirm that the expected filtered list of todos was returned.
        self.assertListEqual(uncompleted_todos, [todo1])

    @patch('app.utils.service.get_todos')
    def test_getting_uncompleted_todos_when_todos_is_none(self, mock_get_todos):
        # Configure mock to return None.
        mock_get_todos.return_value = None

        # Call the service, which will return an empty list.
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called.
        self.assertTrue(mock_get_todos.called)

        # Confirm that an empty list was returned.
        self.assertListEqual(uncompleted_todos, [])
