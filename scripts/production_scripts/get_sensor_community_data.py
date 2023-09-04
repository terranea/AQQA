import pandas as pd
import calendar
import json
import argparse
import concurrent.futures
import requests
from typing import List

def generate_urls(year: int, month: int, sensor_id: int, sensor_type: str = "sds011") -> List[str]:
    """Generate URLs to download data from sensor community sensors."""

    urls = []

    suffix = "csv" if year in [2021, 2022] else "csv.gz"
    days_in_month = calendar.monthrange(year, month)[1]
    
    for day in range(1, days_in_month + 1):
        formatted_date = f"{year}-{month:02d}-{day:02d}"
        url = f"http://archive.sensor.community/{year}/{formatted_date}/{formatted_date}_{sensor_type}_sensor_{sensor_id}.{suffix}"
        urls.append(url)

    return urls

def process_sensor_data(url, sid):
    """extract coordinates of sensor and aggregate PM10 and PM25 values to daily temporal resolution (24h)"""

    try:
        df = pd.read_csv(url, sep=";")
        lat = df.loc[0, "lat"]
        lon = df.loc[0, "lon"]
        p1_value = df["P1"].mean()
        p2_value = df["P2"].mean()
        date = url.split("/")[-2]
        return (date, p1_value, p2_value, lon, lat)
    except Exception as e:
        return None

def create_geojson_from_sensor_data(sensors_of_interest_df: pd.DataFrame, year: int, month: int, path_to_geojson_output: str):
    """Download sensor data for 1 month for all sensors in the list, process data, and save as GeoJSON."""

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _, item in sensors_of_interest_df.iterrows():
            sid = int(item["sensor_id"])
            url_list = generate_urls(year, month, sid)
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": []
                },
                "properties": {
                    "sensor_id": sid,
                    "values": []
                }
            }

            for url in url_list:
                futures.append(executor.submit(process_sensor_data, url, sid))

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    date, p1_value, p2_value, lon, lat = result
                    feature["properties"]["values"].append((date, p1_value, p2_value))
                    feature["geometry"]["coordinates"] = [lon, lat]

            geojson_data["features"].append(feature)

    geojson_string = json.dumps(geojson_data, indent=2)

    with open(path_to_geojson_output, "w") as geojson_file:
        geojson_file.write(geojson_string)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate GeoJSON from Sensor Community Data")
    parser.add_argument("--year", type=int, help="Year for data retrieval")
    parser.add_argument("--month", type=int, help="Month for data retrieval")
    parser.add_argument("--output", type=str, help="Path to GeoJSON output file")
    parser.add_argument("--sensor_id_file", type=str, help="Path to CSV file with sensor IDs")

    args = parser.parse_args()

    if not all([args.year, args.month, args.output, args.sensor_id_file]):
        parser.error("Missing required arguments")

    path_to_sensor_ids = args.sensor_id_file
    sensors_of_interest_df = pd.read_csv(path_to_sensor_ids)
    # TODO: Bug which needs to be fixed. When csv storing the sensor ids is not in the right format the code does not work
    sensors_of_interest_df = sensors_of_interest_df.sample(100, random_state=0)
    create_geojson_from_sensor_data(sensors_of_interest_df, args.year, args.month, args.output)
