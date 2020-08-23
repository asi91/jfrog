import requests
from requests.auth import HTTPBasicAuth

base_url = "https://asihamza.jfrog.io/artifactory"

user = "hamzassi.91@gmail.com"
password = "123Jfrog!"

def ping():
    url = "/api/system/ping"
    resp = requests.get(f"{base_url}{url}", auth=(user, password))
    print(resp.text)

def system_info():
    url = "/api/system"
    resp = requests.get(f"{base_url}{url}", auth=(user, password))
    print(resp.text)


def system_version():
    # artifactory version
    url = "/api/system/version"
    resp = requests.get(f"{base_url}{url}", auth=(user, password))
    print(resp.text)


def storage_info():
    url = "/api/storageinfo"
    resp = requests.get(f"{base_url}{url}", auth=(user, password))
    print(resp.text)

def create_user():
    name = "assi"
    url = f"/api/security/users/{name}"
    user_data = {
        "name": name,
        "email": "hamzassi.91+jf@gmail.com",
        "password": "123Pass!"
    }
    resp = requests.put(f"{base_url}{url}", auth=(user, password), json=user_data)
    print(resp.text)


def delete_user():
    name = "assi"
    url = f"/api/security/users/{name}"
    resp = requests.delete(f"{base_url}{url}", auth=(user, password))
    print(resp.text)


def get_access_token():
    url = "/api/security/token"
    resp = requests.post(f"{base_url}{url}", auth=(user, password), data={"username": user})
    print(resp.text)


if __name__ == "__main__":
    get_access_token()
