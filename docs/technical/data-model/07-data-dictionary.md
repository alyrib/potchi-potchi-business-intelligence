# 1. Purpose

The purpose of this document is to define every field used throughout the Potchi Potchi Business Intelligence solution.

The Data Dictionary establishes a common business language by documenting field names, data types, business definitions, examples and validation rules.

This document serves as the primary reference during dataset creation, Power Query transformations, Power BI semantic modelling and dashboard development.

Unlike the Dataset Design Specification, which describes datasets at a structural level, the Data Dictionary focuses on individual fields and their business meaning.

---

# 2. Naming Standards

The project follows consistent naming conventions to improve readability, maintainability and scalability.

## General Naming Rules

- PascalCase is used for all table and column names.
- Singular nouns are preferred.
- Field names should be descriptive and avoid unnecessary abbreviations.
- Primary Keys end with `ID`.
- Foreign Keys use the same name as their referenced Primary Key.
- Boolean fields begin with `Is` whenever appropriate.
- Monetary values include a descriptive suffix such as `Price`, `Cost` or `Amount`.

## Examples

| Correct | Incorrect |
|----------|-----------|
| ProductID | Product_Id |
| CustomerID | customerid |
| SupplierID | Supplier_Id |
| OrderDate | order_date |
| IsExclusive | ExclusiveFlag |
| NetUnitPrice | NetPriceValue |
| LeadTimeDays | Lead_Time |

## Table Naming

Dimension tables use the prefix:

```text
Dim
```

Examples:

```text
DimCustomer
DimProduct
DimSupplier
DimDate
```

Fact tables use the prefix:

```text
Fact
```

Examples:

```text
FactOrders
FactSales
FactPurchases
FactInventorySnapshot
FactExpenses
```

---

# 3. Data Type Standards

The following data types are used consistently throughout the project.

| Data Type | Purpose | Example |
|-----------|---------|---------|
| Integer | Identifiers, quantities and numeric counters | 125 |
| Decimal | Monetary values and calculated financial metrics | 18.99 |
| Text | Descriptive information | Blind Box |
| Date | Calendar dates | 13 July 2026 |
| Boolean | True / False values | True |

## Monetary Values

Unless otherwise specified, all financial values are stored in **GBP (£)**.

Historical purchasing data may contain additional currency fields to preserve original supplier transactions.

## Dates

Dates follow the United Kingdom format for presentation.

Relationships within the data model use surrogate integer keys (`DateKey`) stored in `YYYYMMDD` format.

## Boolean Fields

Boolean fields contain only:

```text
True
False
```

Examples include:

- IsWeekend
- IsHoliday
- IsCommercialEvent
- IsBlindBox
- IsExclusive
- IsLimitedEdition
- IsAuthorised
- LoyaltyMember
- MarketingOptIn

## Missing Values

Nullable fields should only contain blank values when the information is genuinely unavailable or not applicable.

Blank values must not be used as substitutes for unknown business categories.

---

# 4. DimDate

## Description

Stores the calendar attributes required for time intelligence, seasonal analysis, inventory snapshots and commercial-event reporting.

The table contains one row per calendar date and covers the complete two-year operating period represented within the project.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| DateKey | Integer | No | Unique date identifier stored in `YYYYMMDD` format. | 20260713 | Primary key and fact-table relationships |
| Date | Date | No | Full calendar date. | 13 July 2026 | Time intelligence and date filtering |
| Day | Integer | No | Day number within the month. | 13 | Daily analysis |
| DayOfYear | Integer | No | Sequential day number within the year. | 194 | Year progression analysis |
| DayOfWeek | Text | No | Full weekday name. | Monday | Sales analysis by weekday |
| DayOfWeekNumber | Integer | No | Numeric weekday value used for sorting. | 1 | Sorts weekday names chronologically |
| WeekNumber | Integer | No | ISO week number. | 29 | Weekly performance analysis |
| MonthNumber | Integer | No | Numeric month value. | 7 | Sorts month names chronologically |
| MonthName | Text | No | Full month name. | July | Monthly filtering and reporting |
| MonthShortName | Text | No | Abbreviated month name. | Jul | Compact chart labels |
| YearMonth | Text | No | Unique year and month identifier. | 2026-07 | Monthly trends across multiple years |
| Quarter | Text | No | Calendar quarter. | Q3 | Quarterly analysis |
| YearQuarter | Text | No | Unique year and quarter identifier. | 2026-Q3 | Quarterly trends across multiple years |
| Year | Integer | No | Calendar year. | 2026 | Annual analysis |
| Season | Text | No | UK meteorological season. | Summer | Seasonal sales analysis |
| IsWeekend | Boolean | No | Indicates whether the date falls on Saturday or Sunday. | True | Weekday versus weekend comparison |
| IsMonthEnd | Boolean | No | Indicates whether the date is the final day of the month. | False | Monthly inventory snapshots |
| IsYearEnd | Boolean | No | Indicates whether the date is the final day of the year. | False | Year-end reporting |
| IsHoliday | Boolean | No | Indicates whether the date is an official UK public holiday. | False | Holiday performance analysis |
| HolidayName | Text | Yes | Name of the UK public holiday, when applicable. | Christmas Day | Holiday-specific analysis |
| IsCommercialEvent | Boolean | No | Indicates whether the date is commercially significant. | True | Campaign and seasonal-event analysis |
| CommercialEventName | Text | Yes | Name of the commercial event, when applicable. | Black Friday | Promotional performance analysis |

## Business Rules

- `DateKey` must be unique.
- `DateKey` must follow the `YYYYMMDD` format.
- The table must contain exactly one row per calendar date.
- Dates must not be duplicated.
- `DayOfWeekNumber` must correctly sort `DayOfWeek`.
- `MonthNumber` must correctly sort `MonthName` and `MonthShortName`.
- `HolidayName` may only contain a value when `IsHoliday` is `True`.
- `CommercialEventName` may only contain a value when `IsCommercialEvent` is `True`.
- UK public holidays will be used during the initial project scope.
- Commercial events may include Valentine’s Day, Halloween, Black Friday, Cyber Monday and Christmas shopping periods.

---

# 5. DimCustomer

## Description

Stores descriptive and demographic customer attributes used to analyse customer acquisition, location, channel preference and purchasing behaviour.

The table contains one row per customer.

Personally identifiable information that does not contribute to the analytical objectives, such as email addresses and telephone numbers, is excluded.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| CustomerID | Integer | No | Unique customer identifier. | 1001 | Primary key and fact-table relationships |
| FirstName | Text | No | Fictional customer first name. | Emily | Customer-level exploration |
| LastName | Text | No | Fictional customer surname. | Parker | Customer-level exploration |
| BirthDate | Date | No | Customer date of birth. | 14 March 1996 | Source for age and generation calculations |
| AgeGroup | Text | No | Derived customer age band. | 25–34 | Demographic segmentation |
| Generation | Text | No | Derived generational cohort. | Millennial | Behavioural comparison by generation |
| City | Text | No | Customer city. | London | Geographic analysis |
| Region | Text | No | UK region or nation associated with the customer. | Greater London | Regional performance analysis |
| Country | Text | No | Customer country. | United Kingdom | Geographic filtering and future expansion |
| RegistrationDate | Date | No | Date on which the customer account was created. | 10 January 2026 | Customer acquisition analysis |
| PreferredChannel | Text | No | Customer’s preferred purchasing channel. | TikTok Shop | Channel preference analysis |
| LoyaltyMember | Boolean | No | Indicates whether the customer participates in the loyalty programme. | True | Loyalty performance comparison |
| MarketingOptIn | Boolean | No | Indicates whether the customer agreed to receive marketing communications. | True | Marketing eligibility analysis |
| AcquisitionSource | Text | No | Channel through which the customer first discovered the business. | Instagram | Customer acquisition analysis |
| CustomerStatus | Text | No | Current customer classification. | Active | Active and inactive customer analysis |

## Derived Fields

`AgeGroup` and `Generation` will be derived in Power Query from `BirthDate`.

Recommended `AgeGroup` values:

```text
18–24
25–34
35–44
45–54
55–64
65+
```

Recommended `Generation` values:

```text
Gen Z
Millennial
Gen X
Baby Boomer
```

## Geographic Scope

During the initial operating period, customers are assumed to be located within the United Kingdom.

The `Country` field is retained to support future expansion into Ireland and selected European markets without requiring structural changes to the model.

## Business Rules

- `CustomerID` must be unique.
- `FirstName` and `LastName` cannot be empty.
- `BirthDate` cannot occur after `RegistrationDate`.
- Customers must be at least 18 years old at the time of registration.
- `RegistrationDate` cannot occur after the customer’s first order date.
- `Country` will contain `United Kingdom` during the initial implementation.
- `CustomerStatus` must be `Active` or `Inactive`.
- `PreferredChannel` must reference an approved sales-channel value.
- Gender will not be collected because it does not support the project’s primary business questions.
- Customer metrics such as total spend, number of orders and customer lifetime value must be calculated from fact tables rather than stored within `DimCustomer`.

---

# 6. DimProduct

## Description

Stores descriptive attributes for products selected and curated by Potchi Potchi.

The table contains one row per unique product or SKU.

The dimension describes what the product is. Acquisition costs, selling prices and transaction-level financial values are stored within the relevant fact tables.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| ProductID | Integer | No | Unique product identifier. | 2001 | Primary key and fact-table relationships |
| ProductName | Text | No | Commercial product name. | DIMOO Aquarium Jellyfish | Product-level reporting |
| Brand | Text | No | Product manufacturer or commercial brand. | POP MART | Brand performance analysis |
| License | Text | No | Intellectual property or licensed franchise. Use `Original` for proprietary characters. | Sanrio | Licensed-franchise analysis |
| Character | Text | Yes | Main character represented by the product. | Hello Kitty | Character performance analysis |
| Collection | Text | Yes | Manufacturer collection or release grouping. | Cherry Blossom Series | Collection performance analysis |
| Category | Text | No | High-level product classification. | Collectibles | Category drill-down |
| SubCategory | Text | No | Detailed product classification. | Blind Box | Subcategory drill-down |
| Theme | Text | No | Potchi Potchi-curated thematic classification. | Sakura | Marketing and merchandising analysis |
| SupplierID | Integer | No | Identifier of the supplier associated with the product. | 3 | Relationship with `DimSupplier` |
| ReleaseYear | Integer | Yes | Year in which the product was released. | 2025 | New-release performance analysis |
| MSRP | Decimal | Yes | Manufacturer’s suggested retail price in GBP. | 18.00 | Price-positioning reference |
| Material | Text | Yes | Primary product material. | PVC + ABS | Product attribute analysis |
| RecommendedAge | Text | Yes | Manufacturer’s recommended minimum age. | 15+ | Product information |
| Rarity | Text | No | Product rarity classification. | Secret | Rarity performance analysis |
| IsBlindBox | Boolean | No | Indicates whether the product is sold in blind-box format. | True | Blind-box analysis |
| ProductStatus | Text | No | Current catalogue status. | Active | Active and discontinued product analysis |
| IsLimitedEdition | Boolean | No | Indicates whether the product has a limited production run. | False | Limited-edition performance |
| IsExclusive | Boolean | No | Indicates whether the product is exclusive to a retailer, event or market. | True | Exclusive-product analysis |

## Category Hierarchy

The product hierarchy is structured as:

```text
Category
    ↓
SubCategory
```

Examples:

```text
Collectibles
├── Blind Box
├── Figure
├── Plush
├── Trading Card
└── Acrylic Stand

Accessories
├── Keychain
├── Lanyard
└── Phone Charm

Home
├── Mug
├── Lamp
└── Cushion

Apparel
├── T-Shirt
├── Hoodie
└── Socks

Stationery
├── Notebook
├── Pen
└── Sticker Pack
```

A blind box remains classified as a subcategory of `Collectibles`, even when blind boxes represent the majority of the catalogue.

## Source and Enriched Attributes

Manufacturer-provided attributes include:

- Brand
- License
- Character
- Collection
- ReleaseYear
- MSRP
- Material
- RecommendedAge
- Rarity

Potchi Potchi-enriched attributes include:

- Category
- SubCategory
- Theme
- ProductStatus
- IsLimitedEdition
- IsExclusive

The `Theme` field reflects Potchi Potchi’s merchandising and curatorial strategy rather than the manufacturer’s formal catalogue structure.

## Business Rules

- `ProductID` must be unique.
- `ProductName` cannot be empty.
- `Category` and `SubCategory` must use approved catalogue values.
- Every `SubCategory` must belong to a valid `Category`.
- `SupplierID` must reference an existing supplier.
- `MSRP` cannot be negative.
- `ReleaseYear` cannot occur in the future.
- `ProductStatus` must be `Active`, `Coming Soon` or `Discontinued`.
- `Rarity` must use an approved value such as `Regular`, `Secret`, `Chase`, `Limited` or `Exclusive`.
- Products marketed as officially licensed must be supplied by an authorised supplier.
- Product acquisition cost must not be stored in `DimProduct`.
- Historical selling price and the final amount paid by the customer must be stored within `FactSales`.
- Historical product acquisition costs must be stored within `FactPurchases`.

---

# 7. DimSupplier

## Description

Stores descriptive supplier attributes used for procurement, lead-time, sourcing and supplier-performance analysis.

The table contains one row per supplier.

Operational contact details that do not contribute to the analytical objectives are excluded.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| SupplierID | Integer | No | Unique supplier identifier. | 3 | Primary key and fact-table relationships |
| SupplierName | Text | No | Supplier, manufacturer or distributor name. | Asia Collectibles Distribution | Supplier-level analysis |
| Country | Text | No | Country in which the supplier operates. | China | Sourcing and geographic-risk analysis |
| CurrencyCode | Text | No | Three-letter purchasing currency code. | CNY | Currency and purchasing analysis |
| SupplierType | Text | No | Supplier business classification. | Authorised Distributor | Supplier segmentation |
| LeadTimeDays | Integer | No | Expected delivery time in calendar days. | 28 | Procurement and replenishment planning |
| MinimumOrderValue | Decimal | Yes | Minimum monetary purchase value required by the supplier. | 500.00 | Purchase-order planning |
| MinimumOrderQuantity | Integer | Yes | Minimum number of units required per purchase order or product line. | 12 | Inventory planning |
| PrimaryShippingMethod | Text | No | Main shipping method used by the supplier. | Air Freight | Logistics analysis |
| PaymentTerms | Text | No | Commercial payment arrangement. | Upfront | Cash-flow planning |
| SupplierRating | Decimal | No | Internal supplier-performance score from 1.0 to 5.0. | 4.6 | Supplier comparison |
| IsAuthorised | Boolean | No | Indicates whether the supplier is authorised to distribute the relevant brands. | True | Licensing and authenticity controls |
| SupplierStatus | Text | No | Current supplier status. | Active | Active and inactive supplier analysis |

## Supplier Rating

`SupplierRating` may reflect:

- delivery reliability;
- order accuracy;
- product condition;
- packaging quality;
- communication quality;
- issue-resolution performance.

The initial synthetic dataset will use plausible supplier ratings. A future version may calculate the rating dynamically from purchasing and delivery data.

## Business Rules

- `SupplierID` must be unique.
- `SupplierName` cannot be empty.
- `LeadTimeDays` must be greater than zero.
- `MinimumOrderValue` cannot be negative.
- `MinimumOrderQuantity` cannot be negative.
- `SupplierRating` must be between `1.0` and `5.0`.
- `CurrencyCode` must use a valid three-letter currency code.
- `SupplierStatus` must be `Active`, `On Hold` or `Inactive`.
- Only authorised suppliers may provide products marketed as officially licensed.
- Supplier purchasing totals, order counts, average realised lead time and generated margin must be calculated from fact tables rather than stored within `DimSupplier`.

---

# 8. DimSalesChannel

## Description

Stores descriptive and commercial attributes for the channels through which Potchi Potchi receives customer orders.

The table contains one row per approved sales channel.

A dedicated dimension is required because sales channels have their own attributes, including platform fees, ownership type, marketplace classification, launch dates and operational status.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| SalesChannelID | Integer | No | Unique sales-channel identifier. | 1 | Primary key and `FactOrders` relationship |
| SalesChannelName | Text | No | Commercial channel name. | TikTok Shop | Channel-level analysis |
| ChannelType | Text | No | High-level channel classification. | Social Commerce | Channel segmentation |
| IsOwnedChannel | Boolean | No | Indicates whether Potchi Potchi directly owns and controls the channel. | False | Owned versus third-party analysis |
| IsMarketplace | Boolean | No | Indicates whether the channel operates as a third-party marketplace. | True | Marketplace performance analysis |
| PlatformFeeRate | Decimal | No | Current proportional platform fee charged on eligible sales. | 0.05 | Channel-cost planning |
| LaunchDate | Date | No | Date on which the channel became available to customers. | 1 March 2026 | Channel adoption analysis |
| ChannelStatus | Text | No | Current operational status. | Active | Active and planned channel filtering |

## Initial Channel Values

The first implementation may include:

```text
Website
TikTok Shop
Instagram
```
## Potential ChannelType values include

- Owned E-commerce
- Social Commerce
- Social Referral
- Marketplace

## Business Rules

- SalesChannelID must be unique.
- SalesChannelName cannot be empty.
- PlatformFeeRate must be between 0 and 1.
- LaunchDate cannot occur after the date of an order using that channel.
- ChannelStatus must be Active, Planned or Inactive.
- FactOrders[SalesChannelID] must reference an existing sales channel.
- PreferredChannel in DimCustomer represents customer preference and must not replace the transactional sales channel.
- The current platform fee rate is stored within DimSalesChannel.
- The historical platform fee amount charged on a completed sale must be preserved within FactSales.
- 
---

# Appendix

## Related Documents

| Document | Version | Status |
|----------|---------|--------|
| 01 - Market Research | v0.1.0 | Completed |
| 02 - Business Requirements Document | v0.2.0 | Completed |
| 03 - Data Requirements Document | v0.2.0 | Completed |
| 04 - Dimensional Data Model | v0.2.0 | Completed |
| 05 - Business Financial Assumptions | v0.1.1 | Completed |
| 06 - Dataset Design Specification | v0.2.0 | Completed |
| 07 - Data Dictionary | v0.1.0 | Draft |

---

## Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| v0.1.0 | 14 July 2026 | Alyssa Ribeiro | Initial draft containing dimension definitions, including DimSalesChannel. |
| v0.1.0 | 13 July 2026 | Alyssa Ribeiro | Initial draft containing dimension tables and field definitions. |