## Telangana


### Details

URL = http://ceoaperms.ap.gov.in/TS_Rolls/Rolls.aspx

Year = 2017

Total number of files = 62,370. Of it, 69 files posted to the website are corrupted. The list of corrupted files is [here](telangana_corrupted.csv).

### Script

The [Script](telangana.py) does two things:

1. It produces [telangana.csv](telangana.csv) that contains metadata about the pdfs. The CSV has the following fields: `district, constituency, poll_station_no, poll_station_name, poll_station_location, language, file_name`

2. Downloads all the pdfs to a directory called `telengana_pdfs/`

3. Renames the pdfs as follows:
  * lowercase, snake_case
  * prefix is tel' if language isTelugu' and eng if language is English.
  * 2 digit district number (01 to 31)
  * 2 digit assembly constituency(01, 02, 03, ...)
  * 3 digit polling station number (001, 002, ...)

  sample final pdf name = eng_01_01_001.pdf

#### Running the script

```
pip install -r requirements.txt
python telangana.py
```



