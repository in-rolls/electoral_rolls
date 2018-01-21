#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


MAX_RETRY = 5
PDF_PATH = 'uttarakhand_pdfs'


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


def download_pdf(href):
    url = 'http://election.uk.gov.in/pdf_roll/10102017F/' + href
    print(url)
    pdf_fn = url.split('/')[-1]
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
    return pdf_path


def scrape_uttarakhand():
    """Scrape Electoral Rolls for Uttarakhand
       Download and save all PDF files and out the metadata to uttarakhand.csv with
       the following columns:-

       ac_no, ac_name, filename
    """

    rows = []
    r = requests.get('http://election.uk.gov.in/pdf_roll/10102017F/Uttranchal_pdf_page.htm')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for tr in soup.select('table#AutoNumber2 table tr')[1:]:
            tds = tr.select('td')
            href = tds[1].find('a')['href']
            fn = download_pdf(href)
            rows.append({'ac_no': tds[0].text,
                         'ac_name': tds[1].text,
                         'file_name': fn})
            href = tds[3].find('a')['href']
            fn = download_pdf(href)
            rows.append({'ac_no': tds[2].text,
                         'ac_name': tds[3].text,
                         'file_name': fn})
            #break
    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('uttarakhand.csv', columns=['ac_no', 'ac_name', 'file_name'],
              index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_uttarakhand()
