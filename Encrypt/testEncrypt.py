from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Padding

text = 'This is some great text'
byteText = Padding.pad(text.encode(), 16)

sessionKey = get_random_bytes(32)

AES1 = AES.new(sessionKey, AES.MODE_CBC)
AES2 = AES.new(sessionKey, AES.MODE_CBC, iv=AES1.iv)

cipherText = AES1.encrypt(byteText)

print(cipherText)

plainText = Padding.unpad(AES2.decrypt(cipherText), 16).decode()

print(plainText)

