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
        with open(f"data/boards/{atts['id']}.json", 'r') as file:
            board_json = json.load(file)
            file.close()

        with open(f"data/boards/{atts['id']}.json", 'w') as file:
            now = datetime.datetime.now()

            comment_atts = {
                "uid": atts['uid'],
                "name": atts['name'],
                "date": f"{now.month}/{now.day}/{now.year}",
                "content": atts['content']
            }

            board_json['comments'].append(comment_atts)

            json.dump(board_json, file, indent=4)
    except:
        ret['result'] = False
        ret['reasons'].append('input:invalid')