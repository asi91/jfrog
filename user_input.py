from artifactory import Artifactory
import sys
from credentials import UserCredentials
from requests.exceptions import HTTPError


class UserInput(object):
    """
    Receives the user input,
    instantiates an Artifactory instance,
    performs the desired action
    """

    def __init__(self):
        args = sys.argv
        self.param = args[1] if len(args) > 1 else ""
        self.param = self.param.lower().strip()
        self.user_creds = UserCredentials()
        self.artifactory = None

    def _instantiate_artifactory(self):
        if self.user_creds.is_known_user:
            # The user has been authenticated
            try:
                # Instantiate an Artifactory with the known username and password
                return Artifactory(*self.user_creds.retrieve_user_creds())
            except HTTPError as e:
                print("Something went wrong! Please check your internet connection and retry."
                      "\nIf the issue persists, please contact the maintainer.")
                sys.exit(2)
        else:
            print("Before performing any action against the server you need to authenticate yourself."
                  "\nPlease provide a valid username and password")
            user = input("username: ").strip()
            password = input("password: ").strip()

            if not (user and password):
                print("Username and/or password cannot be empty.\nExiting..")
                sys.exit(2)

            try:
                art = Artifactory(user, password)
                # The user has been authenticated by the Artifactory server. Store the username and password
                self.user_creds.store_user_creds(user, password)
                return art
                # perform desired action
            except HTTPError as e:
                # If the authentication fails (wrong username/ password), no token will be generated
                if e.response.status_code == 401:
                    print("Error! Please provide valid username and password.\nExiting..")
                else:
                    print("Something went wrong! Please check your internet connection and retry."
                          "\nIf the issue persists, please contact the maintainer.")
                sys.exit(2)

    def perform_action(self):
        if not self.param:
            self.show_help()
        elif self.param == "help":
            self.show_help()
        elif self.param == "ping":
            # do ping
            self.artifactory = self._instantiate_artifactory()
            self.do_ping()
        elif self.param == "version":
            # show version
            self.artifactory = self._instantiate_artifactory()
            self.get_version()
        elif self.param == "storage":
            # show storage info
            self.artifactory = self._instantiate_artifactory()
            self.show_storage()
        elif self.param == "create":
            # create user :: ask for user data
            self.artifactory = self._instantiate_artifactory()
            self.create_user()
        elif self.param == "delete":
            # delete user by name
            self.artifactory = self._instantiate_artifactory()
            self.delete_user()
        else:
            # Print error followed by help msg
            self.default_action()

    def show_help(self):
        print("This is a basic custom JFrog CLI that accepts the following actions:\n\n"
              "`help`\t\tLists the capabilities of this CLI.\n"
              "`ping`\t\tChecks the Artifactory server's status.\n"
              "`version`\tLists the Artifactory server's version.\n"
              "`storage`\tLists the Artifactory server's storage details.\n"
              "`create`\tCreates a new user (must provide username, email, password).\n"
              "`delete`\tRemoves the user (must provide username).\n"
              )

    def default_action(self):
        print(f"The requested action `{self.param}` "
              f"is not supported. See the following help message for more details..\n")
        self.show_help()

    def do_ping(self):
        result = self.artifactory.ping()
        print(result)

    def get_version(self):
        result = self.artifactory.system_version()
        print(result)

    def show_storage(self):
        result = self.artifactory.storage_info()
        print(result)

    def create_user(self):
        print("In order to create a new user, you need to provide the following parameters: "
              "name, email and password..\n")

        name = input("name: ").strip()
        email = input("email: ").strip()
        password = input("password: ").strip()

        if not (name and email and password):
            print("Username and/or email and/or password cannot be empty.\nExiting..")
            sys.exit(2)

        try:
            print(self.artifactory.create_or_replace_user(name, email, password))
        except Exception as e:
            print(f"Error! The provided parameters and invalid or insufficient\n{e}")

    def delete_user(self):
        print("Please provide the name of the user you wish to remove.")

        name = input("name: ").strip()

        if not name:
            print("Username cannot be empty.\nExiting..")
            sys.exit(2)

        try:
            print(self.artifactory.delete_user(name))
        except HTTPError as e:
            if e.response.status_code == 404:
                print(f"The user `{name}` does not exist.\nExiting..")
                sys.exit(2)
            else:
                print("Something went wrong! Please check your internet connection and retry."
                      "\nIf the issue persists, please contact the maintainer.")
                sys.exit(2)
