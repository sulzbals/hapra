# Vulnerability

The vulnerability of the server is heartbleeding. It consists on exploiting the heartbeat extension.

## The heartbeat

This is how the heartbeat works: The client sends a packet with an arbitrary length and payload to the server. The server then replies with a packet with the same payload to the client to prove that the connection is still up.

## Exploit

The vulnerable versions of OpenSSL implement the heartbeat response by reading the number of bytes specified by the length field of the packet from memory, starting from the payload's base address. Since no proper bound checking is performed, if this specified length is higher than the actual payload length, data stored after the payload is read and sent to the client. This attack is called heartbleeding, and it was used on this exercise to steal the server's private key, that can be found somewhere in its memory.

# Attack

In this exercise, heartbleeding is used right after Client and Server Hello to retrieve the maximum amount of data stored in the server's RAM (0xFFFF bytes). Then we search this data with regular expressions for the header and footer of the private key. Knowing the start and end limits of the key, it is extracted from the raw data.

## Usage

`python3 heartbleeding.py --ip [HOST_IP]`

## Output

The program should print the private key in standard PEM format. You can pipe it to a file and give its path to wireshark to decrypt the heartbleed.pcap file.

## Stolen data

On `stolen_credentials.txt` there is the login data for squirrelmail, retrieved by decrypting heartbleed.pcap with the server's private key.

On `stolen_mail.txt` there is the only mail from the account's mailbox.

# Prevention

The server's administrator could prevent this kind of attack by either:

* Updating OpenSSL to a version that is not vulnerable;
* Disabling the heartbeat extension.