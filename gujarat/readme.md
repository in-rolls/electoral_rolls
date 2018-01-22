### Gujarat


### Details

URL = http://erms.gujarat.gov.in/ceo-gujarat/master/frmEPDFRoll.aspx

Year = Draft Roll for 2017

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python gujarat.py` to downloads all the pdfs to directory `../data/Gujarat/`
    and creates 'Gujarat.txt' for files that were not downloaded successfully
5. `python gujarat_retry.py` for retrying downloads for files in 'Gujarat.txt'
6. `python gujarat_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  43142
2. The downloaded files are of form NORMAL_AC{assembly constituency number}N{assembly constituency number}{Part Number}.pdf
3. Files not available can be found in 'Gujarat3.txt''

