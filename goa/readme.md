### Goa


### Details

URL = http://ceogoa.nic.in/appln/uil/ElectoralRoll.aspx

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python goa.py` to downloads all the pdfs to directory `../data/Goa/`
    and creates 'goa.txt' for files that were not downloaded successfully
5. `python goa_retry.py` for retrying downloads for files in 'goa.txt'
6. `python goa_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  1604
2. The downloaded files are of form AC{assembly constituency number}_Part{part number}.pdf


