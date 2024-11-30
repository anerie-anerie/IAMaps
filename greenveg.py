import pandas as pd
import folium
import numpy as np

# Step 1: Load CSV file into a pandas DataFrame
data = pd.read_csv('greenveg.csv')

# Step 2: Filter out rows where specific columns have values NaN or <= 0
data_green_space = data[(data['green_space'].notna()) & (data['green_space'] > 0)]  # Green space > 0
data_veg_index = data[(data['veg_index'].notna()) & (data['veg_index'] > 0)]  # Veg index > 0

# Step 3: Remove rows where 'latitude' or 'longitude' is NaN
data_green_space = data_green_space.dropna(subset=['latitude', 'longitude'])
data_veg_index = data_veg_index.dropna(subset=['latitude', 'longitude'])

# Print number of rows in each filtered dataset
print(f"Filtered green space data has {len(data_green_space)} rows")
print(f"Filtered vegetation index data has {len(data_veg_index)} rows")

# Step 4: Extract latitude, longitude, and values for the two variables
latitudes_green_space = data_green_space['latitude']
longitudes_green_space = data_green_space['longitude']
green_space_values = data_green_space['green_space']

latitudes_veg_index = data_veg_index['latitude']
longitudes_veg_index = data_veg_index['longitude']
veg_index_values = data_veg_index['veg_index']

# Step 5: Normalize the green space and veg_index values to map them to a color scale
def normalize_data(value, min_value, max_value):
    norm = (value - min_value) / (max_value - min_value)
    return np.clip(norm, 0, 1)

# Calculate min/max for green space (after extracting the values)
min_green_space = green_space_values.min()
max_green_space = green_space_values.max()

# Calculate min/max for vegetation index (after extracting the values)
min_veg_index = veg_index_values.min()
max_veg_index = veg_index_values.max()

# Color functions for green space and vegetation index
def get_green_space_color(green_space):
    norm = normalize_data(green_space, min_green_space, max_green_space)
    # Custom green color range from light green to dark green
    color_start = np.array([0.6, 0.99, 0.6])  # Light green
    color_end = np.array([0.0, 0.5, 0.0])    # Dark green
    interpolated_color = color_start + norm * (color_end - color_start)
    return f'#{int(interpolated_color[0] * 255):02x}{int(interpolated_color[1] * 255):02x}{int(interpolated_color[2] * 255):02x}'

def get_veg_index_color(veg_index):
    norm = normalize_data(veg_index, min_veg_index, max_veg_index)
    # Custom orange color range from light orange to dark orange
    color_start = np.array([1.0, 0.84, 0.6])  # Light orange
    color_end = np.array([1.0, 0.25, 0.0])   # Dark orange
    interpolated_color = color_start + norm * (color_end - color_start)
    return f'#{int(interpolated_color[0] * 255):02x}{int(interpolated_color[1] * 255):02x}{int(interpolated_color[2] * 255):02x}'

# Step 6: Initialize the map (centered at an average latitude and longitude)
map_center = [data['latitude'].mean(), data['longitude'].mean()]

# Create the map
m = folium.Map(location=map_center, zoom_start=12)

# Step 7: Plot green space data on the map
for idx, row in data_green_space.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    green_space = row['green_space']
    
    # Check if lat/lon are not NaN
    if pd.notna(lat) and pd.notna(lon):
        folium.CircleMarker(
            location=[lat, lon],
            radius=16,
            weight=2,
            color='black',
            fill=True,
            fill_color=get_green_space_color(green_space),  # Custom color function
            fill_opacity=1.0
        ).add_to(m)

# Step 8: Plot vegetation index data on the map
for idx, row in data_veg_index.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    veg_index = row['veg_index']
    
    # Check if lat/lon are not NaN
    if pd.notna(lat) and pd.notna(lon):
        folium.CircleMarker(
            location=[lat, lon],
            radius=16,
            weight=2,
            color='black',
            fill=True,
            fill_color=get_veg_index_color(veg_index),  # Custom color function
            fill_opacity=1.0
        ).add_to(m)

# Step 9: Update the legend with the actual colors based on the data ranges

legend_html = f'''
<div style="position: fixed; 
            bottom: 10vw; left: 5vw; width: 15vw; height: 25vh;
            background-color: white; z-index:9999; border:0.5vw solid grey;
            border-radius: 0.5vw; padding: 10px; font-size: 1vw;">
    <p><b>Legend</b></p>
    <p><b>Green Space</b></p>
    <i style="background: {get_green_space_color(min_green_space)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    Low Green Space <br>
    <i style="background: {get_green_space_color(max_green_space)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    High Green Space <br>
    <br>
    <p><b>Vegetation Index</b></p>
    <i style="background: {get_veg_index_color(min_veg_index)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    Low Vegetation Index <br>
    <i style="background: {get_veg_index_color(max_veg_index)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    High Vegetation Index <br>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Step 10: Save the map as an HTML file
m.save('greenveg_map_with_legend.html')
