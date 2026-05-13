# CI/CD 集成

> 📖 **前置要求**：阅读本附录前请先完成[第 07 章：融会贯通](../07-putting-it-together/README.md)。
>
> ⚠️ **本附录面向已经拥有 CI/CD 流水线的团队。** 如果你不熟悉 GitHub Actions 或 CI/CD 概念，建议先从第 07 章[自动化代码审阅](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional)中介绍的更简单的 pre-commit 钩子方式入手。

本附录展示了如何将 GitHub Copilot CLI 集成到 CI/CD 流水线中，对 pull request 进行自动化代码审阅。

---

## GitHub Actions 工作流

下面这个工作流会在 pull request 被打开或更新时，自动审阅发生变化的文件：

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

## 配置选项

### 限定审阅范围

你可以让审阅聚焦在特定类型的问题上：

```yaml
# Security-only review
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# Performance-only review
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### 处理大型 PR

对于包含大量文件的 PR，可以考虑分批或限制数量：

```yaml
# Limit to first 10 files
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# Or set a timeout per file
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### 团队共享配置

为了在团队内保持审阅风格一致，可以创建一份共享配置：

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

## 替代方案：PR 审阅机器人

如果想要更复杂的审阅工作流，可以考虑使用 GitHub Copilot 云端 agent：

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

## CI/CD 集成的最佳实践

1. **使用 `--silent` 标志** —— 抑制进度输出，让日志更整洁
2. **设置超时** —— 防止挂起的审阅阻塞流水线
3. **过滤文件类型** —— 只审阅相关文件（跳过生成代码、依赖等）
4. **关注速率限制** —— 大型 PR 的审阅要错开节奏
5. **优雅地失败** —— 不要让审阅失败阻塞合并；记录日志后继续

---

## 排错

### CI 中出现「Authentication failed」

确保你的工作流拥有正确的权限：

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### 审阅超时

加大超时时间或缩小审阅范围：

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### 大文件触发 token 上限

跳过过大的文件：

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← 返回第 07 章](../07-putting-it-together/README.md)** | **[返回附录目录](README.md)**
