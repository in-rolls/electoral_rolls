## Punjab


### Details

URL = http://ceopunjab.nic.in/English/fper.aspx

Total Number of Files = 22,883

### Script

The [Script](punjab.py) does three things:

1. Produces [punjab.csv](punjab.csv) that contains metadata about the pdfs. The CSV has the following fields: `district_name, assembly_constituency, ero (intermediate HTML table), mla (intermediate HTML table), mp (intermediate HTML table), total_voters (intermediate HTML table), part_no (from the final HTML table), area_covered (again final HTML table), polling_station_building (final HTML table), filename`

2. Downloads intermediate [HTML files](punjab_htmls.7z)

3. Downloads all the pdfs to a directory called `punjab_pdfs/`

#### Running the script

```
pip install -r requirements.txt
python punjab.py
```
