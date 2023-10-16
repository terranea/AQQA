import geojson
import json
import shapely.wkt
from SPARQLWrapper import SPARQLWrapper, JSON
from config import STRABON_SPARQL_ENDPOINT


if __name__ == "__main__":

    # Create a SPARQLWrapper instance with the endpoint URL
    sparql = SPARQLWrapper(STRABON_SPARQL_ENDPOINT)

    # Provide a list of CO concentration measurements in Geltendorf during January 2020.
    sparql_query = """
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
                    gadm:hasName 'Oberösterreich' ;
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

    # Set the SPARQL query
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()


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

        with open("/mnt/data/output.geojson", "w") as f:
            json.dump(feature_collection, f, indent=2)

    except Exception as e:
        print(e)
    
