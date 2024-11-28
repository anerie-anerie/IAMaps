import pandas as pd
import folium
import matplotlib.cm as cm  # Import colormap from matplotlib

# Step 1: Load CSV file into a pandas DataFrame
data = pd.read_csv('graphlit.csv')

# Step 2: Drop rows where the required columns (litter or vand) are missing
data_litter = data.dropna(subset=['litter'])  # Data for litter
data_graph = data.dropna(subset=['vand'])  # Data for graffiti

# Step 3: Extract latitude, longitude, and Environmental Quality Index (EQI) values for litter
latitudes_litter = data_litter['latitude']
longitudes_litter = data_litter['longitude']
litter_values = data_litter['litter']

# Step 4: Extract latitude, longitude, and graffiti index values for graffiti
latitudes_graph = data_graph['latitude']
longitudes_graph = data_graph['longitude']
graph_values = data_graph['vand']

# Step 5: Normalize the litter EQI values to map them to a color scale (Green)
min_litter = litter_values.min()
max_litter = litter_values.max()

def get_litter_color(litter):
    # Normalize litter values to [0, 1]
    norm = (litter - min_litter) / (max_litter - min_litter)
    color = cm.Greens(norm)  # Greens colormap for litter (light to dark green)
    # Ensure the lightest values start as light green instead of white
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

# Step 6: Normalize the graffiti values to map them to a color scale (Purple)
min_graph = graph_values.min()
max_graph = graph_values.max()

def get_graphiti_color(graphiti):
    # Normalize graffiti values to [0, 1]
    norm = (graphiti - min_graph) / (max_graph - min_graph)
    color = cm.Purples(norm)  # Purples colormap for graffiti (light to dark purple)
    # Ensure the lightest values start as light purple instead of white
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

# Step 7: Initialize the map (centered at an average latitude and longitude)
map_center = [data['latitude'].mean(), data['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Step 8: Plot litter data on the map (green color for litter)
for idx, row in data_litter.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    litter = row['litter']
    folium.CircleMarker(
        location=[lat, lon],
        radius=18,
        weight=2,  # Black outline
        color='black',  # Outline color
        fill=True,
        fill_color=get_litter_color(litter),  # Set the fill color
        fill_opacity=1
    ).add_to(m)

# Step 9: Plot graffiti data on the map (purple color for graffiti)
for idx, row in data_graph.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    graphiti = row['vand']
    folium.CircleMarker(
        location=[lat, lon],
        radius=18,
        weight=2,  # Black outline
        color='black',  # Outline color
        fill=True,
        fill_color=get_graphiti_color(graphiti),  # Set the fill color
        fill_opacity=1
    ).add_to(m)

# Step 10: Save the map as an HTML file
m.save('map_with_litter_and_graphiti_colored.html')
