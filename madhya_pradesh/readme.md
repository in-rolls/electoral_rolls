### Madhya Pradesh


### Details

URL = http://ceomadhyapradesh.nic.in/voterlist2017.aspx

Year = Draft Roll for 2017

### Running Scripts

1. `conda env create -f tools/environment.yml` to install working environment and
    `source activate erolls`
2.  Or, `pip install -r requirements.txt` if not using a conda environment
3. `tools/utils.py` is a helper function for downloading files, and sanity checks
4. `python mp_brute_force.py` to downloads all the pdfs to directory `../data/MP/`
    and creates 'mp.txt' for files that were not downloaded successfully
5. `python mp_retry.py` for retrying downloads for files in 'mp.txt'
6. `python mp_SanityCheck.py` for doing a sanity check on the files downloaded

### Note
1. Total Number of files =  62552
2. The downloaded files are of form A_{District number}_S12A{District number}P{assembly constituency number}.pdf
3. Files not available can be found in 'mp3.txt''

