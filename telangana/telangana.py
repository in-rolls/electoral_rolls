import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import PyPDF2
import os.path
import os

#--------------------define variables-------------------
PDF_FOLDER = 'telangana_pdfs/'
OUTPUT_FILE = 'telangana.csv'
CSV_FLAG = True

# start_position = 'tel_07_020_131.pdf'
start_district_id = 1
start_constituency_id = 1
start_poll_station_no = 1
#-------------------------------------------------------

#--------------------define global functions------------
def makeCookieString(cookie_dic):
    return "; ".join([str(key) + "=" + str(cookie_dic[key]) for key in cookie_dic]) + ';'

# -----------------------------------------------------------------------------------------------------------------------
class TelanganaScraper:
    def __init__(self,
                 base_url='http://ceoaperms.ap.gov.in/TS_Rolls/Rolls.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

    def GetDistrictList(self):
        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            self.form_params = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
            }

            values = Selector(text=ret.text).xpath('//select[@id="ddlDist"]/option/@value').extract()
            names = Selector(text=ret.text).xpath('//select[@id="ddlDist"]/option/text()').extract()

            districts = []
            for idx in range(0, len(values)):
                if values[idx] != '0':
                    district = {
                        'value': values[idx],
                        'name': names[idx]
                    }
                    districts.append(district)

            print(districts)
            return districts
        else:
            print('failed to get district list')
            return None

    def GetConstituencyList(self, district_id):
        # set post data
        params = {
            '__VIEWSTATE': self.form_params['__VIEWSTATE'],
            '__EVENTVALIDATION': self.form_params['__EVENTVALIDATION']
        }
        params['__EVENTTARGET'] = 'ddlDist'
        params['ddlDist'] = district_id

        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            self.form_params = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
            }

            values = Selector(text=ret.text).xpath('//select[@id="ddlAC"]/option/@value').extract()
            names = Selector(text=ret.text).xpath('//select[@id="ddlAC"]/option/text()').extract()

            print(Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0])
            print(Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0])

            constituencies = []
            for idx in range(0, len(values)):
                if values[idx] != '0':
                    constituency = {
                        'value': values[idx],
                        'name': names[idx]
                    }
                    constituencies.append(constituency)

            print(constituencies)
            return constituencies
        else:
            print('fail to get constituency list')
            return None

    def GetPollingStationList(self, district_id, constituency_id):
        # set post data
        params = {
            '__VIEWSTATE': self.form_params['__VIEWSTATE'],
            '__EVENTVALIDATION': self.form_params['__EVENTVALIDATION']
        }
        params['ddlDist'] = district_id
        params['ddlAC'] = constituency_id
        params['btnGetPollingStations'] = 'Get+Polling+Stations'
        print(params)

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)
        print(ret.status_code)
        print(ret.url)
        if ret.status_code == 200:
            trs = Selector(text=ret.text).xpath('//table[@id="GridView1"]/tr').extract()

            stations = []
            for idx in range(1, len(trs)):
                tr = trs[idx]
                tds = Selector(text=tr).xpath('//td/text()').extract()

                base_file_name = '%s_%s_%s.pdf' % ('{0:02d}'.format(int(district_id)), '{0:03d}'.format(int(constituency_id)), '{0:03d}'.format(int(tds[0])))
                download_url = 'http://ceoaperms.ap.gov.in/TS_Rolls/PDFGeneration.aspx?urlPath=D:\SSR_2017_Final_Roles\Telangana\AC_%s\Telugu\S29A%sP%s.PDF' \
                               % (
                                   str('{0:03d}'.format(int(constituency_id))),
                                   str('{0:03d}'.format(int(constituency_id))),
                                   str('{0:03d}'.format(int(tds[0])))
                               )

                # append station for tel
                station = {
                    'poll_station_no': tds[0],
                    'poll_station_name': tds[1],
                    'poll_station_location': tds[2],
                    'language': 'Telugu',
                    'file_name': 'tel_' + base_file_name,
                    'download_url': download_url
                }
                stations.append(station)

                # append station for eng
                download_url = 'http://ceoaperms.ap.gov.in/TS_Rolls/PDFGeneration.aspx?urlPath=D:\SSR_2017_Final_Roles\Telangana\AC_%s\English\S29A%sP%s.PDF' \
                               % (
                                str('{0:03d}'.format(int(constituency_id))),
                                str('{0:03d}'.format(int(constituency_id))),
                                str('{0:03d}'.format(int(tds[0])))
                               )
                station = {
                    'poll_station_no': tds[0],
                    'poll_station_name': tds[1],
                    'poll_station_location': tds[2],
                    'language': 'English',
                    'file_name': 'eng_' + base_file_name,
                    'download_url': download_url
                }
                stations.append(station)

            print(stations)
            return stations
        else:
            print('failed to get polling station list')
            return None

    def DownloadPdfFile(self, download_url, filename):
        # set url
        url = download_url

        # get request
        ret = self.session.get(url, stream=True)

        if ret.status_code == 200:
            with open(PDF_FOLDER + filename, 'wb') as f:
                f.write(ret.content)
            print('success to download %s' % (filename))
        else:
            print('failed to get pdf information')

    def WriteHeader(self):
        # set headers
        header_info = []
        header_info.append('district_name')
        header_info.append('assembly_constituency')
        header_info.append('poll_station_no')
        header_info.append('poll_station_name')
        header_info.append('poll_station_location')
        header_info.append('language')
        header_info.append('file_name')

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def CheckPdfFile(self, file_name):
        if os.path.isfile(PDF_FOLDER + file_name) == True:
            if os.stat(PDF_FOLDER + file_name).st_size == 0:
                os.unlink(PDF_FOLDER + file_name)
                return False

            try:
                print(PDF_FOLDER + file_name);
                PyPDF2.PdfFileReader(open(PDF_FOLDER + file_name, "rb"))
            except PyPDF2.utils.PdfReadError:
                os.unlink(PDF_FOLDER + file_name)
                return False
            else:
                return True
        else:
            return False

    def Start(self):
        if start_district_id == 1 and start_constituency_id == 1 and start_poll_station_no == 1:
            # write header into output csv file
            if CSV_FLAG == True: self.WriteHeader()

        # get district list
        print('getting districts ...')
        districts = self.GetDistrictList()

        for district in districts:
            district_id = district['value']
            district_name = district['name']

            if int(district_id) < start_district_id: continue

            # get constituency list
            print('getting constituencies for %s ...' % (district_name))
            constituencies = self.GetConstituencyList(district_id)

            for constituency in constituencies:
                constituency_id = constituency['value']
                constituency_name =  constituency['name']

                if int(district_id) == start_district_id and int(constituency_id) < start_constituency_id: continue

                # get station list
                print('getting polling stations for %s ...' % (constituency_name))
                stations = self.GetPollingStationList(district_id, constituency_id)

                for station in stations:
                    poll_station_no = station['poll_station_no']
                    poll_station_name = station['poll_station_name']
                    poll_station_location = station['poll_station_location']
                    language = station['language']
                    file_name = station['file_name']
                    download_url = station['download_url']

                    if int(district_id) == start_district_id and int(constituency_id) == start_constituency_id and int(poll_station_no) < start_poll_station_no: continue

                    # download and save pdf file
                    if self.CheckPdfFile(file_name) == False:
                        print('downloading %s for station(%s) ...' % (file_name, poll_station_name))
                        self.DownloadPdfFile(download_url, file_name)

                    if CSV_FLAG == True:
                        # write data into output csv file
                        data =[]
                        data.append(district_name)
                        data.append(constituency_name)
                        data.append(poll_station_no)
                        data.append(poll_station_name)
                        data.append(poll_station_location)
                        data.append(language)
                        data.append(file_name)
                        self.WriteData(data)

            #         break
            #     break
            # break



#------------------------------------------------------- main -------------------------------------------------------

def main():
    # create scraper object
    scraper = TelanganaScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()