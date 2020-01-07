#! /usr/bin/env python3

from ecdsa import NIST256p, SigningKey
from ecdsa.numbertheory import inverse_mod
from hashlib import sha1

def parse_sig(sig):

    # Parse the length of the r part of the signature to get the end position:
    r_end = 4 + int(sig[3])

    # Parse the r part of the signature:
    r = int(sig[4:r_end].hex(), 16)

    # Parse the length of the s part of the signature to get the end position:
    s_end= r_end + 2 + int(sig[r_end+1])

    # Parse the s part of the signature:
    s = int(sig[r_end+2:s_end].hex(), 16)

    return r, s

if __name__ == "__main__":

    # Get the order of the curve:
    n = NIST256p.order

    # Read message 1:
    with open("msg1.txt", "rb") as msg:
        msg1 = msg.read()

    # Read message 2:
    with open("msg2.txt", "rb") as msg:
        msg2 = msg.read()

    # Parse signature of message 1:
    with open("msg1.sig", "rb") as sig:
        r1, s1 = parse_sig(sig.read())

    # Parse signature from message 2:
    with open("msg2.sig", "rb") as sig:
        r2, s2 = parse_sig(sig.read())

    if r1 != r2:
        print("Cannot retrieve private key from signatures with distinct r parts")
        quit()

    # r == r1 == r2
    r = r1

    # Get hashes of messages:
    h1 = int(sha1(msg1).hexdigest(), 16)
    h2 = int(sha1(msg2).hexdigest(), 16)

    # Solve the system in order to find the value of k:
    k = (((h1 - h2) % n) * inverse_mod(s1 - s2, n)) % n

    # Replace k by its value on the first equation in order to find the private key d:
    d = (((s1 * k - h1) % n) * inverse_mod(r, n)) % n

    # Print the private key in PEM format:
    print(SigningKey.from_secret_exponent(d, NIST256p).to_pem().decode())