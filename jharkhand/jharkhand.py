#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  21 9:033:24 2017

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


def getConstt(m_url, i, element_C, element_D):
    driver, mySelect_D, num_D = getDistrict(m_url, element_D)
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id(element_C))
    return driver, mySelect_D, mySelect_C


m_url = "http://164.100.150.3/mrollpdf1/aceng.aspx"
base_url = "http://164.100.150.3/mrollpdf1/ceopdf/"
mdir = '../data/Jharkhand/'
driver, mySelect_D, num_D = getDistrict(m_url, "ddlDistrict")

# Select Dist
i_start = 1
j_start = 1
k_start = 1
num_D = len(mySelect_D.options)
for i in range(i_start, num_D):
    if i != i_start:
        driver, mySelect_D, _ = getDistrict(m_url, "ddlDistrict")
    D_name = mySelect_D.options[i].text
    mySelect_D.options[i].click()
    # Select Constt.
    mySelect_C = Select(driver.find_element_by_id("ddlAC"))
    num_C = len(mySelect_C.options)
    for j in range(j_start, num_C):
        C_name = mySelect_C.options[j].text
        mySelect_C.options[j].click()
        mySelect_P = Select(driver.find_element_by_id("ddlPart"))
        num_P = len(mySelect_P.options)
        p1 = format(int(C_name.split("-")[0]), '03d')
        for k in range(k_start, num_P):
            print(i, j, k)
            poll = mySelect_P.options[k].text
            p2 = format(int(poll.split("-")[0]), '04d')
            suffix = "MR{}/MR{}{}.PDF".format(p1, p1, p2)
            url = base_url + suffix
            filename = suffix.replace("/", "_")
            try:
                flag = utils.download_file_R(url, mdir, filename)
                if flag == 0:
                    with open("jharkhand.txt", "a") as myfile:
                        myfile.write(url + '\n')
            except urllib.error.HTTPError:
                with open("jharkhand.txt", "a") as myfile:
                    myfile.write(url + '\n')
        driver.quit()
        time.sleep(20)
        driver, mySelect_D, mySelect_C = getConstt(m_url, i, "ddlAC", "ddlDistrict")
