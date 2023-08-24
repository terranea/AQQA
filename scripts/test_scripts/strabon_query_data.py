from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == "__main__":

    # Set up the endpoint URL
    endpoint_url = "http://64.225.134.139:9999/Strabon/Query"

    # Create a SPARQLWrapper instance with the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)

    query =     """   
    PREFIX aqqa: <http://example.com/ontologies/aqqa#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX sf: <http://www.opengis.net/ont/sf#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?var ?unit ?time ?measurement
    WHERE {
            ?s 
                a sosa:Observation ;
                sosa:resultTime ?time ;
                sosa:hasSimpleResult ?measurement ;
                sosa:observedProperty ?obsProp .
            ?obsProp 
                rdfs:label ?var ;
                aqqa:hasUnit ?unit .
    }"""

    query = """
    PREFIX gadm: <http://example.com/ontologies/gadm#> 
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

    SELECT ?name ?lvl
    WHERE {
        ?s a gadm:AdministrativeUnit ;
            gadm:hasName ?name ;
            gadm:hasNationalLevel ?lvl ;
            geo:hasGeometry ?geom_ent .

        ?geom_ent geo:asWKT ?geom .
        
        FILTER (geof:sfContains(?geom, 'POINT(9.729870 48.330776)'^^geo:wktLiteral))
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
          print(f"{r['name']['value']} {r['lvl']['value']}")
    except Exception as e:
        print(e)