from SPARQLWrapper import SPARQLWrapper, JSON
from config import STRABON_SPARQL_ENDPOINT

if __name__ == "__main__":

    # Create a SPARQLWrapper instance with the endpoint URL
    sparql = SPARQLWrapper(STRABON_SPARQL_ENDPOINT)

    # load query
    #path_to_query_file = "/workspaces/aqqa-kg-creation-dev/components/sparql_queries/get_gadm_name_by_location.ttl"
    #with open(path_to_query_file, 'r') as file:
    #    sparql_query = file.read()

    sparql_query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX gadm: <http://example.com/ontologies/gadm#>

    SELECT ?obs_result ?obs_time ?foi_ent
    WHERE {
        {
            SELECT ?foi_ent
            WHERE {
                ?foi_ent a sosa:FeatureOfInterest ;
                    geo:intersects ?gadm_ent .
                ?gadm_ent a gadm:AdministrativeUnit ;
                    gadm:hasName 'Linz' ;
                    gadm:hasNationalLevel 3 ;
            } 
        }

        ?obs_ent a sosa:Observation ;
                sosa:hasSimpleResult ?obs_result ; 
                sosa:resultTime ?obs_time ;
                sosa:hasFeatureOfInterest ?foi_ent ;
                sosa:observedProperty ?obs_prop_ent .
        ?obs_prop_ent a sosa:ObservableProperty ;
            rdfs:label 'CO' .

        FILTER (YEAR(?obs_time) = 2020 && MONTH(?obs_time) = 1)
    } 
    """

    # Set the SPARQL query
    sparql.setQuery(sparql_query)

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    try:
       # Execute the query and get the results
       ret = sparql.queryAndConvert()
       for r in ret["results"]["bindings"]:
          print(r)
    except Exception as e:
        print(e)
    
