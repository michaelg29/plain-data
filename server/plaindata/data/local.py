import json
import os

class localData:
    files = []

    def loadFiles():
        try:
            with open('data/files/manifest.json', 'r') as json_file:
                data.files = json.load(json_file)
        except:
            data.files = []

    def saveFiles():
        with open('data/files/manifest.json', 'w') as json_file:
            json.dump(data.files, json_file, indent=4)

    def writeFile(path, content, isBinary = False):
        if isBinary:
            with open("data/files/" + path, 'w') as f:
                f.write(content)
        else:
            with open("data/files/" + path, mode='wb') as out:
                out.write(content.encode('latin1'))