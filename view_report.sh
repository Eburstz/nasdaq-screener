#!/bin/bash
# Quick launcher to view the HTML report in your browser

cd "$(dirname "$0")"

if [ -f "nasdaq_screener_report.html" ]; then
    echo "Opening stock screener report in browser..."
    open nasdaq_screener_report.html
else
    echo "❌ Report not found. Generate it first:"
    echo "   python3 generate_html_report.py NASDAQ_Screener_Results.xlsx"
fi
