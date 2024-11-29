import pandas as pd
import folium
import matplotlib.cm as cm  # Import colormap from matplotlib
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

# Step 5: Normalize the volumes (volums_deci_avg) values to map them to a color scale (Blue)
min_volums = volums_values.min()
max_volums = volums_values.max()

# Print the range for volumes
print(f"Volume values range: {min_volums} to {max_volums}")

# Normalize data to [0, 1] using log transformation
def normalize_data(value, min_value, max_value):
    norm = (np.log(value + 1) - np.log(min_value + 1)) / (np.log(max_value + 1) - np.log(min_value + 1))
    adjusted_norm = 0.5 + 0.5 * np.sin(np.pi * (norm - 0.5))  # Centered around 0.5
    return np.clip(adjusted_norm, 0, 1)

# Calculate min/max for pedestrians (after extracting the values)
min_ped = ped_values.min()
max_ped = ped_values.max()

# Print the range for pedestrians
print(f"Pedestrian values range: {min_ped} to {max_ped}")

# Calculate min/max for traffic (after extracting the values)
min_traffic = traffic_values.min()
max_traffic = traffic_values.max()

# Print the range for traffic
print(f"Traffic values range: {min_traffic} to {max_traffic}")

# Color functions for volumes, pedestrians, and traffic
def get_volums_color(volums):
    norm = normalize_data(volums, min_volums, max_volums)
    color = cm.Purples(norm)  # Try magma colormap for volumes
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

def get_ped_color(ped):
    norm = normalize_data(ped, min_ped, max_ped)
    color = cm.Blues(norm)  # Try inferno colormap for pedestrians
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

def get_traffic_color(traffic):
    norm = normalize_data(traffic, min_traffic, max_traffic)
    color = cm.Oranges(norm)  # Try cividis colormap for traffic
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

# Step 6: Initialize the map (centered at an average latitude and longitude)
# Recalculate map center, ensuring no NaN latitudes or longitudes
map_center = [data['latitude'].mean(), data['longitude'].mean()]

# Check if map_center contains NaN values
if pd.isna(map_center[0]) or pd.isna(map_center[1]):
    print("Error: Map center contains NaN values. Cannot create map.")
else:
    m = folium.Map(location=map_center, zoom_start=12)

    # Step 7: Plot volumes data on the map
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

    # Step 10: Add the custom legend to the map using HTML
    # Define colors for the legend, using specific shades for each category
    vol_low_color = '#f5ebf8'  # Light purple for low volume
    vol_high_color = '#9e7cbf'  # Dark purple for high volume
    ped_low_color = '#add8e6'  # Light blue for low pedestrian count
    ped_high_color = '#00008b'  # Dark blue for high pedestrian count
    traffic_low_color = '#ffbf80'  # Light orange for low traffic
    traffic_high_color = '#ff4500'  # Dark orange for high traffic

    legend_html = f'''
    <div style="position: fixed; 
                bottom: 10vw; left: 5vw; width: 20vw; height: 30vh;
                background-color: white; z-index:9999; border:0.5vw solid grey;
                border-radius: 5px; padding: 10px; font-size: 1vw;">
        <h4><b>Legend</b></h4>
        <p><b>Volume (Decibels)</b></p>
        <i style="background: {vol_low_color}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
        Low Decibels<br>
        <i style="background: {vol_high_color}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
        High Decibels<br>
        <br>
        <p><b>Pedestrian Count</b></p>
        <i style="background: {ped_low_color}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
        Low Pedestrian Count<br>
        <i style="background: {ped_high_color}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
        High Pedestrian Count<br>
        <br>
        <p><b>Traffic Count</b></p>
        <i style="background: {traffic_low_color}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
        Low Traffic Count<br>
        <i style="background: {traffic_high_color}; width: 18px; height: 18px; border-radius: 50%; display: inline-block;"></i>
        High Traffic Count<br>
    </div>
    '''

    m.get_root().html.add_child(folium.Element(legend_html))

    # Step 11: Save the map as an HTML file
    m.save('tourism_map_with_legend.html')
