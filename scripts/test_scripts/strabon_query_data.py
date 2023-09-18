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

     # List values and timestamps of CO2 for location in Linz (coordinate given)
    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX gadm: <http://example.com/ontologies/gadm#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?obs_result ?obs_time
    WHERE {
        ?obs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?foi_ent ;
           sosa:resultTime ?obs_time ;
           sosa:hasSimpleResult ?obs_result ;
           sosa:observedProperty ?obs_prop_ent .
        ?obs_prop_ent a sosa:ObservableProperty ;
           rdfs:label 'PM2.5' .
        ?foi_ent geo:hasGeometry ?foi_geom_ent .
        ?foi_geom_ent geo:asWKT ?foi_geom .

        FILTER (geof:sfWithin('''<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT (14.36343 48.37428)'''^^geo:wktLiteral, ?foi_geom))
    } 
    LIMIT 100
    """

    # List name of municipality of a given location
    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX gadm: <http://example.com/ontologies/gadm#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?gadm_name
    WHERE {
        ?gadm_ent a gadm:AdministrativeUnit ;
                   gadm:hasName ?gadm_name ;
                   gadm:hasNationalLevel 4 ;
                   geo:hasGeometry ?gadm_geom_ent .
        ?gadm_geom_ent geo:asWKT ?gadm_geom .

        FILTER (geof:sfWithin('''<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT (11.03388 48.11644)'''^^geo:wktLiteral, ?gadm_geom))
    } 
    LIMIT 100
    """

    # Combine above two queries - get PM25 measurements of Geltendorf
    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX gadm: <http://example.com/ontologies/gadm#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?obs_time ?obs_result
    WHERE {
        ?obs a sosa:Observation ;
           sosa:hasFeatureOfInterest ?foi_ent ;
           sosa:resultTime ?obs_time ;
           sosa:hasSimpleResult ?obs_result ;
           sosa:observedProperty ?obs_prop_ent .
        ?obs_prop_ent a sosa:ObservableProperty ;
           rdfs:label 'PM2.5' .
        ?foi_ent geo:hasGeometry ?foi_geom_ent .
        ?foi_geom_ent geo:asWKT ?foi_geom .
        ?gadm_ent a gadm:AdministrativeUnit ;
            gadm:hasName 'Geltendorf' ;
            gadm:hasNationalLevel 4 ;
            geo:hasGeometry ?gadm_geom_ent .
        ?gadm_geom_ent geo:asWKT ?gadm_geom .
        FILTER(geof:sfIntersects(?gadm_geom, ?foi_geom)) 
    } 
    LIMIT 100
    """

    # Set the SPARQL query
    sparql.setQuery(query)

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    try:
       # Execute the query and get the results
       ret = sparql.queryAndConvert()
       for r in ret["results"]["bindings"]:
          print(r)
    except Exception as e:
        print(e)