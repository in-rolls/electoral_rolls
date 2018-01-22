#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:49:36 2017

@author: dhingratul
DONE
"""

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
import sys
import os
import time
sys.path.insert(0, '../tools/')
import utils


def getFile(mdir, m_url, i, j):
    # file_path = mdir + "FinalRoll_ACNo_{}PartNo_{}.pdf".format(i + 1, j + 1)
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': mdir}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(m_url)
    mySelect_D = Select(driver.find_element_by_id("DropDownList1"))
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id("DropDownList2"))
    mySelect_C.options[j].click()
    button = driver.find_element_by_xpath('//*[@id="ImagshowMR"]')
    button.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.quit()


# Retry file
m_url = "http://210.212.18.115:8880/"
mdir = '../data/Bihar/'
df = pd.read_table("bihar3.txt", header=None)
missing = df[0].str.split(".pdf").str[0]
ids = missing.str.split("ACNo_").str[1]
ac = ids.str.split("PartNo_").str[0]
part = ids.str.split("PartNo_").str[1]
fid = list(zip(ac, part))
k_start = 879 # 0
for k in range(k_start, len(fid)):
    print(k)
    # indexing starts at 1
    try:
        getFile(mdir, m_url, int(fid[k][0]) - 1, int(fid[k][1]) - 1)
    except ValueError:
         getFile(mdir, m_url, int(fid[k][0]) - 1, int(fid[k][1].split("(")[0]) - 1)

# Remove files (illegal/temp)
remove = True
if remove is True:
    for i in range(1, df.shape[0]):
        os.remove(mdir + df.iloc[i].as_matrix().tolist()[0])

