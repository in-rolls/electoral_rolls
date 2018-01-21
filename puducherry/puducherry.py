import requests
from pyquery import PyQuery
import os
import csv
import sys

# URL = 'https://ceopuducherry.py.gov.in/rolls/rolls.html'
FOLDER = 'puducherry_pdfs'

SITE_URL = 'https://ceopuducherry.py.gov.in/rolls/ac{}.htm'
PDF_URL_BASE = 'https://ceopuducherry.py.gov.in/{}'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36',
}

TIMEOUT = 10

def request(method, url, **kwargs):
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    if 'headers' not in kwargs:
        kwargs['headers'] = HEADERS

    while True:
        try:
            return getattr(requests, method)(url, **kwargs)
        except (
                requests.exceptions.SSLError,
                requests.exceptions.RequestException
            ) as e:
            sleep(TIMEOUT)


def post(url, **kwargs):
    return request('post', url, **kwargs)

def get(url, **kwargs):
    return request('get', url, **kwargs)

def download_file(url, path):
    JOURNAL_FILE = '{}.jor'.format(path)

    if os.path.exists(path) and not os.path.exists(JOURNAL_FILE):
        return

    jf = open(JOURNAL_FILE, 'w')
    jf.close()

    try:
        f = open(path, 'wb')
        r = get(url, stream=True, timeout=TIMEOUT, headers=HEADERS)

        for block in r.iter_content(1024):
            f.write(block)

        os.remove(JOURNAL_FILE)
    except (
            requests.exceptions.SSLError,
            requests.exceptions.RequestException
        ) as e:
        sleep(TIMEOUT)
    finally:
        f.close()

def parse_page(url):
    r = get(url, timeout=10, headers=HEADERS)

    r.raise_for_status()

    pyq = PyQuery(r.text)

    constituency = pyq('h3')[1].text_content().strip().split(' ')[1]

    for child in pyq('table')[0].findall('tr')[1].getchildren():
        td_list = child.find('tr').findall('td')
        # print(i, td.text_content())

        part_no = td_list[0].text_content().strip()
        polling_station = td_list[1]

        polling_station_name = polling_station.text_content().strip().replace('View Voters List in : TAMIL / ENGLISH', '')

        tamil_pdf, en_pdf = polling_station.findall('a')


        en_pdf_url, tamil_pdf_url = en_pdf.get('href'), tamil_pdf.get('href')

        en_pdf_full_url = PDF_URL_BASE.format(en_pdf_url.replace('../', ''))
        tamil_pdf_full_url = PDF_URL_BASE.format(tamil_pdf_url.replace('../', ''))

        en_file_name = '{}_{}.pdf'.format(
            'eng',
            part_no.replace('/', '_').strip()
        )

        tamil_file_name = '{}_{}.pdf'.format(
            'tam',
            part_no.replace('/', '_').strip()
        )

        area = td_list[2].text_content().strip()

        yield {
            'en_pdf_full_url': en_pdf_full_url,
            'tamil_pdf_full_url': tamil_pdf_full_url,
            'part_no': part_no,
            'en_file_name': en_file_name,
            'tamil_file_name': tamil_file_name,
            'area_covered': area,
            'constituency': constituency,
            'polling_station_name': polling_station_name
        }

def main():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    f = open('puducherry.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(f)

    csv_writer.writerow((
        'constituency_name',
        'part_no',
        'poll_station_name',
        'area_covered',
        'file_name_en',
        'file_name_ta'
        )
    )

    for x in range(1, 31):
        url = SITE_URL.format(x)
        page_data_list = parse_page(url)

        for i, page_data in enumerate(page_data_list):
            print('{}/{}/{}\r'.format(x, i, 30), end='')
            sys.stdout.flush()

            en_file_name = page_data['en_file_name']
            ta_file_name = page_data['tamil_file_name']

            download_file(page_data['en_pdf_full_url'], '{}/{}'.format(FOLDER, en_file_name))
            download_file(page_data['tamil_pdf_full_url'], '{}/{}'.format(FOLDER, ta_file_name))

            csv_writer.writerow((
                page_data['constituency'],
                page_data['part_no'],
                page_data['polling_station_name'],
                page_data['area_covered'],
                en_file_name,
                ta_file_name
            ))




if __name__ == '__main__':
    main()
