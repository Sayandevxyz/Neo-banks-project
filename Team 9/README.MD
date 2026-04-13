# 📈 Team 9 — Credit Score Estimator

> **Module 9** of the Neo-Banks collaborative project.
> Estimates a customer's creditworthiness using income data and transaction behaviour.

---

## 🚀 Quick Start

```bash
# Step 1 — Install dependencies
cd "Team 9/backend"
pip install flask flask-cors reportlab

# Step 2 — Start the API
python app.py
# → Running at http://localhost:5000

# Step 3 — Open frontend
# Double-click  Team 9/frontend/index.html  in your browser
```

---

## 📁 File Structure

```
Team 9/
├── backend/
│   ├── app.py            ← Flask REST API (4 endpoints)
│   ├── db.py             ← SQLite connection + schema init
│   ├── models.py         ← Scoring engine + DB queries
│   └── requirements.txt
└── frontend/
    └── index.html        ← CreditLens dashboard (dark mode)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/health` | Liveness check |
| `POST` | `/api/credit/evaluate` | Calculate + save credit score |
| `GET`  | `/api/credit/profile/<id>` | Fetch latest credit profile |
| `GET`  | `/api/credit/history/<id>` | Fetch score history |
| `GET`  | `/api/credit/all` | All profiles (admin) |

### Sample Request — Evaluate

```json
POST /api/credit/evaluate
{
  "customer_id": 1001,
  "customer_name": "Arjun Sharma",
  "monthly_income": 75000,
  "existing_loans": 1,
  "loan_repaid": 3,
  "overdraft_count": 0
}
```

---

## 🧮 Scoring Model

| Component | Max Points | Direction |
|-----------|-----------|-----------|
| Base Score | 300 | — |
| Monthly Income Bracket | +200 | Positive |
| Loans Repaid on Time | +150 | Positive |
| Active Existing Loans | −75 | Penalty |
| Overdraft / Missed Payments | −100 | Penalty |

### Risk Tiers

| Score Range | Category | Color |
|------------|----------|-------|
| 750 – 900 | Excellent | 🟢 Emerald |
| 650 – 749 | Good | 🔵 Sky Blue |
| 500 – 649 | Fair | 🟡 Amber |
| < 500 | Poor | 🔴 Crimson |
