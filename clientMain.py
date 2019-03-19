#!/usr/bin/env python

import Client
import sys

ipAddress = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
portNumber = int(sys.argv[2]) if len(sys.argv) > 2 else 8008
username = sys.argv[3] if len(sys.argv) > 3 else 'Dave'

client = Client.Client('localhost',8008, 'Dave')
client.runClient()

