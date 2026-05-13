![4장: 에이전트와 사용자 정의 지침](../../../04-agents-custom-instructions/images/chapter-header.png)

> **Python 코드 리뷰어, 테스트 전문가, 보안 리뷰어를... 도구 하나로 모두 고용할 수 있다면 어떨까요?**

3장에서는 코드 리뷰, 리팩터링, 디버깅, 테스트 생성, git 통합 같은 핵심 워크플로를 익혔습니다. 이러한 기능만으로도 GitHub Copilot CLI를 활용한 생산성이 크게 높아집니다. 이제 한 단계 더 나아가 봅시다.

지금까지는 Copilot CLI를 범용 어시스턴트로 사용해 왔습니다. 에이전트는 여기에 특정 페르소나와 내장된 표준을 부여할 수 있게 해 줍니다. 예를 들어 타입 힌트와 PEP 8을 강제하는 코드 리뷰어나, pytest 케이스를 작성해 주는 테스트 도우미처럼 말이지요. 동일한 프롬프트라도 목적이 분명한 지침을 가진 에이전트가 처리할 때 결과가 눈에 띄게 좋아진다는 사실을 확인하게 될 것입니다.

## 🎯 학습 목표

이 장을 마치면 다음을 할 수 있게 됩니다:

- 내장 에이전트 사용하기: Plan(`/plan`), Code-review(`/review`), 그리고 자동 에이전트(Explore, Task) 이해하기
- 에이전트 파일(`.agent.md`)을 사용해 전문화된 에이전트 만들기
- 도메인 특화 작업에 에이전트 활용하기
- `/agent`와 `--agent`로 에이전트 전환하기
- 프로젝트 고유 표준을 위한 사용자 정의 지침 파일 작성하기

> ⏱️ **예상 소요 시간**: 약 55분 (읽기 20분 + 실습 35분)

---

## 🧩 실생활 비유: 전문가를 고용하기

집에 도움이 필요할 때 "만능 도우미" 한 사람을 부르지는 않습니다. 전문가를 부릅니다:

| 문제 | 전문가 | 이유 |
|---------|------------|-----|
| 파이프 누수 | 배관공 | 배관 규정을 알고, 전문 도구를 갖추고 있음 |
| 전기 재배선 | 전기 기술자 | 안전 요건을 이해하며, 규정을 준수함 |
| 새 지붕 | 지붕 시공자 | 자재와 지역 기상 조건을 알고 있음 |

에이전트도 같은 방식으로 동작합니다. 일반적인 AI 대신, 특정 작업에 집중하고 따라야 할 올바른 절차를 아는 에이전트를 사용하세요. 한 번 지침을 설정해 두면, 코드 리뷰·테스트·보안·문서화 등 해당 전문성이 필요할 때마다 다시 활용할 수 있습니다.

<img src="../../../04-agents-custom-instructions/images/hiring-specialists-analogy.png" alt="전문가 고용 비유 - 집을 수리할 때 전문 기술자를 부르는 것처럼, AI 에이전트는 코드 리뷰, 테스트, 보안, 문서화 같은 특정 작업에 특화되어 있습니다" width="800" />

---

# 에이전트 사용하기

내장 에이전트와 사용자 정의 에이전트를 곧바로 사용해 보세요.

---

## *에이전트가 처음이신가요?* 여기서 시작하세요!
에이전트를 사용해 본 적도 만들어 본 적도 없으신가요? 이 과정을 위해 알아야 할 모든 것을 정리했습니다.

1. **지금 바로 *내장* 에이전트 사용해 보기:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   이 명령은 단계별 구현 계획을 만들기 위해 Plan 에이전트를 호출합니다.

2. **사용자 정의 에이전트 예시 살펴보기:** 에이전트의 지침을 정의하는 일은 어렵지 않습니다. 제공된 [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) 파일을 보고 패턴을 확인해 보세요.

3. **핵심 개념 이해하기:** 에이전트는 일반인이 아닌 전문가에게 자문을 구하는 것과 같습니다. "프런트엔드 에이전트"는 접근성과 컴포넌트 패턴에 자동으로 집중합니다. 에이전트 지침에 이미 명시되어 있기 때문에 매번 상기시켜 줄 필요가 없습니다.


## 내장 에이전트

**3장 개발 워크플로에서 이미 일부 내장 에이전트를 사용해 봤습니다!**
<br>`/plan`과 `/review`는 사실 내장 에이전트입니다. 이제 내부에서 무슨 일이 일어나고 있는지 알게 되었습니다. 전체 목록은 다음과 같습니다:

| 에이전트 | 호출 방법 | 하는 일 |
|-------|---------------|--------------|
| **Plan** | `/plan` 또는 `Shift+Tab` (모드 순환) | 코딩 전에 단계별 구현 계획을 작성합니다 |
| **Code-review** | `/review` | 스테이징/언스테이징된 변경 사항을 집중적이고 실행 가능한 피드백으로 리뷰합니다 |
| **Init** | `/init` | 프로젝트 구성 파일(지침, 에이전트)을 생성합니다 |
| **Explore** | *자동* | Copilot에게 코드베이스를 탐색하거나 분석하도록 요청할 때 내부적으로 사용됩니다 |
| **Task** | *자동* | 테스트, 빌드, 린트, 의존성 설치 같은 명령을 실행합니다 |

<br>

**내장 에이전트 실제 사용 예** - Plan, Code-review, Explore, Task 호출 예시

```bash
copilot

# Invoke the Plan agent to create an implementation plan
> /plan Add input validation for book year in the book app

# Invoke the Code-review agent on your changes
> /review

# Explore and Task agents are invoked automatically when relevant:
> Run the test suite        # Uses Task agent

> Explore how book data is loaded    # Uses Explore agent
```

Task 에이전트는 어떨까요? 이 에이전트는 무대 뒤에서 진행 상황을 관리·추적하고, 깔끔하고 명확한 형식으로 결과를 보고합니다:

| 결과 | 표시 내용 |
|---------|--------------|
| ✅ **성공** | 간단한 요약 (예: "All 247 tests passed", "Build succeeded") |
| ❌ **실패** | 스택 트레이스, 컴파일러 오류, 상세 로그가 포함된 전체 출력 |


> 📚 **공식 문서**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Copilot CLI에 에이전트 추가하기

자신만의 에이전트를 정의해 워크플로의 일부로 만들 수 있습니다! 한 번 정의해 두면, 그 다음에는 지시만 하면 됩니다!

<img src="../../../04-agents-custom-instructions/images/using-agents.png" alt="네 개의 다채로운 AI 로봇이 각자 다른 도구를 들고 함께 서 있는 모습 - 전문화된 에이전트의 능력을 표현" width="800"/>

## 🗂️ 에이전트 추가하기

에이전트 파일은 `.agent.md` 확장자를 가진 마크다운 파일입니다. 두 부분으로 구성됩니다: YAML 프런트매터(메타데이터)와 마크다운 지침입니다.

> 💡 **YAML 프런트매터가 처음이신가요?** 파일 맨 위에 `---` 표시로 둘러싸인 작은 설정 블록을 말합니다. YAML은 `key: value` 쌍의 모음일 뿐이며, 나머지 파일은 일반 마크다운입니다.

다음은 최소 구성의 에이전트입니다:

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **필수 vs 선택**: `description` 필드는 필수입니다. `name`, `tools`, `model` 같은 다른 필드는 선택 사항입니다.

## 에이전트 파일을 두는 위치

| 위치 | 범위 | 적합한 용도 |
|----------|-------|----------|
| `.github/agents/` | 프로젝트 전용 | 프로젝트 컨벤션이 적용된 팀 공유 에이전트 |
| `~/.copilot/agents/` | 전역 (모든 프로젝트) | 어디서든 사용하는 개인 에이전트 |

**이 프로젝트에는 [.github/agents/](../../../.github/agents/) 폴더에 샘플 에이전트 파일이 포함되어 있습니다.** 직접 작성하거나 제공된 파일을 수정해 사용할 수 있습니다.

<details>
<summary>📂 이 과정의 샘플 에이전트 살펴보기</summary>

| 파일 | 설명 |
|------|-------------|
| `hello-world.agent.md` | 최소 예시 - 여기서 시작하세요 |
| `python-reviewer.agent.md` | Python 코드 품질 리뷰어 |
| `pytest-helper.agent.md` | Pytest 테스트 전문가 |

```bash
# Or copy one to your personal agents folder (available in every project)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

더 많은 커뮤니티 에이전트는 [github/awesome-copilot](https://github.com/github/awesome-copilot)을 참고하세요.

</details>


## 🚀 사용자 정의 에이전트를 사용하는 두 가지 방법

### 대화형 모드
대화형 모드 안에서 `/agent`로 에이전트 목록을 확인하고, 함께 작업할 에이전트를 선택합니다.
선택한 에이전트와 대화를 이어 가세요.

```bash
copilot
> /agent
```

다른 에이전트로 변경하거나 기본 모드로 돌아가려면 `/agent` 명령을 다시 사용하세요.

### 프로그래매틱 모드

특정 에이전트와 함께 새 세션을 곧바로 시작합니다.

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **에이전트 전환**: 언제든 `/agent` 또는 `--agent`를 다시 사용해 다른 에이전트로 전환할 수 있습니다. 표준 Copilot CLI 환경으로 돌아가려면 `/agent`를 사용하고 **no agent**를 선택하세요.

---

# 에이전트 더 깊이 들여다보기

<img src="../../../04-agents-custom-instructions/images/creating-custom-agents.png" alt="작업대 위에서 부품과 도구에 둘러싸여 조립되고 있는 로봇 - 사용자 정의 에이전트 제작을 표현" width="800"/>

> 💡 **이 섹션은 선택 사항입니다.** 내장 에이전트(`/plan`, `/review`)만으로도 대부분의 워크플로에 충분히 강력합니다. 작업 전반에 걸쳐 일관되게 적용되는 전문성이 필요할 때 사용자 정의 에이전트를 만드세요.

아래의 각 주제는 독립적으로 구성되어 있습니다. **관심 있는 부분을 골라 읽으세요. 한 번에 다 읽을 필요는 없습니다.**

| 하고 싶은 것 | 이동할 곳 |
|---|---|
| 에이전트가 일반 프롬프트보다 나은 이유 보기 | [Specialist vs Generic](#specialist-vs-generic-see-the-difference) |
| 한 기능에 여러 에이전트 결합하기 | [Working with Multiple Agents](#working-with-multiple-agents) |
| 에이전트 정리·명명·공유하기 | [Organizing & Sharing Agents](#organizing--sharing-agents) |
| 항상 활성화되는 프로젝트 컨텍스트 설정하기 | [Configuring Your Project for Copilot](#configuring-your-project-for-copilot) |
| YAML 속성과 도구 찾아보기 | [Agent File Reference](#agent-file-reference) |

아래 시나리오를 선택해 펼쳐 보세요.

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>전문가 vs 일반 에이전트: 차이를 직접 확인하기</strong> - 에이전트가 일반 프롬프트보다 더 나은 결과를 내는 이유</summary>

## 전문가 vs 일반 에이전트: 차이를 직접 확인하기

여기서 에이전트의 가치가 분명해집니다. 차이를 살펴보세요:

### 에이전트 없이 (일반 Copilot)

```bash
copilot

> Add a function to search books by year range in the book app
```

**일반적인 출력**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

기본적입니다. 동작은 합니다. 하지만 빠진 것이 많습니다.

---

### Python Reviewer 에이전트와 함께

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
```

**전문가 수준의 출력**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewer 에이전트가 자동으로 포함하는 항목**:
- ✅ 모든 매개변수와 반환 값에 타입 힌트
- ✅ Args/Returns/Raises를 갖춘 포괄적인 docstring
- ✅ 적절한 오류 처리를 포함한 입력 검증
- ✅ 더 나은 성능을 위한 리스트 컴프리헨션
- ✅ 엣지 케이스 처리 (누락되거나 잘못된 year 값)
- ✅ PEP 8 준수 형식
- ✅ 방어적 프로그래밍 관행

**핵심 차이**: 같은 프롬프트인데, 결과는 비교할 수 없을 만큼 좋아졌습니다. 에이전트는 우리가 미처 요청하지 못했을 전문성을 함께 제공합니다.

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>여러 에이전트 함께 사용하기</strong> - 전문가 결합, 세션 도중 전환, 도구로서의 에이전트</summary>

## 여러 에이전트 함께 사용하기

진정한 힘은 전문가들이 한 기능을 위해 함께 일할 때 발휘됩니다.

### 예시: 간단한 기능 만들기

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Use python-reviewer for design
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Switch to pytest-helper for test design
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Synthesize both designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**핵심 통찰**: 여러분은 전문가들을 지휘하는 아키텍트입니다. 세부 사항은 그들이 처리하고, 비전은 여러분이 책임집니다.

<details>
<summary>🎬 실제로 동작하는 모습 보기!</summary>

![Python Reviewer 데모](../../../04-agents-custom-instructions/images/python-reviewer-demo.gif)

*데모 출력은 달라질 수 있습니다 - 사용 모델, 도구, 응답에 따라 표시되는 내용이 다를 수 있습니다.*

</details>

### 도구로서의 에이전트

에이전트가 구성되어 있으면, Copilot은 복잡한 작업을 수행하는 동안 그 에이전트를 도구로 호출할 수도 있습니다. 풀스택 기능을 요청하면 Copilot이 일부 작업을 적절한 전문가 에이전트에게 자동으로 위임할 수도 있습니다.

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>에이전트 정리 및 공유</strong> - 명명, 파일 위치, 지침 파일, 팀 공유</summary>

## 에이전트 정리 및 공유

### 에이전트 이름 짓기

에이전트 파일을 만들 때 이름은 중요합니다. `/agent`나 `--agent` 뒤에 입력하게 될 이름이며, 동료들이 에이전트 목록에서 보게 될 이름이기 때문입니다.

| ✅ 좋은 이름 | ❌ 피해야 할 이름 |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**명명 규칙:**
- 소문자와 하이픈을 사용하세요: `my-agent-name.agent.md`
- 도메인을 포함하세요: `frontend`, `backend`, `devops`, `security`
- 필요할 때는 구체적으로: 단순한 `frontend`보다 `react-typescript`처럼

---

### 팀과 공유하기

`.github/agents/`에 에이전트 파일을 두면 버전 관리됩니다. 저장소에 푸시하면 모든 팀원이 자동으로 받게 됩니다. 그런데 에이전트는 Copilot이 프로젝트에서 읽는 여러 파일 유형 중 하나일 뿐입니다. Copilot은 누군가 `/agent`를 실행하지 않아도 모든 세션에 자동으로 적용되는 **지침 파일**도 지원합니다.

이렇게 생각해 보세요: 에이전트는 필요할 때 호출하는 전문가이고, 지침 파일은 항상 활성화된 팀 규칙입니다.

### 파일을 두는 위치

이미 두 가지 주요 위치를 알고 있습니다(위 [에이전트 파일을 두는 위치](#where-to-put-agent-files) 참조). 다음 결정 트리를 참고해 선택하세요:

<img src="../../../04-agents-custom-instructions/images/agent-file-placement-decision-tree.png" alt="에이전트 파일 위치 결정 트리: 실험 중 → 현재 폴더, 팀 사용 → .github/agents/, 어디서나 → ~/.copilot/agents/" width="800"/>

**간단하게 시작하세요:** 프로젝트 폴더에 `*.agent.md` 파일 하나를 만드세요. 만족스러우면 영구적인 위치로 옮기면 됩니다.

에이전트 파일 외에도 Copilot은 `/agent` 없이 자동으로 적용되는 **프로젝트 수준 지침 파일**도 읽습니다. `AGENTS.md`, `.instructions.md`, `/init`에 대해서는 아래 [Configuring Your Project for Copilot](#configuring-your-project-for-copilot)을 참고하세요.

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Copilot용 프로젝트 구성</strong> - AGENTS.md, 지침 파일, /init 설정</summary>

## Copilot용 프로젝트 구성

에이전트는 필요할 때 호출하는 전문가입니다. **프로젝트 구성 파일**은 다릅니다. Copilot은 모든 세션에서 이 파일들을 자동으로 읽어 프로젝트의 컨벤션, 기술 스택, 규칙을 이해합니다. 누구도 `/agent`를 실행할 필요가 없으며, 저장소에서 작업하는 모든 사람에게 항상 컨텍스트가 활성화됩니다.

### /init으로 빠르게 설정하기

가장 빠른 방법은 Copilot이 직접 구성 파일을 생성하도록 하는 것입니다:

```bash
copilot
> /init
```

Copilot이 프로젝트를 스캔하여 맞춤형 지침 파일을 만들어 줍니다. 이후에 직접 편집할 수 있습니다.

### 지침 파일 형식

| 파일 | 범위 | 비고 |
|------|-------|-------|
| `AGENTS.md` | 프로젝트 루트 또는 중첩 위치 | **크로스 플랫폼 표준** - Copilot 및 다른 AI 어시스턴트에서 동작 |
| `.github/copilot-instructions.md` | 프로젝트 | GitHub Copilot 전용 |
| `.github/instructions/*.instructions.md` | 프로젝트 | 세분화된 주제별 지침 |
| `CLAUDE.md`, `GEMINI.md` | 프로젝트 루트 | 호환성을 위해 지원됨 |

> 🎯 **이제 막 시작하셨나요?** 프로젝트 지침으로 `AGENTS.md`를 사용하세요. 다른 형식은 필요에 따라 나중에 살펴볼 수 있습니다.

### AGENTS.md

`AGENTS.md`는 권장 형식입니다. Copilot 및 다른 AI 코딩 도구에서 모두 동작하는 [열린 표준](https://agents.md/)입니다. 저장소 루트에 두면 Copilot이 자동으로 읽습니다. 이 프로젝트의 [AGENTS.md](../../../AGENTS.md)는 실제 동작하는 예시입니다.

전형적인 `AGENTS.md`는 프로젝트 컨텍스트, 코드 스타일, 보안 요구 사항, 테스트 표준을 기술합니다. 예시 파일의 패턴을 따라 자신만의 파일을 작성해 보세요.

### 사용자 정의 지침 파일 (.instructions.md)

더 세밀한 제어를 원하는 팀은 지침을 주제별 파일로 분리할 수 있습니다. 각 파일은 하나의 관심사를 다루며 자동으로 적용됩니다:

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **참고**: 지침 파일은 어떤 언어와도 함께 동작합니다. 이 예시는 우리 과정 프로젝트에 맞춰 Python을 사용하지만, TypeScript, Go, Rust 또는 팀이 사용하는 어떤 기술이든 비슷한 파일을 만들 수 있습니다.

**커뮤니티 지침 파일 찾기**: [github/awesome-copilot](https://github.com/github/awesome-copilot)에서 .NET, Angular, Azure, Python, Docker 등 다양한 기술을 다루는 미리 만들어진 지침 파일을 찾아볼 수 있습니다.

### 사용자 정의 지침 비활성화

Copilot이 모든 프로젝트별 구성을 무시하도록 해야 할 때(디버깅이나 동작 비교에 유용):

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>에이전트 파일 레퍼런스</strong> - YAML 속성, 도구 별칭, 전체 예시</summary>

## 에이전트 파일 레퍼런스

### 보다 완전한 예시

위에서 [최소 에이전트 형식](#-add-your-agents)을 보았습니다. 다음은 `tools` 속성을 사용하는 보다 포괄적인 에이전트입니다. `~/.copilot/agents/python-reviewer.agent.md`를 만들어 보세요:

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### YAML 속성

| 속성 | 필수 여부 | 설명 |
|----------|----------|-------------|
| `name` | 아니요 | 표시 이름 (기본값은 파일 이름) |
| `description` | **예** | 에이전트가 하는 일 - Copilot이 언제 추천할지 이해하는 데 도움이 됩니다 |
| `tools` | 아니요 | 허용된 도구 목록 (생략하면 모든 도구 사용 가능). 아래 도구 별칭을 참고하세요. |
| `target` | 아니요 | `vscode` 또는 `github-copilot`로만 한정 |

### 도구 별칭

`tools` 목록에는 다음 이름을 사용하세요:
- `read` - 파일 내용 읽기
- `edit` - 파일 편집
- `search` - 파일 검색 (grep/glob)
- `execute` - 셸 명령 실행 (또한: `shell`, `Bash`)
- `agent` - 다른 사용자 정의 에이전트 호출

> 📖 **공식 문서**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Code 전용**: `model` 속성(AI 모델 선택용)은 VS Code에서는 동작하지만 GitHub Copilot CLI에서는 지원되지 않습니다. 크로스 플랫폼 에이전트 파일에 안전하게 포함할 수 있으며, GitHub Copilot CLI는 이를 무시합니다.

### 더 많은 에이전트 템플릿

> 💡 **초보자를 위한 참고**: 아래 예시는 템플릿입니다. **구체적인 기술은 여러분의 프로젝트에서 사용하는 것으로 바꾸세요.** 중요한 것은 에이전트의 *구조*이지, 언급된 특정 기술이 아닙니다.

이 프로젝트에는 [.github/agents/](../../../.github/agents/) 폴더에 동작하는 예시가 포함되어 있습니다:
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) - 최소 예시, 여기서 시작하세요
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) - Python 코드 품질 리뷰어
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) - Pytest 테스트 전문가

커뮤니티 에이전트는 [github/awesome-copilot](https://github.com/github/awesome-copilot)을 참고하세요.

</details>

---

# 실습

<img src="../../../images/practice.png" alt="모니터에 코드가 보이고 램프, 커피잔, 헤드폰이 놓인 따뜻한 책상 - 실습을 위한 분위기" width="800"/>

자신만의 에이전트를 만들고 실제로 동작하는 모습을 확인해 보세요.

---

## ▶️ 직접 해 보기

```bash

# Create the agents directory (if it doesn't exist)
mkdir -p .github/agents

# Create a code reviewer agent
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# Create a documentation agent
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Now use them
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# Or switch agents
copilot
> /agent
# Select "documentor"
> Document @samples/book-app-project/books.py
```

---

## 📝 과제

### 메인 챌린지: 전문화된 에이전트 팀 만들기

직접 해 보기 예시에서는 `reviewer`와 `documentor` 에이전트를 만들었습니다. 이번에는 다른 작업, 즉 책 앱의 데이터 검증을 개선하기 위해 에이전트를 만들고 사용하는 연습을 해 봅시다:

1. 책 앱에 맞춘 3개의 에이전트 파일(`.agent.md`)을 만들고, 각 에이전트당 하나씩 `.github/agents/`에 배치합니다
2. 에이전트 구성:
   - **data-validator**: `data.json`에서 누락되거나 잘못된 데이터(빈 author, year=0, 누락 필드)를 점검합니다
   - **error-handler**: Python 코드의 일관되지 않은 오류 처리를 검토하고 통합된 접근 방식을 제안합니다
   - **doc-writer**: docstring과 README 콘텐츠를 생성하거나 업데이트합니다
3. 각 에이전트를 책 앱에 사용해 보세요:
   - `data-validator` → `@samples/book-app-project/data.json` 감사
   - `error-handler` → `@samples/book-app-project/books.py`와 `@samples/book-app-project/utils.py` 검토
   - `doc-writer` → `@samples/book-app-project/books.py`에 docstring 추가
4. 협업: `error-handler`로 오류 처리의 빈틈을 찾은 다음, `doc-writer`로 개선된 접근 방식을 문서화합니다

**성공 기준**: 일관되고 높은 품질의 결과를 내는 3개의 동작하는 에이전트가 있고, `/agent`로 그 사이를 전환할 수 있어야 합니다.

<details>
<summary>💡 힌트 (펼치려면 클릭)</summary>

**스타터 템플릿**: `.github/agents/`에 에이전트별로 파일 하나씩 만드세요:

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**에이전트 테스트하기:**

> 💡 **참고:** 이미 로컬 저장소 사본에 `samples/book-app-project/data.json`이 있어야 합니다. 만약 없다면, 원본 저장소에서 원본 버전을 내려받으세요:
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Select "data-validator" from the list
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**팁:** YAML 프런트매터의 `description` 필드는 에이전트가 동작하기 위해 반드시 필요합니다.

</details>

### 보너스 챌린지: 지침 라이브러리

요청 시 호출하는 에이전트를 만들어 봤습니다. 이제 그 반대편을 시도해 보세요. **지침 파일**은 `/agent` 없이도 Copilot이 모든 세션에서 자동으로 읽는 파일입니다.

`.github/instructions/` 폴더에 최소 3개의 지침 파일을 만드세요:
- PEP 8과 타입 힌트 규칙을 강제하기 위한 `python-style.instructions.md`
- 테스트 파일에서 pytest 컨벤션을 강제하기 위한 `test-standards.instructions.md`
- JSON 데이터 항목을 검증하기 위한 `data-quality.instructions.md`

각 지침 파일을 책 앱 코드에 적용해 테스트해 보세요.

---

<details>
<summary>🔧 <strong>흔한 실수와 문제 해결</strong> (펼치려면 클릭)</summary>

### 흔한 실수

| 실수 | 발생하는 일 | 해결 방법 |
|---------|--------------|-----|
| 에이전트 프런트매터에 `description` 누락 | 에이전트가 로드되지 않거나 발견되지 않음 | YAML 프런트매터에 항상 `description:`을 포함하세요 |
| 잘못된 에이전트 파일 위치 | 사용하려고 할 때 에이전트를 찾을 수 없음 | `~/.copilot/agents/` (개인) 또는 `.github/agents/` (프로젝트)에 두세요 |
| `.agent.md` 대신 `.md` 사용 | 파일이 에이전트로 인식되지 않을 수 있음 | `python-reviewer.agent.md`처럼 파일 이름을 지정하세요 |
| 지나치게 긴 에이전트 프롬프트 | 30,000자 제한에 걸릴 수 있음 | 에이전트 정의는 집중적으로 유지하고, 상세 지침은 skill을 사용하세요 |

### 문제 해결

**에이전트를 찾을 수 없음** - 에이전트 파일이 다음 위치 중 하나에 있는지 확인하세요:
- `~/.copilot/agents/`
- `.github/agents/`

사용 가능한 에이전트 목록 보기:

```bash
copilot
> /agent
# Shows all available agents
```

**에이전트가 지침을 따르지 않음** - 프롬프트를 보다 명시적으로 작성하고 에이전트 정의에 더 많은 세부 정보를 추가하세요:
- 버전을 포함한 구체적인 프레임워크/라이브러리
- 팀 컨벤션
- 예시 코드 패턴

**사용자 정의 지침이 로드되지 않음** - 프로젝트에서 `/init`을 실행해 프로젝트별 지침을 설정하세요:

```bash
copilot
> /init
```

또는 비활성화되어 있는지 확인하세요:
```bash
# Don't use --no-custom-instructions if you want them loaded
copilot  # This loads custom instructions by default
```

</details>

---

# 요약

## 🔑 핵심 정리

1. **내장 에이전트**: `/plan`과 `/review`는 직접 호출하며, Explore와 Task는 자동으로 동작합니다
2. **사용자 정의 에이전트**는 `.agent.md` 파일에 정의된 전문가입니다
3. **좋은 에이전트**는 명확한 전문성, 표준, 출력 형식을 갖춥니다
4. **다중 에이전트 협업**은 전문성을 결합해 복잡한 문제를 해결합니다
5. **지침 파일**(`.instructions.md`)은 자동 적용되는 팀 표준을 코드화합니다
6. **일관된 결과**는 잘 정의된 에이전트 지침에서 나옵니다

> 📋 **빠른 참조**: 명령과 단축키의 전체 목록은 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)를 참고하세요.

---

## ➡️ 다음 단계

에이전트는 *Copilot이 코드에 접근하고 목적에 맞춰 행동하는 방식*을 바꿉니다. 다음으로 배울 **skill**은 *어떤 단계*를 따르는지를 바꿉니다. 에이전트와 skill의 차이가 궁금하신가요? 5장에서 정면으로 다룹니다.

**[5장: Skills 시스템](../05-skills/README.md)** 에서는 다음을 배웁니다:

- 슬래시 명령 없이 프롬프트에서 자동으로 트리거되는 skill
- 커뮤니티 skill 설치
- SKILL.md 파일로 사용자 정의 skill 만들기
- 에이전트, skill, MCP의 차이
- 각각을 언제 사용해야 하는지

---

**[← 3장으로 돌아가기](../03-development-workflows/README.md)** | **[5장으로 계속 →](../05-skills/README.md)**
