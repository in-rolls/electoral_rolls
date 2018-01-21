#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from selenium import webdriver


MAX_RETRY = 5
PDF_PATH = 'kerala_{0:s}'


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


def scrape_kerala_archives():
    """Scrape Electoral Rolls for Kerala Archives
       Download and save all PDF files and out the metadata to kerala_20xx.csv with
       the following columns:-

       year, leg_assembly, booth_no, file_name
    """

    # Please make sure phantomjs executable available by setting PATH.
    driver = webdriver.PhantomJS()
    driver.get("http://www.ceo.kerala.gov.in/erollArchives.html")
    yi = 0
    while True:
        el_year = driver.find_element_by_xpath("//select[@name='rollYear']")
        opts_year = el_year.find_elements_by_tag_name("option")
        if yi == len(opts_year):
            break
        rows = []
        opt = opts_year[yi]
        yi += 1
        year = opt.get_attribute("value")
        if year != '':
            opt.click()
            n = 0
            while True:
                el_lacno = driver.find_element_by_xpath("//select[@name='lacNo']")
                opts_lacno = el_lacno.find_elements_by_tag_name("option")
                if n == len(opts_lacno):
                    break
                opt_lacno = opts_lacno[n]
                n += 1
                lacno = opt_lacno.get_attribute("value")
                lacno_txt = opt_lacno.text
                if  lacno != '':
                    opt_lacno.click()
                    print(year, lacno, lacno_txt)
                    xpath = "//input[@id='listCmd']"
                    el_btn = driver.find_element_by_xpath(xpath)
                    el_btn.click()
                    xpath = "//span[@class='site-links']/a"
                    links = driver.find_elements_by_xpath(xpath)
                    for a in links[3:]:
                        url = a.get_attribute('href')
                        txt = a.text
                        pdf_fn = '{0:s}_{1:03d}_{2:03d}.pdf'.format(year, int(lacno), int(txt))
                        pdf_dir = PDF_PATH.format(year)
                        if not os.path.exists(pdf_dir):
                            os.makedirs(pdf_dir)
                        pdf_path = os.path.join(pdf_dir, pdf_fn)
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
                        rows.append({'year': year,
                                     'leg_assembly': lacno_txt,
                                     'booth_no': txt,
                                     'file_name': pdf_path})
                        #break
                    #break
            df = pd.DataFrame(rows)
            print("Writing the metadata to CSV file...")
            df.to_csv('kerala_{0:s}.csv'.format(year),
                      columns=['year', 'leg_assembly', 'booth_no',
                               'file_name'], index=False, encoding='utf-8')
            #break
    driver.quit()
    print("Done!")


if __name__ == "__main__":
    scrape_kerala_archives()
