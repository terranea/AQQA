import geojson
import json
import shapely.wkt
from SPARQLWrapper import SPARQLWrapper, JSON
from .config import STRABON_SPARQL_ENDPOINT
import pandas as pd


def query_sparql_endpoint(sparql_query: str):
    """query sparql endpoint"""

    sparql = SPARQLWrapper(STRABON_SPARQL_ENDPOINT)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    return results


def convert_query_output_to_geojson(results: dict):
    """convert query results about cams observations to geojson"""

    try:
        # Execute the query and get the results
        features = []
        for r in results["results"]["bindings"]:
            geom_wkt = r["foi_geom"]["value"]
            obs_time = r["obs_time"]["value"]
            obs_result = r["obs_result"]["value"]

            geom = shapely.wkt.loads(geom_wkt)
            feature = geojson.Feature(geometry=geom, properties={"observation_time": obs_time, "observation_result": obs_result})
            features.append(feature)

        feature_collection = {"type": "FeatureCollection", "features": features}
        
        return feature_collection

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def json_to_dataframe(data):
    """This function convert the results of a sparql query to a dataframe"""

    # Check if the "bindings" key exists in the JSON
    if "results" in data and "bindings" in data["results"]:
        # Extract the "bindings" part from the JSON
        bindings = data["results"]["bindings"]
        # Create an empty list to store the data in a structured format
        formatted_data = []

        for entry in bindings:
            # Create a dictionary to store the data for each entry
            entry_data = {}
            
            # Iterate through the entry's fields
            for field_name, field_data in entry.items():
                entry_data[field_name] = field_data.get("value")

            formatted_data.append(entry_data)

        # Create a pandas DataFrame from the formatted data
        df = pd.DataFrame(formatted_data)
        #df.drop_duplicates(inplace=True)
        return df
    else:
        print("Invalid JSON format. Unable to convert to DataFrame.")
        return None


if __name__ == "__main__":

    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX gadm: <http://example.com/ontologies/gadm#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?obs_time ?obs_result ?foi_geom
    WHERE {
        {
            SELECT ?foi_ent ?gadm_name
            WHERE {
                ?foi_ent a sosa:FeatureOfInterest ;
                    geo:intersects ?gadm_ent .
                ?gadm_ent a gadm:AdministrativeUnit ;
                    gadm:hasName 'Geltendorf' ;
            } 
        }

        ?obs_ent a sosa:Observation ;
            sosa:hasSimpleResult ?obs_result ; 
            sosa:resultTime ?obs_time ;
            sosa:hasFeatureOfInterest ?foi_ent ;
            sosa:observedProperty ?obs_prop_ent .
        ?obs_prop_ent a sosa:ObservableProperty ;
            rdfs:label 'PM10' .
        ?foi_ent geo:hasGeometry ?foi_geom_ent .
        ?foi_geom_ent geo:asWKT ?foi_geom .


        FILTER (YEAR(?obs_time) = 2020 && MONTH(?obs_time) = 1)
        FILTER (?obs_result > 40)
    }
    """

    # query strabon endpoint
    results = query_sparql_endpoint(query)

    # create geojson if possible
    cams_data_geojson = convert_query_output_to_geojson(results)

    # print geojson
    print(cams_data_geojson)



    
