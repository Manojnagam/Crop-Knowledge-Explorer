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
    """Load crop data from JSON file"""
    global crop_data

    try:
        # ✅ Always use absolute path on Render
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(base_dir, "crops_data.json")

        if not os.path.exists(json_file):
            print(f"⚠️ Warning: {json_file} not found! Using sample data.")
            return {
                "Fruits": [
                    {"English": "Papaya", "Tamil": "பப்பாளி"},
                    {"English": "Banana", "Tamil": "வாழை"},
                    {"English": "Guava", "Tamil": "கொய்யா"},
                    {"English": "Pomegranate", "Tamil": "மாதுளை"}
                ],
                "Vegetables": [
                    {"English": "Brinjal", "Tamil": "கத்தரிக்காய்"},
                    {"English": "Carrot", "Tamil": "கேரட்"},
                    {"English": "Cabbage", "Tamil": "முட்டைக்கோஸ்"}
                ]
            }

        with open(json_file, "r", encoding="utf-8") as f:
            crop_data = json.load(f)

        print(f"✅ Loaded crop data successfully with {sum(len(v) for v in crop_data.values())} items.")
        return crop_data

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
    return jsonify(crop_data)

@app.route('/categories')
def get_categories():
    """API endpoint to get available categories"""
    return jsonify({
        "categories": list(crop_data.keys()),
        "counts": {cat: len(items) for cat, items in crop_data.items()}
    })

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "message": "Crop Knowledge Explorer is running"})

if __name__ == '__main__':
    print("Loading Crop Knowledge Explorer...")
    
    # Load data on startup
    crop_data = load_crop_data()
    
    if crop_data:
        print("Data loaded successfully!")
        print("Starting Flask server...")
        print("Open your browser to: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Failed to load data. Please check your data file.")