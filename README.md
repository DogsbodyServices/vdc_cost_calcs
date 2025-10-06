# VDC Cost Calculator

A simple Python CLI tool for calculating monthly and hourly costs for virtual data centre (VDC) compute, storage, and SQL Server licensing, based on a CSV pricing file.

## Features

- Lists all available Compute and Storage SKUs with descriptions and prices from your CSV.
- Interactive CLI selection for compute, storage, and (optionally) SQL Server licensing.
- Correct SQL Server licensing calculation: per month, per 2 vCPUs, rounded up.
- Output subtotals for Compute, Storage, and SQL, plus a grand total.

## Usage

1. Place your `vdc_costs.csv` file in the same directory as the script.  
2. Run the calculator:

    ```bash
    python cost_calculator.py
    ```

3. Follow the prompts to select SKUs, quantities, hours, and licensing.

## Example

```
Available Compute SKUs:
GP4 v1: General Purpose (6 vCPU, 24 GB RAM) (£0.2603/hr)
...

Enter Compute SKU: GP4 v1
Enter Compute quantity: 2
Enter Compute hours: 100

Available Storage SKUs:
PERFSTOR: Performance Storage -1 GB (£0.0002/hr)
...

Enter Storage SKU: PERFSTOR
Enter Storage quantity (in GB): 500
Enter Storage hours: 100

Do you need SQL Server licensing? (y/n): y
Available SQL Server SKUs:
SQL-STD: Microsoft SQL Server Standard Core 2 Licence - Corporate (£169.91/month)
...

Enter SQL Server SKU: SQL-STD

----- COST SUMMARY -----
Compute subtotal: £52.06
Storage subtotal: £10.00
SQL subtotal: £679.64 per month
SQL line: Microsoft SQL Server Standard Core 2 Licence - Corporate x 4: £679.64 per month
GRAND TOTAL: £741.70
```

## License

MIT
