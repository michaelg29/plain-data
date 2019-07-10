import sys
sys.path.append(r"C:\src\business-library\python")

from .dataclient import DataClient
from .request import Request

from mundusinvicte.networking.sockets.TcpListener import TcpListener

class DataServer(TcpListener):
    def __init__(self, ipAddr, port):
        super().__init__(ipAddr, port, True)

    def generateClientObject(self, clientsock, clientaddr):
        return DataClient(clientsock, clientaddr)

    def serverStarted(self):
        print("Server started at", self.ipAddr, "on port", self.port)
        print(r"Type 'stop' to quit")

    def clientConnected(self, client):
        client = DataClient(client.sock, client.addr)
        self.clients.append(client)

    def clientDisconnected(self, client):
        pass

    def msgReceived(self, client, msg):
        req = Request(msg, )

    def serverEvent(self, msg):
        print("SERVER>", msg)

    def cmdThread(self):
        cmd = input()
        if cmd == "stop":
            print("Server shutting down")
            exit()