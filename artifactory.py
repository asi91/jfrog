import requests
import json
from time import time

from decorators import retry_on_network_errors, refresh_access_token


class Artifactory(object):
    """
    Holds the Artifactory configuration data: User, password, base URL, access token,..
    Requires and renews access token
    Performs all requests against the Artifactory REST API
    """

    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd

        self.base_url = "https://asihamza.jfrog.io/artifactory"
        self.users_endpoint = "/api/security/users/"
        self.system_endpoint = "/api/system"

        self._retrieve_access_token_data()

    @retry_on_network_errors(10)
    def _retrieve_access_token_data(self):
        resp = requests.post(
            f"{self.base_url}/api/security/token",
            auth=(self.user, self.passwd),
            data={"username": self.user,
                  "scope": "member-of-groups:admins"}
        )

        resp = json.loads(resp.text)

        self.access_token = resp["access_token"]
        self.token_expire_time = time() + resp["expires_in"]
        self.token_type = resp["token_type"]

        self.headers = {"Authorization": f"{self.token_type} {self.access_token}"}

    @refresh_access_token
    @retry_on_network_errors(10)
    def ping(self):
        return requests.get(f"{self.base_url}{self.system_endpoint}/ping", headers=self.headers).text

    @refresh_access_token
    @retry_on_network_errors(10)
    def system_info(self):
        return requests.get(f"{self.base_url}{self.system_endpoint}", headers=self.headers).text

    @refresh_access_token
    @retry_on_network_errors(10)
    def system_version(self):
        # artifactory version
        return requests.get(f"{self.base_url}{self.system_endpoint}/version", headers=self.headers).text

    @refresh_access_token
    @retry_on_network_errors(10)
    def create_or_replace_user(self, name, email, password, **kwargs):
        user_data = {
            "name": name,
            "email": email,
            "password": password
        }

        for k, v in kwargs.items():
            user_data[k] = v

        resp = requests.put(f"{self.base_url}{self.users_endpoint}{name}", json=user_data, headers=self.headers)

        if resp.ok:
            return resp.text or f"User `{name}` has been created successfully"

        return f"User `{name}` was not found"

    @refresh_access_token
    @retry_on_network_errors(10)
    def delete_user(self, name):
        return requests.delete(f"{self.base_url}{self.users_endpoint}{name}", headers=self.headers).text
