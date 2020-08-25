# asifrog

This is a basic custom JFrog CLI that accepts the following actions:

`help`		Lists the capabilities of this CLI.

`ping`		Checks the Artifactory server's status.

`version`	Lists the Artifactory server's version.

`storage`	Lists the Artifactory server's storage details.

`create`	Creates a new user (must provide username, email, password).

`delete`	Removes the user (must provide username).

**NOTE:** The first time the CLI is used, it'll ask for the username and password of the artifactory server (Ask the admin/author). 