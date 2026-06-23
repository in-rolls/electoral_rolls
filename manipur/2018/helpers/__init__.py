import re, os, csv, requests, time
from urllib.parse import urlparse, urljoin

__all__ = [
	'APP_PATH',
	'urlget',
	'getpath',
	'urldown',
	'relpath',
	'write_csv',
	'urljoin',
	'urlparse',
	'baseurl',
	'isfile',
	'timestamp',
	'TRACK_FILE_TS',
	'append_csv'
]

APP_PATH = os.path.dirname(os.path.dirname(__file__))
TRACK_FILE_TS = '%Y%m%d-%H%M%S'


def getpath(path, *subpath):
	if os.path.isabs(path):
		return os.path.join(path, *subpath)
	return os.path.join(APP_PATH, path, *subpath)


def relpath(path):
	path = getpath(path)
	assert APP_PATH in path
	return path[len(APP_PATH)+1:]


def urlget(url, return_json=False):
	resp = requests.get(url)
	assert resp.status_code == requests.codes.OK
	return resp.json() if return_json else resp.text


def urldown(url, dest):
	path = getpath(dest)
	assert os.path.isdir(path)
	file = os.path.join(path, os.path.basename(url))
	if isfile(file):
		print('File existed: %s' % file)
		return file
	print('Downloading %s...' % url)
	resp = requests.get(url)
	assert resp.status_code == requests.codes.OK
	with open(file, 'wb') as f:
		f.write(resp.content)
	return file


def write_csv(filepath, rows, header=None, start=0, encoding=None, delimiter=',', quote='"'):
	with open(filepath, 'w', newline='', encoding=encoding) as file:
		writer = csv.writer(file, delimiter=delimiter, quotechar=quote)
		# Write empty rows
		if start > 0:
			for i in range(start):
				writer.writerow([])
		# Write header
		if header:
			writer.writerow(header)
		# Writer rows
		writer.writerows(rows)


def append_csv(filepath, row, encoding=None, delimiter=',', quote='"'):
	with open(filepath, 'a', newline='', encoding=encoding) as file:
		writer = csv.writer(file, delimiter=delimiter, quotechar=quote)
		writer.writerow(row)


def baseurl(url):
	assert re.match(r'^https?://[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_.]+/.*', url)
	return os.path.dirname(url) + '/'


def isfile(path):
	return os.path.isfile(path)


def timestamp(fmt=None):
	return time.strftime(fmt) if fmt else time.time()
