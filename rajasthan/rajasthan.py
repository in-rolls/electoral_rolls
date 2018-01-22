#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 20:50:34 2018

@author: dhingratul
"""

import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import urllib
import sys
sys.path.insert(0, '../tools/')
import utils


def getDistrict(m_url, element):
    driver = utils.getDriver(m_url)
    mySelect_D = Select(driver.find_element_by_id(element))
    num_D = len(mySelect_D.options)  # Start from 1, 0 -- Select
    return driver, mySelect_D, num_D


def getConstt(m_url, i, element_C, element_D):
    driver, mySelect_D, num_D = getDistrict(m_url, element_D)
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id(element_C))
    return driver, mySelect_D, mySelect_C


m_url = "http://164.100.153.10/electoralroll/Draftroll_2018.aspx"
mdir = '../data/Rajasthan/'
base_url = "http://www.ceorajasthan.nic.in/erolls/pdf/dper-18/"
driver, _, num_D = getDistrict(m_url, "drddist")
driver.quit()
# Select Dist
i_start = 1
j_start = 1
k_start = 265
for i in range(i_start, num_D):
    driver, mySelect_D, _ = getDistrict(m_url, "drddist")
    mySelect_D.options[i].click()
    time.sleep(1)
    # Select Constt.
    mySelect_C = Select(driver.find_element_by_id("drdass"))
    num_C = len(mySelect_C.options)
    if i == i_start:
        j_start = j_start
    else:
        j_start = 1
    for j in range(j_start, num_C):
        if j != j_start:
            driver, mySelect_D, mySelect_C = getConstt(m_url, i, "drdass", "drddist")
        C_num = int(mySelect_C.options[j].get_attribute("value"))
        mySelect_C.options[j].click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        # Locate table
        table = soup.find('table', id='GridView1')
        rows = soup.findAll('tr')
        num_P = len(rows) - 81 + 1
        if i == i_start and j == j_start:
            k_start = k_start
        else:
            k_start = 1
        for k in range(k_start, num_P):
            print("\n", i, j, k)
            p1 = format(C_num, '03d')
            p2 = format(k, '03d')
            suffix = "A{}/A{}{}.pdf".format(p1, p1, p2)
            fid = suffix.replace("/", "_")
            url = base_url + suffix
            try:
                flag = utils.download_file_R(url, mdir, fid, "rajasthan.txt")
                # flag = utils.download_file_W(url, mdir, filename)
                if flag == 0:
                    with open("rajasthan.txt", "a") as myfile:
                        myfile.write(url + '\n')
            except urllib.error.HTTPError:
                with open("rajasthan.txt", "a") as myfile:
                    myfile.write(url + '\n')
        driver.quit()
        time.sleep(20)
