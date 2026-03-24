import pandas as pd
import numpy as np

# Load Data
img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', low_memory=False)

# Prepare distinct image instances
img_u = img_df.drop_duplicates(subset=['images','cluster_name','bid']).copy()
book_df_sub = book_df[['bid','publishers','printers']].copy()
img_u = img_u.merge(book_df_sub, on='bid', how='left')

# Drop missing place
img_u = img_u.dropna(subset=['place'])

# We only care about clusters that are shared
cluster_sizes = img_u.groupby('cluster_name')['bid'].nunique()
shared_clusters = cluster_sizes[cluster_sizes > 1].index
shared_df = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()

# Create producer
shared_df['producer'] = shared_df['publishers'].fillna('') + " | " + shared_df['printers'].fillna('')
producer_counts = shared_df.groupby('cluster_name')['producer'].nunique(dropna=True)

# Filter to ONLY clusters that crossed institutional boundaries (>1 unique producer)
inst_cross_clusters = producer_counts[producer_counts > 1].index
graph3_df = shared_df[shared_df['cluster_name'].isin(inst_cross_clusters)].copy()

# Count how many unique places (cities) printed each of these mobile clusters
place_counts = graph3_df.groupby('cluster_name')['place'].nunique(dropna=True)

# Use value_counts to explicitly get the counts per number of cities
counts = place_counts.value_counts().sort_index()

print("MAX PLACE COUNTS:", place_counts.max())
print(counts)
