#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:06:50 2017

@author: dhingratul
"""

import urllib
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import sys
sys.path.insert(0, '../tools/')
import utils


def getUrlList(C_name, n_rows):
    L = []
    sf = []
    base_url = 'https://ceo.gujarat.gov.in/download/2017/'
    p1 = format(int(C_name.split('-')[0]), '03d')
    for i in range(1, n_rows + 1):
        p2 = format(i, '04d')
        suffix = 'NORMAL_AC{}/N{}{}.pdf'.format(p1, p1, p2)
        url = base_url + suffix
        L.append(url)
        sf.append(suffix)
    sf = list(map((lambda x: "".join(x.split("/"))), sf))
    return L, sf


def getTableNumber(m_url, mySelect_D, mySelect_C, i, j):
    C_name = mySelect_C.options[j].text
    mySelect_C.options[j].click()
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    # Locate table
    rows = soup.findAll('tr')
    n_rows = len(rows) - 11  # 11 due to tr elements at the top of page
    driver.quit()
    return C_name, n_rows


def getDistrict(m_url):
    driver = utils.getDriver(m_url)
    mySelect_D = Select(driver.find_element_by_id("drpdistrict"))
    num_D = len(mySelect_D.options)  # Start from 1, 0 -- Select
    return driver, mySelect_D, num_D


def getConstt(m_url, i):
    driver, mySelect_D, num_D = getDistrict(m_url)
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id("drpac"))
    return driver, mySelect_D, mySelect_C


m_url = 'http://erms.gujarat.gov.in/ceo-gujarat/master/frmEPDFRoll.aspx'
mdir = '../data/Gujarat/'
driver, mySelect_D, num_D = getDistrict(m_url)

for i in range(1, num_D):
    if i != 1:
        driver, mySelect_D, _ = getDistrict(m_url)
    mySelect_D.options[i].click()
    # Select Constt.
    mySelect_C = Select(driver.find_element_by_id("drpac"))
    num_C = len(mySelect_C.options)
    for j in range(1,  num_C):
        C_name, n_rows = getTableNumber(m_url, mySelect_D, mySelect_C, i, j)
        L, sf = getUrlList(C_name, n_rows)
        for k in range(1, len(L)):
            print('\n', i, j, k)
            try:
                # flag = utils.download_file(L[k], mdir, sf[k], True)
                flag = utils.download_file_R(L[k], mdir, sf[k], "Gujarat.txt")
                # flag = utils.download_file_W(L[k], mdir, sf[k])
                if flag == 0:
                    with open("Gujarat.txt", "a") as myfile:
                        myfile.write(L[k] + '\n')
            except urllib.error.HTTPError:
                with open("Gujarat.txt", "a") as myfile:
                    myfile.write(L[k] + '\n')
        driver.quit()
        time.sleep(20)
        driver, mySelect_D, mySelect_C = getConstt(m_url, i)
