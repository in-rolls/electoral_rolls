#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 3 2017

Webscrape
@author: dhingratul
"""


import urllib
import sys
sys.path.insert(0, '../tools/')
import utils

i_start = 1
i_end = 401

mdir = '../data/Andaman/'
base_url = "http://as1.and.nic.in/newElection/AllPdf/"
for i in range(i_start, i_end + 1):
    print("\n", i)
    url = base_url + str(i) + '.pdf'
    fid = "PART" + "_" + str(i) + '.pdf'
    try:
        flag = utils.download_file(url, mdir, fid)
        if flag == 0:
            with open("Andaman.txt", "a") as myfile:
                myfile.write(url + '\n')
    except urllib.error.HTTPError:
        with open("Andaman.txt", "a") as myfile:
            myfile.write(url + '\n')

