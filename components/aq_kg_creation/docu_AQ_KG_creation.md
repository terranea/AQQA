
# Instructions for creating your own Air Quality Knowledge Graph with CAMS data

To create your own Air Quality Knowledge Graph do the following steps:

## Transform CAMS Air Quality data to RDF


0) The task is to convert CAMS Air Quality data, which can be downloaded from the Atmospheric Data Store (https://ads.atmosphere.copernicus.eu), to RDF so that it can be integrated into semantic web applications, analyzed alongside other linked data sources, and made accessible for advanced data querying and visualization. The data will be converted based on an RDF schema which is based on the popular and well established SOSA ontology (https://www.w3.org/2015/spatial/wiki/SOSA_Ontology) The utilized RDF schema is visualized in the image below:

<img src="../../ontology/AQQA%20ontology.png"
     alt="AQQA RDF Schema"
     style="display: block; margin: 0 auto;"
     width="300" height="150" />

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
    - **PATH_TO_CDSAPIRC**: This constant stores the path to the Climage Data Store API Key. You have to create a key for yourself, store it in a folder and set the contant to the directory of this file. For the API key creation, follow this instructions: https://cds.climate.copernicus.eu/api-how-to 
    - **Path_TO_NAMESPACES_JSON**: This constant points to the json file where relevant namespaces their short forms are saved. 

3) Run the **create_CAMS_AW_RDF.sh** file
    - Make the file executable, by running the following command in the terminal:
    ```bash
    chmod +x filename.sh
    ````
    - Execute the script in the terminal
    ```bash
    ./create_CAMS_AQ_RDF.sh
    ```

4) Check out the outputs.
    - In the BASE_PATH folder you specified shoud be three subfolders:
        - raw: contains the zipped nc-file downloaded from Athmosperic data store
        - processed: contains the clipped and aggregated nc-files. One file for each variable
        - RDF: contains the final RDF file of CAMS Air Quality data


