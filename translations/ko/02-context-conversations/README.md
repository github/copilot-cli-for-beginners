![2장: 컨텍스트와 대화](../../../02-context-conversations/images/chapter-header.png)

> **AI가 한 번에 한 파일이 아니라 코드베이스 전체를 볼 수 있다면 어떻습니까?**

이번 장에서는 GitHub Copilot CLI의 진짜 힘인 **컨텍스트**를 이끌어 냅니다. `@` 구문을 사용해 파일과 디렉터리를 참조하고, Copilot CLI가 여러분의 코드베이스를 깊이 이해하도록 만드는 방법을 배웁니다. 또한 세션 간 대화를 유지하는 방법, 며칠 뒤에도 정확히 멈췄던 지점에서 다시 작업을 이어 가는 방법, 그리고 단일 파일 리뷰로는 절대 잡아낼 수 없는 버그를 교차 파일 분석으로 발견하는 모습을 함께 살펴봅니다.

## 🎯 학습 목표

이번 장을 마치면 다음을 할 수 있습니다.

- `@` 구문을 사용해 파일, 디렉터리, 이미지를 참조합니다.
- `--resume`과 `--continue`로 이전 세션을 다시 이어 갑니다.
- [컨텍스트 윈도우](../../../GLOSSARY.md#context-window)가 어떻게 동작하는지 이해합니다.
- 효과적인 멀티턴 대화를 작성합니다.
- 멀티 프로젝트 워크플로를 위한 디렉터리 권한을 관리합니다.

> ⏱️ **예상 소요 시간**: 약 50분 (읽기 20분 + 실습 30분)

---

## 🧩 실생활 비유: 동료와 함께 일하기

<img src="../../../02-context-conversations/images/colleague-context-analogy.png" alt="컨텍스트가 만드는 차이 - 컨텍스트가 없을 때와 있을 때" width="800"/>

*동료와 마찬가지로 Copilot CLI도 마음을 읽지는 못합니다. 더 많은 정보를 제공하면 사람도, Copilot도 더 정확한 도움을 줄 수 있습니다!*

버그를 동료에게 설명한다고 상상해 봅니다.

> **컨텍스트 없이**: "북 앱이 동작하지 않습니다."

> **컨텍스트와 함께**: "`books.py`, 특히 `find_book_by_title` 함수를 봅니다. 대소문자 구분 없는 매칭이 안 되고 있습니다."

Copilot CLI에 컨텍스트를 제공하려면 *`@` 구문* 을 사용해 특정 파일을 가리키면 됩니다.

---

# 핵심: 기본 컨텍스트

<img src="../../../02-context-conversations/images/essential-basic-context.png" alt="Copilot CLI 대화에서 컨텍스트가 어떻게 흘러가는지를 표현한, 빛의 흐름으로 연결된 빛나는 코드 블록" width="800"/>

이 섹션은 컨텍스트를 효과적으로 다루기 위해 알아야 할 모든 것을 다룹니다. 기본기를 먼저 익힙니다.

---

## @ 구문

`@` 기호는 프롬프트 안에서 파일과 디렉터리를 참조합니다. Copilot CLI에게 "이 파일을 봅니다"라고 알려주는 방법입니다.

> 💡 **참고**: 이 코스의 모든 예제는 이 저장소에 포함된 `samples/` 폴더를 사용하므로, 어떤 명령이든 직접 따라 해 볼 수 있습니다.

### 지금 바로 시도해 보기 (별도 설정 불필요)

컴퓨터에 있는 어떤 파일로도 시도해 볼 수 있습니다.

```bash
copilot

# 가지고 있는 아무 파일이나 가리킵니다
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **마땅한 프로젝트가 없습니까?** 빠르게 테스트 파일을 만들어 봅니다.
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 기본 @ 패턴

| 패턴 | 동작 | 사용 예 |
|---------|--------------|-------------|
| `@file.py` | 파일 하나를 참조 | `Review @samples/book-app-project/books.py` |
| `@folder/` | 디렉터리 안의 모든 파일을 참조 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 여러 파일을 참조 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 단일 파일 참조

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 실제로 동작하는 모습 보기!</summary>

![파일 컨텍스트 데모](../../../02-context-conversations/images/file-context-demo.gif)

*데모 출력은 환경에 따라 달라집니다. 사용하는 모델, 도구, 응답이 여기 표시된 것과 다를 수 있습니다.*

</details>

---

### 여러 파일 참조

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### 디렉터리 전체 참조

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## 교차 파일 인텔리전스

여기서부터 컨텍스트는 진짜 슈퍼파워가 됩니다. 단일 파일 분석도 유용하지만, 교차 파일 분석은 차원이 다릅니다.

<img src="../../../02-context-conversations/images/cross-file-intelligence.png" alt="교차 파일 인텔리전스 - 단일 파일 분석과 교차 파일 분석을 비교하여, 파일을 함께 분석할 때 단일 파일에서는 보이지 않던 버그, 데이터 흐름, 패턴이 드러나는 모습" width="800"/>

### 데모: 여러 파일에 걸친 버그 찾기

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **고급 옵션**: 보안 중심의 교차 파일 분석을 원한다면 Python 보안 예제를 시도합니다.
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 실제로 동작하는 모습 보기!</summary>

![멀티 파일 데모](../../../02-context-conversations/images/multi-file-demo.gif)

*데모 출력은 환경에 따라 달라집니다. 사용하는 모델, 도구, 응답이 여기 표시된 것과 다를 수 있습니다.*

</details>

---

**Copilot CLI가 발견하는 내용**:

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**중요한 이유**: 단일 파일 리뷰로는 더 큰 그림을 놓칩니다. 교차 파일 분석만이 다음을 드러냅니다.
- 통합해야 할 **중복 코드**
- 컴포넌트 간 상호작용을 보여 주는 **데이터 흐름 패턴**
- 유지보수성에 영향을 주는 **아키텍처 문제**

---

### 데모: 60초 만에 코드베이스 이해하기

<img src="../../../02-context-conversations/images/codebase-understanding.png" alt="수동 코드 리뷰 1시간과 AI 지원 분석 10초를 비교하는 분할 화면" width="800" />

새 프로젝트에 합류했습니까? Copilot CLI를 사용해 빠르게 파악합니다.

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**얻게 되는 결과**:

```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**결과**: 코드를 한 시간 동안 읽어야 알 수 있는 내용이 10초로 압축됩니다. 어디에 집중해야 할지 정확히 알게 됩니다.

---

## 실용 예제

### 예제 1: 컨텍스트가 있는 코드 리뷰

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# 이제 Copilot CLI는 파일 전체 내용을 가지고 있어서 구체적인 피드백을 제공할 수 있습니다:
# "49번째 줄: 대소문자를 구분하는 비교 때문에 책을 놓칠 수 있습니다..."
# "29번째 줄: JSON 디코딩 오류는 잡지만 데이터 손상은 기록하지 않습니다..."

> What about @samples/book-app-project/book_app.py?

# 이제 book_app.py를 리뷰하지만, 여전히 books.py 컨텍스트도 인지하고 있습니다
```

### 예제 2: 코드베이스 이해하기

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI가 books.py를 읽고 BookCollection 클래스를 이해합니다

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI가 디렉터리를 스캔하고 요약합니다

> How does the app save and load books?

# Copilot CLI가 이미 본 코드를 통해 흐름을 추적할 수 있습니다
```

<details>
<summary>🎬 멀티턴 대화가 실제로 동작하는 모습 보기!</summary>

![멀티턴 데모](../../../02-context-conversations/images/multi-turn-demo.gif)

*데모 출력은 환경에 따라 달라집니다. 사용하는 모델, 도구, 응답이 여기 표시된 것과 다를 수 있습니다.*

</details>

### 예제 3: 멀티 파일 리팩터링

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI가 두 파일을 모두 보고 중복 코드를 어떻게 합칠지 제안할 수 있습니다
```

---

## 세션 관리

작업하는 동안 세션은 자동으로 저장됩니다. 이전 세션을 다시 열어 멈췄던 지점에서 이어 갈 수 있습니다.

### 세션 자동 저장

모든 대화는 자동으로 저장됩니다. 평소대로 종료하기만 하면 됩니다.

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... 작업을 진행 ...]

> /exit
```

### 가장 최근 세션 다시 이어 가기

```bash
# 멈췄던 지점에서 이어 갑니다
copilot --continue
```

### 특정 세션 다시 이어 가기

```bash
# 세션 목록에서 대화형으로 선택합니다
copilot --resume

# 또는 특정 세션 ID로 이어 갑니다
copilot --resume=abc123

# 또는 세션에 부여한 이름으로 이어 갑니다
copilot --resume="my book app review"
```

> 💡 **세션 ID는 어떻게 찾습니까?** 외울 필요 없습니다. ID 없이 `copilot --resume`을 실행하면 이전 세션의 이름, ID, 마지막 활동 시점이 대화형 목록으로 표시됩니다. 원하는 항목을 고르기만 하면 됩니다.
>
> **여러 터미널은 어떻게 처리됩니까?** 각 터미널 창은 자체 컨텍스트를 가진 별도의 세션입니다. Copilot CLI를 세 개의 터미널에서 열어 두었다면, 그것은 세 개의 별도 세션입니다. 어느 터미널에서든 `--resume`을 실행하면 모두 둘러볼 수 있습니다. `--continue` 플래그는 현재 작업 디렉터리의 세션을 우선 가져오고, 거기에 세션이 없으면 가장 최근에 활동한 세션을 선택합니다.
>
> **재시작하지 않고 세션을 전환할 수 있습니까?** 네. 활성 세션 안에서 `/resume` 슬래시 명령을 사용합니다.
> ```
> > /resume
> # 전환할 세션 목록을 보여 줍니다
> ```

### 세션 정리하기

나중에 찾을 수 있도록 세션에 의미 있는 이름을 부여합니다. 세션을 시작할 때 이름을 지정할 수도 있고, 세션 안에서 언제든 이름을 바꿀 수도 있습니다.

```bash
# 세션을 시작할 때 바로 이름을 지정합니다
copilot --name book-app-review

# 또는 세션 안에서 현재 세션 이름을 변경합니다
copilot

> /rename book-app-review
# 식별이 쉽도록 세션 이름이 변경되었습니다
```

세션에 이름이 부여되면 목록을 뒤지지 않고 이름으로 바로 이어 갈 수 있습니다.

```bash
copilot --resume=book-app-review
```

더 이상 필요하지 않은 세션은 세션 안에서 `/session delete`로 정리할 수 있습니다.

```bash
copilot

> /session delete            # 현재 세션 삭제
> /session delete abc123     # 특정 ID의 세션 삭제
> /session delete-all        # 모든 세션 삭제 (신중하게 사용합니다!)
```

### 컨텍스트 확인 및 관리

파일과 대화를 계속 추가하다 보면 Copilot CLI의 [컨텍스트 윈도우](../../../GLOSSARY.md#context-window)가 점점 채워집니다. 이를 통제할 수 있도록 다음과 같은 명령들이 제공됩니다.

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 현재 세션을 폐기(히스토리 저장 안 함)하고 새 대화를 시작합니다

> /new
# 현재 세션을 종료(검색/이어가기를 위해 히스토리에 저장)하고 새 대화를 시작합니다

> /rewind
# 타임라인 선택기를 열어 대화의 이전 시점으로 되돌릴 수 있게 합니다
```

> 💡 **`/clear` 또는 `/new`를 언제 사용해야 합니까?** books.py를 리뷰하다가 utils.py로 주제를 옮기고 싶다면 먼저 `/new`를 실행합니다(세션 히스토리가 필요 없다면 `/clear`). 그렇지 않으면 이전 주제의 오래된 컨텍스트가 응답을 혼란스럽게 만들 수 있습니다.

> 💡 **실수했거나 다른 접근 방식을 시도하고 싶습니까?** `/rewind`를 사용하거나 Esc를 두 번 누르면 **타임라인 선택기**가 열려, 가장 최근 시점뿐 아니라 대화의 어느 지점으로든 되돌아갈 수 있습니다. 잘못된 길로 들어섰을 때 처음부터 다시 시작하지 않고 되돌아가고 싶을 때 유용합니다.

---

### 멈췄던 지점에서 이어 가기

<img src="../../../02-context-conversations/images/session-persistence-timeline.png" alt="GitHub Copilot CLI 세션이 며칠에 걸쳐 어떻게 유지되는지 보여 주는 타임라인 - 월요일에 시작해 수요일에 전체 컨텍스트를 복원하며 다시 이어 가는 모습" width="800"/>

*세션은 종료할 때 자동으로 저장됩니다. 며칠 뒤에 다시 열어도 파일, 이슈, 진행 상황까지 전체 컨텍스트가 그대로 복원됩니다.*

여러 날에 걸친 다음 워크플로를 상상해 봅니다.

```bash
# 월요일: 처음부터 이름을 부여해 북 앱 리뷰를 시작합니다
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# 수정 작업을 진행합니다...

> /exit
```

```bash
# 수요일: 멈췄던 지점에서 이름으로 바로 이어 갑니다
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**무엇이 강력한가**: 며칠이 지나도 Copilot CLI는 다음을 기억합니다.
- 작업 중이던 정확한 파일
- 번호가 매겨진 이슈 목록
- 이미 처리한 항목
- 대화의 맥락

다시 설명할 필요도, 파일을 다시 읽을 필요도 없습니다. 그냥 이어서 작업하면 됩니다.

---

**🎉 이제 핵심을 모두 익혔습니다!** `@` 구문, 세션 관리(`--name`/`--continue`/`--resume`/`/rename`), 컨텍스트 명령(`/context`/`/clear`)만으로도 매우 생산적으로 일할 수 있습니다. 아래 내용은 모두 선택 사항입니다. 준비가 되었을 때 다시 돌아옵니다.

---

# 선택: 더 깊이 들어가기

<img src="../../../02-context-conversations/images/optional-going-deeper.png" alt="컨텍스트 개념을 더 깊이 탐험하는 모습을 표현한, 푸른빛과 보랏빛이 도는 추상적인 크리스털 동굴" width="800"/>

이 주제들은 위의 핵심 내용을 토대로 합니다. **관심 가는 것을 선택하거나, [실습](#실습)으로 바로 건너뛰어도 됩니다.**

| 알고 싶은 주제... | 이동 |
|---|---|
| 와일드카드 패턴과 고급 세션 명령 | [추가 @ 패턴 및 세션 명령](#추가-패턴) |
| 여러 프롬프트에 걸쳐 컨텍스트 쌓기 | [컨텍스트 인지 대화](#컨텍스트-인지-대화) |
| 토큰 제한과 `/compact` | [컨텍스트 윈도우 이해하기](#컨텍스트-윈도우-이해하기) |
| 참조할 파일을 어떻게 고를지 | [참조할 대상 고르기](#참조할-대상-고르기) |
| 스크린샷과 목업 분석 | [이미지 다루기](#이미지-다루기) |

<details>
<summary><strong>추가 @ 패턴 및 세션 명령</strong></summary>
<a id="additional-patterns"></a>

### 추가 @ 패턴

파워 유저를 위해 Copilot CLI는 와일드카드 패턴과 이미지 참조도 지원합니다.

| 패턴 | 동작 |
|---------|--------------|
| `@folder/*.py` | 폴더 안의 모든 .py 파일 |
| `@**/test_*.py` | 재귀 와일드카드: 어디에 있든 모든 테스트 파일 찾기 |
| `@image.png` | UI 리뷰를 위한 이미지 파일 |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### 세션 정보 보기

```bash
copilot

> /session
# 현재 세션 세부 정보와 워크스페이스 요약을 보여 줍니다

> /usage
# 세션 지표와 통계를 보여 줍니다
```

### 세션 공유하기

```bash
copilot

> /share file ./my-session.md
# 세션을 마크다운 파일로 내보냅니다

> /share gist
# 세션으로 GitHub gist를 생성합니다

> /share html
# 세션을 단독 실행 가능한 인터랙티브 HTML 파일로 내보냅니다
# 동료와 다듬어진 세션 리포트를 공유하거나 참고용으로 저장할 때 유용합니다
```

</details>

<details>
<summary><strong>컨텍스트 인지 대화</strong></summary>
<a id="context-aware-conversations"></a>

### 컨텍스트 인지 대화

진짜 마법은 서로의 결과 위에 쌓이는 멀티턴 대화에서 일어납니다.

#### 예제: 점진적 개선

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[타입이 적용된 버전을 보여 줌]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[검증과 적절한 예외 처리를 추가]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[종합적인 테스트를 생성]
```

각 프롬프트가 어떻게 이전 작업 위에 쌓이는지 살펴봅니다. 이것이 컨텍스트의 힘입니다.

</details>

<details>
<summary><strong>컨텍스트 윈도우 이해하기</strong></summary>
<a id="understanding-context-windows"></a>

### 컨텍스트 윈도우 이해하기

핵심 섹션에서 이미 `/context`와 `/clear`는 알아보았습니다. 여기서는 컨텍스트 윈도우가 어떻게 동작하는지 좀 더 깊이 들여다봅니다.

모든 AI에는 한 번에 고려할 수 있는 텍스트 양인 "컨텍스트 윈도우"가 있습니다.

<img src="../../../02-context-conversations/images/context-window-visualization.png" alt="컨텍스트 윈도우 시각화" width="800"/>

*컨텍스트 윈도우는 책상과 같습니다. 한 번에 일정량만 올려놓을 수 있습니다. 파일, 대화 기록, 시스템 프롬프트가 모두 자리를 차지합니다.*

#### 한계에 도달하면 일어나는 일

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# 파일과 대화를 추가할수록 이 값은 늘어납니다

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 경고: 컨텍스트 한계에 근접합니다

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` 명령

컨텍스트가 가득 차고 있지만 대화를 잃고 싶지 않다면, `/compact`가 히스토리를 요약해 토큰을 확보해 줍니다.

```bash
copilot

> /compact
# 대화 기록을 요약하여 컨텍스트 공간을 확보합니다
# 핵심 결과와 결정 사항은 보존됩니다
```

#### 컨텍스트 효율 팁

| 상황 | 조치 | 이유 |
|-----------|--------|-----|
| 새 주제 시작 | `/clear` | 관련 없는 컨텍스트 제거 |
| 잘못된 방향으로 진행 | `/rewind` | 어느 시점으로든 되돌리기 |
| 긴 대화 | `/compact` | 히스토리 요약, 토큰 확보 |
| 특정 파일이 필요할 때 | `@folder/`가 아니라 `@file.py` | 필요한 것만 로드 |
| 한계에 부딪힐 때 | `/new` 또는 `/clear` | 새로운 컨텍스트 |
| 여러 주제 다룰 때 | 주제별로 `/rename` 사용 | 올바른 세션을 쉽게 이어 가기 |

#### 대규모 코드베이스를 위한 모범 사례

1. **구체적으로**: `@samples/book-app-project/` 대신 `@samples/book-app-project/books.py`
2. **주제 사이에 컨텍스트 정리**: 초점이 바뀔 때 `/new` 또는 `/clear` 사용
3. **`/compact` 사용**: 대화를 요약해 컨텍스트 확보
4. **여러 세션 활용**: 기능이나 주제별로 세션을 하나씩

</details>

<details>
<summary><strong>참조할 대상 고르기</strong></summary>
<a id="choosing-what-to-reference"></a>

### 참조할 대상 고르기

컨텍스트 측면에서 모든 파일이 동등하지는 않습니다. 현명하게 고르는 방법을 알아봅시다.

#### 파일 크기 고려 사항

| 파일 크기 | 대략적인 [토큰](../../../GLOSSARY.md#token) | 전략 |
|-----------|-------------------|----------|
| 작음 (<100줄) | 약 500~1,500 토큰 | 자유롭게 참조 |
| 중간 (100~500줄) | 약 1,500~7,500 토큰 | 특정 파일 위주로 참조 |
| 큼 (500줄 이상) | 7,500+ 토큰 | 선별적으로, 특정 파일 위주 |
| 매우 큼 (1000줄 이상) | 15,000+ 토큰 | 분할하거나 섹션을 노려 참조 고려 |

**구체적인 예시:**
- 북 앱의 Python 파일 4개를 합치면 약 2,000~3,000 토큰
- 일반적인 Python 모듈(200줄) ≈ 약 3,000 토큰
- Flask API 파일(400줄) ≈ 약 6,000 토큰
- package.json ≈ 약 200~500 토큰
- 짧은 프롬프트 + 응답 ≈ 약 500~1,500 토큰

> 💡 **코드용 빠른 추정:** 코드 줄 수에 약 15를 곱하면 대략적인 토큰 수가 나옵니다. 이는 어디까지나 추정치라는 점을 기억합니다.

#### 포함할 것 vs 제외할 것

**높은 가치** (포함합니다):
- 진입점 (`book_app.py`, `main.py`, `app.py`)
- 질문하려는 바로 그 파일
- 대상 파일이 직접 임포트하는 파일
- 설정 파일 (`requirements.txt`, `pyproject.toml`)
- 데이터 모델 또는 데이터 클래스

**낮은 가치** (제외 고려):
- 생성된 파일 (컴파일 결과물, 번들된 자산)
- node modules 또는 vendor 디렉터리
- 큰 데이터 파일이나 픽스처
- 질문과 무관한 파일

#### 구체성 스펙트럼

```
Less specific ────────────────────────► More specific
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ Scans everything                     └─ Just what you need
        (uses more context)                      (preserves context)
```

**넓게 갈 때** (`@samples/book-app-project/`):
- 코드베이스 초기 탐색
- 여러 파일에 걸친 패턴 찾기
- 아키텍처 리뷰

**좁게 갈 때** (`@samples/book-app-project/books.py`):
- 특정 이슈 디버깅
- 특정 파일의 코드 리뷰
- 단일 함수에 대한 질문

#### 실전 예제: 단계적 컨텍스트 로딩

```bash
copilot

# 1단계: 구조부터 파악합니다
> @package.json What frameworks does this project use?

# 2단계: 답변에 따라 범위를 좁힙니다
> @samples/book-app-project/ Show me the project structure

# 3단계: 중요한 부분에 집중합니다
> @samples/book-app-project/books.py Review the BookCollection class

# 4단계: 필요할 때만 관련 파일을 추가합니다
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

이 단계적 접근 방식은 컨텍스트를 집중되고 효율적으로 유지합니다.

</details>

<details>
<summary><strong>이미지 다루기</strong></summary>
<a id="working-with-images"></a>

### 이미지 다루기

대화에 이미지를 포함할 수 있습니다. `@` 구문을 사용하거나, 그냥 **클립보드에서 붙여넣기**(Cmd+V / Ctrl+V)할 수 있습니다. Copilot CLI는 스크린샷, 목업, 다이어그램을 분석해 UI 디버깅, 디자인 구현, 오류 분석을 도울 수 있습니다.

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **더 알아보기**: 지원되는 형식, 실용적인 활용 사례, 이미지와 코드를 결합하는 팁은 [추가 컨텍스트 기능](../appendices/additional-context.md#이미지로-작업하기)을 참고합니다.

</details>

---

# 실습

<img src="../../../images/practice.png" alt="모니터에 코드가 떠 있고, 램프, 커피 잔, 헤드폰이 놓인 따뜻한 분위기의 데스크 셋업 - 실습 준비가 된 모습" width="800"/>

배운 컨텍스트와 세션 관리 기술을 적용해 볼 시간입니다.

---

## ▶️ 직접 해 보기

### 전체 프로젝트 리뷰

이 코스에는 바로 리뷰해 볼 수 있는 샘플 파일이 포함되어 있습니다. copilot을 시작한 뒤 다음 프롬프트를 실행합니다.

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI가 다음과 같은 이슈를 식별합니다:
# - 표시(display) 함수가 중복되었습니다
# - 입력 검증이 누락되었습니다
# - 오류 처리가 일관적이지 않습니다
```

> 💡 **자신의 파일로 시도해 보고 싶습니까?** 작은 Python 프로젝트를 만들고(`mkdir -p my-project/src`) .py 파일을 몇 개 추가한 뒤, `@my-project/src/`로 리뷰합니다. 원한다면 copilot에게 샘플 코드를 만들어 달라고 부탁할 수도 있습니다!

### 세션 워크플로

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI가 검증 방식을 제안]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 나중에 - 멈췄던 지점에서 이어 갑니다
copilot --continue

> Generate tests for the changes we made
```

---

데모를 마쳤다면 다음 변형들도 시도합니다.

1. **교차 파일 챌린지**: book_app.py와 books.py가 어떻게 함께 동작하는지 분석합니다.
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **세션 챌린지**: 세션을 시작하고 `/rename my-first-session`으로 이름을 부여한 뒤, 무언가 작업하고 `/exit`으로 나갑니다. 그런 다음 `copilot --continue`를 실행합니다. 무엇을 하고 있었는지 기억합니까?

3. **컨텍스트 챌린지**: 세션 도중에 `/context`를 실행합니다. 토큰을 얼마나 쓰고 있습니까? `/compact`를 시도한 뒤 다시 확인합니다. (`/compact`에 대한 자세한 내용은 더 깊이 들어가기의 [컨텍스트 윈도우 이해하기](#컨텍스트-윈도우-이해하기)를 참고합니다.)

**자가 점검**: 각 파일을 일일이 여는 것보다 `@folder/`가 왜 더 강력한지를 설명할 수 있다면, 컨텍스트를 이해한 것입니다.

---

## 📝 과제

### 메인 챌린지: 데이터 흐름 추적하기

실습 예제는 코드 품질 리뷰와 입력 검증에 초점을 맞췄습니다. 이제 같은 컨텍스트 기술을 다른 작업에 적용해, 데이터가 앱을 통과해 어떻게 이동하는지 추적해 봅시다.

1. 인터랙티브 세션을 시작합니다: `copilot`
2. `books.py`와 `book_app.py`를 함께 참조합니다:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. 추가 컨텍스트를 위해 데이터 파일도 가져옵니다:
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. 교차 파일 개선을 요청합니다:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. 세션 이름 변경: `/rename data-flow-analysis`
6. `/exit`로 종료한 뒤 `copilot --continue`로 다시 이어 가, 데이터 흐름에 대한 후속 질문을 합니다.

**성공 기준**: 여러 파일에 걸쳐 데이터를 추적하고, 이름이 부여된 세션을 다시 이어 가며, 교차 파일 제안을 받을 수 있어야 합니다.

<details>
<summary>💡 힌트 (펼쳐 보기)</summary>

**시작하기:**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

다음으로 이어 가기: `copilot --continue`

**유용한 명령:**
- `@file.py` - 파일 하나 참조
- `@folder/` - 폴더 안 모든 파일 참조 (끝에 `/` 주의)
- `/context` - 사용 중인 컨텍스트 양 확인
- `/rename <name>` - 쉽게 다시 이어 갈 수 있도록 세션에 이름 부여

</details>

### 보너스 챌린지: 컨텍스트 한계

1. `@samples/book-app-project/`로 북 앱 파일을 한꺼번에 모두 참조합니다.
2. 서로 다른 파일(`books.py`, `utils.py`, `book_app.py`, `data.json`)에 대해 자세한 질문을 여러 개 합니다.
3. `/context`를 실행해 사용량을 확인합니다. 얼마나 빨리 차오릅니까?
4. `/compact`로 공간을 회수하고 대화를 이어 가는 연습을 합니다.
5. 파일 참조를 더 구체적으로(예: 폴더 전체 대신 `@samples/book-app-project/books.py`) 시도해 보고, 컨텍스트 사용량이 어떻게 달라지는지 살펴봅니다.

---

<details>
<summary>🔧 <strong>흔한 실수와 문제 해결</strong> (펼쳐 보기)</summary>

### 흔한 실수

| 실수 | 발생하는 문제 | 해결 방법 |
|---------|--------------|-----|
| 파일명 앞에 `@` 빠뜨리기 | Copilot CLI가 "books.py"를 일반 텍스트로 인식 | 파일을 참조하려면 `@samples/book-app-project/books.py`처럼 작성 |
| 세션이 자동으로 유지된다고 기대 | `copilot`을 새로 시작하면 이전 컨텍스트가 모두 사라짐 | `--continue`(마지막 세션) 또는 `--resume`(세션 선택) 사용 |
| 현재 디렉터리 밖의 파일 참조 | "Permission denied" 또는 "File not found" 오류 | `/add-dir /path/to/directory`로 접근 권한 부여 |
| 주제 전환 시 `/clear`를 사용하지 않음 | 이전 컨텍스트가 새 주제 응답을 혼란스럽게 만듦 | 다른 작업을 시작하기 전에 `/clear` 실행 |

### 문제 해결

**"File not found" 오류** - 올바른 디렉터리에 있는지 확인합니다.

```bash
pwd  # 현재 디렉터리 확인
ls   # 파일 목록 확인

# 그런 다음 copilot을 시작하고 상대 경로를 사용합니다
copilot

> Review @samples/book-app-project/books.py
```

**"Permission denied"** - 디렉터리를 허용 목록에 추가합니다.

```bash
copilot --add-dir /path/to/directory

# 또는 세션 안에서 실행합니다:
> /add-dir /path/to/directory
```

**컨텍스트가 너무 빨리 차오를 때**:
- 파일 참조를 더 구체적으로
- 서로 다른 주제 사이에 `/clear` 사용
- 작업을 여러 세션에 분산

</details>

---

# 요약

## 🔑 핵심 정리

1. **`@` 구문**으로 Copilot CLI에 파일, 디렉터리, 이미지 컨텍스트를 제공합니다.
2. **멀티턴 대화**는 컨텍스트가 누적되면서 서로의 결과 위에 쌓입니다.
3. **세션은 자동 저장**됩니다: 시작 시 `--name`으로 이름을 부여하고, `--resume=<name>`으로 이름으로 이어 가거나, `--continue`로 가장 최근 세션을 이어 갑니다.
4. **컨텍스트 윈도우**에는 한계가 있습니다: `/clear`, `/compact`, `/context`, `/new`, `/rewind`로 관리합니다.
5. **권한 플래그**(`--add-dir`, `--allow-all`)로 멀티 디렉터리 접근을 통제합니다. 신중하게 사용합니다!
6. **이미지 참조**(`@screenshot.png`)는 UI 이슈를 시각적으로 디버깅하는 데 도움이 됩니다.

> 📚 **공식 문서**: 컨텍스트, 세션, 파일 작업에 대한 전체 레퍼런스는 [Use Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli)를 참고합니다.

> 📋 **빠른 참고**: 명령과 단축키의 전체 목록은 [GitHub Copilot CLI 명령 레퍼런스](https://docs.github.com/en/copilot/reference/cli-command-reference)를 확인합니다.

---

## ➡️ 다음 단계

이제 Copilot CLI에 컨텍스트를 제공할 수 있게 되었으니, 실제 개발 작업에 활용해 봅시다. 방금 배운 컨텍스트 기술(파일 참조, 교차 파일 분석, 세션 관리)은 다음 장의 강력한 워크플로의 토대가 됩니다.

[**3장: 개발 워크플로**](../03-development-workflows/README.md) 에서는 다음을 배웁니다.

- 코드 리뷰 워크플로
- 리팩터링 패턴
- 디버깅 지원
- 테스트 생성
- Git 통합

---

[**← 1장으로 돌아가기**](../01-setup-and-first-steps/README.md) | [**3장으로 계속하기 →**](../03-development-workflows/README.md)
