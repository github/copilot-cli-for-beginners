# Crawl Track — GitHub Copilot AI Engineering

This directory contains documentation and resources for the **Crawl** level of the AI Engineering track, where you use GitHub Copilot as an **assistant** for single-file or single-module exercises.

## How This Track Works

### Chain of PRs
Each exercise builds on the previous one. Exercises are numbered Ex 0–15:
- **Ex 0 (Bootstrap):** Set up scaffolding and documentation
- **Ex 1–15:** Progressive exercises that grow in scope and complexity

Each exercise creates a new branch and PR. PRs are small, reversible, and focused on one goal.

### Branch Naming
All branches follow this pattern:
```
crawl/<github-id>/ex<N>-<short-name>
```

Example: `crawl/nowakfli/ex0-bootstrap`

### Evidence in PRs
Every PR must include:
1. **What changed:** Clear summary of modifications
2. **Why:** Motivation and acceptance criteria met
3. **Evidence:** Test output, logs, or metrics proving the change works
4. **Rollback plan:** How to quickly undo if needed

### Copilot Usage
In the Crawl track, Copilot helps with:
- **Inline suggestions:** Code completion while typing
- **/explain:** Understanding existing code
- **/tests:** Generating test cases
- **Chat prompts:** Planning changes before coding

Copilot is your *assistant*—you drive the work, Copilot provides suggestions.

## Repository Structure

```
.
├── ai-track-docs/           # Shared documentation across all exercises
│   ├── SYSTEM-OVERVIEW.md   # Repo summary, entry points, test approach
│   ├── build-test.md        # Exact build and test commands
│   ├── architecture.mmd     # System diagram (Mermaid)
│   ├── dependencies.md      # Dependency policy (added in Ex 7)
│   └── ...                  # Additional docs as exercises progress
├── .copilot-track/
│   └── crawl/               # Crawl track resources
│       └── README.md        # This file
```

## Exercise Pattern

1. Create a branch: `git checkout -b crawl/<id>/ex<N>-<name>`
2. Send full prompt to Copilot Chat
3. Implement changes (Copilot assists)
4. Commit: `git add . && git commit -m "crawl: ex<N> <name>"`
5. Push: `git push -u origin crawl/<id>/ex<N>-<name>`
6. Open PR with evidence and rollback plan
7. Once approved, PR description becomes part of the track record

## Guardrails

- **Keep PRs small:** One goal per exercise
- **No secrets:** Don't commit API keys or credentials
- **Exclude vendor:** Don't modify `node_modules`, `vendor`, or submodules
- **Evidence required:** Every PR needs test output or metrics
- **Reversible:** Every change should be revertible in one commit

## Next Steps

Start with **Ex 1: Repo Orientation** to build a mental model of the codebase and pick a low-risk module to work with throughout the track.
