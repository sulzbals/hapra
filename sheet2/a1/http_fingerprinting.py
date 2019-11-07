#! /usr/bin/env python3

from const import *

import socket
import requests

# Get all open ports:
def port_scan(ip):
    # Try to load ports from cache:
    try:
        with open("./port_cache_" + ip + ".txt", "r") as file:
            ports = list(map(int, file.readlines()))

    except:
        print("Scanning ports. This might take some time...")

        ports = []

        # Try to connect to all ports:
        for port in range(1, 65535):
            # Open a socket:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # If the port accepts the connection, add it to the list:
            # Like connect(), but without throwing exceptions.
            if sock.connect_ex((ip, port)) == 0:
                ports.append(port)

        # Store ports in cache:
        with open("./port_cache_" + ip + ".txt", "w") as file:
            for port in ports:
                file.write("{}\n".format(port))

    return ports

if __name__ == "__main__":
    url_prefix = "http://" + ip + ":"

    # Associate each daemon to the ports it runs on with a
    # dictionary:
    result = {}

    # Open a session for HTTP requests:
    s = requests.Session()

    # Try to speak in HTTP to each open port:
    for port in port_scan(ip):
        # Try a GET HTTP request:
        try:
            r = s.get(url_prefix + str(port))

        # If an exception was thrown, the response was not formatted as
        # HTTP, therefore there is no HTTP server running on the port:
        except:
            continue

        # Identify the HTTP server (daemon) running on the port based on the
        # response header:
        daemon = r.headers["Server"]

        if daemon in result:
            # Append the port to the list of ports the daemon runs on:
            result[daemon].append(port)
        else:
            # Register the daemon found running on this port and associate
            # the port to it:
            result[daemon] = [port]

    # Pretty-print the relation daemon -> ports:
    for daemon, ports in result.items():
        print(daemon + ": " + ", ".join(list(map(str, ports))))