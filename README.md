# 💎 Luxury Retail Financial Dashboard - Alpha Vantage API

## ✅ This Version ACTUALLY Works (Free Tier)

**Uses Alpha Vantage API - Reliable, truly free, been working for years**

### Why Alpha Vantage?
- ✅ **Actually free** - 25 API calls per day (no bait-and-switch)
- ✅ **No legacy restrictions** - all endpoints work for new users
- ✅ **Reliable** - been stable since 2017
- ✅ **Complete data** - Revenue, EBITDA, PBT, PAT, Free Cash Flow
- ✅ **Simple API** - no versioning issues

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Get FREE Alpha Vantage API Key

1. Visit: **https://www.alphavantage.co/support/#api-key**
2. Enter your email
3. Get instant API key (no verification needed!)
4. Copy the key (looks like: `ABC123XYZ`)

### Step 2: Edit Line 21

1. Open `app.py`
2. Line 21: `ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"`
3. Replace with: `ALPHA_VANTAGE_API_KEY = "your_actual_key"`
4. Save

### Step 3: Deploy

1. Upload to GitHub
2. Deploy on Streamlit Cloud
3. Wait 2-3 minutes
4. Dashboard loads with live data!

---

## 📊 What You Get (Dynamic)

### From Alpha Vantage API:
- **Revenue** - Total annual revenue
- **EBITDA** - Operating earnings
- **PBT** - Profit before tax
- **PAT** - Net income
- **Free Cash Flow** - Operating cash minus capex
- **Gross Margin** - Calculated automatically
- **Operating Margin** - Calculated automatically
- **Fiscal Period** - Exact reporting date

### Manual Data (You Update):
- Store counts
- Same-store sales
- Geographic mix

---

## ⚙️ How It Works

### API Rate Limits:
- **25 calls per day** (free tier)
- **5 calls per minute** max
- **5 companies × 2 calls each** = 10 calls total
- **Dashboard caches for 24 hours** (data doesn't change daily)

### Smart Features:
- **Automatic 12-second delays** between API calls (respects rate limit)
- **24-hour caching** (reduces API usage)
- **Progress bar** shows fetching status
- **Automatic fallback** to manual data if API fails
- **Debug mode** to see what's happening

---

## 🏢 Companies Tracked

1. **LVMH** (MC.PA) - EUR
2. **Hermès** (RMS.PA) - EUR
3. **Richemont** (CFR.SW) - CHF
4. **Watches of Switzerland** (WOSG.L) - GBP
5. **The Hour Glass** (AGS.SI) - SGD

---

## ⏱️ First Load Time

**Important:** First time you open the dashboard:
- Takes **~2 minutes** to load
- This is normal! Alpha Vantage has 5 calls/min limit
- Dashboard waits 12 seconds between each company
- Progress bar shows status
- **After first load:** Instant (cached for 24 hours)

---

## 🔧 Updating Manual Data

When quarterly reports come out:

Edit `app.py` lines 28-120 (COMPANIES section):

```python
"LVMH": {
    "manual": {
        "Revenue": 86153000000,  # Update this
        "EBITDA": 24463000000,   # Update this
        # etc...
    }
}
```

Commit → Auto-deploys in 2 minutes

---

## 🎯 Testing Your API Key

Before deploying, test in browser:

```
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=YOUR_KEY
```

**Should see:**
- JSON with IBM stock data
- NO errors

---

## 💡 Tips

### Daily Usage:
- Open dashboard once per day
- Data loads in 2 minutes first time
- Rest of day: instant load (cached)

### API Limit Reached?
- Dashboard automatically uses manual data
- No errors shown
- Just says "Using manual fallback"

### Want Real-Time?
- Upgrade to Premium ($49.99/month)
- 1,200 calls/day
- Faster rate limits

---

## 🐛 Troubleshooting

### "❌ Not Configured"
**Fix:** Add API key at line 21

### "⚠️ Invalid API key"
**Fix:** 
- Copy key again from Alpha Vantage email
- No extra spaces
- Keep the quotes

### "⚠️ Rate limit"
**Fix:**
- Wait 24 hours (resets daily)
- Or use "Manual Data Only" in sidebar

### Dashboard loads but shows N/A
**Normal:** Alpha Vantage may not have complete data for all stocks
- European stocks (LVMH, Hermès) sometimes limited
- Dashboard shows what's available
- Falls back to manual data automatically

---

## 📈 API vs Manual Data

### Use API When:
- You want latest annual reports
- Companies filed recently
- You need exact fiscal dates

### Use Manual When:
- API limit reached
- Need quarterly data (API only shows annual)
- Want operational metrics

**Best:** Use both! API for financials, manual for operational.

---

## 📦 Files

```
luxury-retail-dashboard/
├── app.py              # Main dashboard
├── requirements.txt    # Dependencies
├── runtime.txt        # Python version
├── .streamlit/config.toml
└── README.md
```

---

## ✅ Why This Works When FMP Didn't

| Feature | FMP (Failed) | Alpha Vantage (Works) |
|---------|--------------|----------------------|
| Free tier | Restricted | Actually free |
| New accounts | Legacy error | All features |
| API versions | v3/v4 confusion | One simple API |
| Rate limit | Unclear | Clear (25/day) |
| Reliability | Changed often | Stable since 2017 |

---

**Alpha Vantage has been reliable and free since 2017. No surprises!**
