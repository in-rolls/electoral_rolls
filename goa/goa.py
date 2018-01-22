#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 09:49:05 2017

@author: dhingratul
"""
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import urllib
import sys
sys.path.insert(0, '../tools/')
import utils


def getDistrict(m_url, element):
    driver = utils.getDriver(m_url)
    mySelect_D = Select(driver.find_element_by_id(element))
    num_D = len(mySelect_D.options)  # Start from 1, 0 -- Select
    return driver, mySelect_D, num_D


m_url = "http://ceogoa.nic.in/appln/uil/ElectoralRoll.aspx"
base_url = 'http://ceogoa.nic.in/PDF/EROLL/2017/'
mdir = '../data/Goa/'
driver, _, num_D = getDistrict(m_url, 'ctl00_Main_drpAC')
driver.quit()

i_start = 1
j_start = 1
for i in range(i_start, num_D):
    driver, mySelect_D, _ = getDistrict(m_url, "ctl00_Main_drpAC")
    mySelect_D.options[i].click()
    # Click button
    driver.find_element_by_css_selector('#ctl00_Main_btnSearch').click()
    time.sleep(1)
    # Get HTML data from page
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    # Locate table
    table = soup.find('table', {'class': 'mGridView'})
    rows = soup.findAll('tr')
    n_rows = len(rows)
    driver.quit()
    for j in range(j_start, n_rows):
        print("\n", i, j)
        p1 = format(i, '03d')
        p2 = format(j, '02d')
        suffix = "AC{}/Part{}.pdf".format(p1, p2)
        url = base_url + suffix
        fid = suffix.replace("/", "_")
        try:
            flag = utils.download_file_W(url, mdir, fid)
            if flag == 0:
                with open("goa.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            with open("goa.txt", "a") as myfile:
                myfile.write(url + '\n')
