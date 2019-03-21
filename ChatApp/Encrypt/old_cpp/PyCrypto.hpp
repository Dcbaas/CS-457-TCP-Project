#ifndef                     PYCRYPTO_H
#define                     PYCRYPTO_H

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <openssl/rsa.h>
#include <string>
#include <cstring>


class PyCrypto{
public:
    PyCrypto();
    ~PyCrypto();
    uint8_t* rsa_encrypt(uint8_t* input, size_t inputLen);
    uint8_t* rsa_decrypt(uint8_t* input, size_t inputLen);

    uint8_t* encrypt(uint8_t* input, size_t inputLen);
    uint8_t* decrypt(uint8_t* input, size_t inputLen);
private:
    void handleError();
    std::pubfilename = "RSAbub.pem";
    std::privfileaname = "RSApriv.pem";


    uint8_t key[32];
    uint8_t iv[16];

    EVP_PKEY *pubkey, *privkey;


#endif

