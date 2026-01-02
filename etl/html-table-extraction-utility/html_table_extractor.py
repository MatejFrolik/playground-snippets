import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

# --- SETTINGS (edit these) ---
URL = "https://example.com/page-with-tables"   # Target page with tables
OUTPUT_DIR = Path("tables_output")            # Output folder
TABLE_SELECTOR = "table"                      # CSS selector (e.g. "table.data" / "table#results")
CAPTION_CONTAINS = None                       # e.g. "Firmy" or None to ignore captions


# --- 1) Create output folder (if it doesn't exist) ---
OUTPUT_DIR.mkdir(exist_ok=True)

# --- 2) Download HTML from the target page ---
# We set a User-Agent and a timeout to avoid hanging forever.
resp = requests.get(URL, headers={"User-Agent": "TableMiner/1.0"}, timeout=30)
resp.raise_for_status()
html = resp.text

# --- 3) Parse HTML and select only the tables we want ---
# BeautifulSoup lets us search the HTML structure.
soup = BeautifulSoup(html, "html.parser")

tables = soup.select(TABLE_SELECTOR)

# Optional: filter by caption text if CAPTION_CONTAINS is set
# (Keeps only tables whose <caption> includes the given substring.)
if CAPTION_CONTAINS:
    filtered = []
    for tbl in tables:
        cap = tbl.find("caption")
        if cap and CAPTION_CONTAINS in cap.get_text(strip=True):
            filtered.append(tbl)
    tables = filtered

if not tables:
    raise SystemExit("No <table> elements found with the given selector/filter.")

# --- 4) Convert each HTML <table> to a pandas DataFrame ---
# pandas.read_html can parse an HTML table string into a DataFrame.
dfs = []
for i, tbl in enumerate(tables, start=1):
    parsed_list = pd.read_html(str(tbl), flavor="lxml")  # usually returns a list with 1 DF
    if not parsed_list:
        continue

    df = parsed_list[0]

    # --- 5) Clean up column headers (strip whitespace, flatten MultiIndex if needed) ---
    # Some tables have multi-row headers -> MultiIndex; we flatten it into single strings.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([str(x) for x in tup if str(x) != "nan"]).strip()
                      for tup in df.columns.values]
    else:
        df.columns = [str(c).strip() for c in df.columns]

    # --- 6) Save each table as CSV ---
    # If the table has a caption, we use it for the filename; otherwise we use table index.
    caption = ""
    cap = tbl.find("caption")
    if cap:
        caption = cap.get_text(" ", strip=True)

    safe_name = "".join(ch for ch in (caption or f"table_{i}")
                        if ch.isalnum() or ch in (" ", "_", "-")).strip()
    safe_name = safe_name.replace(" ", "_")[:60] or f"table_{i}"

    csv_path = OUTPUT_DIR / f"{safe_name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Store caption for Excel sheet naming later
    df.attrs["__caption__"] = caption or f"table_{i}"
    dfs.append(df)

# --- 7) Save all tables into one Excel file (one sheet per table) ---
xlsx_path = OUTPUT_DIR / "all_tables.xlsx"
with pd.ExcelWriter(xlsx_path, engine="xlsxwriter") as xw:
    for idx, df in enumerate(dfs, start=1):
        # Excel sheet names must be <= 31 characters
        sheet_name = (df.attrs.get("__caption__", f"table_{idx}") or f"table_{idx}")[:31]
        df.to_excel(xw, sheet_name=sheet_name, index=False)

print(f"Done. Saved {len(dfs)} tables into: {OUTPUT_DIR.resolve()}")
print(f"Excel file: {xlsx_path.resolve()}")
