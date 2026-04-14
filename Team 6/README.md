<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&color=0:0f0c29,50:302b63,100:24243e&height=280&section=header&text=NEO%20BANK&fontSize=90&fontColor=ffffff&fontAlignY=45&desc=⚡%20UPI%20Payment%20Simulator&descSize=24&descAlignY=68&descColor=7eb3ff&stroke=4f8ef7&strokeWidth=2&animation=fadeIn" width="100%" />

</div>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Space+Mono&weight=700&size=22&duration=3000&pause=800&color=7EB3FF&center=true&vCenter=true&width=700&lines=🏦+Full-Stack+UPI+Banking+Simulator;💸+Instant+Peer-to-Peer+Transfers;🔐+PIN-Protected+Secure+Transactions;📊+Real-Time+Dashboard+%26+Analytics;🛡️+Built+by+Team+6+%7C+Led+by+Sayan+Mondal" />

<br/>

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
</p>

<p>
<img src="https://img.shields.io/badge/🚀%20Status-Live%20%26%20Active-00d4aa?style=flat-square"/>
<img src="https://img.shields.io/badge/🧑‍💻%20Team-6-7eb3ff?style=flat-square"/>
<img src="https://img.shields.io/badge/📄%20License-MIT-f0a500?style=flat-square"/>
<img src="https://img.shields.io/badge/🤝%20PRs-Welcome-ff6b9d?style=flat-square"/>
<img src="https://img.shields.io/badge/💳%20UPI-Simulator-4f8ef7?style=flat-square"/>
</p>

</div>

---

<div align="center">
<h2>🎯 &nbsp; What is Neo Bank?</h2>
</div>

> **Neo Bank** is a fully functional **UPI Payment Simulator** built as a web application. It replicates core digital banking features — from account creation to peer-to-peer money transfers — with a clean UI, RESTful API, and persistent SQLite storage.

<div align="center">

```
┌─────────────────────────────────────────────────────────────┐
│  👤 Login with UPI ID   →   💸 Send Money   →   📊 Track It  │
└─────────────────────────────────────────────────────────────┘
```

</div>

---

<div align="center">
<h2>✨ &nbsp; Core Features</h2>
</div>

<table>
<tr>
<td width="50%" valign="top">

### 🔐 Authentication
- UPI ID-based login (no passwords)
- 4-digit PIN for transaction security
- Regex-validated UPI format
- Session-based user state

### 💸 Payments
- Real-time P2P transfers
- Self-transfer protection (blocked)
- Sufficient balance enforcement
- All failures logged automatically

</td>
<td width="50%" valign="top">

### 📊 Dashboard
- Live balance display
- Quick-send functionality


### 📜 Transaction History
- Full chronological log
- Success / Failed status labels
- Sender & receiver UPI IDs


</td>
</tr>
</table>

---

<div align="center">
<h2>📁 &nbsp; Project Architecture</h2>
</div>

```
🏦 Neo-banks-project / Team 6
│
├── 📂 backend/
│   ├── 🐍 app.py                ← Flask app, all REST routes
│   ├── 🐍 database.py           ← SQLite connection & query helpers
│   ├── 🗄️  neobank.db            ← Persistent SQLite database
│   └── 📋 requirements.txt      ← pip dependencies
│
├── 📂 frontend/
│   ├── 🌐 index.html            ← Login / UPI auth screen
│   ├── 🌐 dashboard.html        ← Main dashboard (balance + actions)
│   ├── 🌐 register.html         ← New account registration
│   ├── 🌐 send_money.html       ← Payment initiation screen
│   ├── 🌐 transactions.html     ← Full transaction history view
│   └── 🎨 style.css             ← Global responsive styles
│
├── 📄 README.md
├── 📄 .gitignore

```

---

<div align="center">
<h2>⚙️ &nbsp; Getting Started</h2>
</div>

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sayandevxyz/Neo-banks-project.git
cd Neo-banks-project/Team\ 6
```

### 2️⃣ Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Start the Flask API Server

```bash
python app.py
```

```
✅  Server running at  →  http://localhost:5000
🟢  API health check  →  http://localhost:5000/api/health
```

### 4️⃣ Launch the Frontend

```bash
# Option A — Direct open
open frontend/index.html

# Option B — VS Code Live Server (recommended)
# Right-click index.html → "Open with Live Server"
```

> 🟢 The **"API Connected"** badge in the UI confirms your backend is reachable.

---

<div align="center">
<h2>🌐 &nbsp; REST API Reference</h2>
</div>

<div align="center">

| # | Method | Endpoint | Description | Protected |
|:-:|:------:|:---------|:------------|:---------:|
| 1 | `GET` | `/api/health` | 💚 Server liveness check | ◻️ Public |
| 2 | `GET` | `/api/dashboard` | 📊 Aggregate platform stats | ◻️ Public |
| 3 | `GET` | `/api/users` | 👥 Fetch all users | ◻️ Public |
| 4 | `POST` | `/api/users/create` | ➕ Register new account | ◻️ Public |
| 5 | `POST` | `/api/users/login` | 🔐 Login by UPI ID | ◻️ Public |
| 6 | `POST` | `/api/users/balance` | 💰 Check user balance | 🔒 PIN |
| 7 | `POST` | `/api/payments/send` | 💸 Initiate transfer | 🔒 PIN |
| 8 | `POST` | `/api/transactions` | 📜 Last N transactions | 🔒 PIN |
| 9 | `GET` | `/api/transactions/all` | 📋 All platform transactions | ◻️ Public |

</div>

---

<div align="center">
<h2>🗄️ &nbsp; Database Schema</h2>
</div>

```sql
-- ┌─────────────────────────────────────────────────────┐
-- │                     users                           │
-- └─────────────────────────────────────────────────────┘
CREATE TABLE users (
    id         INTEGER   PRIMARY KEY AUTOINCREMENT,
    name       TEXT      NOT NULL,
    upi_id     TEXT      NOT NULL UNIQUE,       -- e.g. sayan@okicici
    balance    REAL      NOT NULL DEFAULT 0.0
                         CHECK(balance >= 0),   -- never goes negative
    pin        TEXT      NOT NULL,              -- 4-digit PIN
    created_at DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ┌─────────────────────────────────────────────────────┐
-- │                   transactions                      │
-- └─────────────────────────────────────────────────────┘
CREATE TABLE transactions (
    id           INTEGER   PRIMARY KEY AUTOINCREMENT,
    sender_upi   TEXT      NOT NULL,
    receiver_upi TEXT      NOT NULL,
    amount       REAL      NOT NULL CHECK(amount > 0),
    status       TEXT      NOT NULL CHECK(status IN ('Success', 'Failed')),
    note         TEXT      DEFAULT '',
    timestamp    DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

<div align="center">
<h2>🛡️ &nbsp; Validation Rules</h2>
</div>

| ✅ Check | 📐 Rule | ❌ Failure Behaviour |
|:--------|:--------|:--------------------|
| UPI Format | Must match `^\w+@\w+$` regex | Request rejected |
| PIN Strength | Exactly 4 digits | Request rejected |
| Balance Check | Sender balance ≥ transfer amount | Logged as `Failed` |
| Self-Transfer | Sender UPI ≠ Receiver UPI | Blocked at API level |
| Non-Negative Balance | DB `CHECK(balance >= 0)` constraint | DB constraint error |
| Audit Logging | Every failed transaction is stored | Full audit trail |

---

<div align="center">
<h2>🧪 &nbsp; Sample Test Accounts</h2>
</div>

<div align="center">

| 👤 User | 🔑 UPI ID | 🏦 Bank Handle |
|:--------|:----------|:--------------|
| Sayan Mondal | `sayan@okicici` | ICICI (`@okicici`) |
| Team 6 | `team6@ybl` | Yes Bank / PhonePe (`@ybl`) |
| Test Account | `csbs@okhdfcbank` | HDFC Bank (`@okhdfcbank`) |

</div>

> 💡 Enter any of these on the **Login screen** to instantly explore the simulator — no registration needed.

---

<div align="center">
<h2>🛠️ &nbsp; Tech Stack</h2>
</div>

<div align="center">
<img src="https://skillicons.dev/icons?i=python,flask,sqlite,html,css,js,git,github,vscode&theme=dark" />
</div>

<br/>

<div align="center">

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| 🔙 Backend | Python + Flask | REST API server |
| 🗄️ Database | SQLite | Persistent local storage |
| 🖥️ Frontend | HTML + CSS + Vanilla JS | Responsive browser UI |
| 🔧 Dev Tools | VS Code + Git | Development & version control |

</div>

---

<div align="center">
<h2>👑 &nbsp; Team Lead</h2>
</div>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=soft&color=0:0f0c29,50:302b63,100:24243e&height=130&text=Sayan%20Mondal&fontSize=40&fontColor=7eb3ff&desc=Team%20Leader%20%7C%20Team%206%20%7C%20Full-Stack%20Developer&descColor=aaaaaa&descSize=14&descAlignY=75&animation=twinkling" width="60%"/>

<br/><br/>

[![GitHub Follow](https://img.shields.io/github/followers/Sayandevxyz?label=Follow%20%40Sayandevxyz&style=for-the-badge&logo=github&color=0f0c29)](https://github.com/Sayandevxyz)
&nbsp;
[![Visit Profile](https://img.shields.io/badge/Visit%20Profile-github.com%2FSayandevxyz-7eb3ff?style=for-the-badge&logo=github)](https://github.com/Sayandevxyz)

<br/>

<a href="https://github.com/Sayandevxyz">
  <img height="160" src="https://github-readme-stats.vercel.app/api?username=Sayandevxyz&show_icons=true&theme=midnight-purple&hide_border=true&bg_color=0f0c29&title_color=7eb3ff&icon_color=7eb3ff&text_color=cccccc" />
  &nbsp;
  <img height="160" src="https://github-readme-streak-stats.herokuapp.com?user=Sayandevxyz&theme=midnight-purple&hide_border=true&background=0f0c29&ring=7eb3ff&fire=ff6b9d&currStreakLabel=7eb3ff" />
</a>

</div>

---

<div align="center">
<h2>🤝 &nbsp; Contributing</h2>
</div>

We welcome contributions from the community! To get started:

```bash
# 1. Fork this repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Neo-banks-project.git

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git add .
git commit -m "✨ Add: your feature description"

# 5. Push and open a Pull Request
git push origin feature/your-feature-name
```

> 📌 Please follow the existing code style and include a brief description in your PR.

---

<div align="center">
<h2>📜 &nbsp; License</h2>
</div>

<div align="center">

This project is licensed under the **MIT License** — free to use, modify, and distribute.

```
MIT License © 2026 Sayan Mondal & Team 6
```

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=130&section=footer&text=⭐%20Star%20the%20repo%20if%20you%20found%20it%20useful!&fontSize=16&fontColor=7eb3ff&animation=fadeIn" width="100%"/>

<br/>

**Made with 💙 by Team 6 &nbsp;|&nbsp; Led by [Sayan Mondal](https://github.com/Sayandevxyz)**

<img src="https://img.shields.io/github/stars/Sayandevxyz/Neo-banks-project?style=social" />
&nbsp;
<img src="https://img.shields.io/github/forks/Sayandevxyz/Neo-banks-project?style=social" />

</div>
