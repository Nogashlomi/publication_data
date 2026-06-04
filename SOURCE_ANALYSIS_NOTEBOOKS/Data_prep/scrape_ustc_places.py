"""
USTC Place Data Scraper
Extracts place data by decade from USTC website
"""
import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def scrape_places_for_decade(driver, start_year, end_year, timeout=20):
    """
    Scrape place data for a given decade
    Returns list of (place_name, edition_count) tuples
    """
    url = f"https://ustc.ac.uk/explore?q=&fqyf={start_year}&fqyt={end_year}"
    print(f"  Fetching: {start_year}-{end_year}...")

    driver.get(url)
    time.sleep(2)  # Wait for page to load

    try:
        wait = WebDriverWait(driver, timeout)

        # Find and click the "place" filter button to expand it
        place_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'place')]")
        if place_buttons:
            place_buttons[0].click()
            time.sleep(1)  # Wait for expansion

        # Wait for place items to appear (they have numeric counts)
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//label[contains(text(), 'London') or contains(text(), 'Venezia') or contains(text(), 'Paris')]")
        ))

        # Extract place data by finding labels followed by numbers
        places = []

        # Look for the place filter section containing checkboxes and counts
        place_items = driver.find_elements(By.XPATH, "//label[not(@*)]/ancestor::div[1]")

        for item in place_items[:50]:  # Limit to first 50 places
            try:
                text = item.text.strip()
                if not text or len(text) < 2:
                    continue

                # Split place name and count
                # Format is typically: "PlaceName  12345"
                match = re.search(r'(.+?)\s+(\d+)$', text.strip())
                if match:
                    place_name = match.group(1).strip()
                    count = int(match.group(2))

                    # Skip if count is too small (likely not a valid count)
                    if count > 0 and place_name and len(place_name) > 1:
                        places.append((place_name, count))
            except Exception as e:
                continue

        if not places:
            print(f"    Warning: No places found. Page may not have loaded correctly.")

        return places

    except Exception as e:
        print(f"    Error: {str(e)[:100]}")
        return []


def scrape_all_decades(start_year=1450, end_year=1700, decade_size=10):
    """
    Scrape USTC data for all decades in the range
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    all_data = {}

    try:
        # Generate all decades
        decades = []
        for year in range(start_year, end_year, decade_size):
            decades.append((year, min(year + decade_size - 1, end_year)))

        print(f"Starting scrape for {len(decades)} decades...\n")

        for idx, (y_start, y_end) in enumerate(decades, 1):
            places = scrape_places_for_decade(driver, y_start, y_end)
            all_data[f"{y_start}-{y_end}"] = places
            print(f"    Found {len(places)} places")
            time.sleep(1)

        return all_data

    finally:
        driver.quit()


def save_to_csv(data, filename="ustc_places_by_decade.csv"):
    """
    Save aggregated data to CSV
    Format: place, decade, count
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['place', 'decade', 'edition_count'])

        for decade, places in data.items():
            for place_name, count in places:
                writer.writerow([place_name, decade, count])

    print(f"\nData saved to: {filename}")


if __name__ == "__main__":
    print("USTC Place Data Scraper")
    print("=" * 60)
    print("Extracting place data by decade from USTC...\n")

    # Scrape data
    data = scrape_all_decades(start_year=1450, end_year=1700, decade_size=10)

    # Save to CSV
    save_to_csv(data)

    # Print summary
    print("\nSummary:")
    all_places = set()
    for decade_data in data.values():
        for place_name, _ in decade_data:
            all_places.add(place_name)

    total_decades = len(data)
    total_places = len(all_places)
    print(f"  Decades processed: {total_decades}")
    print(f"  Unique places found: {total_places}")
    print(f"\nDecade counts:")
    for decade, places in data.items():
        print(f"  {decade}: {len(places)} places")
