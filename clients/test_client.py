import sys
sys.path.append(r"C:\src\business-library\python")

import mundusinvicte.security.rsa as rsa
import mundusinvicte.security.aes as aes

import pyaes
import socket
import json
from base64 import b64encode

TCP_IP = '127.0.0.1'
TCP_PORT = 5500
BUFFER_SIZE = 8192
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((TCP_IP, TCP_PORT))

# send hello message
response = {
    "name": "Michael",
    "platform": "win32"
}

s.send(bytes(json.dumps(response), 'UTF-8'))

# receive public key
response = json.loads(s.recv(8192).decode('utf_8'))
rsa_key = (response['e'], response['N'])

# generate aes key
key = aes.generateKey().encode('utf8')
aes_ = pyaes.AESModeOfOperationCTR(key)
enc_msg = aes_.encrypt(MESSAGE)

# encrypt aes key and send
response = {
    "shared_key": rsa.encrypt_(rsa_key, key.decode('utf8')),
    "enc_msg": enc_msg.decode('latin1')
}

s.send(json.dumps(response).encode('utf_8'))

# get return message
response = s.recv(8192)

if response.decode('latin1') == MESSAGE:
    print("Secure connection established")
else:
    s.close()
    print("Insecure connection, terminating")
    sys.exit()

while (True):
    msg = input()

    if msg == "stop":
        break

    enc = aes_.encrypt(msg).decode('latin1')

    send = {
        "message": enc
    }
    s.send(json.dumps(send).encode('utf8'))