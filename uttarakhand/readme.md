### Uttarakhand

URL = http://ceo.uk.gov.in/pages/view/27-uttarakhand-state-electoral-rolls-%28in-pdf-format%29

### Script

The [Script](uttarakhand.py) does two things:

1. It produces [uttarakhand.csv](uttarakhand.csv) that contains metadata about the pdfs. The CSV has the following fields: `ac_no, ac_name, filename`

2. Downloads all the pdfs to a directory called `uttarakhand_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python uttarakhand.py
```

### Missing file

There is one missing PDF file (HTTP error 404) for AC No 24 - Rishikesh

## Notes

Historical Rolls from as far back as 2007 available.


