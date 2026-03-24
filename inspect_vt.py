import pandas as pd
vt = pd.read_excel('/Users/nogashlomi/projects/Image_data/visual_tags/VT_2.3.xlsx')
lines_cols = [c for c in vt.columns if 'line' in c.lower() or 'multiple' in c.lower()]
print("VT lines cols:", lines_cols)
if lines_cols:
    print(vt[lines_cols[0]].value_counts(dropna=False))
