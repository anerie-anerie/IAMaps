import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the data
data = pd.read_csv("deciTD.csv")

# Print out missing values in each column
print(data.isna().sum())

# Check summary statistics for 'x' and 'y'
print(data['x'].describe())
print(data['y'].describe())

# Drop rows where either 'x' or 'y' is NaN
df_clean = data.dropna(subset=['x', 'y'])

# Calculate the Pearson correlation coefficient on the cleaned data
correlation_coefficient, p_value = pearsonr(df_clean['x'], df_clean['y'])

# Display the results
print(f"Pearson correlation coefficient: {correlation_coefficient}")
print(f"P-value: {p_value}")

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Scatter plot: Latitude vs Longitude
scatter = plt.scatter(
    data['longitude'], data['latitude'], 
    c=data['x'],  # Color based on 'x' values
    s=data['y'] * 10,  # Size based on 'y' values (scaled for visibility)
    cmap='viridis', alpha=0.8, edgecolor='k'
)

# Add a color bar for the 'x' values
colorbar = plt.colorbar(scatter)
colorbar.set_label('x (ped_average)')

# Add titles and labels
plt.title('Cluster Visualization', fontsize=14)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)

# Annotate points with cluster numbers
for i, row in data.iterrows():
    plt.text(row['longitude'], row['latitude'], str(row['cluster']), fontsize=9, ha='right')

# Show the plot
plt.grid(alpha=0.5)
plt.tight_layout()
plt.show()
