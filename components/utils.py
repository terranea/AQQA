import folium 
from shapely import wkt

def create_folium_map(data, center=[48.15, 14.25], zoom=10):
    """
    Create a Folium map centered around a specific location and add markers based on provided data.

    Args:
        data (list): A list of tuples containing observation results, observation times, and WKT literals.
        center (list): The center of the map in [latitude, longitude] format.
        zoom (int): The initial zoom level of the map.

    Returns:
        folium.Map: A Folium map object with markers added.
    """

    # Create a Folium map centered around the specified location
    m = folium.Map(location=center, zoom_start=zoom)

    # Iterate through the data and add markers to the map
    for obs_result, obs_time, wkt_literal in data:
        # Convert Literal objects to Python types
        obs_result = float(obs_result)
        obs_time = obs_time.value
        geometry = wkt.loads(wkt_literal)

        # Create a GeoJSON representation of the geometry
        geojson = geometry.__geo_interface__

        # Create a GeoJson object and add it to the map
        folium.GeoJson(
            geojson,
            style_function=lambda feature: {
                'fillColor': 'green',  # Change the fill color as needed
                'fillOpacity': 0.5,
                'color': 'black',  # Change the border color as needed
                'weight': 2,
            },
            popup=f"Observation Result: {obs_result}<br>Observation Time: {obs_time}"
        ).add_to(m)

    return m

# Example usage:
# data = [(12.34, datetime.datetime(2023, 9, 20, 12, 0), 'POINT (14.3 48.2)'), ...]
# map = create_folium_map(data)
# map.save('/mnt/data/maps/map.html')