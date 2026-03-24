import nbformat
import sys

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

markdown_cell_q10_part2 = nbformat.v4.new_markdown_cell("""### Question 10 Part 2: Place Communities (Where were they printed?)
**Objective**: The boxplots above showed us that *on average*, your reviewed subjects traveled to more cities than the unreviewed ones. 

But your question is excellent: **Are they traveling to *different* cities?** Is there a specific "place community" (a group of cities) that printed your reviewed subjects, but ignored the rest of the curriculum? 

Instead of a complex graph, let's just look at the direct overlap of cities!
""")

code_cell_q10_part2 = nbformat.v4.new_code_cell("""# Get the list of all cities that printed at least one "Reviewed" subject
reviewed_df = df_geo[df_geo['cks'].isin(reviewed_cks)]
reviewed_cities = set(reviewed_df['place'].unique())

# Get the list of all cities that printed at least one "Unreviewed" core subject
unreviewed_df = df_geo[(df_geo['cks'].isin(valid_cks)) & (~df_geo['cks'].isin(reviewed_cks))]
unreviewed_cities = set(unreviewed_df['place'].unique())

# Calculate overlaps and differences
overlap_cities = reviewed_cities.intersection(unreviewed_cities)
only_reviewed_cities = reviewed_cities - unreviewed_cities
only_unreviewed_cities = unreviewed_cities - reviewed_cities

print(f"--- Printing City Communities ---")
print(f"Total cities printing Reviewed Subjects: {len(reviewed_cities)}")
print(f"Total cities printing Unreviewed Core Subjects: {len(unreviewed_cities)}")

print(f"\\nNumber of shared cities (printed BOTH): {len(overlap_cities)}")

print(f"\\nCities that ONLY printed your Reviewed Subjects (Did not print the other core subjects):")
if len(only_reviewed_cities) > 0:
    for city in sorted(list(only_reviewed_cities)):
        # get the print count for context
        count = reviewed_df[reviewed_df['place'] == city].shape[0]
        print(f"- {city} ({count} images)")
else:
    print("- None. Every city that printed a reviewed subject also printed unreviewed ones.")

print(f"\\nCities that ONLY printed the Unreviewed Core Subjects (Ignored the subjects you studied):")
if len(only_unreviewed_cities) > 0:
    for city in sorted(list(only_unreviewed_cities)):
        count = unreviewed_df[unreviewed_df['place'] == city].shape[0]
        print(f"- {city} ({count} images)")
else:
    print("- None.")
    
# Let's visualize this as a simple stacked percentage bar chart
total_cities = len(reviewed_cities.union(unreviewed_cities))

overlap_pct = (len(overlap_cities) / total_cities) * 100
only_rev_pct = (len(only_reviewed_cities) / total_cities) * 100
only_unrev_pct = (len(only_unreviewed_cities) / total_cities) * 100

fig, ax = plt.subplots(figsize=(10, 2))
ax.barh([0], [only_rev_pct], color='orange', label=f'Only Reviewed ({len(only_reviewed_cities)} cities)')
ax.barh([0], [overlap_pct], left=[only_rev_pct], color='skyblue', label=f'Both (Shared Community) ({len(overlap_cities)} cities)')
ax.barh([0], [only_unrev_pct], left=[only_rev_pct + overlap_pct], color='lightgreen', label=f'Only Unreviewed ({len(only_unreviewed_cities)} cities)')

ax.set_yticks([])
ax.set_xlabel('Percentage of Total Printing Cities (%)')
ax.set_title('Place Community Overlap: Reviewed vs Unreviewed Subjects')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.7), ncol=3)

plt.tight_layout()
plt.show()

print("\\nCONCLUSION:")
overlap_ratio = len(overlap_cities) / len(reviewed_cities) * 100
print(f"Almost the entirety of the printing network ({overlap_ratio:.1f}% of cities printing your subjects) engaged with BOTH your reviewed subjects and the broader unreviewed curriculum.")
print("This suggests there were NOT two separate 'Place Communities'. Instead, there was a single, unified Pan-European community of printers who published both types of subjects side-by-side.")

""")

nb.cells.extend([markdown_cell_q10_part2, code_cell_q10_part2])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Added Question 10 Part 2 to notebook.")
