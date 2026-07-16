# Power BI Semantic Model

The semantic model follows a star schema design with role-playing date dimensions.

![Power BI Semantic Model](../assets/images/powerbi-semantic-model.png)

## Role-Playing Date Dimensions

The model uses multiple date dimensions derived from the base `DimDate` table.

| Dimension | Used by |
|-----------|---------|
| DimOrderDate | FactOrders (OrderDateKey) |
| DimShipDate | FactOrders (ShippedDateKey) |
| DimDeliveryDate | FactOrders (DeliveredDateKey) |
| DimPurchaseDate | FactPurchases (PurchaseDateKey) |
| DimExpenseDate | FactExpenses (ExpenseDateKey) |
| DimSnapshotDate | FactInventorySnapshot (SnapshotDateKey) |

The original `DimDate` table is retained as the canonical calendar dimension and serves as the source for all role-playing date dimensions.