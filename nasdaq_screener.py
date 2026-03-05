#!/usr/bin/env python3
"""
NASDAQ 100 Stock Screener — Interactive Dashboard Edition
Detects MA crossovers and RSI divergences across the NASDAQ 100 index stocks.
Outputs an interactive HTML dashboard with TradingView chart links.

Signals:
1. MA50 crossing MA150 (bullish/bearish)
2. MA20 crossing MA50 (bullish/bearish)
3. RSI divergence (bullish below 30, bearish above 70)
4. Combined: MA50/MA150 crossover + RSI divergence

Sector filters: Renewable Energy, Nuclear Energy, AI, Aschenbrenner AI Infrastructure

Usage:
  python3 nasdaq_screener.py
  python3 nasdaq_screener.py /path/to/output.html
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# ─── CONFIG ───────────────────────────────────────────────────────────────────
LOOKBACK_DAYS = 400        # Enough history for MA150
CROSSOVER_WINDOW = 5       # Days to look back for recent crossovers
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
DIVERGENCE_LOOKBACK = 30   # Bars to look back for divergence peaks/troughs
COMBO_WINDOW = 10          # Days window to match crossover + divergence
BATCH_SIZE = 50            # Tickers per yfinance batch download
DELAY_BETWEEN_BATCHES = 1  # Seconds between batches

# ─── TIMEFRAMES ──────────────────────────────────────────────────────────────
# Each timeframe: (label, yfinance_interval, yfinance_period_or_days, min_bars_needed)
TIMEFRAMES = [
    ("4H",      "1h",  729,  50),    # 4H built from 1h data (729 days max for yfinance 1h)
    ("Daily",   "1d",  400,  200),
    ("Weekly",  "1wk", 2000, 100),
    ("Monthly", "1mo", 3600, 36),
]

# ─── SECTOR TICKER LISTS ─────────────────────────────────────────────────────
# You can add or remove tickers here to customize sector filters
RENEWABLE_ENERGY_TICKERS = [
    "ENPH", "SEDG", "FSLR", "RUN", "CSIQ", "JKS", "ARRY", "MAXN",
    "NOVA", "SHLS", "STEM", "BE", "PLUG", "BLDP", "CLNE", "ORA",
    "CWEN", "AY", "HASI", "NEP", "BEPC", "DQ", "GPRE", "REX",
    "AMSC", "AMPS", "FLNC", "ENVX", "QS", "CHPT", "EVGO", "BLNK",
    "SPWR", "AZRE", "TPIC",
]

NUCLEAR_ENERGY_TICKERS = [
    "CEG", "CCJ", "LEU", "SMR", "OKLO", "NNE", "UEC", "UUUU",
    "DNN", "URG", "NXE", "EU", "BWXT", "GEV",
]

AI_TICKERS = [
    "NVDA", "AMD", "AVGO", "INTC", "MRVL", "ARM", "QCOM", "MU",
    "MSFT", "GOOG", "GOOGL", "META", "AMZN", "AAPL", "CRM", "NOW",
    "SNOW", "PLTR", "AI", "PATH", "DDOG", "CRWD", "ZS", "PANW",
    "NET", "S", "SPLK", "SOUN", "BBAI", "BIGC", "UPST", "IONQ",
    "RGTI", "QUBT", "SMCI", "DELL", "HPE", "ANET", "CDNS", "SNPS",
    "ADSK", "ANSS", "TER", "ONTO", "WOLF", "ACLS", "LSCC", "MCHP",
    "NXPI", "ON", "MPWR", "MBLY", "LAZR", "INVZ", "LIDR",
]

# Leopold Aschenbrenner AI Infrastructure Portfolio
# Thesis: AI compute explosion → chips + power + data centers = bottlenecks
ASCHENBRENNER_TICKERS = [
    # AI Chips / Semiconductors
    "INTC", "AVGO", "NVDA", "TSM", "MU", "TSEM",
    # Optical Networking (data-center connectivity)
    "COHR", "LITE", "AAOI", "CIEN", "ANET",
    # Data Center Hardware
    "SMCI", "DELL", "WDC",
    # Data Center Operators / GPU Cloud
    "CORZ", "EQIX", "DLR",
    # AI Power & Energy
    "BE", "CEG", "NEE", "VST", "NRG",
    # Power Infrastructure (transformers, switchgear)
    "ETN", "VRT", "NVT", "GEV",
    # Bitcoin Miners → AI Compute Pivot
    "CIFR", "RIOT", "MARA", "HUT", "IREN",
    # Small/Mid-Cap AI Infrastructure
    "CRDO", "MTSI", "SITM", "POET",
]

SECTOR_MAP = {}
for t in RENEWABLE_ENERGY_TICKERS:
    SECTOR_MAP.setdefault(t, []).append("Renewable")
for t in NUCLEAR_ENERGY_TICKERS:
    SECTOR_MAP.setdefault(t, []).append("Nuclear")
for t in AI_TICKERS:
    SECTOR_MAP.setdefault(t, []).append("AI")
for t in ASCHENBRENNER_TICKERS:
    SECTOR_MAP.setdefault(t, []).append("Aschenbrenner")


# ─── NASDAQ 100 TICKERS ──────────────────────────────────────────────────────
# Fallback list — used only if live fetch fails
NASDAQ_100_FALLBACK = [
    "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMGN", "AMZN",
    "ANSS", "APP", "ARM", "ASML", "AVGO", "AXON", "AZN", "BIIB", "BKNG", "BKR",
    "CCEP", "CDNS", "CDW", "CEG", "CHTR", "CMCSA", "COIN", "COST", "CPRT", "CRWD",
    "CRDO", "CSCO", "CTAS", "CTSH", "DASH", "DDOG", "DLTR", "DXCM", "EA", "EXC",
    "FANG", "FAST", "FICO", "FTNT", "GEHC", "GILD", "GOOG", "GOOGL", "GFS", "GRAB",
    "HON", "IDXX", "ILMN", "INTC", "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN",
    "LRCX", "LULU", "MAR", "MCHP", "MDB", "MDLZ", "MELI", "META", "MNST", "MRVL",
    "MSFT", "MSTR", "MU", "NFLX", "NVDA", "NXPI", "ODFL", "ON", "ORLY", "PANW",
    "PAYX", "PCAR", "PDD", "PEP", "PLTR", "PYPL", "QCOM", "REGN", "ROST", "SBUX",
    "SMCI", "SNPS", "TEAM", "TOST", "TSLA", "TTD", "TTWO", "TXN", "VRSK", "VRTX",
    "WBD", "WDAY", "XEL", "ZS",
]

def get_nasdaq_tickers():
    """Fetch current NASDAQ 100 tickers dynamically, fall back to hardcoded list."""
    print("Fetching NASDAQ 100 ticker list...")
    # Try fetching from Wikipedia's NDX page
    try:
        import urllib.request, re
        url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
        # Wikipedia has ticker symbols as links: Nasdaq: AAPL or in table cells
        tickers = re.findall(r'(?:NASDAQ|Nasdaq):\s*([A-Z]{1,5})', html)
        if not tickers:
            tickers = re.findall(r'<td[^>]*>\s*<a[^>]*>([A-Z]{1,5})</a>\s*</td>', html)
        tickers = list(dict.fromkeys(tickers))  # dedupe, preserve order
        if len(tickers) >= 95:  # Sanity check: NDX should have ~101 symbols
            print(f"  Found {len(tickers)} NASDAQ 100 tickers (live)")
            return tickers
    except Exception as e:
        print(f"  Live fetch failed ({e})")

    print(f"  Using fallback list ({len(NASDAQ_100_FALLBACK)} tickers)")
    return list(NASDAQ_100_FALLBACK)


# ─── TECHNICAL INDICATORS ────────────────────────────────────────────────────
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def find_local_extrema(series, order=5):
    maxima, minima = [], []
    vals = series.values
    for i in range(order, len(vals) - order):
        if np.all(vals[i] >= vals[i-order:i]) and np.all(vals[i] >= vals[i+1:i+order+1]):
            maxima.append(i)
        if np.all(vals[i] <= vals[i-order:i]) and np.all(vals[i] <= vals[i+1:i+order+1]):
            minima.append(i)
    return maxima, minima


def detect_rsi_divergence(close, rsi, lookback=30):
    if len(close) < lookback + 10:
        return None
    recent = slice(-lookback, None)
    close_r = close.iloc[recent].reset_index(drop=True)
    rsi_r = rsi.iloc[recent].reset_index(drop=True)
    dates_r = close.index[recent]
    maxima, minima = find_local_extrema(close_r, order=3)
    if len(maxima) >= 2:
        i1, i2 = maxima[-2], maxima[-1]
        if (close_r.iloc[i2] > close_r.iloc[i1] and
            rsi_r.iloc[i2] < rsi_r.iloc[i1] and
            rsi_r.iloc[i2] > RSI_OVERBOUGHT):
            return ("Bearish Divergence", dates_r[i2])
    if len(minima) >= 2:
        i1, i2 = minima[-2], minima[-1]
        if (close_r.iloc[i2] < close_r.iloc[i1] and
            rsi_r.iloc[i2] > rsi_r.iloc[i1] and
            rsi_r.iloc[i2] < RSI_OVERSOLD):
            return ("Bullish Divergence", dates_r[i2])
    return None


def detect_ma_crossover(ma_short, ma_long, dates, window=5):
    if len(ma_short) < window + 2:
        return None
    for i in range(-window, 0):
        prev_diff = ma_short.iloc[i-1] - ma_long.iloc[i-1]
        curr_diff = ma_short.iloc[i] - ma_long.iloc[i]
        if np.isnan(prev_diff) or np.isnan(curr_diff):
            continue
        if prev_diff <= 0 and curr_diff > 0:
            return ("Bullish Cross", dates[i])
        if prev_diff >= 0 and curr_diff < 0:
            return ("Bearish Cross", dates[i])
    return None


# ─── ANALYSIS ─────────────────────────────────────────────────────────────────
def analyze_ticker(ticker, hist, min_bars=200):
    if hist is None or len(hist) < min_bars:
        return None
    close = hist['Close']
    dates = hist.index
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()
    ma150 = close.rolling(150).mean()
    rsi = compute_rsi(close, RSI_PERIOD)

    result = {
        'ticker': ticker,
        'last_close': round(float(close.iloc[-1]), 2),
        'last_rsi': round(float(rsi.iloc[-1]), 2) if not np.isnan(rsi.iloc[-1]) else None,
        'ma20': round(float(ma20.iloc[-1]), 2) if not np.isnan(ma20.iloc[-1]) else None,
        'ma50': round(float(ma50.iloc[-1]), 2) if not np.isnan(ma50.iloc[-1]) else None,
        'ma150': round(float(ma150.iloc[-1]), 2) if not np.isnan(ma150.iloc[-1]) else None,
        'sectors': SECTOR_MAP.get(ticker, []),
    }

    cross_50_150 = detect_ma_crossover(ma50, ma150, dates, CROSSOVER_WINDOW)
    result['ma50_150_signal'] = cross_50_150[0] if cross_50_150 else None
    result['ma50_150_date'] = cross_50_150[1].strftime('%Y-%m-%d') if cross_50_150 else None

    cross_20_50 = detect_ma_crossover(ma20, ma50, dates, CROSSOVER_WINDOW)
    result['ma20_50_signal'] = cross_20_50[0] if cross_20_50 else None
    result['ma20_50_date'] = cross_20_50[1].strftime('%Y-%m-%d') if cross_20_50 else None

    div = detect_rsi_divergence(close, rsi, DIVERGENCE_LOOKBACK)
    result['rsi_divergence'] = div[0] if div else None
    result['rsi_div_date'] = div[1].strftime('%Y-%m-%d') if div else None

    result['combined_signal'] = None
    if cross_50_150 and div:
        days_apart = abs((cross_50_150[1] - div[1]).days)
        if days_apart <= COMBO_WINDOW:
            result['combined_signal'] = f"{cross_50_150[0]} + {div[0]}"

    # ─── SIGNAL STRENGTH SCORING ──────────────────────────────────────
    # Score from -5 (Strong Sell) to +5 (Strong Buy)
    # Each signal contributes points in the bullish (+) or bearish (-) direction
    score = 0

    # MA50 x MA150 crossover (heaviest weight — long-term trend)
    if result['ma50_150_signal']:
        score += 2 if 'Bullish' in result['ma50_150_signal'] else -2

    # MA20 x MA50 crossover (medium weight — medium-term momentum)
    if result['ma20_50_signal']:
        score += 1.5 if 'Bullish' in result['ma20_50_signal'] else -1.5

    # RSI divergence (confirms trend reversal)
    if result['rsi_divergence']:
        score += 1.5 if 'Bullish' in result['rsi_divergence'] else -1.5

    # MA alignment bonus: price > MA20 > MA50 > MA150 = strong uptrend
    if result['ma20'] and result['ma50'] and result['ma150']:
        if result['last_close'] > result['ma20'] > result['ma50'] > result['ma150']:
            score += 1  # Perfect bullish alignment
        elif result['last_close'] < result['ma20'] < result['ma50'] < result['ma150']:
            score -= 1  # Perfect bearish alignment

    # RSI extreme bonus
    if result['last_rsi'] is not None:
        if result['last_rsi'] > 80:
            score -= 0.5  # Overbought warning
        elif result['last_rsi'] < 20:
            score += 0.5  # Oversold opportunity

    # Determine rating label
    score = round(score, 1)
    if score >= 4:
        rating = "Strong Buy"
    elif score >= 2:
        rating = "Buy"
    elif score >= 0.5:
        rating = "Weak Buy"
    elif score <= -4:
        rating = "Strong Sell"
    elif score <= -2:
        rating = "Sell"
    elif score <= -0.5:
        rating = "Weak Sell"
    else:
        rating = "Neutral"

    result['score'] = score
    result['rating'] = rating

    return result


def resample_to_4h(df_1h):
    """Resample 1-hour data to 4-hour bars."""
    ohlc = df_1h.resample('4h').agg({
        'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'
    }).dropna()
    return ohlc


def download_and_analyze(tickers, label="All NASDAQ", interval="1d", lookback_days=400, min_bars=200, timeframe_label="Daily"):
    results = []
    total = len(tickers)
    start_date = (datetime.now() - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    print(f"\nScanning {total} tickers for [{label}] on {timeframe_label}...")

    for i in range(0, total, BATCH_SIZE):
        batch = tickers[i:i+BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} tickers)...", end=" ", flush=True)
        try:
            data = yf.download(batch, start=start_date, end=end_date,
                               interval=interval, group_by='ticker', progress=False, threads=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(DELAY_BETWEEN_BATCHES)
            continue

        for ticker in batch:
            try:
                hist = data if len(batch) == 1 else data[ticker].dropna()
                if hist is not None and len(hist) > 0:
                    # Resample to 4H if needed
                    if timeframe_label == "4H":
                        hist = resample_to_4h(hist)
                    if len(hist) < min_bars:
                        continue
                    result = analyze_ticker(ticker, hist, min_bars=min_bars)
                    if result:
                        result['timeframe'] = timeframe_label
                        results.append(result)
            except Exception:
                pass

        print(f"done ({len(results)} analyzed so far)")
        if i + BATCH_SIZE < total:
            time.sleep(DELAY_BETWEEN_BATCHES)
    return results


# ─── HTML DASHBOARD ───────────────────────────────────────────────────────────
def build_html_dashboard(all_results, output_path):
    scan_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    data_json = json.dumps(all_results, default=str)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NASDAQ Screener — {scan_date}</title>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
    --green: #3fb950; --green-bg: rgba(63,185,80,0.12);
    --red: #f85149; --red-bg: rgba(248,81,73,0.12);
    --yellow: #d29922;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
         background: var(--bg); color: var(--text); padding: 20px; }}
  .header {{ display: flex; align-items: center; justify-content: space-between;
             padding: 20px 24px; background: var(--surface); border: 1px solid var(--border);
             border-radius: 12px; margin-bottom: 20px; }}
  .header h1 {{ font-size: 1.4em; font-weight: 600; }}
  .header .meta {{ color: var(--muted); font-size: 0.85em; }}

  .controls {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;
               padding: 16px; background: var(--surface); border: 1px solid var(--border);
               border-radius: 12px; align-items: center; }}
  .controls label {{ color: var(--muted); font-size: 0.8em; text-transform: uppercase;
                     letter-spacing: 0.5px; }}
  .filter-group {{ display: flex; flex-direction: column; gap: 4px; }}
  select, input[type=text] {{
    background: var(--bg); color: var(--text); border: 1px solid var(--border);
    padding: 8px 12px; border-radius: 8px; font-size: 0.9em; outline: none;
  }}
  select:focus, input:focus {{ border-color: var(--accent); }}

  .stats {{ display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }}
  .stat-card {{ padding: 16px 20px; background: var(--surface); border: 1px solid var(--border);
                border-radius: 10px; flex: 1; min-width: 140px; text-align: center;
                cursor: pointer; transition: border-color 0.2s, transform 0.1s; }}
  .stat-card:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
  .stat-card.active {{ border-color: var(--accent); box-shadow: 0 0 8px rgba(88,166,255,0.2); }}
  .stat-card .num {{ font-size: 1.8em; font-weight: 700; }}
  .stat-card .label {{ color: var(--muted); font-size: 0.8em; margin-top: 4px; }}

  .table-wrap {{ overflow-x: auto; border-radius: 12px; border: 1px solid var(--border); }}
  table {{ width: 100%; border-collapse: collapse; background: var(--surface); min-width: 900px; }}
  thead th {{ background: #1c2128; padding: 12px 14px; text-align: left; font-size: 0.8em;
              text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted);
              cursor: pointer; user-select: none; position: sticky; top: 0; white-space: nowrap; }}
  thead th:hover {{ color: var(--text); }}
  thead th .sort-arrow {{ margin-left: 4px; font-size: 0.7em; }}
  tbody td {{ padding: 10px 14px; border-top: 1px solid var(--border); font-size: 0.9em;
              white-space: nowrap; }}
  tbody tr:hover {{ background: rgba(88,166,255,0.04); }}

  .ticker-link {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
  .ticker-link:hover {{ text-decoration: underline; }}
  .bullish {{ color: var(--green); background: var(--green-bg); padding: 3px 8px;
              border-radius: 4px; font-weight: 600; font-size: 0.85em; display: inline-block; }}
  .bearish {{ color: var(--red); background: var(--red-bg); padding: 3px 8px;
              border-radius: 4px; font-weight: 600; font-size: 0.85em; display: inline-block; }}
  .sector-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px;
                 font-size: 0.75em; margin-right: 4px; border: 1px solid var(--border); }}
  .sector-Renewable {{ color: var(--green); border-color: var(--green); }}
  .sector-Nuclear {{ color: var(--yellow); border-color: var(--yellow); }}
  .sector-AI {{ color: var(--accent); border-color: var(--accent); }}
  .sector-Aschenbrenner {{ color: #f0883e; border-color: #f0883e; }}

  .empty {{ text-align: center; padding: 40px; color: var(--muted); }}
  .count {{ color: var(--muted); font-size: 0.85em; margin-bottom: 12px; }}
  .footer {{ text-align: center; color: var(--muted); font-size: 0.8em; margin-top: 20px; padding: 16px; }}

  .rating {{ padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.8em;
             display: inline-block; letter-spacing: 0.3px; white-space: nowrap; }}
  .rating-strong-buy {{ background: #0d5f2c; color: #3fb950; border: 1px solid #238636; }}
  .rating-buy {{ background: rgba(63,185,80,0.15); color: #3fb950; border: 1px solid rgba(63,185,80,0.3); }}
  .rating-weak-buy {{ background: rgba(63,185,80,0.08); color: #7ee787; border: 1px solid rgba(63,185,80,0.15); }}
  .rating-strong-sell {{ background: #5f0d0d; color: #f85149; border: 1px solid #da3633; }}
  .rating-sell {{ background: rgba(248,81,73,0.15); color: #f85149; border: 1px solid rgba(248,81,73,0.3); }}
  .rating-weak-sell {{ background: rgba(248,81,73,0.08); color: #ffa198; border: 1px solid rgba(248,81,73,0.15); }}
  .rating-neutral {{ background: rgba(139,148,158,0.1); color: var(--muted); border: 1px solid var(--border); }}
  .score-bar {{ display: inline-block; height: 6px; border-radius: 3px; margin-left: 6px; vertical-align: middle; }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>NASDAQ 100 Screener</h1>
    <div class="meta">MA Crossovers &amp; RSI Divergences &bull; Click any ticker to open in TradingView</div>
  </div>
  <div class="meta">Scanned: {scan_date}</div>
</div>

<div class="controls">
  <div class="filter-group">
    <label>Timeframe</label>
    <select id="timeframeFilter" onchange="applyFilters()">
      <option value="all">All Timeframes</option>
      <option value="4H">4H</option>
      <option value="Daily" selected>Daily</option>
      <option value="Weekly">Weekly</option>
      <option value="Monthly">Monthly</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Signal Type</label>
    <select id="signalFilter" onchange="applyFilters()">
      <option value="all">All Signals</option>
      <option value="ma50_150">MA50 x MA150</option>
      <option value="ma20_50">MA20 x MA50</option>
      <option value="rsi_div">RSI Divergence</option>
      <option value="combined">Combined (MA + RSI)</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Direction</label>
    <select id="directionFilter" onchange="applyFilters()">
      <option value="all">All</option>
      <option value="bullish">Bullish Only</option>
      <option value="bearish">Bearish Only</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Sector</label>
    <select id="sectorFilter" onchange="applyFilters()">
      <option value="all">All NASDAQ</option>
      <option value="Renewable">Renewable Energy</option>
      <option value="Nuclear">Nuclear Energy</option>
      <option value="AI">AI Companies</option>
      <option value="Aschenbrenner">Aschenbrenner Portfolio</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Rating</label>
    <select id="ratingFilter" onchange="applyFilters()">
      <option value="all">All Ratings</option>
      <option value="strong_buy">Strong Buy</option>
      <option value="buy">Buy / Strong Buy</option>
      <option value="sell">Sell / Strong Sell</option>
      <option value="strong_sell">Strong Sell</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Search Ticker</label>
    <input type="text" id="tickerSearch" placeholder="e.g. NVDA" oninput="applyFilters()">
  </div>
</div>

<div class="stats" id="statsBar"></div>
<div class="count" id="resultCount"></div>

<div class="table-wrap">
<table>
  <thead>
    <tr>
      <th onclick="sortBy('ticker')">Ticker <span class="sort-arrow" id="sort-ticker"></span></th>
      <th onclick="sortBy('timeframe')">TF <span class="sort-arrow" id="sort-timeframe"></span></th>
      <th onclick="sortBy('last_close')">Price <span class="sort-arrow" id="sort-last_close"></span></th>
      <th>Sectors</th>
      <th onclick="sortBy('ma50_150_signal')">MA50 x MA150 <span class="sort-arrow" id="sort-ma50_150_signal"></span></th>
      <th>Date</th>
      <th onclick="sortBy('ma20_50_signal')">MA20 x MA50 <span class="sort-arrow" id="sort-ma20_50_signal"></span></th>
      <th>Date</th>
      <th onclick="sortBy('rsi_divergence')">RSI Divergence <span class="sort-arrow" id="sort-rsi_divergence"></span></th>
      <th>Date</th>
      <th onclick="sortBy('last_rsi')">RSI <span class="sort-arrow" id="sort-last_rsi"></span></th>
      <th onclick="sortBy('combined_signal')">Combined <span class="sort-arrow" id="sort-combined_signal"></span></th>
      <th onclick="sortBy('score')">Score <span class="sort-arrow" id="sort-score"></span></th>
      <th onclick="sortBy('rating')">Rating <span class="sort-arrow" id="sort-rating"></span></th>
    </tr>
  </thead>
  <tbody id="tableBody"></tbody>
</table>
</div>

<div class="footer">
  Data from Yahoo Finance via yfinance &bull; Dashboard auto-generated by nasdaq_screener.py
</div>

<script>
const DATA = {data_json};
let currentSort = {{ col: 'ticker', asc: true }};
let filtered = [];

function signalClass(val) {{
  if (!val) return '';
  return val.toLowerCase().includes('bullish') ? 'bullish' : 'bearish';
}}

function tvLink(ticker) {{
  return `https://www.tradingview.com/chart/?symbol=${{ticker}}`;
}}

function ratingClass(rating) {{
  if (!rating) return 'rating-neutral';
  return 'rating-' + rating.toLowerCase().replace(/\\s+/g, '-');
}}

function scoreBar(score) {{
  if (score == null) return '';
  const abs = Math.min(Math.abs(score), 5);
  const width = abs * 12;
  const color = score > 0 ? 'var(--green)' : score < 0 ? 'var(--red)' : 'var(--muted)';
  return `<span class="score-bar" style="width:${{width}}px;background:${{color}}"></span>`;
}}

function filterByCard(rating) {{
  document.getElementById('ratingFilter').value = rating;
  applyFilters();
}}

function applyFilters() {{
  const tf = document.getElementById('timeframeFilter').value;
  const sig = document.getElementById('signalFilter').value;
  const dir = document.getElementById('directionFilter').value;
  const sec = document.getElementById('sectorFilter').value;
  const rat = document.getElementById('ratingFilter').value;
  const search = document.getElementById('tickerSearch').value.toUpperCase().trim();

  filtered = DATA.filter(r => {{
    if (tf !== 'all' && r.timeframe !== tf) return false;
    let hasSignal = r.ma50_150_signal || r.ma20_50_signal || r.rsi_divergence || r.combined_signal;
    if (!hasSignal) return false;
    if (sig === 'ma50_150' && !r.ma50_150_signal) return false;
    if (sig === 'ma20_50' && !r.ma20_50_signal) return false;
    if (sig === 'rsi_div' && !r.rsi_divergence) return false;
    if (sig === 'combined' && !r.combined_signal) return false;
    if (dir === 'bullish') {{
      let b = [r.ma50_150_signal, r.ma20_50_signal, r.rsi_divergence, r.combined_signal]
              .filter(Boolean).some(s => s.includes('Bullish'));
      if (!b) return false;
    }}
    if (dir === 'bearish') {{
      let b = [r.ma50_150_signal, r.ma20_50_signal, r.rsi_divergence, r.combined_signal]
              .filter(Boolean).some(s => s.includes('Bearish'));
      if (!b) return false;
    }}
    if (rat === 'strong_buy' && r.rating !== 'Strong Buy') return false;
    if (rat === 'buy' && r.score <= 0) return false;
    if (rat === 'sell' && r.score >= 0) return false;
    if (rat === 'strong_sell' && r.rating !== 'Strong Sell') return false;
    if (sec !== 'all' && (!r.sectors || !r.sectors.includes(sec))) return false;
    if (search && !r.ticker.includes(search)) return false;
    return true;
  }});
  sortData();
  render();
}}

function sortBy(col) {{
  if (currentSort.col === col) currentSort.asc = !currentSort.asc;
  else {{ currentSort.col = col; currentSort.asc = true; }}
  sortData();
  render();
}}

function sortData() {{
  const col = currentSort.col;
  const asc = currentSort.asc;
  filtered.sort((a, b) => {{
    let va = a[col], vb = b[col];
    if (va == null) va = '';
    if (vb == null) vb = '';
    if (typeof va === 'number' && typeof vb === 'number') return asc ? va - vb : vb - va;
    return asc ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va));
  }});
}}

function render() {{
  let strongBuy = 0, buy = 0, strongSell = 0, sell = 0;
  filtered.forEach(r => {{
    if (r.rating === 'Strong Buy') strongBuy++;
    else if (r.rating === 'Buy' || r.rating === 'Weak Buy') buy++;
    else if (r.rating === 'Strong Sell') strongSell++;
    else if (r.rating === 'Sell' || r.rating === 'Weak Sell') sell++;
  }});
  const activeRat = document.getElementById('ratingFilter').value;
  document.getElementById('statsBar').innerHTML = `
    <div class="stat-card ${{activeRat==='all'?'active':''}}" onclick="filterByCard('all')"><div class="num" style="color:var(--text)">${{filtered.length}}</div><div class="label">Stocks with Signals</div></div>
    <div class="stat-card ${{activeRat==='strong_buy'?'active':''}}" onclick="filterByCard('strong_buy')"><div class="num" style="color:#3fb950">${{strongBuy}}</div><div class="label">Strong Buy</div></div>
    <div class="stat-card ${{activeRat==='buy'?'active':''}}" onclick="filterByCard('buy')"><div class="num" style="color:#7ee787">${{buy}}</div><div class="label">Buy</div></div>
    <div class="stat-card ${{activeRat==='sell'?'active':''}}" onclick="filterByCard('sell')"><div class="num" style="color:#ffa198">${{sell}}</div><div class="label">Sell</div></div>
    <div class="stat-card ${{activeRat==='strong_sell'?'active':''}}" onclick="filterByCard('strong_sell')"><div class="num" style="color:#f85149">${{strongSell}}</div><div class="label">Strong Sell</div></div>
  `;
  document.getElementById('resultCount').textContent = `Showing ${{filtered.length}} of ${{DATA.length}} stocks scanned`;

  document.querySelectorAll('.sort-arrow').forEach(el => el.textContent = '');
  const arrowEl = document.getElementById(`sort-${{currentSort.col}}`);
  if (arrowEl) arrowEl.textContent = currentSort.asc ? '▲' : '▼';

  const tbody = document.getElementById('tableBody');
  if (filtered.length === 0) {{
    tbody.innerHTML = '<tr><td colspan="14" class="empty">No signals found for current filters</td></tr>';
    return;
  }}
  tbody.innerHTML = filtered.map(r => `
    <tr>
      <td><a class="ticker-link" href="${{tvLink(r.ticker)}}" target="_blank" title="Open ${{r.ticker}} in TradingView">${{r.ticker}}</a></td>
      <td style="color:var(--muted);font-size:0.85em">${{r.timeframe || 'Daily'}}</td>
      <td>${{r.last_close != null ? '$' + r.last_close.toFixed(2) : '—'}}</td>
      <td>${{(r.sectors || []).map(s => `<span class="sector-tag sector-${{s}}">${{s}}</span>`).join('') || '—'}}</td>
      <td>${{r.ma50_150_signal ? `<span class="${{signalClass(r.ma50_150_signal)}}">${{r.ma50_150_signal}}</span>` : '—'}}</td>
      <td style="color:var(--muted);font-size:0.85em">${{r.ma50_150_date || ''}}</td>
      <td>${{r.ma20_50_signal ? `<span class="${{signalClass(r.ma20_50_signal)}}">${{r.ma20_50_signal}}</span>` : '—'}}</td>
      <td style="color:var(--muted);font-size:0.85em">${{r.ma20_50_date || ''}}</td>
      <td>${{r.rsi_divergence ? `<span class="${{signalClass(r.rsi_divergence)}}">${{r.rsi_divergence}}</span>` : '—'}}</td>
      <td style="color:var(--muted);font-size:0.85em">${{r.rsi_div_date || ''}}</td>
      <td style="color:${{r.last_rsi > 70 ? 'var(--red)' : r.last_rsi < 30 ? 'var(--green)' : 'var(--text)'}}">${{r.last_rsi != null ? r.last_rsi.toFixed(1) : '—'}}</td>
      <td>${{r.combined_signal ? `<span class="${{signalClass(r.combined_signal)}}">${{r.combined_signal}}</span>` : '—'}}</td>
      <td style="text-align:center">${{r.score != null ? r.score.toFixed(1) : '—'}}${{scoreBar(r.score)}}</td>
      <td><span class="rating ${{ratingClass(r.rating)}}">${{r.rating || '—'}}</span></td>
    </tr>
  `).join('');
}}

applyFilters();
</script>
</body>
</html>"""
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"\nDashboard saved: {output_path}")


# ─── EMAIL ALERTS ────────────────────────────────────────────────────────────
def send_email_alerts(results, output_dir):
    """Send email if new Strong Buy or Strong Sell signals appear since last run."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Check env vars — skip if not configured
    smtp_user = os.environ.get('ALERT_EMAIL_FROM', '')
    smtp_pass = os.environ.get('ALERT_EMAIL_PASSWORD', '')
    alert_to = os.environ.get('ALERT_EMAIL_TO', '')
    if not (smtp_user and smtp_pass and alert_to):
        print("\nEmail alerts: skipped (ALERT_EMAIL_FROM / ALERT_EMAIL_PASSWORD / ALERT_EMAIL_TO not set)")
        return

    # Load previous signals
    prev_file = os.path.join(output_dir, 'previous_signals.json')
    prev_keys = set()
    if os.path.exists(prev_file):
        try:
            with open(prev_file) as f:
                prev_keys = set(json.load(f))
        except Exception:
            pass

    # Find notable signals (Strong Buy / Strong Sell on Daily timeframe primarily)
    notable = []
    current_keys = []
    for r in results:
        has_signal = r.get('ma50_150_signal') or r.get('ma20_50_signal') or r.get('rsi_divergence')
        if not has_signal:
            continue
        key = f"{r['ticker']}_{r.get('timeframe','Daily')}_{r.get('rating','')}"
        current_keys.append(key)
        if key not in prev_keys and r.get('rating') in ('Strong Buy', 'Strong Sell', 'Buy', 'Sell'):
            notable.append(r)

    # Save current keys for next run
    with open(prev_file, 'w') as f:
        json.dump(current_keys, f)

    if not notable:
        print(f"\nEmail alerts: no new notable signals to report")
        return

    # Build email body
    scan_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    strong_buys = [r for r in notable if r.get('rating') in ('Strong Buy', 'Buy')]
    strong_sells = [r for r in notable if r.get('rating') in ('Strong Sell', 'Sell')]

    body_lines = [f"<h2>NASDAQ 100 Screener Alert — {scan_date}</h2>"]
    body_lines.append(f"<p>{len(notable)} new signal(s) detected.</p>")

    if strong_buys:
        body_lines.append("<h3 style='color:#3fb950'>New Buy Signals</h3><ul>")
        for r in strong_buys:
            tf = r.get('timeframe', 'Daily')
            ticker = r['ticker']
            tv_url = f"https://www.tradingview.com/chart/?symbol={ticker}"
            body_lines.append(
                f"<li><b>{ticker}</b> ({tf}) — {r['rating']} (score: {r.get('score', 0):.1f}) "
                f"| Price: ${r.get('last_close', 0):.2f} "
                f"<a href='{tv_url}'>TradingView</a></li>"
            )
        body_lines.append("</ul>")

    if strong_sells:
        body_lines.append("<h3 style='color:#f85149'>New Sell Signals</h3><ul>")
        for r in strong_sells:
            tf = r.get('timeframe', 'Daily')
            ticker = r['ticker']
            tv_url = f"https://www.tradingview.com/chart/?symbol={ticker}"
            body_lines.append(
                f"<li><b>{ticker}</b> ({tf}) — {r['rating']} (score: {r.get('score', 0):.1f}) "
                f"| Price: ${r.get('last_close', 0):.2f} "
                f"<a href='{tv_url}'>TradingView</a></li>"
            )
        body_lines.append("</ul>")

    body_lines.append(f"<p><a href='https://eburstz.github.io/nasdaq-screener/'>View Full Dashboard</a></p>")

    html_body = "\n".join(body_lines)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Screener Alert: {len(notable)} new signals — {scan_date}"
    msg['From'] = smtp_user
    msg['To'] = alert_to
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"\nEmail alert sent to {alert_to} with {len(notable)} new signals")
    except Exception as e:
        print(f"\nEmail alert failed: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  NASDAQ 100 STOCK SCREENER — Multi-Timeframe")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    base_tickers = get_nasdaq_tickers()

    # Collect all sector extras that aren't already in NASDAQ 100
    base_set = set(base_tickers)
    extra_tickers = []
    for extra_list in [RENEWABLE_ENERGY_TICKERS, NUCLEAR_ENERGY_TICKERS, AI_TICKERS, ASCHENBRENNER_TICKERS]:
        for t in extra_list:
            if t not in base_set:
                extra_tickers.append(t)
                base_set.add(t)

    all_tickers = base_tickers + extra_tickers
    all_results = []

    for tf_label, tf_interval, tf_days, tf_min_bars in TIMEFRAMES:
        print(f"\n{'─'*40}")
        print(f"  Timeframe: {tf_label}")
        print(f"{'─'*40}")
        tf_results = download_and_analyze(
            all_tickers, f"NASDAQ 100 + Sectors",
            interval=tf_interval, lookback_days=tf_days,
            min_bars=tf_min_bars, timeframe_label=tf_label
        )
        all_results.extend(tf_results)

    # Output
    output_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    output_path = os.path.join(output_dir, "NASDAQ_Screener_Dashboard.html")
    if len(sys.argv) > 1:
        output_path = sys.argv[1]

    build_html_dashboard(all_results, output_path)

    has_any = [r for r in all_results
               if r.get('ma50_150_signal') or r.get('ma20_50_signal') or r.get('rsi_divergence')]
    print(f"\n{'='*60}")
    print(f"  DONE: {len(all_results)} stocks scanned, {len(has_any)} with signals")
    print(f"  Open NASDAQ_Screener_Dashboard.html in your browser.")
    print(f"{'='*60}")

    # ─── EMAIL ALERTS ──────────────────────────────────────────────────
    send_email_alerts(all_results, output_dir)


if __name__ == "__main__":
    main()
