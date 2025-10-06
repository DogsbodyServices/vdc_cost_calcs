import csv
import math

def load_pricing(filename):
    pricing_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pricing_data.append(row)
    return pricing_data

def list_skus(pricing_data, category, family=None):
    sku_list = []
    for item in pricing_data:
        if item['Invoice Category'] and category in item['Invoice Category'] and item['SKU ']:
            if family is None or (item['Family'] and family in item['Family']):
                sku_list.append((item['SKU '], item['SKU Description'], item['Unit Price']))
    return sku_list

def find_sku(pricing_data, sku):
    for item in pricing_data:
        if item['SKU '] == sku:
            return item
    return None

def calculate_cost(unit_price, quantity, hours=1):
    price = float(unit_price.replace('£', ''))
    return price * quantity * hours

def main():
    pricing_data = load_pricing('vdc_costs.csv')

    # Compute Section
    print("\nAvailable Compute SKUs:")
    compute_skus = list_skus(pricing_data, "Compute")
    for sku, desc, price in compute_skus:
        print(f"{sku}: {desc} ({price}/hr)")
    compute_sku = input("\nEnter Compute SKU: ").strip()
    compute_item = find_sku(pricing_data, compute_sku)
    if compute_item:
        compute_qty = int(input("Enter Compute quantity: "))
        compute_hours = float(input("Enter Compute hours: "))
        compute_total = calculate_cost(compute_item['Unit Price'], compute_qty, compute_hours)
        # Get vCPU count for SQL licensing calculation
        try:
            vcpus = int(compute_item['CPU'])
        except (KeyError, ValueError):
            vcpus = 0
        print(f"Compute cost: £{compute_total:.2f}")
    else:
        compute_total = 0.0
        vcpus = 0
        compute_qty = 0
        compute_hours = 0
        print("Compute SKU not found.")

    # Storage Section
    print("\nAvailable Storage SKUs:")
    storage_skus = list_skus(pricing_data, "Storage")
    for sku, desc, price in storage_skus:
        print(f"{sku}: {desc} ({price}/hr)")
    storage_sku = input("\nEnter Storage SKU: ").strip()
    storage_item = find_sku(pricing_data, storage_sku)
    if storage_item:
        storage_qty = int(input("Enter Storage quantity (in GB): "))
        storage_hours = float(input("Enter Storage hours: "))
        storage_total = calculate_cost(storage_item['Unit Price'], storage_qty, storage_hours)
        print(f"Storage cost: £{storage_total:.2f}")
    else:
        storage_total = 0.0
        print("Storage SKU not found.")

    # SQL Licensing Section (Monthly per 2 vCPUs, NOT hourly)
    sql_total = 0.0
    sql_line = ""
    sql_needed = input("\nDo you need SQL Server licensing? (y/n): ").strip().lower()
    if sql_needed == "y":
        sql_skus = list_skus(pricing_data, "Licence", "SQL Server")
        if not sql_skus:
            print("No SQL Server SKUs found in the CSV.")
        else:
            print("\nAvailable SQL Server SKUs:")
            for sku, desc, price in sql_skus:
                print(f"{sku}: {desc} ({price}/month)")
            sql_sku = input("\nEnter SQL Server SKU: ").strip()
            sql_item = find_sku(pricing_data, sql_sku)
            if sql_item and vcpus > 0:
                # Number of licences = ceil(vcpus / 2) * compute_qty
                sql_licence_qty = math.ceil(vcpus / 2) * compute_qty
                sql_total = float(sql_item['Unit Price'].replace('£', '')) * sql_licence_qty
                sql_line = f"{sql_item['SKU Description']} x {sql_licence_qty}: £{sql_total:.2f} per month"
                print(f"SQL cost: £{sql_total:.2f} per month")
            else:
                print("No valid SQL SKU or vCPU info; skipping SQL licensing.")
    else:
        sql_total = 0.0

    print("\n----- COST SUMMARY -----")
    print(f"Compute subtotal: £{compute_total:.2f}")
    print(f"Storage subtotal: £{storage_total:.2f}")
    if sql_total:
        print(f"SQL subtotal: £{sql_total:.2f} per month")
        print(f"SQL line: {sql_line}")
    print(f"GRAND TOTAL: £{compute_total + storage_total + sql_total:.2f}")

if __name__ == "__main__":
    main()
