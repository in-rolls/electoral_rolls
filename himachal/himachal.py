#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

import requests
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PyPDF2 import PdfFileReader


# FIXME: Explicit delay 
DELAY = 3
MAX_RETRY = 5
PDF_PATH = 'himachal_pdfs'


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


def is_valid_pdf(fn):
    """Check is the PDF valid
    """
    try:
        with open(fn, 'rb') as f:
            pdf = PdfFileReader(f)
            numpages = pdf.numPages
            pdf.close()
            return (numpages > 0)
    except Exception as e:
        return False


def scrape_himachal():
    """Scrape Electoral Rolls for Himachal Pradesh
       Download and save all PDF files and out the metadata to himachal.csv with
       the following columns:-

       district, assembly_segment, polling_station_name, file_name
    """

    rows = []
    saved_di = 1
    saved_ai = 1
    saved_pi = 1
    driver = None

    while True:
        try:
            options = Options()
            options.add_argument('-headless')

            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.download.manager.showWhenStarting", False)
            fp.set_preference("browser.download.dir", os.path.abspath(PDF_PATH))
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf,application/octet-stream")
            fp.set_preference('plugin.disable_full_page_plugin_for_types', 'application/pdf,application/x-pdf,application/octet-stream"')

            # disable Firefox's built-in PDF viewer
            fp.set_preference("pdfjs.disabled", True)

            # disable Adobe Acrobat PDF preview plugin
            fp.set_preference("plugin.scan.plid.all", False)
            fp.set_preference("plugin.scan.Acrobat", "99.0")

            # Please make sure geckodriver executable available in PATH setting.
            # https://github.com/mozilla/geckodriver/releases
            driver = webdriver.Firefox(fp, firefox_options=options)
            driver.implicitly_wait(20)

            driver.get("http://electionhp.gov.in/pscd/")

            di = saved_di
            while True:
                xpath = "//select[@id='ddlpc']/option"
                dist_options = driver.find_elements_by_xpath(xpath)
                if di == len(dist_options):
                    saved_di = 1
                    break
                dist_opt = dist_options[di]
                dist_txt = dist_opt.text.encode('utf-8')
                data = {'district': dist_txt}
                dist_opt.click()
                time.sleep(DELAY)
                ai = saved_ai
                while True:
                    xpath = "//select[@id='ddlac']/option"
                    ac_options = driver.find_elements_by_xpath(xpath)
                    if ai == len(ac_options):
                        saved_ai = 1
                        break
                    ac_opt = ac_options[ai]
                    ac_txt = ac_opt.text.encode('utf-8')
                    ac_val = int(ac_opt.get_attribute('value'))
                    data['assembly_segment'] = ac_txt
                    ac_opt.click()
                    time.sleep(DELAY)
                    pi = saved_pi
                    while True:
                        xpath = "//select[@id='ddlps']/option"
                        ps_options = driver.find_elements_by_xpath(xpath)
                        if pi == len(ps_options):
                            saved_pi = 1
                            break
                        ps_opt = ps_options[pi]
                        ps_txt = ps_opt.text.encode('utf-8')
                        ps_val = int(ps_opt.get_attribute('value'))
                        print("Downloading...{0:s} / {1:s} / {2:s}"
                                .format(dist_txt, ac_txt, ps_txt))
                        data['polling_station_name'] = ps_txt
                        ps_opt.click()
                        time.sleep(DELAY)
                        pdf_fn = 'A{0:03d}{1:04d}.pdf'.format(ac_val, ps_val)
                        pdf_path = os.path.join(PDF_PATH, pdf_fn)
                        data['file_name'] = pdf_path
                        rows.append(data.copy())
                        if not os.path.exists(pdf_path):
                            xpath = "//a[@id='HyperLink1']"
                            show_btn = driver.find_element_by_xpath(xpath)
                            jscript = "arguments[0].setAttribute('target','')"
                            driver.execute_script(jscript, show_btn)
                            show_btn.click()
                            time.sleep(DELAY)
                            xpath = "//button[@id='download']"
                            el = driver.find_element_by_xpath(xpath)
                            el.click()
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(DELAY)
                        if is_valid_pdf(pdf_path):
                            print("WARN: '{0:s}' is invalid".format(pdf_path))
                        pi += 1
                        #break
                    ai += 1
                    #break
                di += 1
                #break
            driver.quit()
            break
        except Exception as e:
            print("WARN: {0!s}".format(e))
            try:
                driver.quit()
            except:
                pass
            saved_di = di
            saved_ai = ai
            saved_pi = pi
            time.sleep(5)

    df = pd.DataFrame(rows)
    print("Writing the metadata to CSV file...")
    df.to_csv('himachal.csv', columns=['district', 'assembly_segment',
                                       'polling_station_name',
                                       'file_name'],
              index=False, encoding='utf-8')
    print("Done!")


if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)
    scrape_himachal()
