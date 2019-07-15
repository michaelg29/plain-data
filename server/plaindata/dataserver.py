import sys
sys.path.append(r"C:\src\business-library\python")

import json
import pyaes

from .dataclient import DataClient
from .message import Message
from .data import data

from mundusinvicte.networking.sockets.TcpListener import TcpListener
import mundusinvicte.security.rsa as rsa
import mundusinvicte.security.aes as aes

class DataServer(TcpListener):
    def __init__(self, ipAddr, port):
        super().__init__(ipAddr, port, True)

        e, d, N = rsa.generateKeys(256)
        self.pubKey = (e, N)
        self.__privKey = (d, N)

    def generateClientObject(self, clientsock, clientaddr):
        return DataClient(clientsock, clientaddr)

    def serverStarted(self):
        print("Server started at", self.ipAddr, "on port", self.port)
        print(r"Type 'stop' to quit")

    def clientConnected(self, client):
        client.validationStage = 0

    def clientFailedValidation(self, client):
        client.send("Failed validation, disconnecting")
        self._clients.remove(client)
        self.clientDisconnected(client)
        client.sock.close()

    def clientDisconnected(self, client):
        pass

    def msgReceived(self, client, msg):
        if not client.validated:
            self.validateClient(client, msg)
            return

        req = Message(msg, client)
        req.parse()

    def validateClient(self, client, msg):
        """ tcp handshake """
        if client.validationStage == 0:
            # get client hello
            """
            {
                "name": "name",
                "platform": "platform"
            }
            """
            response = json.loads(msg)

            try:
                client.name = response['name']
                client.platform = response['platform']
            except Exception as e:
                print("DATASERVER -- 70:",e)
                self.clientFailedValidation(client)
                return

            # send public key
            response = {
                "e": '{0:00b}'.format(self.pubKey[0]),
                "N": format(self.pubKey[1], 'x')
            }
            client.send(8192, json.dumps(response))

            client.validationStage = 1
        elif client.validationStage == 1:
            # get shared key encrypted with public key
            """
            {
                "shared_key": "encrypted shared key",
                "enc_msg": "encrypted message
            }
            """
            response = json.loads(msg)

            try:
                client.key = rsa.decrypt_(self.__privKey, response['shared_key']).encode('utf8')
                client.aes = pyaes.AESModeOfOperationCTR(client.key)

                client.send(8192, client.aes.decrypt(response['enc_msg']), False)

                client.validated = True
            except Exception as e:
                print("DATASERVER -- 104:",e)
                self.clientFailedValidation(client)
                return

    def serverEvent(self, msg):
        print("SERVER>", msg)

    def cmdThread(self):
        while True:
            cmd = input()
            if cmd == "stop":
                print("Server shutting down")
                exit()