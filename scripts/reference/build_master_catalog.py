"""Builds the master product catalogue CSV."""

from pathlib import Path

import pandas as pd

from .catalog import ALL_PRODUCTS, CATALOG_COLUMNS


def main() -> None:
    """Generate the master product catalogue."""

    df = pd.DataFrame(ALL_PRODUCTS)

    df = df[CATALOG_COLUMNS]

    project_root = Path(__file__).resolve().parents[2]

    output_path = (
        project_root
        / "data"
        / "reference"
        / "master_product_catalog.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_path,
        index=False,
    )

    print("=" * 60)
    print("Master Product Catalogue")
    print("=" * 60)

    print(df)

    print()

    print(f"Products: {len(df)}")

    print(f"Saved to:\n{output_path}")


if __name__ == "__main__":
    main()