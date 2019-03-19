#!/usr/bin/bash

#ONLY RUN ONCE
openssl genpkey -algorithm RSA -out RSApriv.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in RSApriv.pem -out RSApub.pem

