# Crawl Track — How This Works

## Chain-PRs
Each exercise lives on its own branch, created off the **previous exercise's branch** (not main). This forms a chain:

```
main
 └── crawl/<github-id>/ex0-bootstrap
      └── crawl/<github-id>/ex1-repo-orientation
           └── crawl/<github-id>/ex2-build-test-baseline
                └── ...
```

Why chain? So each PR shows only the incremental diff for that exercise — reviewers and your future self can follow the progression clearly.

## Evidence in PRs
Every PR must include:
- **Test output** — paste the result of running your test command
- **Rollback plan** — `revert <SHA>` or describe what to undo
- **Review focus** — one sentence on what the reviewer should look at

If you can't run tests, document why and what manual check you did instead.

## Prompt Usage Pattern
For each exercise:
1. Open Copilot Chat with the repo open in VS Code
2. Paste the exercise prompt from `crawl-walk-run.instructions.md`
3. Append the standard suffix (plan → files → diffs → tests → PR draft)
4. Review Copilot's plan before accepting any file writes
5. Commit only what the acceptance criteria require — nothing more

## Key Files
| File | Purpose |
|------|---------|
| `ai-track-docs/SYSTEM-OVERVIEW.md` | Repo summary + chosen module |
| `ai-track-docs/build-test.md` | Exact build/test commands |
| `ai-track-docs/architecture.mmd` | Mermaid architecture diagram |
| `.copilot-track/crawl/README.md` | This file |
