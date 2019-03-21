from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Padding

class EncryptClient:
    def __init__(self):
        self.publicKey= None
        self.sessionKey = get_random_bytes(32)

    def setPublicKey(self, publicKey):
        self.publicKey = publicKey
        self.rsaCipher = PKCS1_OAEP.new(self.publicKey)
        self._rsaEncrypt()
        return

    def _rsaEncrypt(self):
        self.encryptedSessionKey = self.rsaCipher.encrypt(sessionKey)
        return

    def getEncryptedAESKey(self):
        return self.encryptedSessionKey

    def encrypt(self, plainText):
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC)
        byteText = Padding.pad(plainText.encode(), 16)
        cipherText = aesCipher.encrypt(byteText)
        return cipherText, aesCipher.iv

    def decrypt(self, cipherText, iv):
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC, iv=iv)
        plainText = Padding.unpad(aesCipher.decrypt(cipherText),16).decode()
        return plainText

