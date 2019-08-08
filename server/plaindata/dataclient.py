"""
    data server client class
"""

import sys
sys.path.append(r"C:\src\business-library\python")

from mundusinvicte.networking.sockets.TcpClient import TcpClient

import mundusinvicte.security.aes as aes

class DataClient(TcpClient):
    def __init__(self, socket, addr):
        super().__init__(socket, addr)
        self.validated = False

    """
        encrypts message using aes key and sends
    """
    def encAndSend(self, msg):
        self.send(8192, aes.encrypt(self.key, msg), False)