### Uttarakhand Archives

URL = http://ceo.uk.gov.in/pages/view/27-uttarakhand-state-electoral-rolls-%28in-pdf-format%29

  - [2007](http://election.uk.gov.in/pdf_roll/01012007/Uttranchal_pdf_page.htm)
  - [2008](http://election.uk.gov.in/pdf_roll/01012008/Uttranchal_pdf_page.htm)
  - [2009](http://election.uk.gov.in/pdf_roll/24042009/Uttranchal_pdf_page.htm)
  - [2010](http://election.uk.gov.in/pdf_roll/01012010_N/Uttranchal_pdf_page.htm)
  - [2011](http://ceo.uk.gov.in/pages/view/27/34-a.c.-segment-wise-final-electoral-roll..as-on-01-01-2011..(new)-)
  - [2012](http://election.uk.gov.in/pdf_roll/02012012/Uttranchal_pdf_page.htm)
  - [2013](http://election.uk.gov.in/pdf_roll/01012013S/Uttranchal_pdf_page.htm)
  - [2014](http://election.uk.gov.in/pdf_roll/30042014/Uttranchal_pdf_page.htm)
  - [2015](http://election.uk.gov.in/pdf_roll/01012015F/Uttranchal_pdf_page.htm)
  - [2016](http://election.uk.gov.in/pdf_roll/01102016S/Uttranchal_pdf_page.htm)

### Script

The [Script](uttarakhand_archives.py) does two things:

1. It produces [uttarakhand_20xx.csv](uttarakhand_20xx.csv) that contains metadata about the pdfs. The CSV has the following fields: `year, ac_no, ac_name, filename`

2. Downloads all the pdfs to a directory called `uttarakhand_20xx/`

#### Running the script

```
pip install -r requirements.txt
python uttarakhand_archives.py
```
