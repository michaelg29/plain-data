import json
import os

class data:
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