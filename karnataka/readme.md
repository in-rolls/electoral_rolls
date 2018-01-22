### Karnataka


### Details

URL = http://ceokarnataka.kar.nic.in/DraftRolls_2017/

Year = Draft Roll for 2017

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python karnataka.py` to downloads all the pdfs to directory `../data/Karnataka/`
    and creates 'karnataka.txt' for files that were not downloaded successfully
5. `python karnataka_retry.py` for retrying downloads for files in 'karnataka.txt'
6. `python karnataka_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  9012
2. The downloaded files are of form AC{assembly constituency number}_AC{assembly constituency number}{part number}.pdf


