import os
from pathlib import Path
import json


class UserCredentials(object):
    """
    Stores the user and password in a dedicated file on the file system
    """
    def __init__(self):
        self.main_dir = ".jfrog"
        self.creds_file = ".credentials.json"
        self.home_dir = str(Path.home())
        self.is_known_user = False
        self.file_path = os.path.join(self.home_dir, self.main_dir, self.creds_file)

        self._create_creds_directory()

    def _create_creds_directory(self):
        if os.path.exists(self.file_path):
            self.is_known_user = True
        else:
            os.makedirs(os.path.join(self.home_dir, self.main_dir), exist_ok=True)

    def store_user_creds(self, user, passwd):
        user_creds = {
            "user": user,
            "pass": passwd  # todo: encode?
        }

        with open(self.file_path, "w") as f:
            json.dump(user_creds, f)

    def retrieve_user_creds(self):
        with open(self.file_path) as f:
            user_creds = json.load(f)

        return user_creds["user"], user_creds["pass"]
