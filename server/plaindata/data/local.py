import json
import os

class localData:
    files = {}
    users = {}

    def loadManifest():
        try:
            with open('data/files/manifest.json', 'r') as json_file:
                localData.files = json.load(json_file)
        except:
            localData.files = {}

        try:
            with open('data/files/user_manifest.json', 'r') as json_file:
                localData.users = json.load(json_file)
        except:
            localData.users = {}

    def addToManifest(uid, fid, fileAtts):
        localData.files[fid] = fileAtts

        uid = str(uid)
        
        if uid in localData.users:
            localData.users[uid].append(fid)
        else:
            localData.users[uid] = [ fid ]

    def updateManifest(uid, fileid, fileAtts):
        pass

    def generateFileId():
        if len(localData.files.keys()) == 0:
            return 0
        else:
            return int(list(localData.files.keys())[-1]) + 1

    def saveManifest():
        with open('data/files/manifest.json', 'w') as json_file:
            json.dump(localData.files, json_file, indent=4)

        with open('data/files/user_manifest.json', 'w') as json_file:
            json.dump(localData.users, json_file, indent=4)