import pandas as pd
import random

random.seed(42)

clients = ["Mama Naki", "Kampala Fresh", "Nansana Mart", "Mukasa Dairy", "Kawempe Shop", "Wakiso Milk Point"]
counties = ["Kampala", "Wakiso", "Mukono", "Mpigi"]
products = ["Fresh Milk", "Yoghurt", "Ghee"]

# AUGUST - 243 rows - old naming
august_data = []
for i in range(243):
    august_data.append({
        'date': f"2025-08-{random.randint(1,31):02d}",
        'client_name': random.choice(clients),
        'county': random.choice(counties),
        'product': random.choice(products),
        'qty': random.randint(5, 100),
        'unit_price': random.choice([2000, 2500, 15000])
    })

august = pd.DataFrame(august_data)
august.to_csv("sales_august.csv", index=False)

# SEPTEMBER - 198 rows - new naming from distributor
september_data = []
for i in range(198):
    september_data.append({
        'date': f"2025-09-{random.randint(1,30):02d}",
        'customer_name': random.choice(clients),
        'region': random.choice(counties),  # same as county, different name
        'product': random.choice(products),
        'quantity': random.randint(5, 100), # same as qty
        'price': random.choice([2000, 2500, 15000]) # same as unit_price
    })

september = pd.DataFrame(september_data)
september.to_csv("sales_september.csv", index=False)

print("Done! Files created")
print(f"August: {len(august)} rows | September: {len(september)} rows")



