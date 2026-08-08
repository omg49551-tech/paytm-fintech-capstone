# Part 2 - Credit Risk & Lending ML
## Results Summary

### Default Rate
- Measured default rate: 20.25% (within 15-25% range ✅)
- Missing credit_bureau_score: 80 rows (20%) 

### Model Comparison

| Metric | Logistic Regression | Decision Tree |
|--------|-------------------|---------------|
| Accuracy | 0.84 | 0.78 |
| Precision | 0.65 | 0.52 |
| Recall | 0.37 | 0.41 |
| F1 Score | 0.47 | 0.46 |
| ROC-AUC | 0.81 | 0.71 |

### Risk-Based Pricing Table

| Tier | Count | Avg Default Prob | Actual Default% | Interest Rate |
|------|-------|-----------------|-----------------|---------------|
| Tier 1 (Low) | 25 | 0.020 | 8.0% | 10-12% |
| Tier 2 (Med-Low) | 25 | 0.073 | 12.0% | 13-16% |
| Tier 3 (Med-High) | 25 | 0.234 | 20.0% | 17-20% |
| Tier 4 (High) | 25 | 0.587 | 40.0% | 21-26% |

Monotonicity confirmed ✅ — lower risk tier = lower actual default rate.

### IsolationForest Anomaly Detection
- Contamination rate: 15/265 = 5.66%
- Seeded anomalies (BTXNA*): 15
- Caught by model: 11
- **Recall: 73.3%**

### Preprocessing Steps (in order)
1. Engineered `is_thin_file` flag from raw data (BEFORE split)
2. Train/test split: 75/25, stratified on default, random_state=42
3. Median imputation from TRAINING data only (median = applied to both splits)
4. One-hot encoding of employment_type
5. StandardScaler fit on train only, transform both

### Bias Awareness Note
Employment_type could act as a proxy for gender in India — gig workers skew male, while certain salaried sectors skew female. Monthly income correlates with urban/rural divide. Credit bureau score disadvantages new-to-credit applicants who may belong to lower-income or younger demographics.

**Governance recommendation:** Implement a maker-checker human-in-the-loop review for all declined thin-file applicants before the decision is finalized.

### Final Recommendation
Deploy **Logistic Regression** for Paytm Postpaid because:
- Higher ROC-AUC (0.81 vs 0.71) — better discrimination
- More stable probability estimates for risk-tier pricing
- Less prone to overfitting than Decision Tree
- IsolationForest recall of 73.3% is acceptable for fraud flagging layer
