import pandas as pd
vt = pd.read_excel('visual_tags/VT_2.4_five_zones.xlsx')
print("full terraqueous globe counts:")
print(vt['full terraqueous globe'].value_counts())
print("\nterraqueous globe counts:")
print(vt['terraqueous globe'].value_counts())
