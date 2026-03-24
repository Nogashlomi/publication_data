import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "id": "e7b0d876",
   "metadata": {},
   "source": [
    "# Scatter Plots for Meridian and Horizon Text Parts\n",
    "\n",
    "Visualizing text-parts across time and place for images where 'multiple lines' (material object (double lines)) is 'yes'."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "7dd001f3",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import ast\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import plotly.express as px\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "b3e0b230",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load datasets\n",
    "try:\n",
    "    df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)\n",
    "except FileNotFoundError:\n",
    "    df = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_image_data_feb_25.csv', low_memory=False)\n",
    "\n",
    "try:\n",
    "    books = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', low_memory=False)\n",
    "except FileNotFoundError:\n",
    "    books = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_book_data_feb_25.csv', low_memory=False)\n",
    "\n",
    "vt = pd.read_excel('/Users/nogashlomi/projects/Image_data/visual_tags/VT_2.3.xlsx')\n",
    "\n",
    "# Merge printer/publisher info\n",
    "printer_pub = books[['book', 'printers', 'publishers']].drop_duplicates(subset=['book'])\n",
    "df = df.merge(printer_pub, on='book', how='left')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "a9a2a912",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Filter visual tags for \"multiple lines\" ('material object (double lines)' == 'yes')\n",
    "double_lines_clusters = vt[vt['material object (double lines)'] == 'yes']['cluster_name'].tolist()\n",
    "\n",
    "# Target CKs\n",
    "target_cks = ['CK_Horizon', 'CK_Meridian', 'CK_Meridian Dial']\n",
    "\n",
    "# Ensure cks is string\n",
    "df['cks'] = df['cks'].astype(str)\n",
    "\n",
    "# Apply filters\n",
    "mask_cks = df['cks'].apply(lambda x: any(ck in x for ck in target_cks))\n",
    "mask_cluster = df['cluster_name'].isin(double_lines_clusters)\n",
    "\n",
    "filtered_df = df[mask_cks & mask_cluster].copy()\n",
    "\n",
    "print(f\"Total images matching criteria: {len(filtered_df)}\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d7a4b8df",
   "metadata": {},
   "source": [
    "### Data Cleaning for Plots"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "f5f5f5f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "filtered_df['custom_identifier_str'] = filtered_df['custom_identifier'].astype(str)\n",
    "\n",
    "filtered_df['year'] = pd.to_numeric(filtered_df['year'], errors='coerce')\n",
    "plot_df = filtered_df.dropna(subset=['year', 'place']).copy()\n",
    "\n",
    "plot_df = plot_df.sort_values(by=['place', 'year'])\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a1b2c3d4",
   "metadata": {},
   "source": [
    "### 1. Static Scatter Plot (Y = Place, Color = Custom ID)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "e4e4e4e4",
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(12, 8))\n",
    "\n",
    "sns.scatterplot(\n",
    "    data=plot_df,\n",
    "    x='year',\n",
    "    y='place',\n",
    "    hue='custom_identifier_str',\n",
    "    palette='tab20',\n",
    "    s=100,\n",
    "    alpha=0.7,\n",
    "    edgecolor='w',\n",
    "    linewidth=0.5\n",
    ")\n",
    "\n",
    "plt.title('Text Parts (Multiple Lines) Over Time and Place\\nHorizon & Meridian Images', fontsize=16)\n",
    "plt.xlabel('Year', fontsize=12)\n",
    "plt.ylabel('Place', fontsize=12)\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., title='Custom ID')\n",
    "plt.tight_layout()\n",
    "\n",
    "plt.savefig('/Users/nogashlomi/Desktop/horizon_meridian_lines.png', dpi=300)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b5c6d7e8",
   "metadata": {},
   "source": [
    "### 2. Interactive Scatter Plot (Y = Place, Color = Custom ID)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "f6f6f6f6",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig_interactive = px.scatter(\n",
    "    plot_df,\n",
    "    x='year',\n",
    "    y='place',\n",
    "    color='custom_identifier_str',\n",
    "    hover_data=['part_or_adaption_label', 'part_or_adaption', 'part_type', 'cks', 'bid'],\n",
    "    title='Interactive Plot: Horizon & Meridian Multiple Lines (Y=Place)',\n",
    "    labels={'custom_identifier_str': 'Custom ID'}\n",
    ")\n",
    "\n",
    "fig_interactive.update_traces(marker=dict(size=10, opacity=0.8))\n",
    "fig_interactive.update_layout(height=800, hovermode='closest')\n",
    "fig_interactive.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c1b2c3d4",
   "metadata": {},
   "source": [
    "### 3. Static Scatter Plot (Y = Custom ID, Color = Place)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "d4e4e4e4",
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(12, 10))\n",
    "\n",
    "sns.scatterplot(\n",
    "    data=plot_df,\n",
    "    x='year',\n",
    "    y='custom_identifier_str',\n",
    "    hue='place',\n",
    "    palette='tab20',\n",
    "    s=100,\n",
    "    alpha=0.7,\n",
    "    edgecolor='w',\n",
    "    linewidth=0.5\n",
    ")\n",
    "\n",
    "plt.title('Text Parts (Multiple Lines) by Text ID Over Time\\nHorizon & Meridian Images', fontsize=16)\n",
    "plt.xlabel('Year', fontsize=12)\n",
    "plt.ylabel('Custom ID', fontsize=12)\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., title='Place')\n",
    "plt.tight_layout()\n",
    "\n",
    "plt.savefig('/Users/nogashlomi/Desktop/horizon_meridian_lines_by_id.png', dpi=300)\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a5c6d7e8",
   "metadata": {},
   "source": [
    "### 4. Interactive Scatter Plot (Y = Custom ID, Color = Place)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "a6f6f6f6",
   "metadata": {},
   "outputs": [],
   "source": [
    "fig_interactive2 = px.scatter(\n",
    "    plot_df,\n",
    "    x='year',\n",
    "    y='custom_identifier_str',\n",
    "    color='place',\n",
    "    hover_data=['part_or_adaption_label', 'part_or_adaption', 'part_type', 'cks', 'bid'],\n",
    "    title='Interactive Plot: Horizon & Meridian Multiple Lines (Y=Custom ID)',\n",
    "    labels={'custom_identifier_str': 'Custom ID'}\n",
    ")\n",
    "\n",
    "fig_interactive2.update_traces(marker=dict(size=10, opacity=0.8))\n",
    "fig_interactive2.update_layout(height=800, hovermode='closest')\n",
    "fig_interactive2.show()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open('/Users/nogashlomi/projects/Image_data/dissertation/SA_2.3_horizon_meridian_scatter.ipynb', 'w') as f:
    json.dump(notebook_content, f, indent=1)

print("Notebook created successfully.")

# And let's generate the static plot to save to the Desktop:

# 1. Load data
try:
    df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)
except FileNotFoundError:
    df = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_image_data_feb_25.csv', low_memory=False)

try:
    books = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', low_memory=False)
except FileNotFoundError:
    books = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_book_data_feb_25.csv', low_memory=False)

vt = pd.read_excel('/Users/nogashlomi/projects/Image_data/visual_tags/VT_2.3.xlsx')

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


plt.figure(figsize=(12, 10))

sns.scatterplot(
    data=plot_df,
    x='year',
    y='custom_identifier_str',
    hue='place',
    palette='tab20',
    s=100,
    alpha=0.7,
    edgecolor='w',
    linewidth=0.5
)

plt.title('Text Parts (Multiple Lines) by Text ID Over Time\nHorizon & Meridian Images', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Custom ID', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., title='Place')
plt.tight_layout()

plt.savefig('/Users/nogashlomi/Desktop/horizon_meridian_lines_by_id.png', dpi=300)
print("Saved scatter plot to Desktop/horizon_meridian_lines_by_id.png")

