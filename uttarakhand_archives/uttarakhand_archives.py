#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


MAX_RETRY = 5
PDF_PATH = 'uttarakhand_{:d}'

links = {2007: 'http://election.uk.gov.in/pdf_roll/01012007/Uttranchal_pdf_page.htm',
         2008: 'http://election.uk.gov.in/pdf_roll/01012008/Uttranchal_pdf_page.htm',
         2009: 'http://election.uk.gov.in/pdf_roll/24042009/Uttranchal_pdf_page.htm',
         2010: 'http://election.uk.gov.in/pdf_roll/01012010_N/Uttranchal_pdf_page.htm',
         2011: 'http://ceo.uk.gov.in/pages/view/27/34-a.c.-segment-wise-final-electoral-roll..as-on-01-01-2011..(new)-',
         2012: 'http://election.uk.gov.in/pdf_roll/02012012/Uttranchal_pdf_page.htm',
         2013: 'http://election.uk.gov.in/pdf_roll/01012013S/Uttranchal_pdf_page.htm',
         2014: 'http://election.uk.gov.in/pdf_roll/30042014/Uttranchal_pdf_page.htm',
         2015: 'http://election.uk.gov.in/pdf_roll/01012015F/Uttranchal_pdf_page.htm',
         2016: 'http://election.uk.gov.in/pdf_roll/01102016S/Uttranchal_pdf_page.htm'}


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


def download_pdf(href, base, year):
    url = base + href
    print(url)
    pdf_fn = url.split('/')[-1]
    pdf_path = os.path.join(PDF_PATH.format(year), pdf_fn)
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


def scrape_uttarakhand_archives():
    """Scrape Electoral Rolls for Uttarakhand Archives
       Download and save all PDF files and out the metadata to uttarakhand_20xx.csv with
       the following columns:-

       year, ac_no, ac_name, filename
    """

    
    for y in sorted(links):
        path = PDF_PATH.format(y)
        if not os.path.exists(path):
            os.makedirs(path)
        rows = []
        url = links[y]
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table_rows = soup.select('table#AutoNumber2 table tr')[1:]
            if len(table_rows) == 0:
                table_rows = soup.select('table.dataTable tr')[1:]
            for tr in table_rows:
                tds = tr.select('td')
                href = tds[1].find('a')['href']
                if href.startswith('http://'):
                    base = ''
                elif href.startswith('/'):
                    base = '/'.join(url.split('/')[:3])
                else:
                    base = '/'.join(url.split('/')[:-1]) + '/'
                fn = download_pdf(href, base, y)
                rows.append({'year': y,
                             'ac_no': tds[0].text,
                             'ac_name': tds[1].text,
                             'file_name': fn})
                href = tds[3].find('a')['href']
                fn = download_pdf(href, base, y)
                rows.append({'year': y,
                             'ac_no': tds[2].text,
                             'ac_name': tds[3].text,
                             'file_name': fn})
                #break
        df = pd.DataFrame(rows)
        print("Writing the metadata to CSV file...")
        df.to_csv('uttarakhand_{:d}.csv'.format(y), columns=['year', 'ac_no', 'ac_name', 'file_name'],
                index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    scrape_uttarakhand_archives()
