# USTC Place Data Scraper

Automatically extracts place data by decade from the Universal Short Title Catalogue (USTC) website.

## What it does

- Loops through decades (1450-1700 by default)
- For each decade, filters the USTC database by date range
- Extracts all places and their edition counts
- Saves results to CSV file

## Setup

### 1. Install dependencies

```bash
pip install -r requirements_scraper.txt
```

You also need Chrome/Chromium browser installed. If you don't have it:
- **macOS**: `brew install chromium` or use your existing Chrome
- **Linux**: `sudo apt-get install chromium-browser`
- **Windows**: Download from https://www.chromium.org/

### 2. Get ChromeDriver

The script uses Selenium which requires ChromeDriver. You can:

**Option A: Auto-download (easiest)**
```bash
pip install webdriver-manager
```

Then modify line in script:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Replace: driver = webdriver.Chrome(options=chrome_options)
# With:
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
```

**Option B: Manual install**
- Download from: https://chromedriver.chromium.org/
- Add to PATH or specify path in script

## Usage

```bash
python scrape_ustc_places.py
```

### Customization

Edit the decade range in `scrape_all_decades()` call:
```python
data = scrape_all_decades(start_year=1450, end_year=1700, decade_size=10)
```

For example:
- `start_year=1470, end_year=1500` - Only 1470-1500
- `decade_size=5` - Process 5-year intervals instead of 10

## Output

Creates `ustc_places_by_decade.csv` with columns:
- `place` - Place name
- `decade` - Date range (e.g., "1470-1480")
- `edition_count` - Number of editions from that place in that decade

## Example output

```
place,decade,edition_count
Venezia,1470-1480,706
Roma,1470-1480,667
Köln,1470-1480,483
Paris,1480-1490,452
...
```

## Troubleshooting

**Issue: "No such element" error**
- The page structure may have changed. Update the XPath selectors in the script.

**Issue: Slow/timeout**
- Increase the `timeout` parameter in `scrape_places_for_decade()` function
- Check your internet connection

**Issue: No data extracted**
- The page might be using JavaScript that needs more time to render
- Increase the `time.sleep()` values in the script

## Notes

- The script respects the server with 1-second delays between requests
- First run may take 20-30 minutes depending on decade count
- Results are saved incrementally to CSV after each decade
