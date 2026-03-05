#!/usr/bin/env python3
"""
HTML Report Generator for Stock Screener Results
Creates a beautiful, interactive web page from Excel screener data.

Features:
- Visual cards for each stock with color-coded signals
- Sortable/filterable table
- Signal strength indicators
- Quick stats dashboard
- Mobile-friendly design
"""

import pandas as pd
import sys
from datetime import datetime
from pathlib import Path


def generate_html_report(excel_path, output_html="screener_report.html"):
    """Generate beautiful HTML report from Excel screener results."""

    print(f"Loading data from {excel_path}...")

    # Load data from Excel
    try:
        # Try loading enhanced version first
        df_all = pd.read_excel(excel_path, sheet_name='All MA50×150')
        df_ma20 = pd.read_excel(excel_path, sheet_name='All MA20×50')
        df_rsi = pd.read_excel(excel_path, sheet_name='All RSI Div')
        df_combined = pd.read_excel(excel_path, sheet_name='All Combined')
        enhanced = False

        # Check if this is enhanced version with score column
        if 'Score' in df_all.columns:
            enhanced = True
            df_top = pd.read_excel(excel_path, sheet_name='🌟 TOP PICKS')
            print("  Enhanced Excel detected (with scoring)")
        else:
            print("  Original Excel detected (no scoring)")
    except Exception as e:
        print(f"  Error loading Excel: {e}")
        return None

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASDAQ Stock Screener Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #2d3748;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #1a202c;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #718096;
            font-size: 1.1em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            text-align: center;
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}

        .stat-label {{
            color: #718096;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}

        .section-title {{
            font-size: 1.8em;
            color: #1a202c;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .stock-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .stock-card {{
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .stock-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            border-color: #667eea;
        }}

        .stock-card.bullish {{
            border-left: 5px solid #48bb78;
            background: linear-gradient(to right, #f0fff4 0%, white 100%);
        }}

        .stock-card.bearish {{
            border-left: 5px solid #f56565;
            background: linear-gradient(to right, #fff5f5 0%, white 100%);
        }}

        .stock-card.combined {{
            border-left: 5px solid #ed8936;
            background: linear-gradient(to right, #fffaf0 0%, white 100%);
        }}

        .ticker {{
            font-size: 1.5em;
            font-weight: bold;
            color: #1a202c;
            margin-bottom: 10px;
        }}

        .price {{
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 15px;
        }}

        .signal-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 5px 5px 5px 0;
        }}

        .signal-badge.bullish {{
            background: #48bb78;
            color: white;
        }}

        .signal-badge.bearish {{
            background: #f56565;
            color: white;
        }}

        .signal-badge.info {{
            background: #4299e1;
            color: white;
        }}

        .signal-badge.warning {{
            background: #ed8936;
            color: white;
        }}

        .stock-details {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
        }}

        .detail-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9em;
        }}

        .detail-label {{
            color: #718096;
        }}

        .detail-value {{
            font-weight: 600;
            color: #2d3748;
        }}

        .score-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .score-high {{
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }}

        .score-medium {{
            background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
            color: white;
        }}

        .score-low {{
            background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
            color: white;
        }}

        .risk-badge {{
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
            display: inline-block;
        }}

        .risk-low {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .risk-medium {{
            background: #feebc8;
            color: #7c2d12;
        }}

        .risk-high {{
            background: #fed7d7;
            color: #742a2a;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th {{
            background: #f7fafc;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #2d3748;
            border-bottom: 2px solid #cbd5e0;
            position: sticky;
            top: 0;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}

        tr:hover {{
            background: #f7fafc;
        }}

        .filter-bar {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .filter-group {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-group label {{
            font-weight: 600;
            color: #4a5568;
        }}

        .filter-group select,
        .filter-group input {{
            padding: 8px 12px;
            border: 2px solid #cbd5e0;
            border-radius: 6px;
            font-size: 0.95em;
        }}

        .filter-group button {{
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }}

        .filter-group button:hover {{
            background: #5a67d8;
        }}

        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #a0aec0;
        }}

        .empty-state-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}

        @media (max-width: 768px) {{
            .stock-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 1.8em;
            }}

            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .alert {{
            background: #fef5e7;
            border-left: 4px solid #f39c12;
            padding: 15px 20px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}

        .alert-icon {{
            display: inline-block;
            margin-right: 10px;
            font-size: 1.2em;
        }}

        footer {{
            text-align: center;
            color: white;
            padding: 30px;
            margin-top: 40px;
        }}

        footer a {{
            color: white;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 NASDAQ Stock Screener Report</h1>
            <p class="subtitle">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </header>
"""

    # Add stats dashboard
    total_stocks = len(df_all) + len(df_ma20) + len(df_rsi)
    ma50_count = len(df_all)
    ma20_count = len(df_ma20)
    rsi_count = len(df_rsi)
    combined_count = len(df_combined)

    html += f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_stocks}</div>
                <div class="stat-label">Total Signals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{ma50_count}</div>
                <div class="stat-label">MA50×150</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{ma20_count}</div>
                <div class="stat-label">MA20×50</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{rsi_count}</div>
                <div class="stat-label">RSI Divergence</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{combined_count}</div>
                <div class="stat-label">Combined</div>
            </div>
        </div>
"""

    # Combined signals section (strongest)
    if combined_count > 0:
        html += """
        <div class="section">
            <h2 class="section-title">🔥 Combined Signals (Strongest Setups)</h2>
            <p style="margin-bottom: 20px; color: #718096;">These stocks have MA crossover + RSI divergence within 10 days. Highest confidence signals.</p>
            <div class="stock-grid">
"""

        for _, row in df_combined.iterrows():
            ticker = row['Ticker']
            price = row.get('Price', 'N/A')
            ma_signal = row.get('MA Signal', 'N/A')
            rsi_signal = row.get('RSI Signal', 'N/A')
            combined = row.get('Combined', 'N/A')
            rsi_val = row.get('RSI', 'N/A')

            signal_class = 'bullish' if 'Bullish' in str(ma_signal) else 'bearish'

            score_html = ""
            risk_html = ""
            if enhanced:
                score = row.get('Score', 0)
                risk = row.get('Risk', 'Unknown')

                score_class = 'score-high' if score >= 7.5 else ('score-medium' if score >= 6.0 else 'score-low')
                risk_class = 'risk-low' if 'Low' in risk else ('risk-medium' if 'Medium' in risk else 'risk-high')

                score_html = f'<span class="score-badge {score_class}">Score: {score}</span>'
                risk_html = f'<span class="risk-badge {risk_class}">{risk}</span>'

            html += f"""
                <div class="stock-card combined">
                    <div class="ticker">{ticker} {risk_html}</div>
                    {score_html}
                    <div class="price">${price}</div>
                    <div>
                        <span class="signal-badge {'bullish' if 'Bullish' in str(ma_signal) else 'bearish'}">{ma_signal}</span>
                        <span class="signal-badge info">{rsi_signal}</span>
                    </div>
                    <div class="stock-details">
                        <div class="detail-row">
                            <span class="detail-label">RSI:</span>
                            <span class="detail-value">{rsi_val}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Setup:</span>
                            <span class="detail-value" style="font-size: 0.85em;">{combined}</span>
                        </div>
                    </div>
                </div>
"""

        html += """
            </div>
        </div>
"""

    # Top picks section (if enhanced)
    if enhanced and 'df_top' in locals() and len(df_top) > 0:
        html += """
        <div class="section">
            <h2 class="section-title">⭐ Top Picks (Highest Scoring)</h2>
            <p style="margin-bottom: 20px; color: #718096;">Sorted by signal strength score. Start here for best opportunities.</p>
            <div class="stock-grid">
"""

        for _, row in df_top.head(20).iterrows():  # Top 20
            ticker = row['Ticker']
            score = row.get('Score', 0)
            risk = row.get('Risk', 'Unknown')
            price = row.get('Price', 'N/A')
            signal = row.get('Signal', 'N/A')
            rsi_val = row.get('RSI', 'N/A')
            vol = row.get('Vol', 'N/A')
            momentum_5d = row.get('5D%', 'N/A')

            signal_class = 'bullish' if 'Bullish' in str(signal) else 'bearish'
            score_class = 'score-high' if score >= 7.5 else ('score-medium' if score >= 6.0 else 'score-low')
            risk_class = 'risk-low' if 'Low' in risk else ('risk-medium' if 'Medium' in risk else 'risk-high')

            html += f"""
                <div class="stock-card {signal_class}">
                    <div class="ticker">{ticker} <span class="risk-badge {risk_class}">{risk}</span></div>
                    <span class="score-badge {score_class}">Score: {score}</span>
                    <div class="price">${price}</div>
                    <div>
                        <span class="signal-badge {signal_class}">{signal}</span>
                    </div>
                    <div class="stock-details">
                        <div class="detail-row">
                            <span class="detail-label">RSI:</span>
                            <span class="detail-value">{rsi_val}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Volume:</span>
                            <span class="detail-value">{vol}x</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">5-Day:</span>
                            <span class="detail-value" style="color: {'#48bb78' if momentum_5d > 0 else '#f56565'};">{momentum_5d}%</span>
                        </div>
                    </div>
                </div>
"""

        html += """
            </div>
        </div>
"""

    # MA50×150 signals
    if ma50_count > 0:
        bullish_50_150 = df_all[df_all['Signal'].str.contains('Bullish', na=False)]
        bearish_50_150 = df_all[df_all['Signal'].str.contains('Bearish', na=False)]

        html += f"""
        <div class="section">
            <h2 class="section-title">📈 MA50×150 Crossovers ({ma50_count} signals)</h2>
            <p style="margin-bottom: 20px; color: #718096;">
                <span style="color: #48bb78; font-weight: 600;">● {len(bullish_50_150)} Bullish</span> &nbsp;&nbsp;
                <span style="color: #f56565; font-weight: 600;">● {len(bearish_50_150)} Bearish</span>
            </p>
            <div class="stock-grid">
"""

        for _, row in df_all.head(15).iterrows():  # Top 15
            ticker = row['Ticker']
            price = row.get('Price', 'N/A')
            signal = row['Signal']
            date = row.get('Date', 'N/A')
            rsi_val = row.get('RSI', 'N/A')

            signal_class = 'bullish' if 'Bullish' in signal else 'bearish'

            score_html = ""
            risk_html = ""
            if enhanced and 'Score' in row:
                score = row.get('Score', 0)
                risk = row.get('Risk', 'Unknown')

                score_class = 'score-high' if score >= 7.5 else ('score-medium' if score >= 6.0 else 'score-low')
                risk_class = 'risk-low' if 'Low' in risk else ('risk-medium' if 'Medium' in risk else 'risk-high')

                score_html = f'<span class="score-badge {score_class}">Score: {score}</span>'
                risk_html = f'<span class="risk-badge {risk_class}">{risk}</span>'

            html += f"""
                <div class="stock-card {signal_class}">
                    <div class="ticker">{ticker} {risk_html}</div>
                    {score_html}
                    <div class="price">${price}</div>
                    <div>
                        <span class="signal-badge {signal_class}">{signal}</span>
                    </div>
                    <div class="stock-details">
                        <div class="detail-row">
                            <span class="detail-label">Date:</span>
                            <span class="detail-value">{date}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">RSI:</span>
                            <span class="detail-value">{rsi_val}</span>
                        </div>
                    </div>
                </div>
"""

        html += """
            </div>
        </div>
"""

    # Footer with instructions
    html += f"""
        <div class="section">
            <h2 class="section-title">💡 How to Use This Report</h2>
            <div style="color: #4a5568; line-height: 1.8;">
                <p><strong>1. Start with Combined Signals</strong> - These have multiple confirmations and are highest confidence</p>
                <p><strong>2. {'Check Top Picks by Score' if enhanced else 'Review MA50×150 crossovers'}</strong> - {'Sorted by signal strength (highest first)' if enhanced else 'Longer-term trend changes'}</p>
                <p><strong>3. Verify on Charts</strong> - Open TradingView or your platform to confirm visually</p>
                <p><strong>4. Check Volume</strong> - Higher volume = more reliable signal</p>
                <p><strong>5. Set Stop Losses</strong> - Never trade without risk management</p>
                <br>
                <div class="alert">
                    <span class="alert-icon">⚠️</span>
                    <strong>Important:</strong> This report shows technical signals only. Always do your own research, check fundamentals, and never invest more than you can afford to lose.
                </div>
            </div>
        </div>

        <footer>
            <p>Generated from: {Path(excel_path).name}</p>
            <p>Data is static as of report generation time. Re-run screener for fresh data.</p>
            <p style="margin-top: 10px;">📖 Read QUICK_REFERENCE.md for detailed guidance</p>
        </footer>
    </div>
</body>
</html>
"""

    # Write to file
    output_path = Path(excel_path).parent / output_html
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ HTML report generated: {output_path}")
    print(f"   Open in browser to view")

    return output_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        # Try to find Excel files in current directory
        current_dir = Path.cwd()
        excel_files = list(current_dir.glob("*.xlsx"))

        if not excel_files:
            print("Error: No Excel files found in current directory")
            print("Usage: python3 generate_html_report.py <path_to_excel_file>")
            sys.exit(1)

        # Prefer enhanced, fallback to original
        enhanced = [f for f in excel_files if 'enhanced' in f.name.lower()]
        original = [f for f in excel_files if 'screener' in f.name.lower() and 'enhanced' not in f.name.lower()]

        if enhanced:
            excel_file = enhanced[0]
        elif original:
            excel_file = original[0]
        else:
            excel_file = excel_files[0]

        print(f"Found Excel file: {excel_file}")

    generate_html_report(excel_file)
