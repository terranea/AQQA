
# Instructions for creating your own Air Quality Knowledge Graph with CAMS data

To create your own Air Quality Knowledge Graph do the following steps:

## Transform CAMS AQ data to RDF

1) In the **create_CAMS_AQ_RDF.sh** script define which CAMS AQ data should be donwloaded and converted to RDF. Define the following parameters:
    - **Path to Data** e.g.
    ```bash 
    BASE_PATH="/mnt/data/CAMS"
    ```
    - **Bounding Box** e.g.
    ```bash 
    bounding_box="45.82 50.65 8.95 17.22"
    ```
    - **Years and months of interest** e.g.
    ```bash 
    years=(2020)
    months=(01 02 03 11)
    ```
    - **Air Quality Variables of interest** e.g.
    ```bash
    variables_short=("co" "no2" "o3" "pm10" "pm2p5" "so2")
    variables_long="carbon_monoxide nitrogen_dioxide ozone particulate_matter_10um particulate_matter_2.5um sulphur_dioxide"
    ```
    In this case the variables have to be specified in short and long form. This inconvenience will be fixed in future commits. 

2) In the **data_broker_components/config.py**-file the specified constants need to point to the right files. 
    - **PATH_TO_CDSAPIRC**: This variable stores the path to the Climage Data Store API Key. You have to create a key for yourself, store it in a folder and point the variable to this folder. For the API key creation, follow this instructions: https://cds.climate.copernicus.eu/api-how-to 
    - 




# TODO not working in this format - right now hardcoded it into python command below
#variables=(carbon_monoxide nitrogen_dioxide ozone particulate_matter_10um particulate_matter_2.5um sulphur_dioxide)

variables_short=("co" "no2" "o3" "pm10" "pm2p5" "so2")
variables_short=("co")
type="validated_reanalysis"



Area of Interest (AOI) and the timerange for the CAMS data that should be converted to RDF



1) Create a CDS API Key and store it on your device. 
2) In the 


