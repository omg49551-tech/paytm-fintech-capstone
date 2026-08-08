# Part 1 - Payments & Fraud Analytics
## Files
- `generate_data.py` — generates all 4 CSVs (seed=42)
- `merchants.csv` — 40 merchants
- `users.csv` — 365 users (350 normal + 15 burner)
- `ledger.csv` — 547 transactions
- `gateway_export.csv` — discrepant gateway copy
- `merchant_workbook.xlsx` — Excel workbook
- `sql_queries.py` — 6 SQL fraud detection queries
- `reconcile.py` — payment reconciliation engine
- `chart1_headline.png` — scorecard dashboard
- `chart2_trends.png` — daily GMV & chargeback trends
- `chart3_breakdown.png` — GMV by method & category
- `chart4_merchants_table.png` — top 10 merchants table

## Results

### Reconciliation Output
- Missing in gateway: 27 rows (~5%)
- Extra in gateway: 10 rows (~2%)
- Amount mismatches: 16 rows (~3%)
- Status mismatches: 9 rows (~2%)

### Dashboard Metrics
- Total GMV: ₹2,90,382
- Success Rate: 85.6%
- Match Rate: 90.5%
- Chargeback Ratio: 5.1%

### SQL Findings
- Burner accounts detected: 15 (all seeded rows caught ✅)
- Velocity attack clusters: 8 (all seeded clusters caught ✅)

## Design Decisions
- Fee tiers: UPI=0.5%, Wallet=1.0%, Card=1.8%, Netbanking=1.5%
- Classification: Daily merchant total > INR 5000 AND region != East
- Match rate: identical amount AND status in both ledger and gateway
- Chargeback ratio: count-based, not amount-based
- Burner account: 0 <= account_age_days < 30 with chargeback status
