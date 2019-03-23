import sys
import sys
import socket
import select
import EncryptServer

class Server:
    def __init__(self, portNum = 8008):
        self.socketList = []
        self.unKeyedSockets = []

        self.socketIpMapping = {}
        self.socketUserMapping = {}
        self.socketAesKeyMapping = {}

        self.users = []

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('', portNum))
        self.serversocket.listen(15)
        self.socketList.append(self.serversocket)

        #add stdin to the list for its use
        self.socketList.append(sys.stdin)

        self.encrypter = EncryptServer.EncryptServer()
        return

    def addUser(self, packet, socket):
        data = packet.split(':', 1)
        if data[0] == 'username':
            self.users.append(data[1])
            self.socketUserMapping.update({data[1]: socket})
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
                # We add to list of un keyed sockets to indicate that this socket hasn't sent a 
                # key to our server yet
                (clientSocket, clientAddress) = self.serversocket.accept()
                self.socketList.append(clientSocket)
                self.unKeyedSockets.append(clientSocket)

                self.socketIpMapping.update({clientAddress: clientSocket})
                print('New connection Established. Not Keyed yet')

            elif sys.stdin in readyToRead:
                for line in sys.stdin:
                    line = line.strip()
                    if line == '!list':
                        print(self.users)
                    elif line == '!quit':
                        [self.shutdownSocket(currentSocket) for currentSocket in self.socketList]
                        exit(0)
                    break;
                sys.stdout.flush()
            else:
                for socket in readyToRead:
                    if socket in self.unKeyedSockets:
                        print('Message from unkeyed socket')
                        # Get the key and add it to the socket key mapping
                        rawKey = socket.recv(256)
                        key = self.encrypter.rsaDecrypt(rawKey)
                        self.socketAesKeyMapping.update({socket:key})
                        self.unKeyedSockets.remove(socket)
                    else:
                        print('Incoming Message')
                        cipherPacket = []

                        #source username (16 + dest. username (16) + 255 char messg  + 2 ':' = 287
                        cipherPacket = socket.recv(305)

                        #Did the client close the connection? 
                        if self.manageSocket(socket, cipherPacket):
                            continue

                        #The client didn't close. Handle the packet
                        sourceKey = self.socketAesKeyMapping[socket]
                        plainPacket = self.encrypter.decrypt(cipherPacket,sourceKey)

                        if self.addUser(plainPacket, socket):
                            print('User added')
                            continue

                        listReturn = self.listRequest(plainPacket)
                        if listReturn != None:
                            print(listReturn)
                            cipherPacket = self.encrypter.encrypt(listReturn, sourceKey)
                            socket.send(cipherPacket)
                            continue

                        mssgSrc,mssgDest,text = self.splitPacket(plainPacket)

                        if mssgDest == 'allchat':
                            #Broadcast to all but stdin and the sending socket
                            print(plainPacket)
                            for dest in readyToWrite:
                                if not(dest == sys.stdin or dest == socket or dest == self.serversocket):
                                    destinationKey = self.socketAesKeyMapping[dest]
                                    cipherPacket = self.encrypter.encrypt(plainPacket, destinationKey)
                                    dest.send(cipherPacket)

                        else:
                            if mssgDest in self.socketUserMapping:
                                destSocket = self.socketUserMapping[mssgDest]
                                destinationKey = self.socketAesKeyMapping[destSocket]

                                cipherPacket = self.encrypter.encrypt(plainPacket,destinationKey)
                                destSocket.send(cipherPacket)
                            else:
                                plainPacket = 'Server:error:The person you are trying to contact is not connected to the server'
                                cipherPacket = self.encrypter.encrypt(plainPacket, sourceKey)
                                socket.send(cipherPacket)
                                #Send an error cause it didn't exist
                                continue

    def splitPacket(self, packet):
        message = packet.split(':')
        sourceUser = message[0]
        destUser = message[1]
        text = message[2]
        return sourceUser, destUser, text

    def listRequest(self, packet):
        data = packet.split(':', 1)
        print(data)
        if data[1] == 'list':
            returnList ='Server:' + 'list:' + ''.join(str(user + ':') for user in self.users)
            print(returnList)
            return returnList
        return None

    def findUserIp(self, destUser):
        for user in self.users:
            if user.getUsername() == destUser:
                return user.getIpAddress()
        return False

    def manageSocket(self, socket, buffer):
        if len(buffer) == 0:
            self.shutdownSocket(socket)
            #Remove the socket from the input list and the user:socket dictionary 
            self.socketList.remove(socket)
            for user, clientSocket in self.socketUserMapping.items():
                if clientSocket == socket:
                    del self.socketUserMapping[user]
                    self.users.remove(user)
                    return True
        return False

    def shutdownSocket(self, currentSocket):
        if currentSocket != sys.stdin:
            currentSocket.shutdown(socket.SHUT_RDWR)
            currentSocket.close()
        return

    def quitServer(self):
        for socket in self.socketList:
            if socket == sys.stdin:
                continue
            else:
                socket.close()


