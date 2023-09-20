import os
import xarray as xr
import argparse
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD, SOSA
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
import json
from shapely.geometry import Point


# Constants
OBSERVABLE_PROPERTIES_JSON_PATH = "/workspaces/aqqa-kg-creation-dev/ontology/observableProperties.json"
NAMESPACES_JSON_PATH = "/workspaces/aqqa-kg-creation-dev/ontology/namespaces.json"

def load_json_file(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

# Load dictionaries
variables_dict = load_json_file(OBSERVABLE_PROPERTIES_JSON_PATH)
namespaces_dict = load_json_file(NAMESPACES_JSON_PATH)

# Define the namespaces
namespace_mapping = {namespace["prefix"]: namespace["uri"] for namespace in namespaces_dict.get("namespaces", [])}
aqqa = Namespace(namespace_mapping.get("aqqa", None))
geo = Namespace(namespace_mapping.get("geo", None))
xsd = Namespace(namespace_mapping.get("xsd", None))
sf = Namespace(namespace_mapping.get("sf", None))


def coordinates_to_wkt(x, y):
    "convert point coordinates to wkt literal"
    point = Point(x, y)
    wkt = point.wkt
    return wkt

def create_sensor_rdf(path_to_geojson: str, path_to_rdf_output: str):
    """convert sensor community data (sensors and locations) geojson to rdf file"""

    # Create a graph
    g = Graph()
    g.bind("aqqa", aqqa)

    provider = "SensorCommunityAPI"

    path_to_geojson = path_to_geojson
    with open(path_to_geojson, 'r') as geojson_file:
        data = json.load(geojson_file)

    for sensor in data["features"]:
        
        sensor_id = sensor["properties"]["sensor_id"]
        sensor_coords = sensor["geometry"]["coordinates"]
        sensor_geom_wkt = coordinates_to_wkt(sensor_coords[0], sensor_coords[1])
    
        ent_sensor = URIRef(aqqa[f"sensor?id={sensor_id}"])
        ent_sensor_geom = URIRef(aqqa[f"sensor_location_geom?id={sensor_id}"])
        ent_has_provider = URIRef(aqqa["hasProvider"]) 
        ent_foi = URIRef(aqqa[f"sensor_location?id="])
    
        g.add((ent_sensor, RDF.type, SOSA.Sensor))
        g.add((ent_sensor, geo.hasGeometry, ent_sensor_geom))
        g.add((ent_sensor, aqqa.hasProvider, Literal("Sensor Community API")))
        g.add((ent_sensor_geom, RDF.type, sf.Geometry))
        g.add((ent_sensor_geom, geo.asWKT, Literal(sensor_geom_wkt, datatype=geo.wktLiteral)))

        for observation in sensor["properties"]["values"]:
            timestamp, pm10, pm25 = observation

            ent_observation_pm25 = URIRef(aqqa[f"provider={provider}&sensor_id={sensor_id}&var=pm25&time={timestamp}"])
            ent_observation_pm10 = URIRef(aqqa[f"provider={provider}&sensor_id={sensor_id}&var=pm10&time={timestamp}"])

            g.add((ent_observation_pm25, RDF.type, SOSA.Observation))
            g.add((ent_observation_pm25, SOSA.hasFeatureOfInterest, ent_foi))
            g.add((ent_observation_pm25, SOSA.madeBySensor, ent_sensor))
            g.add((ent_observation_pm25, SOSA.observedProperty, URIRef(aqqa["PM2P5"])))
            g.add((ent_observation_pm25, SOSA.hasSimpleResult, Literal(pm25, datetype=XSD.float)))
            g.add((ent_observation_pm25, SOSA.resultTime, Literal(timestamp, datatype=XSD.date)))

            g.add((ent_observation_pm10, RDF.type, SOSA.Observation))
            g.add((ent_observation_pm10, SOSA.hasFeatureOfInterest, ent_foi))
            g.add((ent_observation_pm10, SOSA.madeBySensor, ent_sensor))
            g.add((ent_observation_pm10, SOSA.observedProperty, URIRef(aqqa["PM10"])))
            g.add((ent_observation_pm10, SOSA.hasSimpleResult, Literal(pm10, datetype=XSD.float)))
            g.add((ent_observation_pm10, SOSA.resultTime, Literal(timestamp, datatype=XSD.date)))
    
    g.serialize(destination=path_to_rdf_output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert Sensor Community data to RDF.")
    
    # Specify CLI arguments
    parser.add_argument("--path-to-geojson", required=True, help="Path to the geojson file containing sensor observations. Output of get_sensor_community_data.py")
    parser.add_argument("--path-to-rdf", required=True, help="Path to save the RDF output file.")
    
    args = parser.parse_args()
    create_sensor_rdf(args.path_to_geojson, args.path_to_rdf)