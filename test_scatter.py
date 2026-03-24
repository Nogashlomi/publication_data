import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. Load data
try:
    df = pd.read_csv('dissertation/full_image_data_feb_25.csv', low_memory=False)
except FileNotFoundError:
    df = pd.read_csv('full_image_data_feb_25.csv', low_memory=False)

try:
    books = pd.read_csv('dissertation/full_book_data_feb_25.csv', low_memory=False)
except FileNotFoundError:
    books = pd.read_csv('full_book_data_feb_25.csv', low_memory=False)

vt = pd.read_excel('visual_tags/VT_2.3.xlsx')

# Merge printer/publisher
printer_pub = books[['book', 'printers', 'publishers']].drop_duplicates(subset=['book'])
df = df.merge(printer_pub, on='book', how='left')

# 2. Filter visual tags for "material object (double lines)" == 'yes'
double_lines_clusters = vt[vt['material object (double lines)'] == 'yes']['cluster_name'].tolist()

# 3. Filter main df
# Target CKs
target_cks = ['CK_Horizon', 'CK_Meridian', 'CK_Meridian Dial']
# Convert cks to string just in case
df['cks'] = df['cks'].astype(str)

mask_cks = df['cks'].apply(lambda x: any(ck in x for ck in target_cks))
mask_cluster = df['cluster_name'].isin(double_lines_clusters)

filtered_df = df[mask_cks & mask_cluster].copy()

filtered_df['custom_identifier_str'] = filtered_df['custom_identifier'].astype(str)

# Data Cleaning
filtered_df['year'] = pd.to_numeric(filtered_df['year'], errors='coerce')
plot_df = filtered_df.dropna(subset=['year', 'place']).copy()

plot_df = plot_df.sort_values(by=['place', 'year'])

# Static Scatter Plot
plt.figure(figsize=(12, 8))

sns.scatterplot(
    data=plot_df,
    x='year',
    y='place',
    hue='custom_identifier_str',
    palette='tab20',
    s=100,
    alpha=0.7,
    edgecolor='w',
    linewidth=0.5
)

plt.title('Text Parts (Multiple Lines) Over Time and Place\nHorizon & Meridian Images', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Place', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., title='Custom ID')
plt.tight_layout()

plt.savefig('/Users/nogashlomi/Desktop/horizon_meridian_lines.png', dpi=300)
print("Saved scatter plot to Desktop/horizon_meridian_lines.png")
