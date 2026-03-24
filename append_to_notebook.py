import nbformat

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

markdown_cell_q1 = nbformat.v4.new_markdown_cell("""## Question 1: Content Keyword Variation
**Objective**: Examine which `cks` (content keywords) had the most variation vs the most exact copying.
We will normalize this by looking at `Unique Clusters / Total Images` for each keyword.

* A ratio close to 0 means the same image (cluster) was reused heavily.
* A ratio close to 1 means there was high variation (different images used).""")

code_cell_q1 = nbformat.v4.new_code_cell("""# Import explicit display for pandas DataFrames
from IPython.display import display

# Assume df_images is loaded in the first cell
df_cks = df_images.dropna(subset=['cks']).copy()

# Step 1: Calculate Total Images and Unique Clusters per Keyword (cks)
keyword_stats = df_cks.groupby('cks').agg(
    total_images=('images', 'count'),
    unique_clusters=('cluster_name', 'nunique')
).reset_index()

# Step 2: Normalize to find "Variation Ratio"
keyword_stats['variation_ratio'] = keyword_stats['unique_clusters'] / keyword_stats['total_images']

# Filter out keywords with very few images to ensure our ratio is meaningful (min_images > 20)
min_images = 20
filtered_stats = keyword_stats[keyword_stats['total_images'] >= min_images]

# Sort by variation
most_varied = filtered_stats.sort_values(by='variation_ratio', ascending=False)
least_varied = filtered_stats.sort_values(by='variation_ratio', ascending=True)

print(f"--- Top 10 MOST varied keywords (High variation = Many different images) ---")
display(most_varied.head(10))

print(f"\\n--- Top 10 LEAST varied keywords (High copying = Exact same images reused) ---")
display(least_varied.head(10))

# Visualizing the variation
plt.figure(figsize=(10, 5))
sns.histplot(filtered_stats['variation_ratio'], bins=20, kde=False, color='skyblue')
plt.title(f'Distribution of Keyword Variation Ratios (Min {min_images} images)')
plt.xlabel('Variation Ratio (Unique Clusters / Total Images)')
plt.ylabel('Number of Keywords')
plt.show()""")

markdown_cell_q2 = nbformat.v4.new_markdown_cell("""## Question 2: Copying Trends Over Time and Accross Places
**Objective**: Test the hypothesis that there is *less exact copying of images* and *more differences between places/printers* over time.

We will measure this in two ways:
1. **Overall Copying Trend**: Does the ratio of `Unique Clusters / Total Images` increase over time?
2. **Geographical Localization Trend**: Does the average number of unique places sharing the same cluster decrease over time?""")

code_cell_q2 = nbformat.v4.new_code_cell("""# 1: General Copying over time
time_stats = df_images.dropna(subset=['year_interval']).groupby('year_interval').agg(
    total_images=('images', 'count'),
    unique_clusters=('cluster_name', 'nunique')
).reset_index()

# Sort chronologically
time_stats = time_stats.sort_values(by='year_interval')
time_stats['variation_ratio'] = time_stats['unique_clusters'] / time_stats['total_images']

# Visualizing general variation over time
plt.figure(figsize=(12, 5))
sns.lineplot(data=time_stats, x='year_interval', y='variation_ratio', marker='o', linewidth=2, color='coral')
plt.title('Overall Image Variation Over Time\\n(Increasing trend = Less exact copying)')
plt.xlabel('Time Period')
plt.ylabel('Variation Ratio (Unique Clusters / Total Volume)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# 2: Differences between places over time
# Filter rows where cluster and place are known
df_time_place = df_images.dropna(subset=['year_interval', 'cluster_name', 'place_category'])

cluster_place_counts = df_time_place.groupby(['year_interval', 'cluster_name']).agg(
    unique_places=('place_category', 'nunique')
).reset_index()

# Average the number of unique places per cluster for each time interval
avg_places_per_interval = cluster_place_counts.groupby('year_interval')['unique_places'].mean().reset_index()
avg_places_per_interval = avg_places_per_interval.sort_values(by='year_interval')

plt.figure(figsize=(12, 5))
sns.lineplot(data=avg_places_per_interval, x='year_interval', y='unique_places', marker='s', linewidth=2, color='teal')
plt.title('Average Geographical Spread of Image Clusters Over Time\\n(Decreasing trend = Clusters are more localized/less shared between places)')
plt.xlabel('Time Period')
plt.ylabel('Average Unique Places per Cluster')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()""")

nb.cells.extend([markdown_cell_q1, code_cell_q1, markdown_cell_q2, code_cell_q2])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

