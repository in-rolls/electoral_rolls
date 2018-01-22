#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 12:53:49 2018

@author: dhingratul
"""
import time
from bs4 import BeautifulSoup
import urllib
import sys
sys.path.insert(0, '../tools/')
import utils

m_url = "http://ceomeghalaya.nic.in/erolls/erolldetails.html"
mdir = '../data/Meghalaya/'
page_url = "http://ceomeghalaya.nic.in/erolls/"
base_url = "http://ceomeghalaya.nic.in/erolls/pdf/english/"

driver = utils.getDriver(m_url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")
table = soup.find('table')
find_a = table.find_all('a', href=True)
driver.quit()
i_start = 1
j_start = 1
for i in range(i_start, len(find_a)):
    const_url = page_url + find_a[i]['href']
    ac = int(find_a[i]['href'].split("-")[0])
    driver = utils.getDriver(const_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    rows = soup.findAll('tr')
    driver.quit()
    for j in range(j_start, len(rows)):
        print("\n", i, j)
        p1 = format(ac, '03d')
        p2 = format(j, '04d')
        suffix = "A{}/A{}{}.pdf".format(p1, p1, p2)
        url = base_url + suffix
        fid = suffix.replace("/", "_")
        try:
            flag = utils.download_file_W(url, mdir, fid)
            if flag == 0:
                with open("Meghalaya.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            with open("Meghalaya.txt", "a") as myfile:
                myfile.write(url + '\n')
        time.sleep(2)
