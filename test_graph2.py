import pandas as pd
import numpy as np

img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv')
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv')

img_u = img_df.drop_duplicates(subset=['images','cluster_name','bid']).copy()
img_u = img_u.merge(book_df[['bid','publishers','printers']], on='bid', how='left')

cluster_sizes = img_u.groupby('cluster_name')['bid'].nunique()
shared_clusters = cluster_sizes[cluster_sizes > 1].index

shared_df = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()

def analyze_sharing(df, col):
    unique_counts = df.groupby('cluster_name')[col].nunique(dropna=True)
    same = sum(unique_counts <= 1)
    diff = sum(unique_counts > 1)
    return same, diff

shared_df['producer'] = shared_df['publishers'].fillna('') + " | " + shared_df['printers'].fillna('')
same_prod, diff_prod = analyze_sharing(shared_df, 'producer')
same_place, diff_place = analyze_sharing(shared_df, 'place')

print(f"Total Shared Clusters: {len(shared_clusters)}")
print(f"Same Producer: {same_prod}, Different Producer: {diff_prod}")
print(f"Same Place: {same_place}, Different Place: {diff_place}")
