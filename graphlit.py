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
    # Normalization: 0 -> dark green, 4 -> lighter green
    norm = (litter - min_litter) / (max_litter - min_litter)
    norm = min(norm, 1)
    color = cm.Greens(0.7 - norm * 0.4)  # Shift to make the light green darker
    color = [max(c, 0.2) for c in color[:3]]  # Ensure RGB components stay above a threshold
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

# Step 6: Normalize the graffiti values to map them to a color scale (Purple)
min_graph = graph_values.min()
max_graph = graph_values.max()

def get_graphiti_color(graphiti):
    # Normalization: 0 -> dark purple, 4 -> lighter purple
    norm = (graphiti - min_graph) / (max_graph - min_graph)
    norm = min(norm, 1)
    color = cm.Purples(0.7 - norm * 0.4)  # Shift to make the light purple darker
    color = [max(c, 0.2) for c in color[:3]]  # Ensure RGB components stay above a threshold
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

# Step 7: Initialize the map
map_center = [data['latitude'].mean(), data['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Step 8: Plot litter data on the map
for idx, row in data_litter.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    litter = row['litter']
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        weight=2,
        color='black',
        fill=True,
        fill_color=get_litter_color(litter),
        fill_opacity=1
    ).add_to(m)

# Step 9: Plot graffiti data on the map
for idx, row in data_graph.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    graphiti = row['vand']
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        weight=2,
        color='black',
        fill=True,
        fill_color=get_graphiti_color(graphiti),
        fill_opacity=1
    ).add_to(m)

legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 17vw; height: 43vh; 
                background-color: rgba(255, 255, 255, 0.7); 
                border: 2px solid grey; z-index: 9999; font-size: 1vw;
                padding: 10px;">
        <b>Litter (EQI)</b><br>
        <i style="background: #3b672e; width: 20px; height: 20px; display: inline-block;"></i> 0 Lots of litter <br>
        <i style="background: #568b42; width: 20px; height: 20px; display: inline-block;"></i> 1 Some litter <br>
        <i style="background: #73ad5d; width: 20px; height: 20px; display: inline-block;"></i> 2 Moderate litter <br>
        <i style="background: #91c87c; width: 20px; height: 20px; display: inline-block;"></i> 3 Less litter <br>
        <i style="background: #b4e3a5; width: 20px; height: 20px; display: inline-block;"></i> 4 No litter <br><br>

        <b>Graffiti (EQI)</b><br>
        <i style="background: #4f2a4f; width: 20px; height: 20px; display: inline-block;"></i> 0 Lots of graffiti <br>
        <i style="background: #704670; width: 20px; height: 20px; display: inline-block;"></i> 1 Some graffiti <br>
        <i style="background: #906390; width: 20px; height: 20px; display: inline-block;"></i> 2 Moderate graffiti <br>
        <i style="background: #b081b0; width: 20px; height: 20px; display: inline-block;"></i> 3 Less graffiti <br>
        <i style="background: #d3aad3; width: 20px; height: 20px; display: inline-block;"></i> 4 No graffiti <br>
    </div>
'''


m.get_root().html.add_child(folium.Element(legend_html))

# Step 11: Save the map as an HTML file
m.save('map_with_litter_and_graphiti_colored_with_legend.html')
