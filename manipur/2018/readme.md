### Manipur

URL = http://www.ceomanipur.nic.in/ElectoralRolls.html

Year = Draft Electoral Roll for 2018

Total number of files = 4,400

Languages = English, Manipuri (see below)

Note from the website: 

  "Note: Manipuri Version is published for Assembly Constituencies 1 to 40 only. Remaining Assembly Constituency, that is, 41 to 60 are published only in English. For English version click here."

4 missing files on the website. See the CSV, relative_path for information about that. 

### Script

The [Script](manipur.py) along with utility functions file in [helpers/](helpers/) does two things:

1. It produces [manipur.csv](manipur.csv) that contains metadata about the pdfs. The CSV has the following fields: `ac_number, ac_name, poll_station_number, poll_station_name, language, relative_path_to_file`. 

2. Downloads all the pdfs to a directory called `manipur_pdfs/` (English files are downloaded to `manipur_pdfs/english/` and Manipuri files to `manipur_pdfs/manipuri/`)

#### Running the script

Create the directories specified on lines 10, 11, and 12 before running the script.

```
pip install -r requirements.txt
python manipur.py
```
