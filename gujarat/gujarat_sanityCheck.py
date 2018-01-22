#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:05:06 2018

@author: dhingratul
"""

import os
import sys
import pandas as pd
sys.path.insert(0, '../tools/')
import utils

mdir = '../data/Gujarat/'
direc = os.listdir(mdir)
for i in range(len(direc)):
    print(i, "/", len(direc))
    flag = utils.is_valid_pdf(mdir + direc[i])
    if flag is False:
        with open("Gujarat3.txt", "a") as myfile:
            myfile.write(direc[i] + '\n')


# Remove files (illegal/temp)
df = pd.read_table("Gujarat3.txt", header=None)
remove = True
if remove is True:
    for i in range(df.shape[0]):
        os.remove(mdir + df.iloc[i].as_matrix().tolist()[0])
