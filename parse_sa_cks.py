import glob
import re
import nbformat
import sys
import pandas as pd

# Find all SA*.ipynb files
notebook_files = glob.glob('/Users/nogashlomi/projects/Image_data/dissertation/SA*.ipynb')

reviewed_cks = set()

# Regex to find anything starting with 'CK_' and ending with quote inside the files
ck_pattern = re.compile(r"'(CK_[^']+)'")

for file in notebook_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    source = cell.source
                    # Check if target_cks is defined in this cell
                    if 'target_cks' in source:
                        matches = ck_pattern.findall(source)
                        reviewed_cks.update(matches)
    except Exception as e:
        print(f"Error reading {file}: {e}")

reviewed_cks_list = sorted(list(reviewed_cks))
print("Reviewed CKS found:", len(reviewed_cks_list))
for ck in reviewed_cks_list:
    print(f"- {ck}")

# Now append this to the main sandbox notebook
sandbox_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'
try:
    with open(sandbox_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q9_part3 = nbformat.v4.new_markdown_cell("""### Question 9 Part 3: Highlighting Reviewed Subjects
**Objective**: We want to take the filtered Core Curriculum graphs and **highlight the specific subjects you have already reviewed** in your `SA_*.ipynb` notebooks. 

This will show us exactly where your current dissertation research sits within the broader Pan-European curriculum. Are you focusing on the central nodes, or some of the edge subjects?

*Highlighted in Orange: Subjects you have reviewed.*
*Highlighted in Light Green: Other core subjects.*
""")

code_cell_q9_part3 = nbformat.v4.new_code_cell(f"""# The list of CKS extracted from the SA*.ipynb notebooks:
reviewed_cks = {reviewed_cks_list}

def draw_cks_network_highlighted(edge_df, weight_col, title, ax, min_edge_weight=3):
    G = nx.Graph()
    
    for cks in valid_cks:
        G.add_node(cks)
        
    for _, row in edge_df.iterrows():
        if row[weight_col] >= min_edge_weight:
            G.add_edge(row['CKS 1'], row['CKS 2'], weight=row[weight_col])
            
    nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree == 0]
    G.remove_nodes_from(nodes_to_remove)

    pos = nx.spring_layout(G, k=0.8, seed=42)
    
    weights = [G[u][v]['weight'] for u,v in G.edges()]
    max_weight = max(weights) if weights else 1
    normalized_weights = [w / max_weight * 5 for w in weights] 

    node_sizes = [cks_counts[node] * 7 for node in G.nodes()]
    
    # --- HIGHLIGHTING LOGIC ---
    # Orange if reviewed, light green if not
    node_colors = ['orange' if node in reviewed_cks else 'lightgreen' for node in G.nodes()]
    
    # We can also make the reviewed nodes larger to stand out more
    highlighted_node_sizes = [size * 1.5 if node in reviewed_cks else size for node, size in zip(G.nodes(), node_sizes)]

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=highlighted_node_sizes, alpha=0.9, edgecolors='gray')
    nx.draw_networkx_edges(G, pos, ax=ax, width=normalized_weights, edge_color='gray', alpha=0.4)
    
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight='bold')

    ax.set_title(title, fontsize=14)
    ax.axis('off')

# --- PLOTTING ---
fig, axes = plt.subplots(1, 2, figsize=(22, 11))

# For Geographic, a weight of 15+ shared cities is a good threshold for the core
draw_cks_network_highlighted(edges_geo, 'Shared_Cities', 'CORE Geographic Co-appearance\\n(Orange = Reviewed in SA Notebooks)', axes[0], min_edge_weight=15)

# For Temporal, a weight of 30+ shared years is a good threshold for the core
draw_cks_network_highlighted(edges_temp, 'Shared_Years', 'CORE Temporal Co-appearance\\n(Orange = Reviewed in SA Notebooks)', axes[1], min_edge_weight=30)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Reviewed Subjects', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Unreviewed Core Subjects', markerfacecolor='lightgreen', markersize=10)
]
axes[0].legend(handles=legend_elements, loc='upper right', fontsize=12)

plt.tight_layout()
plt.show()

print("This graph shows where your current analysis sits within the broader network!")
""")

nb.cells.extend([markdown_cell_q9_part3, code_cell_q9_part3])

with open(sandbox_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Appended Q9 Part 3 to notebook.")

