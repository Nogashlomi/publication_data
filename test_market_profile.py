import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Load Data
img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv')
# Use unique image instances (cluster + book)
img_u = img_df.drop_duplicates(subset=['cluster_name', 'bid']).copy()

# 2. Identify Local vs. Shared Clusters
# A cluster is 'Local' if it only ever appears in one unique 'place'
cluster_places = img_u.groupby('cluster_name')['place'].nunique()
local_clusters = cluster_places[cluster_places == 1].index
shared_clusters = cluster_places[cluster_places > 1].index

# 3. Calculate Composition per City
# We only care about cities with a decent amount of images to avoid noise
top_cities = img_u['place'].value_counts().head(30).index

city_data = []
for city in top_cities:
    city_subset = img_u[img_u['place'] == city]
    total = len(city_subset)
    local_count = city_subset['cluster_name'].isin(local_clusters).sum()
    shared_count = city_subset['cluster_name'].isin(shared_clusters).sum()
    
    city_data.append({
        'City': city,
        'Local': local_count,
        'Shared': shared_count,
        'Total': total,
        'Shared_Pct': (shared_count / total) * 100 if total > 0 else 0
    })

df_viz = pd.DataFrame(city_data)

# Sort by 'Shared_Pct' to show the Hub -> Spoke spectrum
df_viz = df_viz.sort_values('Shared_Pct')

# 4. Plotting
fig, ax = plt.subplots(figsize=(12, 10))

# We use absolute counts but the sorting shows the percentage trend
df_viz.plot(
    x='City', 
    y=['Local', 'Shared'], 
    kind='barh', 
    stacked=True, 
    ax=ax, 
    color=['#74b9ff', '#ff7675'],
    edgecolor='white'
)

# Add percentage labels
for i, (idx, row) in enumerate(df_viz.iterrows()):
    ax.text(row['Total'] + 5, i, f"{row['Shared_Pct']:.1f}% shared", va='center', fontsize=9)

ax.set_title('City Market Profile: Local vs. Shared Woodblock Repertoire', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Number of Unique Image Clusters', fontsize=12)
ax.set_ylabel('Printing City', fontsize=12)
ax.legend(['Unique to this City (Local)', 'Shared with other Cities (Mobile)'], loc='lower right')

plt.tight_layout()
output_path = '/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/city_market_profile_test.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_path}")

# 5. Dependency Analysis: Who feeds the Spokes?
hubs = ['Venice', 'Paris', 'Lyon', 'Wittenberg', 'Rome', 'Cologne']
spokes = df_viz[df_viz['Shared_Pct'] > 75]['City'].tolist()

print("\n--- Spoke Dependency Analysis ---")
for spoke in spokes:
    if spoke in hubs: continue
    
    spoke_clusters = set(img_u[img_u['place'] == spoke]['cluster_name'])
    
    overlaps = {}
    for hub in hubs:
        hub_clusters = set(img_u[img_u['place'] == hub]['cluster_name'])
        overlap = len(spoke_clusters.intersection(hub_clusters))
        overlaps[hub] = (overlap / len(spoke_clusters)) * 100 if len(spoke_clusters) > 0 else 0
    
    # Sort and pick the top two feeds
    sorted_hubs = sorted(overlaps.items(), key=lambda x: x[1], reverse=True)[:2]
    hub_str = ", ".join([f"{h} ({p:.1f}%)" for h, p in sorted_hubs])
    print(f"{spoke:15}: {df_viz[df_viz['City']==spoke]['Shared_Pct'].values[0]:.1f}% Shared. Primary Feeds: {hub_str}")
