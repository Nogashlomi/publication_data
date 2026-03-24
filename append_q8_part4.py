import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q8_part4 = nbformat.v4.new_markdown_cell("""### Question 8 Part 4: Temporal Mapping of City Networks
**Objective**: Representing time is a challenge when cities operate for over a century. A great way to handle this without getting too complex is to calculate the **"Center of Gravity" (Median Year)** for each city's printing activity. 
- If a city printed mostly in the 1480s, it gets an "Early" color (e.g., Yellow/Orange).
- If a city started in 1480 but printed furiously in the 1550s, its median shifts later, and it gets a "Late" color (e.g., Purple/Dark Blue).
This allows us to color-code the network graph by *Era of Peak Influence*.
""")

code_cell_q8_part4 = nbformat.v4.new_code_cell("""import matplotlib.cm as cm
import matplotlib.colors as colors

# 1. Calculate the Median Year of Activity for each city
city_temporal = df_geo.groupby('place').agg(
    median_year=('year', 'median'),
    min_year=('year', 'min'),
    max_year=('year', 'max'),
    total_images=('place', 'count')
)

# Filter to valid cities (>3 images)
city_temporal = city_temporal[city_temporal.index.isin(valid_cities)]

# 2. Set up the Colormap based on the Median Years
min_med = city_temporal['median_year'].min()
max_med = city_temporal['median_year'].max()

# Using a vibrant colormap from Early (Yellow/Orange) to Late (Purple/Dark Blue)
cmap = cm.get_cmap('plasma_r') 
norm = colors.Normalize(vmin=min_med, vmax=max_med)

# Create a color mapping dictionary for our nodes
node_colors_temporal = []
for node in G_all.nodes(): # G_all is from the previous cell
    med_year = city_temporal.loc[node, 'median_year']
    node_colors_temporal.append(cmap(norm(med_year)))

# 3. Draw the graph again with temporal coloring
plt.figure(figsize=(18, 14))

# Same layout and sizing as before
nx.draw_networkx_nodes(G_all, pos, node_color=node_colors_temporal, node_size=node_sizes, alpha=0.85, edgecolors='gray')
nx.draw_networkx_edges(G_all, pos, width=normalized_weights, edge_color='lightgray', alpha=0.5)

# Labeling top hubs and isolated nodes
nx.draw_networkx_labels(G_all, pos, labels=labels, font_size=10, font_weight='bold')

plt.title('Temporal Network of European Printing Hubs\\nNode Color = Median Year of Activity (Peak Influence)\\nNode Size = Print Volume', fontsize=16)
plt.axis('off')

# 4. Add a Colorbar to explain the timeline
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca(), orientation='horizontal', shrink=0.5, pad=0.05)
cbar.set_label('Median Year of Printing Activity', fontsize=12)

plt.show()

# Print out some interesting temporal stats
print("--- Temporal Extremes ---")
print("\\nCities with the EARLIEST Peak Influence (Median Year < 1500):")
early_cities = city_temporal[city_temporal['median_year'] < 1500].sort_values('median_year')
display(early_cities[['median_year', 'total_images']])

print("\\nCities with the LATEST Peak Influence (Median Year > 1560):")
late_cities = city_temporal[city_temporal['median_year'] > 1560].sort_values('median_year', ascending=False)
display(late_cities[['median_year', 'total_images']].head(15))
""")

nb.cells.extend([markdown_cell_q8_part4, code_cell_q8_part4])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 8 Part 4 to notebook.")
