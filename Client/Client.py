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
           printMessage(message)
       elif sys.stdin in readyToRead:
           for line in sys.stdin:
               if line[0] == '/':
                   if line[1]: == 'list':
                       #make a list command
                       continue
                   else:
                       #make a DM for the person specified
                       packet = composeDirectMessage(line)
                       if len(packet) <= 289:
                           self.clientSocket.send(packet)
                       else:
                           print('Message too long. Was not sent')


    def printMessage(message):
        messageList = message.split(':', 2)
        #Print the user list if that was the message
        if messageList[0] == 'userlist':
            displayList(messageList)
            return
        #print an all chat message
        elif messagelist[1] == 'allchat':
            print(str(messagelist[0] + '(in public chat)' + messagelist[2]))
        #print a normal message
        else:
            print(str(messageList[0] + ':' + messageList[2]))
        return

    def composeDirectMessage(line):
        messageDetail = line[1]:.split(' ', 1)
        return str(self.username + ':' + messageDetail[0] + ':' + messageDetail[1])

    def displayList(userList):
        return

