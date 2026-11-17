---
name: security-audit
description: Security audit of a web app or site, especially one built quickly with AI ("vibe-coded"). Use when the user asks "як захистити сайт", "security audit", "перевір на вразливості", or before launching / deploying.
---

# Security audit (vibe-coded app edition)

Work through the codebase; report each finding as `severity (critical/high/med/low) | file:line | issue | exploit scenario | fix`. Fix nothing silently — list first, then offer to patch.

## 1. Secrets
- Hard-coded API keys, tokens, DB URLs in source, `.env` committed, keys in frontend bundles (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` holding secret keys). Check git history (`git log -p -S`), not just HEAD.
- Recommend rotation for anything that leaked.

## 2. AuthN / AuthZ
- Every API route/server action checks the session **and** ownership (IDOR: can user A read/update user B's object by changing an id?).
- Admin routes protected server-side, not only hidden in UI.
- Supabase/Firebase: Row Level Security / security rules enabled on every table/collection; no `anon` write access.
- Passwords hashed (bcrypt/argon2), session cookies `HttpOnly; Secure; SameSite`, JWT secrets strong, expiry set.

## 3. Input handling
- SQL/NoSQL injection (string-built queries), XSS (`dangerouslySetInnerHTML`, `v-html`, unescaped templates), SSRF (server fetches user-supplied URLs), path traversal in file access, command injection (`exec` with user input), unsafe deserialization.
- File uploads: type/size limits, stored outside web root or on object storage, no executable content served.

## 4. Web hardening
- HTTPS only, HSTS; security headers (CSP, X-Content-Type-Options, frame-ancestors / X-Frame-Options, Referrer-Policy).
- CORS not `*` with credentials. CSRF protection on cookie-auth state-changing requests.
- Rate limiting on login, signup, password reset, AI/LLM endpoints (cost abuse), and any paid API proxy.
- Errors don't leak stack traces or SQL in production.

## 5. Dependencies & infra
- `npm audit` / `pip-audit` / equivalent; outdated major frameworks.
- Debug mode off, default credentials changed, DB not publicly reachable, storage buckets not public-listable.
- Backups exist; logging of auth events.

## 6. LLM-specific (if the app calls an AI model)
- Prompt injection from user content reaching tools/actions; model output rendered as HTML; API key exposed client-side; no per-user spend cap.

## Output
Summary table by severity → top 5 fixes to do before launch → offer to apply patches.
