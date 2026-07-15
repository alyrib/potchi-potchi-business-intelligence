"""Fact table generators for the Potchi Potchi project."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import (
    END_DATE,
    EXPENSE_COUNT,
    MONTHLY_SEASONALITY,
    ORDER_COUNT,
    PURCHASE_LINE_COUNT,
    RANDOM_SEED,
    START_DATE,
    TARGET_SALES_LINE_COUNT_MAX,
    TARGET_SALES_LINE_COUNT_MIN,
    YEAR_2024_ORDER_SHARE,
    YEAR_2025_ORDER_SHARE,
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


def _generate_order_dates(
    rng: np.random.Generator,
    purchase_df: pd.DataFrame,
) -> pd.DatetimeIndex:
    """Generate chronological order dates with growth and seasonality."""

    received_purchases = purchase_df.loc[
        purchase_df["ReceivedQuantity"] > 0
    ]

    if received_purchases.empty:
        raise ValueError(
            "FactOrders cannot be generated without received inventory."
        )

    first_inventory_date = pd.to_datetime(
        str(received_purchases["PurchaseDateKey"].min()),
        format="%Y%m%d",
    )

    date_range = pd.date_range(
        start=max(pd.Timestamp(START_DATE), first_inventory_date),
        end=END_DATE,
        freq="D",
    )

    weights = np.array(
        [
            MONTHLY_SEASONALITY[date.month]
            * (
                YEAR_2024_ORDER_SHARE
                if date.year == 2024
                else YEAR_2025_ORDER_SHARE
            )
            for date in date_range
        ],
        dtype=float,
    )

    weights /= weights.sum()

    selected_dates = rng.choice(
        date_range.to_numpy(),
        size=ORDER_COUNT,
        replace=True,
        p=weights,
    )

    return pd.DatetimeIndex(selected_dates).sort_values()


def _create_product_performance_weights(
    rng: np.random.Generator,
    product_df: pd.DataFrame,
) -> dict[int, float]:
    """Create internal sales weights without exporting them to DimProduct."""

    performance_categories = rng.choice(
        ["Top Seller", "Standard", "Slow Moving"],
        size=len(product_df),
        p=[0.15, 0.65, 0.20],
    )

    weight_map = {
        "Top Seller": 4.0,
        "Standard": 1.5,
        "Slow Moving": 0.45,
    }

    return {
        int(product_id): weight_map[performance]
        for product_id, performance in zip(
            product_df["ProductID"],
            performance_categories,
        )
    }


def _theme_seasonality_multiplier(
    theme: str,
    order_date: pd.Timestamp,
) -> float:
    """Return a seasonal demand multiplier for a product theme."""

    theme_lower = str(theme).lower()
    month = order_date.month

    if month in (3, 4) and any(
        word in theme_lower
        for word in ["spring", "flower", "garden", "strawberry"]
    ):
        return 2.0

    if month in (6, 7, 8) and any(
        word in theme_lower
        for word in ["ocean", "seafood", "fruit", "travel"]
    ):
        return 1.7

    if month == 10 and any(
        word in theme_lower
        for word in ["magic", "fantasy", "gothic", "masquerade"]
    ):
        return 2.1

    if month in (11, 12) and any(
        word in theme_lower
        for word in [
            "winter",
            "cozy",
            "dessert",
            "bakery",
            "celebration",
            "love",
            "celestial",
        ]
    ):
        return 1.8

    return 1.0


def _product_discount_rate(
    rng: np.random.Generator,
    order_date: pd.Timestamp,
) -> float:
    """Return a plausible product-level promotional discount rate."""

    # Black Friday period
    if (
        order_date.month == 11
        and 20 <= order_date.day <= 30
    ):
        return float(
            rng.choice(
                [0.10, 0.15, 0.20, 0.25],
                p=[0.25, 0.35, 0.30, 0.10],
            )
        )

    # Christmas campaign
    if order_date.month == 12 and order_date.day <= 20:
        return float(
            rng.choice(
                [0.00, 0.05, 0.10, 0.15],
                p=[0.45, 0.25, 0.20, 0.10],
            )
        )

    # Normal trading period
    return float(
        rng.choice(
            [0.00, 0.05, 0.10],
            p=[0.82, 0.13, 0.05],
        )
    )


def _shipping_details(
    rng: np.random.Generator,
    merchandise_total: float,
) -> tuple[str, float, float]:
    """Return shipping method, customer charge and business cost."""

    shipping_method = str(
        rng.choice(
            [
                "Royal Mail Tracked 24",
                "Royal Mail Tracked 48",
                "DPD Next Day",
                "Evri Standard",
            ],
            p=[0.25, 0.45, 0.10, 0.20],
        )
    )

    shipping_cost_ranges = {
        "Royal Mail Tracked 24": (4.20, 5.20),
        "Royal Mail Tracked 48": (3.40, 4.40),
        "DPD Next Day": (6.20, 8.20),
        "Evri Standard": (2.80, 3.80),
    }

    minimum_cost, maximum_cost = shipping_cost_ranges[
        shipping_method
    ]

    shipping_cost = round(
        rng.uniform(minimum_cost, maximum_cost),
        2,
    )

    if merchandise_total >= 45.00:
        shipping_revenue = 0.00
    elif shipping_method == "DPD Next Day":
        shipping_revenue = 6.99
    else:
        shipping_revenue = 3.99

    return (
        shipping_method,
        shipping_revenue,
        shipping_cost,
    )


def generate_fact_orders_and_sales(
    customer_df: pd.DataFrame,
    product_df: pd.DataFrame,
    sales_channel_df: pd.DataFrame,
    purchase_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate coherent FactOrders and FactSales datasets."""

    rng = np.random.default_rng(RANDOM_SEED + 400)

    customers = customer_df.copy()
    customers["RegistrationDate"] = pd.to_datetime(
        customers["RegistrationDate"]
    )

    channels = sales_channel_df.copy()
    channels["LaunchDate"] = pd.to_datetime(
        channels["LaunchDate"]
    )

    products = product_df.copy()
    product_lookup = products.set_index(
        "ProductID"
    ).to_dict("index")

    product_performance_weights = (
        _create_product_performance_weights(
            rng=rng,
            product_df=products,
        )
    )

    purchases = purchase_df.copy()
    purchases["PurchaseDate"] = pd.to_datetime(
        purchases["PurchaseDateKey"].astype(str),
        format="%Y%m%d",
    )

    purchases["OtherLandedCostAllocated"] = (
        purchases["OtherLandedCostAllocated"].fillna(0.00)
    )

    purchases["LandedUnitCost"] = (
        purchases["UnitCostGBP"]
        + purchases["AllocatedFreightCost"]
        + purchases["ImportDutyAllocated"]
        + purchases["OtherLandedCostAllocated"]
    )

    received_purchases = purchases.loc[
        purchases["ReceivedQuantity"] > 0
    ].sort_values(
        by=["PurchaseDate", "PurchaseLineID"]
    )

    purchase_events: dict[
        pd.Timestamp,
        list[dict[str, object]],
    ] = {}

    for _, purchase in received_purchases.iterrows():
        purchase_date = pd.Timestamp(
            purchase["PurchaseDate"]
        )

        purchase_events.setdefault(
            purchase_date,
            [],
        ).append(
            {
                "ProductID": int(purchase["ProductID"]),
                "Quantity": int(
                    purchase["ReceivedQuantity"]
                ),
                "LandedUnitCost": float(
                    purchase["LandedUnitCost"]
                ),
            }
        )

    order_dates = _generate_order_dates(
        rng=rng,
        purchase_df=purchase_df,
    )

    inventory_quantity: dict[int, int] = {
        int(product_id): 0
        for product_id in products["ProductID"]
    }

    inventory_total_cost: dict[int, float] = {
        int(product_id): 0.00
        for product_id in products["ProductID"]
    }

    sorted_purchase_dates = sorted(purchase_events)
    next_purchase_index = 0

    order_rows: list[dict[str, object]] = []
    sales_rows: list[dict[str, object]] = []

    order_id = 500001
    order_item_id = 900001

    payment_methods = [
        "Visa",
        "Mastercard",
        "PayPal",
        "Apple Pay",
        "Google Pay",
    ]

    for order_date in order_dates:
        order_date = pd.Timestamp(order_date)

        # Add all inventory received on or before the order date.
        while (
            next_purchase_index < len(sorted_purchase_dates)
            and sorted_purchase_dates[next_purchase_index]
            <= order_date
        ):
            receipt_date = sorted_purchase_dates[
                next_purchase_index
            ]

            for receipt in purchase_events[receipt_date]:
                product_id = int(receipt["ProductID"])
                received_quantity = int(receipt["Quantity"])
                landed_cost = float(
                    receipt["LandedUnitCost"]
                )

                inventory_quantity[product_id] += (
                    received_quantity
                )
                inventory_total_cost[product_id] += (
                    received_quantity * landed_cost
                )

            next_purchase_index += 1

        eligible_customers = customers.loc[
            customers["RegistrationDate"] <= order_date
        ]

        if eligible_customers.empty:
            continue

        customer = eligible_customers.iloc[
            int(rng.integers(0, len(eligible_customers)))
        ]

        eligible_channels = channels.loc[
            (channels["LaunchDate"] <= order_date)
            & (channels["ChannelStatus"] == "Active")
        ].copy()

        if eligible_channels.empty:
            continue

        channel_weights = []

        for _, channel_row in eligible_channels.iterrows():
            channel_name = channel_row["SalesChannelName"]

            if channel_name == customer["PreferredChannel"]:
                channel_weights.append(2.5)
            elif channel_name == "Website":
                channel_weights.append(1.5)
            else:
                channel_weights.append(1.0)

        channel_weights_array = np.array(
            channel_weights,
            dtype=float,
        )
        channel_weights_array /= channel_weights_array.sum()

        selected_channel_position = int(
            rng.choice(
                len(eligible_channels),
                p=channel_weights_array,
            )
        )

        channel = eligible_channels.iloc[
            selected_channel_position
        ]

        # Small proportion of abandoned/cancelled orders.
        is_cancelled = bool(rng.random() < 0.02)

        desired_line_count = int(
            rng.choice(
                [1, 2, 3, 4],
                p=[0.05, 0.30, 0.40, 0.25],
            )
        )

        order_sales_rows: list[dict[str, object]] = []
        selected_product_ids: set[int] = set()

        if not is_cancelled:
            for _ in range(desired_line_count):
                available_product_ids = [
                    product_id
                    for product_id, quantity
                    in inventory_quantity.items()
                    if quantity > 0
                    and product_id
                    not in selected_product_ids
                ]

                if not available_product_ids:
                    break

                product_weights = []

                for product_id in available_product_ids:
                    product = product_lookup[product_id]

                    weight = product_performance_weights[
                        product_id
                    ]

                    weight *= _theme_seasonality_multiplier(
                        theme=product["Theme"],
                        order_date=order_date,
                    )

                    release_year = product["ReleaseYear"]

                    if (
                        pd.notna(release_year)
                        and int(release_year)
                        > order_date.year
                    ):
                        weight = 0.00

                    product_weights.append(weight)

                weights_array = np.array(
                    product_weights,
                    dtype=float,
                )

                if weights_array.sum() <= 0:
                    break

                weights_array /= weights_array.sum()

                product_id = int(
                    rng.choice(
                        available_product_ids,
                        p=weights_array,
                    )
                )

                selected_product_ids.add(product_id)
                product = product_lookup[product_id]

                maximum_quantity = min(
                    inventory_quantity[product_id],
                    3,
                )

                quantity = int(
                    rng.choice(
                        range(1, maximum_quantity + 1),
                        p=(
                            [1.0]
                            if maximum_quantity == 1
                            else (
                                [0.82, 0.18]
                                if maximum_quantity == 2
                                else [0.78, 0.17, 0.05]
                            )
                        ),
                    )
                )

                average_unit_cost = (
                    inventory_total_cost[product_id]
                    / inventory_quantity[product_id]
                )

                unit_retail_price = round(
                    float(product["MSRP"])
                    * rng.uniform(0.97, 1.05),
                    2,
                )

                discount_rate = _product_discount_rate(
                    rng=rng,
                    order_date=order_date,
                )

                unit_discount_amount = round(
                    unit_retail_price * discount_rate,
                    2,
                )

                net_unit_price = round(
                    unit_retail_price
                    - unit_discount_amount,
                    2,
                )

                line_net_sales = round(
                    quantity * net_unit_price,
                    2,
                )

                platform_fee_amount = round(
                    line_net_sales
                    * float(channel["PlatformFeeRate"]),
                    2,
                )

                # UK catalogue prices are treated as VAT-inclusive.
                vat_amount = round(
                    line_net_sales * (20 / 120),
                    2,
                )

                order_sales_rows.append(
                    {
                        "OrderItemID": order_item_id,
                        "OrderID": order_id,
                        "ProductID": product_id,
                        "Quantity": quantity,
                        "UnitRetailPrice": unit_retail_price,
                        "UnitDiscountAmount": (
                            unit_discount_amount
                        ),
                        "NetUnitPrice": net_unit_price,
                        "UnitCostAtSale": round(
                            average_unit_cost,
                            2,
                        ),
                        "PlatformFeeAmount": (
                            platform_fee_amount
                        ),
                        "VATAmount": vat_amount,
                    }
                )

                inventory_quantity[product_id] -= quantity
                inventory_total_cost[product_id] -= (
                    average_unit_cost * quantity
                )

                inventory_total_cost[product_id] = max(
                    inventory_total_cost[product_id],
                    0.00,
                )

                order_item_id += 1

        if not order_sales_rows and not is_cancelled:
            # No inventory was available for this generated order.
            continue

        merchandise_total = round(
            sum(
                row["Quantity"] * row["NetUnitPrice"]
                for row in order_sales_rows
            ),
            2,
        )

        discount_code = None
        order_discount_amount = 0.00

        if not is_cancelled:
            promotion_roll = rng.random()

            if (
                customer["LoyaltyMember"]
                and promotion_roll < 0.08
            ):
                discount_code = "LOYALTY5"
                order_discount_amount = min(
                    5.00,
                    merchandise_total,
                )
            elif promotion_roll < 0.13:
                discount_code = "WELCOME5"
                order_discount_amount = min(
                    5.00,
                    merchandise_total,
                )
            elif (
                order_date.month == 11
                and 20 <= order_date.day <= 30
                and promotion_roll < 0.25
            ):
                discount_code = "BLACKFRIDAY10"
                order_discount_amount = round(
                    merchandise_total * 0.10,
                    2,
                )

        if is_cancelled:
            order_status = "Cancelled"
            shipped_date = pd.NaT
            delivered_date = pd.NaT
            shipping_method = "Royal Mail Tracked 48"
            shipping_revenue = 0.00
            shipping_cost = 0.00
        else:
            days_before_end = (
                pd.Timestamp(END_DATE) - order_date
            ).days

            if days_before_end <= 2:
                order_status = str(
                    rng.choice(
                        ["Pending", "Processing"],
                        p=[0.35, 0.65],
                    )
                )
                shipped_date = pd.NaT
                delivered_date = pd.NaT
            elif days_before_end <= 6:
                order_status = str(
                    rng.choice(
                        ["Processing", "Shipped", "Delivered"],
                        p=[0.20, 0.55, 0.25],
                    )
                )
            else:
                order_status = str(
                    rng.choice(
                        ["Delivered", "Shipped", "Processing"],
                        p=[0.95, 0.04, 0.01],
                    )
                )

            shipping_method, shipping_revenue, shipping_cost = (
                _shipping_details(
                    rng=rng,
                    merchandise_total=merchandise_total,
                )
            )

            processing_days = int(rng.integers(1, 4))
            delivery_days = int(rng.integers(1, 6))

            if order_status in ("Shipped", "Delivered"):
                shipped_date = (
                    order_date
                    + pd.Timedelta(days=processing_days)
                )
            else:
                shipped_date = pd.NaT

            if order_status == "Delivered":
                delivered_date = (
                    shipped_date
                    + pd.Timedelta(days=delivery_days)
                )
            else:
                delivered_date = pd.NaT

            if (
                pd.notna(shipped_date)
                and shipped_date > pd.Timestamp(END_DATE)
            ):
                shipped_date = pd.NaT
                delivered_date = pd.NaT
                order_status = "Processing"

            if (
                pd.notna(delivered_date)
                and delivered_date > pd.Timestamp(END_DATE)
            ):
                delivered_date = pd.NaT
                order_status = "Shipped"

        order_rows.append(
            {
                "OrderID": order_id,
                "CustomerID": int(customer["CustomerID"]),
                "OrderDateKey": int(
                    order_date.strftime("%Y%m%d")
                ),
                "ShippedDateKey": (
                    int(shipped_date.strftime("%Y%m%d"))
                    if pd.notna(shipped_date)
                    else None
                ),
                "DeliveredDateKey": (
                    int(delivered_date.strftime("%Y%m%d"))
                    if pd.notna(delivered_date)
                    else None
                ),
                "SalesChannelID": int(
                    channel["SalesChannelID"]
                ),
                "OrderStatus": order_status,
                "PaymentMethod": str(
                    rng.choice(payment_methods)
                ),
                "ShippingMethod": shipping_method,
                "DiscountCode": discount_code,
                "OrderDiscountAmount": round(
                    order_discount_amount,
                    2,
                ),
                "ShippingRevenue": shipping_revenue,
                "ShippingCost": shipping_cost,
                "GiftWrapping": bool(
                    not is_cancelled
                    and rng.random() < 0.12
                ),
                "OrderCurrency": "GBP",
            }
        )

        sales_rows.extend(order_sales_rows)
        order_id += 1

    fact_orders = pd.DataFrame(order_rows)
    fact_sales = pd.DataFrame(sales_rows)

    if fact_orders.empty:
        raise ValueError("FactOrders generation produced no records.")

    if fact_sales.empty:
        raise ValueError("FactSales generation produced no records.")

    if not fact_sales["OrderID"].isin(
        fact_orders["OrderID"]
    ).all():
        raise ValueError(
            "FactSales contains OrderID values not found in FactOrders."
        )

    sales_line_count = len(fact_sales)

    if not (
        TARGET_SALES_LINE_COUNT_MIN
        <= sales_line_count
        <= TARGET_SALES_LINE_COUNT_MAX
    ):
        print(
            "\nWarning: FactSales generated "
            f"{sales_line_count:,} rows. "
            "The documented target is "
            f"{TARGET_SALES_LINE_COUNT_MIN:,}–"
            f"{TARGET_SALES_LINE_COUNT_MAX:,}."
        )

    return fact_orders, fact_sales


def generate_fact_inventory_snapshot(
    product_df: pd.DataFrame,
    purchase_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    sales_df: pd.DataFrame,
) -> pd.DataFrame:
    """Generate monthly inventory snapshots from purchases and sales."""

    rng = np.random.default_rng(RANDOM_SEED + 500)

    products = product_df.copy()

    purchases = purchase_df.copy()
    purchases["PurchaseDate"] = pd.to_datetime(
        purchases["PurchaseDateKey"].astype(str),
        format="%Y%m%d",
    )

    purchases["OtherLandedCostAllocated"] = (
        purchases["OtherLandedCostAllocated"].fillna(0.00)
    )

    purchases["LandedUnitCost"] = (
        purchases["UnitCostGBP"]
        + purchases["AllocatedFreightCost"]
        + purchases["ImportDutyAllocated"]
        + purchases["OtherLandedCostAllocated"]
    )

    orders = orders_df.copy()

    orders["OrderDate"] = pd.to_datetime(
        orders["OrderDateKey"].astype(str),
        format="%Y%m%d",
    )

    orders["ShippedDate"] = pd.to_datetime(
        orders["ShippedDateKey"]
        .astype("Int64")
        .astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    sales_with_orders = sales_df.merge(
        orders[
            [
                "OrderID",
                "OrderDate",
                "ShippedDate",
                "OrderStatus",
            ]
        ],
        on="OrderID",
        how="left",
        validate="many_to_one",
    )

    # ---------------------------------------------------------------
    # Inventory receipt events
    # ---------------------------------------------------------------

    received_purchases = purchases.loc[
        purchases["ReceivedQuantity"] > 0
    ].copy()

    purchase_events: dict[
        pd.Timestamp,
        list[dict[str, object]],
    ] = {}

    for _, purchase in received_purchases.iterrows():
        event_date = pd.Timestamp(purchase["PurchaseDate"])

        purchase_events.setdefault(event_date, []).append(
            {
                "ProductID": int(purchase["ProductID"]),
                "Quantity": int(purchase["ReceivedQuantity"]),
                "UnitCost": float(purchase["LandedUnitCost"]),
            }
        )

    # ---------------------------------------------------------------
    # Inventory dispatch events
    # ---------------------------------------------------------------

    shipped_sales = sales_with_orders.loc[
        sales_with_orders["ShippedDate"].notna()
    ].copy()

    shipment_events: dict[
        pd.Timestamp,
        list[dict[str, object]],
    ] = {}

    for _, sale in shipped_sales.iterrows():
        event_date = pd.Timestamp(sale["ShippedDate"])

        shipment_events.setdefault(event_date, []).append(
            {
                "ProductID": int(sale["ProductID"]),
                "Quantity": int(sale["Quantity"]),
                "UnitCost": float(sale["UnitCostAtSale"]),
            }
        )

    purchase_event_dates = sorted(purchase_events)
    shipment_event_dates = sorted(shipment_events)

    next_purchase_index = 0
    next_shipment_index = 0

    inventory_quantity = {
        int(product_id): 0
        for product_id in products["ProductID"]
    }

    inventory_cost_balance = {
        int(product_id): 0.00
        for product_id in products["ProductID"]
    }

    last_known_unit_cost = {
        int(product_id): 0.00
        for product_id in products["ProductID"]
    }

    snapshot_dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="ME",
    )

    reorder_points = {
        "Blind Box": 12,
        "Figure": 8,
        "Plush": 6,
    }

    safety_stock_levels = {
        "Blind Box": 6,
        "Figure": 4,
        "Plush": 3,
    }

    rows: list[dict[str, object]] = []
    inventory_snapshot_id = 700001

    for snapshot_date in snapshot_dates:
        snapshot_date = pd.Timestamp(snapshot_date)

        # Add inventory received up to the snapshot date.
        while (
            next_purchase_index < len(purchase_event_dates)
            and purchase_event_dates[next_purchase_index]
            <= snapshot_date
        ):
            event_date = purchase_event_dates[
                next_purchase_index
            ]

            for event in purchase_events[event_date]:
                product_id = int(event["ProductID"])
                quantity = int(event["Quantity"])
                unit_cost = float(event["UnitCost"])

                inventory_quantity[product_id] += quantity
                inventory_cost_balance[product_id] += (
                    quantity * unit_cost
                )
                last_known_unit_cost[product_id] = unit_cost

            next_purchase_index += 1

        # Remove inventory dispatched up to the snapshot date.
        while (
            next_shipment_index < len(shipment_event_dates)
            and shipment_event_dates[next_shipment_index]
            <= snapshot_date
        ):
            event_date = shipment_event_dates[
                next_shipment_index
            ]

            for event in shipment_events[event_date]:
                product_id = int(event["ProductID"])
                quantity = int(event["Quantity"])
                unit_cost = float(event["UnitCost"])

                inventory_quantity[product_id] = max(
                    0,
                    inventory_quantity[product_id] - quantity,
                )

                inventory_cost_balance[product_id] = max(
                    0.00,
                    inventory_cost_balance[product_id]
                    - (quantity * unit_cost),
                )

            next_shipment_index += 1

        # Orders placed but not dispatched at the snapshot date.
        reserved_records = sales_with_orders.loc[
            (sales_with_orders["OrderStatus"] != "Cancelled")
            & (sales_with_orders["OrderDate"] <= snapshot_date)
            & (
                sales_with_orders["ShippedDate"].isna()
                | (
                    sales_with_orders["ShippedDate"]
                    > snapshot_date
                )
            )
        ]

        reserved_by_product = (
            reserved_records.groupby("ProductID")["Quantity"]
            .sum()
            .to_dict()
        )

        # Quantities ordered from suppliers but not yet received.
        outstanding_purchases = purchases.loc[
            (purchases["PurchaseDate"] <= snapshot_date)
            & (
                purchases["PurchaseStatus"].isin(
                    [
                        "Ordered",
                        "In Transit",
                        "Partially Received",
                    ]
                )
            )
        ].copy()

        outstanding_purchases["OutstandingQuantity"] = (
            outstanding_purchases["QuantityPurchased"]
            - outstanding_purchases["ReceivedQuantity"]
        ).clip(lower=0)

        on_order_by_product = (
            outstanding_purchases.groupby("ProductID")[
                "OutstandingQuantity"
            ]
            .sum()
            .to_dict()
        )

        for _, product in products.iterrows():
            product_id = int(product["ProductID"])
            units_in_stock = int(
                inventory_quantity[product_id]
            )

            units_reserved = min(
                int(reserved_by_product.get(product_id, 0)),
                units_in_stock,
            )

            maximum_damageable_units = max(
                0,
                units_in_stock - units_reserved,
            )

            # Damage remains uncommon but possible.
            units_damaged = int(
                rng.binomial(
                    n=maximum_damageable_units,
                    p=0.008,
                )
            )

            units_on_order = int(
                on_order_by_product.get(product_id, 0)
            )

            if units_in_stock > 0:
                average_unit_cost = round(
                    inventory_cost_balance[product_id]
                    / units_in_stock,
                    2,
                )
            else:
                average_unit_cost = round(
                    last_known_unit_cost[product_id],
                    2,
                )

            subcategory = str(product["SubCategory"])

            rows.append(
                {
                    "InventorySnapshotID": (
                        inventory_snapshot_id
                    ),
                    "SnapshotDateKey": int(
                        snapshot_date.strftime("%Y%m%d")
                    ),
                    "ProductID": product_id,
                    "UnitsInStock": units_in_stock,
                    "UnitsReserved": units_reserved,
                    "UnitsDamaged": units_damaged,
                    "UnitsOnOrder": units_on_order,
                    "ReorderPoint": reorder_points[
                        subcategory
                    ],
                    "SafetyStock": safety_stock_levels[
                        subcategory
                    ],
                    "AverageUnitCost": average_unit_cost,
                }
            )

            inventory_snapshot_id += 1

    fact_inventory_snapshot = pd.DataFrame(rows)

    expected_rows = len(products) * len(snapshot_dates)

    if len(fact_inventory_snapshot) != expected_rows:
        raise ValueError(
            "Unexpected inventory snapshot row count. "
            f"Expected {expected_rows:,}, generated "
            f"{len(fact_inventory_snapshot):,}."
        )

    duplicate_snapshot_rows = (
        fact_inventory_snapshot.duplicated(
            subset=["SnapshotDateKey", "ProductID"]
        )
    )

    if duplicate_snapshot_rows.any():
        raise ValueError(
            "Duplicate ProductID and SnapshotDateKey "
            "combinations were generated."
        )

    invalid_stock_rows = fact_inventory_snapshot.loc[
        (
            fact_inventory_snapshot["UnitsReserved"]
            + fact_inventory_snapshot["UnitsDamaged"]
        )
        > fact_inventory_snapshot["UnitsInStock"]
    ]

    if not invalid_stock_rows.empty:
        raise ValueError(
            "Reserved and damaged units exceed physical stock."
        )

    return fact_inventory_snapshot