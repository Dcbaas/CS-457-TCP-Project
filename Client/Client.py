import socket
import select
import sys

from Client import EncryptClient
class Client:
    def __init__(self, ipAddress, portNum = 8008, username = '', testing = False):
        self.ENCODED_SPACE = ''.encode()
        self.username = username
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((ipAddress, portNum))
        except Exception as err:
            print("No connection found on host %s at port %s." % (ipAddress, portNum))
            self.clientSocket.close()
            exit()

        self.encrypter = EncryptClient()

        usermessage = str('username:' + self.username)
        self.clientSocket.send(usermessage.encode())

        self.inputList = []
        self.inputList.append(self.clientSocket)
        self.inputList.append(sys.stdin)

        return

    def runClient(self):
        while True:
            readyToRead, readyToWrite, inError = \
                     select.select(self.inputList, self.inputList, self.inputList)

            if self.clientSocket in readyToRead:
                rawPacket = self.clientSocket.recv(289)
                self.manageClient(rawPacket)
                self.handleMessage(rawPacket)

            elif sys.stdin in readyToRead:
                for line in sys.stdin:
                    line = line.strip()
                    self.sendMessage(line)
                    break
                sys.stdout.flush()
    def runHandshake(self):
        """
        The handshake sets sends the server the AES key and the username it will be using while 
        connected.
        """
        #Send the AES key
        self.clientSocket.send(encrypter.getEncryptedAESKey())
        usermessage = str('username:' + self.username)
        
        cipherMessage,iv = self.encrypter.encrypt(usermessage)
        self.clientSocket.send(bytes(cipherMessage + iv))

    def doHandshake(self):
        #Send the AES key
        rsaEncryptedAES = self.cryptoBackend.getEncryptedAESKey()
        print(rsaEncryptedAES)
        self.clientSocket.send(rsaEncryptedAES)

        usermessage = str('username:' + self.username)
        packet, iv = self.cryptoBackend.encrypt(usermessage.encode())
        self.clientSocket.send(bytes(iv + self.ENCODED_SPACE + packet))

    def handleMessage(self, rawPacket):
        splitPacket = rawPacket.split(self.ENCODED_SPACE)

        #The message is the cipher text decrypted and decoded back into a string
        packet = self.cryptoBackend.decrypt(splitPacket[1], splitPacketp[0]).decode()
        source, dest, message = self.splitPacket(packet)

        if dest == 'list':
            self.displayList(message)
        else:
            self._printMessage(source, dest, message)
        return

    def composeDirectMessage(self, line):
        messageDetail = line[1:].split(' ', 1)
        return str(self.username + ':' + messageDetail[0] + ':' + messageDetail[1])

    def displayList(self, userList):
        print('Users:')
        userList = userList.split(':')
        for user in userList:
            print(user)
        return

    def _printMessage(self, source, dest, message):
        '''
        Prints a standard message to the screen. If its a public message, the print statement marks
        the message as such.
        '''
        if dest == 'allchat':
            print(str(source + ' (Public):' + message))
        else:
            print(str(source + ': ' + message))
        return


    def sendMessage(self, rawMessage):
        detail = rawMessage.split(' ', 1)
        packet = ''

        if detail[0] == '!private':
            dest_messae_pair = detail[1].split(' ', 1)
            packet = self.constructPacket(dest_messae_pair[0], dest_messae_pair[1])
        elif detail[0] == '!all':
            packet = self.constructPacket('allchat', detail[1])

        elif detail[0] == '!list':
            packet = str(self.username + ':list')

        elif detail[0] == '!quit':
            self.quitProgram()

        else:
            print('Not a valid command')

        if len(packet) <= 289
            packet, iv = self.cryptoBackend.encrypt(packet.encode)
            self.clientSocket.send(bytes(iv + self.ENCODED_SPACE + packet))
        else:
            print('Message too long')
        return

    def splitPacket(self, packet):
        rawList = packet.split(":", 2)
        source = rawList[0]
        dest = rawList[1]
        detail = rawList[2]
        return source, dest, detail

    def constructPacket(self, dest, message):
        return str(self.username +':' + dest + ':' + message)

    #DEPRICATED 
    async def detectUserInput(self):
        ch = readchar.readchar()
        if ch == '/':
            return True

        return False

    def manageClient(self, buffer):
        if len(buffer) == 0:
            self.quitProgram()

    def quitProgram(self):
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()
        exit(0)

