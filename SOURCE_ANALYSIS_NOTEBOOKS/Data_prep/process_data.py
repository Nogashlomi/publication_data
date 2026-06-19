import pandas as pd
import json
import os

# Paths
BOOK_DATA_PATH = '../../DATA/01_corpus_metadata/full_book_data_feb_25.csv'
IMAGE_DATA_PATH = '../../DATA/02_image_clusters/full_image_data_feb_25.csv'
UCK_DATA_PATH = '../../DATA/03_content_keywords/all_elements_all_ck_ucks.xlsx'
OUTPUT_DIR = '/Users/nogashlomi/projects/Image_data/university_comparison'
OUTPUT_JSON = os.path.join(OUTPUT_DIR, '../../DATA/05_external_datasets/books_data.json')

def process_data():
    print("Loading data...")
    # Load data
    df_books = pd.read_csv(BOOK_DATA_PATH)
    df_images = pd.read_csv(IMAGE_DATA_PATH)
    df_ucks = pd.read_excel(UCK_DATA_PATH)

    print("Processing coordinates...")
    # Get coordinates for each book (bid)
    # Some images might not have coordinates, so we drop those and take the first available for each bid
    coords = df_images.dropna(subset=['latitude', 'longitude']).drop_duplicates(subset=['bid'])[['bid', 'latitude', 'longitude']]
    
    print("Processing UCK values...")
    # Link UCKs to books via images. 
    # all_elements_all_ck_ucks.xlsx has 'images' and 'uck'
    # full_image_data_feb_25.csv has 'images' and 'bid'
    
    # Merge UCKs with image data to get 'bid' for each 'uck'
    df_img_bid = df_images[['images', 'bid']].drop_duplicates()
    df_uck_bid = pd.merge(df_ucks, df_img_bid, on='images', how='inner')
    
    # Group UCKs by bid
    book_ucks = df_uck_bid.groupby('bid')['uck'].apply(lambda x: sorted(list(set(x)))).reset_index()

    print("Merging datasets...")
    # Merge everything into df_books
    df_final = pd.merge(df_books, coords, on='bid', how='left')
    df_final = pd.merge(df_final, book_ucks, on='bid', how='left')

    # Drop entries without coordinates as they can't be shown on map
    df_final = df_final.dropna(subset=['latitude', 'longitude'])
    
    # Fill empty ucks with empty list
    df_final['uck'] = df_final['uck'].apply(lambda x: x if isinstance(x, list) else [])

    # Prepare for JSON
    # Necessary fields: label (title), place, year, latitude, longitude, uck (list)
    books_list = []
    for _, row in df_final.iterrows():
        books_list.append({
            'id': str(row['bid']),
            'title': str(row['label']),
            'place': str(row['place']),
            'year': int(row['year']) if not pd.isna(row['year']) else 0,
            'lat': float(row['latitude']),
            'lon': float(row['longitude']),
            'ucks': row['uck'],
            'authors': str(row['authors']) if not pd.isna(row['authors']) else ""
        })

    print("Processing university data...")
    df_univ = pd.read_excel('/Users/nogashlomi/Desktop/universities.xlsx')
    # Cleanup column names
    df_univ.columns = [c.strip() for c in df_univ.columns]
    
    univ_list = []
    for _, row in df_univ.iterrows():
        # Handle foundation and closing years (e.g. "c.1167", "No (1970)")
        def clean_year(y):
            if pd.isna(y): return None
            import re
            s = str(y)
            nums = re.findall(r'\d+', s)
            return int(nums[0]) if nums else None

        foundation = clean_year(row['Foundation'])
        closing = clean_year(row['Closed / Continuity']) if 'Closed' in row.index[6] else None
        # In the sample 'Closed / Continuity' with 'Yes' means still open
        is_still_open = str(row['Closed / Continuity']).lower() == 'yes'
        closing_year = clean_year(row['Closed / Continuity']) if not is_still_open else 9999

        univ_list.append({
            'label': str(row['University']),
            'city': str(row['City, Country']),
            'lat': float(row['Lat']),
            'lon': float(row['Lon']),
            'foundation': foundation if foundation else 0,
            'closing': closing_year if closing_year else 9999,
            'type_name': str(row['Type / Notes']) if not pd.isna(row['Type / Notes']) else ""
        })

    print(f"Saving {len(books_list)} books to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(books_list, f, indent=2)
    
    OUTPUT_UNIV = os.path.join(OUTPUT_DIR, '../../DATA/05_external_datasets/universities_data.json')
    print(f"Saving {len(univ_list)} universities to {OUTPUT_UNIV}...")
    with open(OUTPUT_UNIV, 'w') as f:
        json.dump(univ_list, f, indent=2)

    print("Done!")

if __name__ == "__main__":
    process_data()
