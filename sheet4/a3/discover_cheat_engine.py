#! /usr/bin/python3

alt_name = b'HaPra'

encoded_cheatengine = open("flappyHacks/assets/gfx/game/Flappy.png", "rb")

bArr = encoded_cheatengine.read()

encoded_cheatengine.close()

result = bytearray()

for i in range(0, len(bArr)):
    result.append(bArr[i] ^ alt_name[i % 5])

decoded_cheatengine = open("cheatengine.dex", "wb")

decoded_cheatengine.write(result)

decoded_cheatengine.close()