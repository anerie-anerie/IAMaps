import pandas as pd
import folium

# Step 1: Load the CSV file into a DataFrame
data = pd.read_csv("land.csv")

# Step 2: Filter out rows without land use information
data = data.dropna(subset=["land_use"])

# Step 3: Define land use mapping with correct shorthand codes to full categories and colors
land_use_mapping = {
    "Ra": {"category": "Residential - Apartment", "color": "#FF6347"},
    "Rs": {"category": "Residential - Semi-detached", "color": "#FF4500"},
    "Rd": {"category": "Residential - Detached", "color": "#B22222"},
    "Rt": {"category": "Residential - Townhouse", "color": "#DC143C"},
    "Il": {"category": "Industrial - Light Manufacturing", "color": "yellow"},
    "Cf": {"category": "Commercial - Fast Food", "color": "#ADD8E6"},
    "Cp": {"category": "Commercial - Personal Services", "color": "#4682B4"},
    "Cm": {"category": "Commercial - Market", "color": "#5F9EA0"},
    "Cs": {"category": "Commercial - Specialty Shop", "color": "#1E90FF"},
    "Co": {"category": "Commercial - Office", "color": "#00BFFF"},
    "Cv": {"category": "Commercial - Vacant", "color": "#87CEEB"},
    "Eh": {"category": "Entertainment - Hotel", "color": "#D8BFD8"},
    "Ec": {"category": "Entertainment - Cinema", "color": "#8A2BE2"},
    "Eb": {"category": "Entertainment - Bar", "color": "#800080"},
    "Er": {"category": "Entertainment - Restaurant", "color": "#9932CC"},
    "Es": {"category": "Entertainment - Sports Center", "color": "#4B0082"},
    "Pe": {"category": "Public Building - Education", "color": "#FFA500"},
    "Pl": {"category": "Public Building - Library", "color": "#FF8C00"},
    "Pc": {"category": "Public Building - Place of Worship", "color": "#FF7F50"},
    "Op": {"category": "Open Space - Park", "color": "#32CD32"},
    "Os": {"category": "Open Space - Sports Field", "color": "#228B22"},
    "Ou": {"category": "Open Space - Unused Land", "color": "#006400"},
    "Od": {"category": "Open Space - Derelict Building", "color": "#2E8B57"},
    "Tb": {"category": "Transport - Bus Stop", "color": "#8B4513"},
    "Tc": {"category": "Transport - Car Park", "color": "#A52A2A"},
    "Sf": {"category": "Services - Financial", "color": "#00008B"},
    "Sm": {"category": "Services - Medical", "color": "#000080"},
    "Sb": {"category": "Services - Business", "color": "#191970"},
}

# Step 4: Create a map centered around an average location
average_lat = data['latitude'].mean()
average_lon = data['longitude'].mean()
m = folium.Map(location=[average_lat, average_lon], zoom_start=16)

# Step 5: Track how many times a coordinate appears with different land uses
coord_counts = {}

# Function to apply an offset based on index in land_use_codes list
def apply_offset(latitude, longitude, index, total_codes, offset=0.0001):
    # If the index is in the first half, apply negative offset (shift left)
    # If the index is in the second half, apply positive offset (shift right)
    if index < total_codes / 2:
        offset_value = -((index + 1) * offset)  # Shift left
    else:
        offset_value = (index - total_codes // 2) * offset  # Shift right
    
    new_lat = latitude  # No change to latitude
    new_lon = longitude + offset_value  # Apply offset to longitude
    return new_lat, new_lon

# Step 6: Add the land use data to the map
for index, row in data.iterrows():
    land_use = row['land_use']
    latitude = row['latitude']
    longitude = row['longitude']
    
    # Clean and split multi-code land use entries (e.g., 'Er, Ec')
    land_use_codes = [code.strip() for code in land_use.split(',')]  # Remove extra spaces
    
    # Process each land use code and add a marker
    total_codes = len(land_use_codes)
    
    for i, code in enumerate(land_use_codes):
        if code in land_use_mapping:
            category = land_use_mapping[code]["category"]
            color = land_use_mapping[code]["color"]
            
            # Apply offset to the coordinates based on the index
            adjusted_lat, adjusted_lon = apply_offset(latitude, longitude, i, total_codes)
            
            # Add a CircleMarker for each land use code
            folium.CircleMarker(
                location=[adjusted_lat, adjusted_lon],
                radius=18,
                color="black",
                fill=True,
                fill_color=color,
                fill_opacity=1.0,
                popup=f"Land Use: {category}"
            ).add_to(m)
        else:
            print(f"Unknown land use code: {code}")

# Special coordinates (you can change this as needed)
special_lat = 45.37671213
special_lon = -75.70777173

# Add a Marker at the special coordinates with a popup message
folium.Marker(
    location=[special_lat, special_lon],
    popup="Special Location: -75.70777173, 45.37671213",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)


# Step 7: Add a custom legend to the map (same as before)
legend_html = """
    <div style="position: fixed; bottom: 10vh; left: 5vw; width: 17vw; height: 76vh; background-color: white; z-index: 9999; border:0.5vw black; padding: 1vw; font-size: 0.8vw;">
        <b>Land Use Legend</b><br>
        <div style="background-color: #FF6347; width: 20px; height: 20px; float: left;"></div> Residential (Apartment)<br>
        <div style="background-color: #FF4500; width: 20px; height: 20px; float: left;"></div> Residential (Semi-detached)<br>
        <div style="background-color: #B22222; width: 20px; height: 20px; float: left;"></div> Residential (Detached)<br>
        <div style="background-color: #DC143C; width: 20px; height: 20px; float: left;"></div> Residential (Townhouse)<br><br>
        <div style="background-color: #ADD8E6; width: 20px; height: 20px; float: left;"></div> Commercial (Fast Food)<br>
        <div style="background-color: #4682B4; width: 20px; height: 20px; float: left;"></div> Commercial (Personal Services)<br>
        <div style="background-color: #1E90FF; width: 20px; height: 20px; float: left;"></div> Commercial (Specialty Shop)<br><br>
        <div style="background-color: #D8BFD8; width: 20px; height: 20px; float: left;"></div> Entertainment (Hotel)<br>
        <div style="background-color: #8A2BE2; width: 20px; height: 20px; float: left;"></div> Entertainment (Cinema)<br>
        <div style="background-color: #800080; width: 20px; height: 20px; float: left;"></div> Entertainment (Bar)<br>
        <div style="background-color: #9932CC; width: 20px; height: 20px; float: left;"></div> Entertainment (Restaurant)<br><br>
        <div style="background-color: #FFA500; width: 20px; height: 20px; float: left;"></div> Public Building (Education)<br>
        <div style="background-color: #FF8C00; width: 20px; height: 20px; float: left;"></div> Public Building (Library)<br>
        <div style="background-color: #FF7F50; width: 20px; height: 20px; float: left;"></div> Public Building (Place of Worship)<br><br>
        <div style="background-color: #32CD32; width: 20px; height: 20px; float: left;"></div> Open Space (Park)<br>
        <div style="background-color: #228B22; width: 20px; height: 20px; float: left;"></div> Open Space (Sports Field)<br>
        <div style="background-color: #006400; width: 20px; height: 20px; float: left;"></div> Open Space (Unused Land)<br><br>
        <div style="background-color: #8B4513; width: 20px; height: 20px; float: left;"></div> Transport (Bus Stop)<br>
        <div style="background-color: #A52A2A; width: 20px; height: 20px; float: left;"></div> Transport (Car Park)<br><br>
        <div style="background-color: #00008B; width: 20px; height: 20px; float: left;"></div> Services (Financial)<br>
        <div style="background-color: #000080; width: 20px; height: 20px; float: left;"></div> Services (Medical)<br>
        <div style="background-color: #191970; width: 20px; height: 20px; float: left;"></div> Services (Business)<br>
    </div>
"""

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

# Step 8: Save the map to an HTML file
m.save("land_use_map_with_offsets.html")

print("Map has been saved to 'land_use_map.html'.")
