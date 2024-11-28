import pandas as pd
import folium
import matplotlib.cm as cm  # Import colormap from matplotlib

# Step 1: Load CSV file into a pandas DataFrame
data = pd.read_csv('data.csv')

# Step 2: Drop rows where the Environmental Quality Index (EQI) is missing
data = data.dropna(subset=['EQI'])

# Step 3: Extract latitude, longitude, and Environmental Quality Index (EQI) values
latitudes = data['latitude']
longitudes = data['longitude']
eqi_values = data['EQI']  # Make sure this matches the column name in your CSV

# Step 4: Normalize the EQI values to map them to a color scale
min_eqi = eqi_values.min()
max_eqi = eqi_values.max()
print(f"Min EQI: {min_eqi}, Max EQI: {max_eqi}")

# Step 5: Create a color map based on EQI values (using Greens colormap for shades of green)
def get_color(eqi):
    # Normalize EQI value to a range [0, 1]
    norm = (eqi - min_eqi) / (max_eqi - min_eqi)  
    # Use a colormap (Greens) to get a green color based on the normalized EQI value
    color = cm.Greens(norm)  # Greens colormap produces shades of green
    return f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'
# higher EQI litter = darker color

# Step 6: Initialize the map (centered at an average latitude and longitude)
m = folium.Map(location=[latitudes.mean(), longitudes.mean()], zoom_start=12)

# Step 7: Plot each point on the map with its corresponding color
for idx, row in data.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    eqi = row['EQI']  # Assuming the column name is 'EQI'

    folium.CircleMarker(
        location=[lat, lon],  # Correctly passing latitude and longitude as a list
        radius=7,  # Increase the radius size for bigger dots (previously 5)
        weight=2,  # Add a border for the circle (outline thickness)
        color=get_color(eqi),  # Set the outline color
        fill=True,
        fill_color=get_color(eqi),  # Set the fill color to the same as the outline
        fill_opacity=1  # Opacity of the filled circle
    ).add_to(m)

# Step 8: Save the map as an HTML file
m.save('map_with_eqi_shades_of_green.html')
