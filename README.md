# Gatekeep - Authentication & Authorization Provider

Gatekeep is a login system I'm building myself, from the ground up, so that all my other projects can share it instead of each one having its own separate login page.

Think of it like a bouncer for a group of buildings. Instead of every building hiring its own bouncer, they all share one — and that one bouncer checks IDs at the door and also keeps a list of who's allowed into which rooms.

```
Client Project A ──┐
Client Project B ──┼──> Gatekeep
Client Project C ──┘        │
                             ├── Checks who you are (login)
                             ├── Checks what you're allowed to do (permissions)
                             ├── Hands out short-lived access passes (tokens)
                             ├── Lets you renew those passes without logging in again
                             ├── Speaks the same login language as "Sign in with Google"
                             └── Can tell other apps who's logged in, safely
```

## Why not just use Auth0 or Firebase?

For a real product, I probably would — they're solid, tested, and save a ton of time.

I'm building this one anyway because I want to actually *understand* how login systems work under the hood instead of just plugging one in. Things like: why do "refresh" tokens exist, why does the login link expire so fast, how does an app know your login is real without ever seeing your password — I wanted to build all of that myself, once, so I actually get it.

The bonus is I end up owning a login system I fully understand, that I can plug into my own future projects for free, without depending on someone else's service.

## What it actually does, in plain terms

- **Sign up and log in** — passwords are never stored as-is, they're hashed (scrambled one-way) so even I can't read them back
- **Gives out a short-lived "access pass"** (called a token) after login — it proves who you are for a little while, then expires
- **Gives out a longer-lived "renewal pass"** (refresh token) — so you don't have to log in again every few minutes, just quietly get a new access pass in the background
- **Notices if a renewal pass gets stolen and reused** — and if it does, shuts down that entire login session instead of just ignoring it
- **Supports "Login with X" style flows** — the same kind of flow you go through when you click "Continue with Google" on some app, fully built and testable
- **Can tell other apps "yes, this is a real logged-in user, here's their info"** — without those apps needing to touch Gatekeep's database directly
- **Understands roles and permissions** — like "admin" vs "regular user" — and can block certain actions unless you have the right role

## Why sign tokens with RS256 instead of a simple shared password?

The short version: with a simple shared secret, *any* service that can check if a token is valid could also fake one. With RS256, Gatekeep keeps a private key that only it has, and everyone else just gets a public key to check tokens with — they can verify, but they can never forge one. It's the difference between giving every branch a copy of the master key vs. giving them a way to check IDs without ever holding the key themselves.

## Built with

- **FastAPI** — the web framework, handles all the incoming requests
- **PostgreSQL + SQLAlchemy** — the database, since users/logins/permissions all relate to each other
- **Alembic** — handles database changes safely as the project grows
- **Argon2** — the password-hashing method
- **RS256 signed tokens** — for the login passes mentioned above

## How a login actually flows through it

1. Someone signs up or logs in
2. If they're using an app that supports it, that app redirects them through Gatekeep's login screen and gets permission to act on their behalf
3. Gatekeep hands back a short-lived access pass and a longer-lived renewal pass
4. When the access pass expires, the app quietly trades the renewal pass for a new one — no re-login needed
5. If a renewal pass ever gets reused after it's already been swapped once, Gatekeep treats that as a red flag and kills that whole login session
6. Any app can ask Gatekeep "who is this token for, and are they real?" using a public verification endpoint — no direct database access needed
7. If the user's role doesn't allow an action, Gatekeep blocks it before it happens

## Where it's at right now

Still being built. The core pieces — signup/login, access + renewal tokens, stolen-token detection, the "Login with X" style flow, and basic roles/permissions — are being built and tested one at a time before this gets connected to any of my real projects.

## Running it locally

```bash
# clone
git clone https://github.com/hm-ritik/Gatekeep_Authentication-Provider.git
cd Gatekeep_Authentication-Provider

# env
cp .env.example .env   # set your Postgres URL, RSA key paths, etc.

# install
pip install -r requirements.txt

# migrate
alembic upgrade head

# run
uvicorn app.main:app --reload
```

---

Built as part of a broader backend infrastructure roadmap — Gatekeep is the piece everything else eventually plugs into.
**Ritik Raushan ** 
