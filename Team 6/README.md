# 💸 UPI Payment Simulator — Full Stack Webpage Demo

A complete full-stack UPI payment simulation project.
**Backend:** Python · Flask · SQLite (standard libraries)
**Frontend:** Responsive webpage demo — HTML · CSS · Vanilla JS
**Report:** Auto-generated PDF via ReportLab

---

## 📁 Project Structure

```
upi_demo/
├── backend/
│   ├── app.py              ← Flask REST API
│   ├── db.py               ← SQLite connection + schema (CREATE TABLE)
│   ├── models.py           ← All SQL queries + business logic
│   └── requirements.txt
├── frontend/
│   └── index.html          ← Full webpage demo (CSS + JS inline)
├── docs/
│   ├── generate_report.py  ← PDF report generator
│   └── UPI_Simulator_Report.pdf
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Flask API
```bash
python app.py
# API: http://localhost:5000
```

### 3. Open the web demo
```
Double-click  frontend/index.html  in your file manager
```
The green "API Connected" badge confirms the backend is reachable.

### 4. Regenerate PDF report (optional)
```bash
cd docs
python generate_report.py
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | `/api/health` | Liveness check |
| GET  | `/api/dashboard` | Aggregate stats |
| GET  | `/api/users` | All users |
| POST | `/api/users/create` | Create account |
| POST | `/api/users/login` | Fetch by UPI ID |
| POST | `/api/users/balance` | Check balance |
| POST | `/api/payments/send` | Send payment |
| POST | `/api/transactions` | Last N transactions |
| GET  | `/api/transactions/all` | All transactions |

---

## 🗄️ Database Schema (SQLite)

```sql
-- Table 1: users
CREATE TABLE users (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    name       TEXT     NOT NULL,
    upi_id     TEXT     NOT NULL UNIQUE,
    balance    REAL     NOT NULL DEFAULT 0.0 CHECK(balance >= 0),
    pin        TEXT     NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: transactions
CREATE TABLE transactions (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    sender_upi   TEXT     NOT NULL,
    receiver_upi TEXT     NOT NULL,
    amount       REAL     NOT NULL CHECK(amount > 0),
    status       TEXT     NOT NULL CHECK(status IN ('Success','Failed')),
    note         TEXT     DEFAULT '',
    timestamp    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## ✅ Validations Built In
- UPI format: `username@bank` (regex)
- PIN: exactly 4 digits
- Balance: non-negative, sufficient for transfer
- Self-transfer: blocked
- All failures logged in transactions table
