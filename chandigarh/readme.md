### Chandigarh


### Details

URL = http://ceochandigarh.nic.in/webpages/Polling2.aspx

Year = Draft Roll for 2018

### Script

The [Script](chandigarh.py) does two things:

1. Produces [chandigarh.csv](chandigarh.csv) that contains metadata about the pdfs. The CSV has the following fields: `booth_no, forms_received, location, area_covered, booth_level_officer, pdf_file_name`

2. Downloads all the pdfs to a directory called `chandigarh_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python chandigarh.py
```
