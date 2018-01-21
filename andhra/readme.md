### Andhra Pradesh

URL = http://ceoandhra.nic.in/home.aspx

There are 41,635 Telugu, and 41,834 English language electoral rolls. 439 English language electoral rolls and 637 Telugu rolls were unavailable. 

The python script [andhra.py](andhra.py) and a script with helper functions in [helpers](helpers/) iterates through the data on the webpage HTML table and does two things:

1. Creates a CSV [andhra.csv](andhra.csv) that tracks the metadata about the pdf files. It has the following columns `district_name (e.g.. 1-Srikakulum), ac_name (e.g., 1-Ichchapuram), polling_station_number (from the HTML table), polling_station_name (HTML table), polling_station_location (HTML table), telugu_file_name, eng_file_name`

2. Stores the pdf files in the folder `andhra_pdfs` with English files under the folder `english/` and Telugu files under the folder `telugu/`.

#### Running the script

```
pip install -r requirements.txt
python andhra.py
```
