---
name: commit-message
description: Generate conventional commit messages - use when creating commits, writing commit messages, or asking for git commit help
---

# Commit Message Skill

Generate commit messages following the Conventional Commits specification.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting (no code change) |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

## Rules

1. Subject line maximum 72 characters
2. Use imperative mood ("add" not "added" or "adds")
3. No period at the end of subject line
4. Separate subject from body with blank line
5. Body explains **what** and **why**, not how

## Examples

Simple:
```
fix(auth): prevent redirect loop on expired sessions
```

With body:
```
feat(api): add rate limiting to public endpoints

- Limits requests to 100/minute per IP
- Returns 429 status with retry-after header
- Configurable via RATE_LIMIT_MAX env variable

Closes #234
```
