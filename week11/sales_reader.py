import csv

total = 0
top_salesperson = ""
top_amount = 0

with open('sales.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        amount = int(row['amount'])
        total += amount
        
        if amount > top_amount:
            top_amount = amount
            top_salesperson = row['name']

print(f"Total Sales: {total}")
print(f"Top Salesperson: {top_salesperson} with {top_amount}")
