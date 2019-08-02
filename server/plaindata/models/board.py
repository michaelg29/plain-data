from ..data.local import localData
from .file import writeFile

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
            "comments": []
        }

        json_content = json.dumps(output)

        with open(f'data/boards/{id}.json', 'w') as out_file:
            out_file.write(json_content)

        localData.addBoardToManifest(output['user'], id)

        ret['id'] = id
    except:
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

        now = datetime.datetime.now()

        comment_atts = {
            "uid": atts['uid'],
            "name": atts['name'],
            "date": f"{now.month}/{now.day}/{now.year}",
            "content": atts['content']
        }

        localData.boards[id]['comments'].append(comment_atts)
    except:
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
    ret = {
        "result": True,
        "reasons": []
    }

    if id in localData.boards:
        ret['values'] = localData.boards['id']
    else:
        ret['result'] = False
        ret['reasons'].append('id:invalid')

    return ret