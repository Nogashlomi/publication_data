import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q5 = nbformat.v4.new_markdown_cell("""## Question 5: True Geographic Spread (Clusters vs. Keywords)
**Objective**: The user rightly pointed out that many clusters only contain a single image, skewing the "1 place only" statistic. We want to:
1. Filter out all clusters that only have 1 image (singleton clusters).
2. Look at the geographic spread of the remaining "real" clusters.
3. Compare the geographic spread of an *average Cluster* to the geographic spread of an *entire Content Keyword*.

This answers: "Are *concepts* universal while their *visual execution* remains local?"
""")

code_cell_q5 = nbformat.v4.new_code_cell("""# Base data with valid place values
df_geo = df_images.dropna(subset=['cluster_name', 'cks', 'place']).copy()

# ----------------------------------------------------
# PART 1: The Spread of Multi-Image Clusters
# ----------------------------------------------------
# Count how many images and unique places are in each cluster
cluster_geo = df_geo.groupby('cluster_name').agg(
    total_images=('place', 'count'),
    unique_places=('place', 'nunique'),
    cks=('cks', 'first') # taking the first since a cluster generally maps to one CKS
).reset_index()

# Filter out single-image clusters (which can fundamentally only exist in 1 place)
multi_img_clusters = cluster_geo[cluster_geo['total_images'] > 1]

print(f"Total Clusters: {len(cluster_geo)}")
print(f"Multi-Image Clusters (Size > 1): {len(multi_img_clusters)}\\n")

print("--- Geographic Spread of MULTI-IMAGE Clusters ---")
spread_distribution = multi_img_clusters['unique_places'].value_counts().sort_index()
display(spread_distribution.to_frame('Num Clusters'))

# Quick pie chart to show localization of multi-image clusters
local_pct = (len(multi_img_clusters[multi_img_clusters['unique_places'] == 1]) / len(multi_img_clusters)) * 100
travel_pct = 100 - local_pct

plt.figure(figsize=(6,6))
plt.pie([local_pct, travel_pct], labels=['Stayed in 1 City', 'Traveled (2+ Cities)'], autopct='%1.1f%%', colors=['#4a90e2', '#e94e77'], startangle=90)
plt.title('Do Multi-Image Clusters Travel?')
plt.show()

# ----------------------------------------------------
# PART 2: The Spread of Content Keywords (Concepts)
# ----------------------------------------------------
# Now we group by Content Keyword rather than cluster
kw_geo = df_geo.dropna(subset=['cks']).groupby('cks').agg(
    total_images=('place', 'count'),
    unique_places=('place', 'nunique')
).reset_index()

# Filter keyword by some minimum relevance so we don't count super obscure keywords
valid_kw_geo = kw_geo[kw_geo['total_images'] > 5]

print("\\n--- Geographic Spread of ENTIRE Content Keywords (Concepts) ---")
print("Average number of unique cities a Content Keyword reaches:", valid_kw_geo['unique_places'].mean())
print("Max cities a single Content Keyword reached:", valid_kw_geo['unique_places'].max())

# ----------------------------------------------------
# PART 3: Comparing the Distributions
# ----------------------------------------------------
# Let's plot the distributions side by side
fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=False)

sns.histplot(multi_img_clusters['unique_places'], bins=range(1, 15), ax=axes[0], color='blue', discrete=True)
axes[0].set_title('Spread of Specific Visual Designs (Clusters)')
axes[0].set_xlabel('Number of Unique Cities')
axes[0].set_ylabel('Count')

sns.histplot(valid_kw_geo['unique_places'], bins=range(1, 15), ax=axes[1], color='green', discrete=True)
axes[1].set_title('Spread of Abstract Concepts (Keywords)')
axes[1].set_xlabel('Number of Unique Cities')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.show()

# Conclusion Summary
avg_cluster_spread = multi_img_clusters['unique_places'].mean()
avg_kw_spread = valid_kw_geo['unique_places'].mean()
print(f"\\nKEY FINDING: Visual designs (clusters) appear in an average of {avg_cluster_spread:.2f} cities.")
print(f"Meanwhile, the theoretical concepts (keywords) appear in an average of {avg_kw_spread:.2f} cities.")
""")

nb.cells.extend([markdown_cell_q5, code_cell_q5])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 5 to notebook.")
