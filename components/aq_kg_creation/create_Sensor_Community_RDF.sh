#!/bin/bash

# Define common variables
BASE_PATH="/mnt/data/Sensor_Community"
years=(2020)
months=(1 2)
PATH_TO_SENSOR_IDS="${BASE_PATH}/sensor_community_ids_test.csv"
OBSERVATIONS_PATH="${BASE_PATH}/observations"

# Create the observations directory if it doesn't exist
mkdir -p "$OBSERVATIONS_PATH"

# Function to run and check Python scripts
run_python_script() {
    script_name="$1"
    shift
    python "data_broker_components/$script_name" "$@"
    if [ $? -eq 0 ]; then
        echo "$script_name script executed successfully for Year $year Month $month."
    else
        echo "Error: $script_name failed for Year $year Month $month."
        exit 1
    fi
}

# Loop over years and months
for year in "${years[@]}"; do
    for month in "${months[@]}"; do
        # Get sensor community data, process and write to geojson
        sensor_data_geojson="$OBSERVATIONS_PATH/sensor_community_data_${year}_${month}.geojson"
        run_python_script "get_sensor_community_data.py" \
            --year "$year" \
            --month "$month" \
            --output "$sensor_data_geojson" \
            --sensor_id_file "$PATH_TO_SENSOR_IDS"

        # Convert the sensor community data to RDF
        sensor_data_rdf="$OBSERVATIONS_PATH/sensor_community_data_${year}_${month}.ttl"
        run_python_script "convert_sensor_comm_geojson_to_rdf.py" \
            --path-to-geojson "$sensor_data_geojson" \
            --path-to-rdf "$sensor_data_rdf"

        echo "Year $year Month $month: Both scripts completed successfully."
    done
done