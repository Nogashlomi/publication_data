import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Data
img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', low_memory=False)

# Prepare distinct image instances
img_u = img_df.drop_duplicates(subset=['images','cluster_name','bid']).copy()
img_u = img_u.merge(book_df[['bid','publishers','printers']], on='bid', how='left')
img_u = img_u.dropna(subset=['place'])

# Total clusters per city (How many distinct images does this city print?)
city_clusters = img_u.groupby('place')['cluster_name'].nunique()

# Filter to genuinely MOBILE clusters (shared across >1 distinct printing house)
img_u['producer'] = img_u['publishers'].fillna('') + " | " + img_u['printers'].fillna('')
producer_counts_all = img_u.groupby('cluster_name')['producer'].nunique(dropna=True)
mobile_clusters = producer_counts_all[producer_counts_all > 1].index

# Mobile clusters per city
mobile_img_u = img_u[img_u['cluster_name'].isin(mobile_clusters)].copy()
city_mobile_clusters = mobile_img_u.groupby('place')['cluster_name'].nunique()

# Calculate Dependency (dependency_pct)
city_stats = pd.DataFrame({
    'total_clusters': city_clusters, 
    'mobile_clusters': city_mobile_clusters
}).fillna(0)

city_stats['dependency_pct'] = (city_stats['mobile_clusters'] / city_stats['total_clusters']) * 100

# Calculate Hub Degree (How many unique other cities does this place share mobile imagery with?)
degree = {}
cluster_to_places = mobile_img_u.groupby('cluster_name')['place'].apply(set).to_dict()
place_to_clusters = mobile_img_u.groupby('place')['cluster_name'].apply(set).to_dict()

for p in city_stats.index:
    if p not in place_to_clusters:
        degree[p] = 0
        continue
    p_clusters = place_to_clusters[p]
    p_connected_places = set()
    for c in p_clusters:
        p_connected_places.update(cluster_to_places[c])
    
    p_connected_places.discard(p) # exclude self
    degree[p] = len(p_connected_places)

city_stats['hub_degree'] = pd.Series(degree)

# Filter to cities with at least 5 clusters to reduce noise
city_stats_filtered = city_stats[city_stats['total_clusters'] >= 5].copy()

# Plotting the Dependency Scatter Plot
fig, ax = plt.subplots(figsize=(14, 10))

sc = ax.scatter(
    city_stats_filtered['dependency_pct'], 
    city_stats_filtered['hub_degree'],
    s=city_stats_filtered['total_clusters'] * 5,  # Node size based on total image output
    alpha=0.6, 
    color='teal',
    edgecolors='black'
)

# Add annotations for major hubs and notable spokes
for place, row in city_stats_filtered.iterrows():
    # Annotate if high degree OR high dependency with reasonable volume
    if row['hub_degree'] > 15 or (row['dependency_pct'] > 90 and row['total_clusters'] > 20):
        ax.text(
            row['dependency_pct'] + 1,  # Offset X slightly
            row['hub_degree'] + 0.5,  # Offset Y slightly
            place, 
            fontsize=10, 
            fontweight='bold',
            ha='left', va='bottom'
        )

# Axes and Titles
ax.set_title('Graph 6: Printing Hubs vs. Spokes (Centrality vs. Dependency)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("Dependency: % of City's Images Found in Mobile Circulation (Cross-Institution)", fontsize=12)
ax.set_ylabel('Hub Degree: Distinct Cities Connected by Mobile Images', fontsize=12)
ax.set_xlim(-5, 115) # Give room for labels on the right
ax.set_ylim(-2, city_stats_filtered['hub_degree'].max() + 5)

ax.grid(True, linestyle='--', alpha=0.5)

# Add a legend for node size
handles, labels = sc.legend_elements(prop='sizes', alpha=0.6, func=lambda s: s/5, num=4)
legend2 = ax.legend(handles, labels, loc='lower right', title='Total Distinct Images\\nProduced by City', bbox_to_anchor=(0.98, 0.05))

plt.tight_layout()
plt.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/graph6_hub_spoke_scatter.png', dpi=300, bbox_inches='tight')
print("Graph 6 Saved successfully to: /Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/graph6_hub_spoke_scatter.png")
