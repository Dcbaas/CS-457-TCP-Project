from enum import Enum
import socket
import select
import sys

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
        self.inputList.append(sys.stdin)
        return

    def runClient():
        readyToRead, readyToWrite, inError = \
                select.select(inputList, inputList, inputList)

        if self.clientSocket in readyToRead:
           message = clientSocket.recv(289)
           #TODO implement the rest of this method


    def printMessage(message):
        messageList = message.split(':', 2)
        if messageList[1] == 'allchat':
            print(str(messageList[0] + '(In public chat)' + messageList[2]))
        else:
            print(str(messageList[0] + ':' + messageList[2]))
        return


class Command(Enum):
    LIST_USERS = '/list'
    EXIT = '/exit'
