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

# generate aes key
key = aes.generateKey().encode('utf8')
aes_ = pyaes.AESModeOfOperationCTR(key)

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
    msg = b""
    while True:
        data = s.recv(8192)

        isFinished = False
        try:
            isFinished = data[-8:] == b"finished"
        except Exception as e:
            print(e)
            msg += data
            continue
        
        if isFinished:
            msg += data[:-8]
            break
        else:
            msg += data

    try:
        msg = msg.decode()
    except: 
        msg = msg.decode('latin1')

    return msg

try:
    # send hello message
    response = {
        "name": "Michael",
        "platform": "win32"
    }

    sendMsg(json.dumps(response), True)
    print('sent hello')

    # receive public key
    response = json.loads(recv())
    rsa_key = (int(response['e']), int(response['N']))
    print('receive public key')

    # encrypt msg
    print("msg:",MESSAGE)
    enc_msg = aes_.encrypt(MESSAGE)

    # encrypt aes key and send
    response = {
        "shared_key": rsa.encrypt_(rsa_key, key.decode('utf8')),
        "enc_msg": enc_msg.decode('latin1')
    }

    sendMsg(json.dumps(response), True)
    print('send aes key')

    # get return message
    response = recv()
    print('get response')

    if response == MESSAGE:
        print("Secure connection established")
    else:
        s.close()
        print("Insecure connection, terminating")
        sys.exit()
except Exception as e:
    import traceback
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)

try:
    contents = open("C:\\Users\\micha\\Downloads\\error_func.pdf", "rb").read()

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