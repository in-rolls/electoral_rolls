### Nagaland


### Details

URL = http://ceonagaland.nic.in/SearchERollPDF.aspx

Year = Draft Electoral Roll for 2018

Total number of files = 2,273

### Script

The [Script](nagaland.py) does two things:

1. It produces `nagaland.csv` that contains metadata about the pdfs. The CSV has the following fields: `district_name, ac, polling_station, filename` The final metadata file is [here](nagaland.csv).

2. Downloads all the pdfs to a directory called `nagaland_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python nagaland.py
```
