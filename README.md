# AQQA
Air Quality Question Answering (AQQA) project for AI4Copernicus


## CAMS Air Quality Data Downloader

This Python script allows you to easily download CAMS (Copernicus Atmosphere Monitoring Service) air quality data from the Atmospheric Data Store (ADS) using the CDS API. It supports downloading data for specified years, months, variables, and types.

## Prerequisites

Before using this script, make sure you have the following:

- A valid `.cdsapirc` file containing your ADS credentials (URL and API key)

## Usage 
```bash
python download_cams_aq_data.py --year YEAR --month MONTH --variables VARIABLE1 VARIABLE2 ... --type DATA_TYPE --output-path OUTPUT_PATH
```

Replace the placeholders:

YEAR: Year for which you want to download the data (e.g., 2020).
MONTH: Month for which you want to download the data (e.g., 01).
VARIABLE1 VARIABLE2 ...: List of variables to download (e.g., carbon_monoxide nitrogen_dioxide ozone).
TYPE: Type of data to download (e.g., validated_reanalysis or interim_reanalysis). At current date validated_reanalysis is only availabe up to 2020
OUTPUT_PATH: Path to save the downloaded data (e.g., /mnt/data/raw/cams_euro_aq_reanalysis/2020/download_2020_01.zip).

Example:
```bash
python download_cams_aq_data.py --year 2020 --month 01 --variables carbon_monoxide nitrogen_dioxide ozone --type validated_reanalysis --output-path /path/to/output.zip
```

