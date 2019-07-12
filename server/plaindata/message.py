import sys
sys.path.append(r"C:\src\business-library\python")

import json

import mundusinvicte.security.aes as aes

from .data import files, saveFiles

class Message:
    def __init__(self, body, sender):
        self.sender = sender
        self.body = self.sender.aes.decrypt(body).decode('utf8')

    def get(self, key):
        return self.json_body(key)

    def parse(self):
        print("parse")
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
            print(self.type)
        except Exception as e:
            print(e)

        if self.type == 'upload-file':
            print('upload')
            try:
                self.filetype = self.get('filetype')
                self.filename = self.get('filename')
                self.author = self.get('author')
                self.contents = self.get('contents')

                atts = {
                    "filetype": self.filetype,
                    "filename": self.filename,
                    "author": self.author,
                    "id": str(int(files[-1]["id"]) + 1)
                }

                print(atts)

                files.append(atts)

                print(files)

                with open('files/' + atts['id'] + '.' + self.filetype, 'w') as f:
                    f.write(self.contents)

                saveFiles()
            except Exception as e:
                print(e)
        elif self.type == 'download-file':
            pass
        elif self.type == 'request':
            pass
        elif self.type == 'send':
            pass
