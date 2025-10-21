#!/usr/bin/env python3
"""
Excel Reader for Vanthavasi Crop Data
Reads Excel file and serves data as JSON via HTTP server
"""

import pandas as pd
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

class ExcelDataHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.df = None
        self.load_excel_data()
        super().__init__(*args, **kwargs)
    
    def load_excel_data(self):
        """Load and process Excel data"""
        try:
            excel_file = "Vanthavasi records for 24 months.xlsx"
            if not os.path.exists(excel_file):
                print(f"Error: {excel_file} not found!")
                return
            
            # Read Excel file
            self.df = pd.read_excel(excel_file)
            print(f"Loaded Excel file with {len(self.df)} rows and {len(self.df.columns)} columns")
            print("Columns:", list(self.df.columns))
            
            # Clean data - remove NaN values and duplicates
            self.df = self.df.dropna(subset=['CROPS (English)'])
            self.df = self.df.drop_duplicates(subset=['CROPS (English)'])
            
            # Create categories based on data
            self.categories = self.create_categories()
            print(f"Created categories: {list(self.categories.keys())}")
            
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            self.df = None
    
    def create_categories(self):
        """Create categories by analyzing the data"""
        categories = {
            'Fruits': [],
            'Vegetables': [],
            'Greens': [],
            'Tubers': [],
            'Herbal': [],
            'Units': []
        }
        
        # Simple keyword-based categorization
        fruit_keywords = ['fruit', 'apple', 'banana', 'mango', 'orange', 'grape', 'berry', 'citrus']
        vegetable_keywords = ['vegetable', 'tomato', 'onion', 'potato', 'carrot', 'cabbage', 'cauliflower']
        greens_keywords = ['green', 'leaf', 'spinach', 'lettuce', 'coriander', 'mint']
        tuber_keywords = ['tuber', 'root', 'ginger', 'turmeric', 'sweet potato']
        herbal_keywords = ['herb', 'medicinal', 'basil', 'oregano', 'thyme']
        
        for _, row in self.df.iterrows():
            crop_name = str(row['CROPS (English)']).lower()
            tamil_name = str(row.get('TAMIL NAME', '')).lower()
            
            # Check for fruit
            if any(keyword in crop_name or keyword in tamil_name for keyword in fruit_keywords):
                categories['Fruits'].append({
                    'english': row['CROPS (English)'],
                    'tamil': row.get('TAMIL NAME', ''),
                    'botanical': row.get('BOTANICAL NAME', ''),
                    'value_added': row.get('VALUE-ADDED PRODUCTS', '')
                })
            # Check for vegetables
            elif any(keyword in crop_name or keyword in tamil_name for keyword in vegetable_keywords):
                categories['Vegetables'].append({
                    'english': row['CROPS (English)'],
                    'tamil': row.get('TAMIL NAME', ''),
                    'botanical': row.get('BOTANICAL NAME', ''),
                    'value_added': row.get('VALUE-ADDED PRODUCTS', '')
                })
            # Check for greens
            elif any(keyword in crop_name or keyword in tamil_name for keyword in greens_keywords):
                categories['Greens'].append({
                    'english': row['CROPS (English)'],
                    'tamil': row.get('TAMIL NAME', ''),
                    'botanical': row.get('BOTANICAL NAME', ''),
                    'value_added': row.get('VALUE-ADDED PRODUCTS', '')
                })
            # Check for tubers
            elif any(keyword in crop_name or keyword in tamil_name for keyword in tuber_keywords):
                categories['Tubers'].append({
                    'english': row['CROPS (English)'],
                    'tamil': row.get('TAMIL NAME', ''),
                    'botanical': row.get('BOTANICAL NAME', ''),
                    'value_added': row.get('VALUE-ADDED PRODUCTS', '')
                })
            # Check for herbal
            elif any(keyword in crop_name or keyword in tamil_name for keyword in herbal_keywords):
                categories['Herbal'].append({
                    'english': row['CROPS (English)'],
                    'tamil': row.get('TAMIL NAME', ''),
                    'botanical': row.get('BOTANICAL NAME', ''),
                    'value_added': row.get('VALUE-ADDED PRODUCTS', '')
                })
            # Default to Units for uncategorized items
            else:
                categories['Units'].append({
                    'english': row['CROPS (English)'],
                    'tamil': row.get('TAMIL NAME', ''),
                    'botanical': row.get('BOTANICAL NAME', ''),
                    'value_added': row.get('VALUE-ADDED PRODUCTS', '')
                })
        
        return categories
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/categories':
            self.send_categories()
        elif path == '/api/category':
            query_params = parse_qs(parsed_path.query)
            category = query_params.get('name', [''])[0]
            self.send_category_data(category)
        else:
            self.send_file()
    
    def send_categories(self):
        """Send available categories"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'categories': list(self.categories.keys()),
            'counts': {cat: len(items) for cat, items in self.categories.items()}
        }
        self.wfile.write(json.dumps(response).encode())
    
    def send_category_data(self, category):
        """Send data for specific category"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if category in self.categories:
            response = {
                'category': category,
                'items': self.categories[category]
            }
        else:
            response = {'error': 'Category not found'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def send_file(self):
        """Serve static files"""
        if self.path == '/':
            self.path = '/index.html'
        
        try:
            with open(self.path[1:], 'rb') as f:
                content = f.read()
            
            # Set content type
            if self.path.endswith('.html'):
                content_type = 'text/html'
            elif self.path.endswith('.css'):
                content_type = 'text/css'
            elif self.path.endswith('.js'):
                content_type = 'application/javascript'
            else:
                content_type = 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

def run_server(port=8000):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ExcelDataHandler)
    print(f"Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.shutdown()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
