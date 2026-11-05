import pandas as pd

august = pd.read_csv("sales_august.csv")
september = pd.read_csv("sales_september.csv")

# Step 1: Rename columns to a standard format
august = august.rename(columns={
    "client_name": "customer",
    "county": "region",
    "qty": "quantity",
    "unit_price": "price"
})

september = september.rename(columns={
    "customer_name": "customer"
})

# Step 2: Add a month column so you know which rows came from where
august["month"] = "August"
september["month"] = "September"

#step 3: Stack the two months into one combined dataset
combined = pd.concat([august, september], ignore_index=True)
print(f"Combined: {len(combined)} rows")

#verify the combined dataset looks right
print(combined.groupby("month")["quantity"].sum())

#step 4: Check data types match
print(august["price"].dtype)
print(september["price"].dtype)


print("Combined columns:", combined.columns.tolist())
print(f"Total rows: {len(combined)} rows")
print(combined.head())

combined.to_csv("dairy_sales_aug_sep_2025.csv", index=False)

#create total revenue per row
combined['total']= combined['quantity'] * combined['price']

#Groupby: split by month, then sum
print(combined.groupby('month')['total'].sum())

#why did september drop #Ghee dropped
print(combined.groupby(['month','product'])['total'].sum())

#Did ghee dropped because we sold fewer tins or price dropped
print(combined.groupby(['month', 'product'])['quantity'].sum())


print(combined.groupby(['month', 'product'])['price'].mean())

print(combined[combined['product'] =='Ghee'].groupby(['month', 'region'])['price'].mean())

print(combined[combined['product'] =='Ghee'].groupby(['month', 'region'])['quantity'].sum())



# Step 4: Which customers grew vs shrank between August and September?

# 1. Total revenue per customer per month
monthly_revenue = combined.groupby(["month", "customer"])["total"].sum().reset_index()

# 2. Pivot so August and September become columns
pivot = monthly_revenue.pivot(index="customer", columns="month", values="total").fillna(0)

# 3. Calculate growth
pivot["growth"] = pivot["September"] - pivot["August"]
pivot["pct_change"] = ((pivot["September"] - pivot["August"]) / pivot["August"] * 100).round(1)

# 4. Top 5 growers
print("--- Top 5 Growing Customers ---")
print(pivot.sort_values("pct_change", ascending=False).head(5))

# 5. Top 5 shrinkers - the ones who hurt us most
print("\n--- Top 5 Shrinking Customers ---")
print(pivot.sort_values("pct_change", ascending=True).head(5))

#what did Mukasa Dairy stopped buying
mukasa = combined[combined['customer'] == 'Mukasa Dairy']
print(mukasa.groupby(['month', 'product'])['total'].sum())
print(mukasa.groupby(['month', 'product'])['price'].mean().round(0))
