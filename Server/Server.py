import sys
import sys
import socket
import select
import asyncio

class Server:
    def __init__(self, portNum = 8008):
        self.socketList = []
        self.socketIpMapping = {}
        self.users = []

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('', portNum))
        self.serversocket.listen(15)
        self.socketList.append(self.serversocket)

        #add stdin to the list for its use
        self.socketList.append(sys.stdin)
        return

    def addUser(self, packet):
        data = packet.split(':', 1)
        if data[0] == 'username':
            self.users.append(data[1])
            return True
        return False

    def runServer(self): 
        while True:
            readyToRead, readyToWrite, hasError = \
                    select.select(
                            self.socketList, 
                            self.socketList, 
                            self.socketList)
            if self.serversocket in readyToRead:
                # A new connection established adding it to the list of sockets
                (clientSocket, clientAddress) = self.serversocket.accept()
                self.socketList.append(clientSocket)
                self.socketIpMapping.update({clientAddress: clientSocket})
            elif sys.stdin in readyToRead:
                #do stuff
                print('Got message from stdin')
                for i in sys.stdin:
                    print('got ' + i)
                    break
                sys.stdout.flush()
            else:
                for socket in readyToRead:
                    messgBuffer = []
                    #source username (16 + dest. username (16) + 255 char messg = 287
                    messgBuffer = socket.recv(289)
                    messgBuffer = messgBuffer.decode()
                    result = self.addUser(messgBuffer)
                    if result == True:
                        continue

                    mssgSrc,mssgDest,text = self.splitPacket(messgBuffer)

                    if mssgDest == 'allchat':
                        #dostuff
                        print('do allchat stuff')
                    else:
                        destIP = self.findUserIp(mssgDest)

                        if destIP == False:
                            #return error to source and contiune
                            continue
                        else: 
                            destSocket = socketIpMapping[destIP]
                            destSocket.send(messgBuffer)

    def splitPacket(self, packet):
        message = packet.split(':')
        sourceUser = message[0]
        destUser = message[1]
        text = message[2]
        return sourceUser, destUser, text

    def allChatMessg(self, packet, socketList):
        return

    def findUserIp(self, destUser):
        for user in self.users:
            if user.getUsername() == destUser:
                return user.getIpAddress()
        return False

