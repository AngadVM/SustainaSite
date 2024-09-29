import folium
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point

# Assume we have these modules for getting wind and solar data
from .wind import get_wind_map
from .solar import get_radiation_map
from .landuse import get_land_use_map

def get_land_use_at_point(gdf, lat, lon):
    """Get the land use type at a specific point."""
    point = Point(lon, lat)
    for idx, row in gdf.iterrows():
        if row['geometry'].contains(point):
            return row.get('landuse', 'unknown')
    return 'unknown'

def is_developable(land_use):
    """Check if the land use type is suitable for renewable energy development."""
    restricted_zones = ['residential', 'commercial', 'agricultural', 'forest']
    return land_use not in restricted_zones

def train_site_classifier(data, labels):
    """Train a Random Forest classifier to identify suitable sites."""
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    print(f"Model accuracy: {clf.score(X_test_scaled, y_test)}")
    
    return clf, scaler

def predict_suitable_sites(clf, scaler, features):
    """Use the trained classifier to predict suitable sites."""
    features_scaled = scaler.transform(features)
    return clf.predict_proba(features_scaled)[:, 1]  # Probability of positive class

def create_ml_renewable_energy_map(address: str, scale: int = 50):
    # Get wind and solar data
    wind_data = get_wind_map(address, scale)
    solar_data = get_radiation_map(address, scale)
    
    # Get land use data
    land_use_map, land_use_gdf = get_land_use_map(address, scale)
    
    if isinstance(wind_data, tuple) and isinstance(solar_data, tuple):
        wind_file, wind_lats, wind_lons, wind_speeds, wind_directions = wind_data
        solar_file, solar_lats, solar_lons, radiation_levels = solar_data
        
        # Combine all features
        features = []
        labels = []
        valid_lats = []
        valid_lons = []
        
        for lat, lon, wind_speed, wind_direction, radiation in zip(
            wind_lats.flatten(), wind_lons.flatten(), 
            wind_speeds.flatten(), wind_directions.flatten(), 
            radiation_levels.flatten()
        ):
            land_use = get_land_use_at_point(land_use_gdf, lat, lon)
            if is_developable(land_use):
                features.append([wind_speed, wind_direction, radiation])
                valid_lats.append(lat)
                valid_lons.append(lon)
                
                # In practice, you would use real labels here
                # This is just a placeholder
                labels.append(1 if (wind_speed > np.mean(wind_speeds) or radiation > np.mean(radiation_levels)) else 0)
        
        features = np.array(features)
        labels = np.array(labels)
        
        # Train the classifier
        clf, scaler = train_site_classifier(features, labels)
        
        # Predict suitability for all sites
        suitability_scores = predict_suitable_sites(clf, scaler, features)
        
        # Create a map centered on the location
        center_lat = (np.min(wind_lats) + np.max(wind_lats)) / 2
        center_lon = (np.min(wind_lons) + np.max(wind_lons)) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add markers for highly suitable locations
        threshold = np.percentile(suitability_scores, 90)  # Top 10% of suitable locations
        for lat, lon, score, wind_speed, radiation in zip(valid_lats, valid_lons, suitability_scores, features[:, 0], features[:, 2]):
            if score >= threshold:
                icon_html = '<div style="font-size: 24px;">🎐</div>' if wind_speed > np.mean(features[:, 0]) else '<div style="font-size: 24px;">☀️</div>'
                folium.Marker(
                    [lat, lon],
                    icon=folium.DivIcon(html=icon_html),
                    tooltip=f"Suitability Score: {score:.2f}"
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
        map_file = f'tmp/{address}_ml_renewable_energy_map.html'
        m.save(map_file)
        
        # Save the trained model for future use
        joblib.dump(clf, 'renewable_energy_site_classifier.joblib')
        joblib.dump(scaler, 'feature_scaler.joblib')
        
        return map_file
    else:
        return "Error: Could not retrieve wind or solar data"
