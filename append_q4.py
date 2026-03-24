import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q4 = nbformat.v4.new_markdown_cell("""## Question 4: Lifespan and Geographical Spread of Clusters
**Objective**: Look at how long clusters live and how geographically spread they are, based on their Content Keyword (`cks`). We want to know which content keywords produce the most long-living clusters.

Definitions:
* **Lifespan of a cluster**: The maximum year minus the minimum year the cluster appears.
* **Geographical spread**: The number of unique places the cluster appears in.""")

code_cell_q4 = nbformat.v4.new_code_cell("""# Clean data for lifespan and geography
df_clean = df_images.dropna(subset=['cluster_name', 'cks', 'year', 'place']).copy()

# Step 1: Calculate lifespan and spread for EACH cluster
# We group by cks and cluster_name. 
cluster_stats = df_clean.groupby(['cks', 'cluster_name']).agg(
    min_year=('year', 'min'),
    max_year=('year', 'max'),
    unique_places=('place', 'nunique'),
    total_images=('cluster_name', 'count')
).reset_index()

# Define lifespan
cluster_stats['lifespan'] = cluster_stats['max_year'] - cluster_stats['min_year']

print("--- General Lifespan of Clusters ---")
display(cluster_stats['lifespan'].describe().to_frame().T)

print("\\nHere is the distribution of cluster lifespans across the whole dataset:")
plt.figure(figsize=(10, 5))
sns.histplot(cluster_stats[cluster_stats['lifespan'] > 0]['lifespan'], bins=40, kde=True, color='teal')
plt.title('Distribution of Cluster Lifespans (excluding 0-year lifespans)')
plt.xlabel('Lifespan (Years)')
plt.ylabel('Number of Clusters')
plt.show()

# Step 2: Aggregate by Content Keyword (CKS)
cks_stats = cluster_stats.groupby('cks').agg(
    num_clusters=('cluster_name', 'count'),
    avg_lifespan=('lifespan', 'mean'),
    max_lifespan=('lifespan', 'max'),
    avg_spread=('unique_places', 'mean'),
    max_spread=('unique_places', 'max')
).reset_index()

# Filter out keywords with very few clusters to reduce noise
cks_stats_filtered = cks_stats[cks_stats['num_clusters'] >= 5].copy()

# Sort by Top Maximum Lifespan
top_lifespan_cks = cks_stats_filtered.sort_values('max_lifespan', ascending=False).head(15)

print("\\n--- Top 15 Content Keywords with the Most Long-Living Clusters ---")
display(top_lifespan_cks[['cks', 'max_lifespan', 'avg_lifespan', 'max_spread', 'avg_spread', 'num_clusters']])

# Visualizing Geographical Spread vs Lifespan for Top Keywords
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=top_lifespan_cks, 
    x='max_lifespan', 
    y='max_spread', 
    size='num_clusters', 
    hue='cks', 
    sizes=(50, 400), 
    alpha=0.8,
    legend=False
)

# Annotate the points
for i, row in top_lifespan_cks.iterrows():
    plt.text(row['max_lifespan'] + 1, row['max_spread'] + 0.1, row['cks'], fontsize=9)

plt.title('Max Lifespan vs Max Geographic Spread of Clusters (Top 15 CKS)')
plt.xlabel('Maximum Lifespan (Years)')
plt.ylabel('Maximum Unique Places (Geographic Spread)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
""")

nb.cells.extend([markdown_cell_q4, code_cell_q4])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 4 to notebook.")
