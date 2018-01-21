import requests
import os
import sys
import csv
from urllib.parse import urlencode
from tqdm import tqdm

BASE_URL = 'http://ceolakshadweep.gov.in/electoralroll/partsListAjax.html'
PARAMS = {
    'distNo': '1',
    'lacNo': '1',
    'sEcho': '1',
    'iColumns': '3',
    'sColumns': '',
    'iDisplayStart': '0',
    'iDisplayLength': '10',
    'iSortingCols': '1',
    'iSortCol_0': '0',
    'sSortDir_0': 'asc',
    'bSortable_0': 'false',
    'bSortable_1': 'false',
    'bSortable_2': 'false',
    'undefined': 'undefined',
}

FOLDER = 'lakshadweep_pdfs'

def download_file(url, target):
    """Download file from url and save to the target
    """

    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        chunk_size = (64 * 1024)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0)) / chunk_size

        total_size += 1

        with open(target, 'wb') as f:
            for data in tqdm(r.iter_content(chunk_size), total=total_size,
                             unit_scale=chunk_size/1024, unit='KB'):
                f.write(data)
        return True
    else:
        print("ERROR: status_code={0:d}".format(r.status_code))
        return False

def main():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    start_count = 0
    params = PARAMS.copy()
    params['iDisplayStart'] = start_count
    params['iDisplayLength'] = 1000

    url = '?'.join((BASE_URL, urlencode(params)))

    r = requests.get(url)

    if r.status_code != 200:
        print('Website returned {}'.format(r.status_code))
        return

    j = r.json()

    f = open('lakshadweep.csv', 'w')

    csv_writer = csv.writer(f)
    csv_writer.writerow(('booth_no', 'polling_station_name', 'file_name'))

    for i, d in enumerate(j['aaData']):
        no, name, url = d

        print('{}/{}\r'.format(i, j['iTotalRecords']), end='')
        sys.stdout.flush()

        pdf_url = url.split('=\'')[-1].split('\'>')[0]
        file_name = pdf_url.split('/')[-1]

        path = '{}/{}'.format(FOLDER, file_name)

        download_file(pdf_url, path)

        csv_writer.writerow((no, name, file_name))
        
if __name__ == '__main__':
    main()
