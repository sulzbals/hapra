#! /bin/sh

for i in 1 2 3; do
	openssl rsa -pubin -inform PEM -text -noout < pk$i.pem
done