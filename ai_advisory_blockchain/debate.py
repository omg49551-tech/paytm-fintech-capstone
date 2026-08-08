# Multi-Agent Debate - Paytm Money
# MOCK_LLM=1 mode (default, graded baseline)
# Chosen ticker: PAYTECH

import os
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN

MOCK_LLM = os.environ.get("MOCK_LLM", "1") == "1"
TICKER = "PAYTECH"

def bull_agent(ticker, data):
    r = RISK_FREE_RATE + data["beta"] * (MARKET_RETURN - RISK_FREE_RATE)
    return (f"BULL: With a CAPM expected return of {r:.1%} against a beta of "
            f"{data['beta']:.2f}, {ticker} offers attractive risk-adjusted upside "
            f"for growth-oriented investors seeking tech exposure.")

def bear_agent(ticker, data):
    return (f"BEAR: {ticker} carries a standard deviation of {data['std_dev']:.0%}, "
            f"making it one of the most volatile assets in the universe. "
            f"With beta at {data['beta']:.2f}, downside risk in a market correction "
            f"could be severe for retail investors.")

def synthesizer_agent(bull_arg, bear_arg, ticker, data):
    r = RISK_FREE_RATE + data["beta"] * (MARKET_RETURN - RISK_FREE_RATE)
    return (f"SYNTHESIZER: {ticker} presents a high-risk, high-reward profile with "
            f"CAPM return of {r:.1%} and volatility of {data['std_dev']:.0%}. "
            f"While the growth potential is compelling as the bull notes, "
            f"the bear's concern about {data['std_dev']:.0%} std dev is valid. "
            f"Suitable only for aggressive investors with a long horizon.")

if __name__ == "__main__":
    print("=" * 60)
    print(f"MULTI-AGENT DEBATE: {TICKER}")
    print(f"Mode: {'MOCK' if MOCK_LLM else 'LLM'}")
    print("=" * 60)
    
    data = STOCK_UNIVERSE[TICKER]
    
    bull = bull_agent(TICKER, data)
    bear = bear_agent(TICKER, data)
    synth = synthesizer_agent(bull, bear, TICKER, data)
    
    print(f"\n{bull}")
    print(f"\n{bear}")
    print(f"\n{synth}")
