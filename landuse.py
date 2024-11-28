import pandas as pd
import folium

# Step 1: Load the CSV file into a DataFrame
data = pd.read_csv("land.csv")

# CLEAN THE DATA! DOESNT FIT ALL THE CODE RPORPELRY KIDS MESSED IT UP
# Step 2: Filter out rows without land use information
data = data.dropna(subset=["land_use"])

# Step 3: Define land use mapping with correct shorthand codes to full categories and colors
land_use_mapping = {
    "Ra": {"category": "Residential - Apartment", "color": "blue"},
    "Rs": {"category": "Residential - Semi-detached", "color": "green"},
    "Rd": {"category": "Residential - Detached", "color": "orange"},
    "Rt": {"category": "Residential - Townhouse", "color": "purple"},
    
    "Il": {"category": "Industrial - Light Manufacturing", "color": "lightblue"},
    
    "Cf": {"category": "Commercial - Fast Food", "color": "yellow"},
    "Cp": {"category": "Commercial - Personal Services", "color": "cyan"},
    "Cm": {"category": "Commercial - Market", "color": "brown"},
    "Cs": {"category": "Commercial - Specialty Shop", "color": "red"},
    "Co": {"category": "Commercial - Office", "color": "pink"},
    "Cv": {"category": "Commercial - Vacant", "color": "gray"},
    
    "Eh": {"category": "Entertainment - Hotel", "color": "lightgreen"},
    "Ec": {"category": "Entertainment - Cinema", "color": "lightyellow"},
    "Eb": {"category": "Entertainment - Bar", "color": "black"},
    "Er": {"category": "Entertainment - Restaurant", "color": "lightblue"},
    
    "Pe": {"category": "Public Building - Education", "color": "darkgreen"},
    "Pl": {"category": "Public Building - Library", "color": "darkred"},
    "Pc": {"category": "Public Building - Place of Worship", "color": "darkblue"},
    
    "Op": {"category": "Open Space - Park", "color": "lime"},
    "Os": {"category": "Open Space - Sports Field", "color": "maroon"},
    "Ou": {"category": "Open Space - Unused Land", "color": "teal"},
    "Od": {"category": "Open Space - Derelict Building", "color": "grey"},
    
    "Tb": {"category": "Transport - Bus Stop", "color": "darkgray"},
    "Tc": {"category": "Transport - Car Park", "color": "darkcyan"},
    
    "Sf": {"category": "Services - Financial", "color": "lightgray"},
    "Sm": {"category": "Services - Medical", "color": "navy"},
    "Sb": {"category": "Services - Business", "color": "green"},
}

# Step 4: Create a map centered around an average location
average_lat = data['latitude'].mean()
average_lon = data['longitude'].mean()
m = folium.Map(location=[average_lat, average_lon], zoom_start=16)

# Step 5: Add the land use data to the map
for index, row in data.iterrows():
    land_use = row['land_use']
    latitude = row['latitude']
    longitude = row['longitude']
    
    # Clean and split multi-code land use entries (e.g., 'Er, Ec')
    land_use_codes = [code.strip() for code in land_use.split(',')]  # Remove extra spaces
    
    # Process each land use code and add a marker
    for code in land_use_codes:
        if code in land_use_mapping:
            category = land_use_mapping[code]["category"]
            color = land_use_mapping[code]["color"]
            
            # Add a CircleMarker for each point
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=8,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"Land Use: {category}"
            ).add_to(m)
        else:
            print(f"Unknown land use code: {code}")

# Step 6: Save the map to an HTML file
m.save("land_use_map.html")

print("Map has been saved to 'land_use_map.html'.")
