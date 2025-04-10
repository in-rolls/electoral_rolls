## Indian Electoral Rolls

We have built a dataset of nearly all the Indian electors. Our data includes information on first and last name, gender, polling station (constituency, district, and state), father or husband's name, among other such details. We assembled this data by scraping and parsing the electoral rolls.

This repository includes scripts for downloading  the PDF electoral rolls from the various state election commission sites. [Parse PDF Rolls](https://github.com/in-rolls/parse_elex_rolls) has scripts for parsing the electoral rolls, scripts for translating native language rolls to English, and information about the resulting CSVs.

### Electoral Rolls

To ameliorate concerns about eligible voters not being on the rolls (and ineligible electors being on the rolls), the [Election Commission of India](http://eci.nic.in/eci/eci.html) mandates that state election commissions publish electoral rolls. As a result, the 36 different election commissions---29 states and 7 union territories---post electoral rolls for each polling station on their websites. The websites vary enormously in design, in the metadata they provide about the polling stations, and the language in which they provide the electoral rolls. For instance, some commissions provide electoral rolls in English, some in the main native language(s) of the state, and some in both the main native language(s) of the state and English. The only thing that is constant is that these electoral rolls are provided in dense pdfs. So we wrote separate scrapers for downloading the pdfs. In many cases, we also downloaded the metadata for each of the polling stations (pdfs) that was on the website. (A [separate repository](https://github.com/in-rolls/poll-station-metadata) uses a different source of data to collate metadata on polling stations.) For scripts, information about the source of the electoral rolls, and such, see the table below. 

### How Do I Get the Electoral Roll PDFs?

Given privacy concerns, we are releasing the data only for research purposes. To access the pdfs, you must agree to take all precautions to maintain the privacy of Indian electors. (There is a difference between data being available in pdfs, split across different sites, sometimes behind CAPTCHA, and a common data dump.) If you would like access to the electoral rolls, please fill out the following [form](https://goo.gl/forms/03YnSiQFpOig4H7H3). 

You will need to also get IRB approval from your respective university or institution. The IRB-approved proposal should include:

1. Case for why the data are necessary
2. Acknowledgment that the data will be kept in a secure environment
3. All the people who will have access to the data
4. That the data will only be used on projects with IRB approval 
5. That data won't be shared with people who are not identified in 3.
6. That publications and presentations will not reveal identifying individual information: only statistical summaries will be presented. 

#### Accessing the Data

The data are available on [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/OG47IV) and via Google Coldline Storage. The GCS buckets are setup as requester pays. So you need to create a project that will be used for billing.

To access data from GCS, you will need to do the following:

```
gsutil -u projectname_for_billing ls gs://in-electoral-rolls/
```

```
gs://in-electoral-rolls/andaman.tar.gz
gs://in-electoral-rolls/andhra_pdfs.tar.gz
gs://in-electoral-rolls/arunachal.tar.gz
gs://in-electoral-rolls/assam.tar.gz
gs://in-electoral-rolls/bihar.tar.gz
gs://in-electoral-rolls/chandigarh_pdfs.tar.gz
gs://in-electoral-rolls/dadra_pdfs.tar.gz
gs://in-electoral-rolls/daman_2015.tar.gz
gs://in-electoral-rolls/daman_2016.tar.gz
...
```

If you would like access to CSVs from parsing the electoral roll pdfs, check out [https://github.com/in-rolls/parse_elex_rolls](https://github.com/in-rolls/parse_elex_rolls). The data are posted on the Harvard Dataverse at [http://dx.doi.org/10.7910/DVN/MUEGDT](http://dx.doi.org/10.7910/DVN/MUEGDT).

### Suggested Citation

Gaurav Sood and Atul Dhingra. 2018. Indian Electoral Rolls PDF Corpus. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/OG47IV

### Scripts and Information by State

| State                                    | Year(s) | Language(s)              |
| ---------------------------------------- | ------- | ------------------------ |
| [Andaman & Nicobar Islands](andaman/)    | 2017    | English                  |
| [Andhra Pradesh](andhra/)                | 2017    | Telugu, English          |
| [Arunachal Pradesh](arunachal/)          | 2017    | English                  |
| [Assam](assam/)                          | 2018    | Bengali                  |
| [Bihar*](bihar/)                         | 2017    | Hindi                    |
| [Chattisgarh](chattisgarh/)--- Not reachable | --      | --                       |
| [Chandigarh](chandigarh/)                | 2018    | Hindi                    |
| [Dadra & Nagar Haveli](dadra/)           | 2017    | Gujarati, English        |
| [Daman & Diu](daman/)                    | 2017    | Gujarati, English        |
| [Goa](goa/)                              | 2018    | English                  |
| [Gujarat](gujarat/)                      | 2017    | Gujarati                 |
| [Haryana](haryana/)                      | 2018    | Hindi                    |
| [Himachal Pradesh](himachal/)            | 2017    | Hindi                    |
| [Jammu & Kashmir](jammu_kashmir/)        | 2018    | Hindi, English, and Urdu |
| [Jharkhand](jharkhand/)                  | 2018    | Hindi                    |
| [Lakshadweep](lakshadweep/)              | 2017    | Malayalam                |
| [Karnataka](karnatka/)                   | 2018    | Kannada                  |
| [Kerala](kerala/)                        | 2018    | Malayalam, English       |
| [Madhya Pradesh](mp/)                    | 2017    | Hindi                    |
| [Maharashtra](maharashtra/)              | 2018    | Marathi                  |
| [Manipur](manipur/)                      | 2018    | Manipuri, English        |
| [Meghalaya](meghalaya/)                  | 2018    | English                  |
| [Mizoram](mizoram/)                      | 2018    | English                  |
| [Nagaland](nagaland/)                    | 2018    | English                  |
| [NCT OF Delhi](delhi/)                   | 2018    | Hindi, English           |
| [Odisha](odisha/)                        | 2018    | Odia                     |
| [Punjab](punjab/)                        | 2018    | Punjabi                  |
| [Puducherry](puducherry/)                | 2018    | Tamil, English           |
| [Rajasthan](rajasthan/)                  | 2014    | Hindi                    |
| [Sikkim](sikkim/)                        | 2018    | English                  |
| [Tamil Nadu](tn/)                        | 2018    | Tamil                    |
| [Telangana](telangana/)                  | 2017    | Telugu                   |
| [Tripura](tripura/)                      | 2018    | Bengali                  |
| [Uttar Pradesh](up/)                     | 2018    | Hindi                    |
| [Uttarakhand](uttarakhand/)              | 2017    | Hindi                    |
| [West Bengal](west_bengal/)                       | 2018    | Bengali                   |


### Archives and 2020

| State                                | Year(s)    | Language(s)       |
| ------------------------------------ | ---------- | ----------------- |
| Bihar (see acknowledgments)          | 2015       | Hindi             |
| [Bihar](https://github.com/in-rolls/bihar-2020-electoral-rolls)                            | 2020       | Hindi             |
| [Daman](daman_archives/)             | 2015--2016 | English, Gujarati |
| [Karnataka](karnataka/)              | 2015--2017 | Kannada           |
| [Kerala](kerala_archives/)           | 2011-2016  | Malyalam          |
| [Uttarakhand](uttarakhand_archives/) | 2007--2016 | Hindi             |

### Acknowledgments

* Bihar 2015 electoral rolls were contributed by Aaditya Dar. Aaditya also pointed us the right way to setup a data access procedure where researchers need to get IRB approval.
* The specifics of IRB are 'inspired' by http://adfdell.pstc.brown.edu/arisreds_data/readme.txt   
* Elian Carsenat helped us craft better directions for how to access data on GOOG storage. 

### License

The scripts are provided under the [MIT license](https://opensource.org/licenses/MIT). 

## 🔗 Adjacent Repositories

- [in-rolls/elector_count](https://github.com/in-rolls/elector_count) — Estimate the total number of electors in a state by counting the number of pages in all the electoral rolls
- [in-rolls/parse_searchable_rolls](https://github.com/in-rolls/parse_searchable_rolls) — Parse Searchable Electoral Rolls
- [in-rolls/google_vision_ocr](https://github.com/in-rolls/google_vision_ocr) — Using Google Vision API to Get Text From (Unreadable) Electoral Rolls
- [in-rolls/poll-station-metadata](https://github.com/in-rolls/poll-station-metadata) — Metadata on Polling Stations, including Officers, data on the building, and link to electoral rolls (some inactive)
- [in-rolls/local_elections_bihar](https://github.com/in-rolls/local_elections_bihar) — Candidate Info. + Valid Votes Won by Cands. in the 2016 Bihar Panchayat Elections
