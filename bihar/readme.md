### Bihar


### Details

URL = http://210.212.18.115:8880/

Year = Draft Roll for 2017

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python bihar.py` to downloads all the pdfs to directory `../data/Bihar/`
5. `python bihar_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  61837
2. The downloaded files are of form FinalRoll_ACNo_{assembly constituency number}PartNo_{part number}.pdf
3. Files not available can be found in 'bihar3.txt''

