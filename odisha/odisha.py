#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from selenium import webdriver

# FIXME: Explicit delay 
DELAY = 3
MAX_RETRY = 5
PDF_PATH = 'odisha_pdfs'


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


def download_pdf(url, type_, dist_no, ac_no, part_no):
    pdf_fn = '{0:s}_{1:02d}_{2:03d}_{3:03d}.pdf'.format(type_, int(dist_no),
                                                        int(ac_no),
                                                        int(part_no))
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


def scrape_odisha():
    """Scrape Electoral Rolls for Odisha
       Download and save all PDF files and out the metadata to odisha.csv with
       the following columns:-

       district_number, district_name, ac_name, ac_number, part_name,
       part_number, type_of_roll (service voter or eroll), filename
    """

    rows = []
    saved_di = 1
    saved_ai = 1
    saved_pi = 1
    driver = None

    while True:
        try:
            # Please make sure phantomjs executable available in the PATH.
            driver = webdriver.PhantomJS()
            driver.get("http://election.ori.nic.in/odishaceo/ViewEroll.aspx")

            di = saved_di
            while True:
                dist_options = driver.find_elements_by_xpath("//select[@id='ddlDistrict']/option")
                if di == len(dist_options):
                    break
                dist_opt = dist_options[di]
                dist_txt = dist_opt.text
                dist_a = dist_txt.split('-')
                dist_name = '-'.join(dist_a[1:])
                data = {'district_number': dist_a[0],
                        'district_name': dist_name}
                dist_opt.click()
                time.sleep(DELAY)
                ai = saved_ai
                while True:
                    ac_options = driver.find_elements_by_xpath("//select[@id='ddlAC']/option")
                    if ai == len(ac_options):
                        saved_ai = 1
                        break
                    ac_opt = ac_options[ai]
                    ac_txt = ac_opt.text
                    ac_a = ac_txt.split('-')
                    data['ac_number'] = ac_a[0]
                    data['ac_name'] = '-'.join(ac_a[1:])
                    ac_opt.click()
                    time.sleep(DELAY)
                    pi = saved_pi
                    while True:
                        xpath = "//select[@id='ddlPart']/option"
                        part_options = driver.find_elements_by_xpath(xpath)
                        if pi == len(part_options):
                            saved_pi = 1
                            break
                        part_opt = part_options[pi]
                        part_txt = part_opt.text
                        print("Downloading...{0:s} / {1:s} / {2:s}"
                                .format(dist_txt, ac_txt, part_txt))
                        part_a = part_txt.split('-')
                        data['part_number'] = part_a[0]
                        data['part_name'] = '-'.join(part_a[1:])
                        part_opt.click()
                        time.sleep(DELAY)
                        xpath = "//a[@id='hlDrafteroll']"
                        eroll = driver.find_element_by_xpath(xpath)
                        url = eroll.get_attribute('href')
                        fn = download_pdf(url, 'eroll', dist_a[0],
                                            ac_a[0], part_a[0])
                        data['type_of_roll'] = 'eroll'
                        data['file_name'] = fn
                        rows.append(data.copy())
                        # FIXME: get only first PDF link of Service voter
                        # It's same for all parts.
                        if pi == 1:
                            xpath = "//a[@id='hlServicevoter']"
                            service = driver.find_element_by_xpath(xpath)
                            url = service.get_attribute('href')
                            fn = download_pdf(url, 'service', dist_a[0],
                                                ac_a[0], part_a[0])
                            data['type_of_roll'] = 'service'
                            data['file_name'] = fn
                            rows.append(data.copy())
                        pi += 1
                        #break
                    ai += 1
                    #break
                di += 1
                #break
            driver.quit()
            break
        except Exception as e:
            if driver:
               try:
                   driver.quit()
               except:
                   pass
            saved_di = di
            saved_ai = ai
            saved_pi = pi
            print("WARN: {0!s}".format(e))
            time.sleep(5)

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('odisha.csv', columns=['district_number', 'district_name',
                                     'ac_name', 'ac_number', 'part_name',
                                     'part_number', 'type_of_roll',
                                     'file_name'], index=False,
              encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_odisha()
