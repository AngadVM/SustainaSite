import folium
import osmnx as ox
from .coords import geocode

def get_land_use_map(address: str, scale: int = 50):
    coords = geocode(address, scale)
    
    if isinstance(coords, list):
        min_lat, max_lat, min_lon, max_lon = coords
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        # Create a map centered on the location
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Fetch land use data from OpenStreetMap
        north, south, east, west = max_lat, min_lat, max_lon, min_lon
        gdf = ox.geometries_from_bbox(north, south, east, west, tags={'landuse': True})

        # Define color scheme for different land use types
        color_map = {
            'residential': 'red',
            'commercial': 'blue',
            'industrial': 'purple',
            'agricultural': 'green',
            'forest': 'darkgreen',
            'grass': 'lightgreen',
            'water': 'lightblue'
        }

        # Add land use polygons to the map
        for idx, row in gdf.iterrows():
            if 'landuse' in row:
                landuse = row['landuse']
                color = color_map.get(landuse, 'gray')  # Default to gray for unknown land use types
                folium.GeoJson(
                    row['geometry'],
                    style_function=lambda x, color=color: {
                        'fillColor': color,
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': 0.7
                    },
                    tooltip=landuse
                ).add_to(m)


        # Add a rectangle to show the bounding box
        folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]], 
                         fill=False, 
                         color='black',
                         weight=2).add_to(m)

        # Add a legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 120px; height: 180px; 
        border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
        ">&nbsp; Land Use Types<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:red"></i> Residential<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:blue"></i> Commercial<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:purple"></i> Industrial<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:green"></i> Agricultural<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:darkgreen"></i> Forest<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:lightgreen"></i> Grass<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:lightblue"></i> Water<br>
        &nbsp; <i class="fa fa-square fa-1x" style="color:gray"></i> Other
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        # Save the map to an HTML file
        map_file = f'tmp/{address}_land_use_map.html'
        m.save(map_file)

        return map_file, gdf
    else:
        return coords  # This will be "Address not documented" if geocoding failed
    
if __name__ == "__main__":

    address = "New York, NY"
    map_file = get_land_use_map(address, scale=10)
    print(f"Land use map saved as: {map_file}")