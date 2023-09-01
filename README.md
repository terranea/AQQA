# AQQA
Air Quality Question Answering (AQQA) project for AI4Copernicus


## CAMS Air Quality Data Downloader

This Python script allows you to easily download CAMS (Copernicus Atmosphere Monitoring Service) air quality data from the Atmospheric Data Store (ADS) using the CDS API. It supports downloading data for specified years, months, variables, and types.

### Prerequisites

Before using this script, make sure you have the following:

- A valid `.cdsapirc` file containing your ADS credentials (URL and API key)

### Usage 
```bash
python download_cams_aq_data.py --year YEAR --month MONTH --variables VARIABLE1 VARIABLE2 ... --type DATA_TYPE --output-path OUTPUT_PATH
```

#### Options

- `--path-to-input`: **Required.** Path to the zipped folder containing CAMS AQ data.
- `--bounding-box`: **Required.** Specify the bounding box for your area of interest. Provide four float values: `lat_min`, `lat_max`, `lon_min`, `lon_max`.
- `--path-to-output`: **Required.** Path to the location where unzipped and preprocessed NetCDF files will be stored.
- `YEAR`: **Required.** Year for which you want to download the data (e.g., 2020).
- `MONTH`: **Required.** Month for which you want to download the data (e.g., 01).
- `VARIABLE1 VARIABLE2 ...`: **Required.** List of variables to download (e.g., carbon_monoxide nitrogen_dioxide ozone).
- `TYPE`: **Required.** Type of data to download (e.g., validated_reanalysis or interim_reanalysis). At the current date, validated_reanalysis is only available up to 2020.
- `OUTPUT_PATH`: **Required.** Path to save the downloaded data (e.g., /mnt/data/raw/cams_euro_aq_reanalysis/2020/download_2020_01.zip).


#### Example:
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
- `--path-to-input`: **Required.** Path to the zipped folder containing CAMS AQ data.
- `--bounding-box`: **Required.** Specify the bounding box for your area of interest. Provide four float values: `lat_min`, `lat_max`, `lon_min`, `lon_max`.
- `--path-to-output`: **Required.** Path to the location where unzipped and preprocessed NetCDF files will be stored.

#### Example
```bash
python preprocess_cams_aq_data.py --path-to-input data.zip --bounding-box 45.82 50.65 8.95 17.22 --path-to-output processed_data
```

#### Output
Processed NetCDF files with aggregated and clipped data will be saved in the specified --path-to-output folder.


## CAMS AQ Data to RDF Conversion

This Python script enables the conversion of CAMS (Copernicus Atmosphere Monitoring Service) air quality data into RDF (Resource Description Framework) observations using a custom ontology. The script reads in air quality data from CAMS AQ and generates RDF triples, which can be used to represent and query the data in a semantic format.

### Usage

```bash
python convert_to_rdf.py --path-to-nc path_to_nc_file --variable variable_name --path-to-rdf path_to_rdf_file
```

#### Options

- `--path-to-nc`: **Required.** Path to the NetCDF file containing CAMS AQ data.
- `--variable`: **Required.** Name of the variable stored in the NetCDF file.
- `--path-to-rdf`: **Required.** Path to save the RDF output file.

#### Example
```bash
python convert_to_rdf.py --path-to-nc data.nc --variable ozone --path-to-rdf output.rdf
```

This example converts the CAMS AQ data from the data.nc NetCDF file, specifically for the "ozone" variable, and saves the resulting RDF triples in the output.rdf file.

#### Details
The script reads air quality observations from CAMS AQ data and converts them into RDF triples using a custom ontology. The RDF triples represent observations made by sensors and include information about the observed property, the feature of interest (location), the result, and the time of the observation.


## Create Reference Raster for CAMS AQ data

This script is designed to extract the cell geometries from CAMS (Copernicus Atmosphere Monitoring Service) AQ (Air Quality) data in NetCDF format and to transform it into RDF with geosparql ontology.

### Prerequisites

Before using this script, make sure you have a CAMS AQ nc file

## Usage

```shell
python script.py --input-file INPUT_FILE --output-file OUTPUT_FILE
```

