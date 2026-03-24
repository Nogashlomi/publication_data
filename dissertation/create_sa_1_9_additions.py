import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1: imports and config
cell1 = nbf.v4.new_code_cell("""\
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_image_data_feb_25.csv', low_memory=False)
books = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_book_data_feb_25.csv', low_memory=False)

# Add printer and publisher
df['printer'] = df['book'].map(books.set_index('book')['printers'])
df['publisher'] = df['book'].map(books.set_index('book')['publishers'])
""")

# Cell 2: Target CKs
cell2 = nbf.v4.new_code_cell("""\
target_cks = [
    'CK_Measurements of the Earth',
    'CK_Correlation Between Distances on Earth and Locations of Stars', 
    'CK_Circle and Diameter Rule', 
    'CK_Assumed Parallellity of the Sun Rays',
    'CK_Planets Sizes and Distances'
]

# Step 1: Filter the DataFrame for rows where 'cks' is in the target_cks list
filtered_df_target_cks = df[df['cks'].isin(target_cks)]

# Step 2: Get the unique 'images' values associated with the target cks
images_with_target_cks = filtered_df_target_cks['images'].unique()

# Step 3: Filter the original DataFrame to include all rows that have these images
filtered_df = df[df['images'].isin(images_with_target_cks)]

# Step 4: Drop other CKs attached to these images
filtered_df = filtered_df[filtered_df['cks'].isin(target_cks)]

# Drop na
filtered_df = filtered_df.dropna(subset=['year', 'place', 'custom_identifier']).copy()

# Convert custom_identifier to an integer (if applicable) then to string
try:
    filtered_df['custom_identifier_str'] = filtered_df['custom_identifier'].astype(float).astype(int).astype(str)
except:
    filtered_df['custom_identifier_str'] = filtered_df['custom_identifier'].astype(str)
""")

# Cell 3: Load Visual Tags and Merge
cell3 = nbf.v4.new_code_cell("""\
visual_tags = pd.read_excel('/Users/nogashlomi/projects/Image_data/visual_tags/VT_1.9.xlsx')
visual_df = pd.merge(filtered_df, visual_tags, on='cluster_name')

# Focus on the 'Diagram' visual tag (column is likely 'diagram')
if 'Diagram' in visual_df.columns:
    diagram_df = visual_df[visual_df['Diagram'] == 1].copy()
elif 'diagram' in visual_df.columns:
    diagram_df = visual_df[visual_df['diagram'] == 1].copy()
else:
    diagram_df = visual_df.copy()
    print("Warning: Diagram tag not found in visual_df")
""")

# Cell 4: Scatter plots
cell4 = nbf.v4.new_code_cell("""\
import os

# For each subgroup (target CK), generate a scatter plot
for keyword in target_cks:
    subgroup_df = diagram_df[diagram_df['cks'] == keyword]
    
    if subgroup_df.empty:
        print(f"No diagram images found for {keyword}")
        continue
    
    # Optional: order places by value counts or alphabetically for consistency
    place_order = sorted(subgroup_df['place'].unique())
    
    plt.figure(figsize=(14, 12))
    sns.scatterplot(
        data=subgroup_df,
        x='year',
        y='place',
        hue='custom_identifier_str',
        palette='tab20',
        s=80,
        alpha=0.7,
        legend=False,
        order=place_order
    )
    plt.title(f'Printings of {keyword} (Diagrams only)\\nOver Time and Place (Colored by custom_id)', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Place', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    filename = f"{keyword.replace(' ', '_').replace('/', '_')}_diagram_scatter.png"
    # plt.savefig(f"/Users/nogashlomi/Desktop/{filename}", dpi=300)
    plt.show()
""")

nb.cells = [cell1, cell2, cell3, cell4]

with open('/Users/nogashlomi/projects/Image_data/dissertation/SA_1.9_additions.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook successfully generated: SA_1.9_additions.ipynb")
