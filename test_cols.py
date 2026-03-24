import pandas as pd
try:
    df = pd.read_csv('dissertation/full_image_data_feb_25.csv', low_memory=False)
except FileNotFoundError:
    df = pd.read_csv('full_image_data_feb_25.csv', low_memory=False)
cols = [c for c in df.columns if 'custom' in c.lower() or 'id' in c.lower()]
print(cols)
