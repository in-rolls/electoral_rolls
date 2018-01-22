### Meghalaya


### Details

URL = http://ceomeghalaya.nic.in/erolls/erolldetails.html

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python meghalaya.py` to downloads all the pdfs to directory `../data/Meghalaya/`
    and creates 'Meghalaya.txt' for files that were not downloaded successfully
5. `python meghalaya_retry.py` for retrying downloads for files in 'Meghalaya.txt'
6. `python meghalaya_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  3038
2. The downloaded files are of form A{District number}_A{District number}{assembly constituency number}.pdf
3. Files not available can be found in 'Meghalaya3.txt''

