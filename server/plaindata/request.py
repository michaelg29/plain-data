import sys
sys.path.append(r"C:\src\business-library\python")

import json
import io

import mundusinvicte.security.aes as aes
from .data import data
from .utils import padNumber

class Request:
    def __init__(self, body, sender):
        self.sender = sender
        self.body = self.sender.aes.decrypt(body).decode('utf8')
        
    def get(self, key):
        return self.json_body[key]

    def parse(self):
        """
        {
            "type": "upload-file",
            "filetype": "pdf",
            "filename": "filename.pdf",
            "author": "author",
            "contents": "contents",
        }
        """

        try:
            self.json_body = json.loads(self.body)
            self.type = self.get('type')
        except Exception as e:
            print("MESSGAE -- 36:", e)

        if self.type == 'upload-file':
            try:
                self.filetype = self.get('filetype')
                self.filename = self.get('filename')
                self.author = self.get('author')
                self.contents = self.get('contents')

                atts = {
                    "filetype": self.filetype,
                    "filename": self.filename,
                    "author": self.author,
                    "id": padNumber(0, 6),
                }

                if len(data.files) != 0:
                    atts['id'] = padNumber(int(data.files[-1]["id"]) + 1, 6)

                data.files.append(atts)

                txt_types = [ "txt" ]
                b_types = [ "pdf" ]

                if self.filetype in txt_types:
                    with open('data/files/' + atts['id'] + '.' + self.filetype, 'w') as f:
                        f.write(self.contents)
                elif self.filetype in b_types:
                    with open("data/files/" + atts['id'] + '.' + atts['filetype'], mode='wb') as out:
                        out.write(self.contents.encode('latin1'))                    
            except Exception as e:
                pass
            finally:
                data.saveFiles()
        elif self.type == 'download-file':
            pass
        elif self.type == 'request':
            pass
        elif self.type == 'send':
            pass