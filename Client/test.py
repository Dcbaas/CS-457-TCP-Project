import EncryptClient

text = 'This is some test text.'

encrypter = EncryptClient.EncryptClient()

cipherPacket = encrypter.encrypt(text)

resultText = encrypter.decrypt(cipherPacket)

print(text)
print(cipherPacket)
print(resultText)


