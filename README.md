# 🗳️ VoteSecure — Online Voting System

**Author: Vipul Ahire**  
**Type: DBMS College Project**  
**Tech Stack: Python (Flask) + SQLite**

---

## 📋 Project Overview

VoteSecure is a lightweight, web-based online voting system built as a DBMS project. It demonstrates real-world concepts such as relational database design, CRUD operations, referential integrity, duplicate-vote prevention, and audit logging — all implemented using Flask and SQLite.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏛️ Election Management | Create elections, set dates, manage status (upcoming / active / completed) |
| 👤 Voter Registration | Register voters with name, email, phone; prevent duplicate email registration |
| ✅ Voter Verification | Admin marks voters as verified before they can vote |
| 🧑‍💼 Candidate Management | Add candidates with party affiliation, linked to a specific election |
| 🗳️ Secure Voting | Verified voters cast exactly one vote per election; duplicates are blocked |
| 📊 Results & Tally | Vote counts, percentage bars, and declared winner (only for completed elections) |
| 📜 Audit Trail | Timestamped log of every significant action for full transparency |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 + Flask |
| Database | SQLite (via Python's built-in `sqlite3`) |
| Frontend | HTML5 + CSS3 (Jinja2 templates) |
| Fonts | Google Fonts (Playfair Display + Source Sans 3) |

---

## 🗄️ Database Schema

### `elections`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| name | TEXT | Election title |
| date | TEXT | Date string |
| status | TEXT | upcoming / active / completed |

### `voters`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| name | TEXT | Full name |
| email | TEXT UNIQUE | Login identifier |
| phone | TEXT | Contact number |
| is_verified | INTEGER | 0 = pending, 1 = verified |

### `candidates`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| name | TEXT | Candidate name |
| party | TEXT | Optional affiliation |
| election_id | INTEGER FK | References elections.id |

### `votes`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| voter_id | INTEGER FK | References voters.id |
| candidate_id | INTEGER FK | References candidates.id |
| election_id | INTEGER FK | References elections.id |
| — | UNIQUE | (voter_id, election_id) prevents double-voting |

### `audit_log`
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| action | TEXT | Human-readable description |
| timestamp | TEXT | yyyy-mm-dd HH:MM:SS |

---

## 🔗 Relationships

```
elections  ──< candidates  (one election → many candidates)
elections  ──< votes        (one election → many votes)
voters     ──< votes        (one voter → many elections, 1 vote each)
candidates ──< votes        (one candidate → many votes)
```

---

## 🚀 How to Run

See **[setup_and_run.md](setup_and_run.md)** for full step-by-step instructions.

**Quick start:**
```bash
# 1. Create venv
python -m venv venv && source venv/bin/activate   # Linux/Mac
# python -m venv venv && venv\Scripts\activate    # Windows

# 2. Install Flask
pip install -r requirements.txt

# 3. Run
python app.py

# 4. Open browser
# http://127.0.0.1:5000/
```

---

## 🌐 Routes Reference

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Dashboard / home |
| `/elections` | GET | List all elections |
| `/add_election` | GET, POST | Create election |
| `/update_election_status/<id>` | POST | Change election status |
| `/voters` | GET | List all voters |
| `/add_voter` | GET, POST | Register voter |
| `/verify_voter/<id>` | POST | Mark voter as verified |
| `/candidates` | GET | List all candidates |
| `/add_candidate` | GET, POST | Add candidate |
| `/vote/<election_id>` | GET, POST | Voting page |
| `/results/<election_id>` | GET | View results (completed only) |
| `/audit` | GET | Audit trail |

---

## ⚠️ Limitations

> This is a **college-level demonstration project** and is not intended for real-world production use.

- No authentication / login system (voter identified by email only)
- No password or session security
- No encryption of stored data
- No email verification
- Single-server, no horizontal scaling
- Not suitable for large-scale elections
- No HTTPS enforcement

---

## 📁 Project Structure

```
online_voting_system/
├── app.py               ← Flask application (routes + DB logic)
├── database.db          ← SQLite database (auto-created on first run)
├── requirements.txt     ← Python dependencies (Flask only)
├── setup_and_run.md     ← Step-by-step setup guide
├── README.md            ← This file
├── static/
│   └── style.css        ← All styling (CSS variables, responsive)
└── templates/
    ├── base.html        ← Shared layout (navbar, footer)
    ├── index.html       ← Dashboard
    ├── elections.html   ← Election list
    ├── add_election.html
    ├── voters.html      ← Voter list + verification
    ├── add_voter.html
    ├── candidates.html  ← Candidate list
    ├── add_candidate.html
    ├── vote.html        ← Voting interface
    ├── results.html     ← Results + tally
    └── audit.html       ← Audit log
```

---

*Built with ❤️ by Vipul Ahire*
