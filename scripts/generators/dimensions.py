"""Dimension table generators for the Potchi Potchi project."""

from __future__ import annotations

import holidays
import pandas as pd

from config import (
    CUSTOMER_COUNT,
    END_DATE,
    RANDOM_SEED,
    START_DATE,
)


def _get_season(month: int) -> str:
    """Return the UK meteorological season for a month."""
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Autumn"


def _commercial_events() -> dict[pd.Timestamp, str]:
    """Return relevant UK commercial events for the reporting period."""
    return {
        pd.Timestamp("2024-02-14"): "Valentine's Day",
        pd.Timestamp("2024-10-31"): "Halloween",
        pd.Timestamp("2024-11-29"): "Black Friday",
        pd.Timestamp("2024-12-02"): "Cyber Monday",
        pd.Timestamp("2025-02-14"): "Valentine's Day",
        pd.Timestamp("2025-10-31"): "Halloween",
        pd.Timestamp("2025-11-28"): "Black Friday",
        pd.Timestamp("2025-12-01"): "Cyber Monday",
    }


def generate_dim_date() -> pd.DataFrame:
    """Generate the complete DimDate dataframe."""
    date_range = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="D",
    )

    df = pd.DataFrame({"Date": date_range})

    df["DateKey"] = df["Date"].dt.strftime("%Y%m%d").astype(int)
    df["Day"] = df["Date"].dt.day
    df["DayOfYear"] = df["Date"].dt.dayofyear
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["DayOfWeekNumber"] = df["Date"].dt.isocalendar().day.astype(int)
    df["WeekNumber"] = df["Date"].dt.isocalendar().week.astype(int)
    df["MonthNumber"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.month_name()
    df["MonthShortName"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["YearQuarter"] = (
        df["Date"].dt.year.astype(str)
        + "-Q"
        + df["Date"].dt.quarter.astype(str)
    )
    df["Year"] = df["Date"].dt.year
    df["Season"] = df["MonthNumber"].map(_get_season)
    df["IsWeekend"] = df["DayOfWeekNumber"].isin([6, 7])
    df["IsMonthEnd"] = df["Date"].dt.is_month_end
    df["IsYearEnd"] = df["Date"].dt.is_year_end

    uk_holidays = holidays.UnitedKingdom(
        years=sorted(df["Year"].unique()),
        subdiv="England",
    )

    df["HolidayName"] = df["Date"].map(
        lambda value: uk_holidays.get(value.date())
    )
    df["IsHoliday"] = df["HolidayName"].notna()

    commercial_events = _commercial_events()
    df["CommercialEventName"] = df["Date"].map(commercial_events)
    df["IsCommercialEvent"] = df["CommercialEventName"].notna()

    column_order = [
        "DateKey",
        "Date",
        "Day",
        "DayOfYear",
        "DayOfWeek",
        "DayOfWeekNumber",
        "WeekNumber",
        "MonthNumber",
        "MonthName",
        "MonthShortName",
        "YearMonth",
        "Quarter",
        "YearQuarter",
        "Year",
        "Season",
        "IsWeekend",
        "IsMonthEnd",
        "IsYearEnd",
        "IsHoliday",
        "HolidayName",
        "IsCommercialEvent",
        "CommercialEventName",
    ]

    return df[column_order]

def generate_dim_expense_category() -> pd.DataFrame:
    """Generate the controlled DimExpenseCategory dataframe."""

    data = [
        {
            "ExpenseCategoryID": 1,
            "ExpenseCategoryName": "Marketing",
            "ExpenseType": "Operating Expense",
            "IsFixed": False,
            "IsRecurring": False,
            "IsDiscretionary": True,
        },
        {
            "ExpenseCategoryID": 2,
            "ExpenseCategoryName": "Software",
            "ExpenseType": "Operating Expense",
            "IsFixed": True,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 3,
            "ExpenseCategoryName": "Website and Domain",
            "ExpenseType": "Operating Expense",
            "IsFixed": True,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 4,
            "ExpenseCategoryName": "Storage",
            "ExpenseType": "Operating Expense",
            "IsFixed": True,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 5,
            "ExpenseCategoryName": "Packaging",
            "ExpenseType": "Operating Expense",
            "IsFixed": False,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 6,
            "ExpenseCategoryName": "Accounting",
            "ExpenseType": "Operating Expense",
            "IsFixed": True,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 7,
            "ExpenseCategoryName": "Insurance",
            "ExpenseType": "Operating Expense",
            "IsFixed": True,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 8,
            "ExpenseCategoryName": "Utilities",
            "ExpenseType": "Operating Expense",
            "IsFixed": False,
            "IsRecurring": True,
            "IsDiscretionary": False,
        },
        {
            "ExpenseCategoryID": 9,
            "ExpenseCategoryName": "Professional Services",
            "ExpenseType": "Operating Expense",
            "IsFixed": False,
            "IsRecurring": False,
            "IsDiscretionary": True,
        },
    ]

    return pd.DataFrame(data)


def generate_dim_sales_channel() -> pd.DataFrame:
    """Generate the controlled DimSalesChannel dataframe."""

    data = [
        {
            "SalesChannelID": 1,
            "SalesChannelName": "Website",
            "ChannelType": "Owned E-commerce",
            "IsOwnedChannel": True,
            "IsMarketplace": False,
            "PlatformFeeRate": 0.00,
            "LaunchDate": "2024-01-01",
            "ChannelStatus": "Active",
        },
        {
            "SalesChannelID": 2,
            "SalesChannelName": "Instagram",
            "ChannelType": "Social Referral",
            "IsOwnedChannel": True,
            "IsMarketplace": False,
            "PlatformFeeRate": 0.00,
            "LaunchDate": "2024-01-01",
            "ChannelStatus": "Active",
        },
        {
            "SalesChannelID": 3,
            "SalesChannelName": "TikTok Shop",
            "ChannelType": "Social Commerce",
            "IsOwnedChannel": False,
            "IsMarketplace": True,
            "PlatformFeeRate": 0.05,
            "LaunchDate": "2024-06-01",
            "ChannelStatus": "Active",
        },
    ]

    df = pd.DataFrame(data)

    df["LaunchDate"] = pd.to_datetime(df["LaunchDate"])

    return df


def generate_dim_supplier() -> pd.DataFrame:
    """Generate the controlled DimSupplier dataframe."""

    data = [
        {
            "SupplierID": 1,
            "SupplierName": "Kawaii Distribution UK",
            "Country": "United Kingdom",
            "CurrencyCode": "GBP",
            "SupplierType": "Authorised Distributor",
            "LeadTimeDays": 5,
            "MinimumOrderValue": 300.00,
            "MinimumOrderQuantity": 6,
            "PrimaryShippingMethod": "Domestic Courier",
            "PaymentTerms": "Net 30",
            "SupplierRating": 4.8,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 2,
            "SupplierName": "Cute Collectibles Europe",
            "Country": "Netherlands",
            "CurrencyCode": "EUR",
            "SupplierType": "Authorised Distributor",
            "LeadTimeDays": 10,
            "MinimumOrderValue": 500.00,
            "MinimumOrderQuantity": 12,
            "PrimaryShippingMethod": "Road Freight",
            "PaymentTerms": "Net 30",
            "SupplierRating": 4.7,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 3,
            "SupplierName": "Sakura Toy Imports",
            "Country": "Japan",
            "CurrencyCode": "JPY",
            "SupplierType": "Wholesaler",
            "LeadTimeDays": 28,
            "MinimumOrderValue": 900.00,
            "MinimumOrderQuantity": 24,
            "PrimaryShippingMethod": "Air Freight",
            "PaymentTerms": "Upfront",
            "SupplierRating": 4.5,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 4,
            "SupplierName": "Mochi Merchandising",
            "Country": "China",
            "CurrencyCode": "CNY",
            "SupplierType": "Manufacturer",
            "LeadTimeDays": 35,
            "MinimumOrderValue": 1200.00,
            "MinimumOrderQuantity": 48,
            "PrimaryShippingMethod": "Air Freight",
            "PaymentTerms": "50% Deposit",
            "SupplierRating": 4.3,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 5,
            "SupplierName": "Pastel Planet Wholesale",
            "Country": "United Kingdom",
            "CurrencyCode": "GBP",
            "SupplierType": "Wholesaler",
            "LeadTimeDays": 4,
            "MinimumOrderValue": 250.00,
            "MinimumOrderQuantity": 6,
            "PrimaryShippingMethod": "Domestic Courier",
            "PaymentTerms": "Net 14",
            "SupplierRating": 4.4,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 6,
            "SupplierName": "Nordic Art Toy Supply",
            "Country": "Germany",
            "CurrencyCode": "EUR",
            "SupplierType": "Authorised Distributor",
            "LeadTimeDays": 12,
            "MinimumOrderValue": 600.00,
            "MinimumOrderQuantity": 12,
            "PrimaryShippingMethod": "Road Freight",
            "PaymentTerms": "Net 30",
            "SupplierRating": 4.6,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 7,
            "SupplierName": "Moon Rabbit Trading",
            "Country": "South Korea",
            "CurrencyCode": "KRW",
            "SupplierType": "Wholesaler",
            "LeadTimeDays": 24,
            "MinimumOrderValue": 800.00,
            "MinimumOrderQuantity": 24,
            "PrimaryShippingMethod": "Air Freight",
            "PaymentTerms": "Upfront",
            "SupplierRating": 4.2,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 8,
            "SupplierName": "Tiny Treasures UK",
            "Country": "United Kingdom",
            "CurrencyCode": "GBP",
            "SupplierType": "Authorised Distributor",
            "LeadTimeDays": 6,
            "MinimumOrderValue": 350.00,
            "MinimumOrderQuantity": 6,
            "PrimaryShippingMethod": "Domestic Courier",
            "PaymentTerms": "Net 30",
            "SupplierRating": 4.9,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 9,
            "SupplierName": "Cloudberry Collectibles",
            "Country": "France",
            "CurrencyCode": "EUR",
            "SupplierType": "Wholesaler",
            "LeadTimeDays": 9,
            "MinimumOrderValue": 450.00,
            "MinimumOrderQuantity": 12,
            "PrimaryShippingMethod": "Road Freight",
            "PaymentTerms": "Net 14",
            "SupplierRating": 4.1,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 10,
            "SupplierName": "Dream Capsule Trading",
            "Country": "China",
            "CurrencyCode": "CNY",
            "SupplierType": "Manufacturer",
            "LeadTimeDays": 40,
            "MinimumOrderValue": 1500.00,
            "MinimumOrderQuantity": 60,
            "PrimaryShippingMethod": "Sea Freight",
            "PaymentTerms": "50% Deposit",
            "SupplierRating": 4.0,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 11,
            "SupplierName": "Little Star Imports",
            "Country": "United States",
            "CurrencyCode": "USD",
            "SupplierType": "Wholesaler",
            "LeadTimeDays": 18,
            "MinimumOrderValue": 700.00,
            "MinimumOrderQuantity": 18,
            "PrimaryShippingMethod": "Air Freight",
            "PaymentTerms": "Upfront",
            "SupplierRating": 4.3,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
        {
            "SupplierID": 12,
            "SupplierName": "Cozy Shelf Distribution",
            "Country": "United Kingdom",
            "CurrencyCode": "GBP",
            "SupplierType": "Wholesaler",
            "LeadTimeDays": 7,
            "MinimumOrderValue": 300.00,
            "MinimumOrderQuantity": 6,
            "PrimaryShippingMethod": "Domestic Courier",
            "PaymentTerms": "Net 14",
            "SupplierRating": 4.5,
            "IsAuthorised": True,
            "SupplierStatus": "Active",
        },
    ]

    return pd.DataFrame(data)


def generate_dim_product(
    master_catalog_path,
    supplier_df: pd.DataFrame,
) -> pd.DataFrame:
    """Generate DimProduct from the controlled master catalogue."""

    catalogue_df = pd.read_csv(master_catalog_path)

    required_columns = [
        "Brand",
        "License",
        "Character",
        "Collection",
        "ProductName",
        "Category",
        "SubCategory",
        "Theme",
        "ReleaseYear",
        "MSRP",
        "Material",
        "RecommendedAge",
        "IsBlindBox",
        "IsLimitedEdition",
        "IsExclusive",
        "SourceURL",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in catalogue_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Master catalogue is missing required columns: "
            + ", ".join(missing_columns)
        )

    if catalogue_df.empty:
        raise ValueError("Master product catalogue cannot be empty.")

    if catalogue_df["ProductName"].duplicated().any():
        duplicated_products = catalogue_df.loc[
            catalogue_df["ProductName"].duplicated(),
            "ProductName",
        ].tolist()

        raise ValueError(
            "Duplicate product names found: "
            + ", ".join(duplicated_products)
        )

    df = catalogue_df.copy()

    df.insert(
        0,
        "ProductID",
        range(2001, 2001 + len(df)),
    )

    supplier_ids = supplier_df["SupplierID"].tolist()

    # Assign suppliers cyclically to guarantee valid foreign keys
    # and reasonable catalogue distribution.
    df["SupplierID"] = [
        supplier_ids[index % len(supplier_ids)]
        for index in range(len(df))
    ]

    df["ProductStatus"] = "Active"

    # Products released in 2025 remain active because the dataset
    # covers the complete 2024–2025 operating period.
    df.loc[
        df["ReleaseYear"].notna()
        & (df["ReleaseYear"] > 2025),
        "ProductStatus",
    ] = "Coming Soon"

    df = df.drop(columns=["SourceURL"])

    column_order = [
        "ProductID",
        "ProductName",
        "Brand",
        "License",
        "Character",
        "Collection",
        "Category",
        "SubCategory",
        "Theme",
        "SupplierID",
        "ReleaseYear",
        "MSRP",
        "Material",
        "RecommendedAge",
        "IsBlindBox",
        "ProductStatus",
        "IsLimitedEdition",
        "IsExclusive",
    ]

    return df[column_order]


def generate_dim_vendor() -> pd.DataFrame:
    """Generate the controlled DimVendor dataframe."""

    data = [
        {
            "VendorID": 1,
            "VendorName": "Shopify",
            "VendorCategory": "E-commerce Platform",
            "Country": "Canada",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 2,
            "VendorName": "Meta",
            "VendorCategory": "Digital Advertising",
            "Country": "United States",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 3,
            "VendorName": "TikTok for Business",
            "VendorCategory": "Digital Advertising",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 4,
            "VendorName": "Canva",
            "VendorCategory": "Design Software",
            "Country": "Australia",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 5,
            "VendorName": "Microsoft",
            "VendorCategory": "Business Software",
            "Country": "United States",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 6,
            "VendorName": "Shurgard Self Storage",
            "VendorCategory": "Storage",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 7,
            "VendorName": "Royal Mail",
            "VendorCategory": "Shipping Services",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 8,
            "VendorName": "Packhelp",
            "VendorCategory": "Packaging Services",
            "Country": "Poland",
            "DefaultCurrencyCode": "EUR",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 9,
            "VendorName": "AXA Business Insurance",
            "VendorCategory": "Insurance",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 10,
            "VendorName": "Xero",
            "VendorCategory": "Accounting Software",
            "Country": "New Zealand",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 11,
            "VendorName": "Companies House",
            "VendorCategory": "Government Services",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 12,
            "VendorName": "Google Workspace",
            "VendorCategory": "Business Software",
            "Country": "United States",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 13,
            "VendorName": "Namecheap",
            "VendorCategory": "Domain Services",
            "Country": "United States",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 14,
            "VendorName": "Octopus Energy",
            "VendorCategory": "Utilities",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
        {
            "VendorID": 15,
            "VendorName": "Independent Business Consultant",
            "VendorCategory": "Professional Services",
            "Country": "United Kingdom",
            "DefaultCurrencyCode": "GBP",
            "VendorStatus": "Active",
        },
    ]

    return pd.DataFrame(data)


def generate_dim_customer() -> pd.DataFrame:
    """Generate the synthetic DimCustomer dataframe."""

    from faker import Faker
    import numpy as np

    rng = np.random.default_rng(RANDOM_SEED + 200)
    fake = Faker("en_GB")
    Faker.seed(RANDOM_SEED + 200)

    locations = [
        ("London", "Greater London"),
        ("Manchester", "North West England"),
        ("Birmingham", "West Midlands"),
        ("Leeds", "Yorkshire and the Humber"),
        ("Glasgow", "Scotland"),
        ("Liverpool", "North West England"),
        ("Bristol", "South West England"),
        ("Edinburgh", "Scotland"),
        ("Cardiff", "Wales"),
        ("Brighton", "South East England"),
        ("Nottingham", "East Midlands"),
        ("Newcastle upon Tyne", "North East England"),
    ]

    location_weights = np.array(
        [0.30, 0.10, 0.09, 0.07, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.06]
    )

    acquisition_sources = [
        "Instagram",
        "TikTok",
        "Organic Search",
        "Google Ads",
        "Referral",
        "Friend Recommendation",
    ]

    acquisition_weights = [
        0.28,
        0.26,
        0.18,
        0.10,
        0.08,
        0.10,
    ]

    preferred_channels = [
        "Website",
        "Instagram",
        "TikTok Shop",
    ]

    preferred_channel_weights = [
        0.48,
        0.14,
        0.38,
    ]

    start_date = pd.Timestamp(START_DATE)
    end_date = pd.Timestamp(END_DATE)

    rows: list[dict[str, object]] = []

    for customer_id in range(1001, 1001 + CUSTOMER_COUNT):
        birth_date = pd.Timestamp(
            fake.date_of_birth(
                minimum_age=18,
                maximum_age=65,
            )
        )

        registration_date = pd.Timestamp(
            rng.choice(
                pd.date_range(
                    start=start_date,
                    end=end_date,
                    freq="D",
                )
            )
        )

        age_at_end = end_date.year - birth_date.year - (
            (end_date.month, end_date.day)
            < (birth_date.month, birth_date.day)
        )

        if age_at_end <= 24:
            age_group = "18–24"
            generation = "Gen Z"
        elif age_at_end <= 34:
            age_group = "25–34"
            generation = "Millennial"
        elif age_at_end <= 44:
            age_group = "35–44"
            generation = "Millennial"
        elif age_at_end <= 54:
            age_group = "45–54"
            generation = "Gen X"
        elif age_at_end <= 64:
            age_group = "55–64"
            generation = "Gen X"
        else:
            age_group = "65+"
            generation = "Baby Boomer"

        city, region = locations[
            rng.choice(
                len(locations),
                p=location_weights,
            )
        ]

        loyalty_member = bool(rng.random() < 0.38)
        marketing_opt_in = bool(rng.random() < 0.62)

        rows.append(
            {
                "CustomerID": customer_id,
                "FirstName": fake.first_name(),
                "LastName": fake.last_name(),
                "BirthDate": birth_date,
                "AgeGroup": age_group,
                "Generation": generation,
                "City": city,
                "Region": region,
                "Country": "United Kingdom",
                "RegistrationDate": registration_date,
                "PreferredChannel": rng.choice(
                    preferred_channels,
                    p=preferred_channel_weights,
                ),
                "LoyaltyMember": loyalty_member,
                "MarketingOptIn": marketing_opt_in,
                "AcquisitionSource": rng.choice(
                    acquisition_sources,
                    p=acquisition_weights,
                ),
                "CustomerStatus": rng.choice(
                    ["Active", "Inactive"],
                    p=[0.88, 0.12],
                ),
            }
        )

    return pd.DataFrame(rows)
