# Stock Screener Quick Reference

## 🎯 Start Here - Daily Workflow

1. Open `nasdaq_screener_enhanced.xlsx`
2. Go to **🌟 TOP PICKS** sheet
3. Look at top 10-20 rows (sorted by score)
4. Check your criteria below

---

## 📊 Score Quick Guide

| Score | Meaning | Action |
|-------|---------|--------|
| **9-10** | Exceptional - Multiple strong confirmations | Investigate immediately |
| **7.5-9** | Strong - Very good setup | Review carefully |
| **6-7.5** | Good - Worth considering | Additional research needed |
| **4-6** | Moderate - Weak signals | Probably skip |
| **<4** | Weak - Minimal confirmation | Skip |

---

## 🎨 Color Coding in Excel

### Score Column
- 🟢 **Dark Green** (7.5+): Strongest signals
- 🟢 **Light Green** (6.0-7.5): Good signals
- 🟠 **Orange** (4.0-6.0): Moderate
- ⚪ **Gray** (<4.0): Weak

### Risk Column
- 🟢 **Green**: Low Risk
- 🟡 **Yellow**: Medium Risk
- 🔴 **Red**: High Risk

---

## 🔢 Indicator Cheat Sheet

### RSI (Relative Strength Index)
```
>70  = Overbought (potential reversal down)
50-70 = Bullish
30-50 = Bearish
<30  = Oversold (potential reversal up)
```

### Volume Ratio
```
<0.8x  = Below average (weak interest)
0.8-1.2x = Normal
1.5-2.0x = Strong interest ✓
>2.0x  = Unusual activity (investigate)
```

### ADX (Trend Strength)
```
<20  = No trend (choppy, avoid)
20-25 = Weak trend
25-40 = Good trend ✓
>40  = Very strong trend ✓✓
```

### Bollinger Band Position (BB%)
```
0-10%  = Near lower band (oversold)
10-40% = Below middle
40-60% = Middle range
60-90% = Above middle
90-100% = Near upper band (overbought)
```

### Price Momentum
```
5-Day %:  Recent swing (today's mood)
20-Day %: Monthly trend (current direction)
60-Day %: Quarterly trend (bigger picture)
```

---

## 🎪 Trading Styles

### Day Trading / Scalping
**Look for:**
- Score: ≥6.5
- MA20×50 signals (faster)
- Volume: ≥1.5x
- 5-Day %: -5% to +5% (not extended)
- Risk: Any (use stops)

### Swing Trading (Days to Weeks)
**Look for:**
- Score: ≥7.0
- MA20×50 or MA50×150
- ADX: ≥25
- Volume: ≥1.2x
- Risk: Low/Medium preferred

### Position Trading (Weeks to Months)
**Look for:**
- Score: ≥7.5
- MA50×150 or Combined signals
- ADX: ≥30
- Market Cap: Large/Mega
- 60-Day %: Positive trend
- Risk: Low/Medium only

---

## 🚦 Signal Strength

### Strong Bullish Setup
```
✓ MA Bullish Cross (50×150 or 20×50)
✓ MACD: Bullish MACD Cross
✓ Volume: >1.5x
✓ ADX: >25
✓ Score: ≥7.0
```

### Strong Bearish Setup
```
✓ MA Bearish Cross (50×150 or 20×50)
✓ MACD: Bearish MACD Cross
✓ Volume: >1.5x
✓ ADX: >25
✓ Score: ≥7.0
```

### Reversal Setup (RSI Divergence)
```
✓ RSI Bullish Divergence (RSI <30)
✓ Price at lower Bollinger Band (BB% <20)
✓ Volume increasing
✓ Score: ≥6.5
```

---

## 🎯 Filtering Tips

### Excel Filter Examples

**Conservative (Low Risk):**
1. Score: ≥7.5
2. Risk: Low
3. Market Cap: Large Cap or Mega Cap
4. ADX: ≥30
5. Volume: ≥1.5

**Moderate (Balanced):**
1. Score: ≥7.0
2. Risk: Low or Medium
3. ADX: ≥25
4. Volume: ≥1.2
5. Signal: Contains "Bullish"

**Aggressive (High Reward):**
1. Score: ≥6.5
2. Market Cap: Small Cap or Mid Cap
3. Volume: ≥2.0 (unusual activity)
4. 5-Day %: Between -5 and +5 (not extended)
5. MACD: Contains "Bullish"

---

## ⚠️ Warning Signs (Skip These)

❌ **Score <6.0** = Weak signals
❌ **ADX <20** = Choppy, no clear trend
❌ **Volume <0.8x** = No interest
❌ **5-Day % >15%** = Already extended (late to the party)
❌ **High Risk + Mega move** = Dangerous combination
❌ **RSI >80 or <20** = Extreme levels (higher risk)

---

## 💡 Pro Tips

### Tip #1: Multiple Confirmations
Don't rely on one signal. Look for:
- **2 indicators minimum** (e.g., MA Cross + Volume)
- **3+ = High confidence** (e.g., MA + MACD + ADX)

### Tip #2: Match Timeframes
- **Short-term trade?** → Use MA20×50, 5D%, Volume
- **Long-term trade?** → Use MA50×150, 60D%, ADX

### Tip #3: Check "Key Factors" Column
Shows what drove the score:
```
"MA50×150 (9/10) | MACD Confirm | Volume 2.1x | ADX 35"
```
This tells you it's a strong setup with multiple confirmations.

### Tip #4: Risk Management
- **Low Risk** = Can use larger position
- **Medium Risk** = Use 50-75% normal size
- **High Risk** = Use 25-50% normal size OR skip

### Tip #5: Don't Chase
If stock already moved 10-15% in 5 days:
- ✓ Wait for pullback
- ✓ Or skip it entirely
- ✗ Don't FOMO into extended moves

---

## 📋 Daily Checklist

**Morning Routine:**
- [ ] Run screener (or use yesterday's if intraday)
- [ ] Open TOP PICKS sheet
- [ ] Filter: Score ≥7.0, Risk = your tolerance
- [ ] Note top 5-10 tickers
- [ ] Check charts on TradingView/Finviz
- [ ] Verify signals visually
- [ ] Check for news/earnings
- [ ] Plan entries/exits/stops

**Before Trade:**
- [ ] Score ≥6.5?
- [ ] Risk level acceptable?
- [ ] Volume confirmation?
- [ ] Chart looks clean?
- [ ] News/fundamentals support trade?
- [ ] Stop loss level identified?
- [ ] Position size calculated?

---

## 🧮 Position Sizing Example

**Account: $10,000**
**Risk per trade: 2% = $200**

### Low Risk Stock
- **Risk:** Low
- **Score:** 8.0
- **Position size:** 100% of planned ($2,000)
- **Stop loss:** $1 below entry
- **Shares:** 200 shares

### Medium Risk Stock
- **Risk:** Medium
- **Score:** 7.0
- **Position size:** 75% of planned ($1,500)
- **Stop loss:** $1.50 below entry
- **Shares:** 133 shares (adjust stop to $1.50)

### High Risk Stock
- **Risk:** High
- **Score:** 7.5 (strong signal but risky)
- **Position size:** 50% of planned ($1,000)
- **Stop loss:** $2 below entry
- **Shares:** 100 shares

---

## 📞 Quick Decision Tree

```
Open TOP PICKS → Sort by Score

Score ≥7.5?
├─ YES → Check Risk Level
│  ├─ Low/Medium → Check Volume ≥1.2x?
│  │  ├─ YES → Check Chart → CANDIDATE ✓
│  │  └─ NO → Skip (no interest)
│  └─ High → Comfortable with risk?
│     ├─ YES → Reduce position size → CANDIDATE ✓
│     └─ NO → Skip
└─ NO → Move to next stock
```

---

## 🔍 Where to Find What

| What You Want | Which Sheet |
|---------------|-------------|
| Best opportunities overall | 🌟 TOP PICKS |
| Only high-scoring stocks | "All High Score" |
| Longer-term trends | "All MA50×150" |
| Shorter-term momentum | "All MA20×50" |
| Reversal setups | "All RSI Div" |
| Strongest setups | "All Combined" |
| Renewable energy plays | "RE High Score" |
| Nuclear sector | "Nuc High Score" |
| AI sector | "AI High Score" |
| Overview and stats | 📊 Summary |

---

## 🎓 Learning Resources

As you use the screener, track:
- Which score range works best for you
- Which risk level you're comfortable with
- Which indicators you rely on most
- Which setups have highest success rate

**Keep a trading journal:**
```
Date: 2026-03-04
Ticker: NVDA
Score: 8.5 | Risk: Low
Entry: $850 | Stop: $830
Exit: $890 (+4.7%)
Notes: MA50×150 bullish + volume spike + MACD confirm
```

---

**Remember: The screener finds opportunities. You make the trading decisions.** ✓

---

## 📞 If You Get Stuck

**Too many results?**
→ Increase score threshold to 7.5+

**No results?**
→ Lower score threshold to 6.0+

**All High Risk?**
→ Filter by Market Cap: Large/Mega Cap only

**Signals contradict each other?**
→ Skip it. Wait for clear setup.

**Not sure what to look at first?**
→ Start with TOP PICKS, top 10 rows, that's it.

---

Print this and keep it next to your screen! 📄
