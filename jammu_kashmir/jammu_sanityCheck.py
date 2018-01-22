#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:05:06 2018

@author: dhingratul
"""

import os
import sys
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/JK/'
direc = os.listdir(mdir)
for i in range(len(direc)):
    print(i, "/", len(direc))
    flag = utils.is_valid_pdf(mdir + direc[i])
    if flag is False:
        with open("jammu3.txt", "a") as myfile:
            myfile.write(direc[i] + '\n')
