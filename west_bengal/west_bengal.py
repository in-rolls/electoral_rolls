import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

# --------------------define variables-------------------
OUTPUT_FILE = 'west_bengal.csv'
DRAFT_ROLLS_FOLDER = 'wb_pdfs/draft_rolls/'
SUPPLEMENTS_FOLDER = 'wb_pdfs/supplements/'


# -------------------------------------------------------

# --------------------define global functions------------

# -----------------------------------------------------------------------------------------------------------------------
class WBScraper:
    def __init__(self,
                 base_url='http://wbceo.in/'
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
        url = 'http://wbceo.in/DistrictList.aspx'

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get district list
            hrefs = Selector(text=ret.text).xpath('//table[@class="dataTable"]/tbody/tr/td/a').extract()

            district_list = []
            for href in hrefs:
                district = {
                    'href': self.base_url + Selector(text=href).xpath('//@href').extract()[0],
                    'name': str(Selector(text=href).xpath('//text()').extract()[0]).split(
                        '\r\n                                ')[1]
                }
                district_list.append(district)

            return district_list
        else:
            print('fail to get district list')

    def GetACList(self, url):
        # set url
        url = url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get ac list
            trs = Selector(text=ret.text).xpath('//table[@class="dataTable"]/tbody/tr').extract()

            ac_list = []
            for tr in trs:
                ac = {
                    'no': str(Selector(text=tr).xpath('//td[1]/text()').extract()[0]).split(
                        '\r\n                            ')[1].split('\r\n')[0],
                    'href': self.base_url + Selector(text=tr).xpath('//td[2]/a/@href').extract()[0],
                    'name': str(Selector(text=tr).xpath('//td[2]/a/text()').extract()[0]).split(
                        '\r\n                                ')[1]
                }
                ac_list.append(ac)

            return ac_list
        else:
            print('fail to get ac list')

    def GetPSList(self, url, page):
        # set url
        url = url

        # set params
        if page > 1:
            params = {
                '__EVENTARGUMENT': 'Page$%s' % (page),
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvPs',
                '__EVENTVALIDATION': self.form_data['__EVENTVALIDATION'],
                '__VIEWSTATE': self.form_data['__VIEWSTATE'],
                '__VIEWSTATEENCRYPTED': self.form_data['__VIEWSTATEENCRYPTED'],
                'ctl00$TopMenu$srch': 'Search'
            }
        else:
            params = {}

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get ps form data
            self.form_data = {
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[
                    0],
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEENCRYPTED':
                    Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEENCRYPTED"]/@value').extract()[0]
            }

            # get ps list
            trs = Selector(text=ret.text).xpath('//table[@class="mGrid"]/tr').extract()

            ps_list = []
            for idx in range(1, len(trs) - 1):
                tr = trs[idx]
                ps = {
                    'no': Selector(text=tr).xpath('//td[1]/span/text()').extract()[0],
                    'name': Selector(text=tr).xpath('//td[2]/span/text()').extract()[0],
                    'draft_roll_href': self.base_url + Selector(text=tr).xpath('//td[3]/a/@href').extract()[0],
                    'supplement_href': self.base_url + Selector(text=tr).xpath('//td[4]/a/@href').extract()[0]
                }
                ps_list.append(ps)

            return ps_list
        else:
            print('fail to get ps list')

    def GetCaptchaTextFromImage(self, image_url):
        from python_anticaptcha import AnticaptchaClient, ImageToTextTask

        import requests
        from io import BytesIO
        try:
            import Image
        except ImportError:
            from PIL import Image

        api_key = 'YYYYYY'

        ret = self.session.get(image_url)
        captcha_fp = BytesIO(ret.content)

        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        return job.get_captcha_text()

    def GetCaptchaImageUrl(self, url):
        # set url
        url = url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            return ('http://wbceo.in/Capcha.ashx')
        else:
            print('fail to get captcha image url')

    def WriteHeader(self):
        # set headers
        header_info = [
            'district_name',
            'ac_no',
            'ac_name',
            'part_no',
            'polling_station_name',
            'filename']

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
            if start_district == district['name']: district_flag = True
            if district_flag == False: continue

            # get ac list
            print('getting ac list for %s...' % (district['name']))
            ac_list = self.GetACList(district['href'])
            print(ac_list)

            for ac in ac_list:
                if start_ac == ac['no']: ac_flag = True
                if ac_flag == False: continue

                page = 1
                while (True):
                    # get ps list
                    print('getting ac list for %s:%s page:%s...' % (district['name'], ac['name'], page))
                    ps_list = self.GetPSList(ac['href'], page)
                    print(ps_list)

                    if ps_list == None or len(ps_list) <= 0: break
                    page += 1

                    for ps in ps_list:
                        if start_ps == ps['no']: ps_flag = True
                        if ps_flag == False: continue

                        # # get captcha image url for draft_roll
                        # print('getting captcha image url for draft_roll...')
                        # captcha_image_url = self.GetCaptchaImageUrl(ps['draft_roll_href'])
                        # print(captcha_image_url)
                        #
                        # # get captcha text from image for draft_roll
                        # print('getting captcha text from image for draft_roll...')
                        # captcha_text = self.GetCaptchaTextFromImage(captcha_image_url)
                        # print(captcha_text)

                        # process draft roll
                        draft_roll_pdf_name = 'a%s%s.pdf' % (
                            str('{0:03d}'.format(int(ac['no']))),
                            str('{0:04d}'.format(int(ps['no']))),
                        )
                        draft_roll_pdf_url = 'http://wbceo.in/EROLLS/PDF/Bengali/A%s/%s' % (
                            str('{0:03d}'.format(int(ac['no']))),
                            draft_roll_pdf_name
                        )

                        self.DownloadPdfFile(draft_roll_pdf_url, DRAFT_ROLLS_FOLDER + draft_roll_pdf_name)

                        # write data into output csv file
                        data = []
                        data.append(district['name'])
                        data.append(ac['no'])
                        data.append(ac['name'])
                        data.append(ps['no'])
                        data.append(ps['name'])
                        data.append(DRAFT_ROLLS_FOLDER + draft_roll_pdf_name)
                        self.WriteData(data)

                        # process supplements
                        supplements_pdf_name = 'a%s%s.pdf' % (
                            str('{0:03d}'.format(int(ac['no']))),
                            str('{0:04d}'.format(int(ps['no']))),
                        )
                        supplements_pdf_url = 'http://wbceo.in/EROLLS/sup02/PDF/Bengali/A%s/%s' % (
                            str('{0:03d}'.format(int(ac['no']))),
                            supplements_pdf_name
                        )

                        self.DownloadPdfFile(supplements_pdf_url, SUPPLEMENTS_FOLDER + supplements_pdf_name)

                        # write data into output csv file
                        data = []
                        data.append(district['name'])
                        data.append(ac['no'])
                        data.append(ac['name'])
                        data.append(ps['no'])
                        data.append(ps['name'])
                        data.append(SUPPLEMENTS_FOLDER + supplements_pdf_name)
                        self.WriteData(data)

            #             break
            #         break
            #     break
            # break


# ------------------------------------------------------- main -------------------------------------------------------
def main():
    # create scraper object
    scraper = WBScraper()

    # start to scrape
    scraper.Start(
        start_district='MALDA',
        start_ac='50',
        start_ps='192'
    )


if __name__ == '__main__':
    main()
