# Kiambu Dairy Co-op Payment Calculator

A simple Python program to calculate daily payments for dairy farmers based on litres supplied and the co-op buying price.

### Features
- Calculates total payment: `Litres × Price per litre`
- Validates farmer names (no numbers, no empty names, allows spaces, hyphen, apostrophe)
- Validates litres (must be a number > 0)
- Remembers buying price using `price.txt` — price stays even after closing the program
- Easy price update — type `admin` as farmer name

### Files






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