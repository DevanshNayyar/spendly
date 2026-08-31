from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import (
    get_db,
    init_db,
    seed_db,
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_expense_summary,
    get_recent_expenses,
    get_category_breakdown,
)

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-change-in-production"  # dev-only, not for production

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html", error="All fields are required.")

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    if get_user_by_email(email):
        return render_template("register.html", error="An account with that email already exists.")

    password_hash = generate_password_hash(password)
    user_id = create_user(name, email, password_hash)

    session["user_id"] = user_id
    return redirect(url_for("landing"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = get_user_by_email(email)

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password")

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user_row = get_user_by_id(user_id)
    summary_row = get_expense_summary(user_id)
    recent_rows = get_recent_expenses(user_id, limit=8)
    breakdown_rows = get_category_breakdown(user_id)

    initials = "".join(part[0] for part in user_row["name"].split()[:2]).upper()

    user = {
        "name": user_row["name"],
        "email": user_row["email"],
        "initials": initials,
        "member_since": datetime.strptime(
            user_row["created_at"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%d %b %Y"),
    }

    recent_expenses = [
        {
            "date": datetime.strptime(row["date"], "%Y-%m-%d").strftime("%d %b %Y"),
            "category": row["category"],
            "amount": row["amount"],
            "description": row["description"],
        }
        for row in recent_rows
    ]

    top_category = breakdown_rows[0]["category"] if breakdown_rows else "—"
    max_category_total = breakdown_rows[0]["total"] if breakdown_rows else 0
    category_breakdown = [
        {
            "category": row["category"],
            "total": row["total"],
            "percent": round((row["total"] / max_category_total) * 100) if max_category_total else 0,
        }
        for row in breakdown_rows
    ]

    return render_template(
        "profile.html",
        user=user,
        expense_count=summary_row["count"],
        total_spent=summary_row["total"],
        recent_expenses=recent_expenses,
        top_category=top_category,
        category_breakdown=category_breakdown,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
