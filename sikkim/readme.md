### Sikkim

URL = http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/Polling%20Station%20wise%20final%20Electoral%20Roll%20published%20on%2010th%20January%202018.html

Year = 2018

Total number of files = 600

### Script

The [Script](sikkim.py) iterates through the HTML Table and does two things:

1. Writes a [sikkim.csv](sikkim.csv) that tracks metadata about the pdf. The pdf has the following columns: `ac_number, ac_name, part_number, polling_station_name, relative_path_to_file`

2. Downloads all the pdfs to sikkim_pdfs/

#### Running the script

```
pip install -r requirements.txt
python sikkim.py
```

### Missing PDF files

There are missing PDF files (return HTTP 404)

- [29_017.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/DRAFT%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/29/AC029PART017-SUP0.pdf)
- [30_009.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/FINAL%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/30/09.pdf)
- [30_011.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/FINAL%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/30/11.pdf)
- [30_013.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/FINAL%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/30/13.pdf)
- [30_018.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/FINAL%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/30/18.pdf)
- [32_001.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/FINAL%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/32/01.pdf) to [32_032.pdf](http://ceosikkim.nic.in/PS_Wise_ele_roll%20w.r.t.2013/PS%20AFTER%20RATIONALISATION/FINAL%20ELECTORAL%20ROLL%20W.R.T.1.1.2017/32/32.pdf)
