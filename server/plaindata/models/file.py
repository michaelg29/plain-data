from ..data.local import localData

def upload(atts):
    fid = localData.generateFileId()

    writeFile(f"{fid}.{atts['filetype']}", atts['content'], atts['bytes'])

    atts.pop('content')
    
    localData.addToManifest(atts['user'], fid, atts)

def writeFile(path, content, isBinary = False):
    if isBinary:
        with open("data/files/" + path, mode='wb') as out:
            out.write(content.encode('latin1'))
    else:
       with open("data/files/" + path, 'w') as f:
            f.write(content)