import pandas as pd
import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q8_part2 = nbformat.v4.new_markdown_cell("""### Question 8 Part 2: Visualizing City Networks with Graphs
**Objective**: A network graph shows the geographic structure of the printing trade much better than a heatmap. We also want to answer the user's question: "Do cities behave differently if we look at the broad *Subjects* (CKS) they share, rather than the specific *Visual Clusters*?" Let's build both networks and compare them!
""")

code_cell_q8_part2 = nbformat.v4.new_code_cell("""import networkx as nx

# 1. Prepare Data for CKS (Concept) Co-occurrences
cks_places = df_geo.groupby('cks')['place'].unique().apply(list)
cks_places = cks_places[cks_places.apply(len) > 1]

co_occurrences_cks = Counter()
for places in cks_places:
    places = sorted(places)
    for pair in itertools.combinations(places, 2):
        co_occurrences_cks[pair] += 1

edges_cks = pd.DataFrame([(k[0], k[1], v) for k, v in co_occurrences_cks.items()], columns=['City 1', 'City 2', 'Shared_CKS'])
edges_cks = edges_cks.sort_values('Shared_CKS', ascending=False)

# 2. Build Network Graphs
# We will look at the top cities to keep the graph readable
top_n = 20
top_cities_list = df_geo['place'].value_counts().head(top_n).index.tolist()

# Filter edges to only include top cities
edges_clust_filtered = edges[(edges['City 1'].isin(top_cities_list)) & (edges['City 2'].isin(top_cities_list))]
edges_cks_filtered = edges_cks[(edges_cks['City 1'].isin(top_cities_list)) & (edges_cks['City 2'].isin(top_cities_list))]


def draw_city_network(edge_df, weight_col, title, ax):
    G = nx.Graph()
    for _, row in edge_df.iterrows():
        # Only add edge if weight is significant enough to declutter, or just add all within top N
        if row[weight_col] > 0: 
            G.add_edge(row['City 1'], row['City 2'], weight=row[weight_col])
    
    # Position nodes using spring layout
    pos = nx.spring_layout(G, k=0.9, seed=42)
    
    # Edge weights for thickness
    weights = [G[u][v]['weight'] for u,v in G.edges()]
    max_weight = max(weights) if weights else 1
    normalized_weights = [w / max_weight * 5 for w in weights] # Scale thickness max to 5
    
    # Node sizes based on degree or total appearances
    node_sizes = [df_geo[df_geo['place'] == node].shape[0] * 3 for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='skyblue', node_size=node_sizes, alpha=0.8, edgecolors='white')
    nx.draw_networkx_edges(G, pos, ax=ax, width=normalized_weights, edge_color='gray', alpha=0.5)
    
    # Labels with background for readability
    labels = nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')

    ax.set_title(title, fontsize=14)
    ax.axis('off')

# Plot side by side
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

draw_city_network(edges_clust_filtered, 'Shared_Clusters', 'City Network: Shared Specific Visuals (Clusters)', axes[0])
draw_city_network(edges_cks_filtered, 'Shared_CKS', 'City Network: Shared Abstract Concepts (CKS)', axes[1])

plt.tight_layout()
plt.show()

print("--- Data Comparison ---")
print(f"Top 10 city pairs sharing VISUALS (Clusters):")
display(edges.head(10).reset_index(drop=True))
print(f"\\nTop 10 city pairs sharing CONCEPTS (CKS):")
display(edges_cks.head(10).reset_index(drop=True))
""")

nb.cells.extend([markdown_cell_q8_part2, code_cell_q8_part2])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Network Graph code to notebook.")
