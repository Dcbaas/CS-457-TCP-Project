#!/usr/bin/env python

import Client
import sys

ipAddress = 'localhost'
portNumber = 8008
username = 'Dave'

if len(sys.argv) == 4:
    ipAddress = sys.argv[1]
    portNumber = int(sys.argv[2])
    username = sys.argv[3]
elif len(sys.argv) != 0:
    print('Usage: ./clientMain.py <ip address> <port number> <username>')
    print('OR: ./clientMain.py')
    exit(1)

client = Client.Client('localhost',8008, 'Dave')
client.runClient()

