"""
	file model class
"""

from ..data.local import localData

import json

"""
	uploads file from client to server
"""
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

"""
	writes file to hard drive
"""
def writeFile(path, content, isBinary = False):
	content = content['data']
	content = ''.join([chr(int(val)) for val in content])

	if isBinary:
		with open("data/files/" + path, mode='wb') as out:
			out.write(content.encode('latin1'))
	else:
		with open("data/files/" + path, 'w') as f:
			f.write(content)

"""
	returns file search results for parameters
"""
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
				continue
		if 'author' in atts:
			if atts['author'] != file['author']:
				continue
		if 'filetype' in atts:
			if atts['filetype'] != file['filetype']:
				continue
		if 'category' in atts:
			if atts['category'] != file['category']:
				continue
		if 'tags' in atts:
			tags = atts['tags'].split(',')
			for tag in tags:
				if tag not in file['tags']:
					matches = False
					continue

		if matches:
			add_item = file
			add_item['id'] = id

			ret['list'].append(add_item)

	return ret

"""
	downloads file from server to client with specified id
"""
def download(id):
	ret = {
		"result": True,
		"reasons": [],
		"values": {}
	}

	id = str(id)

	localData.files[id].pop('content', None)

	ret['values'] = localData.files[id]
	ret['values']['filepath'] = localData.files[id]['filename'] + '.' + localData.files[id]['filetype']
	filetype = localData.files[id]['filetype']
	path = id + '.' + filetype

	try:
		content = readFile(path)

		if not content:
			raise('file:invalid')

		ret['values']['content'] = content

	except:
		ret['result'] = False
		ret['reasons'].append('file:invalid')

	return ret

"""
	read file from hard drive
"""
def readFile(path):
	content = ""
	ret = []

	try:
		with open(f'data/files/{path}', 'rb') as f:
			content = f.read().decode('latin1')
	except:
		pass

	for c in content:
		ret.append(ord(c))

	return ret
