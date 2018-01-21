### Kerala Archive Data


### Details

URL = http://www.ceo.kerala.gov.in/erollArchives.html

### Script

The [Script](kerala_archives.py) does 3 things:

1. Produces metadata files that contain metadata about the pdfs. The CSV has the following fields: `year, leg_assembly, booth_no, eng_file_name`
  - [2011](kerala_2011.csv)
  - [2012](kerala_2012.csv)
  - [2013](kerala_2013.csv)
  - [2014](kerala_2014.csv)
  - [2015](kerala_2015.csv)
  - [2016](kerala_2016.csv)

2. Renames the pdfs as follows:
  * lowercase, snake_case
  * year (4 digit), constituency_number (3 digit code), and polling_station_number (3 digit code)

  so sample file name = 2011_001_001.pdf

3. Downloads all the pdfs to a directory called `kerala_pdfs/kerala_20XX/`

#### Running the script

```
pip install -r requirements.txt
python kerala_archives.py
```

### Corrupted PDF files

#### 2011

* [2011_078_098.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2011/AC078/078098.pdf)

#### 2012

None

#### 2013

None

#### 2014

None

#### 2015

* [2015_078_005.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2015/AC078/078005.pdf)
* [2015_093_110.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2015/AC093/093110.pdf)

#### 2016

* [2016_114_057.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114057.pdf)
* [2016_114_054.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114054.pdf)
* [2016_100_067.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100067.pdf)
* [2016_114_053.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114053.pdf)
* [2016_096_095.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC096/096095.pdf)
* [2016_100_061.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100061.pdf)
* [2016_096_096.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC096/096096.pdf)
* [2016_100_064.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100064.pdf)
* [2016_114_050.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114050.pdf)
* [2016_114_055.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114055.pdf)
* [2016_114_049.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114049.pdf)
* [2016_100_062.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100062.pdf)
* [2016_114_052.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114052.pdf)
* [2016_090_181.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC090/090181.pdf)
* [2016_096_093.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC096/096093.pdf)
* [2016_114_048.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114048.pdf)
* [2016_096_091.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC096/096091.pdf)
* [2016_100_068.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100068.pdf)
* [2016_114_051.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114051.pdf)
* [2016_100_063.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100063.pdf)
* [2016_100_065.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100065.pdf)
* [2016_114_056.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC114/114056.pdf)
* [2016_096_092.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC096/096092.pdf)
* [2016_100_066.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC100/100066.pdf)
* [2016_096_094.pdf](http://www.ceo.kerala.gov.in/pdf/voterslist_2016/AC096/096094.pdf)
