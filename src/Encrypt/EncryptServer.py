from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

class EncryptServer:
    def __init__(self):
        pubFile = open('RSApub.pem', 'r' )
        privFile = open('RSApriv.pem', 'r')

        #I could generate the public key from the private key being read by I choose to load the one
        #already given to me using the command line tools.
        self.privKey = RSA.importKey(privFile.read())
        self.pubKey = RSA.importKey(pubFile.read())

        self.sessionKey = None

        pubFile.close()
        privFile.close()
        return

    def rsaDecrypt(self, cipherText):
        """
        Will always use the private key of the server
        """
        rsaCipher = PKCS1_OAEP.new(privKey)
        self.sessionKey = rsaCipher.decrypt(cipherText)
        return

    def encrypt(self, plainText):
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC)
        byteText = Padding.pad(plainText.encode(), 16)
        cipherText = aesCipher.encrypt(byteText)
        return cipherText, aesCipher.iv


    def decrypt(self, cipherText, iv):
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC, iv=iv)
        plainText = Padding.unpad(aesCipher.decrypt(cipherText),16).decode()
        return plainText


    def getPublicKey():
        return self.pubKey

    def getAESKey():
        return self.symKey

