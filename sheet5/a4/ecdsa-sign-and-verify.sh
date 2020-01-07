#! /bin/sh

openssl dgst -sha1 -sign priv.pem -out my_msg.sig my_msg.txt
openssl dgst -ecdsa-with-SHA1 -verify vk.pem -signature my_msg.sig my_msg.txt