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

markdown_cell_q9 = nbformat.v4.new_markdown_cell("""### Question 9: Content Keyword (CKS) Co-appearance Networks
**Objective**: The user asked for network graphs where the subjects themselves (**Content Keywords / CKS**) are the nodes! 
We want to see how subjects group together based on two criteria:
1.  **Geographic Co-appearance**: If two subjects are frequently printed in the *same cities*, they have a strong connection.
2.  **Temporal Co-appearance**: If two subjects are frequently printed in the *same years* across Europe, they share a temporal connection.
""")

code_cell_q9 = nbformat.v4.new_code_cell("""import networkx as nx
import itertools
from collections import Counter
import matplotlib.pyplot as plt

# We only want to look at reasonably common CKS to avoid a messy 'hairball' graph
cks_counts = df_geo['cks'].value_counts()
valid_cks = cks_counts[cks_counts >= 10].index.tolist() # Subjects that appear at least 10 times

# Filter dataset
df_cks_network = df_geo[df_geo['cks'].isin(valid_cks)]

# --- 1. GEOGRAPHIC Co-appearance ---
# For each city, what unique CKS did they print?
place_cks = df_cks_network.groupby('place')['cks'].unique().apply(list)

co_occurrences_geo = Counter()
for cks_list in place_cks:
    cks_list = sorted(list(cks_list))  # Sort to ensure (A, B) is same as (B, A)
    for pair in itertools.combinations(cks_list, 2):
        co_occurrences_geo[pair] += 1

edges_geo = pd.DataFrame([(k[0], k[1], v) for k, v in co_occurrences_geo.items()], columns=['CKS 1', 'CKS 2', 'Shared_Cities'])

# --- 2. TEMPORAL Co-appearance ---
# For each year, what unique CKS were printed?
year_cks = df_cks_network.groupby('year')['cks'].unique().apply(list)

co_occurrences_temp = Counter()
for cks_list in year_cks:
    cks_list = sorted(list(cks_list))
    for pair in itertools.combinations(cks_list, 2):
        co_occurrences_temp[pair] += 1

edges_temp = pd.DataFrame([(k[0], k[1], v) for k, v in co_occurrences_temp.items()], columns=['CKS 1', 'CKS 2', 'Shared_Years'])

# --- GRAPH DRAWING FUNCTION ---
def draw_cks_network(edge_df, weight_col, title, ax, min_edge_weight=3):
    G = nx.Graph()
    
    # Add nodes (we add all valid CKS so we can spot isolated subjects if any)
    for cks in valid_cks:
        G.add_node(cks)
        
    for _, row in edge_df.iterrows():
        # Only draw the strongest connections to keep the graph readable
        if row[weight_col] >= min_edge_weight:
            G.add_edge(row['CKS 1'], row['CKS 2'], weight=row[weight_col])
            
    # Remove nodes that ended up with 0 edges after filtering for min_edge_weight
    # Alternatively, keep them to show isolation. Let's remove them for visual clarity of clusters
    nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree == 0]
    G.remove_nodes_from(nodes_to_remove)

    pos = nx.spring_layout(G, k=0.8, seed=42)
    
    weights = [G[u][v]['weight'] for u,v in G.edges()]
    max_weight = max(weights) if weights else 1
    normalized_weights = [w / max_weight * 5 for w in weights] 

    # Node sizes based on total overall occurrences
    node_sizes = [cks_counts[node] * 7 for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightgreen', node_size=node_sizes, alpha=0.9, edgecolors='gray')
    nx.draw_networkx_edges(G, pos, ax=ax, width=normalized_weights, edge_color='gray', alpha=0.4)
    
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight='bold')

    ax.set_title(title, fontsize=14)
    ax.axis('off')

# --- PLOTTING ---
fig, axes = plt.subplots(1, 2, figsize=(22, 11))

# For Geographic, a weight of 3+ shared cities is a good threshold
draw_cks_network(edges_geo, 'Shared_Cities', 'Geographic Co-appearance\\n(Subjects printed in the same cities)', axes[0], min_edge_weight=5)

# For Temporal, a weight of 5+ shared years is a good threshold
draw_cks_network(edges_temp, 'Shared_Years', 'Temporal Co-appearance\\n(Subjects printed in the same years)', axes[1], min_edge_weight=10)

plt.tight_layout()
plt.show()

print("--- Top Subject Pairings ---")
print("\\nTop Subject Pairs by Geographic Sharing (Same Cities):")
display(edges_geo.sort_values('Shared_Cities', ascending=False).head(10).reset_index(drop=True))

print("\\nTop Subject Pairs by Temporal Sharing (Same Years):")
display(edges_temp.sort_values('Shared_Years', ascending=False).head(10).reset_index(drop=True))
""")

nb.cells.extend([markdown_cell_q9, code_cell_q9])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 9 to notebook.")
