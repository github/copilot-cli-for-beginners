# CI/CD 統合

> 📖 **前提条件**: この付録を読む前に[第 07 章: すべてをまとめる](../07-putting-it-together/README.md)を完了してください。
>
> ⚠️ **この付録は既存の CI/CD パイプラインを持つチーム向けです。** GitHub Actions や CI/CD の概念に不慣れな場合は、第 07 章の[コードレビューの自動化](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional)セクションにあるよりシンプルなプリコミットフックのアプローチから始めてください。

この付録では、プルリクエストの自動コードレビューのために GitHub Copilot CLI を CI/CD パイプラインに統合する方法を示します。

---

## GitHub Actions ワークフロー

このワークフローはプルリクエストが開かれたり更新されたりしたとき、変更されたファイルを自動的にレビューします:

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
          fetch-depth: 0  # メインブランチとの比較に必要

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # 変更された JS/TS ファイルのリストを取得する
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
            
            # --silent でプログレス出力を抑制する
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // 意味のあるコンテンツがある場合のみ投稿する
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

## 設定オプション

### レビュースコープの制限

特定の種類の問題にレビューを集中させることができます:

```yaml
# セキュリティのみのレビュー
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# パフォーマンスのみのレビュー
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### 大きな PR の処理

ファイルが多い PR では、バッチ処理や制限を検討します:

```yaml
# 最初の 10 ファイルに制限する
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# またはファイルごとにタイムアウトを設定する
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### チーム設定

チーム全体で一貫したレビューを行うために、共有設定を作成します:

```json
// .copilot/config.json (リポジトリにコミットする)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## 代替案: PR レビューボット

より高度なレビューワークフローには、GitHub Copilot クラウドエージェントの使用を検討してください:

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

## CI/CD 統合のベストプラクティス

1. **`--silent` フラグを使う** — よりクリーンなログのためにプログレス出力を抑制する
2. **タイムアウトを設定する** — ハングしたレビューがパイプラインをブロックするのを防ぐ
3. **ファイルタイプをフィルタリングする** — 関連するファイルのみレビューする（生成コード、依存関係をスキップ）
4. **レート制限を意識する** — 大きな PR ではレビューを分散させる
5. **適切に失敗する** — レビューの失敗でマージをブロックしない。ログに記録して続行する

---

## トラブルシューティング

### CI で「認証に失敗しました」

ワークフローに正しい権限があることを確認します:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### レビューがタイムアウトする

タイムアウトを増やすかスコープを減らします:

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### 大きなファイルでトークン制限に達する

非常に大きなファイルをスキップします:

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

[**← 第 07 章に戻る**](../07-putting-it-together/README.md) | [**付録に戻る**](README.md)
