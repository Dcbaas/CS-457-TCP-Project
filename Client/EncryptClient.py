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

    def encrypt(self, plainText):
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC)
        byteText = Padding.pad(plainText.encode(), 16)
        cipherText = aesCipher.encrypt(byteText)
        cipherPacket = bytes(aesCipher.iv + cipherText)
        return cipherPacket

    def decrypt(self, cipherPacket):
        iv, cipherText = self._splitCipherBytes(cipherPacket)
        aesCipher = AES.new(self.sessionKey, AES.MODE_CBC, iv=iv)
        plainText = Padding.unpad(aesCipher.decrypt(cipherText),16)
        return plainText.decode()
    
    def _splitCipherBytes(self, cipherPacket):
        iv = cipherPacket[0:16]
        cipherText = cipherPacket[16:]
        return iv, cipherText

