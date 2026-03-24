import pandas as pd
vt = pd.read_excel('visual_tags/VT_2.4_five_zones.xlsx')
print("Columns in VT_2.4_five_zones.xlsx:")
print(vt.columns.tolist())
print("\nFirst row sample:")
print(vt.iloc[0].to_dict())
