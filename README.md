#asifrog
This is a basic custom JFrog CLI that accepts the following actions:

`help`\t\tLists the capabilities of this CLI.

`ping`\t\tChecks the Artifactory server's status.

`version`\tLists the Artifactory server's version.

`storage`\tLists the Artifactory server's storage details.

`create`\tCreates a new user (must provide username, email, password).

`delete`\tRemoves the user (must provide username).

**NOTE:** The first time the CLI is used, it'll ask for the username and password of the artifactory server (Ask the admin/author). 