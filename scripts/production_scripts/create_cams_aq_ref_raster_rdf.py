import xarray as xr
from shapely.geometry import Polygon, shape
import geojson
import os
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD, RDFS, SOSA, ConjunctiveGraph
from rdflib.plugins.stores import sparqlstore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST
import requests
import json
import argparse

# Constants
NAMESPACES_JSON_PATH = "/workspaces/aqqa-kg-creation-dev/ontology/namespaces.json"

def load_json_file(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

# Load dictionaries
namespaces_dict = load_json_file(NAMESPACES_JSON_PATH)

# Define the namespaces
namespace_mapping = {namespace["prefix"]: namespace["uri"] for namespace in namespaces_dict.get("namespaces", [])}
aqqa = Namespace(namespace_mapping.get("aqqa", None))
geo = Namespace(namespace_mapping.get("geo", None))
xsd = Namespace(namespace_mapping.get("xsd", None))
sf = Namespace(namespace_mapping.get("sf", None))


def nc_geometries_to_geojson(path_to_nc: str, path_to_geojson_output: str):
    """extract cell geometries from netcdf file and save as geojson"""

    # open file with xarray
    ds = xr.open_dataset(path_to_nc)

    # Get the raster data and corresponding coordinates
    data = ds.co.values
    lon = ds.lon.values
    lat = ds.lat.values

    # Calculate the resolution of the grid cells
    lon_resolution = lon[1] - lon[0]
    lat_resolution = lat[1] - lat[0]

    # Create empty lists to store polygons and values
    index_polygon_dic = {}

    # Iterate through each cell in the raster data
    for row in range(len(lat)):
        for col in range(len(lon)):

            # Define the vertices of the polygon for the current cell
            lon_left = lon[col]
            lon_right = lon[col] + lon_resolution
            lat_bottom = lat[row]
            lat_top = lat[row] + lat_resolution

            # Create the polygon for the current cell
            polygon = Polygon([(lon_left, lat_bottom), (lon_right, lat_bottom),
                            (lon_right, lat_top), (lon_left, lat_top)])

            # Append the polygon and its value to the respective lists
            index_polygon_dic[(row, col)] = polygon

    # save grid shapes as geosjaon
    features = []
    for index, geometry in index_polygon_dic.items():
        feature = geojson.Feature(geometry=geometry.__geo_interface__, properties={'index': index})
        features.append(feature)

    # Create a FeatureCollection from the list of features
    feature_collection = geojson.FeatureCollection(features)

    # Export the FeatureCollection to a GeoJSON file
    with open(path_to_geojson_output, 'w') as f:
        geojson.dump(feature_collection, f)


def convert_ref_grid_to_rdf(path_to_geojson: str, path_to_rdf_ouput: str):

    # loading ref raster cells
    with open(path_to_geojson, "r") as f:
        geojson_data = json.load(f)

    features = geojson_data.get("features", [])
    geometries = [feature.get("geometry") for feature in features]
    indexes = [feature.get("properties")["index"] for feature in features]
    shapely_geometries = [shape(geometry).wkt for geometry in geometries]

    # Create a graph
    g = Graph()
    g.bind("aqqa", aqqa)

    # reading geometries and Features of interest into RDF graph
    for i, (index, geom) in enumerate(zip(indexes, shapely_geometries)):
        
        ent_geom_cell = URIRef(aqqa[f"GeomCell_{index[0]}_{index[1]}"])   
        ent_cell = URIRef(aqqa[f"Cell_{index[0]}_{index[1]}"])   
        ent_hasID = URIRef(aqqa["hasID"])

        g.add((ent_cell, RDF.type, SOSA.FeatureOfInterest))
        g.add((ent_cell, ent_hasID, Literal(i)))
        g.add((ent_cell, geo.hasGeometry, ent_geom_cell))
        
        g.add((ent_geom_cell, RDF.type, sf.Geometry))
        g.add((ent_geom_cell, geo.asWKT, Literal(geom, datatype=geo.wktLiteral)))

    g.serialize(destination=path_to_rdf_ouput)


def create_cams_aq_ref_raster(path_to_nc: str, path_to_rdf_output: str):
    """Convert cell geometries of CAMS AQ nc file to RDF file"""


    path_to_geojson = os.path.join("/mnt/data/processed", "tmp_ref.gejson")
    print(path_to_geojson)
    nc_geometries_to_geojson(path_to_nc, path_to_geojson)
    convert_ref_grid_to_rdf(path_to_geojson, path_to_rdf_output)
    os.remove(path_to_geojson)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert cell geometries of CAMS AQ nc file to RDF file.")

    parser.add_argument("--input-file", required=True, help="Path to the input NetCDF.")
    parser.add_argument("--output-file", required=True, help="Path to the output RDF.")

    args = parser.parse_args()

    create_cams_aq_ref_raster(args.input_file, args.output_file)
