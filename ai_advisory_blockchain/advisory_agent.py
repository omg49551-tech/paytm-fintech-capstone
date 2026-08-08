# Advisory Agent - Paytm Money
# MOCK_LLM=1 mode (default, graded baseline)

import os
import math
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

MOCK_LLM = os.environ.get("MOCK_LLM", "1") == "1"

# Prescribed allocation table
ALLOCATION_MAP = {
    "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
    "Moderate":     ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
    "Aggressive":   ["PAYTECH", "PAYFIN", "PAYINFRA"],
}

def get_stock_data(ticker):
    """Tool call - fetches stock data from STOCK_UNIVERSE"""
    return STOCK_UNIVERSE[ticker]

def run_agent(profile):
    investor_id = profile["investor_id"]
    risk_tolerance = profile["risk_tolerance"]
    
    # THINK
    tickers = ALLOCATION_MAP[risk_tolerance]
    weights = [1/3, 1/3, 1/3]
    
    # ACT - tool calls
    stock_data = {t: get_stock_data(t) for t in tickers}
    
    # OBSERVE - compute CAPM return
    capm_returns = []
    for t in tickers:
        beta = stock_data[t]["beta"]
        er = RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)
        capm_returns.append(er)
    
    portfolio_return = sum(w * r for w, r in zip(weights, capm_returns))
    
    # Portfolio variance (rho=0.3 for all pairs)
    rho = 0.3
    std_devs = [stock_data[t]["std_dev"] for t in tickers]
    
    variance = sum((w**2) * (s**2) for w, s in zip(weights, std_devs))
    pairs = [(0,1),(0,2),(1,2)]
    for i, j in pairs:
        variance += 2 * weights[i] * weights[j] * rho * std_devs[i] * std_devs[j]
    
    portfolio_std = math.sqrt(variance)
    
    # DECIDE - escalation check
    escalated = portfolio_std > 0.20
    
    # Narrative (MOCK mode)
    if MOCK_LLM:
        narrative = (f"For {risk_tolerance} investor {investor_id}, we recommend an equal "
                     f"allocation across {tickers} with an expected portfolio return of "
                     f"{portfolio_return:.1%} and volatility of {portfolio_std:.1%}.")
    
    result = {
        "investor_id": investor_id,
        "risk_tolerance": risk_tolerance,
        "tickers": tickers,
        "portfolio_return": portfolio_return,
        "portfolio_std": portfolio_std,
        "escalated": escalated,
        "narrative": narrative,
    }
    return result

if __name__ == "__main__":
    print("=" * 60)
    print("PAYTM MONEY - PORTFOLIO ADVISORY AGENT")
    print(f"Mode: {'MOCK' if MOCK_LLM else 'LLM'}")
    print("=" * 60)
    
    for profile in INVESTOR_PROFILES:
        result = run_agent(profile)
        print(f"\n{result['investor_id']} ({result['risk_tolerance']})")
        print(f"  Tickers: {result['tickers']}")
        print(f"  CAPM Return: {result['portfolio_return']:.2%}")
        print(f"  Portfolio Std Dev: {result['portfolio_std']:.2%}")
        if result['escalated']:
            print(f"  ⚠️  ESCALATED_TO_HUMAN_ADVISOR")
        else:
            print(f"  ✅ AUTO-APPROVED")
        print(f"  {result['narrative']}")
