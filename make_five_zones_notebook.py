import json
import pandas as pd

def create_notebook():
    cells = []
    
    # Cell 1: Imports
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import plotly.express as px\n",
            "import seaborn as sns\n",
            "import matplotlib.pyplot as plt\n",
            "import os"
        ]
    })
    
    # Cell 2: Load Data
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "df = pd.read_csv('full_image_data_feb_25.csv')\n",
            "vt = pd.read_excel('visual_tags/VT_2.4_five_zones.xlsx')\n",
            "print(f'Loaded {len(df)} images and {len(vt)} visual tags.')"
        ]
    })
    
    # Cell 3: Data Merging and Preprocessing
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Filter for Five Zones CK\n",
            "five_zones_df = df[df['cks'].str.contains('CK_Five Zones', na=False)].copy()\n",
            "\n",
            "# Merge with visual tags\n",
            "merged_df = five_zones_df.merge(vt, on='cluster_name', how='inner')\n",
            "\n",
            "# Create a display string for the text part (Custom ID + Part/Adaption)\n",
            "def get_text_part(row):\n",
            "    parts = []\n",
            "    if pd.notna(row['custom_identifier']):\n",
            "        parts.append(str(row['custom_identifier']))\n",
            "    if pd.notna(row['part_or_adaption_label']):\n",
            "        parts.append(str(row['part_or_adaption_label']))\n",
            "    return ' - '.join(parts)\n",
            "\n",
            "merged_df['text_part'] = merged_df.apply(get_text_part, axis=1)\n",
            "merged_df['custom_identifier_str'] = merged_df['custom_identifier'].astype(str)\n",
            "\n",
            "print(f'Filtered to {len(merged_df)} images with Five Zones visual tags.')"
        ]
    })
    
    # Cell 4: Filtering for Specific Categories
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "curved_line = merged_df[merged_df['motion of the sun two dimensional rep curved line'] == 'yes'].copy()\n",
            "straight_line = merged_df[merged_df['motion of the sun two dimensional rep straight line'] == 'yes'].copy()\n",
            "double_sphere = merged_df[merged_df['earth and cosmos'] == 'yes'].copy()\n",
            "\n",
            "curved_line['category'] = 'Curved Line'\n",
            "straight_line['category'] = 'Straight Line'\n",
            "double_sphere['category'] = 'Double Sphere'\n",
            "\n",
            "plot_df = pd.concat([curved_line, straight_line, double_sphere])\n",
            "print(f'Categories: Curved ({len(curved_line)}), Straight ({len(straight_line)}), Double Sphere ({len(double_sphere)})')"
        ]
    })
    
    # Cell 5: Static Plot
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "plt.figure(figsize=(15, 10))\n",
            "sns.scatterplot(data=plot_df, x='year', y='custom_identifier_str', hue='place', style='category', s=100)\n",
            "plt.title('Five Zones Images by Year and Custom ID')\n",
            "plt.xlabel('Year')\n",
            "plt.ylabel('Custom ID')\n",
            "plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')\n",
            "plt.tight_layout()\n",
            "plt.savefig(os.path.expanduser('~/Desktop/five_zones_scatter.png'))\n",
            "plt.show()"
        ]
    })
    
    # Cell 6: Interactive Plot
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig = px.scatter(plot_df, x='year', y='custom_identifier_str', color='place', \n",
            "                 symbol='category', hover_data=['text_part', 'images'],\n",
            "                 title='Interactive Five Zones Scatter Plot')\n",
            "fig.update_layout(height=800)\n",
            "fig.show()"
        ]
    })

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    with open('dissertation/SA_2.4_five_zones_scatter.ipynb', 'w') as f:
        json.dump(notebook, f, indent=4)
    print('Notebook created: dissertation/SA_2.4_five_zones_scatter.ipynb')

if __name__ == '__main__':
    create_notebook()
