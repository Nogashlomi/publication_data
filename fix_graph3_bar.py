import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

code_cell_3_source = """# Filter to ONLY clusters that crossed institutional boundaries (>1 unique producer)
inst_cross_clusters = producer_counts[producer_counts > 1].index
graph3_df = shared_df[shared_df['cluster_name'].isin(inst_cross_clusters)].copy()

# Count how many unique places (cities) printed each of these mobile clusters
place_counts = graph3_df.groupby('cluster_name')['place'].nunique(dropna=True)

# Use value_counts to explicitly get the counts per number of cities
counts = place_counts.value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(counts.index, counts.values, color='#4a9aba', edgecolor='white')

# Ensure X axis has a tick for every integer from 1 to the max number of cities
max_cities = max(counts.index.max(), 10)
ax.set_xticks(range(1, max_cities + 1))

# Add text annotation
size_1_count_place = counts.get(1, 0)
if size_1_count_place > 0:
    ax.text(1, size_1_count_place, f' {size_1_count_place:,}\\n clusters\\n crossed printers\\n but stayed in\\n 1 city', 
            va='bottom', ha='center', fontsize=10, color='#2c3e50', fontweight='bold')

ax.set_xlabel('Number of unique Cities for images shared across >1 Print House', fontsize=11)
ax.set_ylabel('Number of shared identical image clusters', fontsize=11)
ax.set_title('Graph 3: Geographic Spread of Woodblocks moving across Printers\\n'\
             f'Total clusters that moved printers: {len(place_counts):,}', fontsize=12, fontweight='bold')

plt.tight_layout()

# Save the figure
fig.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/Graph_3_City_Sharing.png', dpi=300, bbox_inches='tight')
plt.show()

# Print statistics
prop_shared_city = sum(place_counts > 1) / len(place_counts) * 100
print(f"Clusters that moved printers but stayed strictly within 1 city: {size_1_count_place:,} ({100 - prop_shared_city:.1f}%)")
print(f"Clusters that moved printers AND moved across >1 city: {sum(place_counts > 1):,} ({prop_shared_city:.1f}%)")
print(f"The most widely traveled exact woodblock was used in {place_counts.max()} different cities.")
"""

# Replace the existing code cell for graph 3
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'inst_cross_clusters = producer_counts' in cell.source:
        cell.source = code_cell_3_source
        break

nbf.write(nb, nb_path)
