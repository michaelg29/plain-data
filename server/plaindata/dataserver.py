import sys
sys.path.append(r"C:\src\business-library\python")

import json
import pyaes

from .dataclient import DataClient
from .request import Request

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
        """ tcp handshake """
        
        # get client hello
        """
        {
            "name": "name",
            "platform": "platform"
        }
        """
        response = json.loads(client.sock.recv(8192).decode('utf8'))

        try:
            client.name = response['name']
            client.platform = response['platform']
        except Exception as e:
            self.clientFailedValidation(client)
            return

        # send public key
        response = {
            "e": self.pubKey[0],
            "N": self.pubKey[1]
        }
        client.send(json.dumps(response))

        # get shared key encrypted with public key
        """
        {
            "shared_key": "encrypted shared key",
            "enc_msg": "encrypted message
        }
        """
        response = json.loads(client.sock.recv(16384).decode('utf_8'))

        try:
            client.key = rsa.decrypt_(self.__privKey, response['shared_key']).encode('utf8')
            client.aes = pyaes.AESModeOfOperationCTR(client.key)

            client.send(client.aes.decrypt(response['enc_msg']), False)
        except Exception as e:
            print(e)
            self.clientFailedValidation(client)
            return

        client.validated = True
        print("client is validated")

    def clientFailedValidation(self, client):
        client.send("Failed validation, disconnecting")
        self._clients.remove(client)
        self.clientDisconnected(client)
        client.sock.close()

    def clientDisconnected(self, client):
        pass

    def msgReceived(self, client, msg):
        if not client.validated:
            return

        req = Request(msg, client)
        req.parse()

    def serverEvent(self, msg):
        print("SERVER>", msg)

    def cmdThread(self):
        cmd = input()
        if cmd == "stop":
            print("Server shutting down")
            exit()