import pandas as pd
import numpy as np

# Load Data
img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)

# Prepare distinct image instances
img_u = img_df.drop_duplicates(subset=['images','cluster_name','bid']).copy()
img_u = img_u.dropna(subset=['latitude', 'longitude', 'place'])

# We only care about clusters that are shared
cluster_sizes = img_u.groupby('cluster_name')['bid'].nunique()
shared_clusters = cluster_sizes[cluster_sizes > 1].index
shared_df = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# To find max pairwise distance for a cluster, we can get unique lat/lons per cluster
places = shared_df.drop_duplicates(subset=['cluster_name', 'place'])[['cluster_name', 'latitude', 'longitude']].copy()

max_distances = {}

for cluster, group in places.groupby('cluster_name'):
    coords = group[['latitude', 'longitude']].values
    if len(coords) < 2:
        max_distances[cluster] = 0
        continue
    
    # Calculate all pairwise distances
    n = len(coords)
    max_d = 0
    for i in range(n):
        for j in range(i+1, n):
            d = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            if d > max_d:
                max_d = d
    max_distances[cluster] = max_d

d_series = pd.Series(max_distances)

# Define bins: 0 (stayed in 1 city), 1-100, 100-250, 250-500, 500-750, 750-1000, 1000+
bins = [-1, 0, 100, 250, 500, 750, 1000, 5000]
labels = ['0 km\\n(1 city)', '1-100 km', '101-250 km', '251-500 km', '501-750 km', '751-1000 km', '>1000 km']
cats = pd.cut(d_series, bins=bins, labels=labels)
counts = cats.value_counts().reindex(labels)

print("Distribution of Max Geographic Spread:")
print(counts)
