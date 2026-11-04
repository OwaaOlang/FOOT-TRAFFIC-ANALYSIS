"""
Dairy Co-op Payment Calculator
-------------------------------
Farmer enters their name and litres supplied.
Tool shows total owed at current buying price.

Usage:
    python dairy_calculator.py

Config:
    Edit current_price in the script to update the weekly rate.
    Future version: read from price.txt
"""

def get_current_price():
    """Read price from price.txt, create it if missing."""
    try:
        with open("price.txt", "r") as f:
            content = f.read().strip()
            if not content:
                return 55.0
            return float(content)
    except (FileNotFoundError, ValueError):
        # if file missing or has bad text, use default
        return 55.0

def set_price(new_price):
    """Save new price to price.txt"""
    with open("price.txt", "w") as f:
        f.write(str(new_price))

def is_valid_name(name):
    """Check farmer name"""
    name = name.strip()
    if not name:
        return False, "Name is required."
    if len(name) < 2:
        return False, "Name too short."
    # allow letters, space, hyphen, apostrophe only
    for char in name:
        if not (char.isalpha() or char in " -'"):
            return False, "Name should have only letters."
    return True, "OK"

def calculate_payment(litres, price_per_litre):
    return litres * price_per_litre

def run():
    print("Kiambu Dairy Co-op Payment Calculator")
    print("--------------------------------------")
    
    price = get_current_price()
    print(f"Current buying price: KES {price:.2f} per litre")
    print()

    # --- Admin shortcut to update price ---
    # If you type 'admin' as name, it lets you update price
    name = input("Farmer name: ").strip()
    
    if name.lower() == "admin":
        try:
            new = float(input("Enter new buying price: "))
            if new <= 0:
                print("Price must be greater than zero.")
                return
            set_price(new)
            print(f"Price updated to KES {new:.2f}")
            print("Run the program again for farmers.")
        except ValueError:
            print("Please enter a valid number for price.")
        return

    # --- Normal farmer flow with name check ---
    valid, msg = is_valid_name(name)
    if not valid:
        print(msg)
        return

    # --- Litres with validation and retry ---
    try:
        litres = float(input("Litres supplied today: "))
        if litres <= 0:
            print("Litres must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number for litres.")
        return

    total = calculate_payment(litres, price)

    print()
    print(f"Farmer : {name}")
    print(f"Litres : {litres}")
    print(f"Price : KES {price:.2f}/litre")
    print(f"Total : KES {total:.2f}")

if __name__ == "__main__":
    run()