"""
Potchi Potchi Synthetic Data Generator.

Entry point for generating all project datasets.
"""

from config import RAW_DATA_DIR
from generators.dimensions import (
    generate_dim_date,
    generate_dim_expense_category,
)


def main() -> None:
    """Generate and export all synthetic datasets."""
    print("=" * 60)
    print("Potchi Potchi Synthetic Data Generator")
    print("=" * 60)

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

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

    print("\nDone!")


if __name__ == "__main__":
    main()