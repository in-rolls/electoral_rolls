### Mizoram


### Details

URL = http://ceomizoram.nic.in/ElectoralRollPDF.html

Year = Draft Electoral Roll of 2018

### Script

The [Script](mizoram.py) does two things:

1. It produces [mizoram.csv](mizoram.csv) that contains metadata about the pdfs. The CSV has the following fields: `district (mamit, kolasib, etc.), leg_assembly (hachkek, dampa, etc.), polling_station_name (kahnmun, thinghlun, etc.), file_name`

2. Downloads all the pdfs to a directory called `mizoram_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python mizoram.py
```

