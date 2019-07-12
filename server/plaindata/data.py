import json
import os

files = []

def loadFiles():
    files = []
    with open('files/manifest.json', 'r') as json_file:
        files = json.load(json_file)

    return files

def saveFiles():
    with open('files/manifest.json', 'w') as json_file:
        json.dump(files, json_file)