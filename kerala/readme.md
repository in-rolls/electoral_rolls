## Kerala


### Details

URL = http://www.ceo.kerala.gov.in/electoralrolls.html

Year = Draft Roll for 2018

### Script

The [Script](kerala.py) does 3 things:

1. Produces [kerala.csv](kerala.csv) that contains metadata about the pdfs. The CSV has the following fields: `district, leg_assembly, booth_no, polling_station_name, language, file_name`

2. Downloads all the pdfs to a directory called `kerala_pdfs/`

3. Renames the pdfs as follows:
  * lowercase, snake_case
  * english language rolls have the prefix `eng` and Malayalam language rolls have the prefix `mal`.
  * Second segment is 2 digit district code (01, 02, 03,...)
  * Third segment is 3 digit legislative assembly code (001, 002, 003, ...)
  * Fourth segment is a 3 digit polling_booth_code (001, 002, 003, ...)

  So a sample name = eng_01_001_001.pdf

#### Running the script

```
pip install -r requirements.txt
python kerala.py
```

### Misc. info.:

Archives available from 2011. Script for scraping the archives [here](../kerala_archives/).

