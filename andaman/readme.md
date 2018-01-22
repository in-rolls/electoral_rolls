### Andaman and Nicobar Islands

### Details

URL = http://as1.and.nic.in/newelection/ElectoralRoll.php

Year = Draft Roll for 2017

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python andaman.py` to downloads all the pdfs to directory `../data/Andaman/`
    and creates 'Gujarat.txt' for files that were not downloaded successfully
5. `python andaman_retry.py` for retrying downloads for files in 'Andaman.txt'
6. `python andaman_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  401
2. The downloaded files are of form PART_{Part Number}.pdf

