from .coords import geocode
import folium

def get_map(address: str, scale: int = 50):
    coords = geocode(address, scale)
    
    if isinstance(coords, list):
        min_lat, max_lat, min_lon, max_lon = coords
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        # Create a map centered on the location
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

        # Add a marker for the center point
        folium.Marker([center_lat, center_lon], popup=address).add_to(m)

        # Add a rectangle to show the bounding box
        folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]], 
                         fill=True, 
                         fill_color='red', 
                         fill_opacity=0.05).add_to(m)

        # Save the map to an HTML file
        map_file = f'{address}_map.html'
        m.save(map_file)

