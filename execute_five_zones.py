import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px

def execute_analysis():
    # Load Data
    df = pd.read_csv('dissertation/full_image_data_feb_25.csv')
    books = pd.read_csv('dissertation/full_book_data_feb_25.csv')
    vt = pd.read_excel('visual_tags/VT_2.4_five_zones.xlsx')
    
    # Filter for Five Zones CK
    five_zones_df = df[df['cks'].str.contains('CK_Five Zones', na=False)].copy()
    
    # Merge with visual tags
    merged_df = five_zones_df.merge(vt, on='cluster_name', how='inner')
    
    # Create text_part and custom_identifier_str
    def get_text_part(row):
        parts = []
        if pd.notna(row['custom_identifier']):
            parts.append(str(row['custom_identifier']))
        if pd.notna(row['part_or_adaption_label']):
            parts.append(str(row['part_or_adaption_label']))
        return ' - '.join(parts)
    
    merged_df['text_part'] = merged_df.apply(get_text_part, axis=1)
    merged_df['custom_identifier_str'] = merged_df['custom_identifier'].astype(str)
    
    # Filtering for Specific Categories
    curved_line = merged_df[merged_df['motion of the sun two dimensional rep curved line'] == 'yes'].copy()
    straight_line = merged_df[merged_df['motion of the sun two dimensional rep straight line'] == 'yes'].copy()
    double_sphere = merged_df[merged_df['earth and cosmos'] == 'yes'].copy()
    
    curved_line['category'] = 'Curved Line'
    straight_line['category'] = 'Straight Line'
    double_sphere['category'] = 'Double Sphere'
    
    plot_df = pd.concat([curved_line, straight_line, double_sphere])
    
    if plot_df.empty:
        print('No data found for the specified categories.')
        return

    # Static Plot
    plt.figure(figsize=(15, 10))
    sns.scatterplot(data=plot_df, x='year', y='custom_identifier_str', hue='place', style='category', s=100)
    plt.title('Five Zones Images by Year and Custom ID')
    plt.xlabel('Year')
    plt.ylabel('Custom ID')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    output_path = os.path.expanduser('~/Desktop/five_zones_scatter_by_id.png')
    plt.savefig(output_path)
    print(f'Static plot saved to: {output_path}')
    
    # Save a copy to artifacts directory for walkthrough
    artifact_path = '/Users/nogashlomi/.gemini/antigravity/brain/128d5081-ede9-40af-bdce-8b7265364406/five_zones_scatter_by_id.png'
    plt.savefig(artifact_path)
    print(f'Artifact saved to: {artifact_path}')

if __name__ == '__main__':
    execute_analysis()
