

# Week 12 - Live APIs

## Day 10: Live Exchange Rate Tracker
Built a Python script that fetches live forex rates from open.er-api.com

### Features
- Fetches live USD base rates (160+ currencies)
- Converts KES, UGX, SSP, GHS, ZAR etc to USD
- Error handling for status code & invalid currency codes

### Tech Used
- `requests` library
- `.json()` parsing
- Dictionary access `data['rates'][code]`

### How to Run
pip install requests
python week12/exchange_tracker.py

Example:
Enter code: UGX
Live Rate: 1 USD = 3820 UGX