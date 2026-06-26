![Chapter 05: Skills System](../../../05-skills/images/chapter-header.png)

> **만약 Copilot이 매번 설명할 필요 없이 여러분 팀의 모범 사례를 자동으로 적용해 준다면 어떻습니까?**

이번 장에서는 Agent Skills(에이전트 스킬)에 대해 배웁니다. Skills는 작업과 관련될 때 Copilot이 자동으로 불러오는 지시문 폴더입니다. 에이전트가 Copilot이 *생각하는 방식*을 바꾼다면, 스킬은 Copilot에게 *작업을 완료하는 구체적인 방법*을 알려 줍니다. 보안 관련 질문을 할 때마다 Copilot이 적용하는 보안 감사 스킬을 만들고, 일관된 코드 품질을 보장하는 팀 표준 리뷰 기준을 구축하며, Copilot CLI, VS Code, GitHub Copilot 클라우드 에이전트에서 스킬이 어떻게 동작하는지 익히게 됩니다.


## 🎯 학습 목표

이 장을 마치고 나면 다음을 할 수 있습니다:

- Agent Skills의 동작 방식과 사용 시점 이해
- SKILL.md 파일로 사용자 지정 스킬 만들기
- 공유 저장소의 커뮤니티 스킬 사용
- 스킬, 에이전트, MCP를 언제 사용할지 구분

> ⏱️ **예상 소요 시간**: 약 55분 (읽기 20분 + 실습 35분)

---

## 🧩 실생활 비유: 전동 공구

범용 드릴은 유용하지만, 전용 부속을 끼우면 훨씬 강력해집니다.
<img src="../../../05-skills/images/power-tools-analogy.png" alt="전동 공구 - Copilot의 능력을 확장하는 스킬" width="800"/>


스킬도 같은 방식으로 동작합니다. 작업에 따라 드릴 비트를 바꿔 끼우듯이, 다양한 작업을 위해 Copilot에 스킬을 추가할 수 있습니다:

| 스킬 부속 | 용도 |
|------------|---------|
| `commit` | 일관된 커밋 메시지 생성 |
| `security-audit` | OWASP 취약점 점검 |
| `generate-tests` | 포괄적인 pytest 테스트 작성 |
| `code-checklist` | 팀 코드 품질 표준 적용 |



*스킬은 Copilot이 할 수 있는 일을 확장하는 전용 부속입니다*

---

# 스킬의 동작 방식

<img src="../../../05-skills/images/how-skills-work.png" alt="별이 빛나는 배경 위에 빛의 궤적으로 연결된, Copilot 스킬을 나타내는 RPG 스타일의 빛나는 스킬 아이콘들" width="800"/>

스킬이 무엇이고, 왜 중요하며, 에이전트 및 MCP와 어떻게 다른지 알아봅니다.

---

## *스킬이 처음입니까?* 여기서 시작합니다!

1. **이미 사용 가능한 스킬 확인하기:**
   ```bash
   copilot
   > /skills list
   ```
   이 명령은 Copilot이 찾을 수 있는 모든 스킬을 보여 줍니다. CLI 자체에 함께 제공되는 **기본 내장 스킬**과 프로젝트 및 개인 폴더의 스킬도 포함됩니다.

   > 💡 **기본 내장 스킬**: Copilot CLI에는 처음부터 사용할 수 있는 스킬이 미리 설치되어 있습니다. 예를 들어 `customizing-copilot-cloud-agents-environment` 스킬은 Copilot 클라우드 에이전트의 환경을 사용자 지정하는 가이드를 제공합니다. 이런 스킬은 별도로 만들거나 설치할 필요가 없습니다. `/skills list`를 실행해 어떤 스킬이 있는지 확인합니다.

2. **실제 스킬 파일 살펴보기:** 제공된 [code-checklist SKILL.md](../../../.github/skills/code-checklist/SKILL.md)를 보고 패턴을 확인합니다. YAML frontmatter와 마크다운 지시문으로만 구성되어 있습니다.

3. **핵심 개념 이해하기:** 스킬은 작업별 지시문이며, 여러분의 프롬프트가 스킬의 description과 일치하면 Copilot이 *자동으로* 불러옵니다. 따로 활성화할 필요 없이 자연스럽게 질문하기만 하면 됩니다.


## 스킬 이해하기

Agent Skills는 지시문, 스크립트, 리소스를 담은 폴더로, 작업과 관련될 때 Copilot이 **자동으로 불러옵니다**. Copilot은 여러분의 프롬프트를 읽고 일치하는 스킬이 있는지 확인한 뒤 관련 지시문을 자동으로 적용합니다.

```bash
copilot

> Check books.py against our quality checklist
# Copilot이 "code-checklist" 스킬과 일치한다고 감지합니다
# Python 품질 체크리스트를 자동으로 적용합니다

> Generate tests for the BookCollection class
# Copilot이 "pytest-gen" 스킬을 불러옵니다
# 선호하는 테스트 구조를 적용합니다

> What are the code quality issues in this file?
# Copilot이 "code-checklist" 스킬을 불러옵니다
# 팀 표준에 맞춰 점검합니다
```

> 💡 **핵심 포인트**: 스킬은 여러분의 프롬프트가 스킬의 description과 일치하면 **자동으로 트리거됩니다**. 자연스럽게 묻기만 하면 Copilot이 알아서 관련 스킬을 적용합니다. 스킬은 직접 호출할 수도 있는데, 이는 다음 절에서 다룹니다.

> 🧰 **바로 사용 가능한 템플릿**: 복사해 붙여 넣어 바로 시도해 볼 수 있는 간단한 스킬은 [.github/skills](../../../.github/skills/) 폴더에서 확인합니다.

### 슬래시 명령으로 직접 호출하기

자동 트리거가 스킬의 주된 동작 방식이지만, 스킬 이름을 슬래시 명령으로 사용해 **직접 호출**할 수도 있습니다:

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

특정 스킬이 반드시 사용되도록 명시적으로 제어하고 싶을 때 유용합니다.

#### 한 메시지에서 여러 스킬 결합하기

**한 메시지에서 두 개 이상의 스킬을 호출**할 수 있으며, 스킬 슬래시 명령은 프롬프트의 어디에든 — 맨 앞이 아니라도 — 등장할 수 있습니다. 두 가지 다른 검사를 한 번에 처리하고 싶을 때 편리합니다:

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot은 같은 응답에서 호출된 각 스킬을 모두 적용해, 메시지를 여러 번 보낼 필요를 줄여 줍니다.

> 💡 **팁**: 스킬 슬래시 명령은 문장에서 가장 자연스러운 곳에 둡니다. 메시지의 시작, 중간, 끝 어디든 좋습니다.

> 📝 **스킬 호출 vs 에이전트 호출**: 스킬 호출과 에이전트 호출을 혼동하지 마십시오:
> - **스킬**: `/skill-name <prompt>`, 예: `/code-checklist Check this file`
> - **에이전트**: `/agent` (목록에서 선택) 또는 `copilot --agent <name>` (커맨드 라인)
>
> 같은 이름의 스킬과 에이전트가 둘 다 있다면(예: "code-reviewer"), `/code-reviewer`를 입력하면 에이전트가 아닌 **스킬**이 호출됩니다.

### 스킬이 사용됐는지 어떻게 알 수 있습니까?

Copilot에게 직접 물어볼 수 있습니다:

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### 스킬 vs 에이전트 vs MCP

스킬은 GitHub Copilot 확장 모델의 한 조각일 뿐입니다. 에이전트, MCP 서버와 어떻게 비교되는지 살펴봅니다.

> *MCP는 아직 걱정하지 마십시오. [Chapter 06](../06-mcp-servers/)에서 다룹니다. 스킬이 전체 그림에 어떻게 들어맞는지 보여 주기 위해 여기에 함께 소개합니다.*

<img src="../../../05-skills/images/skills-agents-mcp-comparison.png" alt="에이전트, 스킬, MCP 서버의 차이점과 워크플로에서 어떻게 결합되는지 보여 주는 비교 다이어그램" width="800"/>

| 기능 | 하는 일 | 사용 시점 |
|---------|--------------|-------------|
| **에이전트(Agents)** | AI가 생각하는 방식을 변경 | 다양한 작업에 걸친 전문성이 필요할 때 |
| **스킬(Skills)** | 작업별 지시문을 제공 | 구체적이고 반복 가능한 작업에 자세한 단계가 필요할 때 |
| **MCP** | 외부 서비스와 연결 | API의 실시간 데이터가 필요할 때 |

폭넓은 전문성에는 에이전트, 특정 작업 지시에는 스킬, 외부 데이터에는 MCP를 사용합니다. 한 에이전트가 대화 중에 하나 이상의 스킬을 사용할 수도 있습니다. 예를 들어 에이전트에게 코드 점검을 요청하면 `security-audit` 스킬과 `code-checklist` 스킬을 자동으로 함께 적용할 수 있습니다.

> 📚 **자세히 알아보기**: 스킬 형식과 모범 사례에 대한 전체 레퍼런스는 공식 [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) 문서를 참고합니다.

---

## 수동 프롬프트에서 자동 전문성으로

스킬을 만드는 방법으로 들어가기 전에, 스킬이 *왜* 배울 만한 가치가 있는지 먼저 살펴보겠습니다. 일관성에서 얻는 이점을 보고 나면 "어떻게"가 더 잘 이해될 것입니다.

### 스킬 사용 전: 들쭉날쭉한 리뷰

매번 코드 리뷰를 할 때마다 무언가를 빠뜨릴 수 있습니다:

```bash
copilot

> Review this code for issues
# 일반 리뷰 - 팀의 구체적인 관심사를 놓칠 수 있습니다
```

또는 매번 긴 프롬프트를 작성합니다:

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

소요 시간: 입력에 **30초 이상**. 일관성: **기억에 따라 달라짐**.

### 스킬 사용 후: 자동 적용되는 모범 사례

`code-checklist` 스킬이 설치되어 있다면 자연스럽게 묻기만 하면 됩니다:

```bash
copilot

> Check the book collection code for quality issues
```

**뒤에서 일어나는 일**:
1. Copilot이 프롬프트에서 "code quality"와 "issues"를 인식합니다.
2. 스킬 description을 확인해 `code-checklist` 스킬이 일치한다고 판단합니다.
3. 팀의 품질 체크리스트를 자동으로 불러옵니다.
4. 여러분이 일일이 나열하지 않아도 모든 검사를 적용합니다.

<img src="../../../05-skills/images/skill-auto-discovery-flow.png" alt="스킬 자동 트리거 동작 방식 - Copilot이 여러분의 프롬프트를 적절한 스킬에 자동으로 매칭하는 4단계 흐름" width="800"/>

*자연스럽게 질문합니다. Copilot이 여러분의 프롬프트를 적절한 스킬에 매칭해 자동으로 적용합니다.*

**출력 예시**:
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**차이점**: 팀의 표준이 매번 자동으로 적용되며, 직접 적어 입력할 필요가 없습니다.

---

<details>
<summary>🎬 동작 모습 보기!</summary>

![Skill Trigger Demo](../../../05-skills/images/skill-trigger-demo.gif)

*데모 출력은 다양합니다. 사용하는 모델, 도구, 응답에 따라 화면과 다를 수 있습니다.*

</details>

---

## 규모에 맞는 일관성: 팀 PR 리뷰 스킬

여러분의 팀에 10가지 항목의 PR 체크리스트가 있다고 가정합니다. 스킬이 없다면 모든 개발자가 10가지를 다 기억해야 하고, 누군가는 늘 한두 개를 빠뜨립니다. `pr-review` 스킬이 있으면 팀 전체가 일관된 리뷰를 받게 됩니다:

```bash
copilot

> Can you review this PR?
```

Copilot은 팀의 `pr-review` 스킬을 자동으로 불러와 10가지 항목을 모두 점검합니다:

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**위력**: 모든 팀원이 동일한 표준을 자동으로 적용합니다. 신규 입사자가 체크리스트를 외울 필요가 없습니다. 스킬이 알아서 처리하기 때문입니다.

---

# 사용자 지정 스킬 만들기

<img src="../../../05-skills/images/creating-managing-skills.png" alt="스킬 생성과 관리를 상징하는, 빛나는 LEGO 같은 블록으로 벽을 쌓아 올리는 사람과 로봇의 손" width="800"/>

SKILL.md 파일로 직접 스킬을 만들어 봅니다.

---

## 스킬 위치

스킬은 `.github/skills/`(프로젝트 전용) 또는 `~/.copilot/skills/`(사용자 수준)에 저장합니다.

### Copilot이 스킬을 찾는 방법

Copilot은 다음 위치를 자동으로 스캔합니다:

| 위치 | 범위 |
|----------|-------|
| `.github/skills/` | 프로젝트 전용 (git을 통해 팀과 공유) |
| `~/.copilot/skills/` | 사용자 전용 (개인 스킬) |

### 스킬 구조

각 스킬은 자체 폴더 안에 `SKILL.md` 파일을 가집니다. 선택적으로 스크립트, 예제, 기타 리소스를 함께 포함할 수 있습니다:

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # 필수: 스킬 정의와 지시문입니다
    ├── examples/          # 선택 사항: Copilot이 참조할 수 있는 예제 파일입니다
    │   └── sample.py
    └── scripts/           # 선택 사항: 스킬이 사용할 수 있는 스크립트입니다
        └── validate.sh
```

> 💡 **팁**: 디렉터리 이름은 SKILL.md frontmatter의 `name`과 일치해야 합니다(소문자, 단어는 하이픈으로 구분).

### SKILL.md 형식

스킬은 YAML frontmatter가 있는 단순한 마크다운 형식을 사용합니다:

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML 속성:**

| 속성 | 필수 | 설명 |
|----------|----------|-------------|
| `name` | **예** | 고유 식별자 (소문자, 띄어쓰기 대신 하이픈 사용) |
| `description` | **예** | 스킬이 하는 일과 Copilot이 언제 사용해야 하는지 |
| `license` | 아니오 | 이 스킬에 적용되는 라이선스 |

> 📖 **공식 문서**: [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### 첫 번째 스킬 만들기

OWASP Top 10 취약점을 점검하는 보안 감사 스킬을 만듭니다:

```bash
# 스킬 디렉터리를 생성합니다
mkdir -p .github/skills/security-audit

# SKILL.md 파일을 생성합니다
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# 스킬을 테스트합니다(스킬은 프롬프트에 따라 자동으로 불러와집니다)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot이 "security vulnerabilities"가 스킬과 일치한다고 감지합니다
# OWASP 체크리스트를 자동으로 적용합니다
```

**예상 출력** (실제 결과는 달라질 수 있음):

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## 좋은 스킬 description 작성하기

SKILL.md의 `description` 필드는 매우 중요합니다! Copilot이 여러분의 스킬을 불러올지 결정하는 기준이기 때문입니다:

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **팁**: 자연스럽게 질문할 때 사용하는 키워드를 description에 포함하세요. "security review"라고 말한다면 description에도 "security review"를 넣으세요.

### 스킬과 에이전트 결합하기

스킬과 에이전트는 함께 동작합니다. 에이전트는 전문성을 제공하고, 스킬은 구체적인 지시문을 제공합니다:

```bash
# code-reviewer 에이전트로 시작합니다
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer 에이전트의 전문성이 결합됩니다
# code-checklist 스킬의 체크리스트와 함께 사용됩니다
```

---

# 스킬 관리와 공유

설치된 스킬을 확인하고, 커뮤니티 스킬을 찾아보고, 직접 만든 스킬을 공유합니다.

<img src="../../../05-skills/images/managing-sharing-skills.png" alt="CLI 스킬을 발견, 사용, 생성, 공유하는 사이클을 보여 주는 스킬 관리와 공유" width="800" />

---

## `/skills` 명령으로 스킬 관리하기

`/skills` 명령으로 설치된 스킬을 관리합니다:

| 명령 | 하는 일 |
|---------|--------------|
| `/skills list` | 설치된 모든 스킬 표시 |
| `/skills info <name>` | 특정 스킬의 세부 정보 확인 |
| `/skills add <name>` | 스킬 활성화 (저장소 또는 마켓플레이스에서) |
| `/skills remove <name>` | 스킬 비활성화 또는 제거 |
| `/skills reload` | SKILL.md 파일을 편집한 뒤 스킬 다시 불러오기 |

> 💡 **기억하세요**: 프롬프트마다 스킬을 "활성화"할 필요는 없습니다. 한 번 설치된 스킬은 프롬프트가 description과 일치하면 **자동으로 트리거됩니다**. 위 명령들은 어떤 스킬을 사용할 수 있게 할지 관리하기 위한 것이지, 스킬을 사용하기 위한 것이 아닙니다.

### 예제: 스킬 목록 보기

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>동작 모습 보기!</summary>

![List Skills Demo](../../../05-skills/images/list-skills-demo.gif)

*데모 출력은 다양합니다. 사용하는 모델, 도구, 응답에 따라 화면과 다를 수 있습니다.*

</details>

---

### `/skills reload`는 언제 사용합니까?

스킬의 SKILL.md 파일을 만들거나 수정한 뒤 `/skills reload`를 실행하면 Copilot을 재시작하지 않고도 변경 사항을 반영할 수 있습니다:

```bash
# 스킬 파일을 편집합니다
# 그런 다음 Copilot에서 실행합니다:
> /skills reload
Skills reloaded successfully.
```

> 💡 **참고**: `/compact`로 대화 기록을 요약한 뒤에도 스킬은 계속 유효합니다. 압축 후에 다시 불러올 필요는 없습니다.

---

## 커뮤니티 스킬 찾고 사용하기

### 플러그인으로 스킬 설치하기

> 💡 **플러그인이란?** 플러그인은 스킬, 에이전트, MCP 서버 구성을 함께 묶을 수 있는 설치 가능한 패키지입니다. Copilot CLI를 위한 "앱 스토어" 확장이라고 생각하면 됩니다.

`/plugin` 명령으로 이러한 패키지를 둘러보고 설치할 수 있습니다:

```bash
copilot

> /plugin list
# 설치된 플러그인을 표시합니다

> /plugin marketplace
# 사용 가능한 플러그인을 둘러봅니다

> /plugin install <plugin-name>
# 마켓플레이스에서 플러그인을 설치합니다
```

로컬 플러그인 카탈로그를 최신 상태로 유지하려면 다음을 실행해 새로 고칩니다:

```bash
copilot plugin marketplace update
```

플러그인은 여러 기능을 함께 묶을 수 있습니다. 하나의 플러그인이 서로 연관된 스킬, 에이전트, MCP 서버 구성을 함께 담고 있을 수도 있습니다.

### 커뮤니티 스킬 저장소

미리 만들어진 스킬은 커뮤니티 저장소에서도 받을 수 있습니다:

- [**Awesome Copilot**](https://github.com/github/awesome-copilot) - 스킬 문서와 예제를 포함한 공식 GitHub Copilot 리소스

### GitHub CLI로 커뮤니티 스킬 설치하기

GitHub 저장소에서 스킬을 가장 쉽게 설치하는 방법은 `gh skill install` 명령을 사용하는 것입니다([GitHub CLI v2.90.0 이상](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) 필요):

```bash
# awesome-copilot에서 스킬을 둘러보고 대화형으로 선택합니다
gh skill install github/awesome-copilot

# 또는 특정 스킬을 직접 설치합니다
gh skill install github/awesome-copilot code-checklist

# 모든 프로젝트에서 개인용으로 설치합니다(사용자 범위)
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **설치 전 확인합니다**: 스킬을 설치하기 전에는 항상 `SKILL.md`를 읽습니다. 스킬은 Copilot의 동작을 제어하기 때문에, 악의적인 스킬은 위험한 명령을 실행하거나 예기치 않은 방식으로 코드를 수정하도록 지시할 수 있습니다.

---

# 실습

<img src="../../../images/practice.png" alt="코드가 표시된 모니터, 램프, 커피잔, 헤드폰이 놓여 있어 실습 준비가 된 따뜻한 책상 환경" width="800"/>

배운 내용을 적용해 직접 스킬을 만들고 테스트해 봅니다.

---

## ▶️ 직접 해 보기

### 더 많은 스킬 만들기

서로 다른 패턴을 보여 주는 스킬 두 개를 더 만들어 봅니다. 위의 "첫 번째 스킬 만들기"에서 사용한 `mkdir` + `cat` 워크플로를 따르거나, 스킬을 적절한 위치에 복사해 붙여 넣습니다. 더 많은 예제는 [.github/skills](../../../.github/skills)에 있습니다.

### pytest 테스트 생성 스킬

코드베이스 전반에 일관된 pytest 구조를 보장하는 스킬:

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### 팀 PR 리뷰 스킬

팀 전체에 일관된 PR 리뷰 표준을 적용하는 스킬:

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### 더 나아가기

1. **스킬 만들기 챌린지**: 다음 3가지 항목을 점검하는 `quick-review` 스킬을 만듭니다:
   - bare except 절
   - 누락된 타입 힌트
   - 명확하지 않은 변수 이름

   "Do a quick review of books.py"라고 물어 테스트합니다.

2. **스킬 비교**: 자세한 보안 리뷰 프롬프트를 직접 작성하는 데 걸리는 시간을 측정합니다. 그런 다음 "Check for security issues in this file"이라고만 묻고 security-audit 스킬이 자동으로 불러와지도록 합니다. 스킬이 시간을 얼마나 절약했습니까?

3. **팀 스킬 챌린지**: 여러분 팀의 코드 리뷰 체크리스트를 떠올려 보세요. 그것을 스킬로 인코딩할 수 있습니까? 스킬이 항상 점검해야 할 3가지를 적습니다.

**자가 점검**: `description` 필드가 왜 중요한지(스킬을 불러올지 Copilot이 결정하는 기준이기 때문) 설명할 수 있다면 스킬을 이해한 것입니다.

---

## 📝 과제

### 메인 챌린지: 책 요약 스킬 만들기

위 예제에서는 `pytest-gen`과 `pr-review` 스킬을 만들었습니다. 이번에는 완전히 다른 종류의 스킬, 즉 데이터에서 형식화된 출력을 생성하는 스킬을 만들어 봅니다.

1. 현재 스킬 목록을 확인합니다: Copilot을 실행한 뒤 `/skills list`를 입력합니다. 프로젝트 스킬은 `ls .github/skills/`로, 개인 스킬은 `ls ~/.copilot/skills/`로도 확인할 수 있습니다.
2. `.github/skills/book-summary/SKILL.md`에 책 컬렉션의 형식화된 마크다운 요약을 생성하는 `book-summary` 스킬을 만듭니다.
3. 스킬에는 다음이 포함되어야 합니다:
   - 명확한 name과 description (description은 매칭에 매우 중요!)
   - 구체적인 형식 규칙 (예: title, author, year, read status로 구성된 마크다운 표)
   - 출력 규칙 (예: 읽음 여부에 ✅/❌ 사용, 연도순 정렬)
4. 스킬을 테스트합니다: `@samples/book-app-project/data.json Summarize the books in this collection`
5. `/skills list`로 스킬이 자동 트리거되는지 확인합니다.
6. `/book-summary Summarize the books in this collection`으로 직접 호출도 시도합니다.

**성공 기준**: 책 컬렉션에 대해 질문하면 Copilot이 자동으로 적용하는 동작 가능한 `book-summary` 스킬이 만들어졌습니다.

<details>
<summary>💡 힌트 (펼쳐 보기)</summary>

**시작 템플릿**: `.github/skills/book-summary/SKILL.md`를 만듭니다:

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**테스트:**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# description 일치를 기반으로 스킬이 자동 트리거되어야 합니다
```

**트리거되지 않는다면:** `/skills reload`를 실행한 뒤 다시 물어보세요.

</details>

### 보너스 챌린지: 커밋 메시지 스킬

1. 일관된 형식의 컨벤셔널 커밋 메시지를 생성하는 `commit-message` 스킬을 만듭니다.
2. 변경 사항을 스테이징한 뒤 "Generate a commit message for my staged changes"라고 물어 테스트합니다.
3. 스킬을 문서화하고 `copilot-skill` 토픽을 달아 GitHub에 공유합니다.

---

<details>
<summary>🔧 <strong>흔한 실수와 트러블슈팅</strong> (펼쳐 보기)</summary>

### 흔한 실수

| 실수 | 어떤 일이 일어나는가 | 해결 방법 |
|---------|--------------|-----|
| 파일 이름을 `SKILL.md`가 아닌 다른 이름으로 지정 | 스킬이 인식되지 않음 | 파일 이름은 정확히 `SKILL.md`여야 함 |
| 모호한 `description` 필드 | 스킬이 자동으로 불러와지지 않음 | description은 핵심 발견 메커니즘. 구체적인 트리거 단어를 사용 |
| frontmatter에 `name` 또는 `description` 누락 | 스킬 로드 실패 | YAML frontmatter에 두 필드 모두 추가 |
| 잘못된 폴더 위치 | 스킬을 찾지 못함 | `.github/skills/skill-name/`(프로젝트) 또는 `~/.copilot/skills/skill-name/`(개인) 사용 |

### 트러블슈팅

**스킬이 사용되지 않을 때** - 기대했는데 Copilot이 스킬을 사용하지 않는다면:

1. **description 확인**: 여러분이 묻는 방식과 일치합니까?
   ```markdown
   # 나쁜 예: 너무 모호합니다
   description: Reviews code

   # 좋은 예: 트리거 단어를 포함합니다
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **파일 위치 확인**:
   ```bash
   # 프로젝트 스킬입니다
   ls .github/skills/

   # 사용자 스킬입니다
   ls ~/.copilot/skills/
   ```

3. **SKILL.md 형식 확인**: frontmatter는 필수입니다:
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # 여기에 지시문을 작성합니다
   ```

**스킬이 보이지 않을 때** - 폴더 구조를 확인합니다:
```
.github/skills/
└── my-skill/           # 폴더 이름입니다
    └── SKILL.md        # 정확히 SKILL.md여야 합니다(대소문자 구분)
```

스킬을 만들거나 수정한 뒤에는 `/skills reload`를 실행해 변경 사항이 반영되도록 하세요.

**스킬이 로드되는지 확인하기** - Copilot에게 직접 물어보세요:
```bash
> What skills do you have available for checking code quality?
# Copilot이 찾은 관련 스킬을 설명합니다
```

**내 스킬이 실제로 동작하는지 어떻게 알 수 있습니까?**

1. **출력 형식 확인**: 스킬이 출력 형식(예: `[CRITICAL]` 태그)을 지정했다면 응답에서 이를 찾아보세요.
2. **직접 묻기**: 응답을 받은 뒤 "Did you use any skills for that?"라고 물어보세요.
3. **있을 때와 없을 때 비교**: 같은 프롬프트를 `--no-custom-instructions`와 함께 실행해 차이를 확인합니다:
   ```bash
   # 스킬이 있는 경우입니다
   copilot --allow-all -p "Review @file.py for security issues"

   # 스킬이 없는 경우입니다(기준선 비교)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **특정 검사 항목 확인**: 스킬이 구체적인 검사("functions over 50 lines" 등)를 포함한다면 출력에 그것이 등장하는지 확인합니다.

</details>

---

# 요약

## 🔑 핵심 정리

1. **스킬은 자동입니다**: 프롬프트가 스킬의 description과 일치하면 Copilot이 자동으로 불러옵니다.
2. **직접 호출**: `/skill-name` 슬래시 명령으로 스킬을 직접 호출할 수도 있습니다.
3. **SKILL.md 형식**: YAML frontmatter(name, description, 선택적 license)와 마크다운 지시문으로 구성됩니다.
4. **위치가 중요합니다**: 프로젝트/팀 공유는 `.github/skills/`, 개인 사용은 `~/.copilot/skills/`.
5. **description이 핵심**: 자연스럽게 묻는 방식과 일치하는 description을 작성하세요.

> 📋 **빠른 참조**: 명령과 단축키 전체 목록은 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)를 확인합니다.

---

## ➡️ 다음 단계

스킬은 자동 로드되는 지시문으로 Copilot이 할 수 있는 일을 확장합니다. 그렇다면 외부 서비스에 연결하는 것은 어떨까요? 그것이 바로 MCP의 역할입니다.

[**Chapter 06: MCP Servers**](../06-mcp-servers/README.md)에서는 다음을 배웁니다:

- MCP(Model Context Protocol)란 무엇인가
- GitHub, 파일 시스템, 문서 서비스에 연결하기
- MCP 서버 구성하기
- 다중 서버 워크플로

---

[**← Chapter 04로 돌아가기**](../04-agents-custom-instructions/README.md) | [**Chapter 06으로 계속하기 →**](../06-mcp-servers/README.md)
