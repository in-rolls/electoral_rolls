#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 23:28:58 2017

@author: dhingratul
"""
import urllib.request
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import ssl
import requests
import wget
from PyPDF2 import PdfFileReader


def download_file(pdf_url, mdir, filename, flag=False):
    if flag is True:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(pdf_url, context=context)
    else:
        response = urllib.request.urlopen(pdf_url)

    filename = mdir + filename
    file = open(filename, 'wb')
    file.write(response.read())
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1
    file.close()
    return flag


def download_file_R(pdf_url, mdir, filename, file_out):
    requests.packages.urllib3.disable_warnings()
    while True:  # Keep trying until the webpage successfully downloads
        try:
            r = requests.get(pdf_url, verify=False, timeout=10)
            break  # If it downloads, get out and get on with life
        # If it doesn't download after the timeout period, an exceptions is thrown, and we try again
        except requests.exceptions.RequestException as e:
            with open(file_out, "a") as myfile:
                myfile.write(pdf_url + '\n')

    filename = mdir + filename
    with open(filename,  'wb') as f:
        f.write(r.content)
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1

    return flag


def download_file_W(pdf_url, mdir, filename, flag=False):
    filename = mdir + filename
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(pdf_url, filename)
    if os.stat(filename).st_size == 0:
        flag = 0
    else:
        flag = 1
    return flag


def getDriver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def driverRefresh(driver, m_url, i, j):
    driver.quit()
    driver = getDriver(m_url)
    mySelect_D = Select(driver.find_element_by_id("ddlDist"))
    mySelect_D.options[i].click()
    mySelect_C = Select(driver.find_element_by_id("ddlAC"))
    mySelect_C.options[j].click()
    driver.find_element_by_css_selector('#btnGetPollingStations').click()
    # Get HTML data from page
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    # Locate table
    rows = soup.findAll('tr')
    cols = rows[4].findAll('td')
    return driver, cols


def is_valid_pdf(fn):
    """Check is the PDF valid """
    try:
        with open(fn, 'rb') as f:
            pdf = PdfFileReader(f)
            numpages = pdf.numPages
        return (numpages > 0)
    except Exception as e:
        return False
