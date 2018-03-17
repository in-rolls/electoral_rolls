import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os

#--------------------define variables-------------------
OUTPUT_FILE = 'jammu_kashmir.csv'
REPORT_TYPE = 'PS Wise Report'

OUTPUT_FOLDER = 'pdfs/'
#-------------------------------------------------------

#--------------------define global functions------------

# -----------------------------------------------------------------------------------------------------------------------
class JKScraper:
    def __init__(self,
                 base_url='http://ceojk.nic.in/ElectionPDF/Main.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

    def GetLanguageList(self):
        return [
            'English',
            'Hindi',
            'Urdu'
        ]

    def GetMainFormData(self):
        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get form data
            self.form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION':Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }


        else:
            print('fail to get main form data')

    def GetDistrictList(self, report_type, language):
        # set post data
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__EVENTVALIDATION': self.form_data['__EVENTVALIDATION'],
            '__VIEWSTATE': self.form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.form_data['__VIEWSTATEGENERATOR'],
            'Button1': 'Show',
            'RadioButtonList1': report_type,
            'RadioButtonList2': language
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get district form data
            self.district_form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            # get district list
            options = Selector(text=ret.text).xpath('//select[@id="DistlistP"]/option').extract()

            district_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                district = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                district_list.append(district)

            return district_list
        else:
            print('fail to get district list')

    def GetACList(self, report_type, language, district_id):
        # set post data
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'DistlistP',
            '__EVENTVALIDATION': self.district_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.district_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.district_form_data['__VIEWSTATEGENERATOR'],
            'DistlistP': district_id,
            'RadioButtonList1': report_type,
            'RadioButtonList2': language,
            'txtinput': ''
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get ac form data
            self.ac_form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            # get ac list
            options = Selector(text=ret.text).xpath('//select[@id="AclistP"]/option').extract()

            ac_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                ac = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                ac_list.append(ac)

            return ac_list
        else:
            print('fail to get ac list')

    def GetPSList(self, report_type, language, district_id, ac_id):
        # set post data
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'AclistP',
            '__EVENTVALIDATION': self.ac_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.ac_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.ac_form_data['__VIEWSTATEGENERATOR'],
            'AclistP': ac_id,
            'DistlistP': district_id,
            'RadioButtonList1': report_type,
            'RadioButtonList2': language,
            'txtinput': ''
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get ps form data
            self.ps_form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            # get ps list
            options = Selector(text=ret.text).xpath('//select[@id="PslistP"]/option').extract()

            ps_list = []
            for idx in range(1, len(options)):
                option = options[idx]

                name = Selector(text=option).xpath('//text()').extract()
                if len(name) > 0:
                    name = name[0]
                else:
                    name = ''

                ps = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': name
                }
                ps_list.append(ps)

            return ps_list
        else:
            print('fail to get ps list')

    def GetCaptchaImageUrl(self, report_type, language, district_id, ac_id, ps_id):
        # set post data
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'PslistP',
            '__EVENTVALIDATION': self.ps_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.ps_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.ps_form_data['__VIEWSTATEGENERATOR'],
            'AclistP': ac_id,
            'DistlistP': district_id,
            'PslistP': ps_id,
            'RadioButtonList1': report_type,
            'RadioButtonList2': language,
            'txtinput': ''
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get ps form data
            self.captcha_form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            captcha_image_url = 'http://ceojk.nic.in/ElectionPDF/' + Selector(text=ret.text).xpath('//img[@alt="Captcha"]/@src').extract()[0]
            return captcha_image_url
        else:
            print('fail to get captcha image url')

    def GetDetailInformation(self, report_type, language, district_id, ac_id, ps_id, captcha_text):
        # set post data
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            '__EVENTVALIDATION': self.captcha_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.captcha_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.captcha_form_data['__VIEWSTATEGENERATOR'],
            'AclistP': ac_id,
            'DistlistP': district_id,
            'PslistP': ps_id,
            'BtnPs': 'Get Report',
            'RadioButtonList1': report_type,
            'RadioButtonList2': language,
            'txtinput': captcha_text
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get download form data
            self.download_form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            }

            temp = Selector(text=ret.text).xpath('//span[@id="errlbl"]/b/font/text()').extract()
            if len(temp) > 0 and temp[0] == 'Report Does Not Exist':
                filename = 'null'
            else:
                temp = Selector(text=ret.text).xpath('//span[@id="FName"]/font/text()').extract()
                if len(temp) > 0:
                    filename = temp[0]
                else:
                    temp = Selector(text=ret.text).xpath('//span[@id="FName"]/text()').extract()
                    if len(temp) > 0:
                        filename = temp[0]
                    else:
                        # filename = temp[0]
                        filename = 'error'

            detail_info = {
                'filename': filename
            }
            return detail_info
        else:
            print('fail to get detail information')

    def GetCaptchaTextFromImage(self, image_url):
        from python_anticaptcha import AnticaptchaClient, ImageToTextTask

        import requests
        from io import BytesIO
        try:
            import Image
        except ImportError:
            from PIL import Image

        api_key = 'API KEY'

        response = requests.get(image_url)
        captcha_fp = BytesIO(response.content)

        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()
        return job.get_captcha_text()

    def WriteHeader(self):
        # set headers
        header_info = []
        header_info.append('language')
        header_info.append('district_number')
        header_info.append('district_name')
        header_info.append('ac_number')
        header_info.append('ac_name')
        header_info.append('ps_number')
        header_info.append('ps_name')
        header_info.append('filename')

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a', encoding='utf-8'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def DownloadPdfFile(self, report_type, language, district_id, ac_id, ps_id, download_url, filename):
        print('downloading %s' % (download_url))
        if os.path.isfile(filename) == True:
            print('this file already downloaded.')
            return 'ok'

        # set post data
        params = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'LnkFile',
            '__EVENTVALIDATION': self.download_form_data['__EVENTVALIDATION'],
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.download_form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.download_form_data['__VIEWSTATEGENERATOR'],
            'AclistP': ac_id,
            'DistlistP': district_id,
            'PslistP': ps_id,
            'RadioButtonList1': report_type,
            'RadioButtonList2': language,
            'txtinput': ''
        }

        # set url
        url = download_url

        # get request
        ret = self.session.post(url, data=params, stream=True)

        if ret.status_code == 200:
            # print(ret.content)
            with open(filename, 'wb') as f:
                f.write(ret.content)
            print('success to download %s' % (filename))
            return 'ok'
        else:
            print('fail to get pdf file: %s' % (download_url))
            return 'fail'

    def Start(self,
              START_LANGUAGE = '',
              START_DISTRICT = '',
              START_AC = '',
              START_PS = ''):

        error_flag = True
        while(error_flag == True):
            error_flag = False

            # write header into output csv file
            if START_LANGUAGE == '' and START_DISTRICT == '' and START_AC == '' and START_PS == '': self.WriteHeader()

            # get main form data
            print('getting main form data ...')
            self.GetMainFormData()
            print(self.form_data)

            # get language list
            print('getting language list ...')
            language_list = self.GetLanguageList()
            print(language_list)

            language_flag = False
            if START_LANGUAGE == '': language_flag = True

            district_flag = False
            if START_DISTRICT == '': district_flag = True

            ac_flag = False
            if START_AC == '': ac_flag = True

            ps_flag = False
            if START_PS == '': ps_flag = True

            for language in language_list:
                if START_LANGUAGE == language: language_flag = True
                if language_flag == False: continue

                # get district list
                print('getting district list for %s:%s...' % (REPORT_TYPE, language))
                district_list = self.GetDistrictList(REPORT_TYPE, language)
                print(district_list)

                for district in district_list:
                    if START_DISTRICT == district['value']: district_flag = True
                    if district_flag == False: continue

                    # get ac list
                    print('getting ac list for %s:%s:%s...' % (REPORT_TYPE, language, district['name']))
                    ac_list = self.GetACList(REPORT_TYPE, language, district['value'])
                    print(ac_list)

                    for ac in ac_list:
                        if START_AC == ac['value']: ac_flag = True
                        if ac_flag == False: continue

                        # get ps list
                        print('getting ac list for %s:%s:%s:%s...' % (REPORT_TYPE, language, district['name'], ac['name']))
                        ps_list = self.GetPSList(REPORT_TYPE, language, district['value'], ac['value'])
                        print(ps_list)

                        for ps in ps_list:
                            if START_PS == ps['value']: ps_flag = True
                            if ps_flag == False: continue

                            print('getting ac list for %s:%s:%s:%s:%s...' % (
                            REPORT_TYPE, language, district['name'], ac['name'], ps['name']))
                            # get captcha image url
                            print('getting captcha image url...')
                            captcha_image_url = self.GetCaptchaImageUrl(REPORT_TYPE, language, district['value'],
                                                                        ac['value'], ps['value'])
                            print(captcha_image_url)

                            # get captcha text from image
                            print('getting captcha text from image...')
                            captcha_text = self.GetCaptchaTextFromImage(captcha_image_url)
                            print(captcha_text)

                            # get detail information(filename)
                            print('getting detail information(filename)...')
                            detail_info = self.GetDetailInformation(REPORT_TYPE, language, district['value'], ac['value'], ps['value'], captcha_text)
                            print(detail_info)

                            if detail_info['filename'] == 'error':
                                START_LANGUAGE = language
                                START_DISTRICT = district['value']
                                START_AC = ac['value']
                                START_PS = ps['value']
                                error_flag = True
                                print('restart===================================================================')
                                break
                            else:
                                self.DownloadPdfFile(REPORT_TYPE, language, district['value'], ac['value'], ps['value'], self.base_url, OUTPUT_FOLDER + detail_info['filename'])

                            # write data into output csv file
                            data = []
                            data.append(language)
                            data.append(district['value'])
                            data.append(district['name'])
                            data.append(ac['value'])
                            data.append(ac['name'])
                            data.append(ps['value'])
                            data.append(ps['name'])
                            data.append(detail_info['filename'])
                            self.WriteData(data)

                        if error_flag == True: break
                    if error_flag == True: break
                if error_flag == True: break

                #             break
                #         break
                #     break
                # break

#------------------------------------------------------- main -------------------------------------------------------
def main():
    # create scraper object
    scraper = JKScraper()

    # start to scrape
    scraper.Start(
              START_LANGUAGE = 'Urdu',
              START_DISTRICT = '8',
              START_AC = '50',
              START_PS = '43')

if __name__ == '__main__':
    main()
