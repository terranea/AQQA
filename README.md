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

#### Options
YEAR: Year for which you want to download the data (e.g., 2020).
MONTH: Month for which you want to download the data (e.g., 01).
VARIABLE1 VARIABLE2 ...: List of variables to download (e.g., carbon_monoxide nitrogen_dioxide ozone).
TYPE: Type of data to download (e.g., validated_reanalysis or interim_reanalysis). At current date validated_reanalysis is only availabe up to 2020
OUTPUT_PATH: Path to save the downloaded data (e.g., /mnt/data/raw/cams_euro_aq_reanalysis/2020/download_2020_01.zip).

#### Exampole:
```bash
python download_cams_aq_data.py --year 2020 --month 01 --variables carbon_monoxide nitrogen_dioxide ozone --type validated_reanalysis --output-path /path/to/output.zip
```


## CAMS Air Quality Data Preprocessing

This Python script allows you to preprocess CAMS (Copernicus Atmosphere Monitoring Service) air quality data. The script extracts specific variables from zipped NetCDF files, clips them to a specified bounding box, and performs temporal aggregation before saving the results as new NetCDF files.

### Usage 

```bash
python preprocess_cams_aq_data.py --path-to-input path_to_zip_folder --bounding-box lat_min lat_max lon_min lon_max --path-to-output path_to_output_folder
```

Replace the placeholders path_to_zip_folder, lat_min, lat_max, lon_min, lon_max, and path_to_output_folder with your actual values.

#### Options
--path-to-input: Required. Path to the zipped folder containing CAMS AQ data.
--bounding-box: Required. Specify the bounding box for your area of interest. Provide four float values: lat_min, lat_max, lon_min, lon_max.
--path-to-output: Required. Path to the location where unzipped and preprocessed NetCDF files will be stored.

#### Example
```bash
python preprocess_cams_aq_data.py --path-to-input data.zip --bounding-box 45.82 50.65 8.95 17.22 --path-to-output processed_data
```

#### Output
Processed NetCDF files with aggregated and clipped data will be saved in the specified --path-to-output folder.