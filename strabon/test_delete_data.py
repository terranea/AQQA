from SPARQLWrapper import SPARQLWrapper, POST, DIGEST

# Endpoint URL to delete data
sparql = SPARQLWrapper("http://localhost:9999/Strabon/Query")
sparql.setHTTPAuth(DIGEST)
sparql.setCredentials("endpoint", "endpoint")
sparql.setMethod(POST)

# SPARQL DELETE query to remove triples or graphs
sparql.setQuery(
    """
        DELETE {
            ?s ?p ?o .
        } WHERE {
            ?s ?p ?o .
        }
    """
)

results = sparql.query()
print(results.response.read())