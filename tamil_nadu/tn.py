#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 14:10:33 2018

@author: dhingratul
"""
import time
import sys
from bs4 import BeautifulSoup
import re
import urllib
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/TN/'
m_url = "http://elections.tn.gov.in/PDF/"

i_start = 1
i_end = 235  # 235
j_start = 0

for i in range(i_start, i_end):
    time.sleep(5)
    p_url = m_url + "ac{}.htm".format(i)
    driver = utils.getDriver(p_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    driver.quit()
    find_a = soup.find_all('a', attrs={'href': re.compile("^http://")})
    if len(find_a) == 0:
        find_a = soup.find_all('a', attrs={'href': re.compile("^dt")})
    for j in range(j_start, len(find_a)):
        time.sleep(1)
        print("\n", i, j)
        url = find_a[j]['href']
        fid = url.split("PDF/")[1].replace("/", "_")
        try:
            flag = utils.download_file(url, mdir, fid)
            if flag == 0:
                with open("tn.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            with open("tn.txt", "a") as myfile:
                myfile.write(url + '\n')
