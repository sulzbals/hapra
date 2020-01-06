#   RSA Small Exponent (Aufgabe 3)

##  1. Untersuchen Sie mit Hilfe von OpenSSL die öffentlichen Schlüssel und bestimmen Sie die verwendeten Parameter. Was fällt Ihnen auf?

By running the script `rsa-examine-keys.sh`, it is possible to notice that all three keys are composed of different modulus, but the exponent is always `3`.

##  2. Nutzen Sie Ihre Erkenntnis um die Nachricht ohne Kenntnis eines privaten Schlüssels dennoch zu entschlüsseln.

Let `n` the number of encrypted messages and `e` the exponent common to all keys, we have `n >= e`, since `3 >= 3`. Given that, we can perform a RSA Broadcast attack by finding `C` with the Chinese Remaining Theorem and calculating its cubic root.

The message can be decrypted by running `python3 rsa-broadcast-attack.py`. It is `The answer to life the universe and everything = 42`.