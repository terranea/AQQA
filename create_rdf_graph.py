from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
import matplotlib.pyplot as plt
import networkx as nx
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from rdflib.plugins.sparql import prepareQuery

# Define the namespaces
aqqa = Namespace("http://example.com/ontologies/aqqa#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
sosa = Namespace("http://www.w3.org/ns/sosa/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
geo = Namespace("http://www.opengis.net/ont/geosparql#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Create a graph
g = Graph()
g.bind("aqqa", aqqa)


# Ingest the RDF data
g.add((aqqa.PM25, RDF.type, sosa.ObservableProperty))
g.add((aqqa.PM25, rdfs.label, Literal('PM 2.5')))
g.add((aqqa.PM25, aqqa.hasUnit, Literal('µg m-3')))
g.add((aqqa.PM25, rdfs.comment, Literal('24 hour mean value of CAMS PM2.5 reanalysis data at surface')))

g.add((aqqa.Cell_X, RDF.type, sosa.FeatureOfInterest))
g.add((aqqa.Cell_X, aqqa.hasID, Literal(1, datatype=XSD.integer)))
g.add((aqqa.Cell_X, geo.hasGeometry, aqqa.GeomCell_X))

g.add((aqqa.GeomCell_X, RDF.type, geo.Geometry))
g.add((aqqa.GeomCell_X, geo.asWKT, Literal("POINT (-73.935242 40.730610)", datatype=geo.wktLiteral)))

g.add((aqqa.CellID_X_timestamp_1000_var_PM25, RDF.type, sosa.Observation))
g.add((aqqa.CellID_X_timestamp_1000_var_PM25, sosa.observedProperty, aqqa.PM25))
g.add((aqqa.CellID_X_timestamp_1000_var_PM25, sosa.hasSimpleResult, Literal(14.4)))
g.add((aqqa.CellID_X_timestamp_1000_var_PM25, sosa.resultTime, Literal("2023-07-20T15:30:00", datatype=XSD.dateTime)))


# Print the graph to see the ingested data (optional)
#print(g.serialize(format="turtle"))

# Save the graph to a file (optional)
#g.serialize(destination="output.rdf", format="turtle")

# Visualize the graph
"""
g_nx = rdflib_to_networkx_multidigraph(g)
pos = nx.spring_layout(g_nx)
nx.draw(g_nx, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=8, font_weight='bold', arrowsize=12)
plt.show()
"""

# Execute Query 1
query1 = prepareQuery(
    """SELECT ?observation ?label ?unit ?resultTime
       WHERE {
         ?observableProperty rdf:type sosa:ObservableProperty ;
                             rdfs:label "PM 2.5" ;
                             aqqa:hasUnit ?unit .
  
         ?observation sosa:observedProperty ?observableProperty ;
                      rdfs:label ?label ;
                      sosa:resultTime ?resultTime .
       }"""
)

results1 = g.query(query1)
print("Query 1 Results:")
for row in results1:
    print(f"Observation: {row['observation']}, Label: {row['label']}, Unit: {row['unit']}, Result Time: {row['resultTime']}")





