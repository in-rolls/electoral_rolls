#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
import lxml.html


MAX_RETRY = 5
PDF_PATH = 'daman_{:d}'

links = {2015: 'http://ceodaman.nic.in/Final%20%20PHOTO%20ELECTORAL%20ROLL-%202015/polling_station_wise_roll_in_eng.htm',
         2016: 'http://ceodaman.nic.in/Final-Photo-Electoral-Roll-2016/polling_station_wise_roll_in_eng.htm'}


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


def scrape_daman_archives():
    """Scrape Electoral Rolls for Daman Archives
       Download and save all PDF files and out the metadata to daman_201x.csv with
       the following columns:-

       year, language, poll_station_no, file_name
    """

    for y in sorted(links):
        path = PDF_PATH.format(y)
        if not os.path.exists(path):
            os.makedirs(path)
        url = links[y]
        doc = lxml.html.parse(url)
        stations = doc.xpath('//option/text()')
        base_url = '/'.join(url.split('/')[:-1])
        rows = []
        for lang in ['English', 'Gujarati']:
            for no in stations:
                url = (base_url +
                       '/pdf/{lang:s}/A0010{no:03d}.PDF').format(lang=lang,
                                                                  no=int(no))
                print(url)
                pdf_fn = '{lang:s}_{no:03d}.pdf'.format(
                    lang=lang[:3].lower(), no=int(no))
                pdf_path = os.path.join(PDF_PATH.format(y), pdf_fn)
                if not os.path.exists(pdf_path):
                    retry = 0
                    while retry < MAX_RETRY:
                        try:
                            if not download_file(url, pdf_path):
                                print("FAIL: [{0:s}]({1:s})".format(pdf_path,
                                                                    url))
                            break
                        except Exception as e:
                            print("WARN: {0!s}".format(e))
                            print("Retry again in 5s...")
                            retry += 1
                            time.sleep(5)
                rows.append({'year': y,
                             'language': lang,
                             'poll_station_no': no,
                             'file_name': pdf_path})
                #break
            #break

        df = pd.DataFrame(rows)
        print("Writing the metadata to CSV file...")
        df.to_csv('daman_{:d}.csv'.format(y),
                  columns=['year', 'language', 'poll_station_no',
                           'file_name'],
                  index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    scrape_daman_archives()
