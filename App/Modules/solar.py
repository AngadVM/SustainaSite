import folium
from folium.plugins import HeatMap
import numpy as np
from .coords import geocode

def get_radiation_map(address: str, scale: int = 50):
    coords = geocode(address, scale)
    if isinstance(coords, list):
        min_lat, max_lat, min_lon, max_lon = coords
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        # Create a map centered on the location
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True)

        # Generate sample data for radiation levels
        # In a real-world scenario, you would fetch this data from a reliable source
        num_points = 1000
        lats = np.random.uniform(min_lat, max_lat, num_points)
        lons = np.random.uniform(min_lon, max_lon, num_points)
        
        # Simulate radiation data (replace this with actual data in a real scenario)
        # Values are in kWh/m^2/year, typical range for solar radiation
        radiation_levels = np.random.uniform(800, 2200, num_points)

        # Create data for heatmap
        heat_data = [[lat, lon, rad] for lat, lon, rad in zip(lats, lons, radiation_levels)]

        # Add heatmap to the map
        HeatMap(heat_data, 
                min_opacity=0.2,
                max_val=max(radiation_levels),
                radius=15, 
                blur=10, 
                max_zoom=1,
                gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'},
        ).add_to(m)

        # Add a rectangle to show the bounding box
        folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]],
                         fill=False,
                         color='black',
                         weight=2).add_to(m)

        # Add a color scale legend
        colormap = folium.LinearColormap(
            colors=['blue', 'lime', 'yellow', 'red'],
            vmin=min(radiation_levels),
            vmax=max(radiation_levels),
            caption='Average Annual Solar Radiation (kWh/m^2/year)'
        )
        colormap.add_to(m)

        # Save the map to an HTML file
        map_file = f'tmp/{address}_radiation_map.html'
        m.save(map_file)
        return map_file, lats, lons, radiation_levels
    else:
        return coords  # This will be "Address not documented" if geocoding failed

if __name__ == "__main__":
    address = "Phoenix, AZ"
    map_file = get_radiation_map(address, scale=10)
    print(f"Radiation map saved as: {map_file}")