import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

markdown_cell_5 = nbf.v4.new_markdown_cell("""### Graph 5 — Maximum Geographic Spread per Shared Image Cluster

For every image cluster that was printed in more than one book, what was the **maximum geographic distance** it traveled? By computing the greatest distance between any two cities where a specific woodblock was printed, we can see the distribution of how far images circulated. Images that were shared but never left their origin city have a spread of 0 km.""")

code_cell_5 = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Filter to shared clusters only
cluster_sizes_spread = img_u.groupby('cluster_name')['bid'].nunique()
shared_clusters_spread = cluster_sizes_spread[cluster_sizes_spread > 1].index
spread_df = img_u[img_u['cluster_name'].isin(shared_clusters_spread)].copy()
spread_df = spread_df.dropna(subset=['latitude', 'longitude', 'place'])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Get unique lat/lons per cluster to compute pairwise distances
places = spread_df.drop_duplicates(subset=['cluster_name', 'place'])[['cluster_name', 'latitude', 'longitude']].copy()

max_distances = {}
for cluster, group in places.groupby('cluster_name'):
    coords = group[['latitude', 'longitude']].values
    if len(coords) < 2:
        max_distances[cluster] = 0
        continue
    
    # Calculate all pairwise distances to find the maximum physical spread
    n = len(coords)
    max_d = 0
    for i in range(n):
        for j in range(i+1, n):
            d = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            if d > max_d:
                max_d = d
    max_distances[cluster] = max_d

d_series = pd.Series(max_distances)

# Bin the maximum distances
bins = [-1, 0, 100, 250, 500, 750, 1000, 5000]
labels = ['0 km\\n(1 city)', '1-100\\nkm', '101-250\\nkm', '251-500\\nkm', '501-750\\nkm', '751-1000\\nkm', '>1000\\nkm']
cats = pd.cut(d_series, bins=bins, labels=labels)
counts = cats.value_counts().reindex(labels)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(counts.index, counts.values, color='#27ae60', edgecolor='white')

# Add exact count on top of every bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + counts.values.max()*0.02, f'{yval:,}', 
            ha='center', va='bottom', fontsize=10, color='#2c3e50', fontweight='bold')

ax.set_ylim(0, counts.values.max() * 1.15)
ax.set_xlabel('Maximum Distance Between Printing Locations', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Shared Image Clusters', fontsize=12, fontweight='bold')
ax.set_title('Graph 5: Total Geographic Spread of Shared Woodblocks\\n'\
             f'(Based on {len(d_series):,} shared image clusters)', fontsize=14, fontweight='bold')

plt.tight_layout()

# Save the figure
fig.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/Graph_5_Geo_Spread.png', dpi=300, bbox_inches='tight')
plt.show()

# Print statistics
print(f"Clusters that were shared but never left their origin city: {counts.iloc[0]:,} ({counts.iloc[0]/len(d_series)*100:.1f}%)")
print(f"Clusters that spread across Europe (>750 km): {counts.iloc[-2] + counts.iloc[-1]:,} ({(counts.iloc[-2] + counts.iloc[-1])/len(d_series)*100:.1f}%)")
""")

nb.cells.extend([markdown_cell_5, code_cell_5])
nbf.write(nb, nb_path)
