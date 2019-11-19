#   Vulnerability

There is a vulnerability on the sysadmin's update script: While most of the URLs used to download the packages have HTTPS as scheme, the one to wireshark_3.0.5-1_amd64.deb is HTTP, so it is not encrypted.

#   Attack

The attack consists in:

1. Building a fake debian package, that has the same metadata (name, version, dependencies, etc.) as the real one, and installs a shell script on /usr/bin/wireshark that creates the file ~/hacked.txt when executed. This way, when the sysadmin run "wireshark" as root, /root/hacked.txt will be created.
2. Spoofing, to be a man-in-the-middle of the gateway and the victim.
3. Intercepting the packet addressed to the victim that contains the original package as payload.
4. Replacing the payload by the fake debian package.
5. Delivering this modified packet to the victim instead.

##  Instructions

1. Build the fake package:

`dpkg-deb --build wireshark_3.0.5-1`

2. Enable IP forwarding (as root):

`echo 1 > /proc/sys/net/ipv4/ip_forward`

3. Initialise the Netfilterqueue (as root):

`iptables -I FORWARD -j NFQUEUE --queue-num [QUEUE_NUM]`

4. Run debianspoof (as root):

`python3 debianspoof.py -v [VICTIM_IP] -g [GATEWAY_IP] -q [QUEUE_NUM]`

#   Prevention

The prevention to this attack is simple: Never use HTTP to download packages, only HTTPS.