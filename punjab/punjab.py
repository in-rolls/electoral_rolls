import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import PyPDF2
import os.path
import os

#--------------------define variables-------------------
PDF_FOLDER = 'punjab_pdfs/'
HTML_FOLDER = 'punjab_htmls/'
OUTPUT_FILE = 'punjab.csv'
ERROR_URL_FILE = 'error_url.csv'
CSV_FLAG = True
#-------------------------------------------------------

#--------------------define global functions------------
def makeCookieString(cookie_dic):
    return "; ".join([str(key) + "=" + str(cookie_dic[key]) for key in cookie_dic]) + ';'

# -----------------------------------------------------------------------------------------------------------------------

class PunjabScraper:
    def __init__(self,
                 base_url='http://ceopunjab.nic.in/English/fper.aspx'
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
            # print(ret.text)
            areas = Selector(text=ret.text).xpath('//map[@name="FPMap2"]/area/@href').extract()

            districts = []
            for idx in range(0, len(areas)):
                district = {
                    'district_url': 'http://ceopunjab.nic.in/English/' + areas[idx],
                    'name': areas[idx].split('.')[0]
                }
                districts.append(district)

            print(districts)
            return districts
        else:
            print('failed to get district list')
            return None

    def GetConstituencyList(self, url):
        # set url
        # url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            areas = Selector(text=ret.text).xpath('//map[@name="FPMap2"]/area/@href').extract()

            constituencies = []
            for idx in range(0, len(areas)):
                district = {
                    'constrituency_url': 'http://ceopunjab.nic.in/English/' + areas[idx],
                    'id': areas[idx].split('=')[1]
                }
                constituencies.append(district)

            print(constituencies)
            return constituencies
        else:
            print('failed to get constituency list')
            return None

    def GetIntermediateHtml(self, url):
        # set url
        # url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            with open(HTML_FOLDER + 'temp_intermediate.html', 'wb') as f:
                f.write(ret.content)

            self.form_params = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
                'ctl00$CheckJS45$hfClientJSEnabled': 'True',
                'ctl00$ContentPlaceHolder1$btnVoterlist': 'Electoral+Rolls+(PDF)'
            }
            # print(self.form_params)

            trs = Selector(text=ret.text).xpath('//div[@id="ctl00_ContentPlaceHolder1_AcPanel"]/table[1]/tr').extract()
            intermediate_data = {
                'assembly_constituency': Selector(text=trs[0]).xpath('//td[3]/font/text()').extract()[0],
                'total_voters': Selector(text=trs[1]).xpath('//td[3]/font/text()').extract()[0],
                'total_polling_stations': Selector(text=trs[2]).xpath('//td[3]/font/text()').extract()[0],
                'total_polling_station_locations': Selector(text=trs[3]).xpath('//td[3]/font/text()').extract()[0],
                'assembly_constituency_district': Selector(text=trs[4]).xpath('//td[3]/font/text()').extract()[0],
                'ero': Selector(text=trs[5]).xpath('//td[3]/font/text()').extract()[0],
                'mla': Selector(text=trs[6]).xpath('//td[3]/font/text()').extract()[0],
                'parliamentary_constituency': Selector(text=trs[7]).xpath('//td[3]/font/text()').extract()[0],
                'mp': Selector(text=trs[8]).xpath('//td[3]/font/text()').extract()[0]
            }
            print(intermediate_data)
            return(intermediate_data)
        else:
            print('failed to get constituency list')
            return None

    def GetFinalHtml(self, url):
        print(url)
        # set post data
        params = self.form_params

        # set url
        # url = self.base_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            with open(HTML_FOLDER + 'temp_final.html', 'wb') as f:
                f.write(ret.content)

            trs = Selector(text=ret.text).xpath('//div[@id="ctl00_ContentPlaceHolder1_Panel1"]/table/tr').extract()

            final_data_list = []
            for idx in range(1, len(trs)):
                tr = trs[idx]
                base_filename = Selector(text=tr).xpath('//td[1]/font/a/@href').extract()[0]
                file_name = str(base_filename).replace('..%2ferollpdf%2f', '').replace('%5c', '_')
                final_data = {
                    'file_name': file_name,
                    'pdf_url': 'http://ceopunjab.nic.in/English/' + base_filename,
                    'part_no': Selector(text=tr).xpath('//td[1]/font/a/text()').extract()[0],
                    'area_covered_in_part': Selector(text=str(Selector(text=tr).xpath('//td[2]/font').extract()).replace('<br>', '\n')).xpath('//font/text()').extract()[0],
                    'polling_station_building': Selector(text=str(Selector(text=tr).xpath('//td[3]/font').extract()).replace('<br>', '\n')).xpath('//font/text()').extract()[0]
                }
                final_data_list.append(final_data)

            print(final_data_list)
            return(final_data_list)
        else:
            print('failed to get constituency list')
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
        header_info.append('ero')
        header_info.append('mla')
        header_info.append('mp')
        header_info.append('total_voters')
        header_info.append('part_no')
        header_info.append('area_covered')
        header_info.append('polling_station_building')
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
        # write header into output csv file
        if CSV_FLAG == True: self.WriteHeader()

        # get district list
        print('getting districts ...')
        districts = self.GetDistrictList()

        for district in districts:
            district_url = district['district_url']
            district_name = district['name']

            # get constituency list
            print('getting constituencies for %s ...' % (district_name))
            constituencies = self.GetConstituencyList(district_url)

            for constituency in constituencies:
                constituency_id = constituency['id']
                constituency_url =  constituency['constrituency_url']

                # get intermediate data
                print('getting intermediate data for %s ...' % (constituency_id))
                intermediate_data = self.GetIntermediateHtml(constituency_url)
                district_name = intermediate_data['assembly_constituency_district']
                assembly_constituency = intermediate_data['assembly_constituency']
                ero = intermediate_data['ero']
                mla = intermediate_data['mla']
                mp = intermediate_data['mp']
                total_voters = intermediate_data['total_voters']

                # get final data
                print('getting final data for %s ...' % (constituency_id))
                final_data_list = self.GetFinalHtml(constituency_url)

                if final_data_list != None:
                    for final_data in final_data_list:
                        final_pdf_file_name = final_data['file_name']
                        final_pdf_url = final_data['pdf_url']
                        final_part_no = final_data['part_no']
                        final_area_covered_in_part = final_data['area_covered_in_part']
                        final_polling_station_building = final_data['polling_station_building']

                        if self.CheckPdfFile(final_pdf_file_name) == False:
                            # download and save pdf file
                            print('downloading %s for part no(%s) ...' % (final_pdf_file_name, final_part_no))
                            self.DownloadPdfFile(final_pdf_url, final_pdf_file_name)

                            # error url
                            writer = csv.writer(open(ERROR_URL_FILE, 'w'), delimiter=',', lineterminator='\n')
                            writer.writerow([final_pdf_file_name, final_pdf_url])

                        if CSV_FLAG == True:
                            # write data into output csv file
                            data =[]
                            data.append(district_name)
                            data.append(assembly_constituency)
                            data.append(ero)
                            data.append(mla.encode('ascii', 'ignore').decode('ascii'))
                            data.append(mp)
                            data.append(total_voters)
                            data.append(final_part_no)
                            data.append(final_area_covered_in_part)
                            data.append(final_polling_station_building)
                            data.append(final_pdf_file_name)
                            self.WriteData(data)

                    # rename html files
                    if not os.path.isfile(HTML_FOLDER + 'intermediate_' + assembly_constituency + '.html'):
                        os.rename(HTML_FOLDER + 'temp_intermediate.html', HTML_FOLDER + 'intermediate_' + assembly_constituency + '.html')
                    if not os.path.isfile(HTML_FOLDER + 'final_' + assembly_constituency + '.html'):
                        os.rename(HTML_FOLDER + 'temp_final.html', HTML_FOLDER + 'final_' + assembly_constituency + '.html')

            #         break
            #     break
            # break



#------------------------------------------------------- main -------------------------------------------------------

def main():
    # create scraper object
    scraper = PunjabScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()