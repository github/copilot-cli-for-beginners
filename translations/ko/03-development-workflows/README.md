![Chapter 03: 개발 워크플로](../../../03-development-workflows/images/chapter-header.png)

> **AI가 여러분이 미처 묻지도 않은 버그를 찾아낼 수 있다면 어떨까요?**

이번 챕터에서는 GitHub Copilot CLI가 여러분의 일상 도구가 됩니다. 매일 의존하고 있는 워크플로(테스팅, 리팩터링, 디버깅, Git) 안에서 Copilot CLI를 직접 사용해 봅니다.

## 🎯 학습 목표

이 챕터를 마치면 다음과 같은 일을 할 수 있게 됩니다.

- Copilot CLI로 종합적인 코드 리뷰 수행하기
- 레거시 코드를 안전하게 리팩터링하기
- AI의 도움으로 이슈 디버깅하기
- 자동으로 테스트 생성하기
- Copilot CLI를 git 워크플로에 통합하기

> ⏱️ **예상 소요 시간**: 약 60분 (읽기 15분 + 실습 45분)

---

## 🧩 실생활 비유: 목수의 워크플로

목수는 단순히 도구 사용법만 아는 것이 아니라, 작업별로 *워크플로*를 가지고 있습니다.

<img src="../../../03-development-workflows/images/carpenter-workflow-steps.png" alt="가구 만들기(측정, 절단, 조립, 마감), 손상 수리(평가, 제거, 수리, 매칭), 품질 점검(검사, 접합부 테스트, 정렬 확인) 세 가지 워크플로 레인을 보여 주는 장인의 작업장" width="800"/>

마찬가지로 개발자도 작업별로 워크플로를 가지고 있습니다. GitHub Copilot CLI는 이러한 각 워크플로를 향상시켜 일상적인 코딩 작업에서 더욱 효율적이고 효과적으로 일할 수 있도록 도와줍니다.

---

# 다섯 가지 워크플로

<img src="../../../03-development-workflows/images/five-workflows.png" alt="코드 리뷰, 테스팅, 디버깅, 리팩터링, git 통합 워크플로를 나타내는 다섯 개의 빛나는 네온 아이콘" width="800"/>

아래 각 워크플로는 독립적으로 구성되어 있습니다. 현재 필요한 것을 골라 보거나, 전체를 차례대로 진행해 보세요.

---

## 원하는 길을 선택하세요

이 챕터에서는 개발자가 일반적으로 사용하는 다섯 가지 워크플로를 다룹니다. **하지만 한 번에 전부 읽을 필요는 없습니다!** 각 워크플로는 아래 접을 수 있는 섹션 안에 독립적으로 들어 있습니다. 필요한 것, 그리고 현재 프로젝트에 가장 잘 맞는 것을 골라 보세요. 나머지는 나중에 다시 돌아와서 살펴봐도 됩니다.

<img src="../../../03-development-workflows/images/five-workflows-swimlane.png" alt="코드 리뷰, 리팩터링, 디버깅, 테스트 생성, Git 통합의 다섯 가지 개발 워크플로를 가로형 스윔레인으로 표현" width="800"/>

| 하고 싶은 일 | 이동하기 |
|---|---|
| 머지 전에 코드 리뷰하기 | [Workflow 1: Code Review](#workflow-1-code-review) |
| 지저분하거나 오래된 코드 정리하기 | [Workflow 2: Refactoring](#workflow-2-refactoring) |
| 버그를 추적하고 수정하기 | [Workflow 3: Debugging](#workflow-3-debugging) |
| 코드에 대한 테스트 생성하기 | [Workflow 4: Test Generation](#workflow-4-test-generation) |
| 더 나은 커밋과 PR 작성하기 | [Workflow 5: Git Integration](#workflow-5-git-integration) |
| 코딩 전에 리서치하기 | [Quick Tip: Research Before You Plan or Code](#빠른-팁-계획하거나-코딩하기-전에-먼저-리서치하기) |
| 처음부터 끝까지 버그 수정 워크플로 살펴보기 | [Putting It All Together](#모두-합치기-버그-수정-워크플로) |

**아래에서 워크플로를 선택해 펼쳐 보고**, 해당 영역에서 GitHub Copilot CLI가 개발 과정을 어떻게 향상시키는지 확인해 보세요.

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>Workflow 1: Code Review</strong> - 파일 리뷰, /review 에이전트 사용, 심각도 체크리스트 작성</summary>

<img src="../../../03-development-workflows/images/code-review-swimlane-single.png" alt="코드 리뷰 워크플로: 리뷰, 이슈 식별, 우선순위 지정, 체크리스트 생성" width="800"/>

### 기본 리뷰

이 예제에서는 `@` 기호를 사용해 파일을 참조함으로써, Copilot CLI가 리뷰를 위해 파일 내용에 직접 접근할 수 있도록 합니다.

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![Code Review Demo](../../../03-development-workflows/images/code-review-demo.gif)

*데모 출력은 매번 달라질 수 있습니다. 사용하는 모델, 도구, 응답이 여기 보이는 것과 다를 수 있습니다.*

</details>

---

### 입력 검증 리뷰

프롬프트에 신경 쓰는 카테고리를 나열해서, Copilot CLI가 특정 관심사(여기서는 입력 검증)에 집중해 리뷰하도록 요청해 보세요.

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### 크로스 파일 프로젝트 리뷰

`@`로 디렉터리 전체를 참조하면, Copilot CLI가 프로젝트 안의 모든 파일을 한꺼번에 스캔할 수 있습니다.

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### 인터랙티브 코드 리뷰

멀티턴 대화를 사용해 더 깊이 파고들어 보세요. 폭넓은 리뷰로 시작한 다음, 세션을 다시 시작하지 않고 후속 질문을 이어갈 수 있습니다.

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI provides detailed review

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI shows potential issues with empty strings, special characters

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI generates prioritized action items
```

### 리뷰 체크리스트 템플릿

Copilot CLI에게 출력 형식을 명시적으로 요청해 보세요(여기서는 이슈에 그대로 붙여넣을 수 있는 심각도별 markdown 체크리스트).

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Git 변경 사항 이해하기 (/review를 위해 중요)

`/review` 명령을 사용하기 전에 git에서의 두 가지 변경 유형을 이해해야 합니다.

| 변경 유형 | 의미 | 확인 방법 |
|-------------|---------------|------------|
| **Staged 변경** | `git add`로 다음 커밋에 포함하도록 표시한 파일 | `git diff --staged` |
| **Unstaged 변경** | 수정했지만 아직 추가하지 않은 파일 | `git diff` |

```bash
# Quick reference
git status           # Shows both staged and unstaged
git add file.py      # Stage a file for commit
git diff             # Shows unstaged changes
git diff --staged    # Shows staged changes
```

### /review 명령 사용하기

`/review` 명령은 내장된 **code-review 에이전트**를 호출하며, 이 에이전트는 staged/unstaged 변경 사항을 신호 대 잡음비가 높은 출력으로 분석하도록 최적화되어 있습니다. 자유 형식의 프롬프트를 작성하는 대신 슬래시 명령을 사용해 전문화된 내장 에이전트를 트리거하세요.

```bash
copilot

> /review
# Invokes the code-review agent on staged/unstaged changes
# Provides focused, actionable feedback

> /review Check for security issues in authentication
# Run review with specific focus area
```

> 💡 **팁**: code-review 에이전트는 변경 사항이 대기 중일 때 가장 잘 동작합니다. `git add`로 파일을 스테이징하면 더 집중된 리뷰를 받을 수 있습니다.

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>Workflow 2: Refactoring</strong> - 코드 재구성, 관심사 분리, 에러 처리 개선</summary>

<img src="../../../03-development-workflows/images/refactoring-swimlane-single.png" alt="리팩터링 워크플로: 코드 평가, 변경 계획, 구현, 동작 검증" width="800"/>

### 간단한 리팩터링

> **먼저 이것부터 시도해 보세요:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

간단한 개선부터 시작하세요. book 앱에서 다음을 시도해 보세요. 각 프롬프트는 `@` 파일 참조와 구체적인 리팩터링 지시를 함께 사용해, Copilot CLI가 무엇을 변경해야 하는지 정확히 알 수 있도록 합니다.

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **리팩터링이 처음이신가요?** 복잡한 변형을 시도하기 전에 type hint 추가나 변수명 개선처럼 간단한 요청부터 시작해 보세요.

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![Refactor Demo](../../../03-development-workflows/images/refactor-demo.gif)

*데모 출력은 매번 달라질 수 있습니다. 사용하는 모델, 도구, 응답이 여기 보이는 것과 다를 수 있습니다.*

</details>

---

### 관심사 분리

하나의 프롬프트에서 `@`로 여러 파일을 참조하면, Copilot CLI가 리팩터링의 일환으로 파일 간에 코드를 옮길 수 있습니다.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### 에러 처리 개선

관련된 두 파일을 제공하고 공통 관심사를 설명하면, Copilot CLI가 두 파일에 걸친 일관된 수정 방안을 제안할 수 있습니다.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### 문서화 추가

상세한 글머리 기호 목록을 사용해 각 docstring에 무엇이 들어가야 하는지 정확히 지정하세요.

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### 테스트와 함께 안전하게 리팩터링하기

멀티턴 대화에서 관련된 두 요청을 연이어 진행해 보세요. 먼저 테스트를 생성한 다음, 그 테스트를 안전망으로 삼아 리팩터링합니다.

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Get tests first

> Now refactor the BookCollection class to use a context manager for file operations

# Refactor with confidence - tests verify behavior is preserved
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>Workflow 3: Debugging</strong> - 버그 추적, 보안 감사, 파일 간 이슈 추적</summary>

<img src="../../../03-development-workflows/images/debugging-swimlane-single.png" alt="디버깅 워크플로: 에러 이해, 근본 원인 파악, 수정, 테스트" width="800"/>

### 간단한 디버깅

> **먼저 이것부터 시도해 보세요:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

무엇이 잘못되었는지 설명하는 것부터 시작하세요. 다음은 buggy book 앱에서 시도해 볼 수 있는 일반적인 디버깅 패턴입니다. 각 프롬프트는 `@` 파일 참조와 명확한 증상 설명을 함께 사용해, Copilot CLI가 버그를 찾고 진단할 수 있도록 합니다.

```bash
copilot

# Pattern: "Expected X but got Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Pattern: "Unexpected behavior"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Pattern: "Wrong results"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **디버깅 팁**: *증상*(보이는 현상)과 *기대값*(원래 일어나야 하는 일)을 함께 설명하세요. 나머지는 Copilot CLI가 알아서 파악합니다.

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![Fix Bug Demo](../../../03-development-workflows/images/fix-bug-demo.gif)

*데모 출력은 매번 달라질 수 있습니다. 사용하는 모델, 도구, 응답이 여기 보이는 것과 다를 수 있습니다.*

</details>

---

### "버그 탐정" - AI가 관련된 다른 버그를 찾아냅니다

이 부분에서 컨텍스트 인식 디버깅의 진가가 드러납니다. buggy book 앱에서 다음 시나리오를 시도해 보세요. `@`로 파일 전체를 제공하고, 사용자가 보고한 증상만 설명하세요. Copilot CLI는 근본 원인을 추적하고, 근처에 있는 다른 버그까지 발견해 줄 수도 있습니다.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI가 하는 일**:
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**왜 중요한가**: Copilot CLI는 파일 전체를 읽고, 버그 보고의 컨텍스트를 이해한 뒤, 명확한 설명과 함께 구체적인 수정안을 제시합니다.

> 💡 **보너스**: Copilot CLI는 파일 전체를 분석하기 때문에, 여러분이 묻지 않은 *다른* 이슈까지 발견하는 경우가 많습니다. 예를 들어, author 검색을 수정하면서 `find_book_by_title`의 대소문자 구분 버그까지 함께 짚어 줄 수도 있습니다!

### 실전 보안 사이드바

자기 코드의 디버깅도 중요하지만, 운영 애플리케이션의 보안 취약점을 이해하는 것은 매우 중요합니다. 다음 예제를 시도해 보세요. 익숙하지 않은 파일을 Copilot CLI에 가리키며 보안 이슈를 감사해 달라고 요청합니다.

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

이 파일은 운영 앱에서 실제로 마주치게 되는 보안 패턴을 보여 줍니다.

> 💡 **자주 마주치는 보안 용어:**
> - **SQL Injection**: 사용자 입력이 데이터베이스 쿼리에 직접 들어가, 공격자가 악성 명령을 실행할 수 있게 되는 취약점
> - **Parameterized queries**: 안전한 대안으로, 플레이스홀더(`?`)를 사용해 사용자 데이터와 SQL 명령을 분리합니다
> - **Race condition**: 두 작업이 동시에 일어나며 서로 간섭하는 상황
> - **XSS (Cross-Site Scripting)**: 공격자가 웹 페이지에 악성 스크립트를 주입하는 공격

---

### 에러 이해하기

스택 트레이스를 `@` 파일 참조와 함께 프롬프트에 직접 붙여넣으면, Copilot CLI가 에러를 소스 코드에 매핑할 수 있습니다.

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### 테스트 케이스로 디버깅하기

정확한 입력과 관찰된 출력을 설명해, Copilot CLI가 추론할 수 있는 구체적이고 재현 가능한 테스트 케이스를 제공하세요.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### 코드 전반에 걸친 이슈 추적

여러 파일을 참조하고 데이터 흐름을 따라가 달라고 요청하면, Copilot CLI가 이슈가 시작되는 지점을 찾아낼 수 있습니다.

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### 데이터 이슈 이해하기

데이터를 읽는 코드와 함께 데이터 파일도 포함시키면, Copilot CLI가 전체 그림을 이해한 상태에서 에러 처리 개선안을 제안할 수 있습니다.

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>Workflow 4: Test Generation</strong> - 종합적인 테스트와 엣지 케이스를 자동으로 생성</summary>

<img src="../../../03-development-workflows/images/test-gen-swimlane-single.png" alt="테스트 생성 워크플로: 함수 분석, 테스트 생성, 엣지 케이스 포함, 실행" width="800"/>

> **먼저 이것부터 시도해 보세요:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### "테스트 폭발" - 2개의 테스트 vs 15개 이상의 테스트

테스트를 직접 작성할 때 개발자들은 보통 2~3개의 기본 테스트만 만듭니다.
- 유효한 입력 테스트
- 유효하지 않은 입력 테스트
- 엣지 케이스 테스트

Copilot CLI에게 종합 테스트를 생성해 달라고 요청하면 어떤 일이 벌어지는지 보세요! 다음 프롬프트는 `@` 파일 참조와 함께 구조화된 글머리 기호 목록을 사용해, Copilot CLI가 철저한 테스트 커버리지를 달성하도록 안내합니다.

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![Test Generation Demo](../../../03-development-workflows/images/test-gen-demo.gif)

*데모 출력은 매번 달라질 수 있습니다. 사용하는 모델, 도구, 응답이 여기 보이는 것과 다를 수 있습니다.*

</details>

---

**얻게 되는 결과**: 다음을 포함한 15개 이상의 종합 테스트를 받게 됩니다.

```python
class TestBookCollection:
    # Happy path
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # Find operations
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # Edge cases
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # Data persistence
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # Special characters
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**결과**: 30초 만에, 직접 떠올리고 작성하면 한 시간이 걸릴 만한 엣지 케이스 테스트를 얻게 됩니다.

---

### 단위 테스트

특정 함수 하나를 대상으로 테스트하려는 입력 카테고리를 나열하면, Copilot CLI가 집중적이고 철저한 단위 테스트를 생성합니다.

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### 테스트 실행하기

여러분의 도구 체인에 대해 평범한 한국어(또는 영어) 질문을 Copilot CLI에 던져 보세요. 적절한 셸 명령을 생성해 줍니다.

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI responds:
# cd samples/book-app-project && python -m pytest tests/
# Or for verbose output: python -m pytest tests/ -v
# To see print statements: python -m pytest tests/ -s
```

### 특정 시나리오에 대한 테스트

해피 패스를 넘어서 다루고 싶은 까다로운 시나리오를 나열하면, Copilot CLI가 그에 맞는 테스트를 생성합니다.

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 기존 파일에 테스트 추가하기

특정 함수에 대한 *추가* 테스트를 요청하면, Copilot CLI가 기존 테스트를 보완하는 새로운 케이스를 생성해 줍니다.

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>Workflow 5: Git Integration</strong> - 커밋 메시지, PR 설명, /pr, /delegate, /diff</summary>

<img src="../../../03-development-workflows/images/git-integration-swimlane-single.png" alt="Git 통합 워크플로: 변경 사항 스테이징, 메시지 생성, 커밋, PR 생성" width="800"/>

> 💡 **이 워크플로는 기본적인 git 사용법(스테이징, 커밋, 브랜치)에 익숙하다고 가정합니다.** git이 처음이라면 다른 네 가지 워크플로를 먼저 시도해 보세요.

### 커밋 메시지 생성

> **먼저 이것부터 시도해 보세요:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — 변경 사항을 스테이징한 다음 이 명령을 실행해, Copilot CLI가 커밋 메시지를 작성하는 모습을 확인해 보세요.

이 예제는 `-p` 인라인 프롬프트 플래그를 셸 명령 치환과 함께 사용해, `git diff` 출력을 Copilot CLI에 직접 파이프하여 일회성 커밋 메시지를 생성합니다. `$(...)` 구문은 괄호 안의 명령을 실행한 뒤 그 출력을 바깥 명령에 삽입합니다.

```bash

# See what changed
git diff --staged

# Generate commit message using [Conventional Commit](../../../GLOSSARY.md#conventional-commit) format
# (structured messages like "feat(books): add search" or "fix(data): handle empty input")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Output: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![Git Integration Demo](../../../03-development-workflows/images/git-integration-demo.gif)

*데모 출력은 매번 달라질 수 있습니다. 사용하는 모델, 도구, 응답이 여기 보이는 것과 다를 수 있습니다.*

</details>

---

### 변경 사항 설명

`git show` 출력을 `-p` 프롬프트에 파이프하면, 마지막 커밋에 대한 평범한 언어의 요약을 받을 수 있습니다.

```bash
# What did this commit change?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR 설명

`git log` 출력을 구조화된 프롬프트 템플릿과 결합해, 완전한 pull request 설명을 자동으로 생성할 수 있습니다.

```bash
# Generate PR description from branch changes
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### 인터랙티브 모드에서 현재 브랜치에 /pr 사용하기

Copilot CLI의 인터랙티브 모드에서 브랜치 작업을 하고 있다면, `/pr` 명령으로 pull request 작업을 할 수 있습니다. `/pr`을 사용해 PR을 보거나, 새 PR을 만들거나, 기존 PR을 수정하거나, 브랜치 상태에 따라 Copilot CLI가 자동으로 결정하도록 할 수 있습니다.

```bash
copilot

> /pr [view|create|fix|auto]
```

### 푸시 전 리뷰

`git diff main..HEAD`를 `-p` 프롬프트 안에 넣으면, 모든 브랜치 변경 사항을 푸시 전에 빠르게 점검할 수 있습니다.

```bash
# Last check before pushing
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### 백그라운드 작업을 위한 /delegate 사용

`/delegate` 명령은 작업을 GitHub Copilot 클라우드 에이전트에 넘깁니다. `/delegate` 슬래시 명령(또는 `&` 단축키)을 사용해, 잘 정의된 작업을 백그라운드 에이전트에 위임할 수 있습니다.

```bash
copilot

> /delegate Add input validation to the login form

# Or use the & prefix shortcut:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Commits your changes to a new branch
# 2. Opens a draft pull request
# 3. Works in the background on GitHub
# 4. Requests your review when done
```

다른 작업에 집중하면서 완료시키고 싶은, 잘 정의된 작업에 매우 유용합니다.

### 세션 변경 사항 리뷰를 위한 /diff 사용

`/diff` 명령은 현재 세션 동안 이루어진 모든 변경 사항을 보여 줍니다. 커밋하기 전에 Copilot CLI가 수정한 모든 내용을 시각적인 diff로 확인할 때 이 슬래시 명령을 사용하세요.

```bash
copilot

# After making some changes...
> /diff

# Shows a visual diff of all files modified in this session
# Great for reviewing before committing
```

</details>

---

## 빠른 팁: 계획하거나 코딩하기 전에 먼저 리서치하기

라이브러리를 조사하거나, 모범 사례를 이해하거나, 익숙하지 않은 주제를 탐색해야 할 때, 코드를 작성하기 전에 `/research`를 사용해 깊이 있는 리서치를 진행해 보세요.

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot은 GitHub 저장소와 웹 자료를 검색한 뒤, 참고 자료와 함께 요약을 반환합니다. 새 기능을 시작하기 전에 정보에 기반한 결정을 내리고 싶을 때 유용합니다. 결과는 `/share`로 공유할 수 있습니다.

> 💡 **팁**: `/research`는 `/plan`보다 *먼저* 사용할 때 잘 동작합니다. 접근 방식을 리서치한 뒤, 구현을 계획하세요.

---

## 모두 합치기: 버그 수정 워크플로

다음은 보고된 버그를 수정하는 전체 워크플로입니다.

```bash

# 1. Understand the bug report
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. Debug the issue and fix (continuing in same session)
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. Generate tests for the fix
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# Exit the interactive session

> /exit

# 4. Run git add

# Stage the changes so git diff --staged has something to work with
git add .

# 5. Generate commit message
copilot -p "Generate commit message for: $(git diff --staged)"

# Example Output: "fix(books): support partial author name search"

# 6. Commit changes (optional)

git commit -m "<paste generated message>"
```

### 버그 수정 워크플로 요약

| 단계 | 작업 | Copilot 명령 |
|------|--------|-----------------|
| 1 | 버그 이해 | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | 분석 및 수정 | `> Show me the function and fix the issue` |
| 3 | 테스트 생성 | `> Generate tests for [specific scenarios]` |
| 4 | 변경 사항 스테이징 | `git add .` |
| 5 | 커밋 메시지 생성 | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | 변경 사항 커밋 | `git commit -m "<paste generated message>"` |

---

# 실습

<img src="../../../images/practice.png" alt="코드가 표시된 모니터, 램프, 커피 컵, 헤드폰이 놓인 따뜻한 분위기의 책상 - 실습 준비가 된 모습" width="800"/>

이제 여러분이 직접 이 워크플로들을 적용해 볼 차례입니다.

---

## ▶️ 직접 해 보기

데모를 끝마쳤다면, 다음 변형을 시도해 보세요.

1. **버그 탐정 챌린지**: `samples/book-app-buggy/books_buggy.py`의 `mark_as_read` 함수를 디버깅해 달라고 Copilot CLI에 요청해 보세요. 한 권만이 아니라 모든 책이 읽음 처리되는 이유를 잘 설명해 주었나요?

2. **테스트 챌린지**: book 앱의 `add_book` 함수에 대한 테스트를 생성해 보세요. 여러분이 떠올리지 못했을 엣지 케이스가 몇 개나 포함되어 있는지 세어 보세요.

3. **커밋 메시지 챌린지**: book 앱 파일에 작은 변경을 가하고 스테이징(`git add .`)한 뒤 다음을 실행해 보세요.
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   여러분이 빠르게 작성했을 것보다 메시지가 더 나은가요?

**셀프 체크**: "이 버그를 디버깅해 줘"가 "버그를 찾아 줘"보다 더 강력한 이유를 설명할 수 있다면, 개발 워크플로를 이해한 것입니다(컨텍스트가 중요합니다!).

---

## 📝 과제

### 메인 챌린지: 리팩터링, 테스트, 그리고 출시

실습 예제는 `find_book_by_title`과 코드 리뷰에 집중했습니다. 이제 `book-app-project`의 다른 함수에 동일한 워크플로 기술을 적용해 보세요.

1. **리뷰**: `books.py`의 `remove_book()`을 엣지 케이스와 잠재적 이슈 관점에서 리뷰해 달라고 Copilot CLI에 요청합니다.
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **리팩터링**: 대소문자 구분 없는 매칭이나, 책을 찾지 못했을 때 유용한 피드백을 반환하는 등 엣지 케이스를 처리하도록 `remove_book()`을 개선해 달라고 Copilot CLI에 요청합니다.
3. **테스트**: 개선된 `remove_book()` 함수에 대해 다음을 다루는 pytest 테스트를 생성합니다.
   - 존재하는 책을 제거
   - 대소문자 구분 없는 제목 매칭
   - 존재하지 않는 책에 대해 적절한 피드백 반환
   - 빈 컬렉션에서 제거
4. **리뷰**: 변경 사항을 스테이징하고 `/review`를 실행해 남아 있는 이슈가 있는지 확인합니다.
5. **커밋**: conventional commit 메시지를 생성합니다.
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 힌트 (클릭하여 펼치기)</summary>

**각 단계에 대한 샘플 프롬프트:**

```bash
copilot

# Step 1: Review
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# Step 2: Refactor
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# Step 3: Test
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# Step 4: Review
> /review

# Step 5: Commit
> Generate a conventional commit message for this refactor
```

**팁:** `remove_book()`을 개선한 뒤, Copilot CLI에 "Are there any other functions in this file that could benefit from the same improvements?"라고 물어 보세요. `find_book_by_title()`이나 `find_by_author()`에도 비슷한 변경을 제안해 줄 수 있습니다.

</details>

### 보너스 챌린지: Copilot CLI로 애플리케이션 만들기

> 💡 **참고**: 이 GitHub Skills 실습은 Python이 아니라 **Node.js**를 사용합니다. 여기서 연습하는 GitHub Copilot CLI 기법(이슈 생성, 코드 생성, 터미널에서의 협업)은 어떤 언어에든 적용할 수 있습니다.

이 실습에서는 Node.js 계산기 앱을 만들면서, GitHub Copilot CLI로 이슈를 만들고, 코드를 생성하고, 터미널에서 협업하는 방법을 보여 줍니다. CLI를 설치하고, 템플릿과 에이전트를 사용하며, 명령줄 기반의 반복적인 개발을 연습하게 됩니다.

##### <img src="../../../images/github-skills-logo.png" width="28" align="center" /> ["Create applications with the Copilot CLI" Skills 실습 시작하기](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>흔한 실수와 트러블슈팅</strong> (클릭하여 펼치기)</summary>

### 흔한 실수

| 실수 | 무슨 일이 벌어지나 | 해결 방법 |
|---------|--------------|-----|
| "Review this code"처럼 모호한 프롬프트 사용 | 구체적인 이슈를 놓친 일반적인 피드백 | 구체적으로: "Review for SQL injection, XSS, and auth issues" |
| 코드 리뷰에 `/review`를 사용하지 않음 | 최적화된 code-review 에이전트를 놓침 | 신호 대 잡음비가 높은 출력에 맞게 튜닝된 `/review` 사용 |
| 컨텍스트 없이 "find bugs"라고만 요청 | Copilot CLI가 어떤 버그를 겪고 있는지 모름 | 증상을 설명: "Users report X happens when Y" |
| 프레임워크를 지정하지 않고 테스트 생성 | 테스트가 잘못된 문법이나 단언 라이브러리를 쓸 수 있음 | 명시: "Generate tests using Jest" 또는 "using pytest" |

### 트러블슈팅

**리뷰가 불완전해 보일 때** - 무엇을 봐야 하는지 더 구체적으로 알려주세요.

```bash
copilot

# Instead of:
> Review @samples/book-app-project/book_app.py

# Try:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**테스트가 내 프레임워크와 맞지 않을 때** - 프레임워크를 지정하세요.

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**리팩터링이 동작을 바꿀 때** - 동작을 보존하라고 Copilot CLI에 요청하세요.

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# 요약

## 🔑 핵심 정리

<img src="../../../03-development-workflows/images/specialized-workflows.png" alt="모든 작업을 위한 전문 워크플로: 코드 리뷰, 리팩터링, 디버깅, 테스팅, Git 통합" width="800"/>

1. **코드 리뷰**는 구체적인 프롬프트와 함께 사용할 때 종합적이 됩니다
2. **리팩터링**은 먼저 테스트를 생성해 두면 더 안전합니다
3. **디버깅**은 Copilot CLI에 에러와 코드를 모두 보여 줄 때 효과가 큽니다
4. **테스트 생성**에는 엣지 케이스와 에러 시나리오를 포함해야 합니다
5. **Git 통합**은 커밋 메시지와 PR 설명을 자동화합니다

> 📋 **빠른 참고**: 전체 명령과 단축키 목록은 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)에서 확인하세요.

---

## ✅ 체크포인트: 핵심을 마스터했습니다

**축하합니다!** 이제 GitHub Copilot CLI로 생산적으로 일하는 데 필요한 모든 핵심 기술을 갖추었습니다.

| 기술 | 챕터 | 할 수 있게 된 것 |
|-------|---------|----------------|
| 기본 명령 | Ch 01 | 인터랙티브 모드, 플랜 모드, 프로그래매틱 모드(-p), 슬래시 명령 사용 |
| 컨텍스트 | Ch 02 | `@`로 파일 참조, 세션 관리, 컨텍스트 윈도우 이해 |
| 워크플로 | Ch 03 | 코드 리뷰, 리팩터링, 디버깅, 테스트 생성, git 통합 |

챕터 04~06은 추가적인 기능들을 다루며, 더 큰 강력함을 더해 주는 학습 가치가 있는 내용입니다.

---

## 🛠️ 나만의 워크플로 만들기

GitHub Copilot CLI를 사용하는 단 하나의 "정답"은 없습니다. 자신만의 패턴을 만들어 가는 동안 참고할 만한 몇 가지 팁입니다.

> 📚 **공식 문서**: GitHub의 권장 워크플로와 팁은 [Copilot CLI best practices](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices)에서 확인하세요.

- 사소하지 않은 작업이라면 **`/plan`으로 시작하세요.** 실행 전에 계획을 다듬으세요. 좋은 계획은 더 나은 결과로 이어집니다.
- **잘 동작한 프롬프트는 저장해 두세요.** Copilot CLI가 실수했을 때, 무엇이 잘못되었는지 메모해 두세요. 시간이 지나면 여러분만의 플레이북이 됩니다.
- **자유롭게 실험하세요.** 어떤 개발자는 길고 상세한 프롬프트를 선호하고, 어떤 개발자는 짧은 프롬프트와 후속 질문을 선호합니다. 다양한 접근 방식을 시도해 보고 자연스럽게 느껴지는 것을 찾아보세요.

> 💡 **다음에 배울 것**: 챕터 04와 05에서는 자신의 모범 사례를 Copilot CLI가 자동으로 로드하는 커스텀 인스트럭션과 스킬로 코드화하는 방법을 배웁니다.

---

## ➡️ 다음 단계

남은 챕터들은 Copilot CLI의 기능을 확장하는 추가 기능들을 다룹니다.

| 챕터 | 다루는 내용 | 언제 필요한가 |
|---------|----------------|---------------------|
| Ch 04: Agents | 전문화된 AI 페르소나 만들기 | 도메인 전문가(프론트엔드, 보안)가 필요할 때 |
| Ch 05: Skills | 작업별 인스트럭션 자동 로드 | 같은 프롬프트를 자주 반복할 때 |
| Ch 06: MCP | 외부 서비스 연결 | GitHub, 데이터베이스 등에서 실시간 데이터가 필요할 때 |

**추천**: 일주일 정도 핵심 워크플로를 사용해 본 뒤, 구체적인 필요가 생겼을 때 챕터 04~06으로 돌아오세요.

---

## 추가 주제로 계속하기

[**Chapter 04: Agents and Custom Instructions**](../04-agents-custom-instructions/README.md)에서는 다음을 배웁니다.

- 내장 에이전트(`/plan`, `/review`) 사용
- `.agent.md` 파일로 전문화된 에이전트(프론트엔드 전문가, 보안 감사자) 만들기
- 멀티 에이전트 협업 패턴
- 프로젝트 표준을 위한 커스텀 인스트럭션 파일

---

[**← Chapter 02로 돌아가기**](../02-context-conversations/README.md) | [**Chapter 04로 계속하기 →**](../04-agents-custom-instructions/README.md)
