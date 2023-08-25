from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == "__main__":

    # Set up the endpoint URL
    endpoint_url = "http://64.225.134.139:9999/Strabon/Query"

    # Create a SPARQLWrapper instance with the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)

    # List observations with geometries
    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 

    SELECT ?s ?geom
    WHERE {
        ?s a sosa:Observation ;
           sosa:hasFeatureOfInterest ?foi .
        ?foi geo:hasGeometry ?geom_ent .
        ?geom_ent geo:asWKT ?geom .
    } 
    LIMIT 10
    """

    # List values and timestamps of CO2 for municipality called Neukirchen
    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX gadm: <http://example.com/ontologies/gadm/>

    SELECT ?obs_time ?obs_result
    WHERE {
        ?obs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?foi ;
           sosa:resultTime ?obs_time ;
           sosa:hasSimpleResult ?obs_result .
        ?foi geo:hasGeometry ?geom_ent .
        ?geom_ent geo:asWKT ?geom .
        ?gadm_name a gadm:AdministrativeUnit ;
                   gadm:hasName 'Neurkirchen' ;
                   geo:hasGeometry ?gadm_geom_ent .
        ?gadm_geom_ent geo:asWKT ?gadm_geom .
        FILTER(geof:sfIntersects(?gadm_geom, ?geom)) 
    } 
    LIMIT 10
    """

    # Set the SPARQL query
    sparql.setQuery(query)

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    try:
       # Execute the query and get the results
       ret = sparql.queryAndConvert()
       for r in ret["results"]["bindings"]:
          print(f"{r['obs_time']} {r['obs_result']}")
    except Exception as e:
        print(e)