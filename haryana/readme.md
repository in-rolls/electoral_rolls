## Haryana


### Details

URL = http://ceoharyana.nic.in/?module=draftroll

Year = 2018

Total number of files = 17,018

### Script

The [Script](haryana.py) does 2 things:

1. Produces [haryana.csv](haryana.csv) that contains metadata about the pdfs. The CSV has the following fields: `district_name, assembly_constituency, polling_station_name, filename`

2. Downloads all the pdfs to a directory called `haryana_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python haryana.py
```
