import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN, KMeans

# Step 1: Load the data
data = pd.read_csv('tdtour.csv')  # Replace with your CSV file name

# Rename columns for clarity
data = data.rename(columns={'ped_avg': 'x', 'deci_avg': 'y'})

data['x'] = data['x'].replace(0, np.nan)
data['y'] = data['y'].replace(0, np.nan)

# Step 2: Prepare coordinates
coordinates = data[['latitude', 'longitude']].values

# Use k-means clustering to create exactly 10 clusters
kmeans = KMeans(n_clusters=10, random_state=42)
clusters = kmeans.fit_predict(coordinates)

# Add cluster labels
data['cluster'] = clusters

# Aggregate `x` and `y` values within each cluster
grouped = data.groupby('cluster')
aggregated = grouped.agg({
    'latitude': 'mean',
    'longitude': 'mean',
    'x': 'mean',
    'y': 'mean'
}).reset_index()

# Drop clusters where both `x` and `y` are NaN
aggregated = aggregated.dropna(subset=['x', 'y'], how='all')
print(aggregated)

# Optional: Save the results
aggregated.to_csv('deciTD.csv', index=False)
