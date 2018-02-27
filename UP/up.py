#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  22 12:04:24 2017

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


def getConstt(m_url, i, element_C, element_D):
    driver, mySelect_D, num_D = getDistrict(m_url, element_D)
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id(element_C))
    return driver, mySelect_D, mySelect_C


m_url = "http://164.100.180.82/ceouptemp/RollPDF.aspx"
mdir = '../data/up/'
D_element = "ctl00_ContentPlaceHolder1_DDLDistrict"
C_element = "ctl00_ContentPlaceHolder1_DDL_AC"
button = "#ctl00_ContentPlaceHolder1_Button1"
driver, _, num_D = getDistrict(m_url, D_element)
driver.quit()
# Select Dist
i_start = 1
j_start = 1
k_start = 1
for i in range(i_start, num_D):
    driver, mySelect_D, _ = getDistrict(m_url, D_element)
    D_name = mySelect_D.options[i].text
    mySelect_D.options[i].click()
    # Select Constt.
    mySelect_C = Select(driver.find_element_by_id(C_element))
    num_C = len(mySelect_C.options)
    for j in range(j_start, num_C):
        C_name = mySelect_C.options[j].text
        mySelect_C.options[j].click()
        driver.find_element_by_css_selector(button).click()
        # Get HTML data from page
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        # Locate Links
        find_a = soup.find_all('a',  {"class": "linknavup1"}, href=True)
        base_url = find_a[0]['href'].split("P")[0]
        num = soup.find('span', {"id": "ctl00_ContentPlaceHolder1_Label1"}).text
        num_k = int(num.split("Total")[-1].split("record(s)")[0])
        for k in range(k_start, num_k):
            print(i, j, k)
            p = format(k, '03d')
            url = base_url + "P{}.pdf".format(p)
            filename = url.split("Rollpdf/")[-1].replace("/", "_")
            try:
                flag = utils.download_file_R(url, mdir, filename, "up.txt")
                if flag == 0:
                    with open("up.txt", "a") as myfile:
                        myfile.write(url + '\n')
            except urllib.error.HTTPError:
                with open("up.txt", "a") as myfile:
                    myfile.write(url + '\n')
        driver.quit()
        time.sleep(20)
        driver, mySelect_D, mySelect_C = getConstt(m_url, i, C_element, D_element)
