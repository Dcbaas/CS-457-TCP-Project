from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Padding

class EncryptClient:
    def __init__(self):
        publicKeyFile = open('./RSApub.pem')
        self.sessionKey = get_random_bytes(32)

        self.publicKey = RSA.importKey(publicKeyFile.read())
        self.rsaCipher = PKCS1_OAEP.new(self.publicKey)
        publicKeyFile.close()
        return

    def getEncryptedAESKey(self):
        self.encryptedSessionKey = self.rsaCipher.encrypt(self.sessionKey)
        return self.encryptedSessionKey

    def encrypt(self, plainBytes):
        """
        This function is expected to get the bytes not the text itself
        """
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC)
        byteText = Padding.pad(plainText, 16)
        cipherText = aesCipher.encrypt(byteText)
        return cipherBytes, aesCipher.iv

    def decrypt(self, cipherBytes, iv):
        """
        This returns the plainBytes not the string itself
        """
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC, iv=iv)
        plainBytes = Padding.unpad(aesCipher.decrypt(cipherText),16)
        return plainBytes

