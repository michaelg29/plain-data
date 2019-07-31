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

class BoardActions:
    CREATE = "create"
    UPDATE = "update"
    COMMENT = "comment"

class FileActions:
    UPLOAD = "upload"
    DOWNLOAD = "download"
    EDIT = "edit"

class Request:
    def __init__(self, body, sender):
        self.sender = sender
        self.body = aes.decrypt(self.sender.key, body)

        self.response = {}
        
    def get(self, key):
        return self.json_body[key]

    def setInvalid(self, result, reasons):
        self.set('response', result)
        self.response['reasons'].append(reasons)

    def invalidType(self):
        self.setInvalid('format-error', 'type:invalid')

    def invalidAction(self):
        self.setInvalid('format-error', 'action:invalid')

    def set(self, key, value):
        self.response[key] = value

    def parse(self):
        """

            sample request

            {
                "reqId": "reqId",
                "type": "account"|"file"|"board",
                "action": "action",
                "values": {

                }
            }

        """

        try:
            self.json_body = json.loads(self.body)
            
            self.set('reqId', self.get('reqId'))

            self.type = self.get('type')
            self.action = self.get('action')
            self.reasons = []

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
                        self.set('values', user_values)
                    else:
                        self.setInvalid('login-fail', [])
                elif self.action == AccountActions.CREATE:
                    pass
                elif self.action == AccountActions.FORGOT:
                    pass
                elif self.action == AccountActions.UPDATE:
                    pass
                else:
                    self.invalidAction()
            elif self.type == Types.BOARD:
                if self.action == BoardActions.CREATE:
                    pass
                elif self.action == BoardActions.UPDATE:
                    pass
                elif self.action == BoardActions.COMMENT:
                    pass
                else:
                    self.invalidAction()
            elif self.type == Types.FILE:
                if self.action == FileActions.UPLOAD:
                    pass
                elif self.action == FileActions.EDIT:
                    pass
                elif self.action == FileActions.DOWNLOAD:
                    pass
                else:
                    self.invalidAction()
            else:
                self.invalidType()

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