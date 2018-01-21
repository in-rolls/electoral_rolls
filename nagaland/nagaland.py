import requests
import csv
import os
import sys
from bs4 import BeautifulSoup
from time import sleep

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36',
}

DISTRICT = {
    '01': 'DIMAPUR',
    '12': 'KIPHIRE',
    '03': 'KOHIMA',
    '10': 'LONGLENG',
    '06': 'MOKOKCHUNG',
    '09': 'MON',
    '02': 'PEREN',
    '05': 'PHEK',
    '04': 'PUGHOBOTO',
    '11': 'TUENSANG',
    '08': 'WOKHA',
    '07': 'ZUNHEBOTO',
}

fieldname_list = (
    'district_name',
    'polling_station',
    'ac',
    'filename'
)

CSV_FILE = 'nagaland.csv'
BASE_URL = 'http://ceonagaland.nic.in/'
POST_URL = 'http://ceonagaland.nic.in/SearchERollPDF.aspx'
FOLDER = 'nagaland_pdfs'


headers = {
    'Pragma':'no-cache',
    'Origin':'http://ceonagaland.nic.in',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en;q=0.9',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.89 Chrome/62.0.3202.89 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept':'*/*',
    'Cache-Control':'no-cache',
    'X-Requested-With':'XMLHttpRequest',
    'Cookie':'ASP.NET_SessionId=gal2azi4tyyfv0x045e2ko11',
    'Connection':'keep-alive',
    'X-MicrosoftAjax':'Delta=true',
    'Referer':'http://ceonagaland.nic.in/SearchERollPDF.aspx',
}

REPLACE_FIELD_LIST = (
    '__EVENTTARGET',
    '__EVENTVALIDATION',
    '__VIEWSTATE',
    '__VIEWSTATEGENERATOR',
)
# data verification depends on cookie and eventtarget & eventvalidation & viewstate
BASIS_DATA = {
    '__ASYNCPOST': 'true',
    '__EVENTTARGET': 'ctl00$CPHBody$DropDownListDistrict',
    '__EVENTVALIDATION': '8CREIOJJB4kjtSefmyrNMxDnp4sNoKAOsxovdWlJB5sQbrMNxjVp2u7o8n0VtbJVTXPJD24vZKxGErAWmE7M09RgE31aOx8AiBy+XIdOX4h9lv4RlIxHwn6+dMG99LJTmgD8vxK6PnXjM2n4Cxo/kbRnJF/BeczJONbP1JbsAWiMROLWTnLtU8wuSnAqp1M1ybP3oSOVhcHmZpLjY904URuvg8cVPszVd6CZjEiP5n5Si/qV4pw9WeghWqda9ZSxaUULXiC/S+0smIGYeFpNZH5W1eDnnbxEEJZDjWen+h+BicwnyqWOQj/lWfFtFpbJwQWhlO8RWqJaPDEni3HQKnXG/r9kmko/XXCZ3Y1BMPkRNgWPAMMhEhadu62vC+W58h5M5t0F2VJH99CN2JNxVS7oD8rnbVcBM6b/Gmkn9Ag1OHEwie+1W7Ei9ZrOFJNE33mFasFtrV9EjZVVAx5gLWhdx9NJusHeL2dtdzBCNy/x7kWDQqE2lTtvUQ3Ki69RJu+nRsWu0NlJVzxs',
    '__VIEWSTATE': 'w4dnszFKA59X4mXDlUdC1AbIcQMo3FDsy1xHjU6svY/yx2I9hRhFTz5tiagvBL02AiE04p2PIdM4lJJTULV87JmTgAW46PS1/arBNbXJXkx2lZz72Q+Fd2sM5zAlAMoam+0wTkJiavJyn1i4LHQrluWwVwEoWuSfr01aFuA/pS52qLu+mfS0YsjdfQ0cazSr9upeumv7sieASM+or/9n/w3+lhcU5pQjR+YXptpjM/R3P9lZUhExl7cITvKU1z/hu1xL2YXwKQr+KQccHqXr/w/hELsojpkCj0ZdZlA95+wCcgJwgvZHkaOLe29a2MEN9EJxn3rrGQHG7iKlXVYAqNPpGYJvPe6mrZ4Qj6CpHXoq0yTwr/KvxuIFTtBRFkTHxzWfJDyKIa39pDa//M+HvWdifk3Qj4t2rSw2iOWb6Eq18ddWbLVZIXDjwIXc8JfWGVsOxlqy643a81+1mYuCJ3zDiFTM7TzX9Q++ey7YF/gyfGnt0G59ZyqIol3YeE2QM90fz6QhfRarniMLv0U3EXZGcrirQX8mHxH+SHZA7Vd7U00vijzjw1xfrH+xrKP6CgleMB5RcD6k4iipqE0FlA0lO01jHzRZ4LcBeipbqhq57XPHIFUzATogMZdG243AXQlyJx+5ZxiNGO5lrrRMTIuzg0Nt0ZtQxgfwKKIWttaBiYQi7PcEroNdf6FykcdwF2MrawwmUlBSWTTl',
    '__VIEWSTATEGENERATOR': '803F11C8',
    'ctl00$CPHBody$DropDownListAC': 'Select AC...',
    'ctl00$CPHBody$DropDownListDistrict': '01',
    'ctl00$CPHBody$sm1': 'ctl00$CPHBody$sm1|ctl00$CPHBody$DropDownListDistrict'
}

TIMEOUT = 10

def request(method, url, **kwargs):
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    if 'headers' not in kwargs:
        kwargs['headers'] = HEADERS

    while True:
        try:
            return getattr(requests, method)(url, **kwargs)
        except (
                requests.exceptions.SSLError,
                requests.exceptions.RequestException
            ) as e:
            sleep(TIMEOUT)

def post(url, **kwargs):
    return request('post', url, **kwargs)

def get(url, **kwargs):
    return request('get', url, **kwargs)

def get_data(data):
    return post(
        POST_URL,
        data=data,
        headers=headers
    )

def download_file(url, path):
    JOURNAL_FILE = '{}.jor'.format(path)

    if os.path.exists(path) and not os.path.exists(JOURNAL_FILE):
        return

    jf = open(JOURNAL_FILE, 'w')
    jf.close()

    try:
        f = open(path, 'wb')
        r = get(url, stream=True, timeout=TIMEOUT, headers=HEADERS)

        for block in r.iter_content(1024):
            f.write(block)

        os.remove(JOURNAL_FILE)
    except (
            requests.exceptions.SSLError,
            requests.exceptions.RequestException
        ) as e:
        sleep(TIMEOUT)
    finally:
        f.close()

def get_district_data(district_id):
    data = BASIS_DATA.copy()

    data['ctl00$CPHBody$DropDownListDistrict'] = district_id
    r = get_data(data)

    data_list = [x.strip() for x in r.text.split('\n')]
    select_index = data_list.index('</select>')
    select_data = data_list[:select_index+1]

    select_data_list = ''.join(select_data).split('|')
    select_idx = select_data_list.index('CPHBody_UPAC')

    bs_select = BeautifulSoup(select_data_list[select_idx+1], 'html.parser')

    ac_list = []

    for i, option in enumerate(bs_select.find_all('option')):
        if i == 0:
            continue

        ac_list.append((
            option.get('value'),
            option.text
        ))

    api_data_list = ''.join(data_list[select_index+1:]).split('|')

    district_data = []

    for ac_id, ac_name in ac_list:
        data_second = BASIS_DATA.copy()

        data_second['ctl00$CPHBody$DropDownListDistrict'] = district_id
        data_second['ctl00$CPHBody$DropDownListAC'] = ac_id

        for field in REPLACE_FIELD_LIST:
            field_idx = api_data_list.index(field)

            if field_idx > 0:
                data_second[field] = api_data_list[field_idx+1]

        district_data.extend(list(get_ac(data_second, ac_name)))

    return district_data


def get_ac(data, ac_name):
    r2 = get_data(data)

    data_two_list = [x.strip() for x in r2.text.split("|")]
    # print(data_two_list)
    data_idx = data_two_list.index('CPHBody_UPResults')

    html_data = data_two_list[data_idx+1]
    bs = BeautifulSoup(html_data, 'html.parser')

    tr_list = bs.find_all('tr')

    for tr in tr_list:
        a = tr.find('a')
        yield {
            'pdf_uri': a.get('href'),
            'number': a.text,
            'name': ac_name,
        }

def main():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    f = open(CSV_FILE, 'w', encoding='utf-8')   
    csv_writer = csv.writer(f)
    csv_writer.writerow(fieldname_list)

    item_count = len(DISTRICT.items())

    for i, d in enumerate(DISTRICT.items()):
        district_id, district_name = d
        # print(district_name)
        data_list = get_district_data(district_id)

        for x, data in enumerate(data_list):
            print('{}/{}/{}\r'.format(i, x, item_count), end='')
            sys.stdout.flush()

            pdf_uri = data['pdf_uri']
            pdf_name = pdf_uri.split('/')[-1]
            pdf_url = '{}{}'.format(BASE_URL, pdf_uri)
            poll_station = data['number']
            ac = data['name']
            path = '{}/{}'.format(FOLDER, pdf_name)

            download_file(pdf_url, path)

            csv_writer.writerow((district_name, poll_station, ac, pdf_name))

if __name__ == '__main__':
    main()
