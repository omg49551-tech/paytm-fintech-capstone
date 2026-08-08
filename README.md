# paytm-fintech-capstone
Paytm FinTech Analytics &amp; AI Platform - Capstone
## Repository Structure
paytm-fintech-capstone/
├── payments_fraud_analytics/
├── credit_risk_lending_ml/
├── ai_advisory_blockchain/
└── README.md
## Setup & Run

### Requirements
```bash
pip install pandas numpy matplotlib scikit-learn
```

### Part 1 — Payments & Fraud Analytics
```bash
cd payments_fraud_analytics
python generate_data.py
python sql_queries.py
python reconcile.py
```

### Part 2 — Credit Risk & Lending ML
```bash
cd credit_risk_lending_ml
python generate_data.py
python credit_risk_ml.py
```

### Part 3 — AI Advisory & Blockchain
```bash
cd ai_advisory_blockchain
python advisory_agent.py
python extract_disclosure.py
python debate.py
python dcf_calculator.py
```

## Design Decisions

### Part 1
- Fee tiers: UPI 0.5%, Wallet 1.0%, Card 1.8%, Netbanking 1.5%
- Classification rule: Daily merchant total > INR 5000 AND region != East
- Match rate counts only transactions with identical amount AND status in both files

### Part 2
- Stratified split preserves 20.25% default rate in both train/test
- Median imputation computed from training data only
- IsolationForest contamination = 15/265 = 5.66%
- Logistic Regression recommended over Decision Tree (AUC 0.81 vs 0.71)

### Part 3
- All files run in MOCK_LLM=1 mode (default, no API key needed)
- CAPM uses beta only, never analyst_expected_return
- Terminal growth (4%) is 3%+ below WACC — all 9 sensitivity cells valid
