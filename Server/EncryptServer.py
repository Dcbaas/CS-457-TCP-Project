from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Padding
class EncryptServer:
    def __init__(self):
        privFile = open('RSApriv.pem', 'r')

        self.ENCODED_SPACE = ' '.encode()

        #I could generate the public key from the private key being read by I choose to load the one
        #already given to me using the command line tools.
        self.privKey = RSA.importKey(privFile.read())

        privFile.close()
        return

    def rsaDecrypt(self, cipherText):
        """
        Will always use the private key of the server
        """
        rsaCipher = PKCS1_OAEP.new(privKey)
        return rsaCipher.decrypt(cipherText)

    def encrypt(self, plainText, key):
        aesCipher = AES.new(key, AES.MODE_CBC)
        byteText = Padding.pad(plainText.encode(), 16)
        cipherText = aesCipher.encrypt(byteText)
        print(cipherText)

        cipherPacket = (aesCipher.iv + cipherText)
        return cipherPacket

    def decrypt(self, cipherPacket, key):
        iv, cipherText = self._splitCipherBytes(cipherPacket)
        print(cipherText)
        aesCipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decipheredText = aesCipher.decrypt(cipherText)
        plainText = Padding.unpad(decipheredText, 16).decode()
        return plainText

    def getPublicKey():
        return self.pubKey

    def getAESKey():
        return self.symKey
    
    def _splitCipherBytes(self, cipherPacket):
        iv = cipherPacket[0:16]
        cipherText = cipherPacket[16:]
        return iv, cipherText

