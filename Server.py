import sys
import socket
import asyncio

class Server:
    def __init__(self, portNum = 8008):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((socket.gethostname(), portNum))
        serversocket.listen(5)
        return
    
    
    async def runServer(): 
        return 
