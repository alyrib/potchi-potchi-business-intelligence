"""Dimension table generators for the Potchi Potchi project."""

from __future__ import annotations

import holidays
import pandas as pd

from config import END_DATE, START_DATE


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