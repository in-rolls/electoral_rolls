### Maharashtra


### Details

URL = https://103.23.150.75/Search/SearchPDF.aspx

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python maharashtra.py` to downloads all the pdfs to directory `../data/Maharashtra/`
    and creates 'maharashtra.txt' for files that were not downloaded successfully
5. `python maharashtra_retry.py` for retrying downloads for files in 'maharashtra.txt'
6. `python maharashtra_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  91450
2. The downloaded files are of form A{District number}_A{District number}{assembly constituency number}.pdf
3. Files not available can be found in 'maharashtra3.txt''

