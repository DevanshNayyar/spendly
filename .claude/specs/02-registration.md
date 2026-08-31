# Spec: Registration

## Overview
This step implements the `POST /register` handler so new users can actually create an account instead of hitting a GET-only stub. It builds directly on the database layer from Step 1 (`users` table, `get_db()`, password hashing) and turns the existing `register.html` form into a working signup flow: validate input, check for a duplicate email, hash the password, insert the user, and start a logged-in session. This is the first of the auth steps in the Spendly roadmap and unblocks login/logout/profile work later.

## Depends on
- Step 1 — Database setup (`database/db.py`: `get_db()`, `init_db()`, `users` table with `email` UNIQUE, `password_hash`)

## Routes
- `GET /register` — render the signup form — public (already implemented, no change to behavior)
- `POST /register` — validate form data, create the user, log them in, redirect — public

## Database changes
No database changes. The `users` table (id, name, email, password_hash, created_at) already supports registration as defined in `database/db.py`. No new columns or tables needed.

## Templates
- **Create:** none
- **Modify:**
  - `templates/register.html` — change form `action="/register"` to `action="{{ url_for('register') }}"`; render `{{ error }}` for validation/duplicate-email failures (block already exists, just needs real data)

## Files to change
- `app.py` — change `register()` to accept `GET` and `POST`; add validation, duplicate-email check, password hashing, insert, session creation, redirect on success
- `database/db.py` — add a `create_user(name, email, password_hash)` helper (and a `get_user_by_email(email)` helper for the duplicate check) so no DB logic lives in `app.py`
- `templates/register.html` — fix hardcoded form action to use `url_for()`

## Files to create
None

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already available and used in `database/db.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No new routes beyond `POST /register` on the existing `/register` path
- Validate on the server even though HTML5 `required` attributes exist client-side
- On duplicate email or validation failure, re-render `register.html` with `error` set — do not redirect to an error page
- On success, store the new user's id in the Flask session and redirect to `/` (profile/dashboard route is still a stub per Step 4)

## Definition of done
- [ ] Submitting the register form with a new name/email/password creates a row in `users` with a hashed (not plaintext) password
- [ ] Submitting with an email that already exists re-renders `register.html` showing an error, and does not create a duplicate row
- [ ] Submitting with a missing field re-renders `register.html` showing an error, and does not create a row
- [ ] After successful registration, the session contains the new user's id
- [ ] `register.html` form posts via `url_for('register')`, not a hardcoded path
- [ ] App starts and `/register` (GET and POST) works on port 5001 without errors
