# 06. Dataset Design Specification

**Project:** Potchi Potchi Business Intelligence  
**Document:** Dataset Design Specification  
**Version:** v0.3.0  
**Author:** Alyssa da Silva Ribeiro  
**Last Updated:** 13 July 2026  
**Status:** Draft

---

# Table of Contents

1. Purpose
2. Design Principles
3. Dataset Overview
4. Dataset Specifications
5. Dataset Relationships
6. Dataset Naming Convention
7. Storage Structure
8. Future Improvements
9. Appendix

---

# 1. Purpose

This document defines the design specifications for every dataset that will support the Potchi Potchi Business Intelligence solution.

Unlike the Data Dictionary, which describes individual fields, this document focuses on dataset architecture, expected volumes, granularity, storage conventions and refresh strategy.

The objective is to establish a consistent blueprint before dataset creation begins.

---

# 2. Design Principles

The following principles guide dataset design throughout this project.

- Each dataset has a single business purpose.
- Every dataset has a clearly defined level of granularity.
- Fact and Dimension tables remain separated.
- Historical values are preserved whenever required.
- Primary and foreign keys ensure referential integrity.
- Dataset sizes should remain realistic for a small business operating over a two-year period.
- Synthetic data should reflect plausible business behaviour rather than randomly generated values.

---

# 3. Dataset Overview

The project will contain eight primary datasets.

| Dataset | Table Type | Expected Rows |
|----------|------------|--------------:|
| Calendar | Dimension | 731 |
| Customers | Dimension | 1,500 |
| Products | Dimension | 120 |
| Suppliers | Dimension | 12 |
| Orders | Fact | 6,000 |
| Order Items / FactSales | Fact | 15,000–18,000 |
| Purchases | Fact | 500–800 |
| Sales Channels | Dimension | 3–5 |
| Inventory Snapshot | Fact | 1,440 |
| Expenses | Fact | 250 |

The expected dataset volume represents approximately two years of business activity.

---

# 4. Dataset Specifications

## Calendar.csv

**Purpose**

Stores the complete date dimension used throughout the Power BI semantic model.

| Property | Value |
|----------|-------|
| Table Type | Dimension |
| Granularity | One row per calendar day |
| Expected Rows | 731 |
| Refresh | Static |
| Primary Key | DateKey |
| Used By | All Fact Tables |

---

## Customers.csv

**Purpose**

Stores customer information.

| Property | Value |
|----------|-------|
| Table Type | Dimension |
| Granularity | One row per customer |
| Expected Rows | 1,500 |
| Refresh | Daily |
| Primary Key | CustomerID |
| Used By | Orders, FactSales |

---

## Products.csv

**Purpose**

Stores the product catalogue.

| Property | Value |
|----------|-------|
| Table Type | Dimension |
| Granularity | One row per product |
| Expected Rows | 120 |
| Refresh | Weekly |
| Primary Key | ProductID |
| Foreign Key | SupplierID |
| Used By | FactSales, Inventory Snapshot |

---

## Suppliers.csv

**Purpose**

Stores supplier information.

| Property | Value |
|----------|-------|
| Table Type | Dimension |
| Granularity | One row per supplier |
| Expected Rows | 12 |
| Refresh | Monthly |
| Primary Key | SupplierID |
| Used By | Products, Expenses |

---

## SalesChannels.csv

**Purpose**

Stores approved sales channels and their commercial attributes.

| Property | Value |
|----------|-------|
| Table Type | Dimension |
| Granularity | One row per sales channel |
| Expected Rows | 3–5 |
| Refresh | When a channel or fee rule changes |
| Primary Key | SalesChannelID |
| Used By | FactOrders and channel-profitability analysis |

### Notes

The dimension stores the current platform fee rate and channel classification.

Historical fee amounts charged on completed sales are preserved within `FactSales` so that past profitability does not change when platform rates are updated.

---

## Orders.csv

**Purpose**

Stores customer orders.

| Property | Value |
|----------|-------|
| Table Type | Fact |
| Granularity | One row per order |
| Expected Rows | 6,000 |
| Refresh | Daily |
| Primary Key | OrderID |
| Used By | Power BI Measures |

---

## OrderItems.csv

**Purpose**

Stores products sold within each order.

| Property | Value |
|----------|-------|
| Table Type | Fact |
| Granularity | One row per product sold |
| Expected Rows | 15,000–18,000 |
| Refresh | Daily |
| Primary Key | OrderItemID |
| Foreign Keys | OrderID, ProductID |
| Used By | Revenue Analysis |

---

## Purchases.csv

**Purpose**

Stores historical product acquisition transactions and landed costs.

| Property | Value |
|----------|-------|
| Table Type | Fact |
| Granularity | One row per product purchased within a supplier purchase order |
| Expected Rows | 500–800 |
| Refresh | Per purchase transaction |
| Primary Key | PurchaseLineID |
| Foreign Keys | ProductID, SupplierID, DateKey |
| Degenerate Dimension | PurchaseOrderID |
| Used By | Procurement, inventory valuation, supplier and profitability analysis |

### Notes

Purchase costs must be preserved historically.

Inventory acquisition must not also be recorded within Expenses. Freight, import duties and other landed costs associated directly with a product purchase are allocated within this dataset.

---

## InventorySnapshot.csv

**Purpose**

Stores historical inventory levels.

| Property | Value |
|----------|-------|
| Table Type | Fact |
| Granularity | One row per product per monthly snapshot |
| Expected Rows | 1,440 |
| Refresh | Monthly |
| Primary Key | InventorySnapshotID |
| Foreign Key | ProductID |
| Used By | Inventory Dashboard |

---

## Expenses.csv

**Purpose**

Stores operating expenses.

| Property | Value |
|----------|-------|
| Table Type | Fact |
| Granularity | One row per expense transaction |
| Expected Rows | 250 |
| Refresh | Monthly |
| Primary Key | ExpenseID |
| Used By | Financial Dashboard |

---

# 5. Dataset Relationships

The datasets are connected through primary and foreign keys.

| Parent | Child | Key |
|----------|---------|-----|
| Calendar | Orders | DateKey |
| Calendar | Order Items | DateKey |
| Calendar | Inventory Snapshot | DateKey |
| Calendar | Expenses | DateKey |
| Customers | Orders | CustomerID |
| Products | Order Items | ProductID |
| Suppliers | Products | SupplierID |
| Calendar | Purchases | DateKey |
| Products | Purchases | ProductID |
| Suppliers | Purchases | SupplierID |
| Sales Channels | Orders | SalesChannelID |

Referential integrity should always be maintained.

---

# 6. Dataset Naming Convention

Datasets follow a consistent naming convention.

| Dataset | File Name |
|----------|-----------|
| Calendar | Calendar.csv |
| Customers | Customers.csv |
| Products | Products.csv |
| Suppliers | Suppliers.csv |
| Orders | Orders.csv |
| Order Items | OrderItems.csv |
| Inventory Snapshot | InventorySnapshot.csv |
| Expenses | Expenses.csv |
| Purchases | Purchases.csv |
| Sales Channels | SalesChannels.csv |

---

# 7. Storage Structure

Datasets will be stored using CSV format.

Recommended folder structure:

data/
├── raw/
├── processed/
└── reference/

Future versions may incorporate automated ETL pipelines.

---

# 8. Future Improvements

Future enhancements may include:

- Automated dataset generation
- SQL database integration
- Incremental refresh
- API integrations
- Cloud storage
- Data warehouse migration

---

# 9. Appendix

## Related Documents

| Document | Version | Status |
|----------|---------|--------|
| 01 - Market Research | v0.1.0 | Completed |
| 02 - Business Requirements Document | v0.1.0 | Completed |
| 03 - Data Requirements Document | v0.1.0 | Completed |
| 04 - Dimensional Data Model | v0.1.0 | Completed |
| 05 - Business Financial Assumptions | v0.1.0 | Completed |
| 06 - Dataset Design Specification | v0.1.0 | Draft |
| 07 - Data Dictionary | Planned | Planned |

---

## Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| v0.3.0 | 14 July 2026 | Alyssa Ribeiro | Added the Sales Channels dataset and channel-fee design. |
| v0.2.0 | 13 July 2026 | Alyssa Ribeiro | Added product purchasing fact table and separated product attributes, purchase costs and historical sales values. |
| v0.1.0 | 13 July 2026 | Alyssa da Silva Ribeiro | Initial draft. |