
import pandas as pd

def reconcile_payments(ledger_df, gateway_df):
    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])
    
    missing_in_gateway = ledger_df[ledger_df["transaction_id"].isin(ledger_ids - gateway_ids)]
    extra_in_gateway = gateway_df[gateway_df["transaction_id"].isin(gateway_ids - ledger_ids)]
    
    common_ids = ledger_ids & gateway_ids
    merged = pd.merge(
        ledger_df[ledger_df["transaction_id"].isin(common_ids)][["transaction_id","amount_inr","status"]],
        gateway_df[gateway_df["transaction_id"].isin(common_ids)][["transaction_id","amount_inr","status"]],
        on="transaction_id", suffixes=("_ledger","_gateway")
    )
    amount_mismatch = merged[merged["amount_inr_ledger"] != merged["amount_inr_gateway"]].copy()
    amount_mismatch["difference"] = amount_mismatch["amount_inr_gateway"] - amount_mismatch["amount_inr_ledger"]
    status_mismatch = merged[merged["status_ledger"] != merged["status_gateway"]]
    
    return missing_in_gateway, extra_in_gateway, amount_mismatch, status_mismatch

if __name__ == "__main__":
    ledger_df = pd.read_csv("ledger.csv")
    gateway_df = pd.read_csv("gateway_export.csv")
    missing, extra, amt_mismatch, status_mismatch = reconcile_payments(ledger_df, gateway_df)
    print(f"Missing in gateway: {len(missing)} rows")
    print(f"Extra in gateway: {len(extra)} rows")
    print(f"Amount mismatches: {len(amt_mismatch)} rows")
    print(f"Status mismatches: {len(status_mismatch)} rows")
