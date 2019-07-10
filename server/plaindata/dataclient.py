import sys
sys.path.append(r"C:\src\business-library\python")

from mundusinvicte.networking.sockets.TcpClient import TcpClient

class DataClient(TcpClient):
    def __init__(self, socket, addr):
        self.__super__(socket, addr)