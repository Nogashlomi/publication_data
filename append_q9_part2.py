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

markdown_cell_q9_part2 = nbformat.v4.new_markdown_cell("""### Question 9 Part 2: Filtering the "Hairball" (The Core Curriculum)
**Objective**: As observed, analyzing the full network of subjects creates a massive, unreadable hairball. This is an exciting finding: it means the entire visual tradition of these astronomy texts was a tightly interconnected, **Pan-European standardized language**, rather than distinct regional silos.

However, to make the graph readable and see what sits at the very heart of this hairball, we must significantly raise the threshold. We will now only draw connections if two subjects were printed together in **15+ distinct cities** or **30+ distinct years**. This will strip away the noise and reveal the absolute "Core Curriculum."
""")

code_cell_q9_part2 = nbformat.v4.new_code_cell("""# We reuse the edges_geo and edges_temp from the previous cell, but drastically increase the threshold!

fig, axes = plt.subplots(1, 2, figsize=(22, 11))

# Previously 5, now we require them to be printed in the same 15+ unique cities
draw_cks_network(edges_geo, 'Shared_Cities', 'CORE Geographic Co-appearance\\n(Subjects sharing 15+ Cities)', axes[0], min_edge_weight=15)

# Previously 10, now we require them to be printed in the same 30+ unique years
draw_cks_network(edges_temp, 'Shared_Years', 'CORE Temporal Co-appearance\\n(Subjects sharing 30+ Years)', axes[1], min_edge_weight=30)

plt.tight_layout()
plt.show()

print("This filtered view reveals the absolute 'Core Curriculum' of subjects that were printed constantly, everywhere together.")
""")

nb.cells.extend([markdown_cell_q9_part2, code_cell_q9_part2])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 9 Part 2 to notebook.")
