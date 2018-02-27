#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 13:29:51 2018

@author: dhingratul
"""

import pandas as pd
import sys
import urllib
import os
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/up/'
prefix = 'http://164.100.180.82/Rollpdf/'
df = pd.read_table("up3.txt", header=None)
for i in range(df.shape[0]):
    print(i, '/', df.shape[0])
    fid = df.iloc[i].as_matrix()[0]
    t_url = prefix + fid.replace("_", "/")
    try:
        flag = utils.download_file_W(t_url, mdir, fid)
        if flag == 0:
            with open("up4.txt", "a") as myfile:
                myfile.write(fid + '\n')
    except urllib.error.HTTPError:
            with open("up4.txt", "a") as myfile:
                myfile.write(fid + '\n')

# Remove files (illegal/temp)
df = pd.read_table("up4.txt", header=None)
remove = True
if remove is True:
    for i in range(df.shape[0]):
        print(i)
        try:
            os.remove(mdir + df.iloc[i].as_matrix().tolist()[0])
        except FileNotFoundError:
            pass
