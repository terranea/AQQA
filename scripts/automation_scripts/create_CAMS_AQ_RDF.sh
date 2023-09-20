#!/bin/bash

# Define common variables
BASE_PATH="/mnt/data/CAMS"
years=(2020)
months=(01 02)
# TODO not working in this format
#bounding_box=(45.82 50.65 8.95 17.22) - right now hard hardcoded it into python command below
# TODO not working in this format - right now hardcoded it into python command below
#variables=(carbon_monoxide nitrogen_dioxide ozone particulate_matter_10um particulate_matter_2.5um sulphur_dioxide)
variables_short=("co" "no2" "o3" "pm10" "pm2p5" "so2")
#variables_short=("co")
type="validated_reanalysis"


# Function to run and check Python scripts
run_python_script() {
    script_name="$1"
    shift
    python "../data_broker_components/$script_name" "$@"
    if [ $? -eq 0 ]; then
        echo "$script_name script executed successfully for Year $year Month $month."
    else
        echo "Error: $script_name failed for Year $year Month $month."
        exit 1
    fi
}

# Loop over years
for year in "${years[@]}"; do
    # Loop over months
    for month in "${months[@]}"; do
        
        # Download CAMS AQ data
        output_path_cams_aq_folder="${BASE_PATH}/raw/${year}/${month}"
        mkdir -p "$output_path_cams_aq_folder"
        run_python_script "download_cams_aq_data.py" \
            --year "$year" \
            --month "$month" \
            --variables carbon_monoxide nitrogen_dioxide ozone particulate_matter_10um particulate_matter_2.5um sulphur_dioxide \
            --type "$type" \
            --output-path "${output_path_cams_aq_folder}/cams_aq_${year}_${month}_${type}.zip"
        
        # Preprocess the downloaded data
        path_to_nc_folder="${BASE_PATH}/processed/${year}/${month}"
        mkdir -p "$path_to_nc_folder"
        run_python_script "preprocess_cams_aq_data.py" \
            --path-to-input "${output_path_cams_aq_folder}/cams_aq_${year}_${month}_${type}.zip" \
            --bounding-box 45.82 50.65 8.95 17.22 \
            --path-to-output "$path_to_nc_folder"

        # Convert CAMS AQ observations to RDF
        path_to_rdf_folder="${BASE_PATH}/RDF/observations/${year}/${month}"
        mkdir -p "$path_to_rdf_folder"
        for variable in "${variables_short[@]}"; do
            run_python_script "convert_cams_aq_nc_to_rdf.py" \
                --path-to-nc "${path_to_nc_folder}/cams_aq_${variable}_${year}${month}.nc" \
                --variable "$variable" \
                --path-to-rdf "${path_to_rdf_folder}/cams_aq_${year}_${month}_${variable}.ttl"
        done
    done
done

# Create RDF file for reference grid
path_to_ref_grid_rdf="${BASE_PATH}/RDF/CAMS_reference_grid.ttl"
run_python_script "create_cams_aq_ref_raster_rdf.py" \
    --input-file "${path_to_nc_folder}/cams_aq_${variable}_${year}${month}.nc" \
    --output-file "$path_to_ref_grid_rdf"
