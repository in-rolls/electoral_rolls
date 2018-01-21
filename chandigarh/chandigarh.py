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
PDF_PATH = 'chandigarh_pdfs'


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


def extract_url(soup, no):
    no = int(no) - 1
    a = soup.select('a#ContentPlaceHolder1_grdPollingStation_hlnkBoothNo_{0:d}'.format(no))[0]
    return 'http://ceochandigarh.nic.in/webpages/' + a['href']


def download_url(url):
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


def scrape_charadigarh():
    """Scrape Electoral Rolls for Chanadigarh
       Download and save all PDF files and out the metadata to chandigarh.csv
       with the following columns:-

       booth_no, forms_received, location, area_covered, booth_level_officer,
       pdf_file_name
    """

    rows = []
    # Please make sure phantomjs executable available in PATH setting.
    driver = webdriver.PhantomJS()
    driver.get("http://ceochandigarh.nic.in/webpages/Polling2.aspx")
    element = driver.find_element_by_xpath("//a[@id='ContentPlaceHolder1_lnkCompletelist']")
    element.click()
    html = driver.page_source
    driver.quit()
    
    dfs = pd.read_html(html,
                      attrs={'id': 'ContentPlaceHolder1_grdPollingStation'},
                      header=0)
    df = dfs[0]
    df.columns = ['booth_no', 'forms_received', 'location', 'area_covered',
                  'booth_level_officer']

    soup = BeautifulSoup(html, 'html.parser')
    df['url'] = df.booth_no.apply(lambda c: extract_url(soup, c))
    df['pdf_file_name'] = df.url.apply(lambda c: download_url(c))

    print("Writing the metadata to CSV file...")
    df.to_csv('chandigarh.csv',
              columns=['booth_no', 'forms_received', 'location',
                       'area_covered', 'booth_level_officer',
                       'pdf_file_name'], index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_charadigarh()
