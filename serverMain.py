#!/usr/bin/env python
import sys
from Server import Server

portNum = 8008
password = 'password'

if len(sys.argv) == 3:
    portNum = int(sys.argv[1])
    password = str(sys.argv[2])
elif len(sys.argv) != 1:
    print('Usage: ./serverMain.py <port number>')
    print('OR: ./serverMain.py')
    exit(1)

server = Server(portNum, password)
server.runServer()

