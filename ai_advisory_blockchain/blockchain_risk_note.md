# Blockchain & Crypto Risk Analysis
## Paytm Money — Advisory Appendix

---

## 1. Stablecoin & DeFi/DAO Governance Risk

Before Paytm could responsibly surface a "Paytm Crypto Insights" watchlist feature to retail users, two critical risk areas must be addressed.

**Stablecoin Risk:** There is a fundamental difference between fiat-collateralized and algorithmic stablecoins. Fiat-collateralized stablecoins (e.g., USDC, USDT) maintain their peg by holding equivalent reserves in real-world assets like USD or government bonds. These carry counterparty and custodial risk but are generally more stable. Algorithmic stablecoins, by contrast, maintain their peg through code-based supply-demand mechanisms with no underlying collateral. The collapse of TerraUSD (UST) in May 2022 — which lost its peg entirely and wiped out approximately $40 billion in market value within days — demonstrates the catastrophic failure risk of algorithmic designs. For a retail-facing platform like Paytm, only fiat-collateralized stablecoins with transparent, audited reserves should ever be surfaced, and even then with clear risk disclosures.

**DeFi/DAO Governance Risk:** Decentralized Finance protocols are governed by tokenomics — voting rights distributed to token holders. This creates several risks for retail users. First, governance attacks occur when large token holders (whales) vote to drain protocol treasuries. Second, tokenomics can be designed to benefit early insiders at the expense of retail participants through vesting cliffs and unlock schedules. Third, DAO decisions can change protocol rules overnight with no regulatory recourse. Paytm would need to assess governance token distribution, treasury transparency, and smart contract audit history before featuring any DeFi protocol.

---

## 2. Crypto Asset Allocation Recommendation for Paytm Money

**Recommendation: Maximum 0% allocation for standard retail advisory portfolios.**

Standard CAPM-style portfolio theory does not favor including cryptocurrency in an optimal portfolio for the following reasons:

- **No intrinsic value or dividends:** Unlike equities (which represent ownership in cash-generating businesses) or bonds (which pay coupons), cryptocurrency generates no cash flows. Its value is entirely speculative and driven by sentiment.
- **Heavy-tailed, positively-skewed returns:** Crypto returns exhibit extreme kurtosis — occasional massive gains mask frequent severe losses. This makes standard mean-variance optimization unreliable.
- **Survivorship bias:** Most cryptocurrencies launched since 2009 have gone to zero. Performance statistics are dominated by Bitcoin and Ethereum, creating a misleading picture of the asset class.
- **High transaction costs:** Retail crypto trading involves exchange fees, spread costs, and in DeFi, gas fees — all of which erode returns significantly.
- **Low/negative correlation benefit is overstated:** While crypto has historically shown low correlation with equities, during market stress events (e.g., March 2020, November 2022) correlations spiked, eliminating the diversification benefit exactly when it was most needed.

For Paytm Money's retail advisory product, the justified recommendation is **zero allocation** to cryptocurrency for Conservative and Moderate investors. For Aggressive investors with a horizon exceeding 10 years who explicitly request crypto exposure and demonstrate understanding of the risks, a maximum of 2-3% could be considered as a satellite position — but this should never be part of the default model portfolio.

---

## 3. T.A.N.G. Fraud Framework — UPI/Wallet + Lending + Wealth Platform

The T.A.N.G. framework identifies four social-engineering triggers: **Temptation, Authority, Need, and Greed.** For Paytm's specific combination of UPI payments, lending, and wealth management, the two most relevant vectors are:

### Vector 1: Authority-Based UPI Fraud (Impersonation)
**Risk:** Fraudsters impersonate Paytm customer support, bank officials, or KYC agents and pressure users to share OTPs, UPI PINs, or authorize "test transactions." The Authority trigger is especially potent because Paytm is a recognized brand — users trust communications appearing to come from it.

**Bank-side defense:** **Real-time transaction anomaly scoring with step-up authentication.** When a UPI transaction is initiated from a new device, new beneficiary, or unusual location, the system automatically triggers an additional authentication step (biometric or secondary OTP) and sends an out-of-band SMS alert. This breaks the fraudster's script since they cannot intercept the secondary channel.

### Vector 2: Greed-Based Investment Fraud (Fake Wealth Schemes)
**Risk:** On the Paytm Money side, fraudsters exploit the Greed trigger by promoting fake "guaranteed return" investment schemes via WhatsApp or Telegram, claiming to be Paytm Money advisors offering exclusive high-yield products. Victims are directed to invest through fake UPI payment links that route funds to fraudster accounts.

**Bank-side defense:** **Payee name verification with cooling-off period for large transfers.** For any first-time payment above INR 10,000 to a new beneficiary, the bank displays the registered payee name for confirmation and enforces a 4-hour cooling-off period before release. This gives victims time to verify and report before funds are irreversibly transferred. Combined with a merchant category block on known fraudulent UPI IDs maintained in a shared RBI fraud registry, this significantly reduces successful fund transfers.

---
*All analysis uses MOCK_LLM=1 (default mode). No LLM API calls were made.*
