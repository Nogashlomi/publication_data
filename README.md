# Thesis Publication Data

This repository contains the data and code used to generate the quantitative visualizations and analyses for the dissertation *"The Evolution of Visual Language in Early Modern Astronomy"*.

## Structure

* **`dissertation/`**
  This folder contains the core datasets (CSV and Excel files), SPARQL queries, and the Jupyter Notebooks (`.ipynb`) used for the source analysis (SA) and contextual chapters. The notebooks are kept in their original state to ensure that the sequential data processing steps (loading DataFrames, filtering, etc.) continue to run without breaking path dependencies.

* **`FIGURE_MAPPING.md`**
  A complete mapping table that links the specific figures (and their captions) appearing in the final thesis PDF to the exact Jupyter Notebook(s) that generated them. Use this table if you want to find the code responsible for a specific graph in the thesis!

## Environment Setup
This project uses `uv` for dependency management. To recreate the exact environment used for the thesis, run:
```bash
uv sync
```
This will create a `.venv` virtual environment with all required dependencies installed. You can then select this environment as your Jupyter kernel to run the notebooks.

*(Note: If you copied this folder from another location, make sure to delete any old `.venv` or `myenv` folders first, as they contain hardcoded paths to the old location, and then run `uv sync` to generate a fresh one).*
