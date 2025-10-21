#!/usr/bin/env python3
"""
Excel to JSON Converter for Crop Knowledge Explorer
==================================================

This script reads crop data from Excel files and converts it to JSON format
for the Crop Knowledge Explorer web application.

Features:
- Eliminates duplicates completely
- Precise category classification
- Clean data processing
- Detailed reporting

Author: Organixnatura
"""

import pandas as pd
import json
import re
import os
from typing import Dict, List, Tuple, Set

def normalize_crop_name(name: str) -> str:
    """
    Normalize crop name for consistent matching:
    - Convert to lowercase
    - Remove extra spaces
    - Remove punctuation except parentheses
    - Handle common variations
    """
    if not name or pd.isna(name):
        return ""
    
    # Convert to string and strip whitespace
    name = str(name).strip()
    
    # Skip invalid entries
    if (name.lower() in ['nan', 'none', '', 'unnamed', 's.no', 'value-added products', 'crops', 'tamil name'] or
        name.isdigit() or len(name) < 3):
        return ""
    
    # Handle common variations
    name = name.replace("ladies finger", "bhendi")
    name = name.replace("lady's finger", "bhendi")
    name = name.replace("lady finger", "bhendi")
    
    # Remove extra spaces and normalize
    name = re.sub(r'\s+', ' ', name)
    
    return name.lower()

def get_classification_keywords() -> Dict[str, List[str]]:
    """
    Get precise keyword lists for crop classification
    """
    return {
        "Fruits": [
            "banana", "papaya", "mango", "guava", "pomegranate"
        ],
        "Vegetables": [
            "brinjal", "bitter gourd", "bottle gourd", "cabbage", "carrot", "beetroot",
            "beans", "bhendi", "okra", "pumpkin", "cauliflower", "broccoli", "moringa"
        ],
        "Greens": [
            "spinach", "palak", "lettuce", "amaranthus"
        ],
        "Tubers": [
            "cassava", "sweet potato", "potato"
        ],
        "Herbal": [
            "ashwagandha", "tulsi", "vetiver", "aloe vera", "curry leaves", "fenugreek", "coriander"
        ],
        "Units": [
            "dairy unit", "goat unit", "poultry unit", "vermi compost unit", "azolla unit"
        ]
    }

def classify_crop(crop_name: str, keywords: Dict[str, List[str]]) -> str:
    """
    Classify a crop based on its name using precise keyword matching
    """
    if not crop_name:
        return "Units"  # Default category
    
    crop_normalized = normalize_crop_name(crop_name)
    
    # Check each category with precise matching
    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            if keyword.lower() in crop_normalized:
                return category
    
    # If no match found, default to Units
    return "Units"

def load_excel_data(file_path: str) -> pd.DataFrame:
    """Load Excel file with robust error handling"""
    try:
        print(f"Loading Excel file: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        # Try different engines for better compatibility
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception:
            df = pd.read_excel(file_path, engine='xlrd')
        
        print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df
        
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        raise

def find_crop_columns(df: pd.DataFrame) -> Tuple[str, str]:
    """
    Intelligently find the English and Tamil crop name columns
    """
    print("Analyzing column structure...")
    
    # Look for common column names
    english_col = None
    tamil_col = None
    
    # Check for exact matches first
    for col in df.columns:
        col_lower = str(col).lower().strip()
        if 'crop' in col_lower and 'english' in col_lower:
            english_col = col
        elif 'crop' in col_lower and 'tamil' in col_lower:
            tamil_col = col
        elif col_lower == 'crops':
            english_col = col
        elif 'tamil' in col_lower and 'name' in col_lower:
            tamil_col = col
    
    # If not found, analyze column content
    if not english_col or not tamil_col:
        print("Analyzing column content to find crop data...")
        
        for i, col in enumerate(df.columns):
            if df[col].dtype == 'object':
                # Sample values from this column
                sample_values = df[col].dropna().astype(str).head(20).tolist()
                valid_crops = [v for v in sample_values if v.strip() and len(v) > 2]
                
                if len(valid_crops) > 5:
                    # Check if this looks like English crop names
                    english_indicators = ['banana', 'papaya', 'mango', 'brinjal', 'carrot', 'cabbage', 'potato', 'spinach', 'bhendi', 'okra']
                    has_english = any(any(indicator in str(val).lower() for indicator in english_indicators) for val in valid_crops)
                    
                    if has_english and not english_col:
                        english_col = col
                        print(f"Found English column: {col}")
                    elif not has_english and not tamil_col:
                        tamil_col = col
                        print(f"Found Tamil column: {col}")
    
    # Fallback: use first two object columns
    if not english_col:
        object_cols = [col for col in df.columns if df[col].dtype == 'object']
        if object_cols:
            english_col = object_cols[0]
            print(f"Using first object column as English: {english_col}")
    
    if not tamil_col:
        object_cols = [col for col in df.columns if df[col].dtype == 'object' and col != english_col]
        if object_cols:
            tamil_col = object_cols[0]
            print(f"Using second object column as Tamil: {tamil_col}")
    
    return english_col, tamil_col

def process_crop_data(df: pd.DataFrame, english_col: str, tamil_col: str) -> List[Dict]:
    """
    Process and clean crop data from the DataFrame
    """
    print("Processing crop data...")
    
    crops = []
    seen_crops = set()  # Track duplicates
    skipped_items = []
    
    for _, row in df.iterrows():
        try:
            # Get English and Tamil names
            english_name = str(row.get(english_col, '')).strip() if pd.notna(row.get(english_col)) else ''
            tamil_name = str(row.get(tamil_col, '')).strip() if pd.notna(row.get(tamil_col)) else ''
            
            # Skip invalid entries
            if (not english_name or 
                english_name.lower() in ['nan', 'none', '', 'unnamed', 's.no', 'value-added products', 'crops', 'tamil name', 'fruits', 'vegetables', 'greens', 'tubers', 'herbal', 'units'] or
                english_name.isdigit() or 
                len(english_name) < 3):
                skipped_items.append(english_name)
                continue
            
            # Clean Tamil name
            if tamil_name.lower() in ['nan', 'none', '']:
                tamil_name = ''
            
            # Check for duplicates (case-insensitive)
            crop_key = english_name.lower().strip()
            if crop_key in seen_crops:
                print(f"Duplicate found and skipped: {english_name}")
                continue
            
            seen_crops.add(crop_key)
            
            crops.append({
                'English': english_name,
                'Tamil': tamil_name
            })
            
        except Exception as e:
            print(f"Warning: Error processing row: {e}")
            continue
    
    print(f"Processed {len(crops)} unique crops")
    if skipped_items:
        print(f"Skipped {len(skipped_items)} invalid entries")
    
    return crops

def create_crops_json(crops: List[Dict], keywords: Dict[str, List[str]]) -> Dict:
    """
    Create the final JSON structure with proper classification
    """
    print("Classifying crops into categories...")
    
    # Initialize categories
    classified_crops = {category: [] for category in keywords.keys()}
    
    # Classify each crop
    for crop in crops:
        category = classify_crop(crop['English'], keywords)
        classified_crops[category].append(crop)
    
    return classified_crops

def generate_final_report(classified_crops: Dict) -> None:
    """
    Generate the final summary report
    """
    print("\n" + "="*60)
    print("FINAL CLASSIFICATION SUMMARY")
    print("="*60)
    
    total_crops = 0
    category_counts = {}
    
    for category, crops in classified_crops.items():
        count = len(crops)
        total_crops += count
        category_counts[category] = count
        print(f"{category}: {count} items")
    
    print(f"\nTotal crops classified: {total_crops}")
    print("="*60)
    
    # Print the required summary format
    print(f"\ncrops_data.json created successfully!")
    print(f"Fruits: {category_counts.get('Fruits', 0)} | "
          f"Vegetables: {category_counts.get('Vegetables', 0)} | "
          f"Greens: {category_counts.get('Greens', 0)} | "
          f"Tubers: {category_counts.get('Tubers', 0)} | "
          f"Herbal: {category_counts.get('Herbal', 0)} | "
          f"Units: {category_counts.get('Units', 0)}")

def main():
    """
    Main function to convert Excel to JSON
    """
    try:
        # Configuration
        excel_file = "Vanthavasi records for 24 months.xlsx"
        json_file = "crops_data.json"
        
        print("Crop Knowledge Explorer - Excel to JSON Converter")
        print("="*60)
        
        # Load Excel data
        df = load_excel_data(excel_file)
        
        # Find crop columns
        english_col, tamil_col = find_crop_columns(df)
        
        if not english_col:
            raise ValueError("Could not find English crop column")
        
        print(f"Using columns: English='{english_col}', Tamil='{tamil_col}'")
        
        # Get classification keywords
        keywords = get_classification_keywords()
        
        # Process crop data
        crops = process_crop_data(df, english_col, tamil_col)
        
        if not crops:
            raise ValueError("No valid crops found in the Excel file")
        
        # Classify crops
        classified_crops = create_crops_json(crops, keywords)
        
        # Save to JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(classified_crops, f, ensure_ascii=False, indent=2)
        
        # Generate final report
        generate_final_report(classified_crops)
        
        print(f"\nOutput file: {json_file}")
        print(f"Ready for deployment!")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\nConversion completed successfully!")
    else:
        print("\nConversion failed!")
        exit(1)