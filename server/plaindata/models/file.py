from ..data.local import localData

import json

def upload(atts):
	ret = {
		"result": True,
		"reasons": []
	}

	try:
		fid = localData.generateFileId()

		writeFile(f"{fid}.{atts['filetype']}", atts['content'], atts['bytes'])

		atts.pop('content')
		
		localData.addFileToManifest(atts['user'], fid, atts)
	except:
		ret['reasons'].append('file:invalid')

	return ret

def writeFile(path, content, isBinary = False):
	content = content['data']
	content = ''.join([chr(int(val)) for val in content])

	if isBinary:
		with open("data/files/" + path, mode='wb') as out:
			out.write(content.encode('latin1'))
	else:
		with open("data/files/" + path, 'w') as f:
			f.write(content)