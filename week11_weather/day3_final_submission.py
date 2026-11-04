"""
TRAVEL WEATHER TOOL - AI Masterclass Day 3
How to run:
1. pip install requests python-dotenv
2. Create .env file with OPENWEATHER_API_KEY=your_key
3. python week11/day3_travel_info.py
4. Enter any city/district e.g. Mbarara, Gulu, Kampala, Nairobi, London

What it does:
- Takes user input (city name) - not hardcoded
- Makes 3 API calls: OpenWeather Current + OpenWeather Forecast + World Bank Country Info
- Combines results into one readable report + saves to JSON
"""

import os
import json
import requests
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime

load_dotenv()

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Weather API Error: {r.status_code} - City not found")
            return None
    except Exception as e:
        print(f"Error connecting to weather API: {e}")
        return None

def get_forecast(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def get_country_info(code):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        url = f"https://api.worldbank.org/v2/country/{code}?format=json"
        r = requests.get(url, headers=headers, timeout=15)
        j = r.json()
        if len(j) > 1 and j[1]:
            info = j[1][0]
            return {
                "name": info.get("name"),
                "region": info.get("region", {}).get("value"),
                "capital": info.get("capitalCity"),
                "income": info.get("incomeLevel", {}).get("value")
            }
    except Exception as e:
        print(f"Country API Error (handled gracefully): {e}")
    return None

def run_tool():
    print("=== Travel Weather Tool ===")
    city = input("Enter city/district: ").strip()
    
    # Error handling 1: Empty input
    if not city:
        print("Error: You must enter a city name. Using Kampala as default.")
        city = "Kampala"

    weather = get_weather(city)
    
    # Error handling 2: City not found (graceful)
    if not weather:
        print(f"\nCould not find '{city}'. Please check spelling and try again.")
        print("Examples: Kampala, Mbarara, Gulu, Nairobi, London")
        return

    country_code = weather["sys"]["country"]
    country = get_country_info(country_code)
    forecast = get_forecast(city)

    # Clean readable output for non-technical user
    print(f"\n--- CURRENT WEATHER in {city.title()}, {country_code} ---")
    print(f"Temperature: {weather['main']['temp']}C (feels like {weather['main']['feels_like']}C)")
    print(f"Condition: {weather['weather'][0]['description'].title()}")
    print(f"Humidity: {weather['main']['humidity']}% | Wind: {weather['wind']['speed']} m/s")

    if country:
        print(f"\n--- ABOUT {country_code} ---")
        print(f"Country: {country['name']}")
        print(f"Region: {country['region']}")
        print(f"Capital: {country['capital']}")

    if forecast:
        print(f"\n--- 5-DAY PREDICTION for {city.title()} ---")
        daily = defaultdict(list)
        for item in forecast["list"]:
            day = datetime.fromtimestamp(item["dt"]).strftime("%a %d Oct")
            daily[day].append(item)
        for day, items in list(daily.items())[:5]:
            temps = [i["main"]["temp"] for i in items]
            cond = items[len(items)//2]["weather"][0]["description"].title()
            print(f"{day}: {min(temps):.0f}C - {max(temps):.0f}C | {cond}")

    # Save to JSON file (requirement)
    output = {
        "city": city,
        "current_weather": weather,
        "forecast": forecast,
        "country_info": country
    }
    filename = f"{city.lower()}_weather_report.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nReport saved to {filename} ✅")

run_tool()