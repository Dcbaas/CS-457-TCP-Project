#include "PyCrypto.hpp"

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <openssl/rsa.h>
#include <string>
#include <cstring>

PyCrypto::PyCrypto(){

}

PyCrypto::~PyCrypto(){
}

uint8_t* PyCrypto::rsa_encrypt(uint8_t* input, size_t inputLen){
    EVP_PKEY_CTX *ctx;
    uint8_t* out = new uint8_t[512];
    size_t outlen;
    ctx = EVP_PKEY_CTX_new(key, NULL);
    if (!ctx)
        handleErrors();
    if (EVP_PKEY_encrypt_init(ctx) <= 0)
        handleErrors();
    if (EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_OAEP_PADDING) <= 0)
        handleErrors();
    if (EVP_PKEY_encrypt(ctx, NULL, &outlen, in, inlen) <= 0)
        handleErrors();
    if (EVP_PKEY_encrypt(ctx, out, &outlen, in, inlen) <= 0)
        handleErrors();

    return out;
}


uint8_t* PyCrypto::rsa_decrypt(uint8_t* input, size_t inputLen){

}

uint8_t* PyCrypto::encrypt(uint8_t* input, size_t inputLen){
}

uint8_t* PyCrypto::decrypt(uint8_t* input, size_t inputLen){

}

void PyCrypto::handleError(){
    ERR_print_errors_fp(stderr);
}
