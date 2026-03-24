import pandas as pd

# Load book data to get locations
book_df = pd.read_csv('/Users/nogashlomi/projects/Image_data/dissertation/full_book_data_feb_25.csv', low_memory=False)

# Get unique cities and their lat/long if available in book_df
# Let's check what columns we have
print("Columns in book_df:")
print(book_df.columns.tolist())

# Check for lat/lon columns
geo_cols = [c for c in book_df.columns if 'lat' in c.lower() or 'lon' in c.lower() or 'lng' in c.lower()]
print(f"Potential geo columns: {geo_cols}")

# Extract unique places
places = book_df['place'].dropna().unique()
print(f"Total unique places: {len(places)}")
print("Sample places:", places[:10])

# If coordinates are not in book_df, we might need a lookup table or common coordinates
if geo_cols:
    sample_geo = book_df[['place'] + geo_cols].drop_duplicates().head(10)
    print("Sample geo data:")
    print(sample_geo)
else:
    print("No obvious lat/lon columns found in book_df.")
