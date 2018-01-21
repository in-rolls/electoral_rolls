import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import PyPDF2
import os.path
import os

#--------------------define variables-------------------
PDF_FOLDER = 'haryana_pdfs/'
OUTPUT_FILE = 'haryana.csv'
CSV_FLAG = True
#-------------------------------------------------------

#--------------------define global functions------------
def makeCookieString(cookie_dic):
    return "; ".join([str(key) + "=" + str(cookie_dic[key]) for key in cookie_dic]) + ';'

# -----------------------------------------------------------------------------------------------------------------------

class HaryanaScraper:
    def __init__(self,
                 base_url='http://ceoharyana.nic.in/?module=draftroll',
                 checkdraft_url='http://ceoharyana.nic.in/directs/check_draft.php'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url
        self.checkdraft_url = checkdraft_url

    def GetDistrictList(self):
        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            values = Selector(text=ret.text).xpath('//select[@id="district"]/option/@value').extract()
            names = Selector(text=ret.text).xpath('//select[@id="district"]/option/text()').extract()

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
        params = {}
        params['Type'] = 'dist'
        params['ID'] = district_id

        # set url
        url = self.checkdraft_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            values = Selector(text=ret.text).xpath('//select[@id="ac"]/option/@value').extract()
            names = Selector(text=ret.text).xpath('//select[@id="ac"]/option/text()').extract()

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
            print('failed to get constituency list')
            return None

    def GetPollingStationList(self, constituency_id):
        # set post data
        params = {}
        params['Type'] = 'ac'
        params['ID'] = constituency_id

        # set url
        url = self.checkdraft_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            values = Selector(text=ret.text).xpath('//select[@id="ps"]/option/@value').extract()
            names = Selector(text=ret.text).xpath('//select[@id="ps"]/option/text()').extract()

            stations = []
            for idx in range(0, len(values)):
                if values[idx] != '0':
                    station = {
                        'value': values[idx],
                        'name': names[idx]
                    }
                    stations.append(station)

            print(stations)
            return stations
        else:
            print('failed to get polling station list')
            return None

    def GetPdfInfo(self, station_id):
        # set post data
        params = {}
        params['Type'] = 'pdf'
        params['ID'] = station_id

        # set url
        url = self.checkdraft_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            download_url = Selector(text=ret.text).xpath('//a/@href').extract()[0]
            file_name = Selector(text=ret.text).xpath('//a/text()').extract()[0]

            pdf_info = {
                'download_url': download_url,
                'file_name': file_name.split('/')[1]
            }

            print(pdf_info)
            return pdf_info
        else:
            print('failed to get pdf information')
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
        header_info.append('polling_station_name')
        header_info.append('filename')

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
        # write header into output csv file
        if CSV_FLAG == True: self.WriteHeader()

        # get district list
        print('getting districts ...')
        districts = self.GetDistrictList()

        for district in districts:
            district_id = district['value']
            district_name = district['name']

            # get constituency list
            print('getting constituencies of %s ...' % (district_name))
            constituencies = self.GetConstituencyList(district_id)

            for constituency in constituencies:
                constituency_id = constituency['value']
                constituency_name =  constituency['name']

                # get station list
                print('getting polling stations of %s ...' % (constituency_name))
                stations = self.GetPollingStationList(constituency_id)

                for station in stations:
                    station_id = station['value']
                    station_name = station['name']

                    # get pdf information
                    print('getting pdf information of %s ...' % (station_name))
                    pdf_info = self.GetPdfInfo(station_id)

                    download_url = pdf_info['download_url']
                    filename = pdf_info['file_name']

                    # download and save pdf file
                    if self.CheckPdfFile(filename) == False:
                        print('downloading %s ...' % (filename))
                        self.DownloadPdfFile(download_url, filename)

                    if CSV_FLAG == True:
                        # write data into output csv file
                        data =[]
                        data.append(district_name)
                        data.append(constituency_name)
                        data.append(station_name)
                        data.append(filename)
                        self.WriteData(data)

            #         break
            #
            #     break
            # break



#------------------------------------------------------- main -------------------------------------------------------

def main():
    # create scraper object
    scraper = HaryanaScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()
