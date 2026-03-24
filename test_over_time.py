import pandas as pd
import numpy as np

# Load Data
img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', low_memory=False)

# Prepare distinct image instances
img_u = img_df.drop_duplicates(subset=['images','cluster_name','bid']).copy()
book_df_sub = book_df[['bid','publishers','printers']].copy()
img_u = img_u.merge(book_df_sub, on='bid', how='left')

# Drop missing year, lat, lon
img_u = img_u.dropna(subset=['year', 'latitude', 'longitude'])
img_u['year'] = pd.to_numeric(img_u['year'], errors='coerce')
img_u = img_u.dropna(subset=['year'])

# We only care about clusters that are shared
cluster_sizes = img_u.groupby('cluster_name')['bid'].nunique()
shared_clusters = cluster_sizes[cluster_sizes > 1].index
df = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()

# Create producer
df['producer'] = df['publishers'].fillna('') + " | " + df['printers'].fillna('')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Find origin for each cluster (the earliest printing)
origins = df.loc[df.groupby('cluster_name')['year'].idxmin()]
origins = origins[['cluster_name', 'producer', 'latitude', 'longitude', 'year']].rename(columns={
    'producer': 'orig_prod',
    'latitude': 'orig_lat',
    'longitude': 'orig_lon',
    'year': 'orig_year'
})

# Merge origins back to main df
df = df.merge(origins, on='cluster_name', how='left')

# Exclude the exact origin instances 
copies = df[df['year'] > df['orig_year']].copy()

# Calculate metrics
copies['is_diff_producer'] = (copies['producer'] != copies['orig_prod']).astype(int)
copies['distance_to_origin'] = haversine(copies['latitude'].values, copies['longitude'].values, copies['orig_lat'].values, copies['orig_lon'].values)

# Group by Decade
copies['decade'] = (copies['year'] // 10) * 10
decade_stats = copies.groupby('decade').agg(
    total_copies=('bid', 'count'),
    pct_diff_producer=('is_diff_producer', 'mean'),
    mean_distance=('distance_to_origin', 'mean')
).reset_index()

decade_stats['pct_diff_producer'] *= 100

pd.set_option('display.max_rows', 50)
print(decade_stats)
