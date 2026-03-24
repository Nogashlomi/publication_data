import pandas as pd
vt = pd.read_excel('visual_tags/VT_2.4_five_zones.xlsx')
print("Counts for motion of the sun two dimensional rep curved line:")
print(vt['motion of the sun two dimensional rep curved line'].value_counts())
print("\nCounts for motion of the sun two dimensional rep straight line:")
print(vt['motion of the sun two dimensional rep straight line'].value_counts())
print("\nCounts for earth and cosmos:")
print(vt['earth and cosmos'].value_counts())
