from app.utils.constants import BASE_URL
import requests


# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Third-party imports...

# Local imports...

TODOS_URL = urljoin(BASE_URL, "todos")
USERS_URL = urljoin(BASE_URL, "users")


def get_todos():
    response = requests.get(TODOS_URL)
    if response.ok:
        return response
    else:
        return None


def get_uncompleted_todos():
    response = get_todos()
    if response is None:
        return []
    else:
        todos = response.json()
        return [todo for todo in todos if todo.get("completed") == False]


def get_users():
    response = requests.get(USERS_URL)
    if response.ok:
        return response
    else:
        return None


def get_user(id):
    USER_URL = urljoin(BASE_URL, "users/" + str(id))
    response = requests.get(USER_URL)

    if response.ok:
        return response
    else:
        return None
