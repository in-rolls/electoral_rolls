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
import time


m_url = "http://210.212.18.115:8880/"
mdir = '../data/Bihar'
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': mdir}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)
driver.get(m_url)
# time.sleep(5)
# browser.quit()

# Select Dist
time.sleep(2)
mySelect_D = Select(driver.find_element_by_id("DropDownList1"))
i_start = 0
j_start = 0
for i in range(i_start, len(mySelect_D.options)):
    time.sleep(2)
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id("DropDownList2"))
    for j in range(j_start, len(mySelect_C.options)):
        time.sleep(1)
        print(i, j)
        mySelect_C.options[j].click()
        button = driver.find_element_by_xpath('//*[@id="ImagshowMR"]')
        button.send_keys(Keys.ENTER)

    driver.quit()
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(m_url)
    mySelect_D = Select(driver.find_element_by_id("DropDownList1"))
