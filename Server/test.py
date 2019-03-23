from Crypto.Random import get_random_bytes
import EncryptServer

text = 'This is the best text here'
key = get_random_bytes(32)

encrypter = EncryptServer.EncryptServer()

cipherPacket = encrypter.encrypt(text, key)

resultText = encrypter.decrypt(cipherPacket, key)

print(cipherPacket)
print(resultText)
