# Thesis Publication Data

This repository contains the data and source code used to generate the quantitative visualizations and analyses for the dissertation *"The Evolution of Visual Language in Early Modern Astronomy"*.

## Structure

* **`DATA/`**
  This folder contains all the core datasets (CSV and Excel files) representing the corpus metadata, image clusters, visual tags, and content keywords used throughout the research.

* **`SOURCE_ANALYSIS_NOTEBOOKS/`**
  This folder contains the suite of Jupyter Notebooks (`.ipynb`) used for the source analysis and contextual chapters. 
  * Note: The notebooks are published as an exploratory archive and are kept exactly in their original sequential state. This ensures that data processing steps (like loading DataFrames and filtering variables) remain perfectly intact for reproducibility.
  * Every single notebook in this folder directly generates at least one visualization included in the final thesis.

* **`COMPREHENSIVE_FIGURE_MAPPING.md`**
  A mapping table that links the specific Figures from the thesis by their numbers to the  Jupyter Notebook(s) that generated them. Use this table as a directory to find the underlying code responsible for any specific graph in the thesis.

## Environment Setup
This project uses `uv` for modern, fast dependency management in Python. To recreate the exact environment used for the thesis, run:
```bash
uv sync
```
This will automatically create a `.venv` virtual environment and install all required dependencies (such as pandas, matplotlib, networkx, etc.). You can then select this environment as your kernel in Jupyter to run the notebooks.
