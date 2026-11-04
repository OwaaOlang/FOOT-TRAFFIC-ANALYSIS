import requests

try:
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Let user choose
        currency = input("Enter code (UGX, SSP, KES, TZS, etc): ").upper()
        
        if currency in data['rates']:
            rate = data['rates'][currency]
            print(f"Live Rate: 1 USD = {rate} {currency}")
            
            for amount in [10000, 50000, 100000]:
                usd_value = amount / rate
                print(f"{currency} {amount:,} = USD {usd_value:.2f}")
        else:
            print(f"Code {currency} not found")

except Exception as e:
    print(f"Error: {e}")
