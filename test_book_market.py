import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
img_u = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv')
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv')

# 1. Identify Local vs. Shared Clusters
# Local: Appears in only 1 book
# Shared: Appears in >1 book
cluster_counts = img_u['cluster_name'].value_counts()
shared_clusters = cluster_counts[cluster_counts > 1].index
local_clusters = cluster_counts[cluster_counts == 1].index

# 2. Analyze each book
book_stats = []
for bid, group in img_u.groupby('bid'):
    local_count = group['cluster_name'].isin(local_clusters).sum()
    shared_count = group['cluster_name'].isin(shared_clusters).sum()
    book_stats.append({
        'bid': bid,
        'Local': local_count,
        'Shared': shared_count,
        'Total': local_count + shared_count
    })

df_books = pd.DataFrame(book_stats)

# 3. Merge with metadata for Year
df_books = df_books.merge(book_df[['bid', 'year']], on='bid')
df_books = df_books.sort_values('year')

# 4. Plotting
fig, ax = plt.subplots(figsize=(20, 8))

# We use an index for X to keep books distinct even if in the same year
df_books['x_idx'] = range(len(df_books))

ax.bar(df_books['x_idx'], df_books['Local'], label='Unique to this Book', color='#74b9ff')
ax.bar(df_books['x_idx'], df_books['Shared'], bottom=df_books['Local'], label='Shared with others', color='#ff7675')

# Set ticks to show years periodically
tick_indices = range(0, len(df_books), max(1, len(df_books)//20))
ax.set_xticks(tick_indices)
ax.set_xticklabels(df_books['year'].iloc[tick_indices], rotation=45)

ax.set_title('Graph 7: Woodblock Composition per Book (Sorted by Year)', fontsize=16, fontweight='bold')
ax.set_xlabel('Books (Ordered by Year)', fontsize=12)
ax.set_ylabel('Number of Woodblocks', fontsize=12)
ax.legend()

plt.tight_layout()
output_path = '/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/book_composition_time_test.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Graph saved to {output_path}")

# Calculate some stats for the user
df_books['Shared_Pct'] = (df_books['Shared'] / df_books['Total']) * 100
print(f"\nAverage sharing percentage per book: {df_books['Shared_Pct'].mean():.1f}%")
print(f"Number of books with 100% shared images: {len(df_books[df_books['Shared_Pct'] == 100])}")
print(f"Number of books with 0% shared images: {len(df_books[df_books['Shared_Pct'] == 0])}")
