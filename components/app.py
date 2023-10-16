import streamlit as st
import folium
from streamlit_folium import st_folium
from aq_kg_text_interface.openai_text_to_sparql import text_to_sparql

# Set the width for the sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create a Streamlit sidebar
st.sidebar.title("Sidebar")
text_input = st.sidebar.text_input("Enter text here")

# Button to commit the action
if st.sidebar.button("Commit"):
    sparql_query = text_to_sparql(text_input)
    st.sidebar.text(sparql_query)

# Create a Folium map
st.title("Interactive Map")
map_ = folium.Map(location=[0, 0], zoom_start=2)

# Render the Folium map in Streamlit
st.markdown('### Map')
folium.LayerControl().add_to(map_)
out = st_folium(map_, height=650, width=650)
