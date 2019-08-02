import sys
sys.path.append(r"C:\src\business-library\python")

import json
import io

import mundusinvicte.security.aes as aes
from .data.local import localData
from .utils import padNumber

from .models.user import validateUser, createUser, setFlag, saveUser
from .models.file import upload, download, search
from .models.board import createBoard, comment, boardSearch, retrieve

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
    SEARCH = "search"
    RETRIEVE = "retrieve"

class FileActions:
    UPLOAD = "upload"
    DOWNLOAD = "download"
    EDIT = "edit"
    SEARCH = "search"

class Request:
    def __init__(self, body, sender):
        self.sender = sender
        self.body = aes.decrypt(self.sender.key, body)

        self.response = {}
        
    def get(self, key):
        return self.json_body[key]

    def getClientVal(self, key):
        return self.json_body['values'][key]

    def setSuccess(self):
        self.set('response', True)

    def setInvalid(self, reason):
        self.set('response', False)
        self.response['reasons'].append(reason)

    def setInvalidWithMultipleErrors(self, reasons):
        for reason in reasons:
            self.setInvalid(reason)

    def invalidType(self):
        self.setInvalid('format:type:invalid')

    def invalidAction(self):
        self.setInvalid('format:action:invalid')

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
            self.set("reasons", [])

            if self.type == Types.ACCOUNT:
                if self.action == AccountActions.LOGIN:
                    uname = self.getClientVal('u')
                    pwd = self.getClientVal('p')

                    results = validateUser(uname, pwd)

                    if results:
                        self.setSuccess()
                        user_values = {
                            "i": results[0],
                            "l": results[1],
                            "f": results[2],
                            "e": results[3]
                        }
                        self.set('values', user_values)
                    else:
                        self.setInvalidWithMultipleErrors('login:failed')
                elif self.action == AccountActions.CREATE:
                    user_ = {
                        "LastName": self.getClientVal('l'),
                        "FirstName": self.getClientVal('f'),
                        "Username": self.getClientVal('u'),
                        "Password": self.getClientVal('p'),
                        "Email": self.getClientVal('e')
                    }

                    results = createUser(user_)

                    if results['result']:
                        self.setSuccess()
                        self.set('values', { 'i' : results['id'] })
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == AccountActions.FORGOT:
                    id = self.getClientVal('i')
                    email = self.getClientVal('e')

                    results = setFlag(id, email, 'password:forgot')

                    if results['result']:
                        self.setSuccess()
                        # TODO: Send email to user
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == AccountActions.UPDATE:
                    user_ = {
                        "LastName": self.getClientVal('l'),
                        "FirstName": self.getClientVal('f'),
                        "Username": self.getClientVal('u'),
                        "Password": self.getClientVal('p'),
                        "Email": self.getClientVal('e')
                    }

                    results = saveUser(user_)

                    if results['result']:
                        self.setSuccess()
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                else:
                    self.invalidAction()
            elif self.type == Types.BOARD:
                if self.action == BoardActions.CREATE:
                    results = createBoard(self.get('values'))

                    if results['result']:
                        self.setSuccess()
                        self.set('values', { 'id': results['id'] })
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == BoardActions.UPDATE:
                    pass
                elif self.action == BoardActions.COMMENT:
                    results = createBoard(self.get('values'))

                    if results['result']:
                        self.setSuccess()
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == BoardActions.SEARCH:
                    results = boardSearch(self.get('values'))

                    if results['result']:
                        self.setSuccess()
                        self.set('list', results['list'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == BoardActions.RETRIEVE:
                    results = retrieve(self.getClientVal('id'))

                    if results['result']:
                        self.set('values', result['values'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                else:
                    self.invalidAction()
            elif self.type == Types.FILE:
                if self.action == FileActions.UPLOAD:
                    results = upload(self.get('values'))

                    if results['result']:
                        self.setSuccess()
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == FileActions.EDIT:
                    pass
                elif self.action == FileActions.DOWNLOAD:
                    results = download(self.getClientVal('fid'))

                    if results['result']:
                        self.setSuccess()
                        self.set('values', results['values'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == FileActions.SEARCH:
                    results = search(self.get('values'))

                    if results['result']:
                        self.setSuccess()
                        self.set('list', results['list'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                else:
                    self.invalidAction()
            else:
                self.invalidType()

            self.sender.encAndSend(json.dumps(self.response))

        except:
            import traceback
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)