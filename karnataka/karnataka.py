import time
from selenium.webdriver.support.ui import Select
import urllib
import sys
from bs4 import BeautifulSoup
sys.path.insert(0, '../tools/')
import utils


mdir = '../data/Karnataka/'
# Total 39 ACs
i_start = 1
j_start = 1
num_ac = 40
for i in range(i_start, num_ac):
    m_url = "http://ceokarnataka.kar.nic.in/DraftRolls_2017/Part_List.aspx?ACNO={}".format(i)
    driver = utils.getDriver(m_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    # Locate table
    table = soup.find('table')
    rows = soup.findAll('tr')
    n_polls = len(rows) - 4
    driver.quit()
    for j in range(j_start,  n_polls + 1):
        print('\n', i, j)
        b_url = "http://ceokarnataka.kar.nic.in/DraftRolls_2017/Kannada/WOIMG/"
        p1 = format(i, '03d')
        p2 = format(j, '04d')
        suffix = "AC{}/AC{}{}.pdf" .format(p1, p1, p2)
        url = b_url + suffix
        fid = suffix.replace("/", "_")
        try:
            flag = utils.download_file_W(url, mdir, fid)
            if flag == 0:
                with open("karnataka.txt", "a") as myfile:
                    myfile.write(url + '\n')
        except urllib.error.HTTPError:
            with open("karnataka.txt", "a") as myfile:
                myfile.write(url + '\n')
