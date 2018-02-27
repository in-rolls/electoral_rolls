### Uttar Pradesh


### Details

URL = http://164.100.180.82/ceouptemp/RollPDF.aspx

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python up.py` to downloads all the pdfs to directory `../data/UP/` and creates
    'up.txt' for files that were not downloaded successfully
5. `python up_retry.py` for retrying downloads for files in 'up.txt'
6. `python up_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  151,843
2. The downloaded files are of form AC{assembly constituency number}_S24A{assembly constituency number}P{polling station number}.pdf
3. Files not available online can be found in ``up4.txt``