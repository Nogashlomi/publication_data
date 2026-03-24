import nbformat as nbf
nb_path = '/Users/nogashlomi/projects/Image_data/dissertation/sharing_chapter_six.ipynb'
nb = nbf.read(nb_path, as_version=4)

markdown_cell = nbf.v4.new_markdown_cell("""### Graph 2 — The Conditions of Exact Image Sharing

Focusing only on the images that appear in more than one book, what are the conditions of their sharing? Are they monopolized by a single printing house? Do they travel to different cities?""")

code_cell = nbf.v4.new_code_cell("""# Get the list of clusters that are shared
shared_clusters = cluster_sizes[cluster_sizes > 1].index
shared_df = img_u[img_u['cluster_name'].isin(shared_clusters)].copy()

# Create a combined 'producer' field (publisher + printer)
shared_df['producer'] = shared_df['publishers'].fillna('') + " | " + shared_df['printers'].fillna('')

def analyze_sharing(df, col):
    unique_counts = df.groupby('cluster_name')[col].nunique(dropna=True)
    same = sum(unique_counts <= 1) # all books have the exact same value
    diff = sum(unique_counts > 1)
    return same, diff

same_prod, diff_prod = analyze_sharing(shared_df, 'producer')
same_place, diff_place = analyze_sharing(shared_df, 'place')

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Colors
colors_prod = ['#8ea6b4', '#d16a54'] # Same, Diff
colors_place = ['#4a9aba', '#e07b54']

# Chart 1: Printing House Sharing
axs[0].pie([same_prod, diff_prod], 
           labels=[f'Same Printer / Publisher\\n[{same_prod:,}]', f'Different Printers / Publishers\\n[{diff_prod:,}]'],
           autopct='%1.1f%%', startangle=90, colors=colors_prod, 
           textprops={'fontsize': 11, 'color': '#2c3e50', 'fontweight': 'bold'},
           wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
axs[0].set_title(f'Sharing by Printer / Publisher', fontsize=12, fontweight='bold')

# Chart 2: Geographic Sharing
axs[1].pie([same_place, diff_place], 
           labels=[f'Same City\\n[{same_place:,}]', f'Different Cities\\n[{diff_place:,}]'],
           autopct='%1.1f%%', startangle=90, colors=colors_place,
           textprops={'fontsize': 11, 'color': '#2c3e50', 'fontweight': 'bold'},
           wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
axs[1].set_title(f'Sharing by Geography', fontsize=12, fontweight='bold')

plt.suptitle(f'Graph 2: Conditions of Exact Image Sharing\\n(Total Shared Clusters: {len(shared_clusters):,})', fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()

# Save the figure
fig.savefig('/Users/nogashlomi/projects/nog_thesis/figures/corrections_round/chpater6/Graph_2_Sharing_Conditions.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Of the {len(shared_clusters):,} exact images that are shared across multiple books:")
print(f" - {diff_prod:,} ({diff_prod/len(shared_clusters)*100:.1f}%) involve books printed by DIFFERENT printers or publishers.")
print(f" - {diff_place:,} ({diff_place/len(shared_clusters)*100:.1f}%) involve books printed in DIFFERENT cities.")""")

nb.cells.extend([markdown_cell, code_cell])
nbf.write(nb, nb_path)
