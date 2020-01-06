#! /usr/bin/env python3

from functools import reduce
from Crypto.PublicKey import RSA

# Chinese remainder algorithm from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod 

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1 

# Root algorithm for large numbers from https://riptutorial.com/python/example/8751/computing-large-integer-roots

def nth_root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1

if __name__ == '__main__':

    n = []
    c = []

    # Load all the key modulus and ciphertexts into integers:
    for i in [1, 2, 3]:
        with open('pk{}.pem'.format(i), 'r') as key_file:
            n.append(int(RSA.importKey(''.join(key_file.read()).strip()).__getattr__('n')))

        with open('msg{}.bin'.format(i), 'rb') as msg_file:
            c.append(int(msg_file.read().hex(), 16))

    # Solve the system via Chinese Remainder Theorem:
    C = chinese_remainder(n, c)

    # The solution is the cubic root of C:
    sol = nth_root(C, 3)

    # Convert the solution to hexadecimal, then decode it into a string:
    msg = bytearray.fromhex(hex(sol)[2:]).decode()

    print("The decrypted message is: \"" + msg + "\"")