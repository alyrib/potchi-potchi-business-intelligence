"""Fact table generators for the Potchi Potchi project."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import (
    END_DATE,
    EXPENSE_COUNT,
    PURCHASE_LINE_COUNT,
    RANDOM_SEED,
    START_DATE,
)


EXCHANGE_RATES_TO_GBP = {
    "GBP": 1.0000,
    "EUR": 0.8600,
    "USD": 0.7900,
    "CNY": 0.1100,
    "JPY": 0.0054,
    "KRW": 0.00058,
}


def _generate_purchase_dates(
    rng: np.random.Generator,
    count: int,
) -> pd.DatetimeIndex:
    """Generate purchase dates with stronger restocking before peak seasons."""

    dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="D",
    )

    month_weights = {
        1: 0.85,
        2: 0.90,
        3: 0.95,
        4: 1.00,
        5: 1.00,
        6: 0.90,
        7: 0.85,
        8: 1.00,
        9: 1.20,
        10: 1.45,
        11: 1.35,
        12: 0.75,
    }

    weights = np.array(
        [month_weights[date.month] for date in dates],
        dtype=float,
    )

    # The business grows during its second year.
    weights *= np.where(dates.year == 2025, 1.45, 1.00)
    weights /= weights.sum()

    selected_dates = rng.choice(
        dates.to_numpy(),
        size=count,
        replace=True,
        p=weights,
    )

    return pd.DatetimeIndex(selected_dates).sort_values()


def _calculate_base_unit_cost(
    rng: np.random.Generator,
    subcategory: str,
    msrp: float,
) -> float:
    """Calculate a plausible wholesale cost in GBP."""

    cost_ratio_ranges = {
        "Blind Box": (0.43, 0.57),
        "Figure": (0.48, 0.62),
        "Plush": (0.42, 0.58),
    }

    minimum_ratio, maximum_ratio = cost_ratio_ranges[subcategory]
    ratio = rng.uniform(minimum_ratio, maximum_ratio)

    return round(msrp * ratio, 2)


def _calculate_allocated_costs(
    rng: np.random.Generator,
    country: str,
    shipping_method: str,
) -> tuple[float, float, float | None]:
    """Generate freight, import duty and other landed costs per unit."""

    if country == "United Kingdom":
        freight = rng.uniform(0.20, 0.60)
        import_duty = 0.00
    elif shipping_method == "Road Freight":
        freight = rng.uniform(0.45, 1.10)
        import_duty = rng.uniform(0.05, 0.30)
    elif shipping_method == "Sea Freight":
        freight = rng.uniform(0.60, 1.40)
        import_duty = rng.uniform(0.35, 1.10)
    else:
        freight = rng.uniform(1.00, 2.60)
        import_duty = rng.uniform(0.40, 1.50)

    other_cost = (
        round(rng.uniform(0.05, 0.45), 2)
        if rng.random() < 0.18
        else None
    )

    return (
        round(freight, 2),
        round(import_duty, 2),
        other_cost,
    )


def _determine_purchase_status(
    rng: np.random.Generator,
    purchase_date: pd.Timestamp,
) -> str:
    """Assign a plausible purchase status based on transaction date."""

    reporting_end = pd.Timestamp(END_DATE)
    days_before_end = (reporting_end - purchase_date).days

    if days_before_end <= 30:
        return rng.choice(
            [
                "Received",
                "Partially Received",
                "In Transit",
                "Ordered",
                "Cancelled",
            ],
            p=[0.45, 0.15, 0.20, 0.15, 0.05],
        )

    return rng.choice(
        [
            "Received",
            "Partially Received",
            "Cancelled",
        ],
        p=[0.91, 0.07, 0.02],
    )


def generate_fact_purchases(
    product_df: pd.DataFrame,
    supplier_df: pd.DataFrame,
) -> pd.DataFrame:
    """Generate historical supplier purchase transactions."""

    rng = np.random.default_rng(RANDOM_SEED + 100)

    supplier_lookup = supplier_df.set_index("SupplierID").to_dict("index")

    purchase_dates = _generate_purchase_dates(
        rng=rng,
        count=PURCHASE_LINE_COUNT,
    )

    rows: list[dict[str, object]] = []
    purchase_line_id = 300001
    purchase_order_number = 1

    while len(rows) < PURCHASE_LINE_COUNT:
        purchase_date = purchase_dates[len(rows)]

        supplier_id = int(
            rng.choice(product_df["SupplierID"].unique())
        )

        supplier_products = product_df.loc[
            product_df["SupplierID"] == supplier_id
        ]

        supplier = supplier_lookup[supplier_id]

        remaining_lines = PURCHASE_LINE_COUNT - len(rows)
        line_count = min(
            int(rng.integers(1, 6)),
            len(supplier_products),
            remaining_lines,
        )

        selected_products = supplier_products.sample(
            n=line_count,
            replace=False,
            random_state=int(rng.integers(0, 1_000_000)),
        )

        purchase_order_id = (
            f"PO-{purchase_date.year}-{purchase_order_number:04d}"
        )

        purchase_status = _determine_purchase_status(
            rng=rng,
            purchase_date=purchase_date,
        )

        currency_code = supplier["CurrencyCode"]
        base_exchange_rate = EXCHANGE_RATES_TO_GBP[currency_code]

        exchange_rate = round(
            base_exchange_rate * rng.uniform(0.96, 1.04),
            6,
        )

        for _, product in selected_products.iterrows():
            minimum_order_quantity = int(
                supplier["MinimumOrderQuantity"]
            )

            quantity_multiplier = int(rng.integers(1, 5))
            quantity_purchased = (
                minimum_order_quantity * quantity_multiplier
            )

            if purchase_status == "Received":
                received_quantity = quantity_purchased
            elif purchase_status == "Partially Received":
                shortage = int(
                    rng.integers(
                        1,
                        max(2, round(quantity_purchased * 0.15)),
                    )
                )
                received_quantity = quantity_purchased - shortage
            else:
                received_quantity = 0

            unit_cost_gbp = _calculate_base_unit_cost(
                rng=rng,
                subcategory=product["SubCategory"],
                msrp=float(product["MSRP"]),
            )

            unit_cost_original_currency = round(
                unit_cost_gbp / exchange_rate,
                2,
            )

            (
                allocated_freight_cost,
                import_duty_allocated,
                other_landed_cost_allocated,
            ) = _calculate_allocated_costs(
                rng=rng,
                country=supplier["Country"],
                shipping_method=supplier[
                    "PrimaryShippingMethod"
                ],
            )

            rows.append(
                {
                    "PurchaseLineID": purchase_line_id,
                    "PurchaseOrderID": purchase_order_id,
                    "PurchaseDateKey": int(
                        purchase_date.strftime("%Y%m%d")
                    ),
                    "SupplierID": supplier_id,
                    "ProductID": int(product["ProductID"]),
                    "QuantityPurchased": quantity_purchased,
                    "ReceivedQuantity": received_quantity,
                    "UnitCostOriginalCurrency": (
                        unit_cost_original_currency
                    ),
                    "CurrencyCode": currency_code,
                    "ExchangeRateToGBPAtPurchase": exchange_rate,
                    "UnitCostGBP": unit_cost_gbp,
                    "AllocatedFreightCost": (
                        allocated_freight_cost
                    ),
                    "ImportDutyAllocated": (
                        import_duty_allocated
                    ),
                    "OtherLandedCostAllocated": (
                        other_landed_cost_allocated
                    ),
                    "PurchaseStatus": purchase_status,
                }
            )

            purchase_line_id += 1

        purchase_order_number += 1

    return pd.DataFrame(rows)


def generate_fact_expenses(
    vendor_df: pd.DataFrame,
    expense_category_df: pd.DataFrame,
) -> pd.DataFrame:
    """Generate synthetic non-inventory operating expense transactions."""

    rng = np.random.default_rng(RANDOM_SEED + 300)

    vendor_lookup = vendor_df.set_index("VendorID").to_dict("index")
    category_lookup = expense_category_df.set_index(
        "ExpenseCategoryID"
    ).to_dict("index")

    category_vendor_map = {
        "Marketing": [2, 3],
        "Software": [4, 5, 10, 12],
        "Website and Domain": [1, 13],
        "Storage": [6],
        "Packaging": [8],
        "Accounting": [10, 15],
        "Insurance": [9],
        "Utilities": [14],
        "Professional Services": [11, 15],
    }

    amount_ranges_gbp = {
        "Marketing": (40.00, 650.00),
        "Software": (10.00, 95.00),
        "Website and Domain": (8.00, 240.00),
        "Storage": (120.00, 260.00),
        "Packaging": (35.00, 420.00),
        "Accounting": (35.00, 300.00),
        "Insurance": (25.00, 180.00),
        "Utilities": (20.00, 140.00),
        "Professional Services": (60.00, 750.00),
    }

    payment_methods = [
        "Business Debit Card",
        "Business Credit Card",
        "Bank Transfer",
        "PayPal",
        "Direct Debit",
    ]

    all_dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="D",
    )

    category_ids = expense_category_df[
        "ExpenseCategoryID"
    ].to_numpy()

    category_weights = np.array(
        [0.20, 0.16, 0.08, 0.10, 0.18, 0.07, 0.05, 0.07, 0.09],
        dtype=float,
    )

    rows: list[dict[str, object]] = []

    for expense_id in range(100001, 100001 + EXPENSE_COUNT):
        expense_category_id = int(
            rng.choice(category_ids, p=category_weights)
        )

        category = category_lookup[expense_category_id]
        category_name = category["ExpenseCategoryName"]

        vendor_id = int(
            rng.choice(category_vendor_map[category_name])
        )
        vendor = vendor_lookup[vendor_id]

        expense_date = pd.Timestamp(rng.choice(all_dates))

        minimum_amount, maximum_amount = amount_ranges_gbp[
            category_name
        ]

        expense_amount_gbp = round(
            rng.uniform(minimum_amount, maximum_amount),
            2,
        )

        currency_code = vendor["DefaultCurrencyCode"]

        exchange_rates = {
            "GBP": 1.0000,
            "EUR": 0.8600,
            "USD": 0.7900,
        }

        exchange_rate = exchange_rates[currency_code]

        expense_amount_original_currency = round(
            expense_amount_gbp / exchange_rate,
            2,
        )

        if expense_date > pd.Timestamp(END_DATE) - pd.Timedelta(
            days=20
        ):
            expense_status = rng.choice(
                ["Planned", "Approved", "Paid", "Cancelled"],
                p=[0.15, 0.20, 0.60, 0.05],
            )
        else:
            expense_status = rng.choice(
                ["Paid", "Cancelled"],
                p=[0.97, 0.03],
            )

        rows.append(
            {
                "ExpenseID": expense_id,
                "ExpenseDateKey": int(
                    expense_date.strftime("%Y%m%d")
                ),
                "ExpenseCategoryID": expense_category_id,
                "VendorID": vendor_id,
                "ExpenseDescription": (
                    f"{category_name} expense - "
                    f"{vendor['VendorName']}"
                ),
                "ExpenseAmountOriginalCurrency": (
                    expense_amount_original_currency
                ),
                "CurrencyCode": currency_code,
                "ExchangeRateToGBPAtPayment": exchange_rate,
                "ExpenseAmountGBP": expense_amount_gbp,
                "PaymentMethod": rng.choice(payment_methods),
                "ExpenseStatus": expense_status,
            }
        )

    return pd.DataFrame(rows).sort_values(
        by=["ExpenseDateKey", "ExpenseID"]
    ).reset_index(drop=True)