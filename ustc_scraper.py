#!/usr/bin/env python3
"""
USTC Place Data Scraper
מחלץ את כל המקומות עם ספירת מהדורות לכל עשור
"""

import csv
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def extract_places_from_page(driver, decade_start, decade_end):
    """
    מחלץ את כל המקומות מהעמוד הנוכחי
    """
    places = {}

    try:
        # חכה שהעמוד ייטען
        time.sleep(2)

        # קבל את כל ה-text של העמוד
        body_text = driver.find_element(By.TAG_NAME, 'body').text

        # חלץ מה-DOM - חפש את כל ה-labels והמספרים
        labels = driver.find_elements(By.TAG_NAME, 'label')

        print(f"\n[{decade_start}-{decade_end}] נמצאו {len(labels)} labels")

        for label in labels:
            label_text = label.text.strip()

            # דלג על labels שלא רלוונטיות
            if not label_text or len(label_text) < 2 or label_text in ['From', 'To', 'Find place', 'place']:
                continue

            # חפש את המספר בparent container
            try:
                parent = label.find_element(By.XPATH, './ancestor::div[contains(@class, "")]')
                parent_text = parent.text

                # חלץ מספרים מהטקסט של ה-parent
                import re
                numbers = re.findall(r'\b(\d+)\b', parent_text)

                if numbers:
                    # קח את המספר הגדול ביותר (זה בדרך כלל ספירת המהדורות)
                    count = max([int(n) for n in numbers])

                    if count > 0 and label_text not in places:
                        places[label_text] = count
                        print(f"  ✓ {label_text}: {count}")
            except:
                pass

        # אם לא קיבלנו הרבה, נסה דרך ישירה יותר
        if len(places) < 3:
            print(f"  ⚠️ חילוץ חלול, מנסה דרך חלופית...")

            # חפש patterns בטקסט הגולמי
            import re

            # נתונים ידועים - תוקם ידני אם צריך
            known_places = {
                'Venezia': 706,
                'Roma': 667,
                'Köln': 483,
                'Augsburg': 359,
                'Milano': 312,
                'Strasbourg': 268,
                'Lübeck': 0,
                'Basel': 0,
                'Paris': 0,
                'London': 0,
                'Leipzig': 0,
                'Deventer': 0,
                'Napoli': 0,
                'Gouda': 0,
            }

            for place in known_places:
                if place in body_text:
                    print(f"  • {place} נמצא בטקסט")

        return places

    except Exception as e:
        print(f"  ❌ שגיאה: {e}")
        return {}

def scrape_all_decades():
    """
    מחלץ נתונים לכל עשור מ-1470 עד 1650
    """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=chrome_options)

    all_data = []
    decades = []

    # יצור רשימה של כל העשורים
    for year in range(1470, 1650, 10):
        decades.append((year, year + 9))

    print(f"🔍 חילוץ נתונים ל-{len(decades)} עשורים (1470-1650)\n")
    print("=" * 60)

    try:
        for decade_start, decade_end in decades:
            url = f"https://ustc.ac.uk/explore?q=&fqyf={decade_start}&fqyt={decade_end}"

            print(f"\n📍 טוען עמוד: {decade_start}-{decade_end}")
            print(f"   URL: {url}")

            driver.get(url)
            time.sleep(3)

            # חלץ את המקומות
            places = extract_places_from_page(driver, decade_start, decade_end)

            # שמור לנתונים הסופיים
            for place, count in places.items():
                all_data.append({
                    'place': place,
                    'decade': f'{decade_start}-{decade_end}',
                    'edition_count': count
                })

            if places:
                print(f"   ✅ סה'כ {len(places)} מקומות בעשור זה")

            time.sleep(1)  # דלק בין בקשות

        # שמור לקובץ CSV
        output_file = '/Users/nogashlomi/projects/Image_data/ustc_data/ustc_places_all_decades.csv'

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['place', 'decade', 'edition_count'])
            writer.writeheader()
            writer.writerows(all_data)

        print(f"\n{'='*60}")
        print(f"✅ סיום! שמורים בקובץ: {output_file}")
        print(f"   סה'כ שורות: {len(all_data)}")
        print(f"   מקומות ייחודיים: {len(set(d['place'] for d in all_data))}")

        return all_data

    finally:
        driver.quit()

if __name__ == '__main__':
    data = scrape_all_decades()
