---
name: brag
description: Build a "brag document" of what the user actually accomplished — from git history, merged PRs, closed issues and notes — for performance reviews, CVs, LinkedIn or portfolio. Use when the user says "brag", "що я зробив за місяць/рік", "для резюме", "performance review".
---

# Brag doc

1. Ask the period (default: last 3 months) and the audience (manager review / CV / LinkedIn / portfolio).
2. Gather evidence:
   - `git log --author="<user>" --since=<date> --no-merges --stat` in each repo the user names.
   - PRs/issues via GitHub tools if available; any notes/changelog files.
3. Group commits into **achievements**, not tasks: feature shipped, bug class eliminated, performance gained, process improved, people helped.
4. For each achievement write: **What** (one line) · **Impact** (numbers: users, ms, %, $, hours saved — ask if unknown, never invent) · **Evidence** (PR/commit links) · **Skills** shown.
5. Output `BRAG.md` sorted by impact, plus a version tailored to the audience (3 CV bullets in "Did X, resulting in Y, by Z" form, or a short LinkedIn post using the no-ai-slop rules).
