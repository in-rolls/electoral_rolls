### Tamil Nadu


### Details

URL = http://13.71.116.95/pdfformat/

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python tn.py` to downloads all the pdfs to directory `../data/TN/`
    and creates 'tn.txt' for files that were not downloaded successfully
5. `python tn_retry.py` for retrying downloads for files in 'tn.txt'
6. `python tn_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  59698
2. The downloaded files are of form dt_{district Number}_A{assembly constituency number}_A{assembly constituency number}{Part Number}.pdf
3. Files not available can be found in 'tn3.txt''

