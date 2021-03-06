#! /usr/bin/env python3

import socket
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="Host IP", default="10.0.23.15")
    options = parser.parse_args()
    return options

ports = [210, 2100, 2121, 21000]

# Random username:
user = "invalid_user"

# After a little research it is possible to determine the 331 response messages for each daemon:
daemon_responses = {
    "vs-ftpd": "331 Please specify the password.",              # From docker image fauria/vsftpd
    "pro-ftpd": "331 Password required for " + user,            # From ftp.freeradius.org
    "py-ftpd": "331 Give me password",                          # By elimination
    "pure-ftpd": "331 User " + user + " OK. Password required"  # From the source code
}

port_responses = {}

if __name__ == "__main__":
    options = get_arguments()

    for port in ports:
        # Open a socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((options.ip, port))
        sock.recv(1024)

        # The response will be 331:
        sock.send(bytearray("USER " + user + "\r\n", "utf-8"))
        response = sock.recv(1024).decode("utf-8").strip()

        # Associate the response message to the port:
        port_responses[response] = port

        sock.send(b'QUIT\r\n')
        sock.recv(1024)

    result = {}

    # Create a new dictionary associating each daemon to the port
    # it is running on:
    for daemon, response in daemon_responses.items():
        result[daemon] = port_responses[response]

    # Pretty-print the relation daemon -> port:
    for daemon, port in result.items():
        print(daemon + ": " + str(port))