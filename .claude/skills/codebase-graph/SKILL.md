---
name: codebase-graph
description: Build a queryable map of a codebase (modules, dependencies, key "god" nodes, subsystems) so the agent stops re-grepping the project every session and saves tokens. Use when starting work in an unfamiliar or large repo, or when the user says "граф проекту", "map the codebase", "graphify".
---

# Codebase graph

Inspired by the open-source tool **graphify** (`/graphify .` → graph.html, GRAPH_REPORT.md, graph.json via tree-sitter, no LLM). If the user wants that exact tool, look up its repo and install instructions first; do not guess package names. Otherwise build an equivalent map locally:

## Build
1. Inventory: languages, entry points (main, routes, CLI, workers), configs, schemas (SQL/migrations), docs.
2. Extract edges deterministically where possible (import/require statements, route → handler, handler → service → DB table, config → consumer). Use grep/AST tools available in the repo (`tsc --listFiles`, `madge`, `pydeps`, `go list -deps`) if installed.
3. Mark every edge **EXTRACTED** (seen literally in source) or **INFERRED** (your deduction) — never mix them.
4. Compute: most-connected nodes ("god nodes"), clusters/subsystems, cycles, dead/orphan modules.

## Output (in `.claude/graph/`)
- `graph.json` – `{nodes:[{id,type,file}], edges:[{from,to,kind,provenance}]}`
- `GRAPH_REPORT.md` – 1-paragraph overview, subsystem list with key files, god nodes, cycles, "where to start for X" table.
- Optionally `graph.html` – a self-contained interactive view (vanilla JS force layout, no CDN needed).

## Use
On later questions ("what links auth and the DB?", "path from A to B", "explain RateLimiter") answer from the graph first, open only the files on the path. Rebuild when many files changed (check `git diff --stat` since the graph's commit, stored in the report header).
