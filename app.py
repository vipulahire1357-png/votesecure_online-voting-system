"""
Online Voting System
Author: Vipul Ahire
Tech Stack: Python (Flask) + SQLite
"""

import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = "voting_system_secret_key_2024"

DATABASE = "database.db"

# ─────────────────────────────────────────────
# DATABASE HELPERS
# ─────────────────────────────────────────────

def get_db():
    """Open a database connection tied to the request context."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_db(sql, args=(), one=False):
    """Run a SELECT query and return rows."""
    cur = get_db().execute(sql, args)
    rows = cur.fetchall()
    return (rows[0] if rows else None) if one else rows


def modify_db(sql, args=()):
    """Run an INSERT / UPDATE / DELETE and commit."""
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur.lastrowid


def log_action(action: str):
    """Append an entry to the audit log."""
    modify_db(
        "INSERT INTO audit_log (action, timestamp) VALUES (?, ?)",
        (action, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )


# ─────────────────────────────────────────────
# DATABASE INITIALISATION
# ─────────────────────────────────────────────

def init_db():
    """Create all tables if they do not already exist."""
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(
        """
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
        """
    )
    db.commit()
    db.close()


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────

@app.route("/")
def index():
    stats = {
        "elections":  query_db("SELECT COUNT(*) AS c FROM elections",  one=True)["c"],
        "voters":     query_db("SELECT COUNT(*) AS c FROM voters",     one=True)["c"],
        "candidates": query_db("SELECT COUNT(*) AS c FROM candidates", one=True)["c"],
        "votes":      query_db("SELECT COUNT(*) AS c FROM votes",      one=True)["c"],
    }
    recent_elections = query_db(
        "SELECT * FROM elections ORDER BY id DESC LIMIT 5"
    )
    return render_template("index.html", stats=stats, recent_elections=recent_elections)


# ─────────────────────────────────────────────
# ELECTIONS
# ─────────────────────────────────────────────

@app.route("/elections")
def elections():
    all_elections = query_db("SELECT * FROM elections ORDER BY date DESC")
    return render_template("elections.html", elections=all_elections)


@app.route("/add_election", methods=["GET", "POST"])
def add_election():
    if request.method == "POST":
        name   = request.form["name"].strip()
        date   = request.form["date"].strip()
        status = request.form["status"]

        if not name or not date:
            flash("All fields are required.", "error")
            return redirect(url_for("add_election"))

        modify_db(
            "INSERT INTO elections (name, date, status) VALUES (?, ?, ?)",
            (name, date, status),
        )
        log_action(f"Election created: '{name}' on {date} (status: {status})")
        flash(f"Election '{name}' created successfully!", "success")
        return redirect(url_for("elections"))

    return render_template("add_election.html")


@app.route("/update_election_status/<int:election_id>", methods=["POST"])
def update_election_status(election_id):
    new_status = request.form["status"]
    election   = query_db("SELECT * FROM elections WHERE id = ?", (election_id,), one=True)
    if not election:
        flash("Election not found.", "error")
        return redirect(url_for("elections"))

    modify_db("UPDATE elections SET status = ? WHERE id = ?", (new_status, election_id))
    log_action(f"Election '{election['name']}' status changed to '{new_status}'")
    flash("Election status updated.", "success")
    return redirect(url_for("elections"))


# ─────────────────────────────────────────────
# VOTERS
# ─────────────────────────────────────────────

@app.route("/voters")
def voters():
    all_voters = query_db("SELECT * FROM voters ORDER BY id DESC")
    return render_template("voters.html", voters=all_voters)


@app.route("/add_voter", methods=["GET", "POST"])
def add_voter():
    if request.method == "POST":
        name  = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()

        if not name or not email or not phone:
            flash("All fields are required.", "error")
            return redirect(url_for("add_voter"))

        existing = query_db("SELECT id FROM voters WHERE email = ?", (email,), one=True)
        if existing:
            flash("A voter with this email is already registered.", "error")
            return redirect(url_for("add_voter"))

        modify_db(
            "INSERT INTO voters (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone),
        )
        log_action(f"Voter registered: {name} ({email})")
        flash(f"Voter '{name}' registered successfully!", "success")
        return redirect(url_for("voters"))

    return render_template("add_voter.html")


@app.route("/verify_voter/<int:voter_id>", methods=["POST"])
def verify_voter(voter_id):
    voter = query_db("SELECT * FROM voters WHERE id = ?", (voter_id,), one=True)
    if not voter:
        flash("Voter not found.", "error")
        return redirect(url_for("voters"))

    modify_db("UPDATE voters SET is_verified = 1 WHERE id = ?", (voter_id,))
    log_action(f"Voter verified: {voter['name']} ({voter['email']})")
    flash(f"Voter '{voter['name']}' has been verified.", "success")
    return redirect(url_for("voters"))


# ─────────────────────────────────────────────
# CANDIDATES
# ─────────────────────────────────────────────

@app.route("/candidates")
def candidates():
    all_candidates = query_db(
        """
        SELECT c.*, e.name AS election_name
        FROM candidates c
        JOIN elections e ON c.election_id = e.id
        ORDER BY c.id DESC
        """
    )
    return render_template("candidates.html", candidates=all_candidates)


@app.route("/add_candidate", methods=["GET", "POST"])
def add_candidate():
    all_elections = query_db("SELECT * FROM elections WHERE status != 'completed'")

    if request.method == "POST":
        name        = request.form["name"].strip()
        party       = request.form["party"].strip()
        election_id = request.form["election_id"]

        if not name or not election_id:
            flash("Candidate name and election are required.", "error")
            return redirect(url_for("add_candidate"))

        modify_db(
            "INSERT INTO candidates (name, party, election_id) VALUES (?, ?, ?)",
            (name, party or None, election_id),
        )
        election = query_db("SELECT name FROM elections WHERE id = ?", (election_id,), one=True)
        log_action(f"Candidate added: {name} ({party or 'Independent'}) to election '{election['name']}'")
        flash(f"Candidate '{name}' added successfully!", "success")
        return redirect(url_for("candidates"))

    return render_template("add_candidate.html", elections=all_elections)


# ─────────────────────────────────────────────
# VOTING
# ─────────────────────────────────────────────

@app.route("/vote/<int:election_id>", methods=["GET", "POST"])
def vote(election_id):
    election = query_db("SELECT * FROM elections WHERE id = ?", (election_id,), one=True)
    if not election:
        flash("Election not found.", "error")
        return redirect(url_for("elections"))

    if election["status"] != "active":
        flash("Voting is only allowed for active elections.", "error")
        return redirect(url_for("elections"))

    candidates_list = query_db(
        "SELECT * FROM candidates WHERE election_id = ?", (election_id,)
    )

    if request.method == "POST":
        voter_email  = request.form["voter_email"].strip().lower()
        candidate_id = request.form.get("candidate_id")

        voter = query_db("SELECT * FROM voters WHERE email = ?", (voter_email,), one=True)
        if not voter:
            flash("No voter found with that email. Please register first.", "error")
            return render_template("vote.html", election=election, candidates=candidates_list)

        if not voter["is_verified"]:
            flash("Your account is not verified. Please contact the administrator.", "error")
            return render_template("vote.html", election=election, candidates=candidates_list)

        already_voted = query_db(
            "SELECT id FROM votes WHERE voter_id = ? AND election_id = ?",
            (voter["id"], election_id),
            one=True,
        )
        if already_voted:
            flash("You have already voted in this election.", "error")
            return render_template("vote.html", election=election, candidates=candidates_list)

        if not candidate_id:
            flash("Please select a candidate.", "error")
            return render_template("vote.html", election=election, candidates=candidates_list)

        modify_db(
            "INSERT INTO votes (voter_id, candidate_id, election_id) VALUES (?, ?, ?)",
            (voter["id"], candidate_id, election_id),
        )
        log_action(
            f"Vote cast by voter ID {voter['id']} in election '{election['name']}'"
        )
        flash("Your vote has been recorded successfully! 🎉", "success")
        return redirect(url_for("elections"))

    return render_template("vote.html", election=election, candidates=candidates_list)


# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────

@app.route("/results/<int:election_id>")
def results(election_id):
    election = query_db("SELECT * FROM elections WHERE id = ?", (election_id,), one=True)
    if not election:
        flash("Election not found.", "error")
        return redirect(url_for("elections"))

    if election["status"] != "completed":
        flash("Results are only available after the election is completed.", "error")
        return redirect(url_for("elections"))

    tally = query_db(
        """
        SELECT c.id, c.name, c.party,
               COUNT(v.id) AS vote_count
        FROM candidates c
        LEFT JOIN votes v ON c.id = v.candidate_id
        WHERE c.election_id = ?
        GROUP BY c.id
        ORDER BY vote_count DESC
        """,
        (election_id,),
    )

    total_votes = sum(row["vote_count"] for row in tally)
    winner = tally[0] if tally else None

    return render_template(
        "results.html",
        election=election,
        tally=tally,
        total_votes=total_votes,
        winner=winner,
    )


# ─────────────────────────────────────────────
# AUDIT LOG
# ─────────────────────────────────────────────

@app.route("/audit")
def audit():
    logs = query_db("SELECT * FROM audit_log ORDER BY id DESC")
    return render_template("audit.html", logs=logs)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("✅ Database initialised.")
    print("🚀 Starting Online Voting System…")
    print("🌐 Open: http://127.0.0.1:5000/")
    app.run(debug=True)
