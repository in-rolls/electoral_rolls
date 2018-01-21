## Puducherry


### Details

URL = https://ceopuducherry.py.gov.in/rolls/rolls.html

Year = 2018

Total number of files = 913

Languages = Tamil, English

#### Script

The [Script](puducherry.py) does two things:

1. Produces [puducherry.csv](puducherry.csv) that contains metadata about the pdfs. The CSV has the following fields: `constituency_name, part_no, poll_station_name, area_covered, file_names_en, file_names_ta`

2. Downloads all the pdfs to a directory called `puducherry_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python puducherry.py
```
