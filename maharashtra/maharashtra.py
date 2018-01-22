#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 10:26:57 2017

@author: dhingratul
"""

import time
from selenium.webdriver.support.ui import Select
import urllib
import sys
sys.path.insert(0, '../tools/')
import utils


def getDistrict(m_url, element):
    driver = utils.getDriver(m_url)
    mySelect_D = Select(driver.find_element_by_id(element))
    num_D = len(mySelect_D.options)  # Start from 1, 0 -- Select
    return driver, mySelect_D, num_D


def getConstt(m_url, i, element):
    driver, mySelect_D, num_D = getDistrict(m_url, 'mainContent_DistrictList')
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id(element))
    return driver, mySelect_D, mySelect_C


m_url = 'https://103.23.150.75/Search/SearchPDF.aspx'
mdir = '../data/Maharashtra/'
driver, mySelect_D, num_D = getDistrict(m_url, 'mainContent_DistrictList')
for i in range(1, num_D):
    if i != 1:
        driver, mySelect_D, _ = getDistrict(m_url, 'mainContent_DistrictList')
    mySelect_D.options[i].click()
    # Select Constt.
    mySelect_C = Select(driver.find_element_by_id('mainContent_AssemblyList'))
    num_C = len(mySelect_C.options)
    for j in range(1, num_C):
        C_name = mySelect_C.options[j].text
        C_name = C_name.split(" - ")[0]
        mySelect_C.options[j].click()
        mySelect_P = Select(driver.find_element_by_id('mainContent_PartList'))
        num_P = len(mySelect_P.options)
        links = []
        names = []
        for k in range(1, num_P):
            print('\n', i, j, k)
            base_url = 'https://103.23.150.75/searchpdf/pdf/'
            p1 = format(int(C_name), '03d')
            p2 = format(int(mySelect_P.options[k].text.split(' - ')[0]), '04d')
            prefix = 'A{}/A{}{}.pdf'.format(p1, p1, p2)
            url = base_url + prefix
            fid = prefix.replace("/", "_")
            try:
                #flag = utils.download_file_W(url, mdir, fid, True)
                flag = utils.download_file_R(url, mdir, fid, "Maharashtra.txt")
                if flag == 0:
                    with open("Maharashtra.txt", "a") as myfile:
                        myfile.write(url + '\n')
            except urllib.error.HTTPError:
                with open("Maharashtra.txt", "a") as myfile:
                    myfile.write(url + '\n')
        driver.quit()
        time.sleep(10)
        driver, mySelect_D, mySelect_C = getConstt(m_url, i, 'mainContent_AssemblyList')

