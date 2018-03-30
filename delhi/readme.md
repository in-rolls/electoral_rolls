### Delhi

### Details

URL = http://ceodelhi.gov.in/Content/AccemblyConstituenty.aspx

Year = Draft Roll for 2018

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python delhi_brute_force.py` to downloads all the pdfs to directory `../data/Delhi/`
    and creates 'delhi.txt' for files that were not downloaded successfully
5. `python delhi_retry.py` for retrying downloads for files in 'delhi.txt'
6. `python delhi_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  13402
2. The downloaded files are of form AC{{assembly constituency number}}_AC{assembly constituency number}{Part Number}.pdf
3. There are some files missing from Hindi/English version of the download, please see ``diff.txt`` for details
