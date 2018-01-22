### Jharkhand


### Details

URL = http://164.100.150.3/mrollpdf1/aceng.aspx

Year = Draft Roll for 2017

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python jharkhand.py` to downloads all the pdfs to directory `../data/jharkhand/`
    and creates 'jharkhand.txt' for files that were not downloaded successfully
5. `python jharkhand_retry.py` for retrying downloads for files in 'jharkhand.txt'
6. `python jharkhand_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  28710
2. The downloaded files are of form MR{assembly constituency number}_MR{assembly constituency number}{part number}.pdf
3. Files not reachable:
    http://164.100.150.3/mrollpdf1/ceopdf/MR002/MR0020305.PDF
    http://164.100.150.3/mrollpdf1/ceopdf/MR002/MR0020319.PDF
    http://164.100.150.3/mrollpdf1/ceopdf/MR002/MR0020321.PDF
    http://164.100.150.3/mrollpdf1/ceopdf/MR002/MR0020334.PDF
    http://164.100.150.3/mrollpdf1/ceopdf/MR002/MR0020344.PDF
    http://164.100.150.3/mrollpdf1/ceopdf/MR017/MR0170272.PDF
    http://164.100.150.3/mrollpdf1/ceopdf/MR020/MR0200088.PDF
