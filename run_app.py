#!/usr/bin/env python3
"""
Simple startup script for the Multilingual Crop Knowledge App
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def check_excel_file():
    """Check if Excel file exists"""
    excel_file = "Vanthavasi records for 24 months.xlsx"
    if not os.path.exists(excel_file):
        print(f"✗ Error: {excel_file} not found!")
        print("Please make sure the Excel file is in the same directory as this script.")
        return False
    print(f"✓ Found Excel file: {excel_file}")
    return True

def main():
    """Main function"""
    print("🌱 Multilingual Crop Knowledge App")
    print("=" * 40)
    
    # Check Excel file
    if not check_excel_file():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    print("\n🚀 Starting the application...")
    print("The app will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server\n")
    
    # Start the server
    try:
        from excel_reader import run_server
        run_server(8000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except ImportError as e:
        print(f"✗ Error importing excel_reader: {e}")
        print("Make sure all files are in the same directory.")

if __name__ == "__main__":
    main()

