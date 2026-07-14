![챕터 01: 첫걸음](../../../01-setup-and-first-steps/images/chapter-header.png)

> **AI가 버그를 즉시 발견하고, 혼란스러운 코드를 설명하고, 동작하는 스크립트를 생성하는 모습을 봅니다. 그런 다음 GitHub Copilot CLI를 사용하는 세 가지 방식을 배웁니다.**

이 챕터에서 진정한 마법이 시작됩니다! 개발자들이 GitHub Copilot CLI를 "빠른 통화 한 통으로 시니어 엔지니어를 부르는 것"이라고 표현하는 이유를 직접 경험하게 됩니다. AI가 초 단위로 보안 버그를 발견하고, 복잡한 코드를 쉬운 영어로 설명하고, 즉시 동작하는 스크립트를 생성하는 모습을 보게 됩니다. 그런 다음 세 가지 상호작용 모드(Interactive, Plan, Programmatic)를 마스터하여 어떤 작업에 어떤 모드를 사용해야 하는지 정확히 알게 됩니다.

> ⚠️ **사전 요건**: 아직 [**챕터 00: 빠른 시작**](../00-quick-start/README.md)을 완료하지 않았다면 먼저 완료합니다. 아래 데모를 실행하기 전에 GitHub Copilot CLI가 설치되고 인증되어 있어야 합니다.

## 🎯 학습 목표

이 챕터를 마치면:

- 직접 해보는 데모를 통해 GitHub Copilot CLI가 제공하는 생산성 향상을 경험합니다
- 어떤 작업에 어떤 모드(Interactive, Plan, Programmatic)를 사용해야 하는지 선택할 수 있습니다
- 슬래시 명령어로 세션을 제어할 수 있습니다

> ⏱️ **예상 시간**: 약 45분 (읽기 15분 + 실습 30분)

---

# 첫 번째 Copilot CLI 경험

<img src="../../../01-setup-and-first-steps/images/first-copilot-experience.png" alt="모니터에 코드가 표시되고 AI 지원을 나타내는 빛나는 입자가 보이는 책상에 앉은 개발자" width="800"/>

바로 시작해서 Copilot CLI가 무엇을 할 수 있는지 확인합니다.

---

## 시작하기: 첫 번째 프롬프트

인상적인 데모에 들어가기 전에 지금 바로 시도할 수 있는 간단한 프롬프트로 시작해 봅니다. **코드 저장소가 필요 없습니다!** 터미널을 열고 Copilot CLI를 시작합니다:

```bash
copilot
```

초보자 친화적인 프롬프트를 시도합니다:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Python을 사용하지 않아도 괜찮습니다! 원하는 언어에 대해 질문하면 됩니다.

얼마나 자연스러운지 느껴 봅니다. 동료에게 묻는 것처럼 질문만 하면 됩니다. 탐색이 끝나면 `/exit`를 입력하여 세션을 종료합니다.

**핵심 통찰**: GitHub Copilot CLI는 대화형입니다. 시작하기 위해 특별한 문법이 필요 없습니다. 그냥 질문하면 됩니다.

## 실제 동작 보기

이제 개발자들이 "빠른 통화 한 통으로 시니어 엔지니어를 부르는 것"이라고 부르는 이유를 알아봅시다.

> 📖 **예제 읽는 방법**: `>`로 시작하는 줄은 대화형 Copilot CLI 세션 안에서 입력하는 프롬프트입니다. `>` 접두사가 없는 줄은 터미널에서 실행하는 쉘 명령어입니다.

> 💡 **예제 출력에 대하여**: 강의 전반에 걸쳐 표시되는 샘플 출력은 예시입니다. Copilot CLI의 응답은 매번 다르므로 단어, 형식, 세부 사항이 다를 수 있습니다. 정확한 텍스트보다는 반환되는 *정보의 유형*에 집중합니다.

### 데모 1: 초 단위 코드 리뷰

강의에는 의도적인 코드 품질 문제가 있는 샘플 파일이 포함되어 있습니다. 로컬 머신에서 작업 중이며 아직 저장소를 클론하지 않았다면 아래 `git clone` 명령어를 실행하고 `copilot-cli-for-beginners` 폴더로 이동한 다음 `copilot` 명령어를 실행합니다.

```bash
# 로컬에서 작업 중이며 아직 클론하지 않았다면 저장소를 클론합니다
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Copilot을 시작합니다
copilot
```

대화형 Copilot CLI 세션 안에서 다음을 실행합니다:

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 기호는 무엇에 사용됩니까?** `@` 기호는 Copilot CLI에게 파일을 읽으라고 지시합니다. 챕터 02에서 자세히 배울 예정입니다. 지금은 명령어를 그대로 복사합니다.

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![코드 리뷰 데모](../../../01-setup-and-first-steps/images/code-review-demo.gif)

*데모 출력은 다를 수 있습니다. 모델, 도구, 응답은 여기 표시된 것과 다를 수 있습니다.*

</details>

---

**핵심**: 몇 초 만에 전문적인 코드 리뷰가 완성됩니다. 수동 리뷰는... 그보다 훨씬 더 오래 걸립니다!

---

### 데모 2: 혼란스러운 코드 설명

코드를 보면서 이게 무엇을 하는지 의아해한 적이 있습니까? Copilot CLI 세션에서 이것을 시도합니다:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![코드 설명 데모](../../../01-setup-and-first-steps/images/explain-code-demo.gif)

*데모 출력은 다를 수 있습니다. 모델, 도구, 응답은 여기 표시된 것과 다를 수 있습니다.*

</details>

---

**결과**: (여러분의 출력은 다를 수 있습니다) Copilot CLI가 파일을 읽고, 코드를 이해하고, 쉬운 영어로 설명합니다.

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**핵심**: 인내심 있는 멘토가 설명하는 것처럼 복잡한 코드를 설명해 줍니다.

---

### 데모 3: 동작하는 코드 생성

그렇지 않으면 15분을 구글링에 쓸 함수가 필요합니까? 세션에서 계속:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![코드 생성 데모](../../../01-setup-and-first-steps/images/generate-code-demo.gif)

*데모 출력은 다를 수 있습니다. 모델, 도구, 응답은 여기 표시된 것과 다를 수 있습니다.*

</details>

---

**결과**: 복사해서 즉시 실행할 수 있는 완전한 함수가 몇 초 만에 생성됩니다.

완료되면 세션을 종료합니다:

```
> /exit
```

**핵심**: 즉각적인 결과, 그리고 전체 과정을 하나의 연속된 세션에서 진행했습니다.

---

# 모드와 명령어

<img src="../../../01-setup-and-first-steps/images/modes-and-commands.png" alt="Copilot CLI 모드와 명령어를 나타내는 빛나는 화면, 다이얼, 이퀄라이저가 있는 미래적인 제어판" width="800"/>

Copilot CLI가 무엇을 할 수 있는지 보았습니다. 이제 이러한 기능을 *효과적으로 사용하는 방법*을 이해해 봅시다. 핵심은 서로 다른 상황에 세 가지 상호작용 모드 중 어느 것을 사용할지 아는 것입니다.

> 💡 **참고**: Copilot CLI에는 여러분의 입력을 기다리지 않고 작업을 수행하는 **Autopilot** 모드도 있습니다. 강력하지만 전체 권한 부여가 필요하고 프리미엄 요청을 자율적으로 사용합니다. 이 강의는 아래 세 가지 모드에 집중합니다. 기본에 익숙해지면 Autopilot을 안내해 드리겠습니다.

---

## 🧩 실생활 비유: 외식하기

GitHub Copilot CLI를 사용하는 것을 외식하는 것에 비유해 봅니다. 식당 계획부터 주문까지, 상황마다 다른 접근이 필요합니다:

| 모드 | 외식 비유 | 사용 시기 |
|------|----------------|-------------|
| **Plan** | 식당까지 GPS 경로 | 복잡한 작업 - 경로를 파악하고, 경유지를 검토하고, 계획에 동의한 다음 출발 |
| **Interactive** | 웨이터와 대화 | 탐색 및 반복 - 질문하고, 조정하고, 실시간 피드백 받기 |
| **Programmatic** | 드라이브스루 주문 | 빠르고 구체적인 작업 - 환경에 머물면서 빠르게 결과 얻기 |

외식과 마찬가지로 각 접근 방식이 언제 적합한지 자연스럽게 배우게 됩니다.

<img src="../../../01-setup-and-first-steps/images/ordering-food-analogy.png" alt="GitHub Copilot CLI를 사용하는 세 가지 방법 - Plan 모드(식당까지 GPS 경로), Interactive 모드(웨이터와 대화), Programmatic 모드(드라이브스루)" width="800"/>

*작업에 따라 모드를 선택합니다: 계획이 먼저 필요할 때는 Plan, 대화형 협업에는 Interactive, 빠른 단발성 결과에는 Programmatic*

### 어떤 모드로 시작해야 합니까?

**Interactive 모드로 시작합니다.**
- 실험하고 후속 질문을 할 수 있습니다
- 대화를 통해 컨텍스트가 자연스럽게 쌓입니다
- 실수를 `/clear`로 쉽게 수정할 수 있습니다

익숙해지면 다음을 시도합니다:
- **Programmatic 모드** (`copilot -p "<your prompt>"`) - 빠른 일회성 질문에
- **Plan 모드** (`/plan`) - 코딩 전에 더 자세히 계획해야 할 때

---

## 세 가지 모드

### 모드 1: Interactive 모드 (여기서 시작합니다)

<img src="../../../01-setup-and-first-steps/images/interactive-mode.png" alt="Interactive 모드 - 질문에 답하고 주문을 조정할 수 있는 웨이터와 대화하는 것처럼" width="250"/>

**최적 용도**: 탐색, 반복, 다중 회전 대화. 질문에 답하고, 피드백을 받고, 즉석에서 주문을 조정할 수 있는 웨이터와 대화하는 것과 같습니다.

대화형 세션을 시작합니다:

```bash
copilot
```

지금까지 보신 것처럼 자연스럽게 타이핑할 수 있는 프롬프트가 표시됩니다. 사용 가능한 명령어에 대한 도움말을 보려면 다음을 입력합니다:

```
> /help
```

**핵심 통찰**: Interactive 모드는 컨텍스트를 유지합니다. 실제 대화처럼 각 메시지가 이전 메시지를 기반으로 합니다.

#### Interactive 모드 예제

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

각 프롬프트가 이전 답변을 기반으로 한다는 점을 주목합니다. 매번 처음부터 시작하는 것이 아니라 대화를 나누고 있습니다.

---

### 모드 2: Plan 모드

<img src="../../../01-setup-and-first-steps/images/plan-mode.png" alt="Plan 모드 - GPS를 사용하여 여행 전에 경로를 계획하는 것처럼" width="250"/>

**최적 용도**: 실행 전에 접근 방식을 검토하고 싶은 복잡한 작업. GPS를 사용하여 여행 전에 경로를 계획하는 것과 유사합니다.

Plan 모드는 코드를 작성하기 전에 단계별 계획을 세우는 데 도움을 줍니다. `/plan` 명령어를 사용하거나 **Shift+Tab**을 눌러 Plan 모드로 전환합니다:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **팁**: **Shift+Tab**으로 Interactive → Plan → Autopilot 모드를 순환합니다. 대화형 세션 중 언제든지 눌러 명령어를 입력하지 않고도 모드를 전환할 수 있습니다.

`--plan` 플래그를 사용하여 Copilot CLI를 plan 모드로 직접 시작할 수도 있습니다:

```bash
copilot --plan
```

**Plan 모드 출력:** (여러분의 출력은 다를 수 있습니다)

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**핵심 통찰**: Plan 모드를 사용하면 코드가 작성되기 전에 접근 방식을 검토하고 수정할 수 있습니다. 계획이 완료되면 나중을 위해 파일에 저장하도록 Copilot CLI에 지시할 수도 있습니다. 예를 들어 "Save this plan to `mark_as_read_plan.md`"라고 하면 계획 세부 사항이 담긴 마크다운 파일이 생성됩니다.

> 💡 **더 복잡한 것을 원합니까?** 이것을 시도합니다: `/plan Add search and filter capabilities to the book app`. Plan 모드는 간단한 기능부터 전체 애플리케이션까지 확장됩니다.

> 📚 **Autopilot 모드**: Shift+Tab이 **Autopilot**이라는 세 번째 모드를 순환한다는 것을 눈치채셨을 수 있습니다. Autopilot 모드에서 Copilot은 각 단계마다 여러분의 입력을 기다리지 않고 전체 계획을 실행합니다 — 동료에게 작업을 넘기고 "완료되면 알려줘"라고 말하는 것과 같습니다. 일반적인 워크플로우는 plan → accept → autopilot이며, 먼저 계획을 잘 작성하는 능력이 필요합니다. `copilot --autopilot`으로 직접 autopilot으로 시작할 수도 있습니다. Interactive와 Plan 모드에 먼저 익숙해진 다음 준비가 되면 [공식 문서](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)를 참조합니다.

---

### 모드 3: Programmatic 모드

<img src="../../../01-setup-and-first-steps/images/programmatic-mode.png" alt="Programmatic 모드 - 웨이터 없이 빠르게 주문하는 드라이브스루처럼" width="250"/>

**최적 용도**: 자동화, 스크립트, CI/CD, 단발성 명령어. 웨이터 없이 빠르게 주문하는 드라이브스루처럼.

상호작용이 필요 없는 일회성 명령어에는 `-p` 플래그를 사용합니다:

```bash
# 코드를 생성합니다
copilot -p "Write a function that checks if a number is even or odd"

# 빠른 도움을 받습니다
copilot -p "How do I read a JSON file in Python?"
```

**핵심 통찰**: Programmatic 모드는 빠른 답변을 제공하고 종료합니다. 대화 없이 입력 → 출력만 있습니다.

<details>
<summary>📚 <strong>더 나아가기: 스크립트에서 Programmatic 모드 사용</strong> (클릭하여 펼치기)</summary>

익숙해지면 쉘 스크립트에서 `-p`를 사용할 수 있습니다:

```bash
#!/bin/bash

# 커밋 메시지를 자동으로 생성합니다
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# 파일을 리뷰합니다
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **`--allow-all`에 대하여**: 이 플래그는 모든 권한 프롬프트를 건너뛰어 Copilot CLI가 파일 읽기, 명령어 실행, URL 접근을 먼저 묻지 않고 수행하게 합니다. 대화형 세션이 없어 작업을 승인할 수 없는 programmatic 모드(`-p`)에서는 필요합니다. 직접 작성한 프롬프트와 신뢰할 수 있는 디렉터리에서만 `--allow-all`을 사용합니다. 신뢰할 수 없는 입력이나 민감한 디렉터리에서는 절대 사용하지 않습니다.

</details>

---

## 필수 슬래시 명령어

Copilot CLI를 시작할 때 처음 배우면 좋은 명령어들입니다:

| 명령어 | 기능 | 사용 시기 |
|---------|--------------|-------------|
| `/ask` | 대화 기록에 영향을 주지 않고 빠른 질문 | 현재 작업을 방해하지 않고 빠른 답변이 필요할 때 |
| `/clear` | 대화를 지우고 새로 시작 | 주제를 전환할 때 |
| `/help` | 사용 가능한 모든 명령어 표시 | 명령어가 기억나지 않을 때 |
| `/model` | AI 모델 표시 또는 전환 | AI 모델을 변경하고 싶을 때 |
| `/plan` | 코딩 전에 작업 계획 수립 | 더 복잡한 기능에 |
| `/research` | GitHub 및 웹 소스를 사용한 심층 조사 | 코딩 전에 주제를 조사해야 할 때 |
| `/exit` | 세션 종료 | 완료되었을 때 |

> 💡 **`/ask` vs 일반 채팅**: 일반적으로 보내는 모든 메시지는 진행 중인 대화의 일부가 되어 향후 응답에 영향을 줍니다. `/ask`는 "비공개" 단축키입니다 — 세션 컨텍스트를 오염시키지 않고 `/ask What does YAML mean?`처럼 빠른 일회성 질문에 적합합니다.

> 💡 **탭 완성**: 슬래시 명령어를 입력할 때 **Tab** 키를 눌러 명령어 이름을 자동 완성하거나 사용 가능한 서브커맨드와 인수를 순환할 수 있습니다. 명령어의 정확한 이름이 기억나지 않을 때 특히 유용합니다.

시작을 위해서는 이것으로 충분합니다! 익숙해지면 추가 명령어를 탐색할 수 있습니다.

> 📚 **공식 문서**: 전체 명령어 및 플래그 목록은 [CLI 명령어 참조](https://docs.github.com/copilot/reference/cli-command-reference)를 참조합니다.

<details>
<summary>📚 <strong>추가 명령어</strong> (클릭하여 펼치기)</summary>

> 💡 위의 필수 명령어로 일상적인 사용의 많은 부분을 커버할 수 있습니다. 이 참조는 더 탐색하고 싶을 때를 위한 것입니다.

### 에이전트 환경

| 명령어 | 기능 |
|---------|--------------|
| `/agent` | 사용 가능한 에이전트 탐색 및 선택 |
| `/env` | 로드된 환경 세부 정보 표시 — 활성화된 지침, MCP 서버, 스킬, 에이전트, 플러그인 |
| `/init` | 저장소에 Copilot 지침 초기화 |
| `/mcp` | MCP 서버 구성 관리 |
| `/skills` | 향상된 기능을 위한 스킬 관리 |

> 💡 에이전트는 [챕터 04](../04-agents-custom-instructions/README.md)에서, 스킬은 [챕터 05](../05-skills/README.md)에서, MCP 서버는 [챕터 06](../06-mcp-servers/README.md)에서 다룹니다.

### 모델 및 서브에이전트

| 명령어 | 기능 |
|---------|--------------|
| `/delegate` | GitHub Copilot 클라우드 에이전트에 작업 위임 |
| `/fleet` | 복잡한 작업을 병렬 서브태스크로 분할하여 빠르게 완료 |
| `/model` | AI 모델 표시 또는 전환 |
| `/tasks` | 백그라운드 서브에이전트 및 분리된 쉘 세션 보기 |

### 코드

| 명령어 | 기능 |
|---------|--------------|
| `/diff` | 현재 디렉터리의 변경 사항 검토 |
| `/pr` | 현재 브랜치의 풀 리퀘스트 작업 |
| `/research` | GitHub 및 웹 소스를 사용한 심층 조사 실행 |
| `/review` | 코드 리뷰 에이전트를 실행하여 변경 사항 분석 |
| `/terminal-setup` | 멀티라인 입력 지원 활성화 (shift+enter 및 ctrl+enter) |

### 권한

| 명령어 | 기능 |
|---------|--------------|
| `/add-dir <directory>` | 허용 목록에 디렉터리 추가 |
| `/allow-all [on\|off\|show]` | 모든 권한 프롬프트 자동 승인; `on`으로 활성화, `off`로 비활성화, `show`로 현재 상태 확인 |
| `/yolo` | `/allow-all on`의 단축키 — 모든 권한 프롬프트 자동 승인 |
| `/cwd`, `/cd [directory]` | 작업 디렉터리 보기 또는 변경 |
| `/list-dirs` | 허용된 모든 디렉터리 표시 |

> ⚠️ **주의해서 사용합니다**: `/allow-all`과 `/yolo`는 확인 프롬프트를 건너뜁니다. 신뢰할 수 있는 프로젝트에는 좋지만 신뢰할 수 없는 코드에는 주의합니다.

### 세션

| 명령어 | 기능 |
|---------|--------------|
| `/clear` | 현재 세션을 포기하고(기록 저장 없음) 새 대화 시작 |
| `/compact` | 컨텍스트 사용량 줄이기 위해 대화 요약 |
| `/context` | 컨텍스트 창 토큰 사용량 및 시각화 표시 |
| `/keep-alive` | Copilot CLI가 활성화되는 동안 시스템 절전 방지 — 노트북에서 장시간 작업 시 유용 |
| `/new` | 현재 세션을 종료하고(검색/재개를 위해 기록에 저장) 새 대화 시작 |
| `/resume` | 다른 세션으로 전환 (선택적으로 세션 ID 또는 이름 지정) |
| `/rename` | 현재 세션 이름 변경 (이름을 생략하면 자동 생성) |
| `/rewind` | 타임라인 선택기를 열어 대화의 이전 지점으로 되돌리기 |
| `/usage` | 세션 사용량 지표 및 통계 표시 |
| `/session` | 세션 정보 및 워크스페이스 요약 표시; `/session delete`, `/session delete <id>`, `/session delete-all`로 세션 삭제 |
| `/share` | 세션을 마크다운 파일, GitHub gist, 또는 독립형 HTML 파일로 내보내기 |

### 표시

| 명령어 | 기능 |
|---------|--------------|
| `/statusline` (또는 `/footer`) | 세션 하단 상태 표시줄에 표시할 항목 사용자 정의 (디렉터리, 브랜치, 노력, 컨텍스트 창, 할당량) |
| `/theme` | 터미널 테마 보기 또는 설정 |

### 도움말 및 피드백

| 명령어 | 기능 |
|---------|--------------|
| `/changelog` | CLI 버전의 변경 로그 표시 |
| `/feedback` | GitHub에 피드백 제출 |
| `/help` | 사용 가능한 모든 명령어 표시 |

### 빠른 쉘 명령어

`!` 접두사를 사용하여 AI를 거치지 않고 쉘 명령어를 직접 실행합니다:

```bash
copilot

> !git status
# AI를 거치지 않고 git status를 직접 실행합니다

> !python -m pytest tests/
# pytest를 직접 실행합니다
```

### 모델 전환

Copilot CLI는 OpenAI, Anthropic, Google 등의 여러 AI 모델을 지원합니다. 사용 가능한 모델은 구독 수준과 지역에 따라 다릅니다. `/model`을 사용하여 옵션을 확인하고 전환합니다:

```bash
copilot
> /model

# 사용 가능한 모델을 표시하고 선택할 수 있습니다. Sonnet 4.5를 선택합니다.
```

> 💡 **팁**: 일부 모델은 다른 것보다 더 많은 "프리미엄 요청"을 소비합니다. **1x**로 표시된 모델(Claude Sonnet 4.5 등)은 훌륭한 기본값입니다. 유능하고 효율적입니다. 배수가 높은 모델은 프리미엄 요청 할당량을 더 빠르게 사용하므로 정말 필요할 때를 위해 아껴 둡니다.

> 💡 **어떤 모델을 선택해야 할지 모르겠습니까?** 모델 선택기에서 **`Auto`**를 선택하면 Copilot이 각 세션에 가장 적합한 모델을 자동으로 선택합니다. 시작 단계이고 모델 선택에 대해 고민하고 싶지 않다면 훌륭한 기본값입니다.

</details>

---

# 실습

<img src="../../../images/practice.png" alt="코드가 표시된 모니터, 램프, 커피잔, 헤드폰이 있는 아늑한 책상 설정" width="800"/>

배운 내용을 실제로 적용할 시간입니다.

---

## ▶️ 직접 해보기

### Interactive 탐색

Copilot을 시작하고 후속 프롬프트를 사용하여 도서 앱을 반복적으로 개선합니다:

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 기능 계획

`/plan`을 사용하여 Copilot CLI가 코드를 작성하기 전에 구현을 계획하게 합니다:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# 계획을 검토합니다
# 승인하거나 수정합니다
# 단계별 구현을 지켜봅니다
```

### Programmatic 모드로 자동화

`-p` 플래그를 사용하면 대화형 모드에 들어가지 않고 터미널에서 직접 Copilot CLI를 실행할 수 있습니다. 다음 스크립트를 저장소 루트에서 터미널(Copilot 안이 아닌)에 복사하여 도서 앱의 모든 Python 파일을 검토합니다.

```bash
# 도서 앱의 모든 Python 파일을 검토합니다
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# 도서 앱의 모든 Python 파일을 검토합니다
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

데모를 완료한 후 이러한 변형을 시도합니다:

1. **Interactive 챌린지**: `copilot`을 시작하고 도서 앱을 탐색합니다. `@samples/book-app-project/books.py`에 대해 묻고 연속으로 3번 개선을 요청합니다.

2. **Plan 모드 챌린지**: `/plan Add rating and review features to the book app`을 실행합니다. 계획을 꼼꼼히 읽습니다. 이해가 됩니까?

3. **Programmatic 챌린지**: `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`를 실행합니다. 처음 시도에 잘 됐습니까?

---

## 💡 팁: 웹이나 모바일에서 CLI 세션 제어하기

GitHub Copilot CLI는 **원격 세션**을 지원합니다. 터미널에 물리적으로 있지 않아도 웹 브라우저(데스크톱 또는 모바일)나 GitHub Mobile 앱에서 실행 중인 CLI 세션을 모니터링하고 상호작용할 수 있습니다.

`--remote` 플래그로 원격 세션을 시작합니다:

```bash
copilot --remote
```

Copilot CLI가 링크를 표시하고 QR 코드에 접근할 수 있게 합니다. 휴대폰이나 데스크톱 브라우저 탭에서 링크를 열어 실시간으로 세션을 확인하고, 후속 프롬프트를 전송하고, 계획을 검토하고, 원격으로 에이전트를 조종합니다. 세션은 사용자별이므로 자신의 Copilot CLI 세션에만 접근할 수 있습니다.

활성 세션 안에서 언제든지 원격 액세스를 활성화할 수도 있습니다:

```
> /remote
```

원격 세션에 대한 추가 세부 정보는 [Copilot CLI 공식 문서](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely)에서 찾을 수 있습니다.

---

## 📝 과제

### 메인 챌린지: 도서 앱 유틸리티 개선

실습 예제는 `book_app.py` 검토 및 리팩토링에 집중했습니다. 이제 다른 파일인 `utils.py`에서 동일한 기술을 연습합니다:

1. 대화형 세션 시작: `copilot`
2. 파일 요약 요청: "Summarize @samples/book-app-project/utils.py and explain what each function in this file does"
3. 입력 유효성 검사 추가 요청: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. 오류 처리 개선 요청: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. 독스트링 요청: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. 컨텍스트가 프롬프트 간에 유지되는 방식을 관찰합니다. 각 개선이 이전 것을 기반으로 합니다
7. `/exit`로 종료

**성공 기준**: 여러 단계의 대화를 통해 입력 유효성 검사, 오류 처리, 독스트링이 포함된 개선된 `utils.py`가 완성됩니다.

<details>
<summary>💡 힌트 (클릭하여 펼치기)</summary>

**시도할 샘플 프롬프트:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**흔한 문제:**
- Copilot CLI가 명확화 질문을 하면 자연스럽게 답변합니다
- 컨텍스트가 유지되므로 각 프롬프트가 이전 것을 기반으로 합니다
- 다시 시작하고 싶으면 `/clear`를 사용합니다

</details>

### 보너스 챌린지: 모드 비교하기

예제에서는 검색 기능에 `/plan`을, 배치 검토에 `-p`를 사용했습니다. 이제 새로운 작업인 `BookCollection` 클래스에 `list_by_year()` 메서드 추가를 세 가지 모드 모두로 시도합니다:

1. **Interactive**: `copilot` → 단계별로 메서드를 설계하고 구축하도록 요청
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**성찰**: 어떤 모드가 가장 자연스럽게 느껴졌습니까? 각 모드를 언제 사용하겠습니까?

---

<details>
<summary>🔧 <strong>흔한 실수 & 문제 해결</strong> (클릭하여 펼치기)</summary>

### 흔한 실수

| 실수 | 결과 | 해결 방법 |
|---------|--------------|-----|
| `/exit` 대신 `exit` 입력 | Copilot CLI가 "exit"를 명령어가 아닌 프롬프트로 처리 | 슬래시 명령어는 항상 `/`로 시작 |
| 다중 회전 대화에 `-p` 사용 | 각 `-p` 호출은 이전 호출의 기억이 없는 독립적인 것 | 컨텍스트를 쌓는 대화에는 interactive 모드(`copilot`) 사용 |
| `$`나 `!`가 포함된 프롬프트에 따옴표 없이 사용 | 쉘이 Copilot CLI가 보기 전에 특수 문자를 해석 | 프롬프트를 따옴표로 감쌉니다: `copilot -p "What does $HOME mean?"` |
| Esc를 한 번 눌러 실행 중인 작업 취소 | 단일 Esc는 더 이상 진행 중인 작업을 취소하지 않음(실수 방지) | Copilot CLI가 처리 중일 때 취소하려면 **Esc를 두 번** 누릅니다 |

### 문제 해결

**"Model not available"** - 구독에 모든 모델이 포함되지 않을 수 있습니다. `/model`을 사용하여 사용 가능한 것을 확인합니다.

**"Context too long"** - 대화가 전체 컨텍스트 창을 사용했습니다. `/clear`를 사용하여 리셋하거나 새 세션을 시작합니다.

**"Rate limit exceeded"** - 몇 분 기다렸다가 다시 시도합니다. 딜레이를 포함한 배치 작업에는 programmatic 모드를 사용하는 것을 고려합니다.

</details>

---

# 요약

## 🔑 핵심 요점

1. **Interactive 모드**는 탐색 및 반복에 적합합니다 - 컨텍스트가 이어집니다. 지금까지 한 말을 기억하는 사람과 대화하는 것과 같습니다.
2. **Plan 모드**는 일반적으로 더 복잡한 작업에 사용됩니다. 구현 전에 검토합니다.
3. **Programmatic 모드**는 자동화에 사용됩니다. 상호작용이 필요 없습니다.
4. **필수 명령어** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`)로 대부분의 일상 사용이 가능합니다.

> 📋 **빠른 참조**: 전체 명령어 및 단축키 목록은 [GitHub Copilot CLI 명령어 참조](https://docs.github.com/en/copilot/reference/cli-command-reference)를 확인합니다.

---

## ➡️ 다음 단계

세 가지 모드를 이해했으니 이제 Copilot CLI에 코드에 대한 컨텍스트를 제공하는 방법을 배워 봅시다.

[**챕터 02: 컨텍스트와 대화**](../02-context-conversations/README.md)에서 배울 내용:

- 파일과 디렉터리를 참조하는 `@` 문법
- `--resume`과 `--continue`를 사용한 세션 관리
- 컨텍스트 관리가 Copilot CLI를 진정으로 강력하게 만드는 방법

---

[**← 강의 홈으로**](../README.md) | [**챕터 02로 계속 →**](../02-context-conversations/README.md)
