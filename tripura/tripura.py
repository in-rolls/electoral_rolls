#!/usr/bin/env python3

from helpers import urlget, urldown, urljoin, getpath, relpath, \
	timestamp, TRACK_FILE_TS, append_csv

TRIPURA_PDF_DIR = 'tripura_pdfs'
TRIPURA_TRACK_DIR = './'

WEST_JS_URL = 'http://ceotripura.nic.in/PSCDROM/Draft_2018/PC01/html/js/list.js'
WEST_BASE_URL = 'http://ceotripura.nic.in/PSCDROM/Draft_2018/PC01/'
EAST_JS_URL = 'http://ceotripura.nic.in/PSCDROM/Draft_2018/PC02/html/js/list.js'
EAST_BASE_URL = 'http://ceotripura.nic.in/PSCDROM/Draft_2018/PC02/'
CSV_HEADER = ('district_name', 'ac_number', 'ac_name', 'poll_station_number', 'filename')
OUTPUT_FILE = getpath(TRIPURA_TRACK_DIR, 'Tripura-%s.csv' % timestamp(TRACK_FILE_TS))

class Tripura:

	def __init__(self):
		self.districts = [
			District(js_url=WEST_JS_URL, base_url=WEST_BASE_URL),
			District(js_url=EAST_JS_URL, base_url=EAST_BASE_URL)
		]

	def download(self):
		# Write CSV header
		append_csv(OUTPUT_FILE, CSV_HEADER)
		# Run download
		for district in self.districts:
			district.download()


class District:

	def __init__(self, js_url, base_url):
		self.js_url = js_url
		self.base_url = base_url
		self.js_content = None
		self.pcno = None
		self.name = None
		self.rolls = []

	def parse_js(self):
		assert self.js_content is not None
		left = []
		right = []
		getpair = lambda x: x.split('=')[1].strip(' \';').split(maxsplit=1)
		getnum = lambda x: x.split('=')[1].strip(' \';')
		for line in self.js_content.split('\r\n'):
			line = line.strip()
			if line.startswith('PC='):
				num, name = getpair(line)
				self.pcno = 'pc%02d' % int(num)
				self.name = name.strip()
			elif line.startswith('ac['):
				num, name = getpair(line)
				left.append((int(num), name.strip()))
			elif line.startswith('maxPart['):
				num = getnum(line)
				right.append(int(num))
		return zip(left, right)

	def get_pdf_url(self, ac_num, poll_num):
		path = '{pcno}/a{acno}/ac{acno}{part}.pdf'.format(
			pcno=self.pcno,
			acno='%03d' % ac_num,
			part='%04d' % poll_num
		)
		return urljoin(self.base_url, path)

	def download(self):
		try:
			js = urlget(self.js_url)
		except AssertionError:
			return

		self.js_content = js
		parsed = self.parse_js()

		for item in parsed:
			ac, polls = item
			ac_num, ac_name = ac
			for i in range(polls):
				poll_num = i + 1
				url = self.get_pdf_url(ac_num, poll_num)
				try:
					file = urldown(url=url, dest=getpath(TRIPURA_PDF_DIR))
				except AssertionError:
					file = None
				row = (
					self.name,
					str(ac_num),
					ac_name,
					str(poll_num),
					relpath(file) if file is not None else 'Not available / Unable to download'
				)
				self.rolls.append(row)
				append_csv(OUTPUT_FILE, row)


if __name__ == '__main__':
	try:
		site = Tripura()
		site.download()
	except KeyboardInterrupt:
		pass
	finally:
		print('Exit!')
