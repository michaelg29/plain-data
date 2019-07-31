import sys
sys.path.append(r"C:\src\business-library\python")

import json
import io

import mundusinvicte.security.aes as aes
from .data.local import localData
from .utils import padNumber

from .models.user import validateUser

class Types:
    ACCOUNT = "account"
    BOARD = "board"
    FILE = "file"

class AccountActions:
    LOGIN = "login"
    CREATE = "create"
    UPDATE = "update"
    FORGOT = "forgot"

class Request:
    def __init__(self, body, sender):
        self.sender = sender
        self.body = aes.decrypt(self.sender.key, body)

        self.response = {}
        
    def get(self, key):
        return self.json_body[key]

    def setInvalid(self, result, reasons):
        self.set('response', result)
        self.set('reasons', reasons)

    def set(self, key, value):
        self.response[key] = value

    def parse(self):
        try:
            self.json_body = json.loads(self.body)
            
            self.set('reqId', self.get('reqId'))

            self.type = self.get('type')
            self.action = self.get('action')

            if self.type == Types.ACCOUNT:
                if self.action == AccountActions.LOGIN:
                    uname = self.get('values')['u']
                    pwd = self.get('values')['p']

                    results = validateUser(uname, pwd)

                    if results:
                        self.set('result', 'login-success')
                        user_values = {
                            "i": results[0],
                            "l": results[1],
                            "f": results[2],
                            "e": results[3]
                        }
                    else:
                        self.setInvalid('login-fail', [])
            elif self.type == Types.BOARD:
                pass
            elif self.type == Types.FILE:
                pass
            else:
                self.setInvalid('format-error', [ 'type:invalid' ])

            self.sender.encAndSend(json.dumps(self.response))

        except:
            import traceback
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)

# if self.type == 'upload-file':
#     print('upload file request')
#     try:
#         self.contents = self.get('contents')

#         atts = {
#             "filetype": self.get('filetype'),
#             "filename": self.get('filename'),
#             "author": self.get('author'),
#             "id": padNumber(0, 6),
#         }

#         if len(localData.files) != 0:
#             atts['id'] = padNumber(int(localData.files[-1]["id"]) + 1, 6)

#         localData.files.append(atts)

#         txt_types = [ "txt" ]
#         b_types = [ "pdf" ]

#         localData.writeFile(atts['id'] + '.' + atts['filetype'], atts['filetype'] in b_types)
#     except Exception as e:
#         pass
#     finally:
#         data.saveFiles()
# elif self.type == 'download-file':
#     pass
# elif self.type == 'request':
#     pass
# elif self.type == 'send':
#     pass