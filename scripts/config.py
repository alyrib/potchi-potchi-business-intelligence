"""Central configuration for the Potchi Potchi synthetic data generator."""

from pathlib import Path

# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# ---------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------

RANDOM_SEED = 42

# ---------------------------------------------------------------------
# Reporting period
# ---------------------------------------------------------------------

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

# ---------------------------------------------------------------------
# Dataset volumes
# ---------------------------------------------------------------------

CUSTOMER_COUNT = 1_500
PRODUCT_COUNT = 74
SUPPLIER_COUNT = 12
SALES_CHANNEL_COUNT = 3
VENDOR_COUNT = 15
EXPENSE_CATEGORY_COUNT = 9

ORDER_COUNT = 6_000
TARGET_SALES_LINE_COUNT_MIN = 15_000
TARGET_SALES_LINE_COUNT_MAX = 18_000
PURCHASE_LINE_COUNT = 650
EXPENSE_COUNT = 250

# ---------------------------------------------------------------------
# Business assumptions
# ---------------------------------------------------------------------

INITIAL_CAPITAL_GBP = 20_000
INITIAL_INVENTORY_BUDGET_GBP = 13_850

DEFAULT_COUNTRY = "United Kingdom"
DEFAULT_CURRENCY = "GBP"

AVERAGE_ORDER_VALUE_GBP = 38.00
AVERAGE_UNITS_PER_ORDER = 2.4

# ---------------------------------------------------------------------
# Inventory assumptions
# ---------------------------------------------------------------------

INITIAL_STORAGE_TYPE = "Home Storage"
EXTERNAL_STORAGE_TYPE = "Shurgard Self Storage – Deptford"

MONTHLY_INVENTORY_SNAPSHOTS = True

# ---------------------------------------------------------------------
# Growth and seasonality
# ---------------------------------------------------------------------

YEAR_2024_ORDER_SHARE = 0.40
YEAR_2025_ORDER_SHARE = 0.60

MONTHLY_SEASONALITY = {
    1: 0.78,
    2: 0.90,
    3: 0.96,
    4: 1.00,
    5: 1.02,
    6: 0.98,
    7: 0.88,
    8: 0.92,
    9: 1.04,
    10: 1.15,
    11: 1.38,
    12: 1.55,
}

# ---------------------------------------------------------------------
# Customer behaviour
# ---------------------------------------------------------------------

CUSTOMER_SEGMENT_WEIGHTS = {
    "Casual": 0.70,
    "Regular": 0.22,
    "Collector": 0.08,
}

# ---------------------------------------------------------------------
# Product performance
# ---------------------------------------------------------------------

PRODUCT_PERFORMANCE_WEIGHTS = {
    "Top Seller": 0.15,
    "Standard": 0.65,
    "Slow Moving": 0.20,
}