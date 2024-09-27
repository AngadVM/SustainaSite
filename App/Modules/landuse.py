import folium
from folium.plugins import MarkerCluster
import osmnx as ox
import geopandas as gpd
from shapely.geometry import box
import matplotlib.colors as mcolors
import tempfile

def get_land_use_map(address: str, scale: int = 50):
    # Use osmnx to geocode the address
    location = ox.geocode(address)
    
    if location:
        latitude, longitude = location[0], location[1]
        radius_deg = scale / 111  # Convert length in km to degrees

        # Define the bounding box
        north, south = latitude + radius_deg, latitude - radius_deg
        east, west = longitude + radius_deg / ox.projection.get_earth_radius_at_latitude(latitude), longitude - radius_deg / ox.projection.get_earth_radius_at_latitude(latitude)

        # Create a GeoDataFrame with the bounding box
        bbox = box(west, south, east, north)
        gdf = gpd.GeoDataFrame({'geometry': [bbox]}, crs='EPSG:4326')

        # Get land use data from OpenStreetMap
        tags = {'landuse': True}
        land_use = ox.geometries_from_bbox(north, south, east, west, tags)

        # Create a color map for different land use types
        land_use_types = land_use['landuse'].unique()
        color_map = {lu: mcolors.rgb2hex(mcolors.hsv_to_rgb((i/len(land_use_types), 0.8, 0.8))) 
                     for i, lu in enumerate(land_use_types)}

        # Create a map centered on the location
        m = folium.Map(location=[latitude, longitude], zoom_start=12)

        # Add land use polygons to the map
        for _, row in land_use.iterrows():
            if row['geometry'].geom_type == 'Polygon':
                folium.Polygon(
                    locations=[(y, x) for x, y in row['geometry'].exterior.coords],
                    color=color_map.get(row['landuse'], 'gray'),
                    fill=True,
                    fillColor=color_map.get(row['landuse'], 'gray'),
                    fillOpacity=0.7,
                    popup=f"Land use: {row['landuse']}"
                ).add_to(m)

        # Add a marker for the center point
        folium.Marker([latitude, longitude], popup=address).add_to(m)

        # Add the bounding box
        folium.GeoJson(gdf).add_to(m)

        # Create a legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 220px; height: 130px; 
        border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
        ">&nbsp; Land Use Types <br>
        '''
        for lu, color in color_map.items():
            legend_html += f'<i class="fa fa-square fa-1x" style="color:{color}"></i> {lu}<br>'
        legend_html += '</div>'
        m.get_root().html.add_child(folium.Element(legend_html))

        # Save the map to a temporary HTML file
        _, temp_html = tempfile.mkstemp(suffix=".html")
        m.save(temp_html)        

    else:
        return "Address not found"

if __name__ == "__main__":
    address = input("Enter an address: ")
    scale = int(input("Enter the scale in km: "))
    result = get_land_use_map(address, scale)
    if isinstance(result, Image.Image):
        result.show()  # This will display the image
    else:
        print(result)  # This will print the error message