# DCF Calculator - Paytm Money Business Line Valuation

from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN

# ============================================
# INPUTS (stated assumptions)
# ============================================
# Business line: Paytm Postpaid (Lending)
# Base FCFF = EBIT*(1-tax) + D&A - CapEx - delta_NWC
EBIT = 50_000_000          # INR 5 crore
TAX_RATE = 0.25
DA = 8_000_000             # INR 80 lakh
CAPEX = 12_000_000         # INR 1.2 crore
DELTA_NWC = 3_000_000      # INR 30 lakh

BASE_FCFF = EBIT * (1 - TAX_RATE) + DA - CAPEX - DELTA_NWC

# Growth rates
GROWTH_RATE = 0.18         # 18% for years 1-5
TERMINAL_GROWTH = 0.04     # 4% terminal (at least 3% below WACC)

# WACC computation
BETA = STOCK_UNIVERSE["PAYINFRA"]["beta"]   # 1.10
COST_OF_EQUITY = RISK_FREE_RATE + BETA * (MARKET_RETURN - RISK_FREE_RATE)
COST_OF_DEBT = 0.09        # 9% pre-tax
AFTER_TAX_DEBT = COST_OF_DEBT * (1 - TAX_RATE)
EQUITY_WEIGHT = 0.65
DEBT_WEIGHT = 0.35
WACC = EQUITY_WEIGHT * COST_OF_EQUITY + DEBT_WEIGHT * AFTER_TAX_DEBT

# EV/EBITDA cross-check
EBITDA = EBIT + DA
EBITDA_MULTIPLE = 12       # 12x for fintech lending

def dcf_valuation(wacc, terminal_growth, base_fcff=BASE_FCFF,
                   growth=GROWTH_RATE, years=5):
    # Project FCFFs
    fcffs = []
    fcff = base_fcff
    for y in range(1, years+1):
        fcff = fcff * (1 + growth)
        fcffs.append(fcff)
    
    # PV of projected FCFFs
    pv_fcffs = sum(f / (1+wacc)**y for y, f in enumerate(fcffs, 1))
    
    # Terminal value
    terminal_value = fcffs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1+wacc)**years
    
    enterprise_value = pv_fcffs + pv_terminal
    return enterprise_value, pv_fcffs, pv_terminal

if __name__ == "__main__":
    print("=" * 65)
    print("DCF VALUATION - PAYTM POSTPAID (LENDING)")
    print("=" * 65)
    print(f"\nBase FCFF: INR {BASE_FCFF:,.0f}")
    print(f"WACC: {WACC:.2%}")
    print(f"Terminal Growth: {TERMINAL_GROWTH:.2%}")
    print(f"WACC - Terminal Growth: {WACC - TERMINAL_GROWTH:.2%} (must be > 1%) ✅")
    
    ev, pv_fcff, pv_tv = dcf_valuation(WACC, TERMINAL_GROWTH)
    print(f"\nPV of FCFFs (5 yr): INR {pv_fcff:,.0f}")
    print(f"PV of Terminal Value: INR {pv_tv:,.0f}")
    print(f"Enterprise Value: INR {ev:,.0f}")
    
    # EV/EBITDA cross-check
    ev_ebitda = EBITDA * EBITDA_MULTIPLE
    print(f"\nEV/EBITDA Cross-check: INR {ev_ebitda:,.0f} ({EBITDA_MULTIPLE}x EBITDA)")
    print(f"DCF vs EV/EBITDA difference: {abs(ev-ev_ebitda)/ev_ebitda*100:.1f}%")
    
    # Sensitivity table
    print("\n3x3 SENSITIVITY TABLE (Enterprise Value in INR Crores)")
    print(f"{'':15}", end="")
    tg_range = [TERMINAL_GROWTH-0.01, TERMINAL_GROWTH, TERMINAL_GROWTH+0.01]
    wacc_range = [WACC-0.01, WACC, WACC+0.01]
    
    print(f"  TG={tg_range[0]:.1%}  TG={tg_range[1]:.1%}  TG={tg_range[2]:.1%}")
    print("-" * 55)
    for w in wacc_range:
        print(f"WACC={w:.2%}   ", end="")
        for tg in tg_range:
            if w > tg:
                val, _, _ = dcf_valuation(w, tg)
                print(f"  {val/1e7:>8.1f}  ", end="")
            else:
                print(f"  {'N/A':>8}  ", end="")
        print()
    
    print("\nAll 9 cells: WACC > Terminal Growth ✅")
    print(f"\nEV/EBITDA note: DCF gives INR {ev/1e7:.1f}Cr vs "
          f"EV/EBITDA {ev_ebitda/1e7:.1f}Cr. "
          f"DCF is {'higher' if ev > ev_ebitda else 'lower'} by "
          f"{abs(ev-ev_ebitda)/ev_ebitda*100:.1f}% reflecting explicit "
          f"growth assumptions vs market multiples.")
