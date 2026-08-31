# Spec: Login and Logout

## Overview
This step implements the `POST /login` handler and the `GET /logout` route so users can actually authenticate and end their session, instead of hitting a GET-only login stub and a placeholder logout string. It builds on the `users` table and password hashing from Step 1, and the session-based login pattern already established in Step 2 (registration). This is the second of the auth steps in the Spendly roadmap and unblocks profile/dashboard work later, since those pages will require a logged-in session.

## Depends on
- Step 1 — Database setup (`database/db.py`: `get_db()`, `users` table with `email` UNIQUE, `password_hash`)
- Step 2 — Registration (`create_user`, `get_user_by_email` helpers; `session["user_id"]` pattern established in `POST /register`)

## Routes
- `GET /login` — render the sign-in form — public (already implemented, no change to behavior)
- `POST /login` — validate credentials against the `users` table, start a session, redirect — public
- `GET /logout` — clear the session and redirect to the landing page — logged-in

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at) already supports credential lookup via the existing `get_user_by_email(email)` helper in `database/db.py`. No new columns or tables needed.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — change form `action="/login"` to `action="{{ url_for('login') }}"`; render `{{ error }}` for invalid-credential failures (mirror the `auth-error` block already used in `register.html`)

## Files to change
- `app.py` — change `login()` to accept `GET` and `POST`; add credential validation (look up user by email, verify password hash) and session creation on success; implement `logout()` to clear the session and redirect (replacing the `"Logout — coming in Step 3"` stub string)
- `templates/login.html` — fix hardcoded form action to use `url_for()`

## Files to create
None

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is available alongside `generate_password_hash`, which is already imported from `werkzeug.security` in the codebase.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` for verification — never compare plaintext)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No new routes beyond `POST /login` on the existing `/login` path and `GET /logout`
- Validate on the server even though HTML5 `required` attributes exist client-side
- On unknown email or wrong password, re-render `login.html` with a single generic `error` (e.g. "Invalid email or password") — do not reveal whether the email exists
- On successful login, store the user's id in the Flask session and redirect to `/` (profile/dashboard route is still a stub per Step 4)
- `logout()` must use `session.clear()` (or pop `user_id`) and redirect to `landing`, never return a raw string
- No DB logic inline in `app.py` — credential lookup goes through the existing `get_user_by_email` helper in `database/db.py`

## Definition of done
- [ ] Submitting the login form with a registered user's correct email/password logs them in and redirects to `/`
- [ ] Submitting with a correct email but wrong password re-renders `login.html` showing a generic error, and does not create a session
- [ ] Submitting with an email that doesn't exist re-renders `login.html` showing the same generic error, and does not create a session
- [ ] After successful login, the session contains the user's id
- [ ] Visiting `/logout` while logged in clears the session and redirects to the landing page
- [ ] `login.html` form posts via `url_for('login')`, not a hardcoded path
- [ ] App starts and `/login` (GET and POST) and `/logout` work on port 5001 without errors
