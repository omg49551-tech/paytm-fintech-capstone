
import sqlite3
import pandas as pd

conn = sqlite3.connect("paytm_payments.db")
merchants = pd.read_csv("merchants.csv")
users = pd.read_csv("users.csv")
ledger = pd.read_csv("ledger.csv")
merchants.to_sql("merchants", conn, if_exists="replace", index=False)
users.to_sql("users", conn, if_exists="replace", index=False)
ledger.to_sql("transactions", conn, if_exists="replace", index=False)

# Query 1
q1 = pd.read_sql("""SELECT DISTINCT transaction_id, user_id, amount_inr, payment_method, status FROM transactions ORDER BY amount_inr DESC LIMIT 10""", conn)
print("Q1 - Top 10 Transactions:\n", q1.to_string())

# Query 2
q2 = pd.read_sql("""SELECT status, COUNT(*) as txn_count, SUM(amount_inr) as total_amount_inr FROM transactions GROUP BY status HAVING COUNT(*) > 1 ORDER BY total_amount_inr DESC""", conn)
print("\nQ2 - Summary by Status:\n", q2.to_string())

# Query 3
q3 = pd.read_sql("""SELECT t.transaction_id, t.amount_inr, t.status, m.merchant_name, m.category, m.region FROM transactions t INNER JOIN merchants m ON t.merchant_id = m.merchant_id WHERE t.status = 'chargeback' ORDER BY t.amount_inr DESC LIMIT 10""", conn)
print("\nQ3 - Chargebacks with Merchant (INNER JOIN):\n", q3.to_string())

# Query 4
q4 = pd.read_sql("""SELECT COUNT(*) as total_chargebacks, COUNT(DISTINCT t.user_id) as unique_users_affected, SUM(t.amount_inr) as total_chargeback_amount_inr FROM transactions t LEFT JOIN users u ON t.user_id = u.user_id WHERE t.status = 'chargeback'""", conn)
print("\nQ4 - Chargeback Impact (LEFT JOIN):\n", q4.to_string())

# Query 5
q5 = pd.read_sql("""SELECT t.transaction_id, t.user_id, u.signup_date, t.transaction_time, t.amount_inr, t.status, CAST((julianday(t.transaction_time) - julianday(u.signup_date)) AS INTEGER) as account_age_days FROM transactions t INNER JOIN users u ON t.user_id = u.user_id WHERE t.status = 'chargeback' AND (julianday(t.transaction_time) - julianday(u.signup_date)) >= 0 AND (julianday(t.transaction_time) - julianday(u.signup_date)) < 30 ORDER BY account_age_days ASC""", conn)
print(f"\nQ5 - Burner Accounts Found: {len(q5)}")
print(q5.to_string())

# Query 6
q6 = pd.read_sql("""SELECT user_id, STRFTIME('%Y-%m-%d %H:', transaction_time) || CAST((CAST(STRFTIME('%M', transaction_time) AS INTEGER) / 10) * 10 AS TEXT) as time_bucket, COUNT(*) as txn_count, SUM(amount_inr) as total_amount FROM transactions GROUP BY user_id, time_bucket HAVING COUNT(*) >= 3 ORDER BY txn_count DESC""", conn)
print(f"\nQ6 - Velocity Attack Clusters Found: {len(q6)}")
print(q6.to_string())

conn.close()
print("\nAll queries done!")
