# ⚙️ Setup & Run Guide

**Author: Vipul Ahire**  
**Project: Online Voting System (DBMS Project)**

---

## Prerequisites

- Python 3.8 or higher installed
- pip (Python package manager)

Verify Python is installed:
```bash
python --version
```

---

## Step 1 — Extract the Project

Place the `online_voting_system/` folder anywhere on your computer.

```
online_voting_system/
├── app.py
├── init_db.py          ← Demo data script
├── requirements.txt
├── static/style.css
└── templates/  (all .html files)
```

---

## Step 2 — Open Terminal / Command Prompt

Navigate into the project folder:

```bash
cd path\to\online_voting_system
```

---

## Step 3 — Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 — Populate Demo Database (Recommended)

Run the demo data script to pre-fill the database with realistic sample data:

```bash
python init_db.py
```

Expected output:
```
⏳ Initialising demo database…

════════════════════════════════════════════════════
  ✅  VoteSecure — Demo Database Ready
════════════════════════════════════════════════════
  📊 elections          3 rows
  📊 voters            15 rows
  📊 candidates        12 rows
  📊 votes             22 rows
  📋 audit_log         55 rows
────────────────────────────────────────────────────

  🗳️  Vote Distribution

  [COMPLETED]  Student Council Election 2024
    Aditya Rane           ██████         6 vote(s)
    Kavya Deshpande       ███            3 vote(s)
    Nikhil Pawar          ██             2 vote(s)
    Shruti Gaikwad        █              1 vote(s)

  [ ACTIVE ]   Club President Election 2025
    Tejas Kulkarni        ████           4 vote(s)
    ...

  [UPCOMING]   Cultural Fest Committee 2025
               (No votes — upcoming election)

  🌐  Open: http://127.0.0.1:5000/
════════════════════════════════════════════════════
```

---

## Step 6 — Run the Application

```bash
python app.py
```

---

## Step 7 — Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📋 Demo Walkthrough

| What to show | Where |
|-------------|-------|
| Dashboard stats | `/` |
| Election list + statuses | `/elections` |
| Voter list (verified vs unverified) | `/voters` |
| Candidates per election | `/candidates` |
| Cast a vote (use a verified email) | `/vote/2` |
| View completed results | `/results/1` |
| Audit trail | `/audit` |

**Sample verified voter emails for voting:**
```
vipul.ahire@college.edu
sneha.patil@college.edu
rahul.deshmukh@college.edu
arjun.sharma@college.edu
```

---

## 🔄 Reset & Re-populate

```powershell
# Windows PowerShell
del database.db
python init_db.py
python app.py
```
```bash
# macOS / Linux
rm database.db && python init_db.py && python app.py
```

---

## ⚠️ Troubleshooting (Windows)

| Error | Fix |
|-------|-----|
| `source` not recognized | Use `venv\Scripts\Activate.ps1` instead |
| Permission denied on venv | Run `Remove-Item -Recurse -Force venv` then recreate |
| ExecutionPolicy error | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Port already in use | Change `app.run(port=5001)` in `app.py` |

---

*Author: Vipul Ahire*
