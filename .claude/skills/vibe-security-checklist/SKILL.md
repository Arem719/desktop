---
name: vibe-security-checklist
description: Quick hardening pass for a vibe-coded site — fix the common holes, then report what was found and fixed. Use when the user says "щоб хакери не зламали сайт", "захисти сайт", "quick security pass". For a deep audit use the security-audit skill instead.
---

# Vibe-coded site: quick hardening pass

Go through every item. For each: check the code → fix if broken → note the result. Ask before anything destructive (rotating keys, rewriting git history).

1. Proper authentication (vetted library/provider, no home-made crypto, sessions expire).
2. Remove API keys and secrets from code; move to environment variables.
3. Enable CSP (Content-Security-Policy) and other security headers.
4. Close the database to the public internet; least-privilege DB user; row-level security where applicable.
5. Store passwords only as hashes (bcrypt/argon2).
6. Log suspicious logins (bursts of failures, new locations).
7. Validate all forms on the server, not only in the browser.
8. Protect against XSS (escape output, no raw HTML from users).
9. Lock down the admin panel (server-side role check, not just a hidden link).
10. Use parameterized queries everywhere (no string-built SQL).
11. One-time, expiring password-reset links.
12. Check environment variables: nothing secret exposed to the frontend bundle.
13. Rate-limit requests (login, signup, reset, API, AI endpoints).
14. Remove unused packages.
15. Restrict upload file types and sizes.
16. Verify prices and payments on the server (never trust client-sent amounts).
17. Hide service files and backups (`.env`, `.git`, `*.bak`, `*.sql` not web-served).
18. Update vulnerable dependencies (`npm audit` / equivalent).
19. Scan git history for leaked keys; rotate any found.
20. Finally, test the defenses (try the attacks above against the fixed code).

## Report
Table: `# | check | status (ok / fixed / needs you) | what was done`. Then list anything the user must do by hand (e.g. rotate a key in a provider dashboard).
