#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:00:18 2018

@author: dhingratul
"""

import pandas as pd
import sys
import urllib
import time
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/Gujarat/'
df = pd.read_table("Andaman.txt", header=None)
i_start = 0
for i in range(i_start, df.shape[0]):
    if i % 50 == 0:
        time.sleep(5)
    print("\n", i, '/', df.shape[0])
    url = df.iloc[i].as_matrix()[0]
    fid = url.split("AllPdf/")[-1].replace("/", "")
    try:
        flag = utils.download_file_W(url, mdir, fid)
        if flag == 0:
            with open("Andaman2.txt", "a") as myfile:
                myfile.write(url + '\n')
    except urllib.error.HTTPError:
        with open("Andaman2.txt", "a") as myfile:
            myfile.write(url + '\n')
