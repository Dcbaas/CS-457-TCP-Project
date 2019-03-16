import socket;

class ClientSocket:
    def __init__(self, userName):
        self.userName = userName
        #TODO Padd the username with spaces if its less than 16 chars
        self.clientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.clientSocket == None:
            print('The socket couldn\'t be setup')

    def connect(self, ipAddress = 'localhost', portNumber = 8008):
        """ Do I need an error here?
        """
        self.clientSocket.connect((ipAddress, portNumber))
        return

    async def reciveMessage(self):
        messg = clientSocket.recv(271)
        return messg

    def sendMessage(self, messg):
        sendBuff = ''.join([self.userName, messg])

        clientSocket.send(sendBuff)
        return
    def disconnect(self):
        clientSocket.close()
        return

