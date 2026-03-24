import json
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Graph 6: The Hub-and-Spoke Model (Dependency vs. Centrality)\\n",
        "\\n",
        "To visualize the power dynamics between different printing centers, we can measure two key metrics for each city:\\n",
        "1. **Dependency Ratio (X-axis):** What percentage of a city's total woodblock imagery comes from shared (circulating) clusters, rather than exclusive local production?\\n",
        "2. **Out-Degree / Hub Centrality (Y-axis):** How many *unique other cities* does this city share its woodblocks with?\\n",
        "\\n",
        "Cities with high out-degree and moderate-to-high dependency act as major **Hubs** (e.g., Venice, Paris, Lyon), deeply integrated into the European network. Conversely, cities with 100% dependency and lower out-degrees act as dependent **Spokes**."
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 1. Calculate City Image Statistics\\n",
        "# Total clusters per city (How many distinct images does this city print?)\\n",
        "city_clusters = img_u.groupby('place')['cluster_name'].nunique()\\n",
        "\\n",
        "# Shared clusters per city (Using our strictly filtered cross-printer shared clusters)\\n",
        "shared_img_u = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()\\n",
        "city_shared_clusters = shared_img_u.groupby('place')['cluster_name'].nunique()\\n",
        "\\n",
        "# Calculate Dependency (shared_pct)\\n",
        "city_stats = pd.DataFrame({\\n",
        "    'total_clusters': city_clusters, \\n",
        "    'shared_clusters': city_shared_clusters\\n",
        "}).fillna(0)\\n",
        "\\n",
        "city_stats['shared_pct'] = (city_stats['shared_clusters'] / city_stats['total_clusters']) * 100\\n",
        "\\n",
        "# 2. Calculate Hub Degree (How many unique other cities does this place share imagery with?)\\n",
        "degree = {}\\n",
        "cluster_to_places = shared_img_u.groupby('cluster_name')['place'].apply(set).to_dict()\\n",
        "place_to_clusters = shared_img_u.groupby('place')['cluster_name'].apply(set).to_dict()\\n",
        "\\n",
        "for p in city_stats.index:\\n",
        "    if p not in place_to_clusters:\\n",
        "        degree[p] = 0\\n",
        "        continue\\n",
        "    p_clusters = place_to_clusters[p]\\n",
        "    p_connected_places = set()\\n",
        "    for c in p_clusters:\\n",
        "        p_connected_places.update(cluster_to_places[c])\\n",
        "    \\n",
        "    p_connected_places.discard(p) # exclude self\\n",
        "    degree[p] = len(p_connected_places)\\n",
        "\\n",
        "city_stats['hub_degree'] = pd.Series(degree)\\n",
        "\\n",
        "# Filter to cities with at least 10 clusters to reduce noise\\n",
        "city_stats_filtered = city_stats[city_stats['total_clusters'] >= 5].copy()\\n",
        "\\n",
        "# 3. Plotting the Dependency Scatter Plot\\n",
        "fig, ax = plt.subplots(figsize=(14, 10))\\n",
        "\\n",
        "sc = ax.scatter(\\n",
        "    city_stats_filtered['shared_pct'], \\n",
        "    city_stats_filtered['hub_degree'],\\n",
        "    s=city_stats_filtered['total_clusters'] * 5,  # Node size based on total image output\\n",
        "    alpha=0.6, \\n",
        "    color='teal',\\n",
        "    edgecolors='black'\\n",
        ")\\n",
        "\\n",
        "# Add annotations for major hubs and notable spokes\\n",
        "texts = []\\n",
        "for place, row in city_stats_filtered.iterrows():\\n",
        "    # Annotate if high degree OR high dependency with reasonable volume\\n",
        "    if row['hub_degree'] > 15 or (row['shared_pct'] > 90 and row['total_clusters'] > 20):\\n",
        "        ax.text(\\n",
        "            row['shared_pct'] + 1,  # Offset X slightly\\n",
        "            row['hub_degree'] + 0.5,  # Offset Y slightly\\n",
        "            place, \\n",
        "            fontsize=10, \\n",
        "            fontweight='bold',\\n",
        "            ha='left', va='bottom'\\n",
        "        )\\n",
        "\\n",
        "# Axes and Titles\\n",
        "ax.set_title('Graph 6: Printing Hubs vs. Spokes (Centrality vs. Dependency)', fontsize=16, fontweight='bold', pad=20)\\n",
        "ax.set_xlabel('Dependency: % of City\\'s Images Found in Shared Circulation', fontsize=12)\\n",
        "ax.set_ylabel('Hub Degree: Distinct Cities Connected by Shared Images', fontsize=12)\\n",
        "ax.set_xlim(-5, 115) # Give room for labels on the right\\n",
        "ax.set_ylim(-2, city_stats_filtered['hub_degree'].max() + 5)\\n",
        "\\n",
        "ax.grid(True, linestyle='--', alpha=0.5)\\n",
        "\\n",
        "# Add a legend for node size\\n",
        "handles, labels = sc.legend_elements(prop='sizes', alpha=0.6, func=lambda s: s/5, num=4)\\n",
        "legend2 = ax.legend(handles, labels, loc='lower right', title='Total Distinct Images\\\\nProduced by City', bbox_to_anchor=(0.98, 0.05))\\n",
        "\\n",
        "plt.tight_layout()\\n",
        "plt.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/graph6_hub_spoke_scatter.png', dpi=300, bbox_inches='tight')\\n",
        "plt.show()"
    ]
}

# Instead of blindly appending, check if graph 6 exists and replace it, otherwise append.
found_idx = -1
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'markdown' and 'Graph 6: The Hub-and-Spoke Model' in "".join(cell.get('source', [])):
        found_idx = i
        break

if found_idx != -1:
    nb['cells'] = nb['cells'][:found_idx] + [markdown_cell, code_cell]
else:
    nb['cells'].append(markdown_cell)
    nb['cells'].append(code_cell)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Successfully appended Graph 6 to notebook")
