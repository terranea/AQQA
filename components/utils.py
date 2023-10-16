import geojson
import json
import shapely.wkt
from SPARQLWrapper import SPARQLWrapper, JSON


def sparql_cams_query_output_to_geojson(results: dict, path_to_geojson: str):

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
    
    with open(path_to_geojson, "w") as f:
        json.dump(feature_collection, f, indent=2)

