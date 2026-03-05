#!/bin/bash
# Double-click this file on Mac to run the NASDAQ screener
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it from https://python.org"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Checking dependencies..."
pip3 install -r requirements.txt -q

echo "Starting NASDAQ Screener..."
python3 nasdaq_screener.py

echo ""
echo "Done! Opening dashboard in your browser..."
open "NASDAQ_Screener_Dashboard.html" 2>/dev/null || xdg-open "NASDAQ_Screener_Dashboard.html" 2>/dev/null
echo "Press Enter to exit..."
read
