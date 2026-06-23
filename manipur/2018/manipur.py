#!/usr/bin/env python3

from bs4 import BeautifulSoup
from helpers import urlget, getpath, relpath, baseurl, urljoin, urldown, \
	timestamp, TRACK_FILE_TS, append_csv

ENGLISH = 'English'
MANIPURI = 'Manipuri'

MANIPUR_PDF_ENGLISH_DIR = 'manipur_pdfs/english'
MANIPUR_PDF_MANIPURI_DIR = 'manipur_pdfs/manipuri'
MANIPUR_TRACK_DIR = './'

ENGLISH_URL = 'http://www.ceomanipur.nic.in/ElectoralRolls/ElectoralRolls_English.html'
MANIPURI_URL = 'http://www.ceomanipur.nic.in/ElectoralRolls/ElectoralRolls_Manipuri.html'
CSV_HEADER = ('ac_number', 'ac_name', 'poll_station_number', 'poll_station_name', 'language', 'relative_path')
OUTPUT_FILE = getpath(MANIPUR_TRACK_DIR, 'Manipur-%s.csv' % timestamp(TRACK_FILE_TS))


class Manipur:

	def __init__(self):
		self.rolls = [
			{
				'url': ENGLISH_URL,
				'lang': ENGLISH,
				'html': None,
				'data': []
			},
			{
				'url': MANIPURI_URL,
				'lang': MANIPURI,
				'html': None,
				'data': []
			}
		]

	def download(self):
		# Write CSV header
		append_csv(OUTPUT_FILE, CSV_HEADER)

		# Search rolls
		search = {'class': 'styletblfont'}
		for item in self.rolls:
			html = urlget(item['url'])
			assert html
			item['html'] = html
			base = baseurl(item['url'])
			soup = BeautifulSoup(html, 'lxml')
			table = soup.find('table', search)
			links = table.find_all('a')
			rolls = []
			for link in links:
				url = urljoin(base, link.get('href'))
				try:
					num, name = [x.strip() for x in link.text.split('-')]
				except (ValueError, TypeError):
					continue
				else:
					rolls.append(Roll(num, name, url, item['lang']))
			item['data'] = sorted(rolls, key=lambda x: x.key)

		# Run download rolls
		for item in self.rolls:
			for roll in item['data']:
				roll.download()


class Roll:

	def __init__(self, ac_num, ac_name, url, lang):
		self.url = url
		self.key = int(ac_num)
		self.ac_num = ac_num
		self.ac_name = ac_name
		self.lang = lang
		self.html = None
		self.polls = []

	def download(self):
		html = urlget(self.url)

		assert html
		self.html = html
		base = baseurl(self.url)
		soup = BeautifulSoup(html, 'lxml')
		table = soup.find('center')
		td = table.find_all('td')

		assert td
		data = []
		for element in td[1:]:
			a = element.find('a')
			if a:
				data.append((a.text.strip(), urljoin(base, a.get('href'))))
			else:
				data.append(element.text.strip())

		polls = []
		for i in range(0, len(data), 2):
			try:
				num = data[i]
				name, url = data[i+1]
			except (ValueError, IndexError):
				continue
			else:
				name = ' '.join([word.strip() for word in name.split()]).strip()
				polls.append(Poll(num, name, url, self.lang, self.ac_num, self.ac_name))

		self.polls = sorted(polls, key=lambda x: x.key)

		# Download polls
		for poll in self.polls:
			poll.download()


class Poll:

	def __init__(self, station_num, station_name, url, lang, ac_num, ac_name):
		self.url = url
		self.key = int(station_num.split('/')[1].strip(' >'))
		self.ac_num = ac_num
		self.ac_name = ac_name
		self.station_num = station_num
		self.station_name = station_name
		self.lang = lang
		self.file = None
		if lang == ENGLISH:
			self.outdir = getpath(MANIPUR_PDF_ENGLISH_DIR)
		elif lang == MANIPURI:
			self.outdir = getpath(MANIPUR_PDF_MANIPURI_DIR)
		else:
			raise NotImplementedError

	def download(self):
		try:
			self.file = urldown(url=self.url, dest=self.outdir)
		except AssertionError:
			pass

		row = (
			self.ac_num,
			self.ac_name,
			self.station_num,
			self.station_name,
			self.lang,
			relpath(self.file) if self.file is not None else 'Not available / Unable to download'
		)
		append_csv(OUTPUT_FILE, row)


if __name__ == '__main__':
	try:
		site = Manipur()
		site.download()
	except KeyboardInterrupt:
		pass
	finally:
		print('Exit!')
