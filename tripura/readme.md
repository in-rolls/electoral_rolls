### Tripura

URL = http://ceotripura.nic.in/Draft_2018.asp

Year = Draft Electoral Roll for 2018

Total number of files = 3,170

### Script

The [Script](tripura.py) along with a utility function file in [helpers/)(helpers/) does two things:

1. It produces [tripura.csv](tripura.csv) that contains metadata about the pdfs. The CSV has the following fields: `district_name, ac_name, ac_number, poll_station_number, filename`

2. Downloads all the pdfs to a directory called `tripura_pdfs/`

#### Running the script

Create tripura_pdfs and tripura directories specified on lines 6 and 7 of `tripura.py`

```
pip install -r requirements.txt
python tripura.py
```

