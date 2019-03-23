import socket
import select
import sys
import Encrypt.EncryptClient
class Client:
    def __init__(self, ipAddress, portNum = 8008, username = ''):
        self.username = username
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((ipAddress, portNum))
        except Exception as err:
            print("No connection found on host %s at port %s." % (ipAddress, portNum))
            self.clientSocket.close()
            exit()

        self.inputList = []
        self.inputList.append(self.clientSocket)
        self.inputList.append(sys.stdin)

        self.activeUsers = []
        self.encrypter = EncryptClient.EncryptClient()
        self.sendHandshake()
        return

    def runClient(self):
        while True:
            readyToRead, readyToWrite, inError = \
                     select.select(self.inputList, self.inputList, self.inputList)

            if self.clientSocket in readyToRead:
                packet = self.clientSocket.recv(289)
                self.manageClient(packet)
                self.handleMessage(packet)

            elif sys.stdin in readyToRead:
                for line in sys.stdin:
                    line = line.strip()
                    self.sendMessage(line)
                    break
                sys.stdout.flush()

    def handleMessage(self, packet):

        plainText = self.encrypter.decrypt(packet)

        source, dest, message = self.splitPacket(plainText)

        if dest == 'list':
            self.displayList(message)
        else:
            self._printMessage(source, dest, message)
        return

    #NOT BEING USED. CONSIDER REMOVING
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
        plainPacket = ''

        if detail[0] == '!private':
            dest_messae_pair = detail[1].split(' ', 1)
            plainPacket = self.constructPacket(dest_messae_pair[0], dest_messae_pair[1])

        elif detail[0] == '!all':
            plainPacket = self.constructPacket('allchat', detail[1])

        elif detail[0] == '!list':
            plainPacket = str(self.username + ':list')

        elif detail[0] == '!quit':
            self.quitProgram()

        else:
            print('Not a valid command')

        if len(plainPacket) <= 289:
            cipherPacket = self.encrypter.encrypt(plainPacket)
            self.clientSocket.send(cipherPacket)
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

    def manageClient(self, buffer):
        if len(buffer) == 0:
            self.quitProgram()

    def quitProgram(self):
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()
        exit(0)

    def sendHandshake(self):
        """
        The handshake involves sending an encrypted aes key and the username of this client
        """
        encryptedKey = self.encrypter.getEncryptedAESKey()
        self.clientSocket.send(encryptedKey)

        usermessage = str('username:' + self.username)
        encryptedUserMessage = self.encrypter.encrypt(usermessage)
        self.clientSocket.send(encryptedUserMessage)
        return

