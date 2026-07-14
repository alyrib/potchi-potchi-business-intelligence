# 03. Data Requirements Document

**Project:** Potchi Potchi Business Intelligence  
**Document:** Data Requirements Document (DRD)  
**Version:** v0.4.0  
**Author:** Alyssa da Silva Ribeiro  
**Last Updated:** 13 July 2026  
**Status:** Draft

---

# Table of Contents

1. Purpose
2. Business Questions
3. Required Datasets
4. Data Sources
5. Dataset Specifications 
6. Data Granularity
7. Data Quality Requirements
8. Refresh Frequency
9. Data Relationships
10. Data Assumptions
11. Appendix

---

# 1. Purpose

The purpose of this document is to define all datasets, fields and data quality requirements necessary to support the Business Intelligence solution described in the Business Requirements Document.

This document serves as the bridge between business requirements and data modelling.

---

# 2. Business Questions

The proposed Business Intelligence solution must answer the following questions.

| Business Question | Required Dataset(s) |
|-------------------|--------------------|
| Is the business profitable? | Orders, Order Items, Expenses |
| Which products sell the most? | Order Items, Products |
| Which brands generate the highest profit? | Products, Order Items |
| Which collections perform best? | Products, Order Items |
| Which customers purchase most frequently? | Customers, Orders |
| What is the current inventory value? | Inventory, Products |
| Which products should be reordered? | Inventory, Order Items |
| When should external storage be rented? | Inventory, Expenses |
| When is Brazil expansion financially viable? | Orders, Expenses, Inventory |

---

# 3. Required Datasets

The Business Intelligence solution will require the following datasets.

| Dataset | Purpose |
|----------|---------|
| Customers | Customer information |
| Products | Product catalogue |
| Orders | Order header information |
| Order Items | Individual products sold within each order |
| Purchases | Product acquisition and landed-cost transactions |
| Inventory | Inventory management |
| Expenses | Business operating expenses |
| Suppliers | Supplier information |
| Sales Channels | Sales-channel attributes, ownership and platform fee rules |
| Calendar | Date dimension |
| Vendors | Service providers and non-inventory business payees |
| Expense Categories | Standardised operating-expense classifications |

---

# 4. Data Sources

Since this project represents a fictional business, all datasets will be manually created to simulate realistic business operations.

Future versions of the project may replace simulated datasets with data imported directly from:

- Shopify
- WooCommerce
- Stripe
- PayPal
- Google Analytics
- Inventory Management Systems

---

# 5. Dataset Specifications

## Customers

### Purpose

Stores customer information.

### Required Fields

| Field | Data Type | Required |
|---------|-----------|----------|
| CustomerID | Integer | Yes |
| FirstName | Text | Yes |
| LastName | Text | Yes |
| Email | Text | Yes |
| Country | Text | Yes |
| City | Text | Yes |
| RegistrationDate | Date | Yes |

---

## Products

### Purpose

Stores all products available for sale.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| ProductID | Integer | Yes |
| ProductName | Text | Yes |
| Brand | Text | Yes |
| Collection | Text | Yes |
| Character | Text | Yes |
| Category | Text | Yes |
| MSRP | Decimal | No |
| ReleaseYear | Integer | No |
| Rarity | Text | Yes |
| Material | Text | No |
| RecommendedAge | Text | No |
| IsBlindBox | Boolean | Yes |
| ProductStatus | Text | Yes |
| IsExclusive | Boolean | Yes |
| IsLimitedEdition | Boolean | Yes |
| SupplierID | Integer | Yes |

---

## Order Items

### Purpose

Stores each product sold within an order.

One row represents one product line within one customer order. Historical transaction values are preserved to ensure that price changes and discounts do not alter previous sales results.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| OrderItemID | Integer | Yes |
| OrderID | Integer | Yes |
| ProductID | Integer | Yes |
| Quantity | Integer | Yes |
| ListUnitPrice | Decimal | Yes |
| UnitDiscountAmount | Decimal | Yes |
| NetUnitPrice | Decimal | Yes |
| UnitCostAtSale | Decimal | Yes |

---

## Order Items

### Purpose

Stores every product sold within each order.

One row represents one product sold.

Historical transaction values are preserved within this dataset to ensure accurate financial reporting even if product prices change in the future.

### Required Fields

| Field | Data Type | Required |
|---------|-----------|----------|
| OrderItemID | Integer | Yes |
| OrderID | Integer | Yes |
| ProductID | Integer | Yes |
| Quantity | Integer | Yes |
| UnitPrice | Decimal | Yes |

---

## Purchases

### Purpose

Stores product acquisition transactions from suppliers.

One row represents one product purchased within a supplier purchase order. This dataset preserves historical acquisition costs, exchange rates, freight charges and import-related costs.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| PurchaseLineID | Integer | Yes |
| PurchaseOrderID | Integer | Yes |
| PurchaseDate | Date | Yes |
| SupplierID | Integer | Yes |
| ProductID | Integer | Yes |
| QuantityPurchased | Integer | Yes |
| UnitCostOriginalCurrency | Decimal | Yes |
| CurrencyCode | Text | Yes |
| ExchangeRateToGBP | Decimal | Yes |
| UnitCostGBP | Decimal | Yes |
| FreightCostAllocated | Decimal | Yes |
| ImportDutyAllocated | Decimal | Yes |
| OtherLandedCostAllocated | Decimal | No |
| TotalLandedCost | Decimal | Yes |

---

## Inventory

### Purpose

Stores inventory information.

### Required Fields

| Field | Data Type | Required |
|---------|-----------|----------|
| ProductID | Integer | Yes |
| CurrentStock | Integer | Yes |
| ReorderPoint | Integer | Yes |
| SafetyStock | Integer | Yes |
| LastRestockDate | Date | Yes |

---

## Expenses

### Purpose

Stores non-inventory operating-expense transactions.

One row represents one business expense transaction.

Product purchases, freight, import duties and other directly attributable inventory-acquisition costs must not be recorded within this dataset, as they belong to the Purchases dataset.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| ExpenseID | Integer | Yes |
| ExpenseDate | Date | Yes |
| ExpenseCategoryID | Integer | Yes |
| VendorID | Integer | Yes |
| ExpenseDescription | Text | Yes |
| ExpenseAmountOriginalCurrency | Decimal | Yes |
| CurrencyCode | Text | Yes |
| ExchangeRateToGBPAtPayment | Decimal | Yes |
| ExpenseAmountGBP | Decimal | Yes |
| PaymentMethod | Text | Yes |
| ExpenseStatus | Text | Yes |

Note: Inventory acquisition costs must not be recorded within Expenses, as they are captured separately within the Purchases dataset. Expenses contains only non-inventory operating costs.

---

## Suppliers

### Purpose

Stores supplier information.

### Required Fields

| Field | Data Type | Required |
|---------|-----------|----------|
| SupplierID | Integer | Yes |
| SupplierName | Text | Yes |
| Country | Text | Yes |
| ContactEmail | Text | No |

---

## Sales Channels

### Purpose

Stores the sales channels through which customer orders are placed.

One row represents one approved sales channel. The dataset centralises channel attributes and fee rules used for profitability analysis.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| SalesChannelID | Integer | Yes |
| SalesChannelName | Text | Yes |
| ChannelType | Text | Yes |
| IsOwnedChannel | Boolean | Yes |
| IsMarketplace | Boolean | Yes |
| PlatformFeeRate | Decimal | Yes |
| LaunchDate | Date | Yes |
| ChannelStatus | Text | Yes |

---

## Vendors

### Purpose

Stores information about service providers and non-inventory business payees.

Vendors provide operational services to Potchi Potchi but do not supply products intended for resale.

Examples include Shopify, Meta, Shurgard, Canva and utility providers.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| VendorID | Integer | Yes |
| VendorName | Text | Yes |
| VendorCategory | Text | Yes |
| Country | Text | Yes |
| DefaultCurrencyCode | Text | Yes |
| VendorStatus | Text | Yes |

---

## Expense Categories

### Purpose

Stores standardised business-expense classifications.

Each category describes the nature, behaviour and recurrence of an operating expense.

### Required Fields

| Field | Data Type | Required |
|-------|-----------|----------|
| ExpenseCategoryID | Integer | Yes |
| ExpenseCategoryName | Text | Yes |
| ExpenseType | Text | Yes |
| IsFixed | Boolean | Yes |
| IsRecurring | Boolean | Yes |
| IsDiscretionary | Boolean | Yes |

---

## Calendar

### Purpose

Provides the Date Dimension required for time intelligence calculations.

### Required Fields

| Field | Data Type |
|---------|-----------|
| Date | Date |
| Day | Integer |
| Month | Integer |
| Month Name | Text |
| Quarter | Text |
| Year | Integer |
| Week Number | Integer |

---

# 6. Data Granularity

Data granularity defines the level of detail stored within each dataset.

Establishing the correct level of granularity is essential to ensure accurate reporting, prevent duplicate aggregations and support a scalable dimensional model within Power BI.

| Dataset | Granularity | Description |
|----------|-------------|-------------|
| Customers | One row per customer | Each record represents a unique customer. |
| Products | One row per product | Each record represents a unique product available for sale. |
| Orders | One row per order | Each record represents a completed customer order. |
| Order Items | One row per product sold | Each record represents a single product included within an order. Multiple records may belong to the same order. |
| Purchases | One row per product purchased within a supplier purchase order | Each record represents one product acquisition line with its historical purchase and landed costs. |
| Inventory | One row per product | Each record represents the current inventory status of a product. |
| Expenses | One row per operating-expense transaction | Each record represents one non-inventory business expense paid or planned by Potchi Potchi. |
| Suppliers | One row per supplier | Each record represents a supplier providing products to the business. |
| Sales Channels | One row per sales channel | Each record represents one approved channel through which orders may be placed. |
| Calendar | One row per calendar date | Each record represents a unique calendar day used for time intelligence calculations. |
| Vendors | One row per vendor | Each record represents one operational service provider or non-inventory payee. |
| Expense Categories | One row per expense category | Each record represents one standardised operating-expense classification. |

---

### Granularity Principles

The following principles should be maintained throughout the project:

- Each dataset must have a clearly defined level of detail.
- No dataset should contain duplicate business entities.
- Transactional datasets (such as **Order Items**) should preserve historical values and should not be overwritten when business data changes.
- Master datasets (such as **Products** and **Customers**) represent the latest known information about each entity.
- Relationships between datasets must preserve referential integrity while supporting accurate analytical reporting.

---

# 7. Data Quality Requirements

The following business rules must always be respected.

- CustomerID must be unique.
- ProductID must be unique.
- SupplierID must be unique.
- OrderID must be unique.
- OrderItemID must be unique.
- Quantity cannot be negative.
- UnitPrice cannot be negative.
- ShippingCost cannot be negative.
- CurrentStock cannot be negative.
- Dates cannot be empty.
- Every OrderItem must reference an existing Order.
- Every Product must reference an existing Supplier.
- QuantityPurchased must be greater than zero.
- UnitCostGBP cannot be negative.
- ExchangeRateToGBP must be greater than zero.
- TotalLandedCost cannot be negative.
- Every purchase must reference an existing Product and Supplier.
- SalesChannelID must be unique.
- PlatformFeeRate must be between 0 and 1.
- SalesChannelName cannot be empty.
- ChannelStatus must be Active, Planned or Inactive.
- Every order must reference an existing sales channel.
- Inventory purchases must not also be recorded as operating expenses.
- NetUnitPrice must equal ListUnitPrice minus UnitDiscountAmount.
- VendorID must be unique.
- VendorName cannot be empty.
- VendorStatus must be Active, On Hold or Inactive.
- ExpenseCategoryID must be unique.
- ExpenseCategoryName cannot be empty.
- Every expense must reference an existing Vendor and Expense Category.
- ExpenseAmountOriginalCurrency cannot be negative.
- ExchangeRateToGBPAtPayment must be greater than zero.
- ExpenseAmountGBP cannot be negative.
- Inventory-acquisition costs must not be recorded within Expenses.

---

# 8. Refresh Frequency

| Dataset | Refresh Frequency |
|----------|-------------------|
| Orders | Daily |
| Order Items | Daily |
| Inventory | Daily |
| Expenses | Monthly |
| Products | Weekly |
| Customers | Daily |
| Calendar | Static |

---

# 9. Data Relationships

The datasets will be connected using the following primary relationships.

| Parent Table | Child Table | Key |
|---|---|---|
| Customers | Orders | CustomerID |
| Orders | Order Items | OrderID |
| Products | Order Items | ProductID |
| Suppliers | Products | SupplierID |
| Products | Inventory Snapshot | ProductID |
| Calendar | Orders | OrderDateKey |
| Suppliers | Purchases | SupplierID |
| Sales Channels | Orders | SalesChannelID |
| Products | Purchases | ProductID |
| Calendar | Purchases | PurchaseDateKey |
| Vendors | Expenses | VendorID |
| Expense Categories | Expenses | ExpenseCategoryID |

These relationships will later be implemented within the Power BI semantic model.

---

# 10. Data Assumptions

The following assumptions apply.

- All orders are completed successfully.
- Inventory movements are recorded accurately.
- Product prices stored in Products represent current selling prices.
- Historical sales prices are preserved in Order Items.
- Shipping costs are recorded at order level.
- Business expenses are recorded monthly.

---

# 11. Appendix

## Related Documents

| Document | Version | Status |
|----------|---------|--------|
| 01 - Market Research | v0.1.0 | Completed |
| 02 - Business Requirements Document | v0.1.0 | Draft |
| 03 - Data Requirements Document | v0.1.0 | Draft |
| 04 - Data Dictionary | Planned | Planned |

---

## Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| v0.4.0 | 14 July 2026 | Alyssa Ribeiro | Added Vendors and Expense Categories datasets and revised the expense architecture. |
| v0.3.0 | 14 July 2026 | Alyssa Ribeiro | Added the Sales Channels dataset and platform-fee requirements. |
| v0.2.0 | 13 July 2026 | Alyssa Ribeiro | Added product purchasing fact table and separated product attributes, purchase costs and historical sales values. |
| v0.1.0 | 13 July 2026 | Alyssa da Silva Ribeiro | Initial draft. |

---

## References

This document is based on the business requirements defined for the Potchi Potchi Business Intelligence project.