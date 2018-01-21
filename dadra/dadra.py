#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from selenium import webdriver


MAX_RETRY = 5
PDF_PATH = 'dadra_pdfs'


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


def scrape_dadra():
    """Scrape Electoral Rolls for Dadra
       Download and save all PDF files and out the metadata to dadra.csv with
       the following columns:-

       language, main_or_supplementary, part_no, file_name
    """

    rows = []
    # Please make sure phantomjs executable available in PATH setting.
    driver = webdriver.PhantomJS()
    driver.get("http://ceodnh.nic.in/Electoral2017.aspx")
    langs = {'guj': 'RadioButton1',
             'eng': 'RadioButton2'}
    for l in langs:
        data = {'language': l}
        xpath = "//input[@id='ctl00_ContentPlaceHolder1_{0:s}']".format(langs[l])
        driver.find_element_by_xpath(xpath).click()
        # Main/Suplementary - ctl00_ContentPlaceHolder1_DropDownList1
        # 1 - 266 - ctl00_ContentPlaceHolder1_DropDownList2
        for t in ['Main', 'Suplementary']:
            if t == 'Main':
                m_s = 'main'
            else:
                m_s = 'supp'
            data['main_or_supplementary'] = m_s
            xpath = "//select[@id='ctl00_ContentPlaceHolder1_DropDownList1']" \
                    "/option[text()='{0:s}']".format(t)
            driver.find_element_by_xpath(xpath).click()
            for no in range(1, 267):
                data['part_no'] = no
                xpath = "//select[@id='ctl00_ContentPlaceHolder1_DropDownList2']" \
                        "/option[text()='{0:d}']".format(no)
                driver.find_element_by_xpath(xpath).click()
                xpath = "//input[@id='ctl00_ContentPlaceHolder1_btn_GetDetail']"
                el_btn = driver.find_element_by_xpath(xpath)
                el_btn.click()
                iframe = driver.find_element_by_xpath("//iframe")
                url = iframe.get_attribute('src')
                print(url)
                pdf_fn = '{0:s}_{1:s}_{2:03d}.pdf'.format(
                    l, m_s, no)
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
        #break
    driver.quit()

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('dadra.csv', columns=['language', 'main_or_supplementary',
                                    'part_no', 'file_name'], index=False,
                                    encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_dadra()
