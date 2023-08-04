from SPARQLWrapper import SPARQLWrapper, POST, DIGEST

# Endpoint URL to delete data
sparql = SPARQLWrapper("http://64.225.134.139:9999/Strabon/")
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