import os
import xarray as xr
import argparse
from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD, SOSA
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from utils import unix_ts_to_date_str 
import json

# Define the namespaces
aqqa = Namespace("http://example.com/ontologies/aqqa#")
geo = Namespace("http://www.opengis.net/ont/geosparql#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
sf = Namespace("http://www.opengis.net/ont/sf#")

def convert_cams_aq_data_to_rdf(path_to_nc_file: str, var_name: str, path_to_rdf_file: str):
    """Reading in air quality observations from CAMS AQ into AQ graph with custom ontology"""
    
    path_to_observable_property_json = "/workspaces/aqqa-kg-creation-dev/ontology/observableProperties.json"
    with open(path_to_observable_property_json) as json_file:
        variables_dict = json.load(json_file)

    # Create a graph
    g = Graph()
    g.bind("aqqa", aqqa)


    ds = xr.open_dataset(path_to_nc_file)
    measurement_var = ds.variables[var_name.lower()]
    time_var = ds.variables["time"]

    for t_i, time in enumerate(time_var):
        for row_i in range(measurement_var.data.shape[1]):
            for col_i in range(measurement_var.data.shape[2]):
                t = unix_ts_to_date_str(time.item())
                measurement_value = measurement_var.data[t_i, row_i, col_i]

                ent_obs = URIRef(aqqa[f"Cell_{row_i}_{col_i}_ts_{t}_var_{var_name}"])
                ent_cell = URIRef(aqqa[f"Cell_{row_i}_{col_i}"])   
                ent_geom_cell = URIRef(aqqa[f"GeomCell_{row_i}_{col_i}"])   
                ent_obs_prop = URIRef(aqqa[f"{var_name}"])
                ent_cams_sensor = URIRef(aqqa[f"CAMS_AQ_reanalysis_ensemble_lvl_0"])
    
                g.add((ent_obs, RDF.type, SOSA.Observation))
                g.add((ent_obs, SOSA.madeBySensor, ent_cams_sensor))
                g.add((ent_obs, SOSA.observedProperty, ent_obs_prop))
                g.add((ent_obs, SOSA.hasFeatureOfInterest, ent_cell))
                g.add((ent_obs, SOSA.hasSimpleResult, Literal(measurement_value)))
                g.add((ent_obs, SOSA.resultTime, Literal(t, datatype=XSD.date)))

    g.serialize(destination=path_to_rdf_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert CAMS AQ data to RDF observations.")
    
    # Specify CLI arguments
    parser.add_argument("--path-to-nc", required=True, help="Path to the NetCDF file.")
    parser.add_argument("--variable", required=True, help="name of variable stored in nc file")
    parser.add_argument("--path-to-rdf", required=True, help="Path to save the RDF output file.")
    
    args = parser.parse_args()
    convert_cams_aq_data_to_rdf(args.path_to_nc, args.variable, args.path_to_rdf)


    


