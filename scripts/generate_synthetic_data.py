"""
Potchi Potchi Synthetic Data Generator.

Entry point for generating all project datasets.
"""

from config import RAW_DATA_DIR
from generators.dimensions import (
    generate_dim_date,
    generate_dim_expense_category,
    generate_dim_product,
    generate_dim_sales_channel,
    generate_dim_supplier,
    generate_dim_vendor,
    generate_dim_customer,
)

from generators.facts import (
    generate_fact_expenses,
    generate_fact_orders_and_sales,
    generate_fact_purchases,
)


def main() -> None:
    """Generate and export all synthetic datasets."""
    print("=" * 60)
    print("Potchi Potchi Synthetic Data Generator")
    print("=" * 60)

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    master_catalog_path = (
    RAW_DATA_DIR.parent
    / "reference"
    / "master_product_catalog.csv"
    )

    print("\nGenerating DimDate...")
    dim_date = generate_dim_date()

    output_path = RAW_DATA_DIR / "DimDate.csv"
    dim_date.to_csv(
        output_path,
        index=False,
        date_format="%Y-%m-%d",
    )

    print(dim_date.head())
    print(f"\nRows generated: {len(dim_date):,}")
    print(f"Saved to: {output_path}")

    print("\nGenerating DimExpenseCategory...")
    dim_expense_category = generate_dim_expense_category()

    expense_category_output_path = (
        RAW_DATA_DIR / "DimExpenseCategory.csv"
    )

    dim_expense_category.to_csv(
        expense_category_output_path,
        index=False,
    )

    print(dim_expense_category)
    print(
        f"\nRows generated: {len(dim_expense_category):,}"
    )
    print(f"Saved to: {expense_category_output_path}")

    print("\nGenerating DimSalesChannel...")
    dim_sales_channel = generate_dim_sales_channel()

    sales_channel_output_path = RAW_DATA_DIR / "DimSalesChannel.csv"

    dim_sales_channel.to_csv(
        sales_channel_output_path,
        index=False,
        date_format="%Y-%m-%d",
    )

    print(dim_sales_channel)
    print(f"\nRows generated: {len(dim_sales_channel):,}")
    print(f"Saved to: {sales_channel_output_path}")

    print("\nGenerating DimSupplier...")
    dim_supplier = generate_dim_supplier()

    supplier_output_path = RAW_DATA_DIR / "DimSupplier.csv"

    dim_supplier.to_csv(
        supplier_output_path,
        index=False,
    )

    print(dim_supplier)
    print(f"\nRows generated: {len(dim_supplier):,}")
    print(f"Saved to: {supplier_output_path}")

    print("\nGenerating DimVendor...")
    dim_vendor = generate_dim_vendor()

    vendor_output_path = RAW_DATA_DIR / "DimVendor.csv"

    dim_vendor.to_csv(
        vendor_output_path,
        index=False,
    )

    print(dim_vendor)
    print(f"\nRows generated: {len(dim_vendor):,}")
    print(f"Saved to: {vendor_output_path}")

    print("\nGenerating DimCustomer...")
    dim_customer = generate_dim_customer()

    customer_output_path = RAW_DATA_DIR / "DimCustomer.csv"

    dim_customer.to_csv(
        customer_output_path,
        index=False,
        date_format="%Y-%m-%d",
    )

    print(dim_customer.head())
    print(f"\nRows generated: {len(dim_customer):,}")
    print(f"Saved to: {customer_output_path}")

    print("\nGenerating DimProduct...")
    dim_product = generate_dim_product(
        master_catalog_path=master_catalog_path,
        supplier_df=dim_supplier,
    )

    product_output_path = RAW_DATA_DIR / "DimProduct.csv"

    dim_product.to_csv(
        product_output_path,
        index=False,
    )

    print(dim_product.head())
    print(f"\nRows generated: {len(dim_product):,}")
    print(f"Saved to: {product_output_path}")

    print("\nGenerating FactPurchases...")
    fact_purchases = generate_fact_purchases(
        product_df=dim_product,
        supplier_df=dim_supplier,
    )

    purchases_output_path = RAW_DATA_DIR / "FactPurchases.csv"

    fact_purchases.to_csv(
        purchases_output_path,
        index=False,
    )

    print(fact_purchases.head())
    print(f"\nRows generated: {len(fact_purchases):,}")
    print(f"Saved to: {purchases_output_path}")

    print("\nGenerating FactExpenses...")
    fact_expenses = generate_fact_expenses(
        vendor_df=dim_vendor,
        expense_category_df=dim_expense_category,
    )

    expenses_output_path = RAW_DATA_DIR / "FactExpenses.csv"

    fact_expenses.to_csv(
        expenses_output_path,
        index=False,
    )

    print(fact_expenses.head())
    print(f"\nRows generated: {len(fact_expenses):,}")
    print(f"Saved to: {expenses_output_path}")

    print("\nGenerating FactOrders and FactSales...")

    fact_orders, fact_sales = generate_fact_orders_and_sales(
        customer_df=dim_customer,
        product_df=dim_product,
        sales_channel_df=dim_sales_channel,
        purchase_df=fact_purchases,
    )

    orders_output_path = RAW_DATA_DIR / "FactOrders.csv"
    sales_output_path = RAW_DATA_DIR / "FactSales.csv"

    fact_orders.to_csv(
        orders_output_path,
        index=False,
    )

    fact_sales.to_csv(
        sales_output_path,
        index=False,
    )

    print(fact_orders.head())
    print(f"\nOrders generated: {len(fact_orders):,}")
    print(f"Saved to: {orders_output_path}")

    print()
    print(fact_sales.head())
    print(f"\nSales lines generated: {len(fact_sales):,}")
    print(f"Saved to: {sales_output_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()