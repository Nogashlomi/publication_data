import pandas as pd
img_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_image_data_feb_25.csv', nrows=2)
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', nrows=2)
print("IMG COLUMNS:", img_df.columns.tolist())
print("BOOK COLUMNS:", book_df.columns.tolist())
