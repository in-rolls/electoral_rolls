### Daman and Diu Archives

URLs:

  - [2015](http://ceodaman.nic.in/Final%20%20PHOTO%20ELECTORAL%20ROLL-%202015/MainPage.htm)
  - [2016](http://ceodaman.nic.in/Final-Photo-Electoral-Roll-2016/MainPage.htm)

### Script

The [Script](daman_archives.py) does 3 things: 

1. Produces [daman_2015.csv](daman_2015.csv) and [daman_2016.csv](daman_2016.csv) that contains metadata about the pdfs. The CSV has the following fields: `year, language, poll_station_no, file_name`

2. Downloads all the pdfs to a directory called `daman_201x/`

3. Renames the pdfs:  
  * English language rolls have the prefix `eng` and Gujarati language rolls have the prefix `guj`.
  * The polling station no. is a 3 digit number. 
  
  So a sample name = eng_001.pdf

#### Running the script

```
pip install -r requirements.txt
python daman_archives.py
```

### Misc. info.

There is no electoral rolls in Gujarati for 2016.
