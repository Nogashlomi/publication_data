import pandas as pd
df = pd.read_csv('dissertation/full_image_data_feb_25.csv')
print("Columns in image data:", df.columns.tolist())
five_zones = df[df['cks'].str.contains('CK_Five Zones', na=False)]
print("Sample rows for Five Zones:")
print(five_zones[['year', 'place']].head())
