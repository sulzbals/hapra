import hashlib

prefix = "36979765629224074726367327745686243"
target = "fd8b6b5944fcede476bd62989044bd0fa36400e8"

# For all combinations of possible suffixes:
for suffix in range(0, 99999):
    # Concatenate the known prefix to the suffix, which is filled by 0s in the left to be always 5 characters long.
    attempt = prefix + str(suffix).zfill(5)

    # If the hash of the concatenation is equal to the one we are looking for, return its md5sum.
    if hashlib.sha1(attempt.encode("utf-8")).hexdigest() == target:
        print(hashlib.md5(attempt.encode("utf-8")).hexdigest())
        quit()