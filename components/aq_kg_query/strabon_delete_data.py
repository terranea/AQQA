from SPARQLWrapper import SPARQLWrapper, POST, DIGEST
from config import STRABON_SPARQL_ENDPOINT

# Endpoint URL to delete data
sparql = SPARQLWrapper(STRABON_SPARQL_ENDPOINT)
sparql.setHTTPAuth(DIGEST)
sparql.setCredentials("endpoint", "endpoint")
sparql.setMethod(POST)

# SPARQL DELETE query to remove triples or graphs
sparql.setQuery(
    """
        DELETE WHERE {?s ?p ?o} 
    """
)

results = sparql.query()