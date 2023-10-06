#!/bin/bash

# Define common variables
BASE_PATH="/mnt/data/GADM"

# path to input data
path_to_austria_gadm_zip="${BASE_PATH}/raw/gadm41_AUT_shp.zip"
#path_to_german_gadm_zip="${BASE_PATH}/raw/gadm41_DEU_shp.zip"

# path to output
path_to_austria_rdf="${BASE_PATH}/RDF/gadm_AUT_RDF.ttl"
#path_to_german_rdf="${BASE_PATH}/RDF/gadm_DEU_RDF.ttl"

# Function to run and check Python scripts
run_python_script() {
    script_name="$1"
    shift
    python "../data_broker_components/$script_name" "$@"
    if [ $? -eq 0 ]; then
        echo "$script_name script executed successfully"
    else
        echo "Error: $script_name failed"
        exit 1
    fi
}

# Create GADM RDF for Austria
run_python_script "create_gadm_rdf.py" \
    --input-file $path_to_austria_gadm_zip \
    --output-file $path_to_austria_rdf

# Create GADM RDF for Germany
#run_python_script "create_gadm_rdf.py" \
#    --input-file $path_to_german_gadm_zip \
#    --output-file $path_to_german_rdf


        

