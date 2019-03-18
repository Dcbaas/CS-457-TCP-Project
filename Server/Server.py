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
        self.serversocket.bind((socket.gethostname(), portNum))
        self.serversocket.listen(15)
        self.socketList.append(self.serversocket)

        #add stdin to the list for its use
        self.socketList.append(sys.stdin)
        return

    def runServer(self): 
        while True:
            readyToRead, readyToWrite, hasError = \
                    select.select(
                            self.socketList, 
                            self.socketList, 
                            self.socketList)
            if self.serversocket in readyToRead:
                # A new connection established adding it to the list of sockets
                (clientSocket, clientAddress) = serversocket.accept()
                socketList.append(clientSocket)
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
                    mssgLen = socket.recv(289)
                    mssgSrc,mssgDest,text = splitPacket(messgBuffer)

                    if mssgDest == 'allchat':
                        #dostuff
                        print('do allchat stuff')
                    else:
                        destIP = findUserIp(mssgDest)

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
        text = message[3]
        return sourceUser, destUser, text

    #DEPRICATED AFTER NO USE
    def constructPacket(self, source,dest,text):
        return str(source + ':' + dest + ':' + text)

    def allChatMessg(self, packet, socketList):
        return

    def findUserIp(self, destUser):
        for user in self.users:
            if user.getUsername() == destUser:
                return user.getIpAddress()
        return False

