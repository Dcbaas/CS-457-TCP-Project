import socket
import select
import sys
import readchar
import asyncio

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

        if self.username == '':
            self.username = input("Enter your username: ")

        self.inputList = []
        self.inputList.append(self.clientSocket);

        self.activeUsers = []
        return

    def runClient(self):
        inputGiven = False
        inputGiven = async_to_sync(detectUserInput)()

        while True:
            readyToRead, readyToWrite, inError = \
                     select.select(inputList, inputList, inputList)

            if self.clientSocket in readyToRead:
                message = clientSocket.recv(289)
                handleMessage(message)

            if inputGiven == True:
                inputGiven = False
                sendMessage()
                inputGiven = async_to_sync(detectUserInput)()

    def handleMessage(self, packet):
        source, dest, message = splitPacket(packet)

        if source == 'list':
            displayList(message)
        else:
            _printMessage(source, dest, message)
        return

    def composeDirectMessage(self, line):
        messageDetail = line[1:].split(' ', 1)
        return str(self.username + ':' + messageDetail[0] + ':' + messageDetail[1])

    def displayList(self, userList):
        print('Users:')
        for user in userList:
            print(userList)
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


    def sendMessage(self):
        raw_messsage = input(self.username + ': ')
        detail = raw_messsage.split(' ', 1)
        packet = ''

        if detail[0] == '!private':
            dest_messae_pair = detail[1].split(' ', 1)
            packet = constructPacket(dest_messae_pair[0], dest_messae_pair[1])
        elif detail[0] == '!all':
            packet = constructPacket('allchat', detail[1])

        elif detail[0] == '!list':
            packet = str(username + ':list')

        elif detail[0] == '!quit':
            quitProgram()

        else:
            print('Not a valid command')

        if len(packet) <= 289:
            clientSocket.send(packet)
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

    async def detectUserInput(self):
        ch = readchar.readchar()
        if ch == '/':
            return True

        return False

    def quitProgram(self):
        clientSocket.shutdown()
        clientSocket.close()
        exit(0)

