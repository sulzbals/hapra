#   HMAC Length Extension Attack (Aufgabe 2)

##  Attack description

The script `bruteforce.py` can be used to discover the key length through brute-force and append an arbitrary message to the message of the day.

I used the `hashpumpy` library to apply the `SHA-256` algorithm starting from the original HMAC. It generates the necessary padding, appends the new message, and recalculates the HMAC given the assumed key length. The key lengths are tested from 1 to the specified maximum value, or until the attack succeeds. Each test submits the padded original message plus the appended message and the new HMAC to the server, then looks the response up for a success message.

##  Script usage

`python3 bruteforce.py -l [MAX_KEY_LENGTH] -m [NEW_MSG]`

The URL of the server, original HMAC and path to original message of the day can be changed through optional parameters, use with `--help` to check out those options.

##  Result

The script discovers that the key length is 20 bytes. The new message of the day is consequently appended to the server's message of the day.

##  Geben Sie die erweiterte Nachricht zusammen mit Ihrer neuen HMAC auch als Textdatei ab.

The extended message is stored on `ext_motd.txt` and the new HMAC is stored on `hmac.txt`. You can try another messages as well with the script.

##  Warum muss Ihre Zeichnkette zwingenderweise mit dem Buchstaben ”H” beginnen?

If you check the contents of `ext_motd.txt`, you will see that the padding between the original message and the appended one is:

`\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x48`

The padding consists of two parts:

1. All the space between the end of the data to be hashed and the next address congruent to 56 (mod 64) is filled by 0s, except the first bit, which is set to 1. In practice, it will add a padding until the end of a 64-byte long block, except the last 8 bytes of it, which are reserved. This chunk, on our example, is:

`\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00`

2. The remaining 8 bytes contain the length, in bits, of the whole message, which is (k + m) * 8 = (20 + 373) * 8 = 3144. This chunk is, in our example:

`\x00\x00\x00\x00\x00\x00\x0c\x48`

Since the only byte of the padding that can be interpreted as an `ASCII` character is the last one (`\x48`), its respective character "`H`" will always be printed between the old message of the day and the appended one.