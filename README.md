# Risikogebiete_api

An API for the countries classified as risk areas by Germany in the context of SARS-CoV-2.


## Background

In June 2020, the German Robert Koch Institut started publishing reports of the different countries presenting an increased risk of infection with SARS-CoV-2 and classified as risk areas. These reports are accessible in pdf format at this address: [https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html)

This project intends to provide the published reports in csv and json formats for easier analysis.
- each report is available in the folder [individual_reports](./individual_reports)
- all the reports are merged in one file: [data.csv](./data.csv) / [data.json](./data.json)

The list of parsed reports is updated every day at midnight German time (GMT+1).


## Format
### Dates
The dates and times of each report are given in the ISO 8601 format. When the time is mentioned on the report it is added, otherwise it is left as 00:00:00

### Countries
The reports parsed are the ones in German, but the countries are provided in English, along with their respective iso3166 codes (alpha 2, alpha 3 and numeric).

### Regions
Parsing of different regions is not implemented. If only a region from a country is part of the list, the country will appear in the reports.


## Disclaimer

The format that the RKI has used for their report has changed multiple times. As well, their reports are most probably typed by hand. When there are new typos and the program can't translate a country in English, i will try to fix the code to accommodate for these new typos as fast as possible.

In that case, as long as the typo is not solved, the mistyped country will be shown as written in the original report, and without the iso3166 codes.


## Development

To run the program (from the root directory):
1. create a virtual environment: `python -m venv .venv`
1. install the dependencies: `pip install -r requirements_dev.txt`
1. install the program: `pip install -e .`
1. (install the pre-commit hooks: `pre-commit install`)
1. the program is accessible from the command line by typing: `risikogebiete_api`


## Dependencies

- pdfminer.six
- requests
- beautifulsoup4
- aiofiles
- aiohttp
- aiocsv
- country_list
- iso3166


## Credits

All the reports are published by the Robert Koch Institut, so without their work this repository would not exist.
