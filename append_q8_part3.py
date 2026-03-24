import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q8_part3 = nbformat.v4.new_markdown_cell("""### Question 8 Part 3: The Complete Visual Network (Including Isolated Cities)
**Objective**: The user rightly pointed out we shouldn't just look at who is connected, but who is *isolated*. Who printed these books completely on their own, using their own distinct visual programs without sharing clusters with anyone else?
Here, we build a network graph of ALL cities (that printed at least 3 images to filter out noise) and show the isolated nodes!
""")

code_cell_q8_part3 = nbformat.v4.new_code_cell("""import networkx as nx

# Get all cities that printed at least a few images (let's say > 3 images to filter noise)
city_counts = df_geo['place'].value_counts()
valid_cities = city_counts[city_counts > 3].index.tolist()

# Filter our edges to only these valid cities
edges_all_filtered = edges[(edges['City 1'].isin(valid_cities)) & (edges['City 2'].isin(valid_cities))]

G_all = nx.Graph()

# 1. Add ALL valid cities as nodes FIRST (this guarantees isolated cities are included)
for city in valid_cities:
    G_all.add_node(city)

# 2. Add the edges (connections based on shared clusters)
for _, row in edges_all_filtered.iterrows():
    if row['Shared_Clusters'] > 0:
        G_all.add_edge(row['City 1'], row['City 2'], weight=row['Shared_Clusters'])

# Prepare drawing parameters
pos = nx.spring_layout(G_all, k=0.5, iterations=50, seed=42) # Spread them out

# Differentiate isolated nodes from connected nodes by color
isolated_nodes = list(nx.isolates(G_all))
node_colors = ['salmon' if node in isolated_nodes else 'skyblue' for node in G_all.nodes()]

# Size nodes based on how many total images they printed
node_sizes = [city_counts[node] * 2 for node in G_all.nodes()]

# Edge thickness based on weight
weights = [G_all[u][v]['weight'] for u,v in G_all.edges()]
max_weight = max(weights) if weights else 1
normalized_weights = [(w / max_weight) * 3 for w in weights]


plt.figure(figsize=(16, 12))

# Draw the network
nx.draw_networkx_nodes(G_all, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8, edgecolors='white')
nx.draw_networkx_edges(G_all, pos, width=normalized_weights, edge_color='gray', alpha=0.4)

# Only label the isolated nodes and the top 15 biggest hubs to avoid text overlap
labels = {}
top_15_hubs = city_counts.head(15).index.tolist()
for node in G_all.nodes():
    if node in isolated_nodes or node in top_15_hubs:
        labels[node] = node

nx.draw_networkx_labels(G_all, pos, labels=labels, font_size=9, font_weight='bold')

# Custom Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Connected City (Shares Visuals)', markerfacecolor='skyblue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Isolated City (Unique Visual Program)', markerfacecolor='salmon', markersize=10)
]
plt.legend(handles=legend_elements, loc='upper right', fontsize=12)

plt.title('The Complete European Printing Network (Shared Visual Clusters)\\nNode Size = Print Volume. Red Nodes = Completely Isolated', fontsize=16)
plt.axis('off')
plt.show()

print(f"Total Printing Cities Analyzed (with >3 images): {len(valid_cities)}")
print(f"Isolated Cities (No shared clusters with anyone): {len(isolated_nodes)}")
print("\\nList of Isolated Cities with their own distinct visual programs:")
for city in isolated_nodes:
    print(f"- {city} ({city_counts[city]} images printed)")
""")

nb.cells.extend([markdown_cell_q8_part3, code_cell_q8_part3])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 8 Part 3 to notebook.")
