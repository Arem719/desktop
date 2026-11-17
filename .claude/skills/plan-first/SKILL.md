---
name: plan-first
description: Before building a feature or app, ask clarifying questions, write a plan and split it into small verifiable tasks, then execute task by task. Use for any non-trivial build request ("зроби додаток", "додай фічу", "build me...") or when the user says "спершу план".
---

# Plan first, then build

## 1. Clarify (max 5 questions, one message)
Only questions whose answers change the build: goal & user, must-have vs nice-to-have, constraints (stack, hosting, budget, deadline), data/auth needs, what "done" looks like. Offer a default for each so the user can answer "ok".

## 2. Write the plan → `PLAN.md`
- Goal (1–2 lines) and acceptance criteria (checkable bullets).
- Architecture sketch: components, data model, external services.
- Risks / unknowns and how each will be de-risked.
- Out of scope.

## 3. Split into tasks → `TASKS.md`
- 30–90 min each, ordered by dependency, each with a **done check** (test, command, or visible result).
- First task = thinnest end-to-end slice that runs.

## 4. Execute
- One task at a time: implement → run its check → tick it in TASKS.md → short status line.
- If a task reveals the plan is wrong, update PLAN.md and tell the user before continuing.
- Commit after each completed task with a clear message.
