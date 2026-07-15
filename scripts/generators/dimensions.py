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
            "IsRecurring": False,
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