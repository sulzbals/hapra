#! /usr/bin/env python3

import argparse
import random

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", dest="num", help="Number of keys to be generated", default="1")
    options = parser.parse_args()
    return options

# Key is composed of five blocks of characters that belong to the following set:
valid_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
             'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'W', 'X', 'Y', 'Z']

# Check if given ordinal can be interpreted as a character contained in our set:
def is_valid(ordinal):
    try:
        return chr(ordinal) in valid_set
    except:
        return False

# Get a random character from the valid characters set:
def get_valid_random():
    return random.choice(valid_set)

# Generate first block, which must satisfy the constraint "c0 ^ c1 ^ c2 ^ c3 ^ c4 == 0x41":
def first_block():
    while True:
        # Generate c0-3 randomly:
        c0 = get_valid_random()
        c1 = get_valid_random()
        c2 = get_valid_random()
        c3 = get_valid_random()

        # Get the ord(c4) that satisfies the constraint:
        o4 = (ord(c0) ^ ord(c1) ^ ord(c2) ^ ord(c3)) ^ 0x41

        # If c4 is a valid character, the block is valid and can be returned:
        if is_valid(o4):
            return c0 + c1 + c2 + c3 + chr(o4)

# Generate second block, which must satisfy the constraint "c0 ^ c1 ^ c2 == c4":
def second_block():
    while True:
        # Generate c0-3 randomly:
        c0 = get_valid_random()
        c1 = get_valid_random()
        c2 = get_valid_random()
        c3 = get_valid_random()

        # Get the ord(c4) that satisfies the constraint:
        o4 = ord(c0) ^ ord(c1) ^ ord(c2)

        # If c4 is a valid character, the block is valid and can be returned:
        if is_valid(o4):
            return c0 + c1 + c2 + c3 + chr(o4)

# Generate third block, which must satisfy the constraint "c0 & c1 & c2 & c3 == c4":
def third_block():
    while True:
        # Generate c0-3 randomly:
        c0 = get_valid_random()
        c1 = get_valid_random()
        c2 = get_valid_random()
        c3 = get_valid_random()

        # Get the ord(c4) that satisfies the constraint:
        o4 = ord(c0) & ord(c1) & ord(c2) & ord(c3)

        # If c4 is a valid character, the block is valid and can be returned:
        if is_valid(o4):
            return c0 + c1 + c2 + c3 + chr(o4)

# Generate fourth block, which must satisfy the constraint "(c0 | c2 | c4) & 0xf == c1 ^ c3":
def fourth_block():
    while True:
        # Generate c{0,1,2,4} randomly:
        c0 = get_valid_random()
        c1 = get_valid_random()
        c2 = get_valid_random()
        c4 = get_valid_random()

        # Get the ord(c3) that satisfies the constraint:
        o3 = ((ord(c0) | ord(c2) | ord(c4)) & 0xf) ^ ord(c1)

        # If c3 is a valid character, the block is valid and can be returned:
        if is_valid(o3):
            return c0 + c1 + c2 + chr(o3) + c4

# Generate fifth block, which must satisfy the constraint "(c0 == c1 - 1) && (c2 == c3 + 1) && (c4 == 'X')":
def fifth_block():
    while True:
        c0 = get_valid_random()
        o1 = ord(c0) + 1
        c2 = get_valid_random()
        o3 = ord(c2) - 1
        c4 = 'X'

        # If c1 and c3 are valid characters, the block is valid and can be returned:
        if is_valid(o1) and is_valid(o3):
            return c0 + chr(o1) + c2 + chr(o3) + c4

# Key is composed of the five blocks delimited by '-':
def gen_key():
    return first_block()  + '-' + \
           second_block() + '-' + \
           third_block()  + '-' + \
           fourth_block() + '-' + \
           fifth_block()

if __name__ == "__main__":
    opt = get_arguments()

    for _ in range(int(opt.num)):
        print(gen_key())