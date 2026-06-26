# CI/CD 통합

> 📖 **사전 학습**: 이 부록을 읽기 전에 [7장: 모두 합치기](../07-putting-it-together/README.md)를 먼저 마칩니다.
>
> ⚠️ **이 부록은 이미 CI/CD 파이프라인을 운영 중인 팀을 위한 것입니다.** GitHub Actions나 CI/CD 개념이 처음이라면, 7장의 [코드 리뷰 자동화](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional) 섹션에 있는 더 단순한 pre-commit 훅 방식부터 시작합니다.

이 부록에서는 풀 리퀘스트에서 자동 코드 리뷰를 수행하기 위해 GitHub Copilot CLI를 CI/CD 파이프라인에 통합하는 방법을 보여 줍니다.

---

## GitHub Actions 워크플로

다음 워크플로는 풀 리퀘스트가 열리거나 업데이트될 때 변경된 파일을 자동으로 리뷰합니다:

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
          fetch-depth: 0  # main 브랜치와 비교하기 위해 필요합니다

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # 변경된 JS/TS 파일 목록을 가져옵니다
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
            
            # 진행 상황 출력을 억제하려면 --silent를 사용합니다
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // 의미 있는 내용이 있을 때만 게시합니다
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

## 구성 옵션

### 리뷰 범위 제한하기

특정 유형의 이슈에 집중하도록 리뷰를 좁힐 수 있습니다:

```yaml
# 보안 전용 리뷰를 수행합니다
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# 성능 전용 리뷰를 수행합니다
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### 큰 PR 다루기

파일이 많은 PR에서는 배치로 처리하거나 개수를 제한하는 방법을 고려합니다:

```yaml
# 처음 10개 파일로 제한합니다
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# 또는 파일마다 타임아웃을 설정합니다
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### 팀 공통 구성

팀 전체에서 일관된 리뷰를 보장하려면 공유 구성 파일을 만들어 둡니다:

```json
// .copilot/config.json (리포지토리에 커밋됨)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## 대안: PR 리뷰 봇

더 정교한 리뷰 워크플로가 필요하다면, GitHub Copilot 클라우드 에이전트를 활용하는 것도 좋은 선택입니다:

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

## CI/CD 통합 모범 사례

1. **`--silent` 플래그 사용** - 진행 상황 출력을 억제해 로그를 깔끔하게 유지합니다.
2. **타임아웃 설정** - 리뷰가 멈춰 파이프라인을 막지 않도록 합니다.
3. **파일 형식 필터링** - 관련 있는 파일만 리뷰합니다(생성된 코드, 의존성 파일은 제외).
4. **레이트 리밋 인지** - 큰 PR은 리뷰를 분산해서 실행합니다.
5. **우아하게 실패하기** - 리뷰 실패가 머지를 막지 않도록 합니다. 로그만 남기고 진행합니다.

---

## 트러블슈팅

### CI에서 "Authentication failed"

워크플로에 올바른 권한이 부여되어 있는지 확인합니다:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### 리뷰가 타임아웃됨

타임아웃을 늘리거나 범위를 줄입니다:

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### 큰 파일에서 토큰 한도 초과

매우 큰 파일은 건너뜁니다:

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

[**← 7장으로 돌아가기**](../07-putting-it-together/README.md) | [**부록 목록으로 돌아가기**](README.md)
