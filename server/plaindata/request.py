import sys
sys.path.append(r"C:\src\business-library\python")

import json
import io

import mundusinvicte.security.aes as aes
from .data.local import localData
from .utils import padNumber

class Request:
    def __init__(self, body, sender):
        self.sender = sender
        self.body = self.sender.aes.decrypt(body).decode('utf8')
        
    def get(self, key):
        return self.json_body[key]

    def parse(self):
        try:
            self.json_body = json.loads(self.body)
            self.type = self.get('type')
        except Exception as e:
            print("MESSGAE -- 36:", e)

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