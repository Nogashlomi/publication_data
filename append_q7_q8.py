import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q7 = nbformat.v4.new_markdown_cell("""## Question 7: Top Subjects (Content Keywords) by Geographic Spread and Lifespan
**Objective**: We want to zoom out from the clusters and look at the subjects (the Content Keywords) themselves. 
- Which subjects were debated or printed in the highest number of unique cities?
- Which subjects survived the longest as overarching themes (spanning the maximum number of years from their first to last appearance)?
""")

code_cell_q7 = nbformat.v4.new_code_cell("""# Base data 
df_geo = df_images.dropna(subset=['year', 'place', 'cks']).copy()

# Group by cks to find overall geographic spread and lifespan of the SUBJECT
ck_stats = df_geo.groupby('cks').agg(
    unique_places=('place', 'nunique'),
    min_year=('year', 'min'),
    max_year=('year', 'max'),
    total_images=('place', 'count')
).reset_index()

ck_stats['lifespan'] = ck_stats['max_year'] - ck_stats['min_year']

top_geo_cks = ck_stats.sort_values('unique_places', ascending=False).head(15)
top_life_cks = ck_stats.sort_values('lifespan', ascending=False).head(15)

print("--- Top 15 Most Geographically Shared Subjects (CKS) ---")
display(top_geo_cks[['cks', 'unique_places', 'lifespan', 'total_images']].reset_index(drop=True))

print("\\n--- Top 15 Most Long-Lived Subjects (CKS) ---")
display(top_life_cks[['cks', 'lifespan', 'unique_places', 'total_images']].reset_index(drop=True))

# Let's plot this correlation!
plt.figure(figsize=(10,6))
sns.scatterplot(data=ck_stats, x='lifespan', y='unique_places', size='total_images', sizes=(20, 500), alpha=0.6)
plt.title('Subject (CKS): Lifespan vs. Geographic Spread')
plt.xlabel('Lifespan (Years)')
plt.ylabel('Unique Cities Reached')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
""")

markdown_cell_q8 = nbformat.v4.new_markdown_cell("""## Question 8: City Networks (Which cities share clusters?)
**Objective**: Now we look at the specific connections between cities. If Cluster X appears in both Venice and Paris, those two cities share a link.
By counting these shared clusters, we can see if there are tight-knit networks of cities (e.g. Italian cities copying each other, or trans-Alpine hubs) and which cities are completely isolated.
""")


code_cell_q8 = nbformat.v4.new_code_cell("""import itertools
from collections import Counter

# Filter to clusters that appear in >1 place
clusters_places = df_geo.groupby('cluster_name')['place'].unique().apply(list)
clusters_places = clusters_places[clusters_places.apply(len) > 1]

# Count co-occurrences of cities
co_occurrences = Counter()
for places in clusters_places:
    # Sort to ensure (City A, City B) is same as (City B, City A)
    places = sorted(places)
    for pair in itertools.combinations(places, 2):
        co_occurrences[pair] += 1

# Convert to DataFrame
edges = pd.DataFrame([(k[0], k[1], v) for k, v in co_occurrences.items()], columns=['City 1', 'City 2', 'Shared_Clusters'])
edges = edges.sort_values('Shared_Clusters', ascending=False)

print("--- Top 20 Strongest City Connections (Most Shared Clusters) ---")
display(edges.head(20).reset_index(drop=True))

# Create a heatmap of the top 15 most prolific cities to see the network visually
top_cities = df_geo['place'].value_counts().head(15).index.tolist()
heatmap_data = pd.DataFrame(index=top_cities, columns=top_cities).fillna(0)

for _, row in edges.iterrows():
    c1, c2, wt = row['City 1'], row['City 2'], row['Shared_Clusters']
    if c1 in top_cities and c2 in top_cities:
        heatmap_data.at[c1, c2] = wt
        heatmap_data.at[c2, c1] = wt

# Mirror the matrix (since it's undirected)
for c1 in top_cities:
    for c2 in top_cities:
        if c1 != c2:
            val = max(heatmap_data.at[c1, c2], heatmap_data.at[c2, c1])
            heatmap_data.at[c1, c2] = val
            heatmap_data.at[c2, c1] = val
        else:
            heatmap_data.at[c1, c2] = 0 # No self-loops in heatmap for visual clarity

plt.figure(figsize=(12, 10))
sns.heatmap(heatmap_data.astype(float), annot=True, cmap='Reds', fmt='g', linewidths=.5)
plt.title('Heatmap of Shared Clusters Between Top 15 Cities')
plt.tight_layout()
plt.show()
""")

nb.cells.extend([markdown_cell_q7, code_cell_q7, markdown_cell_q8, code_cell_q8])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Questions 7 & 8 to notebook.")
