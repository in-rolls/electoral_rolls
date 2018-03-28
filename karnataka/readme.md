## Karnataka Electoral Rolls

We have 48,412 files for 2018, 46,552 files for 2017, 46,550 for 2016, and 46,551 for 2015. 

For files that we couldn't fetch (that end in a 404), the `filename` column in the respective CSV (links below) has a NULL. For 2017, we were able to fetch all the files. For 2015 and 2018, we couldn't fetch one file each. And for 2016, we couldn't fetch two files.

### Scripts

For each of the years 2015--2018, we wrote a python script (the scripts don't differ by much) that did two things:

1. Created a CSV file (encoded in UTF-8) with the following columns: `district_no, district_name, ac_no, ac_name, part_no, polling_station_name, filename`. The filename for files that 404 are missing. 

2. Downloaded all the PDFs to a local folder `karnataka_20XX`

Links to the scripts:

* [karnataka_2018.py](karnataka_2018.py) iterates through the 2018 final electoral rolls posted at http://ceokarnataka.kar.nic.in/FinalRoll-2018/Dist_List.aspx
* [karnataka_2017.py](karnataka_2017.py) iterates over the 2017 final electoral rolls posted at http://ceokarnataka.kar.nic.in/FinalRoll-2017/
* [karnataka_2016.py](karnataka_2016.py) iterates over the 2016 final electoral rolls posted at http://ceokarnataka.kar.nic.in/FinalRoll_2016/
* [karnataka_2015.py](karnataka_2015.py) iterates over the 2015 final electoral rolls posted at http://ceokarnataka.kar.nic.in/FinalRoll_2015/

Links to the CSVs:

* [karnataka_2018.csv](karnataka_2018.csv) 
* [karnataka_2017.csv](karnataka_2017.csv) 
* [karnataka_2016.csv](karnataka_2016.csv) 
* [karnataka_2015.csv](karnataka_2015.csv)

### Running the Scripts

```
pip install -r requirements.txt
python karnataka_2018.py
```
