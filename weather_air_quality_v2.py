import requests
from datetime import datetime

API_KEY = "fde104393d9a1b3a4945b58f5dfa7336"

# ---------- HELPERS ----------

def format_hour(dt_txt):
    # "2026-11-07 07:00:00" -> "7am"
    dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
    hour = dt.strftime("%I").lstrip("0")
    ampm = dt.strftime("%p").lower()
    return f"{hour}{ampm}"

def aqi_text(aqi):
    return {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}.get(aqi, "Unknown")

# ---------- 1. CURRENT WEATHER ----------

def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()
    if response.status_code != 200:
        print(f"Error: {data.get('message', 'City not found')}")
        return None
    return data

# ---------- 2. FORECAST (Hourly-style) ----------

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()
    if response.status_code != 200:
        return None
    return data

def show_hourly_today(forecast_data):
    print("\n=== Today - Hour by Hour ===")
    print(f"{'Time':<6} {'Temp':<8} {'Feels':<8} {'Rain %':<8} {'Sky'}")
    print("-" * 45)

    today = datetime.now().strftime("%Y-%m-%d")
    now_hour = datetime.now().hour

    for item in forecast_data["list"]:
        dt_txt = item["dt_txt"]
        if not dt_txt.startswith(today):
            continue
        hour_num = int(dt_txt[11:13])
        if hour_num < now_hour:
            continue

        temp = item["main"]["temp"]
        feels = item["main"]["feels_like"]
        rain = int(item.get("pop", 0) * 100)
        sky = item["weather"][0]["description"].title()
        marker = " <- now" if hour_num == now_hour else ""
        print(f"{format_hour(dt_txt):<6} {temp:<8.1f} {feels:<8.1f} {rain}%{'':<4} {sky}{marker}")

def show_5day_forecast(forecast_data):
    print("\n=== 5-Day Forecast ===")
    print(f"{'Date':<12} {'High':<8} {'Low':<8} {'Sky'}")
    print("-" * 40)

    daily = {} # date -> [high, low, sky]
    for item in forecast_data["list"]:
        date = item["dt_txt"][:10]
        hi = item["main"]["temp_max"]
        lo = item["main"]["temp_min"]
        sky = item["weather"][0]["description"].title()

        if date not in daily:
            daily[date] = [hi, lo, sky]
        else:
            daily[date][0] = max(daily[date][0], hi) # true max
            daily[date][1] = min(daily[date][1], lo) # true min

    for date, (hi, lo, sky) in daily.items():
        print(f"{date:<12} {hi:<8.1f} {lo:<8.1f} {sky}")

# ---------- 3. AIR QUALITY ----------

def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()

def show_air_quality(lat, lon):
    data = get_air_quality(lat, lon)
    if not data:
        print("\n=== Air Quality ===\nNot available")
        return
    item = data["list"][0]
    aqi = item["main"]["aqi"]
    comp = item["components"]
    print("\n=== Air Quality ===")
    print(f"AQI: {aqi} ({aqi_text(aqi)})")
    print(f"PM2.5: {comp['pm2_5']} | PM10: {comp['pm10']} | CO: {comp['co']} | NO2: {comp['no2']} | O3: {comp['o3']}")

# ---------- 4. COUNTRY INFO (Safe version - never crashes) ----------

def get_country_info(country_code):
    headers = {"User-Agent": "Mozilla/5.0"}
    code = country_code.upper()

    urls_to_try = [
        f"https://restcountries.com/v3.1/alpha/{code}",
        f"https://api.allorigins.win/raw?url=https://restcountries.com/v3.1/alpha/{code}",
    ]
    for url in urls_to_try:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict): # error dict, not list
                    continue
                if isinstance(data, list) and len(data) > 0 and data[0].get("region"):
                    return data[0]
        except Exception:
            continue

    # Fallback: World Bank - never blocked in UG
    try:
        r = requests.get(f"https://api.worldbank.org/v2/country/{code}?format=json", headers=headers, timeout=15)
        j = r.json()
        if len(j) > 1 and j[1]:
            info = j[1][0]
            return {
                "region": info.get("region", {}).get("value", "Unknown"),
                "capital": [info.get("capitalCity", "")],
                "name": {"common": info.get("name", code)},
                "population": 0
            }
    except Exception:
        pass
    return None

def show_country_info(country_code):
    country = get_country_info(country_code)
    if not country:
        print("\n=== Country info ===\nNot available")
        return
    print("\n=== Country info ===")
    print(f"Country : {country['name']['common']}")
    print(f"Region : {country.get('region', 'Unknown')}")
    print(f"Capital : {', '.join(country.get('capital', []))}")

# ---------- MAIN ----------

def main():
    city = input("Enter city (e.g. Kampala): ").strip()
    if not city:
        city = "Kampala"

    current = get_current_weather(city)
    if not current:
        return

    print(f"\n=== Current Weather in {current['name']} ===")
    print(f"Temp: {current['main']['temp']}°C | Feels like: {current['main']['feels_like']}°C")
    print(f"Weather: {current['weather'][0]['description'].title()} | Humidity: {current['main']['humidity']}%")

    lat, lon = current["coord"]["lat"], current["coord"]["lon"]
    country_code = current["sys"]["country"]

    forecast = get_forecast(city)
    if forecast:
        show_hourly_today(forecast)
        show_5day_forecast(forecast)

    show_air_quality(lat, lon)
    show_country_info(country_code)

if __name__ == "__main__":
    main()