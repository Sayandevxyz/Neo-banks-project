# 🏦 Neo-Banks Project

> A collaborative full-stack digital banking simulation built by 11 teams.
> Each team owns one core module of a modern neo-banking platform.

[![Repo](https://img.shields.io/badge/Repo-Neo--banks--project-0f172a?style=flat-square&logo=github)](https://github.com/Sayandevxyz/Neo-banks-project)
![Teams](https://img.shields.io/badge/Teams-11%20Active-6366f1?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20·%20Flask%20·%20SQLite%20·%20HTML%2FCSS%2FJS-orange?style=flat-square)
![Branch](https://img.shields.io/badge/Branch-main-22c55e?style=flat-square)
---

## 📌 About This Project

**Neo-Banks-Project** is a semester group project where 11 teams independently design, build, and demo one module of a complete digital banking application. Together, all 11 modules form an end-to-end neo-banking system.

Every team delivers:
- ✅ Python + SQLite backend with proper relational schema
- ✅ Flask REST API with clean JSON responses
- ✅ Webpage-style demo (HTML + CSS + Vanilla JS)
- ✅ PDF project report

---

## 🗂️ Repository Structure

```
Neo-banks-project/
│
├── Team 1/    →  Customer Onboarding & KYC System
├── Team 2/    →  Authentication System (PIN + OTP)
├── Team 3/    →  Account Management System
├── Team 4/    →  Transaction Processing System
├── Team 5/    →  Mini Statement Generator
├── Team 6/    →  UPI Payment Simulator
├── Team 7/    →  Expense Analyzer
├── Team 8/    →  Fraud Detection Module
├── Team 9/    →  Credit Score Estimator
├── Team 10/   →  Savings & Investment Planner
├── Team 11/   →  Notification & Alert System
│
└── README.md
```

Each team folder follows the same structure:

```
Team N/
├── backend/
│   ├── app.py            ← Flask REST API
│   ├── db.py             ← SQLite connection + schema
│   ├── models.py         ← SQL queries + business logic
│   └── requirements.txt
├── frontend/
│   └── index.html        ← Webpage demo
├── docs/
│   └── Report.pdf        ← Project report
└── README.md
```

---

## 🛠️ Common Tech Stack

All 11 teams use the same standardised stack:

| Layer | Technology |
|-------|-----------|
| Language | Python 3.7+ |
| Web Framework | Flask + Flask-CORS |
| Database | SQLite via built-in `sqlite3` module |
| Validation | Built-in `re` (regex) module |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Report | ReportLab (PDF generation) |

> **No unnecessary external libraries.** Core logic uses Python standard library only (`sqlite3`, `re`, `os`, `datetime`, `json`).

---

## 👥 All 11 Modules — Overview

| Team | Module | Key Features |
|------|--------|-------------|
| [Team 1](#-team-1--customer-onboarding--kyc-system) | Customer Onboarding & KYC | PAN/Aadhaar validation, profile storage |
| [Team 2](#-team-2--authentication-system) | Authentication System | PIN login, OTP verification, retry limits |
| [Team 3](#-team-3--account-management-system) | Account Management | Create account, balance check, summary |
| [Team 4](#-team-4--transaction-processing-system) | Transaction Processing | Deposit, withdraw, transfer, logs |
| [Team 5](#-team-5--mini-statement-generator) | Mini Statement Generator | Last N txns, date/customer filters |
| [Team 6](#-team-6--upi-payment-simulator) | UPI Payment Simulator | UPI transfer, ID validation, history |
| [Team 7](#-team-7--expense-analyzer) | Expense Analyzer | Categorise spending, monthly summary |
| [Team 8](#-team-8--fraud-detection-module) | Fraud Detection | Flag transactions, patterns, fraud score |
| [Team 9](#-team-9--credit-score-estimator) | Credit Score Estimator | Income + behaviour based scoring |
| [Team 10](#-team-10--savings--investment-planner) | Savings & Investment Planner | FD suggestions, goal planning |
| [Team 11](#-team-11--notification--alert-system) | Notification & Alert System | OTP, transaction, and fraud alerts |

---

---

## 👤 Team 1 — Customer Onboarding & KYC System

> Handles new customer registration and document validation before any banking service is enabled.

### Features
- Add customer details (name, DOB, address, contact)
- Validate **PAN** format — regex: `[A-Z]{5}[0-9]{4}[A-Z]`
- Validate **Aadhaar** format — 12 digits
- Store and retrieve basic customer profile
- KYC status tracking (Pending / Verified / Rejected)

### Database Schema

```sql
CREATE TABLE customers (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    full_name   TEXT     NOT NULL,
    dob         TEXT     NOT NULL,
    phone       TEXT     NOT NULL UNIQUE,
    email       TEXT,
    pan_number  TEXT     NOT NULL UNIQUE,
    aadhaar     TEXT     NOT NULL UNIQUE,
    address     TEXT,
    kyc_status  TEXT     NOT NULL DEFAULT 'Pending'
                         CHECK(kyc_status IN ('Pending','Verified','Rejected')),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/kyc/register` | Add new customer |
| `POST` | `/api/kyc/validate` | Validate PAN / Aadhaar format |
| `GET`  | `/api/kyc/profile/<id>` | Fetch customer profile |
| `PUT`  | `/api/kyc/status` | Update KYC status |
| `GET`  | `/api/kyc/all` | List all customers |

### Validation Rules
- PAN: 5 uppercase letters + 4 digits + 1 uppercase letter (e.g. `ABCDE1234F`)
- Aadhaar: exactly 12 digits, no spaces
- Phone: 10 digits starting with 6–9
- DOB: `YYYY-MM-DD` format

---

---

## 🔐 Team 2 — Authentication System (PIN + OTP)

> Secures all banking operations with a dual-layer authentication system: 4-digit PIN and time-sensitive OTP.

### Features
- Login with 4-digit PIN linked to customer account
- OTP generation and verification (6 digits, 5-minute expiry)
- Retry limit logic — account locked after 3 failed attempts
- Session token issued on successful login
- Unlock account after cooldown period

### Database Schema

```sql
CREATE TABLE auth_users (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id  INTEGER  NOT NULL UNIQUE,
    pin_hash     TEXT     NOT NULL,
    failed_tries INTEGER  NOT NULL DEFAULT 0,
    is_locked    INTEGER  NOT NULL DEFAULT 0,
    locked_until DATETIME,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE otp_log (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER  NOT NULL,
    otp_code    TEXT     NOT NULL,
    expires_at  DATETIME NOT NULL,
    is_used     INTEGER  NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/set-pin` | Set/update PIN for a user |
| `POST` | `/api/auth/login` | Login with PIN |
| `POST` | `/api/auth/otp/generate` | Generate OTP |
| `POST` | `/api/auth/otp/verify` | Verify OTP |
| `POST` | `/api/auth/unlock` | Unlock locked account |

### Logic Flow
```
Login attempt → Check PIN →
  ✓ Correct    → Reset failed_tries → Issue session
  ✗ Incorrect  → failed_tries++ →
      If tries >= 3 → Lock account for 15 minutes
```

---

---

## 🏦 Team 3 — Account Management System

> Manages bank account creation, balance tracking, and account summaries for all customers.

### Features
- Create savings / current account linked to a customer
- Generate unique account number
- Real-time balance check
- Full account summary (type, balance, status, opened date)
- Activate / deactivate account

### Database Schema

```sql
CREATE TABLE accounts (
    id             INTEGER  PRIMARY KEY AUTOINCREMENT,
    account_number TEXT     NOT NULL UNIQUE,
    customer_id    INTEGER  NOT NULL,
    account_type   TEXT     NOT NULL CHECK(account_type IN ('Savings','Current')),
    balance        REAL     NOT NULL DEFAULT 0.0 CHECK(balance >= 0),
    status         TEXT     NOT NULL DEFAULT 'Active'
                            CHECK(status IN ('Active','Inactive','Closed')),
    opened_on      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/accounts/create` | Open a new bank account |
| `POST` | `/api/accounts/balance` | Check account balance |
| `POST` | `/api/accounts/summary` | Full account summary |
| `PUT`  | `/api/accounts/status` | Activate / deactivate account |
| `GET`  | `/api/accounts/all` | List all accounts (admin) |

### Account Number Format
- Auto-generated: `ACC` + 10 random digits (e.g. `ACC1234567890`)

---

---

## 💳 Team 4 — Transaction Processing System

> The core money-movement engine: handles deposits, withdrawals, and transfers between accounts with a full audit log.

### Features
- Deposit money into any active account
- Withdraw with balance check
- Transfer between two accounts (atomic operation)
- Full transaction log with timestamps
- Transaction reference number generation

### Database Schema

```sql
CREATE TABLE accounts (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT    NOT NULL UNIQUE,
    customer_name  TEXT    NOT NULL,
    balance        REAL    NOT NULL DEFAULT 0.0 CHECK(balance >= 0)
);

CREATE TABLE transactions (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    ref_number  TEXT     NOT NULL UNIQUE,
    account_no  TEXT     NOT NULL,
    txn_type    TEXT     NOT NULL CHECK(txn_type IN ('Deposit','Withdrawal','Transfer')),
    amount      REAL     NOT NULL CHECK(amount > 0),
    to_account  TEXT     DEFAULT NULL,
    balance_after REAL   NOT NULL,
    status      TEXT     NOT NULL CHECK(status IN ('Success','Failed')),
    timestamp   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/txn/deposit` | Deposit into account |
| `POST` | `/api/txn/withdraw` | Withdraw from account |
| `POST` | `/api/txn/transfer` | Transfer between accounts |
| `GET`  | `/api/txn/history/<account>` | Transaction history |
| `GET`  | `/api/txn/ref/<ref_number>` | Lookup by reference |

### Transfer Logic
```
Validate both accounts → Check sender balance →
Deduct from sender → Credit to receiver →
Log both legs → Return updated balances
```

---

---

## 📄 Team 5 — Mini Statement Generator

> Generates concise transaction statements with flexible filtering — by count, date range, or customer.

### Features
- Fetch **last N transactions** for any account (`ORDER BY timestamp DESC LIMIT N`)
- **Date-wise filtering** — statements between two dates
- **Customer-wise filtering** — all accounts for one customer
- Formatted output table in the web demo
- Downloadable statement summary

### Database Schema

```sql
CREATE TABLE transactions (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    account_no  TEXT     NOT NULL,
    customer_id INTEGER  NOT NULL,
    txn_type    TEXT     NOT NULL,
    amount      REAL     NOT NULL CHECK(amount > 0),
    description TEXT     DEFAULT '',
    balance_after REAL   NOT NULL,
    txn_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/statement/last-n` | Last N transactions |
| `POST` | `/api/statement/date-range` | Filter by start & end date |
| `POST` | `/api/statement/customer` | All transactions for a customer |
| `GET`  | `/api/statement/all` | Full log (admin) |

### Key SQL Queries

```sql
-- Last N transactions
SELECT * FROM transactions
WHERE account_no = ?
ORDER BY txn_date DESC
LIMIT ?;

-- Date range filter
SELECT * FROM transactions
WHERE account_no = ?
  AND txn_date BETWEEN ? AND ?
ORDER BY txn_date DESC;
```

---

---

## 💸 Team 6 — UPI Payment Simulator

> Simulates a complete UPI payment flow — from account registration to money transfer.

### Features
- Send money via UPI ID to any recipient
- Validate UPI ID format: `username@bank` (regex)
- PIN-verified payment with balance enforcement
- All transactions logged (Success and Failed)
- Fetch last N transactions using `ORDER BY … LIMIT N`
- Live dashboard with stats

### Database Schema

```sql
CREATE TABLE users (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    name       TEXT     NOT NULL,
    upi_id     TEXT     NOT NULL UNIQUE,
    balance    REAL     NOT NULL DEFAULT 0.0 CHECK(balance >= 0),
    pin        TEXT     NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

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

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/health` | Liveness check |
| `GET`  | `/api/dashboard` | Aggregate stats |
| `POST` | `/api/users/create` | Create UPI account |
| `POST` | `/api/users/login` | Fetch by UPI ID |
| `POST` | `/api/users/balance` | Check balance |
| `POST` | `/api/payments/send` | Send money (PIN-verified) |
| `POST` | `/api/transactions` | Last N transactions |
| `GET`  | `/api/transactions/all` | All transactions |

### Payment Flow
```
Validate UPI formats → Check not self-transfer →
Validate amount → Sender exists in DB →
Verify PIN → Check balance →
Deduct & log Success  OR  Log Failed → Return result
```

---

---

## 📊 Team 7 — Expense Analyzer

> Categorises every transaction automatically and generates monthly spending reports with over/under spending insights.

### Features
- Auto-categorise spending (Food, Travel, Bills, Shopping, Healthcare, Others)
- Monthly spending summary per category
- Over Spending / Under Spending report vs. set budget
- Spending trend comparison across months

### Database Schema

```sql
CREATE TABLE expense_categories (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL UNIQUE
);

CREATE TABLE expenses (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    account_no    TEXT     NOT NULL,
    category_id   INTEGER  NOT NULL REFERENCES expense_categories(id),
    amount        REAL     NOT NULL CHECK(amount > 0),
    description   TEXT     DEFAULT '',
    expense_date  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budgets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no    TEXT    NOT NULL,
    category_id   INTEGER NOT NULL REFERENCES expense_categories(id),
    monthly_limit REAL    NOT NULL CHECK(monthly_limit > 0),
    month         TEXT    NOT NULL
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/expense/add` | Log a new expense |
| `POST` | `/api/expense/monthly` | Monthly category summary |
| `POST` | `/api/expense/report` | Over/Under spending report |
| `POST` | `/api/expense/categorise` | Auto-categorise a description |
| `GET`  | `/api/expense/categories` | All available categories |

### Spending Report Logic
```
For each category:
  Spent = SUM(amount) WHERE month = ? AND category = ?
  Budget = monthly_limit for that category
  Status = "Over" if Spent > Budget else "Under"
```

---

---

## 🚨 Team 8 — Fraud Detection Module (Rule-Based)

> Monitors all transactions in real time and flags suspicious activity based on predefined rules and a computed fraud score.

### Features
- Flag **high-value transactions** above a threshold
- Detect **unusual frequency** — too many transactions in short time
- Flag **odd-hour transactions** (e.g. 1 AM – 4 AM)
- Compute a **Fraud Detection Score** (0–100)
- Alert log with rule that was triggered

### Database Schema

```sql
CREATE TABLE fraud_rules (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name   TEXT    NOT NULL,
    description TEXT,
    threshold   REAL,
    is_active   INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE fraud_alerts (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    account_no    TEXT     NOT NULL,
    transaction_id INTEGER,
    rule_id       INTEGER  NOT NULL REFERENCES fraud_rules(id),
    fraud_score   REAL     NOT NULL DEFAULT 0.0,
    alert_status  TEXT     NOT NULL DEFAULT 'Open'
                           CHECK(alert_status IN ('Open','Reviewed','Dismissed')),
    flagged_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/fraud/check` | Check a transaction for fraud |
| `GET`  | `/api/fraud/alerts` | All open fraud alerts |
| `POST` | `/api/fraud/score` | Get fraud score for an account |
| `PUT`  | `/api/fraud/alert/review` | Mark alert as reviewed |
| `GET`  | `/api/fraud/rules` | List all detection rules |

### Fraud Score Logic
```
Score components (additive):
  +30  → Amount > ₹50,000
  +25  → More than 5 transactions in 1 hour
  +20  → Transaction between 1 AM and 4 AM
  +15  → New account (< 30 days old)
  +10  → Different city/IP than usual

Score ≥ 70 → High Risk   🔴
Score 40–69 → Medium Risk 🟡
Score < 40  → Low Risk    🟢
```

---

---

## 📈 Team 9 — Credit Score Estimator

> Estimates a customer's creditworthiness using income data and transaction behaviour, classifying them into risk tiers.

### Features
- Score based on declared **monthly income**
- Score based on **transaction behaviour** (frequency, repayments, overdrafts)
- Classify user into risk category: Excellent / Good / Fair / Poor
- Score history tracking over time
- Recommendations to improve score

### Database Schema

```sql
CREATE TABLE credit_profiles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER NOT NULL UNIQUE,
    monthly_income  REAL    NOT NULL,
    existing_loans  INTEGER NOT NULL DEFAULT 0,
    loan_repaid     INTEGER NOT NULL DEFAULT 0,
    overdraft_count INTEGER NOT NULL DEFAULT 0,
    credit_score    REAL    NOT NULL DEFAULT 0.0,
    risk_category   TEXT    NOT NULL DEFAULT 'Unrated',
    evaluated_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE score_history (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id  INTEGER  NOT NULL,
    score        REAL     NOT NULL,
    risk_label   TEXT     NOT NULL,
    evaluated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/credit/evaluate` | Calculate credit score |
| `GET`  | `/api/credit/profile/<id>` | Fetch credit profile |
| `GET`  | `/api/credit/history/<id>` | Score history |
| `GET`  | `/api/credit/all` | All credit profiles (admin) |

### Scoring Model
```
Base Score: 300

+ Up to 200 pts  → Monthly income bracket
+ Up to 150 pts  → Loans repaid on time
− Up to 100 pts  → Overdraft / missed payments
+ Up to 100 pts  → Account age & activity

Final Score:
  750–900 → Excellent 🟢
  650–749 → Good      🔵
  500–649 → Fair      🟡
  < 500   → Poor      🔴
```

---

---

## 💰 Team 10 — Savings & Investment Planner

> Helps customers plan their finances by suggesting saving percentages, recommending Fixed Deposits, and setting financial goals.

### Features
- Suggest optimal **saving percentage** based on income and expenses
- Recommend **basic FD (Fixed Deposit)** plans based on available surplus
- **Goal planning** — set a target amount and get a monthly savings plan
- FD maturity calculator
- Progress tracking for active goals

### Database Schema

```sql
CREATE TABLE saving_plans (
    id              INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER  NOT NULL,
    monthly_income  REAL     NOT NULL,
    monthly_expense REAL     NOT NULL,
    saving_percent  REAL     NOT NULL,
    monthly_saving  REAL     NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fd_plans (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER  NOT NULL,
    principal     REAL     NOT NULL,
    rate_percent  REAL     NOT NULL,
    tenure_months INTEGER  NOT NULL,
    maturity_amt  REAL     NOT NULL,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE goals (
    id             INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id    INTEGER  NOT NULL,
    goal_name      TEXT     NOT NULL,
    target_amount  REAL     NOT NULL,
    monthly_saving REAL     NOT NULL,
    months_needed  INTEGER  NOT NULL,
    progress       REAL     NOT NULL DEFAULT 0.0,
    status         TEXT     NOT NULL DEFAULT 'Active'
                            CHECK(status IN ('Active','Completed')),
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/planner/saving-suggestion` | Get saving % recommendation |
| `POST` | `/api/planner/fd-recommend` | FD plan recommendation |
| `POST` | `/api/planner/fd-calculator` | Calculate FD maturity amount |
| `POST` | `/api/planner/goal/create` | Create a savings goal |
| `GET`  | `/api/planner/goal/<id>` | Get goal progress |

### Saving Suggestion Logic
```
Surplus = Monthly Income − Monthly Expense
Saving % suggestion:
  Surplus > 50% income  → Save 30%
  Surplus 25–50%        → Save 20%
  Surplus 10–25%        → Save 10%
  Surplus < 10%         → Review expenses first

FD Rate used: 6.5% p.a. (standard bank rate)
Maturity = P × (1 + r/n)^(n×t)
```

---

---

## 🔔 Team 11 — Notification & Alert System

> Manages and delivers all banking alerts — OTP notifications, transaction confirmations, and fraud warnings.

### Features
- **OTP Alerts** — trigger and log OTP sent events
- **Transaction Alerts** — auto-notify on every debit/credit
- **Fraud Alerts** — push high-priority warnings for flagged activity
- Alert history per customer
- Mark alerts as read / acknowledged

### Database Schema

```sql
CREATE TABLE notifications (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    customer_id   INTEGER  NOT NULL,
    alert_type    TEXT     NOT NULL CHECK(alert_type IN ('OTP','Transaction','Fraud','General')),
    message       TEXT     NOT NULL,
    is_read       INTEGER  NOT NULL DEFAULT 0,
    priority      TEXT     NOT NULL DEFAULT 'Normal'
                           CHECK(priority IN ('Low','Normal','High','Critical')),
    sent_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alert_templates (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type    TEXT    NOT NULL,
    template_text TEXT    NOT NULL
);
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/notify/send` | Send a notification |
| `POST` | `/api/notify/otp` | Send OTP alert |
| `POST` | `/api/notify/transaction` | Send transaction alert |
| `POST` | `/api/notify/fraud` | Send fraud warning |
| `GET`  | `/api/notify/inbox/<id>` | Fetch all alerts for customer |
| `PUT`  | `/api/notify/read/<id>` | Mark alert as read |

### Alert Priority Rules
```
OTP alert         → Priority: High
Transaction alert → Priority: Normal
Fraud alert       → Priority: Critical
General           → Priority: Low
```

---

---

## ▶️ Running Any Module

All 11 modules follow the exact same run pattern:

```bash
# Step 1 — Go into the team folder
cd "Team N/backend"

# Step 2 — Install dependencies (same for all teams)
pip install flask flask-cors reportlab

# Step 3 — Start the API
python app.py
# → Running at http://localhost:5000

# Step 4 — Open the web demo
# Double-click  Team N/frontend/index.html  in your browser
```

> ⚠️ Flask must be running **before** opening the frontend. Look for the green **"API Connected"** badge in the demo.

---

## 📋 Submission Checklist (All Teams)

| Item | Required |
|------|----------|
| `backend/db.py` — DB connection + `CREATE TABLE` | ✅ |
| `backend/models.py` — All SQL queries + logic | ✅ |
| `backend/app.py` — Flask REST API | ✅ |
| `backend/requirements.txt` | ✅ |
| `frontend/index.html` — Webpage demo | ✅ |
| `docs/Report.pdf` — Project report | ✅ |
| `README.md` — Module documentation | ✅ |

---

## 📄 Standard Libraries Used (All Teams)

| Module | Purpose |
|--------|---------|
| `sqlite3` | Database connection and all SQL queries |
| `re` | Regex validation (PAN, Aadhaar, UPI, phone, email) |
| `os` | File path handling |
| `datetime` | Timestamps and date arithmetic |
| `json` | Request/response serialisation (via Flask) |
| `random` | OTP and reference number generation |

---

## 🔗 Branches

| Branch | Purpose |
|--------|---------|
| `main` | Final submitted code from all teams |
| `dev` | Development / work-in-progress |

---

<div align="center">

**Neo-Banks-Project** &nbsp;·&nbsp; 11 Teams &nbsp;·&nbsp; Full-Stack Digital Banking Simulation

*Department of Computer Science*

</div>
