import sys
sys.path.append(r"C:\src\business-library\python")

import json

import mundusinvicte.security.aes as aes

class Request:
    def __init__(self, body, sender):
        self.body = body
        self.sender = sender

    def parse(self):
        self.json_body = json.loads(self.body)

        print("encrypted msg:", self.json_body['message'])
        print("decrypted msg:", self.sender.aes.decrypt(self.json_body['message']).decode('utf8'))
