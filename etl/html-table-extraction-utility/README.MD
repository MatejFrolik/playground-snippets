# HTML Table Extraction Utility (Python)

## Overview
This project is a lightweight Python utility for extracting HTML tables from web pages and exporting them into structured CSV and Excel files.

It serves as a **generic ETL-style ingestion example**, demonstrating how semi-structured HTML data can be normalized and prepared for further analytical processing.

---

## Purpose
The purpose of this project is to demonstrate:
- automated extraction of tabular data from HTML pages
- conversion of HTML tables into structured datasets
- schema normalization across heterogeneous tables
- export of cleaned data into analysis-ready formats

The project focuses on **robustness, clarity, and reusability**, not on scraping a specific website.

---

## Data Disclaimer
This project works exclusively with **publicly available HTML content**.

All data:
- originate from external URLs provided by the user
- are processed as-is without proprietary or business-specific context
- are used solely for demonstration and learning purposes

No internal, confidential, or restricted data are included in this repository.

---

## Workflow
1. Download HTML content from a target URL.
2. Parse the page using BeautifulSoup.
3. Identify and extract `<table>` elements.
4. Convert HTML tables into pandas DataFrames.
5. Normalize column headers and table schemas.
6. Export results into:
   - individual CSV files
   - a consolidated Excel file (one table per sheet)

---

## Key Features
- Support for multiple tables per page
- Automatic handling of multi-level table headers
- Optional column standardization and schema alignment
- CSV and Excel export
- Simple, extensible architecture

---

## Tech Stack
- Python
- requests
- pandas
- BeautifulSoup
- lxml
- xlsxwriter

---

## How to Run
- VS Code

### Requirements
Install required dependencies:
```bash
pip install requests pandas beautifulsoup4 lxml xlsxwriter
```
### Configuration
URL = "https://example.com"

### Execution
python main.py

### Output
tables_output/
├── table_1_1.csv

├── table_1_2.csv

├── ...

└── all_tables.xlsx


