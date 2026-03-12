# CI/CD 集成

> 📖 **前置要求**: 阅读本附录前，请先完成 [第 07 章: 综合实战](../07-putting-it-together/README.md)。
>
> ⚠️ **本附录适用于已有 CI/CD 流水线的团队。** 如果你刚接触 GitHub Actions 或 CI/CD 概念，请先从第 07 章 [代码评审自动化](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional) 中更简单的 pre-commit hook 方案开始。

本附录展示如何将 GitHub Copilot CLI 集成到 CI/CD 流水线中，以便在 Pull Request 上自动执行代码评审。

---

## GitHub Actions 工作流

下面的工作流会在 Pull Request 创建或更新时，自动评审变更文件:

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
          fetch-depth: 0  # 用于与 main 分支进行比较

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # 获取变更的 JS/TS 文件列表
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
            
            # 使用 --silent 抑制进度输出
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // 仅在有有效内容时发布
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

### 限定评审范围

你可以将评审聚焦到某类问题:

```yaml
# 仅安全评审
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# 仅性能评审
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### 处理大型 PR

当 PR 文件较多时，建议分批或限制数量:

```yaml
# 仅处理前 10 个文件
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# 或者对每个文件设置超时
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### 团队统一配置

为确保团队评审口径一致，可创建共享配置:

```json
// .copilot/config.json (提交到仓库)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## 可选方案: PR 评审机器人

如果你需要更高级的评审工作流，可考虑使用 Copilot coding agent:

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

## CI/CD 集成最佳实践

1. **使用 `--silent` 参数** - 抑制进度输出，让日志更干净
2. **设置超时** - 避免卡住的评审阻塞流水线
3. **按文件类型过滤** - 仅评审相关文件（跳过生成代码、依赖等）
4. **关注速率限制** - 大型 PR 评审应适当分散调用
5. **优雅失败** - 评审失败时记录并继续，不阻塞合并

---

## 故障排查

### CI 中出现 "Authentication failed"

请确保工作流具备正确权限:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### 评审超时

提高超时或缩小评审范围:

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### 大文件触发 token 限制

跳过超大文件:

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← 返回第 07 章](../07-putting-it-together/README.md)** | **[返回附录](README.zh-CN.md)**
