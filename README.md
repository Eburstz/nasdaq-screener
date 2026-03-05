# NASDAQ Stock Screener

Automated daily scanner that detects **MA crossovers** and **RSI divergences** across all NASDAQ-listed stocks. Results are published as an interactive HTML dashboard with direct TradingView chart links.

## Signals Detected

| Signal | Description |
|--------|-------------|
| MA50 x MA150 | 50-day MA crossing 150-day MA (bullish/bearish) |
| MA20 x MA50 | 20-day MA crossing 50-day MA (bullish/bearish) |
| RSI Divergence | Price/RSI divergence with RSI above 70 or below 30 |
| Combined | MA crossover + RSI divergence within 10 days |

## Sector Filters

- **All NASDAQ** (~3,300 stocks)
- **Renewable Energy** (ENPH, FSLR, PLUG, etc.)
- **Nuclear Energy** (CEG, CCJ, SMR, OKLO, etc.)
- **AI Companies** (NVDA, AMD, PLTR, etc.)

## Setup

### 1. Create a GitHub repo

```bash
cd "Moving Averages"
git init
git add .
git commit -m "Initial commit — NASDAQ screener"
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-screener.git
git branch -M main
git push -u origin main
```

### 2. Enable GitHub Pages

1. Go to your repo on GitHub > **Settings** > **Pages**
2. Under "Source", select **Deploy from a branch**
3. Branch: `main`, Folder: `/docs`
4. Click Save

### 3. Run the first scan

1. Go to **Actions** tab in your repo
2. Click **NASDAQ Screener** in the left sidebar
3. Click **Run workflow** > **Run workflow**
4. Wait ~15-20 minutes for the scan to complete

Your dashboard will be live at: `https://YOUR_USERNAME.github.io/nasdaq-screener/`

## Schedule

The scan runs automatically **Monday-Friday at 4:30 PM ET** (30 min after market close). You can also trigger it manually anytime from the Actions tab.

## Running Locally

```bash
pip install -r requirements.txt
python nasdaq_screener.py
open NASDAQ_Screener_Dashboard.html
```

## Customizing

Edit the ticker lists at the top of `nasdaq_screener.py` to add/remove stocks from sector filters. Key config values:

- `CROSSOVER_WINDOW` - how many days back to detect crossovers (default: 5)
- `RSI_OVERBOUGHT` / `RSI_OVERSOLD` - RSI thresholds (default: 70/30)
- `DIVERGENCE_LOOKBACK` - bars to scan for divergence (default: 30)
- `COMBO_WINDOW` - max days between MA cross and RSI divergence to count as combined (default: 10)
