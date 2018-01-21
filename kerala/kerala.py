#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver


MAX_RETRY = 5
PDF_PATH = 'kerala_pdfs'


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


def query_kerala_table(distno_val, lacno_val, data):
    """Query data table by distno and lacno
    """

    rows = []

    distno_txt = data['district']
    lacno_txt = data['leg_assembly']

    # Looking the total records by getting just one row
    params = {'distNo': distno_val,
              'lacNo': lacno_val,
              'iDisplayLength': 1}
    r = requests.get('http://www.ceo.kerala.gov.in/electoralroll/partsListAjax.html?sEcho=1&iColumns=3&sColumns=&iDisplayStart=0&iSortingCols=1&iSortCol_0=0&sSortDir_0=asc&bSortable_0=false&bSortable_1=false&bSortable_2=false&undefined=undefined', params=params)
    if r.status_code == 200:
        total = r.json()['iTotalDisplayRecords']
        print("Scraping {0:s}, {1:s} (Total {2:d})".format(distno_txt,
                                                           lacno_txt, total))
        # Query all records at one time
        params = {'distNo': distno_val,
                  'lacNo': lacno_val,
                  'iDisplayLength': total}
        r = requests.get('http://www.ceo.kerala.gov.in/electoralroll/partsListAjax.html?sEcho=1&iColumns=3&sColumns=&iDisplayStart=0&iSortingCols=1&iSortCol_0=0&sSortDir_0=asc&bSortable_0=false&bSortable_1=false&bSortable_2=false&undefined=undefined', params=params)
        if r.status_code == 200:
            js = r.json()
            for d in js['aaData']:
                booth_no = d[0]
                data['booth_no'] = booth_no
                polling_station_name = d[1]
                data['polling_station_name'] = polling_station_name
                soup = BeautifulSoup(d[2], 'html.parser')
                for a in soup.find_all('a'):
                    lang = a.text.lower()
                    url = a['href']
                    print(url)
                    pdf_fn = '{0:s}_{1:02d}_{2:03d}_{3:03d}.pdf'.format(
                        lang, int(distno_val), int(lacno_val), int(booth_no))
                    pdf_path = os.path.join(PDF_PATH, pdf_fn)
                    data['{0:s}_file_name'.format(lang)] = pdf_path
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
    return rows


def scrape_kerala():
    """Scrape Electoral Rolls for Kerala
       Download and save all PDF files and out the metadata to kerala.csv with
       the following columns:-

       district, leg_assembly, booth_no, polling_station_name, mal_file_name,
       eng_file_name
    """

    rows = []
    # Please make sure phantomjs executable available in PATH setting.
    driver = webdriver.PhantomJS()
    driver.get("http://www.ceo.kerala.gov.in/electoralrolls.html")
    el_distno = driver.find_element_by_xpath("//select[@name='distNo']")
    distno_options = el_distno.find_elements_by_tag_name("option")
    for distno_opt in distno_options:
        distno_val = distno_opt.get_attribute("value")
        distno_txt = distno_opt.text
        if distno_val != '':
            distno_opt.click()
            data = {'district': distno_txt}
            el_lacno = driver.find_element_by_xpath("//select[@name='lacNo']")
            lacno_options = el_lacno.find_elements_by_tag_name("option")
            for lacno_opt in lacno_options:
                lacno_val = lacno_opt.get_attribute("value")
                lacno_txt = lacno_opt.text
                if lacno_val != '':
                    data['leg_assembly'] = lacno_txt
                    new_rows = query_kerala_table(distno_val, lacno_val, data)
                    rows.extend(new_rows)
                    #break
            #break
    driver.quit()

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('kerala.csv', columns=['district', 'leg_assembly', 'booth_no',
                                     'polling_station_name', 'eng_file_name',
                                     'mal_file_name'], index=False,
                                     encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_kerala()
