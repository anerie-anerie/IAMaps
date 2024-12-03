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

# Step 5: Normalize the litter EQI values to map them to a color scale (Green) with reverse mapping
min_litter = litter_values.min()
max_litter = litter_values.max()

def get_litter_color(litter):
    # Reverse normalization: 4 -> light and 0 -> dark
    norm = 1 - (litter - min_litter) / (max_litter - min_litter)
    color = cm.Greens(norm)  # Greens colormap for litter (light to dark green)
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

# Step 6: Normalize the graffiti values to map them to a color scale (Purple) with reverse mapping
min_graph = graph_values.min()
max_graph = graph_values.max()

def get_graphiti_color(graphiti):
    # Reverse normalization: 4 -> light and 0 -> dark
    norm = 1 - (graphiti - min_graph) / (max_graph - min_graph)
    color = cm.Purples(norm)  # Purples colormap for graffiti (light to dark purple)
    # Avoid white (ensure the color stays purple)
    color = [max(c, 0.3) for c in color[:3]]  # Ensure the RGB components stay above a threshold
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


#FIX THE LEGEND!
# Step 10: Add a custom legend to the map
legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 30vw; height: 39vh; 
                background-color: rgba(255, 255, 255, 0.7); 
                border: 2px solid grey; z-index: 9999; font-size: 1vw;
                padding: 10px;">
        <b>Litter (EQI)</b><br>
        <i style="background: #f7f7f7; width: 20px; height: 20px; display: inline-block;"></i> 0 lots of litter <br>
        <i style="background: #7fbc41; width: 20px; height: 20px; display: inline-block;"></i> 1<br>
        <i style="background: #a5d86b; width: 20px; height: 20px; display: inline-block;"></i> 2<br>
        <i style="background: #c1e59f; width: 20px; height: 20px; display: inline-block;"></i> 3<br>
        <i style="background: #e7f8d4; width: 20px; height: 20px; display: inline-block;"></i> 4 No litter <br><br>

        <b>Graffiti (EQI)</b><br>
        <i style="background: #f9f1f9; width: 20px; height: 20px; display: inline-block;"></i> 0 Lots of Litter <br>
        <i style="background: #d3a8d3; width: 20px; height: 20px; display: inline-block;"></i> 1<br>
        <i style="background: #a67ba6; width: 20px; height: 20px; display: inline-block;"></i> 2<br>
        <i style="background: #7b5a7b; width: 20px; height: 20px; display: inline-block;"></i> 3<br>
        <i style="background: #5a375a; width: 20px; height: 20px; display: inline-block;"></i> 4 less litter vanadlism <br>
    </div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Step 11: Save the map as an HTML file
m.save('map_with_litter_and_graphiti_colored_with_legend.html')
