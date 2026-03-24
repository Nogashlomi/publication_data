import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q10 = nbformat.v4.new_markdown_cell("""### Question 10: Comparative Analysis: Reviewed vs. Unreviewed Subjects
**Objective**: Now we directly compare the fundamental nature of the subjects you chose to review against those you left out. 

Do the subjects in your dissertation have a significantly wider geographic spread than average? Did they live longer? Do they have a richer, more diverse set of visual variations (clusters)? Let's look at the stats.
""")

code_cell_q10 = nbformat.v4.new_code_cell("""import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# We already have df_geo and reviewed_cks defined from previous cells
# We will look at all valid CKS (printed >= 10 times)
ocks_stats = df_geo[df_geo['cks'].isin(valid_cks)].groupby('cks').agg(
    unique_places=('place', 'nunique'),
    min_year=('year', 'min'),
    max_year=('year', 'max'),
    num_clusters=('cluster_name', 'nunique'),
    total_images=('place', 'count')
).reset_index()

ocks_stats['lifespan'] = ocks_stats['max_year'] - ocks_stats['min_year']

# Tag them as Reviewed or Unreviewed
ocks_stats['Status'] = ocks_stats['cks'].apply(lambda x: 'Reviewed (SA Notebooks)' if x in reviewed_cks else 'Unreviewed (Other Core)')

print("--- Statistical Summary of Subjects (CKS) ---")
display(ocks_stats.groupby('Status')[['unique_places', 'lifespan', 'num_clusters', 'total_images']].mean().round(2).rename(columns={
    'unique_places': 'Avg. Geographic Spread (Cities)',
    'lifespan': 'Avg. Temporal Lifespan (Years)',
    'num_clusters': 'Avg. Visual Diversity (Num Clusters)',
    'total_images': 'Avg. Total Print Volume'
}))

# Let's plot these distributions to see the spread, not just the averages.
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
sns.set_theme(style="whitegrid")
colors = {'Reviewed (SA Notebooks)': 'orange', 'Unreviewed (Other Core)': 'lightgreen'}

# 1. Geographic Spread
sns.boxplot(data=ocks_stats, x='Status', y='unique_places', ax=axes[0], palette=colors)
axes[0].set_title('Geographic Spread Distribution')
axes[0].set_ylabel('Number of Unique Cities')
axes[0].set_xlabel('')

# 2. Temporal Lifespan
sns.boxplot(data=ocks_stats, x='Status', y='lifespan', ax=axes[1], palette=colors)
axes[1].set_title('Temporal Lifespan Distribution')
axes[1].set_ylabel('Lifespan (Years)')
axes[1].set_xlabel('')

# 3. Visual Diversity (Number of Clusters)
sns.boxplot(data=ocks_stats, x='Status', y='num_clusters', ax=axes[2], palette=colors)
axes[2].set_title('Visual Diversity Distribution')
axes[2].set_ylabel('Number of Unique Visual Clusters')
axes[2].set_xlabel('')

plt.tight_layout()
plt.show()

# Deep Dive: Cluster specific analysis within these subjects
# Do the clusters within reviewed subjects travel more than clusters in unreviewed subjects?
cluster_stats_within_cks = df_geo[df_geo['cks'].isin(valid_cks)].groupby(['cks', 'cluster_name']).agg(
    cluster_places=('place', 'nunique')
).reset_index()

cluster_stats_within_cks['Status'] = cluster_stats_within_cks['cks'].apply(lambda x: 'Reviewed' if x in reviewed_cks else 'Unreviewed')

avg_cluster_travel = cluster_stats_within_cks.groupby('Status')['cluster_places'].mean()
print("\\n--- How widely did their specific visual execution travel? ---")
print(f"Average number of cities a specific visual cluster traveled to:")
print(f"In Reviewed Subjects: {avg_cluster_travel['Reviewed']:.2f} cities")
print(f"In Unreviewed Subjects: {avg_cluster_travel['Unreviewed']:.2f} cities")
""")

nb.cells.extend([markdown_cell_q10, code_cell_q10])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 10 to notebook.")
