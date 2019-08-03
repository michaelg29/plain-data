from ..data.local import localData
from .file import writeFile
from plaindata.utils import getDate

import json
import datetime

def createBoard(atts):
    ret = {
        "result": True,
        "reasons": []
    }

    try:
        id = localData.generateBoardId()

        output = {
            "user": atts['user'],
            "title": atts['title'],
            "creator": atts['creator'],
            "category": atts['category'],
            "tags": atts['tags'],
            "content": atts['content'],
            "date": getDate(),
            "comments": []
        }

        localData.addBoardToManifest(output['user'], str(id), output)

        ret['id'] = id
    except:
        import traceback, sys
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        ret['result'] = False
        ret['reasons'].append('input:invalid')

    return ret

def comment(atts):
    ret = {
        "result": True,
        "reasons": []
    }

    try:
        id = str(atts['id'])
        ret['id'] = id

        comment_atts = {
            "uid": atts['uid'],
            "name": atts['name'],
            "date": getDate(),
            "subject": atts['subject'],
            "content": atts['content']
        }

        localData.boards[id]['comments'].append(comment_atts)
    except:
        import traceback, sys
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        ret['result'] = False
        ret['reasons'].append('input:invalid')

    return ret

def boardSearch(atts):
    ret = {
        "result": True,
        "reasons": [],
        "list": []
    }

    for id, board in localData.boards.items():
        matches = True

        if 'title' in atts:
            if atts['title'] not in board['title']:
                continue
        if 'creator' in atts:
            if atts['creator'] != board['creator']:
                continue
        if 'category' in atts:
            if atts['category'] != board['category']:
                continue
        if 'tags' in atts:
            tags = atts['tags'].separate(',')
            for tag in tags:
                if tag not in board['tags']:
                    matches = False
                    continue

        if matches:
            add_item = board
            add_item['id'] = id

            ret['list'].append(add_item)

    return ret

def retrieve(id):
    id = str(id)

    ret = {
        "result": True,
        "reasons": [],
        "id": id
    }

    if id in localData.boards:
        ret['values'] = localData.boards[id]
        ret['values']['id'] = id
    else:
        ret['result'] = False
        ret['reasons'].append('id:invalid')

    return ret