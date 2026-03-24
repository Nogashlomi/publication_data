import nbformat

notebook_path = '/Users/nogashlomi/projects/Image_data/history_data_analysis_sandbox.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

markdown_cell_q3 = nbformat.v4.new_markdown_cell("""## Question 3: Comparing the Four Chapters of Tractatus
**Objective**: Look at the variation ratio (`Unique Clusters / Total Images`) across the four different chapters you examined (from `images_with_chapters_2024-10-14.xlsx`).

We will:
1. Examine the **overall variation** per chapter.
2. See what the content variation looks like *within* the specific keywords assigned to each chapter.""")

code_cell_q3 = nbformat.v4.new_code_cell("""# Load the chapters mapping
df_chapters = pd.read_excel('images_with_chapters_2024-10-14.xlsx')

# Clean the chapter column to just the main 4 chapters (ignoring the edge case splits for now)
def extract_primary_chapter(chap_str):
    if pd.isna(chap_str): return None
    chap_str = str(chap_str)
    if 'Tractatus Chapter 1' in chap_str: return 'Chapter 1'
    if 'Tractatus Chapter 2' in chap_str: return 'Chapter 2'
    if 'Tractatus Chapter 3' in chap_str: return 'Chapter 3'
    if 'Tractatus Chapter 4' in chap_str: return 'Chapter 4'
    return None

df_chapters['primary_chapter'] = df_chapters['chapter'].apply(extract_primary_chapter)

# Filter out empty ones
df_chaps_clean = df_chapters.dropna(subset=['primary_chapter']).copy()

# Step 1: Overall Variation Ratio per Chapter
chapter_overall = df_chaps_clean.groupby('primary_chapter').agg(
    total_images=('images', 'count'),
    unique_clusters=('cluster_name', 'nunique')
).reset_index()

chapter_overall['variation_ratio'] = chapter_overall['unique_clusters'] / chapter_overall['total_images']

print("--- Overall Variation Ratio By Chapter ---")
display(chapter_overall)

# Plotting overall chapter variation
plt.figure(figsize=(8, 5))
sns.barplot(data=chapter_overall, x='primary_chapter', y='variation_ratio', palette='viridis')
plt.title('Overall Variation Ratio by Tractatus Chapter')
plt.ylabel('Variation Ratio (Unique Clusters / Total Images)')
plt.xlabel('Chapter')
for i, v in enumerate(chapter_overall['variation_ratio']):
    plt.text(i, v + 0.005, f"{v:.3f}", ha='center')
plt.show()

# Step 2: Content Keyword Variation WITHIN each Chapter
# What's the average variation ratio of the keywords in each chapter?
# First, group by chapter AND keyword (cks)
chap_kw_stats = df_chaps_clean.dropna(subset=['cks']).groupby(['primary_chapter', 'cks']).agg(
    total_images=('images', 'count'),
    unique_clusters=('cluster_name', 'nunique')
).reset_index()

chap_kw_stats['variation_ratio'] = chap_kw_stats['unique_clusters'] / chap_kw_stats['total_images']

# Filter to meaningful keywords (e.g. at least 10 images)
chap_kw_stats = chap_kw_stats[chap_kw_stats['total_images'] >= 10]

# Now, average the variation ratio across keywords for each chapter
chap_avg_kw_variation = chap_kw_stats.groupby('primary_chapter')['variation_ratio'].mean().reset_index()

print("\\n--- Average Variation Ratio of Keywords Within Each Chapter ---")
display(chap_avg_kw_variation)

# To see the distribution of keywords per chapter, a boxplot is great!
plt.figure(figsize=(10, 6))
sns.boxplot(data=chap_kw_stats, x='primary_chapter', y='variation_ratio', palette='Set2')
sns.stripplot(data=chap_kw_stats, x='primary_chapter', y='variation_ratio', color='black', alpha=0.5)
plt.title('Distribution of Keyword Variation Ratios Within Chapters')
plt.ylabel('Variation Ratio of a Keyword')
plt.xlabel('Chapter')
plt.show()""")

nb.cells.extend([markdown_cell_q3, code_cell_q3])

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
