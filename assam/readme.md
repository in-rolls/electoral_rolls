### Assam

### Details

URL = http://ceoassam.nic.in/electoralroll.html

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python assam.py` to downloads all the pdfs to directory `../data/Assam/`
    and creates 'assam.txt' for files that were not downloaded successfully
5. `python assam_retry.py` for retrying downloads for files in 'assam.txt'
6. `python assam_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  19014
2. The downloaded files are of form {District number}_{assembly constituency number}NPER{assembly constituency number}PART{part number}.pdf
3. Files not available can be found in 'assam2.txt''

