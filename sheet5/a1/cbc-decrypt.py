#! /usr/bin/env python3

# Format: TRANSFER AMOUNT $1000000 REASON Salary Jan. 2016 DEST #78384 END

import base64

# Bitwise XOR between two byte streams:
def xor(a, b):
    return bytes(ba ^ bb for ba, bb in zip(a, b))

plain = "TRANSFER AMOUNT $1000000 REASON Salary Jan. 2016 DEST #78384 END"
cipher = "wUHhFdm5le/fLoF/G4U0u6FGSNVtkxFA3ZIEwYombzhGF2eYUCOutHTg0h16BtYlBd5FO/XlJkQ058Ev+8hTIA=="

plain = plain.encode() # Convert to bytes
cipher = base64.b64decode(cipher) # Decode in base 64 and convert to bytes

# Split plain and cipher texts into blocks of bytes:
plain_blocks = [plain[i:i+16] for i in range(0, 64, 16)]
cipher_blocks = [cipher[i:i+16] for i in range(0, 64, 16)]

# Get the AES-128 decryption output of the last block:
dec = xor(cipher_blocks[-2], plain_blocks[-1])

# Change the previous ciphertext block so the result of the XOR between it and the decrypted last block generates the
# plaintext we want to inject into the transaction:
cipher_blocks[-2] = xor(dec, b' DEST #31337 END')

# Rebuild the ciphertext stream:
new_cipher = b''
for b in cipher_blocks:
    new_cipher += b

# Encode the new ciphertext into base 64:
new_cipher = base64.b64encode(new_cipher)

# Print it as string:
print(new_cipher.decode())