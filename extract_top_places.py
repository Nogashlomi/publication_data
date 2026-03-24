#!/usr/bin/env python3
"""
Extract top 5 places for each decade from USTC
"""

import csv
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def extract_top_5_places(driver, decade_start, decade_end):
    """Extract top 5 places from current page"""
    try:
        time.sleep(3)

        # Get page source to extract place data
        page_source = driver.page_source

        # Look for the place facet data in the page
        # Pattern: <label>PlaceName</label> followed by <span>COUNT</span>
        import re

        places = {}

        # Try to find the JSON data embedded in the page
        json_patterns = re.findall(r'"([^"]*?)"\s*:\s*(\d{2,4})(?:[,\}])', page_source)

        # Common place names to search for
        known_places = [
            'Venezia', 'Venice', 'Roma', 'Rome', 'Köln', 'Cologne', 'Augsburg', 'Milano', 'Milan',
            'Strasbourg', 'Basel', 'Paris', 'Lyon', 'London', 'Oxford', 'Cambridge', 'Leipzig',
            'Mainz', 'Worms', 'Speyer', 'Frankfurt', 'Deventer', 'Gouda', 'Bruges', 'Antwerp',
            'Leiden', 'Amsterdam', 'Rouen', 'Toulouse', 'Valencia', 'Alcalá', 'Salamanca',
            'Napoli', 'Naples', 'Palermo', 'Lübeck', 'Ulm', 'Nuremberg', 'Vienna', 'Prague',
            'Venice', 'Padova', 'Padua', 'Verona', 'Pisa', 'Florence', 'Firenze', 'Bologna',
            'Brescia', 'Modena', 'Parma', 'Ravenna', 'Reggio', 'Ferrara', 'Como'
        ]

        # Search for each place in page source
        for place in known_places:
            # Find pattern: "PlaceName" followed by a number
            pattern = f'{place}.*?(\\d{{2,5}})'
            matches = re.finditer(pattern, page_source, re.IGNORECASE | re.DOTALL)

            for match in matches:
                try:
                    count = int(match.group(1))
                    # Filter for reasonable counts (between 5 and 100000)
                    if 5 < count < 100000:
                        # Check if this is the right format (not a year or other number)
                        if count not in places.values():
                            places[place.title()] = count
                            break
                except:
                    pass

        # If still no results, try alternative extraction
        if not places:
            # Extract from HTML structure
            text = driver.find_element(By.TAG_NAME, 'body').text
            lines = text.split('\n')

            for i, line in enumerate(lines):
                for place in known_places:
                    if place.lower() in line.lower() and i+1 < len(lines):
                        # Try to get number from next line or same line
                        next_line = lines[i+1] if i+1 < len(lines) else ""
                        numbers = re.findall(r'\b(\d{2,5})\b', line + " " + next_line)
                        if numbers:
                            count = int(numbers[0])
                            if 5 < count < 100000:
                                places[place.title()] = count

        # Sort by count and return top 5
        sorted_places = sorted(places.items(), key=lambda x: x[1], reverse=True)
        return sorted_places[:5]

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []


def main():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    results = []

    try:
        decades = [(year, year + 9) for year in range(1470, 1650, 10)]

        print("=" * 80)
        print("USTC Top 5 Printing Centers by Decade (1470-1650)")
        print("=" * 80 + "\n")

        for idx, (decade_start, decade_end) in enumerate(decades, 1):
            url = f"https://ustc.ac.uk/explore?q=&fqyf={decade_start}&fqyt={decade_end}"

            print(f"[{idx:2d}/18] {decade_start}-{decade_end} ... ", end="", flush=True)

            driver.get(url)
            top_5 = extract_top_5_places(driver, decade_start, decade_end)

            if top_5:
                print(f"✓ Found {len(top_5)} places")
                for rank, (place, count) in enumerate(top_5, 1):
                    print(f"        {rank}. {place}: {count}")
                    results.append({
                        'decade': f'{decade_start}-{decade_end}',
                        'rank': rank,
                        'place': place,
                        'edition_count': count
                    })
            else:
                print("⚠ No data found")

            time.sleep(1)

        # Save results
        output_file = '/Users/nogashlomi/projects/Image_data/ustc_data/top_5_places_by_decade.csv'

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['decade', 'rank', 'place', 'edition_count'])
            writer.writeheader()
            writer.writerows(results)

        print("\n" + "=" * 80)
        print(f"✅ Results saved to: {output_file}")
        print(f"Total records: {len(results)}")
        print("=" * 80)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
