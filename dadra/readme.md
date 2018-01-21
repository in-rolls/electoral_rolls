### Dadra and Nagar Haveli

The final pdfs are posted on Google Cloud Storage:
https://storage.googleapis.com/in-electoral-rolls/dadra_pdfs.tar.gz

Requester pays for the charges associated with downloading the data. For more information about about that, see: https://cloud.google.com/storage/docs/requester-pays

### Details

URL = http://ceodnh.nic.in/Electoral2017.aspx

Year = Final Electoral Roll for 2017

### Script

The [Script](dadra.py) does three things: 

1. Produces [dadra.csv](dadra.csv) that contains metadata about the pdfs. The CSV has the following fields: `language, main_or_supplementary, part_no, file_name`

2. Downloads all the pdfs to a directory called `dadra_pdfs/`

3. Renames files as follows:
   * English language rolls have the prefix `eng` and Gujarati language rolls have the prefix `guj`. 
   * The `main` rolls have the word `main` in them and supplementary `supp`
   * And the last segment is the 3 digit part_no. 
   
   So a sample name = eng_main_001.pdf

#### Running the script

```
pip install -r requirements.txt
python dadra.py
```

### Notes

|lang|type|file_name|
|----|----|--------:|
|eng |main|      266|
|eng |supp|      255|
|guj |main|      266|
|guj |supp|      252|

There are missing supplementary files getting error 404 (File or directory not found).

### Misc. info.:

Draft roll for 2018 is also available.
