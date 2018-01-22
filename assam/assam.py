#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:10:36 2017

@author: dhingratul
"""
from bs4 import BeautifulSoup
import time
import urllib
import sys
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/Assam/'
html = 'soup.html'
url_prefix = 'http://ceoassam.nic.in'
soup = BeautifulSoup(open(html), "html.parser")
rows = soup.findAll('a', href=True)
i_start = 0
for i in range(i_start, len(rows)):
    print(i, '/', len(rows))
    time.sleep(2)
    if i % 100 == 0:
        time.sleep(20)
    url = rows[i]['href']
    if not url:
        pass
    else:
        filename = url.split(".", 1)[1]
        filename = filename.split("/", 1)[1]
        filename = filename.replace("/", "_")
        m_url = url_prefix + url.split(".", 1)[1]  # Split on first delim
        try:
            flag = utils.download_file(m_url, mdir, filename)
            if flag == 0:
                with open("assam.txt", "a") as myfile:
                    myfile.write(m_url + '\n')
        except urllib.error.HTTPError:
            with open("assam.txt", "a") as myfile:
                myfile.write(m_url + '\n')
