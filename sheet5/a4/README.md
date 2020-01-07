#   ECDSA Fixed K (Aufgabe 4)

##  1. Nutzen Sie OpenSSL um die Kurvenparameter des öffentlichen Schlüssels auszulesen. Wie lauten diese?

By running th following command line:

`openssl ec -pubin -inform PEM -text -noout < vk.pem`

I got the following parameters from the output:

`ASN1 OID: prime256v1`

`NIST CURVE: P-256`

##  2. Vergleichen Sie die beiden Signaturen mit einem Hex-Editor. Welche Komponenten sind identisch und was folgt daraus?

It is possible to see that the first bytes of the signatures, which compose the `r` part of the signature, are equal, therefore both signatures share the same `k` value. This can be exploited in order to compute the private key that was used in the signature.

##  3. Berechnen Sie nun aus beiden Signaturen und aus Informationen des öffentlichen Schlüssels den privaten ECDSA Schlüssel mit dem diese Signaturen erstellt wurden. Speichern Sie den berechneten Schlüssel wieder im PEM-Format und dokumentieren Sie Ihr Vorgehen ausführlich.

The private key can be retrieved by running `python3 ecdsa-get-private-key.py`. The script consists of solving the system of equations shown in class:

`s1 ≡ (h1 + rd) / k (mod n)`

`s2 ≡ (h2 + rd) / k (mod n)`

After finding the value of `k`, the first equation is evaluated in order to find the private key `d`. The key can be found on `priv.pem`.

##  4. Nutzen Sie Ihren soeben berechneten privaten Schlüssel um eine Nachricht Ihrer Wahl zu signieren. Sie sollten diese Signatur nun mit dem gegebenen öffentlichen Schlüssel (vk.pem) verifizieren können.

The script `ecdsa-sign-and-verify.sh` signs the custom message stored on `my_msg.txt` with the retrieved private key and verifies it with the provided public key.