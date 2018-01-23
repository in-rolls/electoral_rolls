### Himachal Pradesh

URL = http://electionhp.gov.in/pscd/

Total number of files = 7,840

### Script

The [Script](himachal.py) that iterates through all the 3 dropdowns and does 2 things:

1. Produces [himachal.csv](himachal.csv) that tracks the metadata of the pdf. The CSV has the following fields `district, assembly_segment, polling_station_number, polling_station_name`

2. Downloads all the pdfs to `himachal_pdfs`

#### Running the script

```
pip install -r requirements.txt
python himachal.py
```

