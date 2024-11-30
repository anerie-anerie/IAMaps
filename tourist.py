import pandas as pd
import folium
import numpy as np  # For better normalization

# Step 1: Load CSV file into a pandas DataFrame
data = pd.read_csv('tourist.csv')

# Step 2: Filter out rows where specific columns have values <= 0
data_volums = data[data['deci_avg'] > 0]  # Keep rows where deci_avg > 0
data_ped = data[data['ped_average'] > 0]  # Keep rows where ped_average > 0
data_traffic = data[data['traffic_avg'] > 0]  # Keep rows where traffic_avg > 0

# Step 3: Drop rows with missing values (NaNs) from the filtered data
data_volums = data_volums.dropna(subset=['deci_avg'])  # Drop NaNs for 'deci_avg'
data_ped = data_ped.dropna(subset=['ped_average'])  # Drop NaNs for 'ped_average'
data_traffic = data_traffic.dropna(subset=['traffic_avg'])  # Drop NaNs for 'traffic_avg'

# Print number of rows in each filtered dataset
print(f"Filtered volume data has {len(data_volums)} rows")
print(f"Filtered pedestrian data has {len(data_ped)} rows")
print(f"Filtered traffic data has {len(data_traffic)} rows")

# Step 4: Extract latitude, longitude, and values for the three variables
latitudes_volums = data_volums['latitude']
longitudes_volums = data_volums['longitude']
volums_values = data_volums['deci_avg']

latitudes_ped = data_ped['latitude']
longitudes_ped = data_ped['longitude']
ped_values = data_ped['ped_average']

latitudes_traffic = data_traffic['latitude']
longitudes_traffic = data_traffic['longitude']
traffic_values = data_traffic['traffic_avg']

# Step 5: Normalize the volumes (volums_deci_avg) values to map them to a color scale
min_volums = volums_values.min()
max_volums = volums_values.max()

# Normalize data to [0, 1] using log transformation
def normalize_data(value, min_value, max_value):
    norm = (np.log(value + 1) - np.log(min_value + 1)) / (np.log(max_value + 1) - np.log(min_value + 1))
    adjusted_norm = 0.5 + 0.5 * np.sin(np.pi * (norm - 0.5))  # Centered around 0.5
    return np.clip(adjusted_norm, 0, 1)

# Calculate min/max for pedestrians (after extracting the values)
min_ped = ped_values.min()
max_ped = ped_values.max()

# Calculate min/max for traffic (after extracting the values)
min_traffic = traffic_values.min()
max_traffic = traffic_values.max()

# Color functions for volumes, pedestrians, and traffic

def get_volums_color(volums):
    norm = normalize_data(volums, min_volums, max_volums)
    # Custom oranges color range from #FFDBBB to #FF5F1F
    color_start = np.array([1.0, 0.86, 0.73])  # #FFDBBB (light orange)
    color_end = np.array([1.0, 0.37, 0.12])  # #FF5F1F (dark orange)
    # Interpolate between the start and end colors
    interpolated_color = color_start + norm * (color_end - color_start)
    return f'#{int(interpolated_color[0] * 255):02x}{int(interpolated_color[1] * 255):02x}{int(interpolated_color[2] * 255):02x}'

def get_ped_color(ped):
    norm = normalize_data(ped, min_ped, max_ped)
    # Custom blues color range for pedestrians (light blue to dark blue)
    color_start = np.array([0.67, 0.84, 1.0])  # Light blue for low pedestrian count
    color_end = np.array([0.0, 0.0, 0.5])    # Dark blue for high pedestrian count (adjusted)
    # Interpolate between the start and end colors
    interpolated_color = color_start + norm * (color_end - color_start)
    return f'#{int(interpolated_color[0] * 255):02x}{int(interpolated_color[1] * 255):02x}{int(interpolated_color[2] * 255):02x}'

def get_traffic_color(traffic):
    norm = normalize_data(traffic, min_traffic, max_traffic)
    # Custom greens color range from #98FB98 to #4CBB17
    color_start = np.array([0.6, 0.99, 0.6])  # #98FB98 (light green)
    color_end = np.array([0.3, 0.73, 0.09])  # #4CBB17 (dark green)
    # Interpolate between the start and end colors
    interpolated_color = color_start + norm * (color_end - color_start)
    return f'#{int(interpolated_color[0] * 255):02x}{int(interpolated_color[1] * 255):02x}{int(interpolated_color[2] * 255):02x}'

# Step 6: Initialize the map (centered at an average latitude and longitude)
map_center = [data['latitude'].mean(), data['longitude'].mean()]

# Step 7: Plot volumes data on the map
m = folium.Map(location=map_center, zoom_start=12)

for idx, row in data_volums.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    volums = row['deci_avg']
    folium.CircleMarker(
        location=[lat, lon],
        radius=18,
        weight=2,  # Black outline
        color='black',  # Outline color
        fill=True,
        fill_color=get_volums_color(volums),  # Set the fill color for volumes
        fill_opacity=1
    ).add_to(m)

# Step 8: Plot pedestrians data on the map
for idx, row in data_ped.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    ped = row['ped_average']
    folium.CircleMarker(
        location=[lat, lon],
        radius=18,
        weight=2,  # Black outline
        color='black',  # Outline color
        fill=True,
        fill_color=get_ped_color(ped),  # Set the fill color for pedestrians
        fill_opacity=1
    ).add_to(m)

# Step 9: Plot traffic data on the map
for idx, row in data_traffic.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    traffic = row['traffic_avg']
    folium.CircleMarker(
        location=[lat, lon],
        radius=18,
        weight=2,  # Black outline
        color='black',  # Outline color
        fill=True,
        fill_color=get_traffic_color(traffic),  # Set the fill color for traffic
        fill_opacity=1
    ).add_to(m)

# Step 10: Update the legend with the actual colors based on the data ranges

legend_html = f'''
<div style="position: fixed; 
            bottom: 10vw; left: 5vw; width: 15vw; height: 40vh;
            background-color: white; z-index:9999; border:0.5vw solid grey;
            border-radius: 0.5vw; padding: 10px; font-size: 1vw;">
    <p><b>Legend</b></p>
    <p><b>Volume (Decibels)</b></p>
    <i style="background: {get_volums_color(min_volums)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    Low Decibels <br>
    <i style="background: {get_volums_color(max_volums)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    High Decibels <br>
    <br>
    <p><b>Pedestrian Count</b></p>
    <i style="background: {get_ped_color(min_ped)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    Low Pedestrian Count <br>
    <i style="background: {get_ped_color(max_ped)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    High Pedestrian Count <br>
    <br>
    <p><b>Traffic Count</b></p>
    <i style="background: {get_traffic_color(min_traffic)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    Low Traffic Count <br>
    <i style="background: {get_traffic_color(max_traffic)}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
    High Traffic Count<br>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Step 11: Save the map as an HTML file
m.save('tourism_map_with_legend.html')
