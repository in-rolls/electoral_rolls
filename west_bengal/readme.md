## West Bengal

URL = http://wbceo.in/DistrictList.aspx

The python script [west_bengal.py](west_bengal.py) iterates over all the districts, all the Assembly Constituencies (ACs) within each district, and all the polling stations within each AC, and does two things:

1) downloads all the pdfs in `wb_pdfs/`: the draft_rolls are saved to `wb_pdfs/draft_rolls/` and the supplementary rolls are saved to `wb_pdfs/supplements/`. (We don't download the maps.) 

2) creates [west_bengal.csv](west_bengal.csv) with the following fields
`district_name, ac_no, ac_name, part_no, polling_station_name, filename` (each polling station has 2 rows: 1 for draft roll, 1 for supplementary roll)

### Running the Script

```
pip install -r requirements.txt
python west_bengal.py
```

### Data

There are a total of 154,694 rows (77,347 draft rolls and equal number of supplements) in the CSV. Of this list, we were able to 153,962 files. The files in [invalid_pdfs.csv](invalid_pdfs.csv) could not be fetched.
