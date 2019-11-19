#   Vulnerability

There is a vulnerability on the sysadmin's update script: While most of the URLs used to download the packages have HTTPS as scheme, the one to wireshark_3.0.5-1_amd64.deb is HTTP, so it is not encrypted.

#   Attack

The attack consists of:

1. Building a fake debian package, that has the same metadata as the original one.
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

## Debian package structure

* usr/bin/wireshark: Shellscript that creates `~/hacked.txt` (so when running as root, `/root/hacked.txt` will be created).
* DEBIAN/control: Control fields of the package. They are all identical to the original one's, except for the description (for demonstration purposes).
* DEBIAN/install: Specifies that file `wireshark` is to be installed, so it will be copied to `/usr/bin/wireshark`.

##  Test environment

The attack was tested using two VMs running Ubuntu Bionic (minimal edition) connected to a libvirt virtual network. Notice that the fake package has the same dependencies as the real one, so installation will fail if they are missing.

#   Prevention

The sysadmin could prevent this attack by either:

* Updating the URL to use `https` instead of `http`;
* Extracting the MD5sum of the downloaded package, then retrieving the expected one from the repository and comparing them. If they are not equal, do not install the package. The one respective to the wireshark package we are exploiting can be found on `https://ftp.fau.de/ubuntu/dists/eoan/universe/binary-amd64/Packages.gz`.