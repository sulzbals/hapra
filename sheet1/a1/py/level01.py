import requests
import hashlib

s = requests.Session()

# Access the file to be sorted.
r = s.get("http://10.0.23.24:8005/level01/sort_this")

# Split all lines in a list of strings.
lines = r.text.split()

# Sort this list.
lines.sort()

# Concatenate (join) all strings from the list into one, then hash it to get the secret.
print(hashlib.md5("".join(lines).encode('utf-8')).hexdigest())