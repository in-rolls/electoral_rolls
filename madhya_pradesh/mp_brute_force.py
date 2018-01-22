#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 16:56:48 2018

@author: dhingratul
"""
import urllib
import time
import sys
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/MP/'
base_url = "http://ceomadhyapradesh.nic.in/erollpdf/"
i_start = 1
i_end = 231  # 231
j_start = 1

for i in range(i_start, i_end):
    time.sleep(10)
    if i == i_start:
        j = j_start - 1
    else:
        j = 0
    flag = 1
    while flag == 1:
        if j % 10 == 0:
            time.sleep(10)
        flag = 0
        j += 1
        print("\n", i, j)
        p1 = format(i, '03d')
        p2 = format(j, '03d')
        suffix = "A{}/S12A{}P{}.pdf".format(p1, p1, p2)
        url = base_url + suffix
        fid = suffix.replace("/", "_")
        try:
            flag = utils.download_file(url, mdir, fid)
            if flag == 0:
                with open("mp.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            break
