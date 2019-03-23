import json

class Message:
    def __init__(self, data):
        self.sender = ''
        self.reciver = ''
        self.message = ''
        self.messageStructure = {}
        if type(data) == str:
            #do stuff
        elif type(data) == dict:
            #do stuff

    def _initStr(self, line):
        splitLine = line.split(' ', 2)
        self.sender = 

