#!/usr/bin/env python3
"""
Extract ALL cities from USTC table view (1470-1650)
This script goes through all pages of the USTC search results
and counts editions per city.

IMPORTANT: Your computer must stay ON while this runs.
Expected runtime: 2-6 hours

Usage:
    python3 extract_all_cities.py
"""

import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_driver():
    """Setup Chrome WebDriver in headless mode"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def extract_all_cities():
    """Extract cities from all pages of USTC search results"""

    driver = setup_driver()
    cities = {}
    page_num = 1
    total_rows_processed = 0

    try:
        # Navigate to USTC explore with year filter (1470-1650) in table view
        url = "https://www.ustc.ac.uk/explore?fqyf=1470&fqyt=1650"
        print(f"Loading USTC explore page...")
        driver.get(url)

        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        # Click on Table view button if not already in table view
        try:
            table_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Table')]")
            table_button.click()
            time.sleep(2)
            print("Switched to table view")
        except:
            print("Already in table view or button not found")

        print("\nStarting extraction from all pages...")
        print("=" * 70)

        while True:
            print(f"\n[Page {page_num}] Extracting cities...", end=" ", flush=True)

            try:
                # Get all table rows
                rows = driver.find_elements(By.XPATH, "//tbody/tr")
                rows_on_page = len(rows)

                if rows_on_page == 0:
                    print("No rows found, stopping.")
                    break

                # Extract place field from each row
                # The place is typically in one of the columns
                for row in rows:
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")

                        # Try to find the place column
                        # Usually it's one of the visible columns in the table
                        if len(cells) > 0:
                            # Look for place data - it might be in different columns
                            place_text = None
                            for cell in cells:
                                cell_text = cell.text.strip()
                                # Try to identify which cell contains the place
                                if cell_text and not cell_text.isdigit():
                                    # This is likely the place column
                                    place_text = cell_text
                                    break

                            if place_text and len(place_text) > 0:
                                cities[place_text] = cities.get(place_text, 0) + 1
                                total_rows_processed += 1

                    except Exception as e:
                        pass  # Skip problematic rows

                print(f"Found {rows_on_page} rows, Total cities so far: {len(cities)}")

                # Try to navigate to next page
                try:
                    next_button = driver.find_element(By.XPATH, "//a[contains(@aria-label, 'next') or contains(text(), 'Next')]")
                    next_button.click()
                    time.sleep(1)
                    page_num += 1

                except:
                    # No more pages available
                    print("\nReached end of results")
                    break

                # Print progress every 100 pages
                if page_num % 100 == 0:
                    print(f"\n  [Progress] Processed {page_num} pages, {len(cities)} cities, {total_rows_processed} rows")

            except Exception as e:
                print(f"Error on page {page_num}: {e}")
                break

        print("\n" + "=" * 70)
        print(f"\n✓ Extraction Complete!")
        print(f"  - Pages processed: {page_num}")
        print(f"  - Unique cities: {len(cities)}")
        print(f"  - Total rows processed: {total_rows_processed}")

        # Save to CSV
        output_file = 'ustc_all_cities_complete.csv'
        print(f"\nSaving to {output_file}...")

        sorted_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['city', 'count'])
            for city, count in sorted_cities:
                writer.writerow([city, count])

        print(f"✓ Saved {len(cities)} cities to {output_file}\n")

        # Print top 20 cities
        print("Top 20 Cities by Editions:")
        print("-" * 50)
        for idx, (city, count) in enumerate(sorted_cities[:20], 1):
            print(f"{idx:2}. {city:35} {count:>10,}")

        total = sum(count for _, count in sorted_cities)
        print("-" * 50)
        print(f"TOTAL: {total:,} editions across {len(cities)} cities")

    finally:
        driver.quit()

if __name__ == '__main__':
    print("USTC City Extraction Script")
    print("=" * 70)
    print("This will extract ALL cities from USTC (1470-1650)")
    print("Duration: 2-6 hours")
    print("Computer must stay ON\n")

    try:
        extract_all_cities()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)
