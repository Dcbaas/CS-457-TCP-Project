#!/usr/bin/env python
import sys
import Server

portNum = 8008
if len(sys.argv) == 2:
    portNum = int(sys.argv[1])
elif len(sys.argv) != 0:
    print('Usage: ./serverMain.py <port number>')
    print('OR: ./serverMain.py')
    exit(1)

server = Server.Server(portNum)
server.runServer()

