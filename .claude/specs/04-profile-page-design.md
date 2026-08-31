# Spec: Profile Page Design

## Overview
This step replaces the `GET /profile` stub with a real page that shows the logged-in user their account details (name, email, member-since date) and a summary of their expense activity. It builds on the `users` table and session pattern established in Steps 1–3 (database setup, registration, login/logout). This is the first "logged-in area" page in the Spendly roadmap — it establishes the pattern for requiring authentication on a route, which the upcoming expense CRUD steps (7–9) will reuse. No expense creation/editing happens here; this step is display-only.

## Depends on
- Step 1 — Database setup (`users` and `expenses` tables, `get_db()`)
- Step 2 — Registration (`session["user_id"]` pattern)
- Step 3 — Login and Logout (session-based auth, `logout()`)

## Routes
- `GET /profile` — render the logged-in user's profile with account info and expense summary — logged-in only. If no `session["user_id"]`, redirect to `GET /login`.

No other routes change.

## Database changes
No schema changes. `database/db.py` already has `users` (id, name, email, password_hash, created_at) and `expenses` (id, user_id, amount, category, date, description, created_at) tables.

New read-only helper functions needed in `database/db.py` (no DB logic in `app.py`):
- `get_user_by_id(user_id)` — `SELECT * FROM users WHERE id = ?`, returns one row or `None`
- `get_expense_summary(user_id)` — returns total spend and expense count for the user, e.g. `SELECT COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ?`
- `get_recent_expenses(user_id, limit=5)` — `SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?`, for a "recent activity" list on the profile page

## Templates
- **Create:** `templates/profile.html` — extends `base.html`; shows name, email, "member since" (formatted `created_at`), total expenses count, total amount spent, and a short list (up to 5) of recent expenses (date, category, amount, description). Shows an empty-state message if the user has no expenses yet.
- **Modify:** `templates/base.html` — add a "Profile" link in `nav-links` next to "Sign out" when `session.user_id` is set, using `url_for('profile')`

## Files to change
- `app.py` — implement `profile()`: check `session.get("user_id")`, redirect to `login` if absent, else fetch user + summary + recent expenses and render `profile.html`
- `database/db.py` — add `get_user_by_id`, `get_expense_summary`, `get_recent_expenses` helpers
- `templates/base.html` — add profile nav link for logged-in users

## Files to create
- `templates/profile.html`
- `static/css/profile.css` — page-specific styles (linked via a `{% block head %}` in `profile.html`, per the project convention of one CSS file per page-specific template)

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (unaffected by this step — no password handling here)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No DB logic inline in `app.py` — all queries go through `database/db.py` helpers
- `profile()` must not render `profile.html` for an anonymous visitor — redirect to `url_for('login')` instead of returning an error page
- Do not expose `password_hash` to the template — only pass the fields the page needs
- Format `created_at` and expense `date` values for display in the template/route, not via inline string hacks in the template

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in (e.g. as the seeded demo user) shows the user's name, email, and member-since date
- [ ] The profile page shows the correct total expense count and total amount spent for that user
- [ ] The profile page lists up to 5 most recent expenses, most recent first
- [ ] A user with zero expenses sees an empty-state message instead of an error
- [ ] The navbar shows a "Profile" link when logged in, using `url_for('profile')` (no hardcoded URL)
- [ ] App starts and `/profile` works on port 5001 without errors
