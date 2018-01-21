### Odisha


### Details

URL = http://ceoorissa.nic.in/ViewEroll.asp

### Script

The [Script](odisha.py) does 3 things:

1. Produces [odisha.csv](odisha.csv) with metadata about the pdfs. The CSV has the following fields: `district_number, district_name, ac_name, ac_number, part_name, part_number, type_of_roll (service voter or eroll), filename`

2. Renames the pdfs as follows:
  * type of roll (eroll or service)
  * distict_number (2 digit)
  * ac_number (3 digits)
  * part_number (3 digits).

  so a sample pdf will be named: eroll_01_001_001.pdf

3. Downloads all the pdfs to a directory called `odisha_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python odisha.py
```
