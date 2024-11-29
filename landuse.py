import pandas as pd
import folium

# Step 1: Load the CSV file into a DataFrame
data = pd.read_csv("land.csv")

# Step 2: Filter out rows without land use information
data = data.dropna(subset=["land_use"])

# Step 3: Define land use mapping with correct shorthand codes to full categories and colors
land_use_mapping = {
    # Residential shades of red
    "Ra": {"category": "Residential - Apartment", "color": "#FF6347"},  # Tomato
    "Rs": {"category": "Residential - Semi-detached", "color": "#FF4500"},  # OrangeRed
    "Rd": {"category": "Residential - Detached", "color": "#B22222"},  # Firebrick
    "Rt": {"category": "Residential - Townhouse", "color": "#DC143C"},  # Crimson
    
    # Industrial
    "Il": {"category": "Industrial - Light Manufacturing", "color": "yellow"},
    
    # Commercial shades of blue
    "Cf": {"category": "Commercial - Fast Food", "color": "#ADD8E6"},  # Light Blue
    "Cp": {"category": "Commercial - Personal Services", "color": "#4682B4"},  # Steel Blue
    "Cm": {"category": "Commercial - Market", "color": "#5F9EA0"},  # Cadet Blue
    "Cs": {"category": "Commercial - Specialty Shop", "color": "#1E90FF"},  # Dodger Blue
    "Co": {"category": "Commercial - Office", "color": "#00BFFF"},  # Deep Sky Blue
    "Cv": {"category": "Commercial - Vacant", "color": "#87CEEB"},  # Sky Blue
    
    # Entertainment shades of purple
    "Eh": {"category": "Entertainment - Hotel", "color": "#D8BFD8"},  # Thistle
    "Ec": {"category": "Entertainment - Cinema", "color": "#8A2BE2"},  # BlueViolet
    "Eb": {"category": "Entertainment - Bar", "color": "#800080"},  # Purple
    "Er": {"category": "Entertainment - Restaurant", "color": "#9932CC"},  # DarkOrchid
    "Es": {"category": "Entertainment - Sports Center", "color": "#4B0082"},  # Indigo
    
    # Public Buildings shades of orange
    "Pe": {"category": "Public Building - Education", "color": "#FFA500"},  # Orange
    "Pl": {"category": "Public Building - Library", "color": "#FF8C00"},  # DarkOrange
    "Pc": {"category": "Public Building - Place of Worship", "color": "#FF7F50"},  # Coral
    
    # Open Space shades of green
    "Op": {"category": "Open Space - Park", "color": "#32CD32"},  # LimeGreen
    "Os": {"category": "Open Space - Sports Field", "color": "#228B22"},  # ForestGreen
    "Ou": {"category": "Open Space - Unused Land", "color": "#006400"},  # DarkGreen
    "Od": {"category": "Open Space - Derelict Building", "color": "#2E8B57"},  # SeaGreen
    
    # Transport shades of brown
    "Tb": {"category": "Transport - Bus Stop", "color": "#8B4513"},  # SaddleBrown
    "Tc": {"category": "Transport - Car Park", "color": "#A52A2A"},  # Brown
    
    # Services shades of darker blues
    "Sf": {"category": "Services - Financial", "color": "#00008B"},  # DarkBlue
    "Sm": {"category": "Services - Medical", "color": "#000080"},  # Navy
    "Sb": {"category": "Services - Business", "color": "#191970"},  # MidnightBlue
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
                radius=18,
                color="black",
                fill=True,
                fill_color=color,
                fill_opacity=1.0,
                popup=f"Land Use: {category}"
            ).add_to(m)
        else:
            print(f"Unknown land use code: {code}")

# Step 6: Add a custom legend to the map
legend_html = """
    <div style="position: fixed; 
                bottom: 10vh; left: 5vw; width: 17vw; height: 76vh; 
                background-color: white; z-index: 9999; border:0.5vw black; 
                padding: 1vw; font-size: 0.8vw;">
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

# Step 7: Save the map to an HTML file
m.save("land_use_map_with_legend.html")

print("Map has been saved to 'land_use_map_with_legend.html'.")
