#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


MAX_RETRY = 5
PDF_PATH = 'mizoram_pdfs'


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


def scrape_mizoram():
    """Scrape Electoral Rolls for Mizoram
       Download and save all PDF files and out the metadata to mizoram.csv with
       the following columns:-

       district, leg_assembly, polling_station_name, file_name
    """

    rows = []
    r = requests.get('http://ceomizoram.nic.in/ElectoralRollPDF.html')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        i = 1
        for dist in soup.select('h4.panel-title'):
            data = {'district': dist.text.strip()}
            for leg in soup.select('ul#myTab{0:d} li'.format(i)):
                data['leg_assembly'] = leg.text.strip()
                _id = leg.find('a')['href'][1:]
                for a in soup.select('div#{0:s} a'.format(_id)):
                    data['polling_station_name'] = a.text.strip()
                    url = 'http://ceomizoram.nic.in/' + a['href']
                    print(url)
                    pdf_fn = url.split('/')[-1]
                    pdf_path = os.path.join(PDF_PATH, pdf_fn)
                    data['file_name'] = pdf_path
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
                    rows.append(data.copy())
                    #break
                #break
            i += 1
            #break

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('mizoram.csv', columns=['district', 'leg_assembly',
                                     'polling_station_name', 'file_name'],
                                     index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_mizoram()
