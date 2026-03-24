import pandas as pd

df = pd.read_csv('/Users/nogashlomi/projects/Image_data/full_image_data_feb_25.csv')
target_cks = [
    'CK_Measurements of the Earth',
    'CK_Correlation Between Distances on Earth and Locations of Stars', 
    'CK_Circle and Diameter Rule', 
    'CK_Assumed Parallellity of the Sun Rays',
    'CK_Planets Sizes and Distances'
]

filtered_df_target_cks = df[df['cks'].isin(target_cks)]
images_with_target_cks = filtered_df_target_cks['images'].unique()
filtered_df = df[df['images'].isin(images_with_target_cks)]
filtered_df = filtered_df[filtered_df['cks'].isin(target_cks)]

visual_tags = pd.read_excel('/Users/nogashlomi/projects/Image_data/visual_tags/VT_1.9.xlsx')
visual_df = pd.merge(filtered_df, visual_tags, on='cluster_name')

print("Diagram values:", visual_df['diagram'].unique())
