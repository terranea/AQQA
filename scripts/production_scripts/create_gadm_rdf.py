import os
import argparse
import json
import zipfile
import glob
from pathlib import Path
import fiona
from shapely.geometry import shape
from rdflib import Graph, Literal, Namespace, URIRef, RDF
from rdflib.namespace import GEO
import shutil

# Constants
NAMESPACES_JSON_PATH = "/workspaces/aqqa-kg-creation-dev/ontology/namespaces.json"

def load_json_file(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)
        
# Load dictionaries
namespaces_dict = load_json_file(NAMESPACES_JSON_PATH)

# Define the namespaces
namespace_mapping = {namespace["prefix"]: namespace["uri"] for namespace in namespaces_dict.get("namespaces", [])}
gadm = Namespace(namespace_mapping.get("gadm", None))
xsd = Namespace(namespace_mapping.get("xsd", None))
sf = Namespace(namespace_mapping.get("sf", None))


def create_gadm_rdf(path_to_gadm_folder_zip: str, path_to_output_rdf: str):
    """Converts shp-files within a zipped gadm folder to RDF"""

    # Create a graph
    g = Graph()
    g.bind("gadm", gadm)

    # Unzip gadm data to a temporary folder
    temp_path = Path("tmp_gadm")
    temp_path.mkdir(exist_ok=True)
    with zipfile.ZipFile(path_to_gadm_folder_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_path)
    
    # Get paths to individual shp files
    search_string = str(temp_path / "*.shp")
    path_to_shp_files = glob.glob(search_string)

    for path_to_shp_file in path_to_shp_files:

        adm_lvl = int(Path(path_to_shp_file).stem.split("_")[-1])
        
        # Open the Shapefile using fiona
        with fiona.open(path_to_shp_file, 'r') as src:
            for feature in src:
                geometry = shape(feature['geometry'])
                geometry_wkt = geometry.wkt

                if adm_lvl > 0:
                
                    # extracting information
                    gid = feature["properties"][f"GID_{adm_lvl}"].replace(".", "_")
                    name = feature["properties"][f"NAME_{adm_lvl}"]
                    type_ = feature["properties"][f"TYPE_{adm_lvl}"]
                    country = feature["properties"]["COUNTRY"]
                    
                    # creating entities
                    ent_adm_unit = URIRef(gadm[gid])
                    ent_adm_unit_geom = URIRef(gadm[f"GEOM_{gid}"])
                    ent_hasName = URIRef(gadm["hasName"])
                    ent_hasNationalLevel = URIRef(gadm["hasNationalLevel"])
                    ent_hasType = URIRef(gadm["hasType"])
                    ent_country = URIRef(gadm["country"])
                    ent_hasUpperLevelUnit = URIRef(gadm["hasUpperLevelUnit"].replace(".", "_"))
            
                    # creating rdf triples
                    g.add((ent_adm_unit, RDF.type, gadm.AdministrativeUnit))
                    g.add((ent_adm_unit, ent_hasName, Literal(name)))
                    g.add((ent_adm_unit, ent_hasNationalLevel, Literal(adm_lvl)))
                    g.add((ent_adm_unit, ent_hasType, Literal(type_)))
                    g.add((ent_adm_unit, ent_country, Literal(country)))
                    g.add((ent_adm_unit, GEO.hasGeometry, ent_adm_unit_geom))
                    g.add((ent_adm_unit_geom, RDF.type, sf.Geometry))
                    g.add((ent_adm_unit_geom, GEO.asWKT, Literal(geometry_wkt, datatype=GEO.wktLiteral)))
                
                    gid_upper_lvl = feature["properties"][f"GID_{adm_lvl - 1}"].replace(".", "_")
                    ent_upper_level_unit = URIRef(gadm[gid_upper_lvl])
                    g.add((ent_adm_unit, ent_hasUpperLevelUnit, ent_upper_level_unit))
                
                # in the case of admin level 0
                else:
                    gid = feature["properties"][f"GID_{adm_lvl}"].replace(".", "_")
                    country = feature["properties"]["COUNTRY"]

                    ent_adm_unit = URIRef(gadm[gid])
                    ent_adm_unit_geom = URIRef(gadm[f"GEOM_{gid}"])
                    ent_country = URIRef(gadm["country"])

                    g.add((ent_adm_unit, RDF.type, gadm.AdministrativeUnit))
                    g.add((ent_adm_unit, ent_country, Literal(country)))
                    g.add((ent_adm_unit, GEO.hasGeometry, ent_adm_unit_geom))
                    g.add((ent_adm_unit_geom, RDF.type, sf.Geometry))
                    g.add((ent_adm_unit_geom, GEO.asWKT, Literal(geometry_wkt, datatype=GEO.wktLiteral)))

    # Serialize the RDF graph and remove the temporary folder
    g.serialize(destination=path_to_output_rdf)
    shutil.rmtree(temp_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create RDF file from GADM data.")
    parser.add_argument("--input-file", required=True, help="Path to the zipped GADM folder downloaded from https://gadm.org/.")
    parser.add_argument("--output-file", required=True, help="Path to the output RDF.")
    args = parser.parse_args()
    
    # Define the namespaces
    namespaces_dict = load_json_file(NAMESPACES_JSON_PATH)
    namespace_mapping = {namespace["prefix"]: namespace["uri"] for namespace in namespaces_dict.get("namespaces", [])}
    gadm = Namespace(namespace_mapping.get("gadm", None))

    create_gadm_rdf(args.input_file, args.output_file)


    #https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_AUT_shp.zip
