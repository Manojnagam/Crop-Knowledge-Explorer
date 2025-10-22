#!/usr/bin/env python3
"""
Crop Knowledge Explorer - Flask Web Application
===============================================

A multilingual Flask web application that displays crop data in multiple languages.

Local Development:
    pip install -r requirements.txt
    python app.py

Render Deployment:
    Build Command: pip install -r requirements.txt
    Start Command: gunicorn app:app

Author: Organixnatura
"""

import json
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variable to store crop data
crop_data = {}

def load_crop_data():
    """Load crop data from JSON file with debug info"""
    global crop_data

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(base_dir, "crops_data.json")

        print(f"🔍 Looking for JSON at: {json_file}")
        print(f"📁 File exists: {os.path.exists(json_file)}")

        if not os.path.exists(json_file):
            print(f"⚠️ Warning: {json_file} not found! Using sample data.")
            return {}

        with open(json_file, "r", encoding="utf-8") as f:
            print("📖 Reading JSON file...")
            data = json.load(f)
            print("✅ JSON file loaded successfully.")

        total_items = sum(len(v) for v in data.values())
        print(f"📊 Loaded {total_items} total crop entries across {len(data)} categories.")

        crop_data = data
        return data

    except Exception as e:
        print(f"❌ Error loading crop data: {e}")
        return {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/data')
def get_data():
    """API endpoint to get crop data"""
    if not crop_data:
        print("🔄 Reloading crop data...")
        load_crop_data()
    return jsonify(crop_data)

@app.route('/categories')
def get_categories():
    """API endpoint to get available categories"""
    if not crop_data:
        load_crop_data()
    return jsonify({
        "categories": list(crop_data.keys()),
        "counts": {cat: len(items) for cat, items in crop_data.items()}
    })

@app.route('/crop/<crop_name>')
def get_crop_details(crop_name):
    """API endpoint to get detailed information for a specific crop"""
    if not crop_data:
        load_crop_data()
    
    # Search for the crop across all categories
    for category, crops in crop_data.items():
        for crop in crops:
            # Check if the crop name matches (case-insensitive)
            if (crop.get('English', '').lower() == crop_name.lower() or 
                crop.get('Tamil', '').lower() == crop_name.lower()):
                
                # Create detailed crop information
                crop_details = {
                    "name": crop.get('English', ''),
                    "tamil_name": crop.get('Tamil', ''),
                    "category": category,
                    "languages": {
                        "English": crop.get('English', ''),
                        "Tamil": crop.get('Tamil', ''),
                        "Telugu": crop.get('Telugu', ''),
                        "Hindi": crop.get('Hindi', ''),
                        "Kannada": crop.get('Kannada', '')
                    },
                    "additional_info": {
                        "Scientific Name": "Not available",
                        "Family": "Not available", 
                        "Origin": "Not available",
                        "Growing Season": "Not available",
                        "Nutritional Value": "Not available",
                        "Uses": "Not available",
                        "Cultivation Tips": "Not available"
                    }
                }
                
                # Add any additional fields from the original crop data
                for key, value in crop.items():
                    if key not in ['English', 'Tamil', 'Telugu', 'Hindi', 'Kannada'] and value:
                        crop_details["additional_info"][key] = value
                
                return jsonify(crop_details)
    
    # If crop not found
    return jsonify({"error": "Crop not found"}), 404

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "message": "Crop Knowledge Explorer is running"})

if __name__ == '__main__':
    print("🚀 Loading Crop Knowledge Explorer...")
    crop_data = load_crop_data()

    if crop_data:
        print("✅ Data loaded successfully! Starting Flask server...")
        print("🌍 Open http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ Failed to load data. Please check your crops_data.json file.")