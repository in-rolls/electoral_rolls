## Karnataka Electoral Rolls

The python script [karnataka_2018.py](karnataka_2018.py) iterates through the 2018 final electoral rolls posted at http://ceokarnataka.kar.nic.in/FinalRoll-2018/Dist_List.aspx and does two things:

1. It produces [karnataka.csv](karnataka_2018.csv) (encoded in UTF-8) with the following columns: `district_no, district_name, ac_no, ac_name, part_no, polling_station_name, filename` 

2. Downloads all the pdfs to a local folder called `karnataka_2018/`

### Running the Script

```
pip install -r requirements_2018.txt
python karnataka_2018.py
```

### 2017

The python script [karnataka_2017.py](karnataka_2017.py) iterates over the 2017 draft electoral rolls posted at http://ceokarnataka.kar.nic.in/DraftRolls_2017/ and does two things:

1. It produces [karnataka_2017.csv](karnataka_2017.csv) (encoded in UTF-8) with the following columns: `district_no, district_name, ac_no, ac_name, part_no, polling_station_name, filename` 

2. Downloads all the pdfs to a local folder called `karnataka_2017/`

```
pip install -r requirements_2017.txt
python karnataka_2017.py
```

### Data

We have X,XXX files for 2018 and Y,YYY files for 2017.
