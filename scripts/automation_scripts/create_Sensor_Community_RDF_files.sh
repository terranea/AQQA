#!/bin/bash

# Define lists of years and months
years=(2022)
months=(1 2)
PATH_TO_SENSOR_IDS="/mnt/data/processed/Sensor_Community/sensor_community_ids_aoi_sds011.csv"

# Loop over years
for year in "${years[@]}"; do

    # Loop over months
    for month in "${months[@]}"; do
        # Run the first Python script with the current year and month
        path_to_sensor_geojson="/mnt/data/processed/Sensor_Community/observations/sensor_community_data_${year}_${month}.geojson"
        python ../data_broker_components/get_sensor_community_data.py --year $year --month $month --output $path_to_sensor_geojson --sensor_id_file $PATH_TO_SENSOR_IDS

        # Check the exit status of the first script
        if [ $? -eq 0 ]; then
            echo "First script executed successfully for Year $year Month $month."
        else
            echo "Error: First script failed for Year $year Month $month."
            exit 1
        fi

        # Run the second Python script with the output of the first script
        path_to_sensor_rdf="/mnt/data/processed/RDF/Sensor_Community/sensor_community_data_${year}_${month}.ttl"
        python ../data_broker_components/convert_sensor_comm_geojson_to_rdf.py --path-to-geojson $path_to_sensor_geojson --path-to-rdf $path_to_sensor_rdf

        # Check the exit status of the second script
        if [ $? -eq 0 ]; then
            echo "Second script executed successfully for Year $year Month $month."
        else
            echo "Error: Second script failed for Year $year Month $month."
            exit 1
        fi

        echo "Year $year Month $month: Both scripts completed successfully."
    done
done
