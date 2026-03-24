import pandas as pd
df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', low_memory=False)
lines_cols = [c for c in df.columns if 'line' in c.lower() or 'multiple' in c.lower()]
text_cols = [c for c in df.columns if 'text' in c.lower() or 'part' in c.lower() or 'adaption' in c.lower() or 'custom' in c.lower()]
print("Lines cols:", lines_cols)
print("Text cols:", text_cols)
print("CKs related to horizon/meridian:")
print(df[df['cks'].astype(str).str.contains('Horizon|Meridian')]['cks'].unique())

print("\nValue counts for multiple lines:")
for col in lines_cols:
    if 'multiple' in col:
        print(f"--- {col} ---")
        print(df[col].value_counts(dropna=False))
