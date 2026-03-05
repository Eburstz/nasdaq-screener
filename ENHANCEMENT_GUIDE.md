# Enhanced Stock Screener - User Guide

## What's New

The enhanced screener adds **intelligent scoring, risk assessment, and 5 additional technical indicators** to help you identify the best trading opportunities with minimal effort.

---

## Key Enhancements

### 1. **Signal Strength Scoring (0-10)**
Every stock now gets an overall score based on:
- **MA Crossover Strength** (how far apart the averages are)
- **RSI Divergence Magnitude** (how strong the divergence is)
- **MACD Confirmation** (trend momentum agreement)
- **Volume Spike** (1.5x+ average = strong interest)
- **ADX Trend Strength** (>25 = trending, >40 = strong trend)
- **Bollinger Band Position** (near extremes = oversold/overbought)

**How to use:**
- **Score 7.5-10**: Strongest signals with multiple confirmations → Review first
- **Score 6.0-7.5**: Good signals worth investigating
- **Score 4.0-6.0**: Moderate signals, needs additional analysis
- **Score <4.0**: Weak signals, probably skip

### 2. **Risk Assessment**
Every stock is classified as **Low Risk**, **Medium Risk**, or **High Risk** based on:
- Volatility (Bollinger Band width)
- RSI extremes (>80 or <20 = higher risk)
- Market cap (smaller = higher risk)
- Recent price swings

**Color coded in Excel:**
- 🟢 Green = Low Risk
- 🟡 Yellow = Medium Risk
- 🔴 Red = High Risk

### 3. **Additional Technical Indicators**

#### **MACD (Moving Average Convergence Divergence)**
Shows trend momentum. Look for:
- "Bullish MACD Cross" = momentum turning up
- "Bearish MACD Cross" = momentum turning down
- Best when it confirms your MA crossover signals

#### **ADX (Average Directional Index)**
Measures trend strength (not direction):
- **ADX < 25**: Weak/no trend (choppy market)
- **ADX 25-40**: Trending market
- **ADX > 40**: Strong trend (signals are more reliable)

#### **Bollinger Bands**
Volatility indicator showing price extremes:
- **BB% near 0**: Price at lower band (oversold)
- **BB% near 100**: Price at upper band (overbought)
- **BB Width %**: High = volatile stock, Low = stable

#### **Volume Ratio**
Current volume vs 20-day average:
- **1.0x**: Normal volume
- **1.5x+**: Significant spike (strong interest)
- **2.0x+**: Unusual activity (investigate why)

#### **Price Momentum**
Percentage change over different periods:
- **5-Day %**: Very short-term momentum
- **20-Day %**: Monthly trend
- **60-Day %**: Quarterly trend

### 4. **Market Cap Classification**
Stocks categorized by size:
- **Mega Cap** (>$200B): Safest, least volatile (AAPL, MSFT, NVDA)
- **Large Cap** ($10B-$200B): Established companies
- **Mid Cap** ($2B-$10B): Growth potential, moderate risk
- **Small Cap** ($300M-$2B): Higher risk, higher reward
- **Micro Cap** (<$300M): Highest risk/reward

---

## New Excel Sheets

### 🌟 **TOP PICKS** (Start Here!)
- Shows the **top 50 highest-scoring stocks** across all NASDAQ
- Sorted by score (highest first)
- Includes all key data in one view
- **"Key Factors" column** explains what contributed to the score

**Workflow:**
1. Open Excel → Go to "TOP PICKS" sheet
2. Look at Score 7.5+ stocks first
3. Check Risk level (match your tolerance)
4. Read "Key Factors" to understand why it scored high
5. Note the ticker and do your own research

### 📊 **Summary**
- Overview of all results
- **"High Score (≥6.0)"** stat shows how many strong signals found
- Includes "How to Use This Report" guide
- Explains each indicator

### **High Score Sheets** (NEW)
- Each category (All/RE/Nuc/AI) now has a "High Score" sheet
- Only shows stocks with score ≥6.0
- Pre-filtered for quality
- Sorted by score

---

## How to Use the Enhanced Screener

### For Active Traders (Short-Term)
1. Check **"TOP PICKS"** sheet
2. Filter for **Score ≥7.0** + **Low/Medium Risk**
3. Look for:
   - **MA20×50 signals** (faster)
   - **Volume >1.5x** (strong interest)
   - **MACD confirmation**
4. Focus on **5-Day %** and **20-Day %** momentum

### For Swing Traders (Medium-Term)
1. Check **"TOP PICKS"** or **"MA50×150"** sheets
2. Filter for **Score ≥6.5** + **ADX >25**
3. Look for:
   - **MA50×150 Bullish Cross** (trend change)
   - **Volume confirmation**
   - **RSI not extreme** (30-70 range)
4. Focus on **20-Day %** and **60-Day %** momentum

### For Position Traders (Long-Term)
1. Check **"Combined"** sheets (multiple signals = stronger)
2. Filter for **Score ≥7.0** + **Large/Mega Cap**
3. Look for:
   - **Combined signals** (MA + RSI Divergence)
   - **ADX >30** (strong trend)
   - **Positive 60-Day %** momentum
4. Focus on fundamentals after technical screening

### For Risk Management
1. **Never ignore the Risk column**
2. High Risk stocks = use smaller position sizes
3. Check **BB Width %** (volatility):
   - <10%: Stable (easier to manage)
   - 10-20%: Normal volatility
   - >20%: High volatility (wider stops needed)

---

## Understanding the Scoring System

### Example Breakdown

**Stock: XYZ | Score: 8.2 | Risk: Medium**

**Key Factors: "MA50×150 (8/10) | MACD Confirm | Volume 2.1x | ADX 35"**

**What this means:**
1. **MA50×150 (8/10)**: Strong crossover with good separation between averages
2. **MACD Confirm**: Momentum indicator agrees with the trend
3. **Volume 2.1x**: More than double normal volume (strong interest)
4. **ADX 35**: Moderate-to-strong trending market (not choppy)

**Total Score: 8.2/10** = This is a high-quality setup with multiple confirmations

**Risk: Medium** = Consider position sizing (not full allocation)

---

## Tips for Best Results

### DO:
✅ Start with TOP PICKS sheet (highest scoring opportunities)
✅ Match risk level to your risk tolerance
✅ Read "Key Factors" to understand WHY it scored high
✅ Look for 2+ confirmations (MA + MACD, or MA + Volume)
✅ Check ADX to confirm trending market (>25)
✅ Use score as a filter, not a buy signal

### DON'T:
❌ Buy based on score alone (always do your own research)
❌ Ignore risk level (high scores can still be high risk)
❌ Trade without stop losses (technical signals can fail)
❌ Chase stocks that already moved 15%+ in 5 days
❌ Trade against the overall market trend

---

## Comparing Original vs Enhanced

| Feature | Original | Enhanced |
|---------|----------|----------|
| **Sheets** | 17 | 21 |
| **Indicators** | 3 (MA, RSI) | 8 (MA, RSI, MACD, ADX, BB, Volume, Momentum, Market Cap) |
| **Scoring** | None | 0-10 scale with factors |
| **Risk Assessment** | None | Low/Medium/High |
| **Top Picks** | None | Dedicated sheet with top 50 |
| **Sorting** | Alphabetical | By signal strength (score) |
| **Key Factors** | None | Explains what drives the score |
| **Color Coding** | Basic | Score-based (green/orange/gray) |
| **Actionability** | Lists signals | Prioritizes opportunities |

---

## Example Trading Workflow

1. **Morning:** Run the enhanced screener
   ```bash
   source venv/bin/activate
   python3 nasdaq_screener_enhanced.py
   ```

2. **Open Excel → TOP PICKS sheet**

3. **Filter:**
   - Score ≥7.0
   - Risk = Low or Medium (match your tolerance)
   - Signal = Bullish (if trading long)

4. **Review Top 10:**
   - Read "Key Factors" for each
   - Check if ADX >25 (trending)
   - Note if Volume >1.5x (strong interest)

5. **Chart Analysis:**
   - Open TradingView/Finviz for top candidates
   - Verify the signal visually
   - Check for support/resistance levels
   - Identify entry/exit points

6. **Fundamental Check:**
   - Why did this stock move?
   - Any news/earnings coming up?
   - Is the sector strong?

7. **Trade Planning:**
   - Entry: Near current price or better
   - Stop Loss: Below recent support or MA
   - Target: Based on chart pattern / risk:reward
   - Position Size: Based on risk level

---

## Advanced Features

### Using "Key Factors" Column
This column shows exactly what made the score high. Use it to understand the setup:

- **"MA50×150 (9/10)"**: Very strong crossover
- **"MA20×50 (5/10)"**: Moderate crossover
- **"RSI Div (7/10)"**: Strong divergence
- **"MACD Confirm"**: Trend momentum agrees
- **"Volume 2.3x"**: More than double average
- **"ADX 42"**: Strong trending market
- **"Near Lower BB"**: Potentially oversold
- **"Near Upper BB"**: Potentially overbought

### Combining Filters
In Excel, use multiple filters for precision:

**Conservative Setup:**
- Score ≥7.5
- Risk = Low
- Market Cap = Large/Mega Cap
- ADX >30
- Volume >1.5x

**Aggressive Setup:**
- Score ≥6.5
- Risk = Medium/High
- Market Cap = Small/Mid Cap
- MACD = Bullish MACD Cross
- 5D% >5 (strong momentum)

---

## Troubleshooting

### "Too many results, how do I narrow down?"
Start with score ≥7.5 (only strongest signals). That should give you 10-30 stocks.

### "High score but stock already moved a lot?"
Check **5-Day %** and **20-Day %**. If >10-15%, you might be late. Wait for pullback or skip it.

### "Score is high but I'm nervous"
Check **Risk** column. If it says "High Risk", either:
1. Use smaller position size
2. Wait for confirmation (another green day)
3. Skip it (plenty of other opportunities)

### "What if score is 6.0 but all factors look good?"
Score is just a starting point. If you see strong volume, MACD confirmation, and ADX >35, it might still be worth considering.

---

## Next Steps

1. **Run the enhanced screener daily or weekly**
2. **Track which setups work best for you** (make notes)
3. **Adjust filters to match your trading style**
4. **Combine with your own chart analysis**
5. **Always use proper risk management**

---

## Questions?

The enhanced screener gives you:
- ✅ **Prioritized opportunities** (TOP PICKS)
- ✅ **Signal strength** (0-10 score)
- ✅ **Risk assessment** (Low/Medium/High)
- ✅ **Multiple confirmations** (8 indicators)
- ✅ **Actionable insights** (Key Factors column)

Use it as a **starting point for research**, not as buy/sell signals. Always do your own analysis and manage your risk.

---

**Happy trading!** 📈
