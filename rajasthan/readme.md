### Rajasthan


### Details

URL = http://164.100.153.10/electoralroll/Draftroll_2018.aspx

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python rajasthan.py` to downloads all the pdfs to directory `../data/Rajasthan/`
    and creates 'rajasthan.txt' for files that were not downloaded successfully
5. `python rajasthan_retry.py` for retrying downloads for files in 'rajasthan.txt'
6. `python rajasthan_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  50027
2. The downloaded files are of form A{assembly constituency number}_A{assembly constituency number}{Part Number}.pdf
3. Files not available are in rajasthan2.txt and rajasthan3.txt
