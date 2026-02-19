# CI/CD Integration

> 📖 **Prerequisite**: Complete [Chapter 07: Putting It All Together](../07-putting-it-together/README.md) before reading this appendix.
>
> ⚠️ **This appendix is for teams with existing CI/CD pipelines.** If you're new to GitHub Actions or CI/CD concepts, start with the simpler pre-commit hook approach in Chapter 07's [Code Review Automation](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional) section.

This appendix shows how to integrate GitHub Copilot CLI into your CI/CD pipelines for automated code review on pull requests.

---

## GitHub Actions Workflow

This workflow automatically reviews changed files when a pull request is opened or updated:

```yaml
# .github/workflows/copilot-review.yml
name: Copilot Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed to compare with main branch

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Get list of changed JS/TS files
          FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts|jsx|tsx)$' || true)
          
          if [ -z "$FILES" ]; then
            echo "No JavaScript/TypeScript files changed"
            exit 0
          fi
          
          echo "# Copilot Code Review" > review.md
          echo "" >> review.md
          
          for file in $FILES; do
            echo "Reviewing $file..."
            echo "## $file" >> review.md
            echo "" >> review.md
            
            # Use --silent to suppress progress output
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // Only post if there's meaningful content
            if (review.includes('CRITICAL') || review.includes('HIGH')) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: review
              });
            } else {
              console.log('No critical issues found, skipping comment');
            }
```

---

## Configuration Options

### Limiting Review Scope

You can focus the review on specific types of issues:

```yaml
# Security-only review
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# Performance-only review
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### Handling Large PRs

For PRs with many files, consider batching or limiting:

```yaml
# Limit to first 10 files
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# Or set a timeout per file
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### Team Configuration

For consistent reviews across your team, create a shared configuration:

```json
// .copilot/config.json (committed to repo)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## Alternative: PR Review Bot

For more sophisticated review workflows, consider using the Copilot coding agent:

```yaml
# .github/workflows/copilot-agent-review.yml
name: Request Copilot Review

on:
  pull_request:
    types: [opened, ready_for_review]

jobs:
  request-review:
    runs-on: ubuntu-latest
    steps:
      - name: Request Copilot Review
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.pulls.requestReviewers({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              reviewers: ['copilot[bot]']
            });
```

---

## Best Practices for CI/CD Integration

1. **Use `--silent` flag** - Suppresses progress output for cleaner logs
2. **Set timeouts** - Prevent hung reviews from blocking your pipeline
3. **Filter file types** - Only review relevant files (skip generated code, dependencies)
4. **Rate limit awareness** - Space out reviews for large PRs
5. **Fail gracefully** - Don't block merges on review failures; log and continue

---

## Troubleshooting

### "Authentication failed" in CI

Ensure your workflow has the correct permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### Reviews timing out

Increase timeout or reduce scope:

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### Token limits in large files

Skip very large files:

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← Back to Chapter 07](../07-putting-it-together/README.md)** | **[Return to Appendices](README.md)**
