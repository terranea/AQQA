import requests

# Endpoint URL to delete data
endpoint_url = "http://localhost:9999/Strabon/Store"

# authentication credentials
username = "endpoint"
password = "endpoint"

# SPARQL DELETE query to remove triples or graphs
sparql_delete_query = """
    DELETE
    {
        ?s ?p ?o .
    }
    WHERE
    {
        ?s ?p ?o .
    }
"""

# Set the headers with the content type
headers = {
    "Content-Type": "application/sparql-update"
}

# Make the DELETE request to delete the data
response = requests.delete(endpoint_url, data=sparql_delete_query, headers=headers, auth=(username, password))

# Check the response status
if response.status_code == 200:
    print("Data deleted successfully.")
else:
    print("Error deleting data. Status code:", response.status_code)
    print("Response content:", response.content.decode())