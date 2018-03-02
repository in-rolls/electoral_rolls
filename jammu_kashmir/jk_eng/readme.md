### Jammu and Kashmir


### Details

URL = http://ceojk.nic.in/ElectionPDF/Main.aspx

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python jammu.py` to downloads all the pdfs to directory `../data/JK/`
    and creates 'jammu.txt' for files that were not downloaded successfully
5. `python jammu_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  542
2. The downloaded files are of form EACA{assembly constituency number}PS{polling station number}.pdf
3. Files not available:
    EACA049PS0004.pdf
    EACA049PS0086.pdf
    EACA049PS0118.pdf

