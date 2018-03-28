import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

# --------------------define variables-------------------
OUTPUT_FILE = 'karnataka_2016.csv'
PDF_FOLDER = 'karnataka_2016/'


class KarnatakaScraper:
    def __init__(self,
                 base_url='http://ceokarnataka.kar.nic.in'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

        self.form_data = {
            '__EVENTVALIDATION': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEENCRYPTED': ''
        }

    def GetDistrictList(self):
        # set url
        url = 'http://ceokarnataka.kar.nic.in/FinalRoll_2016/Dist_List.aspx'

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get district list
            trs = Selector(text=ret.text).xpath('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr').extract()

            district_list = []
            for idx in range(1, len(trs)):
                tr = trs[idx]
                district = {
                    'no': Selector(text=tr).xpath('//td[1]/font/text()').extract()[0],
                    'name': Selector(text=tr).xpath('//td[2]/font/a/text()').extract()[0]
                }
                district_list.append(district)

            return district_list
        else:
            print('fail to get district list')

    def GetACList(self, district_no):
        # set url
        url = 'http://ceokarnataka.kar.nic.in/FinalRoll_2016/AC_List.aspx'

        # set params
        params = {
            'DistNo': district_no
        }

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            # get district list
            trs = Selector(text=ret.text).xpath('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr').extract()

            ac_list = []
            for idx in range(1, len(trs)):
                tr = trs[idx]
                ac = {
                    'no': Selector(text=tr).xpath('//td[1]/font/text()').extract()[0],
                    'name': Selector(text=tr).xpath('//td[2]/font/a/text()').extract()[0]
                }
                ac_list.append(ac)

            return ac_list
        else:
            print('fail to get ac list')

    def GetPSList(self, ac_no):
        # set url
        url = 'http://ceokarnataka.kar.nic.in/FinalRoll_2016/Part_List.aspx'

        # set params
        params = {
            'ACNO': ac_no
        }

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            # get district list
            trs = Selector(text=ret.text).xpath('//table[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr').extract()

            ps_list = []
            for idx in range(1, len(trs)):
                tr = trs[idx]
                ps = {
                    'no': Selector(text=tr).xpath('//td[2]/font/text()').extract()[0],
                    'name': Selector(text=tr).xpath('//td[3]/font/a/text()').extract()[0]
                }
                ps_list.append(ps)

            return ps_list
        else:
            print('fail to get ps list')

    def WriteHeader(self):
        # set headers
        header_info = [
            'district_no',
            'district_name',
            'ac_no',
            'ac_name',
            'part_no',
            'polling_station_name',
            'filename'
        ]

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a', encoding='utf-8'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def DownloadPdfFile(self, download_url, filename):
        print('downloading %s' % (filename))
        if os.path.isfile(filename) == True:
            print('this file already downloaded.')
            return

        # set url
        url = download_url

        # get request
        ret = self.session.get(url, stream=True)

        if ret.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(ret.content)
            print('success to download %s' % (filename))
        else:
            print('fail to get pdf file: %s' % (download_url))

    def Start(self,
              start_district='',
              start_ac='',
              start_ps=''):
        # write header into output csv file
        if start_district == '' and start_ac == '' and start_ps == '': self.WriteHeader()

        # get district list
        print('getting district list...')
        district_list = self.GetDistrictList()
        print(district_list)

        district_flag = False
        if start_district == '': district_flag = True

        ac_flag = False
        if start_ac == '': ac_flag = True

        ps_flag = False
        if start_ps == '': ps_flag = True

        for district in district_list:
            if start_district == district['no']: district_flag = True
            if district_flag == False: continue

            # get ac list
            print('getting ac list for %s...' % (district['name']))
            ac_list = self.GetACList(district['no'])
            print(ac_list)

            for ac in ac_list:
                if start_ac == ac['no']: ac_flag = True
                if ac_flag == False: continue

                # get ps list
                print('getting ac list for %s:%s...' % (district['name'], ac['name']))
                ps_list = self.GetPSList(ac['no'])
                print(ps_list)

                for ps in ps_list:
                    if start_ps == ps['no']: ps_flag = True
                    if ps_flag == False: continue

                    # process draft roll
                    file_name = 'AC%s%s.pdf' % (
                        str('{0:03d}'.format(int(ac['no']))),
                        str('{0:04d}'.format(int(ps['no']))),
                    )
                    draft_roll_pdf_url = 'http://ceokarnataka.kar.nic.in/FinalRoll_2016/Kannada/WOIMG/AC%s/%s' % (
                        str('{0:03d}'.format(int(ac['no']))),
                        file_name
                    )
                    self.DownloadPdfFile(draft_roll_pdf_url, PDF_FOLDER + file_name)

                    # write data into output csv file
                    data = []
                    data.append(district['no'])
                    data.append(district['name'])
                    data.append(ac['no'])
                    data.append(ac['name'])
                    data.append(ps['no'])
                    data.append(ps['name'])
                    data.append(file_name)
                    self.WriteData(data)

            #         break
            #     break
            # break

def main():
    # create scraper object
    scraper = KarnatakaScraper()

    # start to scrape
    scraper.Start(
        start_district='',
        start_ac='',
        start_ps=''
    )


if __name__ == '__main__':
    main()
