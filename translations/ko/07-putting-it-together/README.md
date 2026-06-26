![7장: 모두 합치기](../../../07-putting-it-together/images/chapter-header.png)

> **지금까지 배운 모든 것이 이곳에서 하나로 합쳐집니다. 아이디어에서 머지된 PR까지, 한 번의 세션으로 끝내 보세요.**

이번 장에서는 지금까지 배운 모든 내용을 하나의 완성된 워크플로로 통합해 봅니다. 다중 에이전트 협업으로 기능을 만들고, 커밋 전에 보안 이슈를 잡아내는 pre-commit 훅을 설정하며, Copilot을 CI/CD 파이프라인에 통합하고, 단일 터미널 세션 안에서 기능 아이디어를 머지된 PR로 끌고 가는 과정을 익힙니다. 바로 이 지점에서 GitHub Copilot CLI는 진짜 의미의 생산성 증폭기가 됩니다.

> 💡 **참고**: 이번 장은 지금까지 배운 모든 것을 결합하는 방법을 보여 줍니다. **생산적으로 작업하기 위해 반드시 에이전트, 스킬, MCP가 필요한 것은 아닙니다(물론 매우 유용할 수 있습니다).** 핵심 워크플로인 설명 → 계획 → 구현 → 테스트 → 리뷰 → 배포는 0~3장에서 다룬 기본 기능만으로도 충분히 동작합니다.

## 🎯 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 에이전트, 스킬, MCP(Model Context Protocol)를 통합된 워크플로 안에서 결합하기
- 여러 도구를 함께 활용해 완성된 기능 만들기
- 훅으로 기본적인 자동화 구성하기
- 전문적인 개발을 위한 모범 사례 적용하기

> ⏱️ **예상 소요 시간**: 약 75분 (읽기 15분 + 실습 60분)

---

## 🧩 실생활 비유: 오케스트라

<img src="../../../07-putting-it-together/images/orchestra-analogy.png" alt="오케스트라 비유 - 통합된 워크플로" width="800"/>

교향악단은 여러 파트로 구성됩니다:
- **현악기**는 기반을 만들어 줍니다(여러분의 핵심 워크플로처럼).
- **금관악기**는 힘을 더해 줍니다(전문 분야를 가진 에이전트처럼).
- **목관악기**는 색채를 입혀 줍니다(역량을 확장하는 스킬처럼).
- **타악기**는 리듬을 유지해 줍니다(외부 시스템과 연결되는 MCP처럼).

각각만 들으면 한계가 느껴지지만, 잘 지휘된 합주는 웅장한 음악을 만들어 냅니다.

**바로 이것이 이번 장에서 배울 내용입니다!**<br>
*지휘자가 오케스트라를 이끌듯, 여러분은 에이전트, 스킬, MCP를 하나의 워크플로로 지휘합니다.*

먼저 코드를 수정하고, 테스트를 생성하고, 리뷰를 거친 뒤 PR을 만드는 과정을 한 세션 안에서 모두 진행하는 시나리오를 살펴봅시다.

---

## 한 세션으로 아이디어부터 머지된 PR까지

에디터, 터미널, 테스트 러너, GitHub UI를 오가며 매번 맥락을 잃어버리는 대신, 모든 도구를 하나의 터미널 세션에서 결합해 사용할 수 있습니다. 아래의 [통합 패턴](#the-integration-pattern-for-power-users) 섹션에서 이 흐름을 자세히 풀어볼 것입니다.

```bash
# Start Copilot in interactive mode
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot creates high-level plan...

# SWITCH TO PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# SWITCH TO PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# IMPLEMENT
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TEST
> Generate comprehensive tests for the new feature

# Multiple tests are generated similar to the following:
# - Happy path (3 tests) — filters correctly, excludes read, includes unread
# - Edge cases (4 tests) — empty collection, all read, none read, single book
# - Parametrized (5 cases) — varying read/unread ratios via @pytest.mark.parametrize
# - Integration (4 tests) — interplay with mark_as_read, remove_book, add_book, and data integrity

# Review the changes
> /review

# If review passes, use /pr to operate on the pull request for the current branch
> /pr [view|create|fix|auto]

# Or ask naturally if you want Copilot to draft it from the terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**전통적인 방식**: 에디터, 터미널, 테스트 러너, 문서, GitHub UI 사이를 끊임없이 전환합니다. 전환할 때마다 맥락이 끊기고 마찰이 생깁니다.

**핵심 통찰**: 여러분은 마치 건축가처럼 전문가들에게 방향을 제시했습니다. 세부 사항은 그들이 처리했고, 큰 그림은 여러분이 잡았습니다.

> 💡 **한 걸음 더**: 이런 다단계 계획에는 `/fleet`을 활용해 Copilot이 독립적인 하위 작업을 병렬로 실행하도록 해 보세요. 자세한 내용은 [공식 문서](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)를 참고하세요.

---

# 추가 워크플로

<img src="../../../07-putting-it-together/images/combined-workflows.png" alt="기어가 달린 거대한 컬러풀 직소 퍼즐을 함께 맞추고 있는 사람들 - 에이전트, 스킬, MCP가 하나의 통합 워크플로로 결합되는 모습" width="800"/>

4~6장을 마친 파워 유저를 위해, 다음 워크플로들은 에이전트와 스킬, MCP가 어떻게 효율을 배가시키는지 보여 줍니다.

## 통합 패턴

다음은 모든 것을 결합할 때 머릿속에 그릴 멘탈 모델입니다:

<img src="../../../07-putting-it-together/images/integration-pattern.png" alt="통합 패턴 - 4단계 워크플로: 컨텍스트 수집(MCP), 분석 및 계획(에이전트), 실행(스킬 + 수동), 마무리(MCP)" width="800"/>

---

## 워크플로 1: 버그 조사와 수정

모든 도구를 통합한 실제적인 버그 수정 흐름입니다:

```bash
copilot

# PHASE 1: Understand the bug from GitHub (MCP provides this)
> Get the details of issue #1

# Learn: "find_by_author doesn't work with partial names"

# PHASE 2: Research best practice (deep research with web + GitHub sources)
> /research Best practices for Python case-insensitive string matching

# PHASE 3: Find related code
> @samples/book-app-project/books.py Show me the find_by_author method

# PHASE 4: Get expert analysis
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching

# Agent identifies: Method uses exact equality instead of substring matching

# PHASE 5: Fix with agent guidance
> Implement the fix using lowercase comparison and 'in' operator

# PHASE 6: Generate tests
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# PHASE 7: Commit and PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## 워크플로 2: 코드 리뷰 자동화 (선택)

> 💡 **이 섹션은 선택 사항입니다.** Pre-commit 훅은 팀 단위에서 유용하지만, 생산적으로 작업하기 위해 꼭 필요한 것은 아닙니다. 이제 막 시작하는 단계라면 건너뛰어도 됩니다.
>
> ⚠️ **성능 참고**: 이 훅은 스테이징된 파일마다 `copilot -p`를 호출하므로 파일당 몇 초가 소요됩니다. 커밋 규모가 크다면 핵심 파일로만 제한하거나, `/review`를 통해 수동으로 리뷰하는 방식을 고려해 보세요.

**git 훅**은 Git이 특정 시점(예: 커밋 직전)에 자동으로 실행하는 스크립트입니다. 이를 활용해 코드에 대한 자동 검사를 수행할 수 있습니다. 다음은 커밋 시점에 Copilot 리뷰를 자동으로 수행하도록 설정하는 방법입니다:

```bash
# Create a pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    # --allow-all auto-approves file reads/writes so the hook can run unattended.
    # Only use this in automated scripts. In interactive sessions, let Copilot ask for permission.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOS 사용자**: `timeout` 명령은 macOS에 기본 포함되어 있지 않습니다. `brew install coreutils`로 설치하거나, `timeout 60` 부분을 타임아웃 가드 없이 단순한 호출로 바꿔 사용하세요.

> 📚 **공식 문서**: 훅 API 전체는 [Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) 및 [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) 문서를 참고하세요.
>
> 💡 **내장 대안**: Copilot CLI에는 pre-commit과 같은 이벤트에서 자동 실행되는 내장 훅 시스템(`copilot hooks`)도 있습니다. 위처럼 직접 구성하는 git 훅은 모든 것을 세밀하게 제어할 수 있는 반면, 내장 시스템은 설정이 더 간단합니다. 위의 공식 문서를 참고해 자신의 워크플로에 맞는 방식을 선택하세요.

이제 모든 커밋마다 빠른 보안 리뷰가 수행됩니다:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Output:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## 워크플로 3: 새로운 코드베이스 온보딩

새 프로젝트에 합류했을 때, 컨텍스트와 에이전트, MCP를 결합하면 빠르게 적응할 수 있습니다:

```bash
# Start Copilot in interactive mode
copilot

# PHASE 1: Get the big picture with context
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# PHASE 2: Understand a specific flow
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# PHASE 3: Get expert analysis with an agent
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# PHASE 4: Find something to work on (MCP provides GitHub access)
> List open issues labeled "good first issue"

# PHASE 5: Start contributing
> Pick the simplest open issue and outline a plan to fix it
```

이 워크플로는 `@` 컨텍스트, 에이전트, MCP를 단일 온보딩 세션 안에서 결합합니다. 이번 장 앞부분에서 살펴본 통합 패턴 그대로입니다.

---

# 모범 사례와 자동화

여러분의 워크플로를 더 효과적으로 만들어 줄 패턴과 습관입니다.

---

## 모범 사례

### 1. 분석 전에 컨텍스트부터 모으기

분석을 요청하기 전에 항상 컨텍스트를 먼저 수집하세요:

```bash
# Good
> Get the details of issue #42
> /agent
# Select python-reviewer
> Analyze this issue

# Less effective
> /agent
# Select python-reviewer
> Fix login bug
# Agent doesn't have issue context
```

### 2. 차이점 알기: 에이전트, 스킬, 커스텀 인스트럭션

각 도구마다 어울리는 자리가 있습니다:

```bash
# Agents: Specialized personas you explicitly activate
> /agent
# Select python-reviewer
> Review this authentication code for security issues

# Skills: Modular capabilities that auto-activate when your prompt
# matches the skill's description (you must create them first — see Ch 05)
> Generate comprehensive tests for this code
# If you have a testing skill configured, it activates automatically

# Custom instructions (.github/copilot-instructions.md): Always-on
# guidance that applies to every session without switching or triggering
```

> 💡 **핵심 포인트**: 에이전트와 스킬 모두 분석과 코드 생성을 할 수 있습니다. 진짜 차이는 **활성화 방식**에 있습니다. 에이전트는 명시적으로(`/agent`), 스킬은 자동으로(프롬프트와 매칭되어), 커스텀 인스트럭션은 항상 켜져 있습니다.

### 3. 세션을 한 가지 주제에 집중시키기

`/rename`으로 세션에 라벨을 붙이면(히스토리에서 찾기 쉬워집니다) `/exit`으로 깔끔하게 종료할 수 있습니다:

```bash
# Good: One feature per session
> /rename list-unread-feature
# Work on list unread
> /exit

copilot
> /rename export-csv-feature
# Work on CSV export
> /exit

# Less effective: Everything in one long session
```

### 4. Copilot으로 워크플로를 재사용 가능하게 만들기

워크플로를 위키에만 정리해 두는 대신, Copilot이 활용할 수 있도록 저장소에 직접 인코딩하세요:

- **커스텀 인스트럭션** (`.github/copilot-instructions.md`): 코딩 표준, 아키텍처 규칙, 빌드/테스트/배포 단계에 대한 항상 켜져 있는 가이드입니다. 모든 세션이 자동으로 따릅니다.
- **프롬프트 파일** (`.github/prompts/`): 코드 리뷰, 컴포넌트 생성, PR 설명 같은 템플릿처럼, 팀이 공유할 수 있는 재사용 가능한 매개변수화된 프롬프트입니다.
- **커스텀 에이전트** (`.github/agents/`): 보안 리뷰어, 문서 작성자 같은 전문 페르소나를 인코딩해 두면 팀 누구나 `/agent`로 활성화할 수 있습니다.
- **커스텀 스킬** (`.github/skills/`): 단계별 워크플로 지시문을 패키지화해 두면 관련 상황에서 자동으로 활성화됩니다.

> 💡 **얻는 것**: 새로 합류한 팀원이 별다른 노력 없이 여러분의 워크플로를 그대로 사용할 수 있습니다. 누군가의 머릿속에 갇혀 있지 않고 저장소에 함께 들어 있기 때문입니다.

---

## 보너스: 프로덕션 패턴

다음 패턴들은 선택 사항이지만 전문적인 환경에서 큰 가치가 있습니다.

### PR 설명 생성기

```bash
# Generate comprehensive PR descriptions
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD 통합

이미 CI/CD 파이프라인을 운영 중인 팀이라면, GitHub Actions를 사용해 모든 풀 리퀘스트에서 Copilot 리뷰를 자동화할 수 있습니다. 리뷰 댓글을 자동으로 게시하고 critical 이슈만 필터링하는 등의 기능을 포함합니다.

> 📖 **더 알아보기**: 완전한 GitHub Actions 워크플로, 구성 옵션, 트러블슈팅 팁은 [CI/CD 통합](../appendices/ci-cd-integration.md) 문서를 참고하세요.

---

# 실습

<img src="../../../images/practice.png" alt="모니터에 코드가 띄워져 있고, 램프와 커피잔, 헤드폰이 놓인 따뜻한 분위기의 데스크 - 실습을 위한 준비된 모습" width="800"/>

전체 워크플로를 직접 실습해 봅시다.

---

## ▶️ 직접 해 보기

데모를 마쳤다면, 다음 변형들도 시도해 보세요:

1. **엔드 투 엔드 챌린지**: 작은 기능 하나를 골라 보세요(예: "안 읽은 책 목록", "CSV로 내보내기"). 다음과 같이 전체 워크플로를 사용합니다:
   - `/plan`으로 계획 세우기
   - 에이전트(python-reviewer, pytest-helper)로 설계
   - 구현
   - 테스트 생성
   - PR 생성

2. **자동화 챌린지**: 코드 리뷰 자동화 워크플로의 pre-commit 훅을 설정해 보세요. 의도적으로 파일 경로 취약점을 포함한 커밋을 시도해 봅니다. 차단되나요?

3. **나만의 프로덕션 워크플로**: 자주 수행하는 작업에 대해 여러분만의 워크플로를 설계해 체크리스트로 정리해 보세요. 어떤 부분을 스킬, 에이전트, 훅으로 자동화할 수 있을까요?

**자기 점검**: 동료에게 에이전트, 스킬, MCP가 어떻게 함께 동작하는지, 그리고 각각을 언제 사용해야 하는지 설명할 수 있다면 이 강의를 마친 것입니다.

---

## 📝 과제

### 메인 챌린지: 엔드 투 엔드 기능 만들기

실습 예제에서는 "안 읽은 책 목록" 기능을 만들어 보았습니다. 이번에는 다른 기능인 **연도 범위로 책 검색하기**를 가지고 전체 워크플로를 연습해 보세요:

1. Copilot을 시작하고 컨텍스트를 모읍니다: `@samples/book-app-project/books.py`
2. `/plan Add a "search by year" command that lets users find books published between two years`로 계획을 세웁니다.
3. `BookCollection`에 `find_by_year_range(start_year, end_year)` 메서드를 구현합니다.
4. `book_app.py`에 시작/종료 연도를 사용자에게 물어보는 `handle_search_year()` 함수를 추가합니다.
5. 테스트를 생성합니다: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. `/review`로 리뷰합니다.
7. README를 업데이트합니다: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. 커밋 메시지를 생성합니다.

작업하면서 워크플로를 함께 기록해 두세요.

**성공 기준**: Copilot CLI를 사용해 기획, 구현, 테스트, 문서화, 리뷰까지 포함한 전체 흐름으로 아이디어부터 커밋까지 기능을 완성했다면 성공입니다.

> 💡 **보너스**: 4장에서 에이전트를 설정해 두었다면, 직접 만든 커스텀 에이전트도 활용해 보세요. 예를 들어 구현 리뷰용 error-handler 에이전트와 README 업데이트용 doc-writer 에이전트를 만들어 사용할 수 있습니다.

<details>
<summary>💡 힌트 (클릭해서 펼치기)</summary>

**이번 장 첫 부분의 ["한 세션으로 아이디어부터 머지된 PR까지"](#한-세션으로-아이디어부터-머지된-pr까지) 예시 패턴을 그대로 따라 보세요.** 핵심 단계는 다음과 같습니다:

1. `@samples/book-app-project/books.py`로 컨텍스트 수집
2. `/plan Add a "search by year" command`로 계획 수립
3. 메서드와 명령 핸들러 구현
4. 엣지 케이스(잘못된 입력, 결과 없음, 역순 범위)를 포함한 테스트 생성
5. `/review`로 리뷰
6. `@samples/book-app-project/README.md`로 README 업데이트
7. `-p`로 커밋 메시지 생성

**고려해야 할 엣지 케이스:**
- 사용자가 "2000"과 "1990"을 입력한다면(역순 범위)?
- 범위에 해당하는 책이 하나도 없다면?
- 사용자가 숫자가 아닌 값을 입력한다면?

**핵심은 아이디어 → 컨텍스트 → 계획 → 구현 → 테스트 → 문서 → 커밋의 전체 워크플로를 직접 연습해 보는 것**입니다.

</details>

---

<details>
<summary>🔧 <strong>흔한 실수</strong> (클릭해서 펼치기)</summary>

| 실수 | 어떤 일이 벌어지나요 | 해결 방법 |
|---------|--------------|-----|
| 곧바로 구현부터 뛰어들기 | 나중에 비싸게 고쳐야 할 설계 이슈를 놓칩니다 | 먼저 `/plan`으로 접근 방식을 정리하세요 |
| 여러 도구가 도움이 될 상황에서 한 가지만 사용하기 | 더 느리고 덜 꼼꼼한 결과 | 결합하세요: 분석은 에이전트 → 실행은 스킬 → 통합은 MCP |
| 커밋 전에 리뷰하지 않기 | 보안 이슈나 버그가 그대로 통과합니다 | 항상 `/review`를 실행하거나 [pre-commit 훅](#워크플로-2-코드-리뷰-자동화-선택)을 사용하세요 |
| 팀과 워크플로를 공유하는 것을 잊기 | 팀원마다 같은 일을 다시 만들게 됩니다 | 공용 에이전트, 스킬, 인스트럭션에 패턴을 문서화하세요 |

</details>

---

# 정리

## 🔑 핵심 정리

1. **통합 > 분리**: 도구를 결합할 때 영향력이 극대화됩니다.
2. **컨텍스트가 먼저**: 분석 전에 필요한 컨텍스트를 항상 모으세요.
3. **에이전트는 분석, 스킬은 실행**: 일에 맞는 도구를 사용하세요.
4. **반복은 자동화하기**: 훅과 스크립트는 효율을 배가시킵니다.
5. **워크플로를 문서화하기**: 공유 가능한 패턴은 팀 전체에 도움이 됩니다.

> 📋 **빠른 참고**: 전체 명령과 단축키 목록은 [GitHub Copilot CLI 명령 레퍼런스](https://docs.github.com/en/copilot/reference/cli-command-reference)를 참고하세요.

---

## 🎓 강의 완료!

축하합니다! 다음과 같은 내용을 학습했습니다:

| 장 | 학습 내용 |
|---------|-------------------|
| 00 | Copilot CLI 설치 및 빠른 시작 |
| 01 | 세 가지 상호작용 모드 |
| 02 | @ 문법을 활용한 컨텍스트 관리 |
| 03 | 개발 워크플로 |
| 04 | 전문 에이전트 |
| 05 | 확장 가능한 스킬 |
| 06 | MCP를 활용한 외부 연결 |
| 07 | 통합된 프로덕션 워크플로 |

이제 GitHub Copilot CLI를 개발 워크플로에서 진정한 생산성 증폭기로 활용할 준비가 되었습니다.

## ➡️ 다음 단계

배움은 여기서 멈추지 않습니다:

1. **매일 연습하기**: 실제 업무에 Copilot CLI를 사용해 보세요.
2. **나만의 도구 만들기**: 자신의 필요에 맞는 에이전트와 스킬을 만들어 보세요.
3. **지식 공유하기**: 팀이 이 워크플로를 도입할 수 있도록 도와주세요.
4. **최신 정보 따라가기**: GitHub Copilot의 새 기능 소식을 꾸준히 확인하세요.

### 자료

- [GitHub Copilot CLI 문서](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP 서버 레지스트리](https://github.com/modelcontextprotocol/servers)
- [커뮤니티 스킬](https://github.com/topics/copilot-skill)

---

**정말 잘하셨습니다! 이제 멋진 것을 직접 만들어 볼 차례입니다.**

[**← 6장으로 돌아가기**](../06-mcp-servers/README.md) | [**강의 홈으로 돌아가기 →**](../README.md)
