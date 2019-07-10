import sys
sys.path.append(r"C:\src\business-library\python")

import mundusinvicte.security.rsa as rsa
import mundusinvicte.security.aes as aes

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
key = aes.generateKey()
enc_msg = aes.encrypt(key, MESSAGE)

# encrypt aes key and send
response = {
    "shared_key": rsa.encrypt_(rsa_key, key),
    "enc_msg": str(enc_msg)
}

dec = aes.decrypt(key, response['enc_msg'], True)

s.send(json.dumps(response).encode('utf_8'))

# get return message
response = s.recv(8192)

if response == dec:
    print("Secure connection established")
else:
    s.close()
    print("Unsecure connection, terminating")

while (True):
    pass