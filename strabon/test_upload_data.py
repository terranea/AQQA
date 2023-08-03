import requests

# Endpoint URL to upload data
endpoint_url = "http://localhost:9999/Strabon/Query"

# authentication credentials
username = "endpoint"
password = "endpoint"

# RDF data in Turtle format
query = """
PREFIX aqqa: <http://example.com/ontologies/aqqa#> .
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
PREFIX sosa: <http://www.w3.org/ns/sosa/> .
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
PREFIX geo: <http://www.opengis.net/ont/geosparql#> .
PREFIX sf: <http://www.opengis.net/ont/sf#> .
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> .

INSERT DATA {
    aqqa:PM25 
        rdf:type sosa:ObservableProperty ;
        rdfs:label "PM 2.5" ;
        aqqa:hasUnit "µg m-3" ;
        rdfs:comment "24 hour mean value of CAMS PM2.5 reanalysis data at surface" .

    aqqa:Cell_X
        rdf:type sosa:FeatureOfInterest ;
        aqqa:hasID 1 ;
        geo:hasGeometry aqqa:GeomCell_X .

    aqqa:GeomCell_X
        rdf:type sf:Geometry ;
        geo:asWKT "POINT (-73.935242 40.730610)" .

    aqqa:CellID_X_timestamp_1000_var_PM25
        rdf:type sosa:Observation ;
        sosa:observedProperty aqqa:PM25 ;
        sosa:hasSimpleResult 14.4 ;
        sosa:resultTime "2023-07-20T15:30:00"^^xsd:dateTime .
}
"""

# Set the headers with the content type
headers = {
    "Content-Type": "application/sparql-query"
}

# Make the POST request to upload the data
response = requests.post(endpoint_url, data=query, headers=headers, auth=(username, password))

# Check the response status
if response.status_code == 200:
    print("Data uploaded successfully.")
else:
    print("Error uploading data. Status code:", response.status_code)
    print("Response content:", response.content.decode())