import sys
sys.path.append(r"C:\src\business-library\python")

import mundusinvicte.security.rsa as rsa
import mundusinvicte.security.aes as aes

import pyaes
import socket
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 5500
BUFFER_SIZE = 8192
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((TCP_IP, TCP_PORT))

def sendMsg(msg, doEncode):
    send_b = msg.encode('utf8') if doEncode else msg
    send_b += b"finished"
    size = len(send_b)
    i = 0
    
    while i < size:
        if i > size - 8192:
            break
        s.send(send_b[i:i + 8192])
        i += 8192

    s.send(send_b[i:])

def recv():
    msg = ""
    while True:
        data = s.recv(8192).decode()
        if data[-8:] == "finished":
            msg += data[:-8]
            break
        msg += data

    return msg

# send hello message
response = {
    "name": "Michael",
    "platform": "win32"
}

sendMsg(json.dumps(response), True)

# receive public key
response = json.loads(recv())
rsa_key = (int(response['e'], 2), int(response['N'], 16))

# generate aes key
key = aes.generateKey().encode('utf8')
aes_ = pyaes.AESModeOfOperationCTR(key)
enc_msg = aes_.encrypt(MESSAGE)

# encrypt aes key and send
response = {
    "shared_key": rsa.encrypt_(rsa_key, key.decode('utf8')),
    "enc_msg": enc_msg.decode('latin1')
}

sendMsg(json.dumps(response), True)

# get return message
response = recv()

if response == MESSAGE:
    print("Secure connection established")
else:
    s.close()
    print("Insecure connection, terminating")
    sys.exit()

try:
    contents = open("C:\\Users\\Michael Grieco\\Downloads\\error_func.pdf", "rb").read()

    send = {
        "type": "upload-file",
        "filetype": "pdf",
        "filename": "error_func.pdf",
        "author": "Michael Grieco",
        "contents": contents.decode('latin1'),
    }

    send_s = aes_.encrypt(json.dumps(send))
    sendMsg(send_s, False)
except Exception as e:
    print(e)