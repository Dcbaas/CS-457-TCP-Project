import socket
import select
import sys
import readchar
import asyncio

class Client:
    def __init__(self, ipAddress, portNum = 8008, username = ''):
        self.username = username
        self.clientSocket = socket.socket(socket_AF_INET, socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((ipAddress, portNum))
        except Exception as err:
            print("No connection found on host %s at port %s:d" % (ipAddress, portNum))
            self.clientSocket.close()
            exit()

        if self.username == '':
            self.username = input("Enter your username: ")

        self.inputList = []
        self.inputList.append(self.clientSocket);
        return

    def runClient():
        inputGiven = False
        inputGiven = await detectUserInput()

        while True:
            readyToRead, readyToWrite, inError = \
                     select.select(inputList, inputList, inputList)

            if self.clientSocket in readyToRead:
                message = clientSocket.recv(289)
                printMessage(message)

            if inputGiven == True:
                inputGiven = False
                sendMessage()
                inputGiven = await detectUserInput()


        return

    def handleMessage(packet):
        source, dest, message = splitPacket(packet)

        if source = 'list':
            displayList(message)
        else:
            _printMessage(source, dest, message)
        return

    def composeDirectMessage(line):
        messageDetail = line[1]:.split(' ', 1)
        return str(self.username + ':' + messageDetail[0] + ':' + messageDetail[1])

    def displayList(userList):
        print(Users:)
        for user in userList:
            print(userList)
        return

    def _printMessage(source, dest, message):
        '''
        Prints a standard message to the screen. If its a public message, the print statement marks
        the message as such 

        
        '''
        if dest == 'allchat':
            print(str(source + ' (Public):' + message)) 
        else:
            print(str(source + ': ' + message))
        return


    def sendMessage():
        #TODO
        return

    def splitPacket(packet):
        rawList = packet.split(":", 2)
        source = rawList[0]
        dest = rawList[1]
        detail = rawList[2]
        return source, dest, detail

    async def detectUserInput():
        ch = readchar.readchar()
        if ch == '/':
            return True

        return False

