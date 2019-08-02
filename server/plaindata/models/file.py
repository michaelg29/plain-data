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
		ret['result'] = False
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

def search(atts):
	ret = {
		"result": True,
		"reasons": [],
		"list": []
	}

	for id, file in localData.files.items():
		matches = True

		if 'title' in atts:
			if atts['title'] not in file['title']:
				matches = False
				continue
		if 'author' in atts:
			if atts['author'] != file['author']:
				matches = False
				continue
		if 'filetype' in atts:
			if atts['filetype'] != file['filetype']:
				matches = False
				continue
		if 'category' in atts:
			if atts['category'] != file['category']:
				matches = False
				continue
		if 'tags' in atts:
			tags = atts['tags'].separate('|')
			for tag in tags:
				if tag not in file['tags']:
					matches = False
					continue

		if matches:
			add_item = file
			add_item['id'] = id

			ret['list'].append(add_item)

	return ret

def download(id):
	ret = {
		"result": True,
		"reasons": []
	}

	filetype = localData.files[id]['filetype']
	path = str(id) + '.' + filetype

	try:
		content = readFile(path)

		if not content:
			raise('file:invalid')

		ret['values']['content'] = content

	except:
		ret['result'] = False
		ret['reasons'].append('file:invalid')

	return ret

def readFile(path):
	try:
		with open(f'data/files/{path}', 'rb') as f:
			return f.read().decode('latin1')
	except:
		pass
