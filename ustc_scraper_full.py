#!/usr/bin/env python3
"""
USTC Scraper - Extract all places from all decades 1470-1650
"""

import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def extract_places(driver):
    """Extract place data from current page"""
    places = {}

    try:
        # Get all labels and their associated counts
        labels = driver.find_elements(By.XPATH, "//label[..//*[@type='checkbox']]")

        for label in labels:
            label_text = label.text.strip()

            # Skip non-place labels
            if not label_text or label_text in ['From', 'To', 'Find place', 'Filter', 'place']:
                continue

            # Find the sibling generic element with the count
            try:
                # Get the parent div and find the count element
                parent = label.find_element(By.XPATH, 'ancestor::div[1]')
                count_elem = parent.find_element(By.XPATH, ".//span | .//div[contains(@style, 'background')]")
                count_text = count_elem.text.strip()

                if count_text.isdigit():
                    count = int(count_text)
                    if count > 0:
                        places[label_text] = count
            except:
                # Try alternative method
                try:
                    sibling = label.find_element(By.XPATH, 'following-sibling::*[1]')
                    count_text = sibling.text.strip()
                    if count_text.isdigit():
                        places[label_text] = int(count_text)
                except:
                    pass

    except Exception as e:
        print(f"  ❌ Error extracting places: {e}")

    return places

def scrape_all_decades():
    """Main scraping function"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=chrome_options)
    all_data = []

    try:
        # Generate list of all decades
        decades = [(year, year + 9) for year in range(1470, 1650, 10)]

        print("=" * 70)
        print(f"USTC Place Data Extraction (1470-1650)")
        print(f"Total decades: {len(decades)}")
        print("=" * 70 + "\n")

        for idx, (decade_start, decade_end) in enumerate(decades, 1):
            url = f"https://ustc.ac.uk/explore?q=&fqyf={decade_start}&fqyt={decade_end}"

            print(f"[{idx}/{len(decades)}] {decade_start}-{decade_end}", end=" ... ")

            driver.get(url)
            time.sleep(3)  # Wait for page to load

            # Extract places
            places = extract_places(driver)

            if places:
                print(f"✓ Found {len(places)} places")

                for place, count in sorted(places.items(), key=lambda x: x[1], reverse=True):
                    all_data.append({
                        'place': place,
                        'decade': f'{decade_start}-{decade_end}',
                        'edition_count': count
                    })
            else:
                print("⚠ No places found")

            time.sleep(1)  # Delay between requests

        # Save to CSV
        output_file = '/Users/nogashlomi/projects/Image_data/ustc_data/ustc_places_1470_1650.csv'

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['place', 'decade', 'edition_count'])
            writer.writeheader()
            writer.writerows(all_data)

        print("\n" + "=" * 70)
        print(f"✅ Complete! Saved to: {output_file}")
        print(f"Total records: {len(all_data)}")
        print(f"Unique places: {len(set(d['place'] for d in all_data))}")
        print("=" * 70)

        # Print summary statistics
        place_counts = {}
        for d in all_data:
            place_counts[d['place']] = place_counts.get(d['place'], 0) + d['edition_count']

        print("\n📊 Top 20 places by total editions:")
        for place, count in sorted(place_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {place:20} {count:6} editions")

        return all_data

    finally:
        driver.quit()

if __name__ == '__main__':
    scrape_all_decades()
