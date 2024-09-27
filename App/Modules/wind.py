import folium
from folium.plugins import FloatImage
import numpy as np
from .coords import geocode
import math

def get_wind_map(address: str, scale: int = 50):
    coords = geocode(address, scale)
    if isinstance(coords, list):
        min_lat, max_lat, min_lon, max_lon = coords
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        # Create a map centered on the location
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10, control_scale=True)

        # Generate sample data for wind speed and direction
        # In a real-world scenario, you would fetch this data from a reliable source
        num_points = 20
        lats = np.linspace(min_lat, max_lat, num_points)
        lons = np.linspace(min_lon, max_lon, num_points)
        
        # Simulate wind data (replace this with actual data in a real scenario)
        # Wind speed in m/s, direction in degrees (0-360, where 0 is North)
        wind_speeds = np.random.uniform(0, 20, (num_points, num_points))
        wind_directions = np.random.uniform(0, 360, (num_points, num_points))

        # Function to create arrow symbol
        def create_arrow(direction, speed, color):
            return f'''
                <svg width="50" height="50">
                    <defs>
                        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                            <polygon points="0 0, 10 3.5, 0 7" fill="{color}" />
                        </marker>
                    </defs>
                    <line x1="25" y1="25" x2="{25 + 20 * math.sin(math.radians(direction))}" 
                          y2="{25 - 20 * math.cos(math.radians(direction))}" 
                          stroke="{color}" stroke-width="{1 + speed/5}" 
                          marker-end="url(#arrowhead)" />
                </svg>
            '''

        # Blue color scale for wind speed
        def get_color(speed):
            if speed < 5:
                return '#E6F3FF'  # Very light blue
            elif speed < 10:
                return '#99CCFF'  # Light blue
            elif speed < 15:
                return '#3399FF'  # Medium blue
            else:
                return '#0066CC'  # Dark blue

        # Add wind arrows to the map
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                speed = wind_speeds[i, j]
                direction = wind_directions[i, j]
                color = get_color(speed)
                arrow_html = create_arrow(direction, speed, color)
                folium.Marker(
                    [lat, lon],
                    icon=folium.DivIcon(html=arrow_html)
                ).add_to(m)

        # Add a rectangle to show the bounding box
        folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]],
                         fill=False,
                         color='black',
                         weight=2).add_to(m)

        # Add a legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; 
        border:2px solid grey; z-index:9999; font-size:14px; background-color:white;">
            <p style="margin: 5px;">Wind Speed (m/s)</p>
            <p style="margin: 5px;"><span style="color: #E6F3FF;">■</span> 0-5</p>
            <p style="margin: 5px;"><span style="color: #99CCFF;">■</span> 5-10</p>
            <p style="margin: 5px;"><span style="color: #3399FF;">■</span> 10-15</p>
            <p style="margin: 5px;"><span style="color: #0066CC;">■</span> 15+</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        # Save the map to an HTML file
        map_file = f'tmp/{address}_wind_map.html'
        m.save(map_file)
        return map_file, lats, lons, wind_speeds, wind_directions
    else:
        return coords  # This will be "Address not documented" if geocoding failed

if __name__ == "__main__":
    address = "Chicago, IL"
    map_file = get_wind_map(address, scale=10)
    print(f"Wind map saved as: {map_file}")