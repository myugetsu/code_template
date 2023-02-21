"""Common unit testing helpers."""
import base64
import json
import unittest


class FlackTestCase(unittest.TestCase):
    """A TestCase subclass with common functionality used by MicroFlack
    services.
    """

    def get_headers(self, basic_auth=None, token_auth=None):
        """Return the headers to include in the request."""
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json"}
        if basic_auth is not None:
            headers["Authorization"] = "Basic " + base64.b64encode(
                basic_auth.encode("utf-8")
            ).decode("utf-8")
        if token_auth is not None:
            headers["Authorization"] = "Bearer " + token_auth
        return headers

    def get(self, url, basic_auth=None, token_auth=None):
        """Send a GET request through the Flask test client."""
        rv = self.client.get(
            url, headers=self.get_headers(basic_auth, token_auth))
        body = rv.get_data(as_text=True)
        if body is not None and body != "":
            try:
                body = json.loads(body)
            except:
                pass
        return body, rv.status_code, rv.headers

    def post(self, url, data=None, basic_auth=None, token_auth=None):
        """Send a POST request through the Flask test client."""
        d = data if data is None else json.dumps(data)
        rv = self.client.post(
            url, data=d, headers=self.get_headers(basic_auth, token_auth)
        )
        body = rv.get_data(as_text=True)
        if body is not None and body != "":
            try:
                body = json.loads(body)
            except:
                pass
        return body, rv.status_code, rv.headers

    def put(self, url, data=None, basic_auth=None, token_auth=None):
        """Send a PUT request through the Flask test client."""
        d = data if data is None else json.dumps(data)
        rv = self.client.put(
            url, data=d, headers=self.get_headers(basic_auth, token_auth)
        )
        body = rv.get_data(as_text=True)
        if body is not None and body != "":
            try:
                body = json.loads(body)
            except:
                pass
        return body, rv.status_code, rv.headers

    def delete(self, url, basic_auth=None, token_auth=None):
        """Send a DELETE request through the Flask test client."""
        rv = self.client.delete(
            url, headers=self.get_headers(basic_auth, token_auth))
        body = rv.get_data(as_text=True)
        if body is not None and body != "":
            try:
                body = json.loads(body)
            except:
                pass
        return body, rv.status_code, rv.headers


class MockDB:
    def __init__(self, realdb):
        self.last_sql_cmd = None
        self.realdb = realdb
        self.rowcount = 0
        self.fetchall_res = None
        self.description = {
            "name": "id",
            "type_code": 23,
            "name": "external_id",
            "type_code": 1043,
        }

    def execute(self, sql_cmd, *args):
        sql_str = self.realdb.mogrify(sql_cmd, *args)
        print("Got sql_str of %s", sql_str)
        self.last_sql_cmd = sql_str
        return 0

    def mogrify(self, sql_cmd, *args):
        return self.realdb.mogrify(sql_cmd, *args)

    def reset(self):
        self.last_sql_cmd = None

    def set_fetchall_res(self, res):
        self.fetchall_res = res

    def fetchall(self):
        res = self.fetchall_res or [[1, 2]]
        self.fetchall_res = None
        return res

    def fetchone(self):
        res = self.fetchall_res[0] if self.fetchall_res else (1, (2, 3, 4))
        return res
