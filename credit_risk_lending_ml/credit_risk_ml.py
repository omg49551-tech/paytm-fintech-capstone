import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("credit_applicants.csv")
df["is_thin_file"] = df["credit_bureau_score"].isna().astype(int)

X = df.drop(["applicant_id", "default"], axis=1)
y = df["default"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

train_median = X_train["credit_bureau_score"].median()
X_train["credit_bureau_score"] = X_train["credit_bureau_score"].fillna(train_median)
X_test["credit_bureau_score"] = X_test["credit_bureau_score"].fillna(train_median)

X_train = pd.get_dummies(X_train, columns=["employment_type"])
X_test = pd.get_dummies(X_test, columns=["employment_type"])
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(random_state=42, max_iter=1000)
dt = DecisionTreeClassifier(random_state=42)
lr.fit(X_train_scaled, y_train)
dt.fit(X_train_scaled, y_train)

lr_prob = lr.predict_proba(X_test_scaled)[:,1]
dt_prob = dt.predict_proba(X_test_scaled)[:,1]

print("=== MODEL COMPARISON ===")
print(f"Logistic Regression AUC: {roc_auc_score(y_test, lr_prob):.4f}")
print(f"Decision Tree AUC: {roc_auc_score(y_test, dt_prob):.4f}")

behaviour = pd.read_csv("txn_behaviour.csv")
features = StandardScaler().fit_transform(behaviour[["txn_hour","is_new_device","txn_amount_inr"]])
iso = IsolationForest(random_state=42, contamination=15/265)
behaviour["is_anomaly"] = (iso.fit_predict(features) == -1).astype(int)
caught = behaviour[behaviour["txn_id"].str.startswith("BTXNA") & (behaviour["is_anomaly"]==1)]
print(f"IsolationForest Recall: {len(caught)}/15 = {len(caught)/15*100:.1f}%")
