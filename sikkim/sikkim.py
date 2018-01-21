#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
import lxml.html
from collections import defaultdict
from pprint import pprint


MAX_RETRY = 5
PDF_PATH = 'sikkim_pdfs'


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


def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict(table):
    result = defaultdict(lambda : defaultdict())
    for row_i, row in enumerate(table.xpath('./tr')):
        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text_content()
            urls = col.xpath('.//a')
            href = None
            if len(urls):
                href = urls[0].get('href')
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
                result[i][j + 1] = href
    return result


def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


def scrape_sikkim():
    """Scrape Electoral Rolls for Sikkim
       Download and save all PDF files and out the metadata to sikkim.csv with
       the following columns:-

       ac_number, ac_name, part_number, polling_station_name, file_name
    """

    rows = []
    base_url = "http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/"
    url = base_url + "Polling%20Station%20wise%20final%20Electoral%20Roll%20published%20on%2010th%20January%202018.html"
    
    doc = lxml.html.parse(url)
    for table_el in doc.xpath('//table'):
        table = table_to_list(table_el)
        break

    for r in table[3:]:
        if r[5] is None:
            break
        ac = r[0].strip().split(' ')
        ac_no = ac[0]
        ac_name = ' '.join(ac[1:])
        part_no = r[2].strip()
        station_name = ' '.join(r[4].strip().replace('\r\n', ' ').split())
        url = base_url + r[5].strip()
        pdf_fn = '{ac_no:s}_{no:03d}.pdf'.format(ac_no=ac_no, no=int(part_no))
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
        rows.append({'ac_number': ac_no,
                     'ac_name': ac_name,
                     'part_number': part_no,
                     'station_name': station_name,
                     'file_name': pdf_path})
        #break

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('sikkim.csv', columns=['ac_number', 'ac_name', 'part_number',
                                     'station_name', 'file_name'],
                                     index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_sikkim()
