## Jammu and Kashmir

The python script `jammu_kashmir.py` gets all the `PS Wise Reports` PDFs in English, Hindi, and Urdu from http://ceojk.nic.in/ElectionPDF/Main.aspx and creates a CSV `jammu_kasmir.csv` with the following fields: `language, district_number, district_name, ac_number, ac_name, ps_number, ps_name, filename`

* [CSV File](jammu_kashmir.csv)

### Running the script

```
pip install -r requirements.txt
python jammu_kashmir.py
```

### Script for Fetching English Rolls (Previous Version)

Website for J & K Electoral Rolls has changed over time.  [jk_eng/](jk_eng/) was used to fetch the English electoral rolls (available for 2 districts) from a previous iteration of the site.



