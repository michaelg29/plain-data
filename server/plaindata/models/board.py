from ..data.local import localData
from .file import writeFile

import json

def create(atts):
    ret = {
        "result": True,
        "reasons": []
    }

    try:
        id = localData.generateBoardId()

        output = {
            "user": atts['user'],
            "name": atts['name'],
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
    except:
        ret['result'] = False
        ret['reasons'].append('input:invalid')

    return ret