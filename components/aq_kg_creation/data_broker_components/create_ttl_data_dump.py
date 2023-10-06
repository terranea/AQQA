from rdflib import Graph
import os

OUTPUT_PATH = "/mnt/data/AQQA_graph/AQQA_KG.ttl"
PATH_GADM_AUT_POP = "/mnt/data/GADM/RDF/gadm_AUT_RDF_population.ttl"
PATH_GADM_DEU_POP = "/mnt/data/GADM/RDF/gadm_DEU_RDF_population.ttl"
PATH_OBSERVABLE_PROPERTIES = "/mnt/data/AQ_observable_properties.ttl"
PATH_CAMS_REFERENCE_RASTER = "/mnt/data/CAMS/RDF/CAMS_reference_grid_gadm_connections.ttl"
ROOT_PATH_CAMS_OBSERVATIONS = '/mnt/data/CAMS/RDF/observations/'


if __main__ == "__name__":

    graph = Graph()

    # insert data into graph
    graph.parse(PATH_GADM_AUT_POP, format='ttl')
    graph.parse(PATH_GADM_DEU_POP, format='ttl')
    graph.parse(PATH_OBSERVABLE_PROPERTIES, format='ttl')
    graph.parse(PATH_CAMS_REFERENCE_RASTER, format='ttl')

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(ROOT_PATH_CAMS_OBSERVATIONS):
        for file in files:
            # Construct the full path to the file
            file_path = os.path.join(root, file)
            
            # Now you can work with the file_path
            # For example, you can print it or perform some action with the file
            print(file_path)
            graph.parse(file_path, format='ttl')
    
    # Serialize the RDF graph to Turtle and save it to the file
    graph.serialize(destination=OUTPUT_PATH, format='turtle')

