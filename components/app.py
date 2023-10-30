import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from shapely.geometry import shape
from aq_kg_text_interface.openai_text_to_sparql import text_to_sparql
from aq_kg_query.strabon_query_data import query_sparql_endpoint, convert_query_output_to_geojson, json_to_dataframe


def get_geojson_centroid(geojson_data):
    """get centroid (tuple) of geojson geometry"""
    shapely_geometry = shape(geojson_data['features'][0]['geometry'])
    centroid = list(shapely_geometry.centroid.coords)[0]
    centroid = [centroid[1], centroid[0]]
    return centroid

def initialize_state_variables():
    if 'sparql_query' not in st.session_state: 
        st.session_state['sparql_query'] = ""
    if 'query_results' not in st.session_state:
        st.session_state['query_results'] = ""
    if 'query_results_geojson' not in st.session_state:
        st.session_state['query_results_geojson'] = ""
    if 'map_center' not in st.session_state:
        st.session_state['map_center'] = [51.5074, -0.1278]
    
def create_sidebar():
    """create all elements neccessary for sidebar"""

    st.sidebar.title("Sidebar")
    text_input = st.sidebar.text_input("Enter text here")
    convert_button = st.sidebar.button("Convert")
    st.session_state['sparql_query'] = st.sidebar.text_area("Sparql query", value=st.session_state['sparql_query'])
    query_button = st.sidebar.button("Query")

    if convert_button:
        if not text_input:
            st.sidebar.error("There is no text")
        else:
            # convert text to sparql query
            sparql_query = text_to_sparql(text_input)
            st.text("Done")

            if sparql_query[0] == "<" and sparql_query[-1] == ">":
                st.sidebar.error(sparql_query[1:-1])
            else:
                st.session_state['sparql_query'] = sparql_query
                #st.rerun()
    
    # Butto to query the databse
    if query_button:
        if st.session_state['sparql_query'] == "":
            st.sidebar.error("There is no query")
        else:
            # retrieve results from sparql endpoint
            results = query_sparql_endpoint(st.session_state['sparql_query'])
            df_results = json_to_dataframe(results)
            geojson_results = convert_query_output_to_geojson(results)
            st.session_state["query_results"] = df_results
            st.session_state["query_results_geojson"] = geojson_results
            #st.experimental_rerun()


if __name__ == "__main__":

    st.set_page_config(layout="wide")

    initialize_state_variables()

    # create map object
    map_ = folium.Map(location=st.session_state['map_center'], zoom_start=7)

    create_sidebar()

    if st.session_state['query_results_geojson'] != "":

        geojson_layer = folium.GeoJson(
            st.session_state['query_results_geojson'],
            name='GeoJSON Layer',
            style_function=lambda feature: {
                'fillColor': 'blue',
                'fillOpacity': 0.1,
                'color': 'blue',
            },
            highlight_function=lambda x: {'weight': 2, 'color': 'black'},
            tooltip=folium.GeoJsonTooltip(fields=['observation_time', 'observation_result']),
        ).add_to(map_)

        st.session_state['map_center'] = get_geojson_centroid(st.session_state['query_results_geojson']) 

    # create column structure
    col1, col2 = st.columns([1.7, 1.3])

    # create map
    with col1:
        st.markdown('### Map')
        folium.LayerControl().add_to(map_)
        out = st_folium(map_, height=450, width=650)

    # create result table
    with col2:
        if isinstance(st.session_state["query_results"], pd.DataFrame):
            st.dataframe(st.session_state["query_results"])
        else:
            st.dataframe()
    
    pass