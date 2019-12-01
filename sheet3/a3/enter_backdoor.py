#! /usr/bin/env python3

import sys
import hashlib
import struct
import socket

ICMP_ECHO_REQUEST = 8

# From Aufgabe 1 (ping):
def receive_icmp(my_socket):
    recPacket, addr = my_socket.recvfrom(1024)
    header = recPacket[20:28]
    payload = recPacket[28:]
    return payload, addr[0]

# From Aufgabe 1 (ping):
def send_icmp(my_socket, dest_addr, payload):
    dest_addr = socket.gethostbyname(dest_addr)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, 0, 1)
    packet = header + payload
    my_socket.sendto(packet, (dest_addr, 1))

def get_arguments():
    if len(sys.argv) != 5 or sys.argv[1] != "--addr" or sys.argv[3] != "--secret":
        print("Usage: {} --addr [ADDRESS] --secret [SECRET]".format(sys.argv[0]))
        exit()

    return sys.argv[2], sys.argv[4]

if __name__ == '__main__':

    # Parse arguments:
    host, sec = get_arguments()

    # Get a md5sum of the secret:
    secret = hashlib.md5(sec.encode()).digest()

    # Open socket to send ICMP request:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))

    # Send packet:
    send_icmp(sock, host, secret)

    id = None

    while id == None:

        payload, src = receive_icmp(sock)

        if src == host and payload[:16] == secret:

            # The session id comes right after the secret:
            id = payload[16:]

    exit = False

    while not exit:

        # Get user input:
        cmd = bytes(input("root# ").encode())

        # Send session id + command:
        send_icmp(sock, host, id + cmd)

        payload, src = receive_icmp(sock)

        if src == host and payload[:16] == id:

            if payload[16:] == secret:
                # End of session:
                exit = True
                output = payload[32:]
            else:
                output = payload[16:]

            print(output.decode())

    # Close socket:
    sock.close()