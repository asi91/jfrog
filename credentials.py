import os
from pathlib import Path
import json
import hashlib


class UserCredentials(object):
    """
    Stores the user and password in a dedicated file on the file system
    """
    def __init__(self):
        self.main_dir = ".jfrog"
        self.creds_file = ".credentials.json"
        self.home_dir = str(Path.home())
        self.is_known_user = False
        self._create_creds_directory()
        self.file_path = os.path.join(self.home_dir, self.main_dir, self.creds_file)

        self._create_creds_directory()

    def _create_creds_directory(self):
        if os.path.exists(self.file_path):
            self.is_known_user = True
        else:
            os.makedirs(self.file_path)

    def store_user_creds(self, user, passwd):
        user_creds = {
            "user": user,
            "pass": ""
        }

        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            passwd.encode("utf-8"),
            salt,
            100000
        )

        user_creds["pass"] = f"{salt}{key}"

        with open(self.file_path, "w") as f:
            json.dump(user_creds, f)

    def authenticate_user(self, user, passwd):
        with open(self.file_path) as f:
            user_creds = json.load(f)

        if user != user_creds["user"]:
            return False

        salt = user_creds["pass"][:32]

        new_key = key = hashlib.pbkdf2_hmac(
            "sha256",
            passwd.encode("utf-8"),
            salt,
            100000
        )

        if new_key != user_creds[32:]:
            return False

        return True
