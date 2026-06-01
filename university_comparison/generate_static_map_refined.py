import json
import os
import math
from PIL import Image, ImageDraw, ImageFont
from collections import Counter

# === CONFIGURATION ===
LABEL_SIZE = 24 
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
LABEL_PADDING = 5 # Pixels of buffer around each label
# =====================

# Paths
GEOJSON_PATH = '/Users/nogashlomi/projects/Image_data/university_comparison/europe.geojson'
BOOKS_JSON_PATH = '/Users/nogashlomi/projects/Image_data/university_comparison/books_data.json'
UNIV_JSON_PATH = '/Users/nogashlomi/projects/Image_data/university_comparison/universities_data.json'
OUTPUT_PNG = '/Users/nogashlomi/projects/Image_data/university_comparison/comparison_map_refined.png'

# Map settings
WIDTH, HEIGHT = 2400, 1800
LON_MIN, LON_MAX = -10, 30
LAT_MIN, LAT_MAX = 35, 60

# Colors
BG_COLOR = (255, 255, 255)
LAND_COLOR = (241, 245, 249)
BORDER_COLOR = (203, 213, 225)
BOOK_COLOR = (251, 191, 36)
UNIV_COLOR = (67, 56, 202)
LABEL_COLOR = (15, 23, 42)

try:
    font = ImageFont.truetype(FONT_PATH, LABEL_SIZE)
    font_large = ImageFont.truetype(FONT_PATH, LABEL_SIZE + 10)
except:
    font = ImageFont.load_default()
    font_large = font

def project(lat, lon):
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * WIDTH
    y = HEIGHT - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) * HEIGHT
    return x, y

def intersects(rect1, rect2, padding=0):
    r1 = (rect1[0]-padding, rect1[1]-padding, rect1[2]+padding, rect1[3]+padding)
    return not (r1[2] < rect2[0] or r1[0] > rect2[2] or r1[3] < rect2[1] or r1[1] > rect2[3])

def generate_static_map():
    print("Loading data...")
    with open(GEOJSON_PATH, 'r') as f:
        europe_geo = json.load(f)
    with open(BOOKS_JSON_PATH, 'r') as f:
        books = json.load(f)
    with open(UNIV_JSON_PATH, 'r') as f:
        univ = json.load(f)

    place_counts = Counter([b['place'] for b in books])
    place_coords = {b['place']: (b['lat'], b['lon']) for b in books}

    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    print("Drawing countries...")
    for feature in europe_geo['features']:
        geom = feature['geometry']
        polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
        for poly in polys:
            ring = poly[0] if isinstance(poly[0][0], list) else poly
            points = [project(c[1], c[0]) for c in ring]
            if len(points) > 2:
                draw.polygon(points, fill=LAND_COLOR, outline=BORDER_COLOR)

    print("Drawing markers & labels...")
    used_rects = []
    
    # 1. Books and Labels
    sorted_places = sorted(place_counts.items(), key=lambda x: x[1], reverse=True)
    for place, count in sorted_places:
        lat, lon = place_coords[place]
        x, y = project(lat, lon)
        r = 10 + (math.sqrt(count) * 8)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=BOOK_COLOR, outline=(0,0,0))
        
        label_text = place
        placed = False
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            for dist in [r + 10, r + 30, r + 60, r + 100]:
                dx = math.cos(rad) * dist
                dy = math.sin(rad) * dist
                test_x, test_y = x + dx, y + dy
                if dx < 0:
                    text_w = draw.textlength(label_text, font=font)
                    test_x -= text_w
                test_bbox = draw.textbbox((test_x, test_y), label_text, font=font)
                if not any(intersects(test_bbox, r_existing, LABEL_PADDING) for r_existing in used_rects):
                    draw.text((test_x, test_y), label_text, fill=LABEL_COLOR, font=font)
                    used_rects.append(test_bbox)
                    placed = True
                    break
            if placed: break

    # 2. Universities (Foreground)
    for u in univ:
        x, y = project(u['lat'], u['lon'])
        r = 15
        draw.ellipse([x-r, y-r, x+r, y+r], fill=UNIV_COLOR + (140,), outline=(255,255,255))

    # 3. Legend (Upper Left)
    lx, ly = 80, 80
    draw.text((lx, ly), "Legend", fill=LABEL_COLOR, font=font_large)
    ly += 50
    
    draw.ellipse([lx, ly, lx+30, ly+30], fill=BOOK_COLOR, outline=(0,0,0))
    draw.text((lx + 45, ly), "Book Printing Places (Size = # of Books)", fill=LABEL_COLOR, font=font)
    ly += 45
    
    draw.ellipse([lx, ly, lx+30, ly+30], fill=UNIV_COLOR, outline=(255,255,255))
    draw.text((lx + 45, ly), "Universities", fill=LABEL_COLOR, font=font)

    print(f"Saving map to {OUTPUT_PNG}...")
    img.save(OUTPUT_PNG)
    print("Done!")

if __name__ == "__main__":
    generate_static_map()
