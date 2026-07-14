# 05. Business Financial Assumptions

**Project:** Potchi Potchi Business Intelligence  
**Document:** Business Financial Assumptions  
**Version:** v0.1.3  
**Author:** Alyssa da Silva Ribeiro  
**Last Updated:** 13 July 2026  
**Status:** Completed

---

# Table of Contents

1. Purpose
2. Initial Investment
3. Capital Allocation
4. Operational Budget
5. Inventory Investment Strategy
6. Revenue Assumptions
7. Cost Assumptions
8. Profitability Assumptions
9. Business Scenarios
10. Growth Assumptions
11. Strategic Business Rules
12. Expansion Strategy
13. Financial Risks
14. Future Improvements
15. Appendix

---

# 1. Purpose

This document defines the financial assumptions that support the Potchi Potchi Business Intelligence project.

The objective is to establish realistic business rules that will later be used to generate synthetic datasets for reporting and dashboard development.

All simulated financial data created during this project should follow the assumptions defined within this document.

---

# 2. Initial Investment

Potchi Potchi begins operations with an initial capital investment of **£20,000**.

This capital represents the total amount available to launch the business, including inventory purchases, operational costs, marketing activities and emergency cash reserves.

---

# 3. Capital Allocation

The initial investment is allocated as follows.

| Category | Budget |
|----------|---------:|
| Website & Domain | £350 |
| Marketing Budget | £1,800 |
| TikTok Shop Setup | £300 |
| Packaging Materials | £500 |
| Equipment | £700 |
| Emergency Cash Reserve | £2,500 |
| Initial Inventory Investment | **£13,850** |

Total Initial Capital

**£20,000**

---

# 4. Operational Budget

The following recurring operational expenses are assumed.

| Expense | Frequency | Estimated Cost |
|----------|-----------|---------------:|
| Shopify Subscription | Monthly | £25 |
| Website Domain | Annual | £15 |
| Marketing | Monthly | £150 |
| Internet & Utilities Allocation | Monthly | £40 |
| Packaging Replenishment | Monthly | £50 |
| Business Software | Monthly | £20 |

Warehouse rental is excluded during the initial operating phase.

---

# 5. Inventory Investment Strategy

The company adopts a diversified inventory strategy during its first operating period.

Rather than purchasing large quantities of a limited number of products, Potchi Potchi will prioritise catalogue diversity.

### Initial assumptions

- Approximately **100 unique SKUs**
- Average of **20 units per SKU**
- Approximately **2,000 total units**
- Average purchase cost of **£7 per unit**

This strategy supports:

- Product demand testing
- Brand performance analysis
- Inventory optimisation
- Reduced business risk

---

# 6. Revenue Assumptions

The following assumptions will guide synthetic sales generation.

| Metric | Assumption |
|---------|-----------:|
| Average Order Value | £38 |
| Average Units per Order | 2.4 |
| Average Selling Price | £16 |
| Monthly Orders (Initial) | 120 |
| Monthly Growth Rate | 8% |

Revenue growth will be modelled gradually rather than linearly to better reflect realistic business behaviour.

---

# 7. Cost Assumptions

The following costs are expected throughout business operations.

| Cost Category | Assumption |
|---------------|------------|
| Average Product Cost | £7 |
| Average Shipping Cost | £4.50 |
| Packaging Cost per Order | £0.80 |
| Payment Processing Fees | 2.5% of Revenue |
| Marketing Spend | £150 per month |

> **Accounting and Data Modelling Note**
>
> Inventory acquisition is treated separately from operating expenses. Product purchases, freight, import duties and other directly attributable landed costs will be recorded within the Purchases dataset.
>
> The Expenses dataset will contain only non-inventory operating costs such as marketing, software, storage, accounting and utilities.
>
>  **Sales Channel Fees**
>
>  Platform fees are treated as transaction-level variable selling costs and are directly attributable to individual customer orders.
>
> The current fee rate is maintained within the Sales Channel dimension, while the actual fee amount charged on each completed sale is preserved within the sales fact table.
>
> This approach prevents historical profitability from changing when platform fee rates are updated.
>
> **Supplier and Vendor Classification**
>
> Potchi Potchi distinguishes between merchandise suppliers and operational vendors.
>
> - **Suppliers** provide products intended for resale and are analysed through purchasing and inventory processes.
> - **Vendors** provide operational services such as website hosting, advertising, software, storage, accounting and utilities.
>
> Payments to merchandise suppliers are recorded within the Purchases dataset.
>
> Payments to operational vendors are recorded within the Expenses dataset.
>
> This separation prevents inventory acquisition costs from being incorrectly classified as operating expenses.

---

# 8. Profitability Assumptions

Target business performance indicators.

| KPI | Target |
|------|-------:|
| Gross Margin | 55% |
| Net Margin | 18% |
| Inventory Turnover | 6 times per year |
| Order Fulfilment Rate | 98% |
| Stock Availability | 95% |

These values represent long-term business objectives rather than guaranteed outcomes.

---

# 9. Business Scenarios

To support strategic planning and future dashboard simulations, the project defines three financial scenarios representing different business growth trajectories.

These scenarios will be used during dataset generation and may later support interactive scenario analysis within Power BI.

---

## Conservative Scenario

Represents slower-than-expected business growth.

Typical characteristics include:

- Lower customer acquisition.
- Slower sales growth.
- Lower inventory turnover.
- Delayed warehouse expansion.
- Reduced marketing efficiency.

| Metric | Value |
|---------|--------:|
| Monthly Orders | 80 |
| Monthly Growth Rate | 4% |
| Average Order Value | £34 |
| Gross Margin | 50% |
| Net Margin | 12% |

---

## Expected Scenario

Represents the baseline business plan and serves as the default scenario for this project.

| Metric | Value |
|---------|--------:|
| Monthly Orders | 120 |
| Monthly Growth Rate | 8% |
| Average Order Value | £38 |
| Gross Margin | 55% |
| Net Margin | 18% |

---

## Optimistic Scenario

Represents faster business growth driven by stronger customer acquisition and higher demand.

| Metric | Value |
|---------|--------:|
| Monthly Orders | 180 |
| Monthly Growth Rate | 12% |
| Average Order Value | £42 |
| Gross Margin | 58% |
| Net Margin | 22% |

---

## Business Interpretation

The Expected Scenario represents the primary business plan and will be used when generating the initial datasets.

The Conservative and Optimistic scenarios provide alternative planning assumptions and may be implemented in future Power BI dashboards through interactive scenario selection.

This approach enables management to compare financial performance under different market conditions and supports more informed strategic decision-making.

---

# 10. Growth Assumptions

Business growth is expected to occur progressively.

Growth indicators include:

- Increasing monthly orders.
- Increasing repeat customers.
- Expanding product catalogue.
- Improving inventory turnover.
- Increasing customer lifetime value.

Seasonal fluctuations will be incorporated into future datasets.

---

# 11. Strategic Business Rules

## Market Expansion

Business expansion decisions must be supported by measurable performance indicators rather than assumptions.

The company adopts a phased growth strategy, expanding only after achieving predefined financial and operational targets.

This approach minimises operational risk while supporting sustainable growth.

---

# 12. Expansion Strategy

## Warehouse Expansion

The business should evaluate renting external warehouse space when one or more of the following conditions are met.

- Home inventory utilisation exceeds **80%**
- Monthly orders exceed **350**
- Monthly revenue exceeds **£18,000**
- Inventory value exceeds **£25,000**

For this project, warehouse expansion will be represented using **Shurgard Self Storage – Deptford**.

### Geographic Scope

Potchi Potchi will initially operate exclusively within the United Kingdom.

The company follows a phased expansion strategy driven by measurable business performance rather than predetermined timelines.

The planned expansion path is:

1. United Kingdom
2. Ireland
3. Selected European markets

Each expansion phase will only be considered after predefined financial and operational objectives have been consistently achieved.

Expansion decisions will be supported by Business Intelligence dashboards and key performance indicators, including revenue growth, customer acquisition, inventory turnover, profitability and operational capacity.

---

## Brazil Expansion

International expansion should only be considered when the business demonstrates sustainable financial performance.

Expansion indicators include:

- Twelve consecutive profitable months.
- Cash reserves above **£30,000**.
- Inventory turnover greater than **6** per year.
- Net Margin above **18%**.
- Stable supplier relationships.

---

# 13. Financial Risks

Potential financial risks include:

- Currency exchange fluctuations.
- Supplier price increases.
- Shipping cost inflation.
- Seasonal demand volatility.
- Slow-moving inventory.
- Excess stock.
- Lower-than-expected customer acquisition.

These risks should be monitored continuously through the Business Intelligence dashboards.

---

# 14. Future Improvements

Future versions of this project may include:

- Cash Flow Forecasting
- Working Capital Dashboard
- Budget vs Actual Analysis
- Profit Forecasting
- Financial Scenario Simulation
- Monte Carlo Risk Analysis
- Currency Sensitivity Analysis
- Interactive Scenario Comparison (Conservative vs Expected vs Optimistic vs Actual)

---

# 15. Appendix

## Related Documents

| Document | Version | Status |
|----------|---------|--------|
| 01 - Market Research | v0.1.0 | Completed |
| 02 - Business Requirements Document | v0.1.0 | Completed |
| 03 - Data Requirements Document | v0.1.0 | Completed |
| 04 - Dimensional Data Model | v0.1.0 | Completed |
| 05 - Business Financial Assumptions | v0.1.0 | Draft |
| 06 - Dataset Design Specification | Planned | Planned |

---

## Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| v0.1.3 | 14 July 2026 | Alyssa Ribeiro | Clarified the distinction between merchandise suppliers and operational vendors. |
| v0.1.2 | 14 July 2026 | Alyssa Ribeiro | Clarified the treatment of sales-channel platform fees. |
| v0.1.1 | 13 July 2026 | Alyssa Ribeiro | Clarified the separation between inventory acquisition and operating expenses. |
| v0.1.0 | 13 July 2026 | Alyssa da Silva Ribeiro | Initial draft. |