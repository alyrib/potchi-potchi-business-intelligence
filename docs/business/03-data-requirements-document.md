# 03. Data Requirements Document

**Project:** Potchi Potchi Business Intelligence  
**Document:** Data Requirements Document (DRD)  
**Version:** v0.1.0  
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
| Inventory | Inventory management |
| Expenses | Business operating expenses |
| Suppliers | Supplier information |
| Calendar | Date dimension |

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
|---------|-----------|----------|
| ProductID | Integer | Yes |
| ProductName | Text | Yes |
| Brand | Text | Yes |
| Collection | Text | Yes |
| Category | Text | Yes |
| CurrentRetailPrice | Decimal | Yes |
| CurrentCostPrice | Decimal | Yes |
| SupplierID | Integer | Yes |

---

## Orders

### Purpose

Stores information related to each customer order.

One row represents one order.

### Required Fields

| Field | Data Type | Required |
|---------|-----------|----------|
| OrderID | Integer | Yes |
| CustomerID | Integer | Yes |
| OrderDate | Date | Yes |
| ShippingCost | Decimal | Yes |
| Discount | Decimal | No |
| PaymentMethod | Text | Yes |
| OrderStatus | Text | Yes |

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

Stores business operating expenses.

### Required Fields

| Field | Data Type | Required |
|---------|-----------|----------|
| ExpenseID | Integer | Yes |
| ExpenseDate | Date | Yes |
| Category | Text | Yes |
| Description | Text | Yes |
| Amount | Decimal | Yes |

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
| Inventory | One row per product | Each record represents the current inventory status of a product. |
| Expenses | One row per expense transaction | Each record represents a single business expense. |
| Suppliers | One row per supplier | Each record represents a supplier providing products to the business. |
| Calendar | One row per calendar date | Each record represents a unique calendar day used for time intelligence calculations. |

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
|--------------|------------|-----|
| Customers | Orders | CustomerID |
| Orders | Order Items | OrderID |
| Products | Order Items | ProductID |
| Suppliers | Products | SupplierID |
| Products | Inventory | ProductID |
| Calendar | Orders | OrderDate |

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
| v0.1.0 | 13 July 2026 | Alyssa da Silva Ribeiro | Initial draft. |

---

## References

This document is based on the business requirements defined for the Potchi Potchi Business Intelligence project.