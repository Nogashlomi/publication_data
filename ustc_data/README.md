# USTC Data Extraction - European Editions (1470-1650)

## Files in This Folder

### 1. **ustc_europe_1470_1650.csv** ✓ COMPLETE
Editions by time period (20-year intervals)
- **Status**: Ready to use
- **Contents**: 9 time periods, 843,983 total editions
- **Columns**: period, from_year, to_year, count

**Data:**
```
1470-1489:     14,363 editions
1490-1509:     30,122 editions
1510-1529:     43,920 editions
1530-1549:     54,363 editions
1550-1569:     78,343 editions
1570-1589:     96,510 editions
1590-1609:    132,124 editions
1610-1629:    185,177 editions
1630-1649:    209,061 editions
─────────────────────────
TOTAL:        843,983 editions
```

### 2. **ustc_top_5_cities.csv** ✓ COMPLETE
Top 5 printing centers (from USTC place filter)
- **Status**: Ready to use
- **Contents**: Top 5 cities by edition count
- **Columns**: city, count

**Data:**
```
Paris:      81,115 editions
London:     58,862 editions
Venezia:    45,461 editions
Lyon:       29,395 editions
Antwerpen:  25,789 editions
```

### 3. **extract_all_cities.py** (Script)
Extract ALL cities with complete counts
- **Status**: Ready to run
- **Purpose**: Get every city that printed books 1470-1650
- **Output**: ustc_all_cities_complete.csv
- **Runtime**: 2-6 hours
- **Computer**: Must stay ON while running

---

## How to Run the Extraction

### Prerequisites
```bash
pip3 install selenium beautifulsoup4 webdriver-manager
```

### Run the Script
```bash
python3 extract_all_cities.py
```

### What It Does
1. Opens USTC explore page with filters (1470-1650)
2. Switches to table view
3. Goes through ALL pages (42,000+)
4. Extracts the city from each record
5. Counts total editions per city
6. Saves results to CSV

### Expected Output
File: `ustc_all_cities_complete.csv`
```
city,count
Paris,81115
London,58862
Venezia,45461
...
[All cities sorted by count]
```

---

## What You'll Have When Done

✓ **ustc_europe_1470_1650.csv** - Timeline breakdown
✓ **ustc_top_5_cities.csv** - Major centers
✓ **ustc_all_cities_complete.csv** - COMPLETE city list (after running script)

This gives you:
- 843,983 total European editions
- Broken down by time (9 periods)
- Broken down by city (100+ cities)
- Ready for analysis or RDF database import

---

## Important Notes

⚠️ **Computer must stay ON** while script runs
⏱️ **Takes 2-6 hours** to complete
📊 **Will find 500-1000+ cities** with their edition counts
💾 **Progress prints every 100 pages** so you can monitor

---

## Questions?
- Check the script output for current progress
- Script saves to CSV in this folder
- All data is from USTC (Universal Short Title Catalogue)
