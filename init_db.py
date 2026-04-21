"""
init_db.py — Demo Database Setup Script
Online Voting System | Author: Vipul Ahire

Run:  python init_db.py
"""

import sqlite3
from datetime import datetime

DATABASE = "database.db"

# ─────────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────────

ELECTIONS = [
    (1, "Student Council Election 2024", "2024-11-15", "completed"),
    (2, "Club President Election 2025",  "2025-06-20", "active"),
    (3, "Cultural Fest Committee 2025",  "2025-09-10", "upcoming"),
]

# (id, name, email, phone, is_verified)
VOTERS = [
    (1,  "Vipul Ahire",      "vipul.ahire@college.edu",    "9876543210", 1),
    (2,  "Sneha Patil",      "sneha.patil@college.edu",    "9823456781", 1),
    (3,  "Rahul Deshmukh",   "rahul.deshmukh@college.edu", "9812345672", 1),
    (4,  "Priya Kulkarni",   "priya.kulkarni@college.edu", "9801234563", 1),
    (5,  "Arjun Sharma",     "arjun.sharma@college.edu",   "9790123454", 1),
    (6,  "Neha Joshi",       "neha.joshi@college.edu",     "9779012345", 1),
    (7,  "Amit Verma",       "amit.verma@college.edu",     "9768901236", 1),
    (8,  "Pooja Nair",       "pooja.nair@college.edu",     "9757890127", 1),
    (9,  "Karan Mehta",      "karan.mehta@college.edu",    "9746789018", 1),
    (10, "Divya Reddy",      "divya.reddy@college.edu",    "9735678909", 1),
    (11, "Rohan Gupta",      "rohan.gupta@college.edu",    "9724567890", 0),  # unverified
    (12, "Ankita Singh",     "ankita.singh@college.edu",   "9713456781", 0),  # unverified
    (13, "Vikram Yadav",     "vikram.yadav@college.edu",   "9702345672", 1),
    (14, "Meera Iyer",       "meera.iyer@college.edu",     "9691234563", 1),
    (15, "Suresh Bansode",   "suresh.bansode@college.edu", "9680123454", 0),  # unverified
]

# (id, name, party, election_id)
CANDIDATES = [
    # Election 1 — Student Council (completed)
    (1,  "Aditya Rane",     "Progressive Students Front", 1),
    (2,  "Kavya Deshpande", "United Youth Alliance",      1),
    (3,  "Nikhil Pawar",    "Campus First Party",         1),
    (4,  "Shruti Gaikwad",  "Independent",                1),

    # Election 2 — Club President (active)
    (5,  "Tejas Kulkarni",  "Tech Enthusiasts Club",      2),
    (6,  "Rutuja Shinde",   "Creative Circle",            2),
    (7,  "Omkar Jadhav",    "Sports & Culture Wing",      2),
    (8,  "Pallavi More",    "Independent",                2),
    (9,  "Sandesh Nikam",   "Innovation Hub",             2),

    # Election 3 — Cultural Fest (upcoming — no votes)
    (10, "Ishaan Bhosale",  "Arts Council",               3),
    (11, "Tanvi Waghmare",  "Drama & Music Society",      3),
    (12, "Yash Sonawane",   "Independent",                3),
]

# Votes: only verified voters, only completed/active elections
# Distribution designed to produce a clear winner per election
# (voter_id, candidate_id, election_id)
VOTES = [
    # ── Election 1 (completed) — Aditya Rane wins ──
    (1,  1, 1),   # Vipul      → Aditya Rane
    (2,  2, 1),   # Sneha      → Kavya Deshpande
    (3,  1, 1),   # Rahul      → Aditya Rane
    (4,  3, 1),   # Priya      → Nikhil Pawar
    (5,  1, 1),   # Arjun      → Aditya Rane
    (6,  4, 1),   # Neha       → Shruti Gaikwad
    (7,  1, 1),   # Amit       → Aditya Rane
    (8,  2, 1),   # Pooja      → Kavya Deshpande
    (9,  3, 1),   # Karan      → Nikhil Pawar
    (10, 1, 1),   # Divya      → Aditya Rane
    (13, 2, 1),   # Vikram     → Kavya Deshpande
    (14, 1, 1),   # Meera      → Aditya Rane

    # ── Election 2 (active) — Tejas Kulkarni leads ──
    (1,  5, 2),   # Vipul      → Tejas Kulkarni
    (2,  6, 2),   # Sneha      → Rutuja Shinde
    (3,  5, 2),   # Rahul      → Tejas Kulkarni
    (4,  7, 2),   # Priya      → Omkar Jadhav
    (5,  5, 2),   # Arjun      → Tejas Kulkarni
    (6,  8, 2),   # Neha       → Pallavi More
    (7,  9, 2),   # Amit       → Sandesh Nikam
    (8,  6, 2),   # Pooja      → Rutuja Shinde
    (13, 5, 2),   # Vikram     → Tejas Kulkarni
    (14, 7, 2),   # Meera      → Omkar Jadhav
    # unverified voters 11,12,15 intentionally excluded
]


def ts(date_str: str, time_str: str) -> str:
    """Return a formatted timestamp string."""
    return f"{date_str} {time_str}"


# ─────────────────────────────────────────────
# AUDIT LOG ENTRIES
# ─────────────────────────────────────────────

AUDIT_LOGS = []

# Voter registration logs
VOTER_REG_DATES = [
    "2024-10-01 09:15:00", "2024-10-02 10:30:00", "2024-10-03 11:00:00",
    "2024-10-04 09:45:00", "2024-10-05 14:20:00", "2024-10-06 08:55:00",
    "2024-10-07 13:10:00", "2024-10-08 16:05:00", "2024-10-09 10:00:00",
    "2024-10-10 11:30:00", "2024-10-11 09:20:00", "2024-10-12 14:45:00",
    "2024-10-13 08:30:00", "2024-10-14 15:00:00", "2024-10-15 12:00:00",
]

for i, voter in enumerate(VOTERS):
    AUDIT_LOGS.append((
        f"Voter registered: {voter[1]} ({voter[2]})",
        VOTER_REG_DATES[i]
    ))

# Verification logs (only verified voters)
VERIFY_DATES = [
    "2024-10-05 10:00:00", "2024-10-06 10:00:00", "2024-10-07 10:00:00",
    "2024-10-08 10:00:00", "2024-10-09 10:00:00", "2024-10-10 10:00:00",
    "2024-10-11 10:00:00", "2024-10-12 10:00:00", "2024-10-13 10:00:00",
    "2024-10-14 10:00:00", "2024-10-16 10:00:00", "2024-10-17 10:00:00",
]
verified_voters = [v for v in VOTERS if v[4] == 1]
for i, voter in enumerate(verified_voters):
    AUDIT_LOGS.append((
        f"Voter verified: {voter[1]} ({voter[2]})",
        VERIFY_DATES[i]
    ))

# Election creation logs
AUDIT_LOGS += [
    ("Election created: 'Student Council Election 2024' on 2024-11-15 (status: completed)", "2024-10-20 09:00:00"),
    ("Election created: 'Club President Election 2025' on 2025-06-20 (status: active)",     "2025-01-15 10:00:00"),
    ("Election created: 'Cultural Fest Committee 2025' on 2025-09-10 (status: upcoming)",   "2025-03-01 11:00:00"),
]

# Candidate addition logs
CANDIDATE_LOGS = [
    ("Candidate added: Aditya Rane (Progressive Students Front) to election 'Student Council Election 2024'",  "2024-10-25 09:00:00"),
    ("Candidate added: Kavya Deshpande (United Youth Alliance) to election 'Student Council Election 2024'",   "2024-10-25 09:10:00"),
    ("Candidate added: Nikhil Pawar (Campus First Party) to election 'Student Council Election 2024'",         "2024-10-25 09:20:00"),
    ("Candidate added: Shruti Gaikwad (Independent) to election 'Student Council Election 2024'",              "2024-10-25 09:30:00"),
    ("Candidate added: Tejas Kulkarni (Tech Enthusiasts Club) to election 'Club President Election 2025'",     "2025-01-20 10:00:00"),
    ("Candidate added: Rutuja Shinde (Creative Circle) to election 'Club President Election 2025'",            "2025-01-20 10:10:00"),
    ("Candidate added: Omkar Jadhav (Sports & Culture Wing) to election 'Club President Election 2025'",       "2025-01-20 10:20:00"),
    ("Candidate added: Pallavi More (Independent) to election 'Club President Election 2025'",                 "2025-01-20 10:30:00"),
    ("Candidate added: Sandesh Nikam (Innovation Hub) to election 'Club President Election 2025'",             "2025-01-20 10:40:00"),
]
AUDIT_LOGS += CANDIDATE_LOGS

# Vote casting logs — Election 1 (completed)
VOTE_DATES_E1 = [
    "2024-11-15 09:05:00", "2024-11-15 09:18:00", "2024-11-15 09:32:00",
    "2024-11-15 09:47:00", "2024-11-15 10:01:00", "2024-11-15 10:15:00",
    "2024-11-15 10:30:00", "2024-11-15 10:44:00", "2024-11-15 11:00:00",
    "2024-11-15 11:15:00", "2024-11-15 11:30:00", "2024-11-15 11:45:00",
]
e1_voter_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14]
for i, vid in enumerate(e1_voter_ids):
    voter = next(v for v in VOTERS if v[0] == vid)
    AUDIT_LOGS.append((
        f"Vote cast by voter ID {vid} in election 'Student Council Election 2024'",
        VOTE_DATES_E1[i]
    ))

# Vote casting logs — Election 2 (active)
VOTE_DATES_E2 = [
    "2025-06-20 08:10:00", "2025-06-20 08:25:00", "2025-06-20 08:40:00",
    "2025-06-20 08:55:00", "2025-06-20 09:10:00", "2025-06-20 09:25:00",
    "2025-06-20 09:40:00", "2025-06-20 09:55:00", "2025-06-20 10:10:00",
    "2025-06-20 10:25:00",
]
e2_voter_ids = [1, 2, 3, 4, 5, 6, 7, 8, 13, 14]
for i, vid in enumerate(e2_voter_ids):
    AUDIT_LOGS.append((
        f"Vote cast by voter ID {vid} in election 'Club President Election 2025'",
        VOTE_DATES_E2[i]
    ))

# Status change logs
AUDIT_LOGS += [
    ("Election 'Student Council Election 2024' status changed to 'completed'", "2024-11-15 18:00:00"),
    ("Election 'Club President Election 2025' status changed to 'active'",     "2025-06-19 08:00:00"),
]

# Sort all audit logs by timestamp ascending
AUDIT_LOGS.sort(key=lambda x: x[1])


# ─────────────────────────────────────────────
# MAIN SETUP FUNCTION
# ─────────────────────────────────────────────

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")

    # ── Create tables (if not exist) ──────────
    db.executescript("""
        CREATE TABLE IF NOT EXISTS elections (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            date    TEXT    NOT NULL,
            status  TEXT    NOT NULL DEFAULT 'upcoming'
                            CHECK(status IN ('upcoming','active','completed'))
        );

        CREATE TABLE IF NOT EXISTS voters (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            phone       TEXT    NOT NULL,
            is_verified INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS candidates (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            party       TEXT,
            election_id INTEGER NOT NULL,
            FOREIGN KEY (election_id) REFERENCES elections(id)
        );

        CREATE TABLE IF NOT EXISTS votes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id     INTEGER NOT NULL,
            candidate_id INTEGER NOT NULL,
            election_id  INTEGER NOT NULL,
            UNIQUE (voter_id, election_id),
            FOREIGN KEY (voter_id)     REFERENCES voters(id),
            FOREIGN KEY (candidate_id) REFERENCES candidates(id),
            FOREIGN KEY (election_id)  REFERENCES elections(id)
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            action    TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)

    # ── Insert elections ──────────────────────
    db.executemany(
        "INSERT OR IGNORE INTO elections (id, name, date, status) VALUES (?, ?, ?, ?)",
        ELECTIONS
    )

    # ── Insert voters ─────────────────────────
    db.executemany(
        "INSERT OR IGNORE INTO voters (id, name, email, phone, is_verified) VALUES (?, ?, ?, ?, ?)",
        VOTERS
    )

    # ── Insert candidates ─────────────────────
    db.executemany(
        "INSERT OR IGNORE INTO candidates (id, name, party, election_id) VALUES (?, ?, ?, ?)",
        CANDIDATES
    )

    # ── Insert votes (safe: only verified + valid elections) ──
    valid_voter_ids    = {v[0] for v in VOTERS if v[4] == 1}
    valid_election_ids = {e[0] for e in ELECTIONS if e[3] in ("active", "completed")}

    safe_votes = [
        (voter_id, cand_id, elec_id)
        for voter_id, cand_id, elec_id in VOTES
        if voter_id in valid_voter_ids and elec_id in valid_election_ids
    ]
    db.executemany(
        "INSERT OR IGNORE INTO votes (voter_id, candidate_id, election_id) VALUES (?, ?, ?)",
        safe_votes
    )

    # ── Insert audit logs ─────────────────────
    # Clear existing logs to avoid duplicates on re-run
    db.execute("DELETE FROM audit_log")
    db.executemany(
        "INSERT INTO audit_log (action, timestamp) VALUES (?, ?)",
        AUDIT_LOGS
    )

    db.commit()
    db.close()


# ─────────────────────────────────────────────
# SUMMARY REPORT
# ─────────────────────────────────────────────

def print_summary():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    print("\n" + "═" * 52)
    print("  ✅  VoteSecure — Demo Database Ready")
    print("═" * 52)

    tables = ["elections", "voters", "candidates", "votes", "audit_log"]
    for table in tables:
        count = db.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"]
        print(f"  {'📋' if table == 'audit_log' else '📊'} {table:<15} {count:>3} rows")

    print("─" * 52)

    # Per-election vote summary
    print("\n  🗳️  Vote Distribution\n")
    elections = db.execute("SELECT * FROM elections").fetchall()
    for e in elections:
        print(f"  [{e['status'].upper():^10}]  {e['name']}")
        if e["status"] == "upcoming":
            print("               (No votes — upcoming election)\n")
            continue
        candidates = db.execute(
            """SELECT c.name, c.party, COUNT(v.id) AS votes
               FROM candidates c
               LEFT JOIN votes v ON c.id = v.candidate_id
               WHERE c.election_id = ?
               GROUP BY c.id
               ORDER BY votes DESC""",
            (e["id"],)
        ).fetchall()
        for c in candidates:
            bar = "█" * c["votes"]
            print(f"    {c['name']:<22} {bar:<14} {c['votes']} vote(s)")
        print()

    print("  🌐  Open: http://127.0.0.1:5000/")
    print("═" * 52 + "\n")
    db.close()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n⏳ Initialising demo database…")
    init_db()
    print_summary()
