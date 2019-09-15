"""
    request class
"""

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

"""
    types for requests
"""
class Types:
    ACCOUNT = "account"
    BOARD = "board"
    FILE = "file"

"""
    request actions for type account
"""
class AccountActions:
    LOGIN = "login"
    CREATE = "create"
    UPDATE = "update"
    FORGOT = "forgot"

"""
    request actions for type board
"""
class BoardActions:
    CREATE = "create"
    UPDATE = "update"
    COMMENT = "comment"
    SEARCH = "search"
    RETRIEVE = "retrieve"

"""
    request actions for type file
"""
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
        
    """
        returns request parameter with specified key
    """
    def get(self, key):
        return self.json_body[key]

    """
        gets value with specified key from 'values' attribute
    """
    def getClientVal(self, key):
        return self.get('values')[key]

    """
        sets response to False due to specified reason
    """
    def setInvalid(self, reason):
        self.set('response', False)
        self.response['reasons'].append(reason)

    """
        sets response to False due to specified reasons
    """
    def setInvalidWithMultipleErrors(self, reasons):
        self.set('response', False)
        for reason in reasons:
            self.response['reasons'].append(reason)

    """
        sets response to False because of invalid type
    """
    def invalidType(self):
        self.setInvalid('format:type:invalid')

    """
        sets response to False because of invalid action
    """
    def invalidAction(self):
        self.setInvalid('format:action:invalid')

    """
        sets value of response
    """
    def set(self, key, value):
        self.response[key] = value

    """
        parse request body
    """
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
            # load json body
            self.json_body = json.loads(self.body)
            
            # set request id of response to that of request to ensure they match up
            self.set('reqId', self.get('reqId'))

            # get type and action
            self.type = self.get('type')
            self.action = self.get('action')

            # set default values for response
            self.set('response', True)
            self.set("reasons", [])

            if self.type == Types.ACCOUNT:
                if self.action == AccountActions.LOGIN:
                    # get username and password
                    uname = self.getClientVal('u')
                    pwd = self.getClientVal('p')

                    # get results from validation function
                    results = validateUser(uname, pwd)

                    # parse results
                    if results:
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
                    # get user metadata
                    user_ = {
                        "LastName": self.getClientVal('l'),
                        "FirstName": self.getClientVal('f'),
                        "Username": self.getClientVal('u'),
                        "Password": self.getClientVal('p'),
                        "Email": self.getClientVal('e')
                    }

                    # get results from createUser function
                    results = createUser(user_)

                    # parse results
                    if results['result']:
                        self.set('values', { 'i' : results['id'] })
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == AccountActions.FORGOT:
                    # get user id and email
                    id = self.getClientVal('i')
                    email = self.getClientVal('e')

                    # get results from setFlag function
                    results = setFlag(id, email, 'password:forgot')

                    # parse results
                    if results['result']:
                        # TODO: Send email to user
                        pass
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == AccountActions.UPDATE:
                    # get user metadata
                    user_ = {
                        "LastName": self.getClientVal('l'),
                        "FirstName": self.getClientVal('f'),
                        "Username": self.getClientVal('u'),
                        "Password": self.getClientVal('p'),
                        "Email": self.getClientVal('e')
                    }

                    # get results from saveUser function
                    results = saveUser(user_)

                    # parse results
                    if results['result']:
                        pass
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                else:
                    self.invalidAction()
            elif self.type == Types.BOARD:
                if self.action == BoardActions.CREATE:
                    # get results from createBoard function using passed in metadata
                    results = createBoard(self.get('values'))

                    # parse results
                    if results['result']:
                        self.set('values', { 'id': results['id'] })
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == BoardActions.UPDATE:
                    pass
                elif self.action == BoardActions.COMMENT:
                    # get results from comment function using passed in metadata
                    results = comment(self.get('values'))

                    # parse results
                    if results['result']:
                        pass
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == BoardActions.SEARCH:
                    # get results from search function using passed in parameters
                    results = boardSearch(self.get('values'))

                    # parse results
                    if results['result']:
                        self.set('list', results['list'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == BoardActions.RETRIEVE:
                    # get results from retrieve function using passed in id
                    results = retrieve(self.getClientVal('id'))

                    # parse results
                    if results['result']:
                        self.set('values', results['values'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                else:
                    self.invalidAction()
            elif self.type == Types.FILE:
                if self.action == FileActions.UPLOAD:
                    # get results from upload function using passed in metadata
                    results = upload(self.get('values'))

                    # parse results
                    if results['result']:
                        pass
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == FileActions.EDIT:
                    pass
                elif self.action == FileActions.DOWNLOAD:
                    # get results from download function using passed in file id
                    results = download(self.getClientVal('fid'))

                    # parse results
                    if results['result']:
                        self.set('values', results['values'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                elif self.action == FileActions.SEARCH:
                    # get results from search function using passed in parameters
                    results = search(self.get('values'))

                    # parse results
                    if results['result']:
                        self.set('list', results['list'])
                    else:
                        self.setInvalidWithMultipleErrors(results['reasons'])
                else:
                    self.invalidAction()
            else:
                self.invalidType()

            # encrypt and send response
            self.sender.encAndSend(json.dumps(self.response))

        except:
            import traceback
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)