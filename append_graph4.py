import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

markdown_cell_4 = nbf.v4.new_markdown_cell("""### Graph 4 — Geographic and Institutional Distance of Image Sharing Over Time

How did the nature of image sharing change over time? In this analysis, we identify the **origin** of every shared image cluster (its earliest known printing). For every subsequent copy in the dataset, we calculate two metrics:
1. **Geographic Distance**: The flight distance (in km) between the printing city of the copy and the origin city.
2. **Institutional Sharing**: Whether the printer of the copy is different from the original printer.

By aggregating these metrics by decade, we can see if image sharing became more geographically dispersed and institutionally fluid over time.""")

code_cell_4 = nbf.v4.new_code_cell("""import numpy as np

# Retain only clusters that are shared
cluster_sizes_time = img_u.groupby('cluster_name')['bid'].nunique()
shared_clusters_time = cluster_sizes_time[cluster_sizes_time > 1].index
time_df = img_u[img_u['cluster_name'].isin(shared_clusters_time)].copy()

# Ensure we have coordinates and years
time_df = time_df.dropna(subset=['year', 'latitude', 'longitude'])
time_df['year'] = pd.to_numeric(time_df['year'], errors='coerce')
time_df = time_df.dropna(subset=['year'])

# Create unified producer
time_df['producer'] = time_df['publishers'].fillna('') + " | " + time_df['printers'].fillna('')

# Define Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Identify the absolute "origin" instance of each cluster (earliest year)
origins = time_df.loc[time_df.groupby('cluster_name')['year'].idxmin()]
origins = origins[['cluster_name', 'producer', 'latitude', 'longitude', 'year']].rename(columns={
    'producer': 'orig_prod',
    'latitude': 'orig_lat',
    'longitude': 'orig_lon',
    'year': 'orig_year'
})

# Merge origins back into main DataFrame
time_df = time_df.merge(origins, on='cluster_name', how='left')

# Exclude the "origin" printings themselves, only look at the subsequent COPIES
copies = time_df[time_df['year'] > time_df['orig_year']].copy()

# Calculate metrics for each copy
copies['is_diff_producer'] = (copies['producer'] != copies['orig_prod']).astype(int)
copies['distance_to_origin'] = haversine(
    copies['latitude'].values, copies['longitude'].values, 
    copies['orig_lat'].values, copies['orig_lon'].values
)

# Group by Decade
copies['decade'] = (copies['year'] // 10) * 10
decade_stats = copies.groupby('decade').agg(
    total_copies=('bid', 'count'),
    pct_diff_producer=('is_diff_producer', 'mean'),
    mean_distance=('distance_to_origin', 'mean')
).reset_index()

# Convert to percentage
decade_stats['pct_diff_producer'] *= 100

# Exclude decades with very few data points (< 30) to avoid extreme outliers
decade_stats = decade_stats[decade_stats['total_copies'] >= 30]

# Plotting with dual Y-axes
fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = '#3498db'
ax1.set_xlabel('Decade', fontsize=12, fontweight='bold')
ax1.set_ylabel('Mean Geographic Distance from Origin (km)', color=color1, fontsize=12, fontweight='bold')
line1 = ax1.plot(decade_stats['decade'], decade_stats['mean_distance'], color=color1, marker='o', linewidth=2.5, label='Mean Geographic Distance')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(decade_stats['decade'])
ax1.set_xticklabels(decade_stats['decade'].astype(int), rotation=45)

# Secondary Y-axis for percentage
ax2 = ax1.twinx()  
color2 = '#e74c3c'
ax2.set_ylabel('% of Copies Printed by a Different Printer', color=color2, fontsize=12, fontweight='bold')  
line2 = ax2.plot(decade_stats['decade'], decade_stats['pct_diff_producer'], color=color2, marker='s', linewidth=2.5, linestyle='--', label='% Different Printer')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 105) # Percentage axis

# Title and Layout
plt.title('Graph 4: Institutional and Geographic Dispersion of Shared Images Over Time\\n'\
          f'(Based on {len(copies):,} subsequent image copy instances)', fontsize=14, fontweight='bold')

# Combine legends
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='lower right', fontsize=11)

plt.grid(alpha=0.3)
plt.tight_layout()

# Save the figure
fig.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/Graph_4_Time_Dispersion.png', dpi=300, bbox_inches='tight')
plt.show()
""")

nb.cells.extend([markdown_cell_4, code_cell_4])
nbf.write(nb, nb_path)
