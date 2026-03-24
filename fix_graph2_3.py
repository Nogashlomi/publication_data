import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

# Find the markdown cell for Graph 2 and remove it and subsequent cells
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'markdown' and 'Graph 2' in cell.source:
        nb.cells = nb.cells[:i]
        break

# Create new Graph 2
markdown_cell_2 = nbf.v4.new_markdown_cell("""### Graph 2 — Institutional Sharing (Printers/Publishers)

Focusing **only on images that were shared** (clusters appearing in >1 book), how many **different printing houses** (printers/publishers) used the exact same woodblock over its lifespan? This graph counts the shared image clusters by the number of unique institutional producers that printed them. A value of 1 means the shared woodblock stayed entirely within a single printing house.""")

code_cell_2 = nbf.v4.new_code_cell("""# Filter to only clusters that appear in >1 book (shared clusters)
shared_clusters = cluster_sizes[cluster_sizes > 1].index
shared_df = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()

# Create a combined 'producer' field (publisher + printer)
shared_df['producer'] = shared_df['publishers'].fillna('') + " | " + shared_df['printers'].fillna('')

# Count how many unique producers printed each SHARED cluster
producer_counts = shared_df.groupby('cluster_name')['producer'].nunique(dropna=True)

fig, ax = plt.subplots(figsize=(10, 5))
bins = range(1, 15)
ax.hist(producer_counts[producer_counts < 15], bins=bins, color='#d16a54', edgecolor='white', align='left')
ax.set_xticks(range(1, 15))

# Add text annotation
size_1_count = sum(producer_counts == 1)
if size_1_count > 0:
    ax.text(1, size_1_count, f' {size_1_count:,}\\n shared clusters\\n stayed in\\n 1 printing house', 
            va='bottom', ha='center', fontsize=10, color='#2c3e50', fontweight='bold')

ax.set_xlabel('Number of unique Printers/Publishers that used the exact shared image', fontsize=11)
ax.set_ylabel('Number of shared identical image clusters', fontsize=11)
ax.set_title('Graph 2: Distribution of Institutional Sharing (Printers/Publishers)\\n'\
             f'Total shared clusters: {len(producer_counts):,}', fontsize=12, fontweight='bold')

plt.tight_layout()

# Save the figure to the graphs folder
fig.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/Graph_2_Producer_Sharing.png', dpi=300, bbox_inches='tight')
plt.show()

# Print statistics
prop_shared_inst = sum(producer_counts > 1) / len(producer_counts) * 100
print(f"Shared clusters staying strictly within 1 printing house: {size_1_count:,} ({100 - prop_shared_inst:.1f}%)")
print(f"Shared clusters moving across >1 printing house: {sum(producer_counts > 1):,} ({prop_shared_inst:.1f}%)")
print(f"The most widely circulated exact woodblock was used by {producer_counts.max()} different printers/publishers.")
""")

# Create new Graph 3
markdown_cell_3 = nbf.v4.new_markdown_cell("""### Graph 3 — Geographic Sharing (Cities)

Focusing **only on images that were shared** (clusters appearing in >1 book), how many **different cities** did a physical woodblock travel to? This graph counts the shared image clusters by the number of distinct cities they were printed in. A value of 1 means the shared woodblock never left its city of origin.""")

code_cell_3 = nbf.v4.new_code_cell("""# Count how many unique places (cities) printed each SHARED cluster
place_counts = shared_df.groupby('cluster_name')['place'].nunique(dropna=True)

fig, ax = plt.subplots(figsize=(10, 5))
bins = range(1, 10)
ax.hist(place_counts[place_counts < 10], bins=bins, color='#4a9aba', edgecolor='white', align='left')
ax.set_xticks(range(1, 10))

# Add text annotation
size_1_count_place = sum(place_counts == 1)
if size_1_count_place > 0:
    ax.text(1, size_1_count_place, f' {size_1_count_place:,}\\n shared clusters\\n stayed in\\n 1 city', 
            va='bottom', ha='center', fontsize=10, color='#2c3e50', fontweight='bold')

ax.set_xlabel('Number of unique Cities that used the exact shared image', fontsize=11)
ax.set_ylabel('Number of shared identical image clusters', fontsize=11)
ax.set_title('Graph 3: Distribution of Geographic Sharing (Cities)\\n'\
             f'Total shared clusters: {len(place_counts):,}', fontsize=12, fontweight='bold')

plt.tight_layout()

# Save the figure to the graphs folder
fig.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/Graph_3_City_Sharing.png', dpi=300, bbox_inches='tight')
plt.show()

# Print statistics
prop_shared_city = sum(place_counts > 1) / len(place_counts) * 100
print(f"Shared clusters staying strictly within 1 city: {size_1_count_place:,} ({100 - prop_shared_city:.1f}%)")
print(f"Shared clusters moving across >1 city: {sum(place_counts > 1):,} ({prop_shared_city:.1f}%)")
print(f"The most widely traveled exact woodblock was used in {place_counts.max()} different cities.")
""")

nb.cells.extend([markdown_cell_2, code_cell_2, markdown_cell_3, code_cell_3])
nbf.write(nb, nb_path)
