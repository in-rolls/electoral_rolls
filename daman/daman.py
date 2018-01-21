#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm


MAX_RETRY = 5
PDF_PATH = 'daman_pdfs'


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


def scrape_daman():
    """Scrape Electoral Rolls for Daman
       Download and save all PDF files and out the metadata to daman.csv with
       the following columns:-

       language, poll_station_no, file_name
    """

    rows = []
    for lang in ['English', 'Gujarati']:
        for no in range(1, 140):
            url = 'http://ceodaman.nic.in/Final-Photo-Electoral-Roll-2017' \
                  '/pdf/{lang:s}/A00100{no:02d}.PDF'.format(lang=lang, no=no)
            print(url)
            pdf_fn = '{lang:s}_{no:03d}.pdf'.format(
                lang=lang[:3].lower(), no=no)
            pdf_path = os.path.join(PDF_PATH, pdf_fn)
            if not os.path.exists(pdf_path):
                retry = 0
                while retry < MAX_RETRY:
                    try:
                        download_file(url, pdf_path)
                        break
                    except Exception as e:
                        print("WARN: {0!s}".format(e))
                        print("Retry again in 5s...")
                        retry += 1
                        time.sleep(5)
            rows.append({'language': lang,
                         'poll_station_no': no,
                         'file_name': pdf_path})
            #break
        #break

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('daman.csv', columns=['language', 'poll_station_no',
                                    'file_name'], index=False,
                                    encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_daman()
