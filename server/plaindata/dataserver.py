"""
    data server class
"""

import sys
sys.path.append(r"C:\src\business-library\python")

import json

from .dataclient import DataClient
from .request import Request
from .data.local import localData
from .data.git import saveFile, push
from .data.sql import sql

from .models import user

from mundusinvicte.networking.sockets.TcpListener import TcpListener
import mundusinvicte.security.rsa as rsa
import mundusinvicte.security.aes as aes

class DataServer(TcpListener):
    def __init__(self, ipAddr, port):
        super().__init__(ipAddr, port, True)

        e, d, N = rsa.generateKeys(256)
        self.pubKey = (e, N)
        self.__privKey = (d, N)

    """
        gets object of type DataClient with socket and address
    """
    def generateClientObject(self, clientsock, clientaddr):
        return DataClient(clientsock, clientaddr)

    """
        server started callback
    """
    def serverStarted(self):
        print("Server started at", self.ipAddr, "on port", self.port)
        print("Type 'stop' to quit")

        localData.loadManifest()
        sql.sql_init()

        print("=" * 30, '\n\n')

    """
        client connected callback
    """
    def clientConnected(self, client):
        client.validationStage = 0

    """
        execution process if client is not validated
    """
    def clientFailedValidation(self, client):
        client.send("Failed validation, disconnecting")
        self._clients.remove(client)
        self.clientDisconnected(client)
        client.sock.close()

    """
        client disconnected callback
    """
    def clientDisconnected(self, client):
        print("client disconnected")

    """
        message received callback
    """
    def msgReceived(self, client, msg):
        if not client.validated:
            self.validateClient(client, msg)
            return

        msg = ''.join([chr(int(val)) for val in msg.split(',')])
        req = Request(msg, client)
        req.parse()

    """
        client validation process
    """
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
            print("received hello message")

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
            print('sent public key')

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
            print("received aes key")
            try:
                client.key = rsa.decrypt_(self.__privKey, response['shared_key'])
                enc = ''.join([chr(val) for val in response['enc_msg'].values()])

                dec = aes.decrypt(client.key, enc)
                client.send(8192, dec, False)
                print("sent decryption message")

                client.validated = True
                print("client validated")
            except Exception as e:
                import traceback
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)

                self.clientFailedValidation(client)
                return

    """
        server event callback
    """
    def serverEvent(self, msg):
        print("SERVER>", msg)

    """
        command thread callback
    """
    def cmdThread(self):
        while True:
            cmd = input()
            if cmd == "stop":
                print("Server shutting down")
                localData.saveManifest()
                sql.sql_cleanup()
                exit()