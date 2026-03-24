import pandas as pd
df_images = pd.read_csv('dissertation/full_image_data_feb_25.csv', low_memory=False)

# Q1: Keyword variation
df_cks = df_images.dropna(subset=['cks']).copy()
# Note: 'cks' might be lists or comma-separated strings. Assuming it's simple strings for now.
cks_stats = df_cks.groupby('cks').agg(
    total_images=('images', 'count'),
    unique_clusters=('cluster_name', 'nunique')
).reset_index()

cks_stats['variation_ratio'] = cks_stats['unique_clusters'] / cks_stats['total_images']
cks_stats_filtered = cks_stats[cks_stats['total_images'] >= 10]
print("Top 5 keywords with HIGHEST variation:")
print(cks_stats_filtered.sort_values('variation_ratio', ascending=False).head())
print("\nTop 5 keywords with LOWEST variation (most copying):")
print(cks_stats_filtered.sort_values('variation_ratio', ascending=True).head())

# Q2: Variation over time
time_stats = df_images.groupby('year_interval').agg(
    total_images=('images', 'count'),
    unique_clusters=('cluster_name', 'nunique')
).reset_index()
time_stats['variation_ratio'] = time_stats['unique_clusters'] / time_stats['total_images']
print("\nVariation over time:")
print(time_stats.sort_values('year_interval'))

# Q2 part b: Place differences over time
# For each cluster in each interval, how many unique places used it?
cluster_place_stats = df_images.groupby(['year_interval', 'cluster_name']).agg(
    unique_places=('place', 'nunique')
).reset_index()
avg_places_per_cluster = cluster_place_stats.groupby('year_interval')['unique_places'].mean().reset_index()
print("\nAverage unique places per cluster over time:")
print(avg_places_per_cluster.sort_values('year_interval'))
