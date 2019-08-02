import json
import os

class localData:
    files = {}
    users = {}
    boards = {}

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

        try:
            with open('data/boards/user_manifest.json', 'r') as json_file:
                localData.boards = json.load(json_file)
        except:
            localData.boards = {}

    def addFileToManifest(uid, fid, fileAtts):
        localData.files[fid] = fileAtts

        uid = str(uid)
        
        if uid in localData.users:
            localData.users[uid].append(fid)
        else:
            localData.users[uid] = [ fid ]

    def addBoardToManifest(uid, bid):
        if uid in localData.boards:
            localData.boards[uid].append(bid)
        else:
            localData.boards[uid] = [ bid ]

    def generateFileId():
        if len(localData.files.keys()) == 0:
            return 0
        else:
            return int(list(localData.files.keys())[-1]) + 1

    def generateBoardId():
        if len(localData.boards.keys()) == 0:
            return 0
        else:
            return int(list(localData.boards.keys())[-1]) + 1

    def saveManifest():
        with open('data/files/manifest.json', 'w') as json_file:
            json.dump(localData.files, json_file, indent=4)

        with open('data/files/user_manifest.json', 'w') as json_file:
            json.dump(localData.users, json_file, indent=4)

        with open('data/boards/user_manifest.json', 'w') as json_file:
            json.dump(localData.boards, json_file, indent=4)