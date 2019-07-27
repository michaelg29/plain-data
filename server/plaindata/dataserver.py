import sys
sys.path.append(r"C:\src\business-library\python")

import json
import pyaes

from .dataclient import DataClient
from .request import Request
from .data.local import localData
from .data.git import saveFile, push

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
        print("client disconnected")

    def msgReceived(self, client, msg):
        if not client.validated:
            self.validateClient(client, msg)
            return

        req = Request(msg, client)
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
                self.clientFailedValidation(client)
                return

            # send public key
            response = {
                "e": str(self.pubKey[0]),
                "N": str(self.pubKey[1])
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
                client.key = rsa.decrypt_(self.__privKey, response['shared_key'])
                enc = response['enc_msg'][:-1].encode().decode('unicode-escape').encode('ISO-8859-1')

                dec = aes.decrypt(client.key, enc)
                client.send(8192, dec, False)

                client.validated = True
            except Exception as e:
                import traceback
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)

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