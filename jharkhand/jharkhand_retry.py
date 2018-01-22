#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:00:18 2018

@author: dhingratul
"""

import pandas as pd
import sys
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/Jharkhand/'
df = pd.read_table("jharkhand.txt", header=None)
for i in range(df.shape[0]):
    print(i, '/', df.shape[0])
    url = df.iloc[i].as_matrix()[0]
    fid = url.split("ceopdf/")[-1].replace("/", "_")
    flag = utils.download_file(url, mdir, fid)
    if flag == 0:
        with open("jharkhand2.txt", "a") as myfile:
            myfile.write(url + '\n')