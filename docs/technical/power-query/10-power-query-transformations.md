# Power Query Transformations

**Version:** v0.1.0  
**Status:** Completed

---

# Purpose

This document describes the Extract, Transform and Load (ETL) process implemented in Power Query for the Potchi Potchi Business Intelligence project.

The objective of these transformations is to ensure that all datasets are clean, consistent and analytically ready before being loaded into the Power BI semantic model.

The ETL process follows a lightweight ELT approach, where source data is first imported from structured CSV files before undergoing validation, type conversion and standardisation within Power Query.

---

# ETL Workflow

```text
CSV Files
      ↓
Import into Power Query
      ↓
Header Promotion
      ↓
Data Type Validation
      ↓
Column Standardisation
      ↓
Data Quality Validation
      ↓
Load into Semantic Model
```

---

# Data Sources

The solution imports eleven CSV datasets representing the dimensional model.

| Table | Type |
|--------|------|
| DimCustomer | Dimension |
| DimDate | Dimension |
| DimExpenseCategory | Dimension |
| DimProduct | Dimension |
| DimSalesChannel | Dimension |
| DimSupplier | Dimension |
| DimVendor | Dimension |
| FactExpenses | Fact |
| FactInventorySnapshot | Fact |
| FactOrders | Fact |
| FactPurchases | Fact |
| FactSales | Fact |

---

# Transformation Standards

The following transformation standards were consistently applied throughout the project.

## Header Promotion

The first row of each CSV file was promoted to column headers.

Purpose:

- Ensure meaningful field names
- Preserve schema consistency
- Simplify model maintenance

---

## Data Type Assignment

Each column was explicitly assigned an appropriate data type.

Examples include:

| Data Type | Example |
|------------|----------|
| Whole Number | IDs, Quantity |
| Decimal Number | Revenue, Cost |
| Date | Order Date |
| Text | Customer Name |
| Boolean | Loyalty Member |

Explicit typing prevents automatic type detection and improves model reliability.

---

## Column Standardisation

Field names were standardised across all datasets to improve readability and maintain consistency between fact and dimension tables.

Naming conventions include:

- PascalCase table names
- Business-friendly column names
- Consistent key naming

Examples:

- CustomerID
- ProductID
- OrderDate
- SupplierID

---

## Data Validation

Power Query was used to verify dataset integrity before loading into the semantic model.

Validation focused on:

- Correct data types
- Missing values
- Invalid dates
- Referential consistency
- Duplicate key detection

---

# Transformations by Dataset

## Dimension Tables

### DimCustomer

Applied transformations:

- Imported CSV file
- Promoted headers
- Assigned data types
- Validated customer attributes
- Loaded into semantic model

Purpose:

Provides customer demographic information used for segmentation and behavioural analysis.

---

### DimDate

Applied transformations:

- Imported calendar dataset
- Promoted headers
- Converted date-related fields
- Validated Year, Quarter, Month and Week hierarchies

Purpose:

Supports time intelligence across all dashboards.

---

### DimExpenseCategory

Applied transformations:

- Header promotion
- Data type conversion
- Category validation

Purpose:

Standardises operating expense classifications.

---

### DimProduct

Applied transformations:

- Imported product catalogue
- Assigned appropriate data types
- Validated product hierarchy

Purpose:

Provides descriptive attributes for analytical slicing across products, brands and collections.

---

### DimSalesChannel

Applied transformations:

- Header promotion
- Data type validation

Purpose:

Supports channel performance analysis.

---

### DimSupplier

Applied transformations:

- Header promotion
- Data type validation

Purpose:

Stores supplier reference information.

---

### DimVendor

Applied transformations:

- Header promotion
- Data type validation

Purpose:

Stores vendor information used for operating expense analysis.

---

# Fact Tables

## FactSales

Applied transformations:

- Imported transactional dataset
- Promoted headers
- Assigned numeric and date types
- Validated transactional records

Purpose:

Primary dataset used for revenue, profitability and sales analysis.

---

## FactOrders

Applied transformations:

- Header promotion
- Data type validation
- Relationship validation

Purpose:

Supports order-level operational analysis.

---

## FactPurchases

Applied transformations:

- Header promotion
- Data type conversion

Purpose:

Tracks procurement activities and inventory replenishment.

---

## FactInventorySnapshot

Applied transformations:

- Header promotion
- Numeric validation

Purpose:

Stores periodic inventory snapshots used for stock monitoring.

---

## FactExpenses

Applied transformations:

- Header promotion
- Numeric validation
- Expense category validation

Purpose:

Supports operating expense and profitability analysis.

---

# Data Quality Considerations

The synthetic datasets were designed to maintain analytical consistency throughout the project.

Validation activities included:

- Consistent surrogate keys
- Referential integrity between fact and dimension tables
- Standardised categorical values
- Explicit numeric formatting
- Consistent date formatting

---

# Output

Following transformation, all datasets were loaded into the Power BI semantic model where relationships, DAX measures and dashboard visualisations were implemented.

The resulting model provides a clean analytical foundation supporting executive reporting, customer analytics, inventory management, sales performance and financial analysis.

---

# Summary

Power Query serves as the foundation of the Potchi Potchi Business Intelligence solution by preparing all source datasets for analytical consumption.

Although the transformations required only lightweight cleansing due to the controlled nature of the synthetic data, documenting the ETL process reflects industry best practices and improves maintainability, transparency and reproducibility of the solution.