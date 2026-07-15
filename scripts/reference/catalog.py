"""Master product catalogue reference data for Potchi Potchi."""

from __future__ import annotations

from .brands.popmart import POPMART_PRODUCTS
from .brands.jellycat import JELLYCAT_PRODUCTS
from .brands.mofusand import MOFUSAND_PRODUCTS
from .brands.baby_three import BABY_THREE_PRODUCTS
from .brands.lucky_emma import LUCKY_EMMA_PRODUCTS
from .brands.nommi import NOMMI_PRODUCTS
from .brands.rolife_nanci import ROLIFE_NANCI_PRODUCTS
from .brands.sanrio import SANRIO_PRODUCTS


CATALOG_COLUMNS = [
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


ALL_PRODUCTS = [
    *POPMART_PRODUCTS,
    *JELLYCAT_PRODUCTS,
    *MOFUSAND_PRODUCTS,
    *BABY_THREE_PRODUCTS,
    *LUCKY_EMMA_PRODUCTS,
    *NOMMI_PRODUCTS,
    *ROLIFE_NANCI_PRODUCTS,
    *SANRIO_PRODUCTS,
]