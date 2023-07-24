from SPARQLWrapper import SPARQLWrapper, JSON

if __name__ == "__main__":

    # Set up the endpoint URL
    endpoint_url = "http://localhost:9999/Strabon/Query"

    # Create a SPARQLWrapper instance with the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)

    # Set the SPARQL query
    sparql.setQuery(
    """   
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
    )

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    try:
       # Execute the query and get the results
       ret = sparql.queryAndConvert()
       for r in ret["results"]["bindings"]:
          print(f"{r['time']['value']} {r['measurement']['value']} {r['unit']['value']} {r['var']['value']}")
    except Exception as e:
        print(e)