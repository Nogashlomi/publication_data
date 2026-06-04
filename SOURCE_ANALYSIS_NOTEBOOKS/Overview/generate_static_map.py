import json
from PIL import Image, ImageDraw, ImageFont
import os

# Paths
GEOJSON_PATH = '../DATA/05_external_datasets/europe.geojson'
BOOKS_JSON_PATH = '../DATA/05_external_datasets/books_data.json'
UNIV_JSON_PATH = '../DATA/05_external_datasets/universities_data.json'
OUTPUT_PNG = '/Users/nogashlomi/projects/Image_data/university_comparison/comparison_map.png'

# Map settings
WIDTH, HEIGHT = 2400, 1800
LAT_MIN, LAT_MAX = 34, 65
LON_MIN, LON_MAX = -12, 45

# Colors
BG_COLOR = (15, 23, 42)    # #0f172a
LAND_COLOR = (30, 41, 59)  # #1e293b
BORDER_COLOR = (51, 65, 85)# #334155
BOOK_COLOR = (251, 191, 36)# #fbbf24
UNIV_COLOR = (129, 140, 248)# #818cf8
TEXT_COLOR = (56, 189, 248) # #38bdf8

def project(lat, lon):
    # Linear projection (not Mercator, but sufficient for this scale)
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * WIDTH
    y = HEIGHT - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * HEIGHT
    return x, y

def generate_static_map():
    print("Loading data...")
    with open(GEOJSON_PATH, 'r') as f:
        europe_geo = json.load(f)
    with open(BOOKS_JSON_PATH, 'r') as f:
        books = json.load(f)
    with open(UNIV_JSON_PATH, 'r') as f:
        univ = json.load(f)

    # Create image
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    print("Drawing countries...")
    for feature in europe_geo['features']:
        geom = feature['geometry']
        polys = []
        if geom['type'] == 'Polygon':
            polys = [geom['coordinates']]
        elif geom['type'] == 'MultiPolygon':
            polys = geom['coordinates']
        
        for poly in polys:
            points = []
            # In MultiPolygon, the first list is the outer ring
            ring = poly[0] if isinstance(poly[0][0], list) else poly
            for coord in ring:
                points.append(project(coord[1], coord[0]))
            
            if len(points) > 2:
                draw.polygon(points, fill=LAND_COLOR, outline=BORDER_COLOR)

    print("Drawing markers...")
    # Draw Books
    for b in books:
        x, y = project(b['lat'], b['lon'])
        r = 5
        draw.ellipse([x-r, y-r, x+r, y+r], fill=BOOK_COLOR, outline=(255, 255, 255))

    # Draw Universities
    for u in univ:
        x, y = project(u['lat'], u['lon'])
        r = 10
        draw.ellipse([x-r, y-r, x+r, y+r], fill=UNIV_COLOR, outline=(255, 255, 255))

    # Add Title and Legend (Simple drawing since Font loading can be tricky)
    draw.text((50, 50), "Printing & Universities in Europe", fill=TEXT_COLOR)
    draw.rectangle([50, 100, 70, 120], fill=BOOK_COLOR)
    draw.text((80, 100), "Book Printing Places", fill=(255,255,255))
    draw.rectangle([50, 130, 70, 150], fill=UNIV_COLOR)
    draw.text((80, 130), "Universities", fill=(255,255,255))

    print(f"Saving map to {OUTPUT_PNG}...")
    img.save(OUTPUT_PNG)
    print("Done!")

if __name__ == "__main__":
    generate_static_map()
