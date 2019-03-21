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

        self.rsaCipher = PKCS1_OAEP.new(self.privKey)
        self.aesCipher = None

        pubFile.close()
        privFile.close()
        return

    def rsaDecrypt(self, cipherText):
        """
        Will always use the private key of the server
        cipherText (str): The text
        """
        self.sessionKey = self.rsaCipher.decrypt(cipherText)
        return

    def encrypt(self, plainText, iv):
        """
        Will encrypt with the
        """
        return

    def decrypt(self, plainText, iv):
        return

    def getPublicKey():
        return self.pubKey
    
    def getAESKey():
        return self.symKey

