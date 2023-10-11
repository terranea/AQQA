from SPARQLWrapper import SPARQLWrapper, JSON
from config import STRABON_SPARQL_ENDPOINT

if __name__ == "__main__":

    # Create a SPARQLWrapper instance with the endpoint URL
    sparql = SPARQLWrapper(STRABON_SPARQL_ENDPOINT)

    # load query
    path_to_query_file = "/workspaces/aqqa-kg-creation-dev/components/sparql_queries/get_gadm_name_by_location.ttl"
    with open(path_to_query_file, 'r') as file:
        sparql_query = file.read()


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
    
