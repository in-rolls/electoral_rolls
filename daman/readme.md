### Daman and Diu


### Details

URL = http://ceodaman.nic.in/Final-Photo-Electoral-Roll-2017/MainPage.htm

Year = Final Photo Roll for 2017

### Script

The [Script](daman.py) does 3 things:

1. Produces [daman.csv](daman.csv) that contains metadata about the pdfs. The CSV has the following fields: `language, poll_station_no, file_name`

2. Downloads all the pdfs to a directory called `daman_pdfs/`

3. Renames the pdfs:
  * English language rolls have the prefix `eng` and Gujarati language rolls have the prefix `guj`.
  * The polling station no. is a 3 digit number.

  So a sample name = eng_001.pdf

#### Running the script

```
pip install -r requirements.txt
python daman.py
```

### Misc. info.

Draft roll for 2018 is also available. So are electoral rolls for 2015 and 2016.
