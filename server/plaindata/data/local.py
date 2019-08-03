import json
import os

class localData:
    files = {}
    file_users = {}
    boards = {}
    board_users = {}

    def loadManifest():
        try:
            with open('data/files/manifest.json', 'r') as json_file:
                localData.files = json.load(json_file)
        except:
            localData.files = {}

        try:
            with open('data/files/user_manifest.json', 'r') as json_file:
                localData.file_users = json.load(json_file)
        except:
            localData.file_users = {}

        try:
            with open('data/boards/manifest.json', 'r') as json_file:
                localData.boards = json.load(json_file)
        except:
            localData.boards = {}

        try:
            with open('data/boards/user_manifest.json', 'r') as json_file:
                localData.board_users = json.load(json_file)
        except:
            localData.boards = {}

    def addFileToManifest(uid, fid, fileAtts):
        localData.files[fid] = fileAtts

        uid = str(uid)
        
        if uid in localData.file_users:
            localData.file_users[uid].append(fid)
        else:
            localData.file_users[uid] = [ fid ]

    def addBoardToManifest(uid, bid, boardAtts):
        localData.boards[bid] = boardAtts

        uid = str(uid)

        if uid in localData.board_users:
            localData.board_users[uid].append(bid)
        else:
            localData.board_users[uid] = [ bid ]

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
        for key in localData.files:
            localData.files[key].pop('content', None)

        with open('data/files/manifest.json', 'w') as json_file:
            json.dump(localData.files, json_file, indent=4)

        with open('data/files/user_manifest.json', 'w') as json_file:
            json.dump(localData.file_users, json_file, indent=4)

        with open('data/boards/manifest.json', 'w') as json_file:
            json.dump(localData.boards, json_file, indent=4)

        with open('data/boards/user_manifest.json', 'w') as json_file:
            json.dump(localData.board_users, json_file, indent=4)