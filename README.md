# Phyllo Product Analyst Intern Assignment

## Task 1 — Documentation vs API Findings

I compared the published API documentation with the three captured API responses and identified the following mismatches.

| **What the docs say** | **What the API does (file & field)** | **Impact** |
|------------------------|---------------------------------------|------------|
| `status` can only be `pending`, `shipped`, `delivered`, or `cancelled`. | `orders_page1.json` returns `status: refunded`. | Clients relying on documented status values may classify orders incorrectly, leading to inaccurate revenue and reporting. |
| `customer.email` is always present. | `orders_page2.json` returns `customer.email: null`. | Integrations expecting a valid email may fail when sending receipts or syncing customer records. |
| Monetary values are integers in the smallest currency unit (for example, `5470` = $54.70). | `orders_page2.json` returns decimal values such as `53.62`. | Developers following the documentation could calculate incorrect monetary values and financial reports. |
| `GET /v1/orders/{id}` returns `404` when an order does not exist. | `order_ord_9999.json` returns HTTP `200` with `"order": null`. | Clients cannot reliably distinguish between a successful response and a missing resource. |
| Pagination should continue only when `has_more` is `true` using `next_cursor`. | The captured responses and README indicate another page exists despite inconsistent pagination signals. | A client relying only on `has_more` could stop early and miss additional orders. |

### Worst Finding
The monetary format mismatch is the most serious issue. The documentation specifies that monetary values are integers in the smallest currency unit, while the API returns decimal currency values. Any client implementing the API according to the documentation could calculate revenue incorrectly, affecting finance dashboards, reporting, and downstream billing systems.

## Task 2 — Revenue Calculation
**Total Revenue:** **$225.70**
### Assumptions Made

- Included orders from both `orders_page1.json` and `orders_page2.json` because both files represent the same paginated order list.
- Excluded orders with the `cancelled` status because they do not represent completed purchases.
- Excluded orders with the undocumented `refunded` status because I assumed revenue should reflect net revenue rather than refunded transactions.

### Notes
The documentation does not mention a `refunded` status, so it is unclear whether refunded orders should be included in revenue calculations. I excluded them as a documented assumption rather than treating it as a confirmed API rule.
The documentation also states that monetary values are integers in the smallest currency unit, but the responses return decimal currency values. Without clarification, it is impossible to know whether the API or the documentation represents the intended behavior.

## Task 3A — Reply to Priya
**Subject:** Revenue reconciliation issue
Hi Priya,
Thanks for reporting the discrepancy.
I reviewed the order data and found that the API responses are not fully consistent with the published documentation. In particular, the responses include an undocumented `refunded` order status, which can affect how revenue is calculated if all `total` values are summed directly.
I've shared this inconsistency with the engineering team for investigation. Until the API behavior is clarified, revenue calculated from the API may not exactly match the Meridian dashboard.
Thanks for bringing this to our attention.
Best,
Meridian Product Team

## Task 3B — Bug Report

### Title
Monetary values returned in decimal format instead of the documented smallest currency unit.

### Steps to Reproduce
1. Read `API_DOCS.md`, which states that monetary values are integers in the smallest currency unit (for example, `5470` = $54.70).
2. Open `orders_page2.json`.
3. Compare the `subtotal`, `tax`, `shipping`, and `total` fields in `orders_page2.json`.
### Expected Result
The API should return monetary values as integers in the smallest currency unit, matching the published documentation.
### Actual Result
The API returns decimal values such as `44.00`, `3.63`, `5.99`, and `53.62`, which do not match the documented format.
### Impact
Clients implementing the API according to the documentation may calculate incorrect revenue and billing amounts. This can also cause finance reports generated from the API to differ from the Meridian dashboard.
### Severity
**High** — This issue affects financial calculations and can impact every client integrating with the Orders API.
