### Lakshadweep

URL = http://ceolakshadweep.gov.in/electoralrolls.html

Year = Final Electoral Roll for 2017

Total Number of Files = 48

### Script

The [Script](lakshadweep.py) does two things: 

1. Produces [lakshadweep.csv](lakshadweep.csv)  that contains metadata about the pdfs. The CSV has the following fields: `booth_no, polling_station_name, file_name`

2. Downloads all the pdfs to a directory called `lakshadweep_pdfs/`

#### Running the script

```
pip install virtualenv

virtualenv env -p python3.6

env\Scripts\activate

pip install -r requirements.txt
python lakshadweep.py
```
