# 07. Data Dictionary

**Project:** Potchi Potchi Business Intelligence  
**Document:** Data Dictionary  
**Version:** v0.2.0  
**Author:** Alyssa da Silva Ribeiro  
**Last Updated:** 14 July 2026  
**Status:** Completed

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Naming Standards](#2-naming-standards)
3. [Data Type Standards](#3-data-type-standards)
4. [DimDate](#4-dimdate)
5. [DimCustomer](#5-dimcustomer)
6. [DimProduct](#6-dimproduct)
7. [DimSupplier](#7-dimsupplier)
8. [DimSalesChannel](#8-dimsaleschannel)
9. [DimVendor](#13-dimvendor)
10. [DimExpenseCategory](#14-dimexpensecategory)
11. [FactOrders](#9-factorders)
12. [FactSales](#10-factsales)
13. [FactPurchases](#11-factpurchases)
14. [FactInventorySnapshot](#12-factinventorysnapshot)
15. [FactExpenses](#15-factexpenses)
16. [Version Control](#16-version-control)

---

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
Amazon Marketplace
```

## Potential ChannelType values include

- Owned E-commerce
- Social Commerce
- Social Referral
- Marketplace

## Business Rules

- `SalesChannelID` must be unique.
- `SalesChannelName` cannot be empty.
- `PlatformFeeRate` must be between 0 and 1.
- `LaunchDate` cannot occur after the date of an order using that channel.
- `ChannelStatus` must be Active, Planned or Inactive.
- FactOrders[SalesChannelID] must reference an existing sales channel.
- `PreferredChannel` in `DimCustomer` represents customer preference and must not replace the transactional sales channel.
- The current platform fee rate is stored within `DimSalesChannel`.
- The historical platform fee amount charged on a completed sale must be preserved within `FactSales`.

---

# 9. DimVendor

## Description

Stores descriptive attributes for operational service providers and non-inventory business payees.

The table contains one row per vendor.

Vendors differ from suppliers because they provide business services rather than merchandise intended for resale.

Examples include Shopify, Meta, Canva, Shurgard and utility providers.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| VendorID | Integer | No | Unique vendor identifier. | 1 | Primary key and relationship with `FactExpenses` |
| VendorName | Text | No | Vendor or service-provider name. | Shopify | Vendor-level expense analysis |
| VendorCategory | Text | No | High-level vendor classification. | E-commerce Platform | Vendor segmentation |
| Country | Text | No | Country in which the vendor operates or invoices Potchi Potchi. | United Kingdom | Geographic and currency-risk analysis |
| DefaultCurrencyCode | Text | No | Default three-letter invoicing currency. | GBP | Currency analysis |
| VendorStatus | Text | No | Current vendor status. | Active | Vendor filtering and operational analysis |

## Business Rules

- `VendorID` must be unique.
- `VendorName` cannot be empty.
- `DefaultCurrencyCode` must use a valid three-letter currency code.
- `VendorStatus` must be `Active`, `On Hold` or `Inactive`.
- Vendors must not include organisations that provide merchandise intended for resale.
- Every expense must reference an existing vendor.
- Vendor spending totals must be calculated from `FactExpenses`.

---

# 10. DimExpenseCategory

## Description

Stores standardised classifications for non-inventory operating expenses.

The table contains one row per expense category.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| ExpenseCategoryID | Integer | No | Unique expense-category identifier. | 3 | Primary key and relationship with `FactExpenses` |
| ExpenseCategoryName | Text | No | Standardised expense classification. | Marketing | Expense-category analysis |
| ExpenseType | Text | No | High-level accounting or operational classification. | Operating Expense | Expense-type analysis |
| IsFixed | Boolean | No | Indicates whether the expense is generally fixed. | False | Fixed versus variable cost analysis |
| IsRecurring | Boolean | No | Indicates whether the expense normally repeats. | True | Recurring-cost analysis |
| IsDiscretionary | Boolean | No | Indicates whether the expense can generally be reduced or postponed. | True | Cost-reduction and scenario analysis |

## Initial Expense Categories

Potential values include:

```text
Marketing
Software
Website and Domain
Storage
Packaging
Accounting
Insurance
Utilities
Professional Services
```

## Business Rules

- `ExpenseCategoryID` must be unique.
- `ExpenseCategoryName` cannot be empty.
- Every expense must reference an existing expense category.
- Inventory purchases must not be classified as operating expenses.
- Platform fees must not be classified as operating expenses because they are transaction-level selling costs.

---

# 11. FactOrders

## Description

Stores order-level transactional information for customer purchases placed through Potchi Potchi sales channels.

The table contains one row per customer order.

`FactOrders` records information that applies to the order as a whole, including customer, order dates, sales channel, payment method, shipping details, order-level discounts and gift-wrapping selection.

Product-level sales values are stored separately within `FactSales`.

Returns and refunds are stored separately within `FactReturns`.

## Granularity

**One row per customer order.**

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| OrderID | Integer | No | Unique order identifier. | 500001 | Primary key, order counting and order-level analysis |
| CustomerID | Integer | No | Identifier of the customer who placed the order. | 1001 | Relationship with `DimCustomer` |
| OrderDateKey | Integer | No | Date on which the order was placed, stored in `YYYYMMDD` format. | 20260714 | Active relationship with `DimDate` and order-date analysis |
| ShippedDateKey | Integer | Yes | Date on which the order was dispatched, stored in `YYYYMMDD` format. | 20260716 | Processing-time and fulfilment analysis |
| DeliveredDateKey | Integer | Yes | Date on which the order was delivered, stored in `YYYYMMDD` format. | 20260718 | Delivery-time and logistics analysis |
| SalesChannelID | Integer | No | Identifier of the sales channel through which the order was placed. | 2 | Relationship with `DimSalesChannel` |
| OrderStatus | Text | No | Current order lifecycle status. | Delivered | Order fulfilment and cancellation analysis |
| PaymentMethod | Text | No | Payment method selected by the customer. | PayPal | Payment-method analysis |
| ShippingMethod | Text | No | Delivery service or shipping option used for the order. | Royal Mail Tracked 48 | Shipping and carrier analysis |
| DiscountCode | Text | Yes | Promotional code applied to the order, when applicable. | WELCOME10 | Promotion and campaign analysis |
| OrderDiscountAmount | Decimal | No | Total discount applied at order level, excluding line-level product discounts. | 5.00 | Order-level discount and profitability calculations |
| ShippingRevenue | Decimal | No | Amount charged to the customer for shipping. | 3.99 | Shipping revenue and order-profitability analysis |
| ShippingCost | Decimal | No | Actual shipping amount paid by Potchi Potchi. | 4.65 | Shipping-cost and fulfilment-margin analysis |
| GiftWrapping | Boolean | No | Indicates whether the customer requested gift wrapping. | True | Gift-service demand analysis |
| OrderCurrency | Text | No | Three-letter currency code used for the transaction. | GBP | Currency filtering and future international expansion |

## Date Relationships

`OrderDateKey` will be the primary active relationship between `FactOrders` and `DimDate`.

`ShippedDateKey` and `DeliveredDateKey` may be implemented as inactive relationships within the Power BI semantic model and activated within specific DAX measures when analysing fulfilment and delivery timelines.

## Order Status Values

Approved `OrderStatus` values may include:

```text
Pending
Processing
Shipped
Delivered
Cancelled
```

Returns should not be represented through `OrderStatus`, because return requests and refunds belong to the separate `FactReturns` business process.

## Payment Method Values

Initial approved values may include:

```text
Visa
Mastercard
PayPal
Apple Pay
Google Pay
```

## Shipping Method Values

Initial approved values may include:

```text
Royal Mail Tracked 24
Royal Mail Tracked 48
DPD Next Day
Evri Standard
```

## Derived Measures and Attributes

The following values should be calculated rather than stored directly in `FactOrders`:

| Derived Value | Calculation Source | Purpose |
|---|---|---|
| Total Orders | Count of `OrderID` | Order-volume analysis |
| Order Revenue | Related `FactSales` records plus shipping revenue and order-level adjustments | Revenue analysis |
| Average Order Value | Total order revenue divided by total orders | Customer-spend analysis |
| Processing Days | Difference between `OrderDateKey` and `ShippedDateKey` | Fulfilment performance |
| Delivery Days | Difference between `ShippedDateKey` and `DeliveredDateKey` | Carrier and delivery performance |
| IsFirstOrder | Earliest order placed by each customer | New-customer analysis |
| Shipping Margin | `ShippingRevenue` minus `ShippingCost` | Shipping profitability |

## Business Rules

- `OrderID` must be unique.
- Every order must reference an existing customer.
- Every order must reference an existing sales channel.
- `OrderDateKey` is mandatory.
- `ShippedDateKey` cannot occur before `OrderDateKey`.
- `DeliveredDateKey` cannot occur before `ShippedDateKey`.
- Orders with a status of `Pending`, `Processing` or `Cancelled` may have blank shipping and delivery dates.
- `OrderDiscountAmount` cannot be negative.
- `ShippingRevenue` cannot be negative.
- `ShippingCost` cannot be negative.
- `OrderCurrency` must use a valid three-letter currency code.
- `DiscountCode` may be blank when no order-level promotion was applied.
- Every completed order must contain at least one related record in `FactSales`.
- Product-level discounts must not be stored within `OrderDiscountAmount`.
- Product-level selling prices and quantities must be stored within `FactSales`.
- Platform fee amounts must be stored within `FactSales`.
- Returns and refunds must be recorded separately within `FactReturns`.
- `PreferredChannel` in `DimCustomer` must not replace the transactional `SalesChannelID`.

---

# 12. FactSales

## Description

Stores product-level sales transactions completed through Potchi Potchi customer orders.

The table contains one row per product line sold within an order.

`FactSales` preserves the historical selling price, product-level discount, cost assigned at the time of sale, platform fee and VAT amount associated with each transaction.

Order-level information such as customer, sales channel, shipping, payment method and order-wide discounts is stored separately within `FactOrders`.

For sealed blind boxes, the table records the commercial SKU purchased by the customer. It does not assume or infer which hidden variant was received.

## Granularity

**One row per product sold within a customer order.**

A single order may therefore contain multiple `FactSales` records.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| OrderItemID | Integer | No | Unique identifier for the product line within an order. | 900001 | Primary key and sales-line counting |
| OrderID | Integer | No | Identifier of the customer order containing the product line. | 500001 | Links the sales line to `FactOrders` |
| ProductID | Integer | No | Identifier of the commercial product or SKU sold. | 2001 | Relationship with `DimProduct` |
| Quantity | Integer | No | Number of units sold within the order line. | 2 | Units-sold and revenue calculations |
| UnitRetailPrice | Decimal | No | Listed selling price per unit at the time of the transaction, before product-level discount. | 18.00 | Historical pricing and discount analysis |
| UnitDiscountAmount | Decimal | No | Product-level discount applied to each unit. | 2.00 | Promotion and discount analysis |
| NetUnitPrice | Decimal | No | Final selling price per unit after the product-level discount. | 16.00 | Net sales and revenue calculations |
| UnitCostAtSale | Decimal | No | Historical inventory cost assigned to each unit at the time of sale. | 7.50 | Cost of Goods Sold and gross-profit calculations |
| PlatformFeeAmount | Decimal | No | Actual sales-channel fee allocated to the order line. | 1.60 | Channel cost and profitability analysis |
| VATAmount | Decimal | No | VAT amount associated with the sales line. | 5.33 | Tax and net-revenue analysis |

## Pricing Definitions

The monetary fields represent different stages of the transaction.

| Field | Meaning |
|---|---|
| `UnitRetailPrice` | Price advertised by Potchi Potchi at the time of sale |
| `UnitDiscountAmount` | Discount applied to one unit of the product |
| `NetUnitPrice` | Amount charged per unit after the product-level discount |
| `UnitCostAtSale` | Historical cost assigned to one unit when it was sold |
| `PlatformFeeAmount` | Sales-channel fee charged for the completed transaction |
| `VATAmount` | VAT included in or attributable to the sales line |

`MSRP` remains within `DimProduct` as the manufacturer’s suggested retail-price reference and must not replace the historical transaction price.

## Calculated Values

The following financial values should be calculated rather than stored directly.

| Calculated Value | Calculation | Purpose |
|---|---|---|
| Gross Line Revenue | `Quantity × UnitRetailPrice` | Revenue before product-level discount |
| Line Discount Amount | `Quantity × UnitDiscountAmount` | Total product discount for the sales line |
| Net Sales Amount | `Quantity × NetUnitPrice` | Revenue after product-level discount |
| Cost of Goods Sold | `Quantity × UnitCostAtSale` | Historical inventory cost of units sold |
| Gross Profit | `Net Sales Amount − Cost of Goods Sold` | Product-level profitability |
| Gross Margin | `Gross Profit ÷ Net Sales Amount` | Product-level margin percentage |
| Net Revenue Before Other Order Costs | `Net Sales Amount − VATAmount − PlatformFeeAmount` | Revenue after tax and platform fee |
| Average Selling Price | `Net Sales Amount ÷ Quantity` | Average realised selling price |

Order-level discounts, shipping revenue and shipping costs remain within `FactOrders` and must not be duplicated within `FactSales`.

## Blind Box Treatment

For sealed blind-box products, `ProductID` represents the commercial SKU purchased by the customer.

Example:

```text
DIMOO Aquarium Blind Box
```

The transaction must not be recorded as a specific hidden variant unless the customer later provides that information through a separate service such as the Potchi Passport or Swap Club.

### Blind Box Rules

- `FactSales` records the SKU sold by Potchi Potchi.
- The hidden character or variant received by the customer must not be inferred.
- Batch numbers, box positions, weights or unofficial identification methods must not be treated as reliable variant data.
- Customer-submitted variant information, when available, must be stored in a separate future dataset.
- A duplicate hidden character does not alter the original sales transaction.

## Historical Cost Treatment

`UnitCostAtSale` preserves the cost assigned to inventory when the product was sold.

The value is derived from purchasing and inventory valuation records and is stored within `FactSales` to ensure that historical profit remains stable when supplier prices, exchange rates, freight charges or import duties change.

The current or most recent acquisition cost must not overwrite historical values.

## Platform Fee Treatment

The current platform fee rate is stored within `DimSalesChannel`.

The actual platform fee charged on each completed transaction is preserved within `FactSales[PlatformFeeAmount]`.

This separation ensures that historical channel profitability does not change when a platform updates its fee structure.

## Business Rules

- `OrderItemID` must be unique.
- Every sales record must reference an existing order.
- Every sales record must reference an existing product.
- `Quantity` must be greater than zero.
- `UnitRetailPrice` cannot be negative.
- `UnitDiscountAmount` cannot be negative.
- `UnitDiscountAmount` cannot exceed `UnitRetailPrice`.
- `NetUnitPrice` must equal `UnitRetailPrice − UnitDiscountAmount`.
- `NetUnitPrice` cannot be negative.
- `UnitCostAtSale` cannot be negative.
- `PlatformFeeAmount` cannot be negative.
- `VATAmount` cannot be negative.
- A completed order must contain at least one `FactSales` record.
- Product-level discounts must be stored within `FactSales`.
- Order-level discounts must remain within `FactOrders`.
- Shipping revenue and shipping costs must remain within `FactOrders`.
- Return and refund transactions must be recorded separately within `FactReturns`.
- Product acquisition transactions must be recorded separately within `FactPurchases`.
- `ProductID` must represent the commercial SKU sold rather than an unknown blind-box variant.
- Historical prices and costs must never be overwritten by current catalogue or supplier values.

---

# 13. FactPurchases

## Description

Stores historical inventory acquisition transactions from suppliers.

The table contains one row per product purchased within a supplier purchase order.

`FactPurchases` preserves the historical purchase cost, exchange rate, allocated landed costs and receiving information associated with each inventory acquisition.

Unlike `FactSales`, which represents customer transactions, `FactPurchases` records procurement activities and supports inventory valuation, supplier analysis and profitability calculations.

Purchase orders are treated as degenerate dimensions because all relevant purchasing attributes are stored directly within the fact table.

## Granularity

**One row per product purchased within a supplier purchase order.**

A single purchase order may therefore contain multiple `FactPurchases` records.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| PurchaseLineID | Integer | No | Unique identifier for the purchase line. | 300001 | Primary key |
| PurchaseOrderID | Text | No | Purchase order identifier. | PO-2026-001 | Procurement analysis and purchase grouping |
| PurchaseDateKey | Integer | No | Purchase date stored in `YYYYMMDD` format. | 20260315 | Relationship with `DimDate` |
| SupplierID | Integer | No | Supplier providing the inventory. | 4 | Relationship with `DimSupplier` |
| ProductID | Integer | No | Product purchased from the supplier. | 2001 | Relationship with `DimProduct` |
| QuantityPurchased | Integer | No | Number of units ordered from the supplier. | 120 | Procurement-volume analysis |
| ReceivedQuantity | Integer | No | Number of units successfully received into inventory. | 118 | Supplier fulfilment analysis |
| UnitCostOriginalCurrency | Decimal | No | Unit purchase cost in the supplier's original currency. | 80.00 | Historical purchasing analysis |
| CurrencyCode | Text | No | Three-letter ISO currency code. | CNY | Currency analysis |
| ExchangeRateToGBPAtPurchase | Decimal | No | Exchange rate applied when converting the purchase into GBP. | 0.107 | Historical currency conversion |
| UnitCostGBP | Decimal | No | Historical purchase cost converted into GBP. | 8.56 | Inventory valuation |
| AllocatedFreightCost | Decimal | No | Freight cost allocated to each purchased unit. | 0.45 | Landed-cost analysis |
| ImportDutyAllocated | Decimal | No | Import duty allocated to each purchased unit. | 0.18 | Landed-cost analysis |
| OtherLandedCostAllocated | Decimal | Yes | Other allocated acquisition costs such as insurance or customs brokerage. | 0.12 | Total landed-cost analysis |
| PurchaseStatus | Text | No | Current purchase-order status. | Received | Procurement monitoring |

## Procurement Cost Structure

The complete landed cost of a purchased unit is calculated as:

```text
UnitCostGBP
+ AllocatedFreightCost
+ ImportDutyAllocated
+ OtherLandedCostAllocated
```

The total landed cost should be calculated rather than stored to avoid unnecessary redundancy.

## Purchase Status Values

Approved values may include:

```text
Ordered
In Transit
Partially Received
Received
Cancelled
```

## Calculated Values

The following values should be calculated rather than stored.

| Calculated Value | Calculation | Purpose |
|---|---|---|
| Total Purchase Cost | QuantityPurchased × UnitCostGBP | Procurement expenditure |
| Total Freight Cost | QuantityPurchased × AllocatedFreightCost | Freight analysis |
| Total Import Duty | QuantityPurchased × ImportDutyAllocated | Import-cost analysis |
| Total Other Landed Costs | QuantityPurchased × OtherLandedCostAllocated | Procurement-cost analysis |
| Total Landed Cost | QuantityPurchased × (UnitCostGBP + AllocatedFreightCost + ImportDutyAllocated + OtherLandedCostAllocated) | Inventory valuation |
| Supplier Fill Rate | ReceivedQuantity ÷ QuantityPurchased | Supplier performance |

## Historical Cost Treatment

All monetary values represent historical purchasing information.

Supplier price changes, exchange-rate fluctuations and future freight costs must never overwrite historical purchase records.

This approach guarantees stable inventory valuation and accurate historical profitability.

## Purchase Order Treatment

`PurchaseOrderID` is treated as a **degenerate dimension**.

A separate purchase-order dimension is unnecessary because all relevant procurement attributes are stored directly within `FactPurchases`.

## Business Rules

- `PurchaseLineID` must be unique.
- Every purchase line must reference an existing supplier.
- Every purchase line must reference an existing product.
- `PurchaseDateKey` is mandatory.
- `QuantityPurchased` must be greater than zero.
- `ReceivedQuantity` cannot exceed `QuantityPurchased`.
- `ReceivedQuantity` cannot be negative.
- `UnitCostOriginalCurrency` cannot be negative.
- `ExchangeRateToGBPAtPurchase` must be greater than zero.
- `UnitCostGBP` cannot be negative.
- `AllocatedFreightCost` cannot be negative.
- `ImportDutyAllocated` cannot be negative.
- `OtherLandedCostAllocated` cannot be negative.
- `CurrencyCode` must use a valid three-letter ISO currency code.
- `PurchaseStatus` must use an approved procurement status.
- Inventory acquisition costs must not be recorded within `FactExpenses`.
- Historical purchasing values must never be overwritten by current supplier prices.
- Purchase orders are represented by `PurchaseOrderID` and must not require a separate dimension table.

---

# 14. FactInventorySnapshot

## Description

Stores historical inventory positions for Potchi Potchi products.

The table contains one row per product per inventory snapshot date.

`FactInventorySnapshot` preserves the historical state of inventory, including physical stock, reserved units, damaged units, incoming stock, reorder thresholds and inventory cost.

Unlike a current-stock table, inventory snapshots allow the business to analyse how stock levels changed over time without overwriting previous values.

The initial implementation assumes that inventory is held in one active storage location at a time. Multi-location inventory remains outside the scope of version 1.

## Granularity

**One row per product per inventory snapshot date.**

Monthly snapshots will normally be recorded on the final calendar day of each month.

Additional snapshots may be recorded when a significant inventory event occurs, such as:

- a product becoming out of stock;
- a major restock;
- a substantial stock adjustment;
- a significant quantity of damaged inventory.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| InventorySnapshotID | Integer | No | Unique identifier for the inventory snapshot record. | 700001 | Primary key |
| SnapshotDateKey | Integer | No | Date on which the inventory position was recorded, stored in `YYYYMMDD` format. | 20260731 | Relationship with `DimDate` and inventory trend analysis |
| ProductID | Integer | No | Identifier of the product represented by the snapshot. | 2001 | Relationship with `DimProduct` |
| UnitsInStock | Integer | No | Total physical quantity held in inventory at the snapshot date. | 24 | Stock-level and inventory-value analysis |
| UnitsReserved | Integer | No | Quantity already allocated to customer orders but not yet dispatched. | 3 | Available-to-sell calculations |
| UnitsDamaged | Integer | No | Quantity physically held but unavailable for sale because of damage. | 1 | Damaged-stock and supplier-quality analysis |
| UnitsOnOrder | Integer | No | Quantity ordered from suppliers but not yet received. | 12 | Replenishment and incoming-stock analysis |
| ReorderPoint | Integer | No | Sellable stock level at or below which replenishment should be considered. | 8 | Reorder alert calculations |
| SafetyStock | Integer | No | Minimum stock quantity maintained to reduce stockout risk. | 5 | Safety-stock monitoring |
| AverageUnitCost | Decimal | No | Average historical inventory cost per unit at the snapshot date. | 8.42 | Inventory valuation and profitability analysis |

## Inventory Definitions

The inventory fields represent different stock states.

| Field | Meaning |
|---|---|
| `UnitsInStock` | Total physical quantity held by the business |
| `UnitsReserved` | Units committed to orders but not yet dispatched |
| `UnitsDamaged` | Units physically present but not available for sale |
| `UnitsOnOrder` | Units purchased but not yet received |
| `ReorderPoint` | Threshold used to trigger replenishment review |
| `SafetyStock` | Minimum protective stock level |
| `AverageUnitCost` | Average inventory cost assigned to one unit at the snapshot date |

## Calculated Values

The following values should be calculated rather than stored directly.

| Calculated Value | Calculation | Purpose |
|---|---|---|
| Available to Sell | `UnitsInStock − UnitsReserved − UnitsDamaged` | Quantity currently available for customer orders |
| Inventory Value | `UnitsInStock × AverageUnitCost` | Historical value of all physical inventory |
| Sellable Inventory Value | `Available to Sell × AverageUnitCost` | Value of inventory available for sale |
| Damaged Inventory Value | `UnitsDamaged × AverageUnitCost` | Financial impact of damaged stock |
| Reorder Flag | `Available to Sell <= ReorderPoint` | Identifies products requiring replenishment review |
| Safety Stock Breach | `Available to Sell < SafetyStock` | Identifies products below the minimum protective level |
| Stockout Flag | `Available to Sell = 0` | Identifies products unavailable for sale |
| Incoming Coverage | `UnitsOnOrder + Available to Sell` | Near-term expected stock availability |

## Snapshot Frequency

The initial implementation uses monthly inventory snapshots.

Snapshots should normally be recorded on the final calendar day of each month.

Additional event-based snapshots may be created when a product:

- becomes unavailable for sale;
- receives a significant restock;
- experiences a material stock adjustment;
- accumulates a significant quantity of damaged units.

Monthly snapshots provide historical inventory visibility while keeping the dataset compact and suitable for Power BI reporting.

## Historical Cost Treatment

`AverageUnitCost` represents the historical average cost of inventory held on the snapshot date.

The value may be derived from received purchasing transactions and the selected inventory valuation method.

Current supplier prices, later exchange rates or future acquisition costs must not overwrite historical inventory snapshots.

## Storage Location Scope

The first version of the project assumes that Potchi Potchi uses one active storage location at a time.

The expected operational progression is:

```text
Home Storage
    ↓
Shurgard Self Storage – Deptford
```

A storage-location field is not included because version 1 does not require simultaneous stock analysis across multiple locations.

A future `DimStorageLocation` may be introduced if the business operates:

- multiple storage units;
- simultaneous home and external inventory;
- warehouses in different regions;
- international stock locations;
- stock transfers between facilities.

International sales expansion must not automatically be interpreted as international warehouse expansion.

## Business Rules

- `InventorySnapshotID` must be unique.
- Each combination of `SnapshotDateKey` and `ProductID` must be unique.
- Every snapshot must reference an existing product.
- `SnapshotDateKey` is mandatory.
- `UnitsInStock` cannot be negative.
- `UnitsReserved` cannot be negative.
- `UnitsDamaged` cannot be negative.
- `UnitsOnOrder` cannot be negative.
- `UnitsReserved + UnitsDamaged` cannot exceed `UnitsInStock`.
- `ReorderPoint` cannot be negative.
- `SafetyStock` cannot be negative.
- `AverageUnitCost` cannot be negative.
- Monthly snapshots should normally occur on the final calendar day of the month.
- Historical snapshots must never be overwritten by current inventory values.
- Current supplier prices must not replace historical `AverageUnitCost`.
- Inventory purchases must be recorded within `FactPurchases`.
- Customer sales must be recorded within `FactSales`.
- Damaged inventory must remain included in physical stock but excluded from available-to-sell calculations.
- Storage location is excluded from version 1 because inventory is assumed to be held in one active location at a time.

---

# 15. FactExpenses

## Description

Stores non-inventory operating expense transactions incurred by Potchi Potchi during business operations.

The table contains one row per expense transaction.

`FactExpenses` records historical operating costs such as marketing, software subscriptions, storage, website hosting, professional services, insurance and utilities.

Inventory acquisition costs, freight, import duties and other directly attributable landed costs must not be stored within this table, as they belong to `FactPurchases`.

## Granularity

**One row per business expense transaction.**

Each record represents a single operating expense paid or planned by Potchi Potchi.

## Fields

| Field | Data Type | Nullable | Description | Example | Power BI Usage |
|---|---|---|---|---|---|
| ExpenseID | Integer | No | Unique expense transaction identifier. | 100001 | Primary key |
| ExpenseDateKey | Integer | No | Date on which the expense occurred, stored in `YYYYMMDD` format. | 20260714 | Relationship with `DimDate` |
| ExpenseCategoryID | Integer | No | Expense classification. | 3 | Relationship with `DimExpenseCategory` |
| VendorID | Integer | No | Service provider receiving the payment. | 7 | Relationship with `DimVendor` |
| ExpenseDescription | Text | No | Short description of the expense. | July Instagram Campaign | Expense review and auditing |
| ExpenseAmountOriginalCurrency | Decimal | No | Amount paid in the vendor's invoicing currency. | 120.00 | Historical expense analysis |
| CurrencyCode | Text | No | Three-letter ISO currency code. | GBP | Currency reporting |
| ExchangeRateToGBPAtPayment | Decimal | No | Historical exchange rate used for GBP conversion. | 1.000 | Currency conversion |
| ExpenseAmountGBP | Decimal | No | Historical expense value converted into GBP. | 120.00 | Financial reporting |
| PaymentMethod | Text | No | Method used to settle the expense. | Business Debit Card | Cash-flow analysis |
| ExpenseStatus | Text | No | Current expense status. | Paid | Outstanding-expense monitoring |

---

## Expense Categories

Examples include:

```text
Marketing
Software
Website and Domain
Storage
Packaging
Accounting
Insurance
Utilities
Professional Services
```

---

## Expense Status Values

Approved values may include:

```text
Planned
Approved
Paid
Cancelled
```

---

## Payment Method Values

Initial approved values may include:

```text
Business Debit Card
Business Credit Card
Bank Transfer
PayPal
Direct Debit
```

---

## Calculated Values

The following values should be calculated rather than stored directly.

| Calculated Value | Calculation | Purpose |
|---|---|---|
| Monthly Operating Expenses | Sum of `ExpenseAmountGBP` | Monthly financial reporting |
| Annual Operating Expenses | Sum of `ExpenseAmountGBP` | Annual financial reporting |
| Expense by Vendor | Sum of `ExpenseAmountGBP` grouped by Vendor | Vendor-spend analysis |
| Expense by Category | Sum of `ExpenseAmountGBP` grouped by Expense Category | Operating-cost analysis |
| Fixed Operating Costs | Sum where `IsFixed = True` | Fixed-cost analysis |
| Variable Operating Costs | Sum where `IsFixed = False` | Variable-cost analysis |
| Recurring Expenses | Sum where `IsRecurring = True` | Subscription and recurring-cost analysis |
| Discretionary Spending | Sum where `IsDiscretionary = True` | Scenario planning and cost optimisation |

---

## Historical Currency Treatment

All expense values represent historical financial transactions.

Historical exchange rates are preserved to ensure that financial reporting remains consistent even when future currency fluctuations occur.

Current exchange rates must never overwrite historical expense records.

---

## Expense Scope

`FactExpenses` stores only operational expenditure.

Examples include:

- Website hosting
- Shopify subscription
- Marketing campaigns
- Storage rental
- Accounting services
- Business insurance
- Utilities
- Software subscriptions

The following must **not** be stored within `FactExpenses`:

- Product purchases
- Freight associated with inventory acquisition
- Import duties
- Customs charges
- Other landed inventory costs
- Platform fees charged per customer sale

These belong to `FactPurchases` or `FactSales`, depending on the business process.

---

## Business Rules

- `ExpenseID` must be unique.
- Every expense must reference an existing vendor.
- Every expense must reference an existing expense category.
- `ExpenseDateKey` is mandatory.
- `ExpenseAmountOriginalCurrency` cannot be negative.
- `ExchangeRateToGBPAtPayment` must be greater than zero.
- `ExpenseAmountGBP` cannot be negative.
- `CurrencyCode` must use a valid three-letter ISO currency code.
- `ExpenseStatus` must use an approved expense status.
- Inventory acquisition costs must never be recorded within `FactExpenses`.
- Platform fees charged on customer sales must remain within `FactSales`.
- Product purchases must remain within `FactPurchases`.
- Historical expense values must never be overwritten by current exchange rates.

---

# Appendix

## Related Documents

| Document | Version | Status |
|----------|---------|--------|
| 01 - Market Research | Completed |
| 02 - Business Requirements Document | Completed |
| 03 - Data Requirements Document | Completed |
| 04 - Dimensional Data Model | Completed |
| 05 - Business Financial Assumptions | Completed |
| 06 - Dataset Design Specification | Completed |
| 07 - Data Dictionary | Completed |

---

## Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| v0.2.0 | 14 July 2026 | Alyssa Ribeiro | Completed the initial Data Dictionary, including all dimensions, fact tables, business rules and field definitions. |
| v0.1.0 | 14 July 2026 | Alyssa Ribeiro | Initial draft containing FactOrders definitions. |
| v0.1.0 | 14 July 2026 | Alyssa Ribeiro | Initial draft containing dimension definitions, including DimSalesChannel. |
| v0.1.0 | 13 July 2026 | Alyssa Ribeiro | Initial draft containing dimension tables and field definitions. |