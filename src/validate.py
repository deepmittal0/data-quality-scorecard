from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "customers.csv")
issues = []
for col in df.columns:
    for idx in df.index[df[col].isna()]:
        issues.append({"row": int(idx)+2, "column": col, "rule": "NOT_NULL", "value": ""})
dupes = df.index[df.duplicated(keep=False)]
for idx in dupes:
    issues.append({"row": int(idx)+2, "column": "*", "rule": "DUPLICATE_ROW", "value": ""})
for idx, value in df["age"].items():
    if pd.notna(value) and not 18 <= value <= 100:
        issues.append({"row": int(idx)+2, "column": "age", "rule": "RANGE_18_100", "value": value})
for idx, value in df["email"].items():
    if pd.notna(value) and "@" not in str(value):
        issues.append({"row": int(idx)+2, "column": "email", "rule": "EMAIL_FORMAT", "value": value})
log = pd.DataFrame(issues, columns=["row","column","rule","value"])
out = ROOT / "reports"
out.mkdir(exist_ok=True)
log.to_csv(out / "issue_log.csv", index=False)
score = 100 if len(df)==0 else round(max(0, 100*(1-len(log)/max(1,len(df)*len(df.columns)))), 2)
pd.DataFrame([{"rows":len(df),"issues":len(log),"quality_score_pct":score}]).to_csv(out/"scorecard.csv", index=False)
print(f"Rows: {len(df)} | Issues: {len(log)} | Score: {score}%")
