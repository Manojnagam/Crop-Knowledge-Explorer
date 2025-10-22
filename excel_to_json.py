#!/usr/bin/env python3
"""
Robust exporter: Excel or SQLite -> categorized JSON (crops_data.json).
- Auto-detects Excel header row (scans first 12 rows).
- Optionally reads from a SQLite database table (pass --sqlite path/to.db --table table_name).
- Cleans whitespace and common "nan" strings.
- Classifies into main categories (Fruits, Vegetables, Greens, Tubers, Herbal, Units).
- Logs counts and writes crops_data.json.
"""

import pandas as pd
import json
import argparse
import os
import sys
import re
from collections import defaultdict, Counter

# --- Config: keywords used to classify crops to categories (tweak as needed) ---
CATEGORY_KEYWORDS = {
    "Fruits": ["banana", "papaya", "pomegranate", "guava", "mango", "fruit", "jackfruit", "sapota", "orange", "lemon", "apple"],
    "Vegetables": ["brinjal", "bitter gourd", "bottle gourd", "pumpkin", "cabbage", "carrot", "tomato", "okra", "bhendi", "beans", "vegetable", "cauliflower", "radish", "drumstick"],
    "Greens": ["spinach", "palak", "amaranthus", "keerai", "greens", "leaf", "moringa", "curry leaves", "lettuce"],
    "Tubers": ["yam", "potato", "sweet potato", "tapioca", "colocasia", "tuber", "beetroot", "cassava"],
    "Herbal": ["aloe", "neem", "turmeric", "ginger", "herbal", "medicinal", "ashwagandha", "tulsi", "curry leaves", "vetiver"],
    "Units": ["unit", "poultry", "goat", "dairy", "vermicompost", "vermi", "farm unit"]
}

# --- Utility functions ---
def normalize_colname(s):
    if s is None:
        return ""
    return re.sub(r'\s+', ' ', str(s).strip()).lower()

def is_blank_val(v):
    if v is None:
        return True
    s = str(v).strip()
    if s == "":
        return True
    if s.lower() in ("nan", "none", "na", "n/a", "-"):
        return True
    return False

def find_header_row_excel(path, max_scan=12):
    """Scan first max_scan rows and return header row index that contains likely column names"""
    for header in range(0, max_scan):
        try:
            df_try = pd.read_excel(path, header=header, nrows=0)
            cols = [str(c).strip().lower() for c in df_try.columns]
            # look for any expected tokens
            tokens = ("crop", "crops", "tamil", "english", "category", "name")
            if any(any(tok in c for tok in tokens) for c in cols):
                return header
        except Exception:
            continue
    return 0  # fallback to first row

def classify_crop_by_name(name):
    if not isinstance(name, str):
        return None
    n = name.lower()
    for cat, keys in CATEGORY_KEYWORDS.items():
        for k in keys:
            if k in n:
                return cat
    return "Others"

def clean_text(v):
    if v is None:
        return ""
    s = str(v).strip()
    # Replace multiple whitespace with single space
    s = re.sub(r'\s+', ' ', s)
    return s

# --- Main processing ---
def process_dataframe(df, expected_cols=None, debug=False):
    """
    df: pandas DataFrame already loaded with proper header
    expected_cols: dict mapping alternate column names to canonical names (optional)
    Returns: data dict grouped by category, diagnostics dict
    """
    # normalize column names
    original_cols = list(df.columns)
    col_map = {}
    for c in original_cols:
        col_map[c] = normalize_colname(c)

    # Guess which columns correspond to English, Tamil, Telugu, Hindi, Kannada, Category
    lc = [normalize_colname(c) for c in original_cols]

    def find_col(possible_names):
        for pname in possible_names:
            if pname in lc:
                return original_cols[lc.index(pname)]
        return None

    english_col = find_col(["english", "english name", "crop", "crops", "crops name", "name"])
    tamil_col   = find_col(["tamil name", "tamil", "tamil_name", "tamil name "])
    telugu_col  = find_col(["telugu", "telugu name", "telugu_name"])
    hindi_col   = find_col(["hindi", "hindi name", "hindi_name"])
    kannada_col = find_col(["kannada", "kannada name", "kannada_name"])
    category_col= find_col(["category","categories","type","crop type","group"])

    # Fallbacks
    if not english_col:
        # try first non-empty column
        english_col = original_cols[0]
    if not tamil_col:
        tamil_col = None
    if not telugu_col:
        telugu_col = None
    if not hindi_col:
        hindi_col = None
    if not kannada_col:
        kannada_col = None

    diagnostics = {
        "total_rows": len(df),
        "skipped_rows": 0,
        "skipped_examples": [],
        "per_category_counts": Counter(),
        "unclassified": 0
    }

    data = defaultdict(list)

    for idx, row in df.iterrows():
        # Extract raw values
        eng_raw = row.get(english_col, "") if english_col in row else row.iloc[0] if len(row)>0 else ""
        eng = clean_text(eng_raw)

        if is_blank_val(eng):
            diagnostics["skipped_rows"] += 1
            if len(diagnostics["skipped_examples"]) < 10:
                diagnostics["skipped_examples"].append({"idx": int(idx), "reason": "blank english", "row": row.to_dict()})
            continue

        cat = None
        # Prefer explicit category column if present and not blank
        if category_col:
            raw_cat = clean_text(row.get(category_col, ""))
            if not is_blank_val(raw_cat):
                # normalize category words to one of our main categories if possible
                rc_l = raw_cat.lower()
                for k in CATEGORY_KEYWORDS.keys():
                    if k.lower() in rc_l or rc_l in k.lower():
                        cat = k
                        break
                if cat is None:
                    # if category word matches any known token (e.g., "Fruits" spelled), map approximately
                    # else use the raw value as-is (but we'll try classify by name next)
                    cat = raw_cat
        # If no category yet, classify by English crop name
        if not cat:
            cat = classify_crop_by_name(eng)
            if cat == "Others":
                diagnostics["unclassified"] += 1

        # Pull translations, if columns exist
        tamil = clean_text(row.get(tamil_col, "")) if tamil_col else ""
        telugu = clean_text(row.get(telugu_col, "")) if telugu_col else ""
        hindi = clean_text(row.get(hindi_col, "")) if hindi_col else ""
        kannada = clean_text(row.get(kannada_col, "")) if kannada_col else ""

        entry = {
            "English": eng,
            "Tamil": tamil,
            "Telugu": telugu,
            "Hindi": hindi,
            "Kannada": kannada
        }
        
        # Add all other columns from the Excel file
        for col_name, col_value in row.items():
            if col_name not in [english_col, tamil_col, telugu_col, hindi_col, kannada_col, category_col]:
                cleaned_value = clean_text(col_value)
                if not is_blank_val(cleaned_value):
                    entry[col_name] = cleaned_value

        data[cat].append(entry)
        diagnostics["per_category_counts"][cat] += 1

    diagnostics["categories_found"] = dict(diagnostics["per_category_counts"])
    return data, diagnostics

def read_excel_auto(path):
    header_row = find_header_row_excel(path, max_scan=12)
    print(f"Detected header row index: {header_row}")
    df = pd.read_excel(path, header=header_row)
    return df

def read_sqlite_db(db_path, table):
    import sqlite3
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

def main():
    parser = argparse.ArgumentParser(description="Export crops from Excel or SQLite to categorized JSON.")
    parser.add_argument("--excel", "-x", help="Path to Excel (.xlsx) file", default="Vanthavasi records for 24 months.xlsx")
    parser.add_argument("--sqlite", "-s", help="Path to SQLite DB (optional)")
    parser.add_argument("--table", "-t", help="Table name if using SQLite")
    parser.add_argument("--out", "-o", help="Output JSON filename", default="crops_data.json")
    args = parser.parse_args()

    if args.sqlite:
        if not args.table:
            print("If using --sqlite you must supply --table table_name")
            sys.exit(1)
        print(f"Reading SQLite {args.sqlite} table {args.table} ...")
        df = read_sqlite_db(args.sqlite, args.table)
    else:
        if not os.path.exists(args.excel):
            print(f"Excel file not found: {args.excel}")
            sys.exit(1)
        print(f"Reading Excel: {args.excel}")
        df = read_excel_auto(args.excel)

    # Quick info
    print("Raw columns detected:")
    print(list(df.columns))
    print(f"Rows read: {len(df)}")

    data, diagnostics = process_dataframe(df)

    print("Diagnostics summary:")
    print(" Total rows read:", diagnostics["total_rows"])
    print(" Rows skipped (blank English):", diagnostics["skipped_rows"])
    print(" Unclassified by name:", diagnostics["unclassified"])
    print(" Per-category counts:")
    for cat, cnt in diagnostics["per_category_counts"].items():
        print(f"  - {cat}: {cnt}")

    if diagnostics["skipped_examples"]:
        print("Some skipped row examples (first few):")
        for ex in diagnostics["skipped_examples"]:
            print(ex)

    # Save JSON (ensure string keys)
    # Convert defaultdict to normal dict and ensure categories are ordered by name (optional)
    out_dict = {}
    for k in sorted(data.keys()):
        out_dict[k] = data[k]

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out_dict, f, ensure_ascii=False, indent=2)

    print(f"✅ wrote {args.out} ({sum(len(v) for v in out_dict.values())} items across {len(out_dict)} categories)")

if __name__ == "__main__":
    main()
