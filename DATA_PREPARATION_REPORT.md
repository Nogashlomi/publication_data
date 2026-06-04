# Data Preparation and Organization Report

This document outlines the organization and preparation of the image and textual data extracted from the Sphere corpus. The data structure presented here was designed to precisely mirror the methodological pipeline used in the research: from basic corpus metadata through algorithmic and manual image clustering, to semantic content keyword assignment, and finally to targeted visual feature tagging. 

By following this four-step pipeline, the data moves from broad bibliographic extraction toward highly specific historical interpretation, providing a transparent and reproducible foundation for analysis.

## Directory Structure

The data is organized into four main subdirectories that reflect the stages of data preparation and analysis:

```text
DATA/
├── 01_corpus_metadata/
│   ├── full_book_data_feb_25.csv
│   └── part_ids_with_types.csv
│
├── 02_image_clusters/
│   ├── full_image_data_feb_25.csv
│   └── full_image_data_feb_25_corrected_centrality_earth.csv
│
├── 03_content_keywords/
│   ├── all_elements_all_ck_ucks.xlsx
│   └── ucks.csv
│
└── 04_visual_tags/
    ├── visual_overview.xlsx
    ├── visual_tag_book_counts_april_26.xlsx
    ├── visual_tag_categories.csv
    ├── visual_tag_overview_detailed.xlsx
    ├── visual_tag_overview_full_metadata.xlsx
    └── visual_tags/  (Directory containing individual VT_...xlsx files)
│
└── 05_external_datasets/
    ├── books_data.json
    ├── europe.geojson
    ├── printing_centers_1470_1650.csv
    ├── top_5_places_by_decade.csv
    ├── universities_data.json
    └── (Various other scraped datasets and maps)
```

## Folder Contents & Data Description

### 1. `01_corpus_metadata/` (Book-Level Data)
This folder contains the foundational bibliographic data defining the Sphere corpus. It serves as the material and historical scaffolding to which all subsequent images are linked.
*   **`full_book_data_feb_25.csv`**: Contains complete metadata for the ~359 distinct editions included in the corpus (e.g., printing city, year, printers, and categorizations like large/medium/small printing centers).
*   **`part_ids_with_types.csv`**: Links the books to their specific textual subdivisions (e.g., chapters, poems, commentary parts), mapping the structure of the texts themselves.

### 2. `02_image_clusters/` (Image Extraction & Grouping)
This folder represents the first major data transformation: extracting ~20,000 individual content illustrations from the corpus and reducing them to ~3,500 "same-image clusters" (elements) using a combination of machine learning similarity detection and manual expert cleaning.
*   **`full_image_data_feb_25.csv`**: The master dataset of all extracted image regions, tracing each individual image back to its parent cluster (element) and its original source book and page.
*   **`full_image_data_feb_25_corrected_centrality_earth.csv`**: An updated version of the master image dataset containing specific corrections related to the "Centrality of the Earth" visualizations.

### 3. `03_content_keywords/` (Semantic Labeling)
This folder details the mapping of the 3,500 image clusters into ~168 thematic and historically grounded "Content Keywords." This was achieved using a bottom-up location tagging approach, moving from basic geometric/astronomical subjects to broader fields of knowledge.
*   **`all_elements_all_ck_ucks.xlsx`**: A comprehensive mapping file connecting the specific image clusters (elements) to their assigned Content Keywords (CK) and Usage Category Keywords (UCKS).
*   **`ucks.csv`**: A structured dataset specifically focused on Usage Categories, which group illustrations by their practical or disciplinary domains.

### 4. `04_visual_tags/` (Targeted Visual Characteristics)
The final stage of the methodology focused not just on *what* was depicted, but *how* it was depicted. This folder contains data tracking specific visual features (e.g., curved lines, shading, decorative elements) assigned within the context of specific content groups.
*   **`visual_tag_categories.csv` & `visual_overview.xlsx`**: High-level overviews defining the categories used for visual tagging.
*   **`visual_tag_overview_detailed.xlsx` & `visual_tag_overview_full_metadata.xlsx`**: Detailed aggregations linking visual tags back to the full corpus metadata, enabling spatio-temporal tracking of visual conventions.
*   **`visual_tag_book_counts_april_26.xlsx`**: Temporal and spatial distributions of visual characteristics calculated at the book/edition level.
*   **`visual_tags/` (Subdirectory)**: Contains granular, topic-specific Excel files (e.g., `VT_1.1_sphere_definition.xlsx`, `VT_1.8_earth_central.xlsx`). These were used to generate the targeted visualizations for specific thesis chapters, evaluating how different scientific concepts were visually communicated over time.

### 5. `05_external_datasets/` (Supplementary Contextual Data)
This folder contains external datasets scraped or collected to provide broader historical and geographical context for the core Sphere corpus. These datasets were primarily used for comparison, mapping, and establishing the wider landscape of the early modern print market and educational network.
*   **USTC Printing Centers (1470-1650)**: A series of CSV and Excel files (e.g., `printing_centers_1470_1650.csv`, `top_5_places_by_decade.csv`) generated by automatically scraping the Universal Short Title Catalogue (USTC). This dataset contains edition counts for all European printing cities across the 1470-1650 timeframe, allowing for a comparative baseline against the specific production of the Sphere corpus.
*   **University Locations**: JSON and GeoJSON files (e.g., `universities_data.json`, `europe.geojson`) detailing the geographic locations of early modern universities. This data was cross-referenced with printing center data to map the relationship between book production and academic hubs.
*   **Maps**: Static map visualizations (`.png` and `.jpg`) and interactive map data (`.html`) illustrating the spatial distribution discussed in the dissertation.
