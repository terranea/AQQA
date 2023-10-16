import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from aq_kg_text_interface.openai_text_to_sparql import text_to_sparql
from aq_kg_query.strabon_query_data import query_sparql_endpoint, convert_query_output_to_geojson, json_to_dataframe

# set screen wide
st.set_page_config(layout="wide")

# initialize state variables
if 'sparql_query' not in st.session_state: 
    st.session_state['sparql_query'] = ""
if 'query_results' not in st.session_state:
    st.session_state['query_results'] = ""
if 'query_results_geojson' not in st.session_state:
    st.session_state['query_results_geojson'] = ""

# create map object
map_ = folium.Map(location=[51.5074, -0.1278], zoom_start=7)

# Create a sidebar elements
st.sidebar.title("Sidebar")
text_input = st.sidebar.text_input("Enter text here")
convert_button = st.sidebar.button("Convert")
st.session_state['sparql_query'] = st.sidebar.text_area("Sparql query", value=st.session_state['sparql_query'])
query_button = st.sidebar.button("Query")

# Split main page into two columes
col1, col2 = st.columns([2, 1])

# Map Column
with col1:
    st.header("Map")
    folium.LayerControl().add_to(map_)
    out = st_folium(map_, height=650, width=650)

# Result Column
with col2:
    st.header("Results")
    if isinstance(st.session_state["query_results"], pd.DataFrame):
        st.dataframe(st.session_state["query_results"])
    else:
        st.dataframe()

# Button to convert text to sparql query
if convert_button:
    if not text_input:
        st.sidebar.error("There is no text")
    else:
        # convert text to sparql query
        sparql_query = text_to_sparql(text_input)
        st.session_state['sparql_query'] = sparql_query
        st.experimental_rerun()

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

        folium.GeoJson(st.session_state["query_results_geojson"], name="query_results").add_to(map_)
        folium.Marker(location=[51.5074, -0.1278], popup="London").add_to(map_)

        st.experimental_rerun()



