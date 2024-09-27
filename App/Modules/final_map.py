import folium
import numpy as np
from .wind import get_wind_map
from .solar import get_radiation_map

def create_combined_renewable_energy_map(address: str, scale: int = 50):
    # Get wind and solar data
    wind_data = get_wind_map(address, scale)
    solar_data = get_radiation_map(address, scale)
    
    if isinstance(wind_data, tuple) and isinstance(solar_data, tuple):
        wind_file, wind_lats, wind_lons, wind_speeds, wind_directions = wind_data
        solar_file, solar_lats, solar_lons, radiation_levels = solar_data
        
        # Calculate the center of the map
        center_lat = (np.min(wind_lats) + np.max(wind_lats)) / 2
        center_lon = (np.min(wind_lons) + np.max(wind_lons)) / 2
        
        # Create a map centered on the location
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add wind data
        wind_threshold = np.percentile(wind_speeds, 80)  # Top 20% of wind speeds
        for lat, lon, speed in zip(wind_lats.flatten(), wind_lons.flatten(), wind_speeds.flatten()):
            if speed >= wind_threshold:
                folium.Marker(
                    [lat, lon],
                    icon=folium.DivIcon(html='<div style="font-size: 24px;">🎐</div>', class_name='wind-icon'),
                    tooltip=f"Potential Wind Farm Location"
                ).add_to(m)
        
        # Add solar farm markers for top 20% radiation levels
        solar_threshold = np.percentile(radiation_levels, 80)
        for lat, lon, rad in zip(solar_lats, solar_lons, radiation_levels):
            if rad >= solar_threshold:
                folium.Marker(
                    [lat, lon],
                    icon=folium.DivIcon(html='<div style="font-size: 24px;">☀️</div>', class_name='solar-icon'),
                    tooltip=f"Potential Solar Farm Location"
                ).add_to(m)
        
        # Add a legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 250px; 
        border:2px solid grey; z-index:9999; font-size:14px; background-color:white;">
            <p style="margin: 5px;"><span style="font-size: 24px;">🎐</span> Potential Wind Farm Location</p>
            <p style="margin: 5px;"><span style="font-size: 24px;">☀️</span> Potential Solar Farm Location</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save the map
        map_file = f'tmp/{address}_combined_renewable_energy_map.html'
        m.save(map_file)
        return map_file
    else:
        return "Error: Could not retrieve wind or solar data"
