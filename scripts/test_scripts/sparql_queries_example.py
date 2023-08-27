     # List names of 
    query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
    PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
    PREFIX gadm: <http://example.com/ontologies/gadm#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?gadm_name
    WHERE {
        ?gadm_ent a gadm:AdministrativeUnit ;
                   gadm:hasName ?gadm_name ;
                   gadm:hasNationalLevel 4 ;
                   geo:hasGeometry ?gadm_geom_ent .
        ?gadm_geom_ent geo:asWKT ?gadm_geom .

        FILTER (geof:sfWithin('''<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT (14.7038 48.6663)'''^^geo:wktLiteral, ?gadm_geom))
    } 
    LIMIT 100
    """