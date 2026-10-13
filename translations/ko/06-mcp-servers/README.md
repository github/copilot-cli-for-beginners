![Chapter 06: MCP Servers](../../../06-mcp-servers/images/chapter-header.png)

> **Copilot이 GitHub 이슈를 읽고, 데이터베이스를 확인하고, PR까지 만들 수 있다면... 그것도 모두 터미널에서 가능하다면 어떻겠습니까?**

지금까지 Copilot은 여러분이 직접 제공한 것만 다룰 수 있었습니다. `@`로 참조한 파일, 대화 기록, 그리고 자체 학습 데이터가 그것입니다. 그런데 만약 Copilot이 스스로 GitHub 저장소를 확인하거나, 프로젝트 파일을 둘러보거나, 라이브러리의 최신 문서를 찾아볼 수 있다면 어떻겠습니까?

바로 그것이 MCP(Model Context Protocol)가 하는 일입니다. MCP는 Copilot을 외부 서비스에 연결해 실시간의 실제 데이터에 접근할 수 있게 해주는 방식입니다. Copilot이 연결되는 각 서비스를 "MCP 서버"라고 부릅니다. 이 챕터에서는 이러한 연결을 몇 가지 설정해 보고, 어떻게 Copilot을 훨씬 더 유용하게 만드는지 직접 확인해 보겠습니다.

> 💡 **이미 MCP에 익숙하다면** [퀵 스타트로 바로 이동](#내장된-github-mcp-서버로-시작하기)하여 정상 동작을 확인하고 서버 구성을 시작합니다.

## 🎯 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- MCP가 무엇이며 왜 중요한지 이해하기
- `/mcp` 명령으로 MCP 서버 관리하기
- GitHub, 파일 시스템, 문서용 MCP 서버 구성하기
- book app 프로젝트에서 MCP 기반 워크플로 사용하기
- 커스텀 MCP 서버를 언제, 어떻게 만들지 알기 (선택)

> ⏱️ **예상 소요 시간**: 약 50분 (읽기 15분 + 실습 35분)

---

## 🧩 실생활 비유: 브라우저 확장 프로그램

<img src="../../../06-mcp-servers/images/browser-extensions-analogy.png" alt="MCP 서버는 브라우저 확장 프로그램과 같습니다" width="800"/>

MCP 서버를 브라우저 확장 프로그램이라고 생각해 보십시오. 브라우저 자체로도 웹 페이지를 보여줄 수 있지만, 확장 프로그램은 브라우저를 추가 서비스에 연결해 줍니다:

| 브라우저 확장 | 연결되는 대상 | MCP 등가물 |
|-------------------|---------------------|----------------|
| 비밀번호 관리자 | 비밀번호 저장소 | **GitHub MCP** → 저장소, 이슈, PR |
| Grammarly | 글쓰기 분석 서비스 | **Context7 MCP** → 라이브러리 문서 |
| 파일 관리자 | 클라우드 저장소 | **Filesystem MCP** → 로컬 프로젝트 파일 |

확장 프로그램이 없어도 브라우저는 충분히 유용하지만, 확장 프로그램이 있으면 강력한 도구가 됩니다. MCP 서버도 Copilot에게 같은 일을 합니다. 실시간의 실제 데이터 소스에 연결해 주어, GitHub 이슈를 읽고, 파일 시스템을 탐색하고, 최신 문서를 가져오는 등 더 많은 일을 자동으로 할 수 있게 해줍니다.

***MCP 서버는 Copilot을 외부 세계와 연결합니다: GitHub, 저장소, 문서 등***

> 💡 **핵심 인사이트**: MCP가 없으면 Copilot은 여러분이 `@`로 명시적으로 공유한 파일만 볼 수 있습니다. MCP가 있으면 프로젝트를 능동적으로 탐색하고, GitHub 저장소를 확인하고, 문서를 찾아볼 수 있습니다. 모든 것이 자동으로요.

---

<img src="../../../06-mcp-servers/images/quick-start-mcp.png" alt="MCP 서버 연결을 나타내는 떠다니는 기술 아이콘들에 둘러싸여 밝은 전기 스파크와 함께 연결되는 전원 케이블" width="800"/>

# 퀵 스타트: 30초 만에 MCP 시작하기

## 내장된 GitHub MCP 서버로 시작하기
무엇을 구성하기 전에, 지금 바로 MCP가 동작하는 모습을 확인해 봅시다.
GitHub MCP 서버는 기본으로 포함되어 있습니다. 다음을 시도해 보십시오:

```bash
copilot
> List the recent commits in this repository
```

Copilot이 실제 커밋 데이터를 반환한다면, 방금 MCP가 실제로 동작하는 모습을 본 것입니다. 그것이 바로 GitHub MCP 서버가 여러분을 대신해 GitHub에 접근하는 모습입니다. 그러나 GitHub는 *하나의* 서버일 뿐입니다. 이 챕터에서는 더 많은 서버(파일 시스템 접근, 최신 문서 등)를 추가해 Copilot이 더 많은 일을 할 수 있게 만드는 방법을 보여드립니다.

---

## `/mcp show` 명령

`/mcp show`를 사용하면 어떤 MCP 서버가 구성되어 있고 활성화되어 있는지 확인할 수 있습니다:

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub 서버만 보입니까?** 정상입니다! 추가 MCP 서버를 아직 추가하지 않았다면 GitHub만 표시됩니다. 다음 섹션에서 더 추가해 보겠습니다.

> 📚 **모든 MCP 관리 명령을 보려면** 채팅 안에서 `/mcp` 슬래시 명령으로 또는 터미널에서 직접 `copilot mcp`로 서버를 관리할 수 있습니다. 이 챕터 끝에 있는 [전체 명령 레퍼런스](#-추가-mcp-명령)를 참고합니다.

<details>
<summary>🎬 직접 동작 확인하기!</summary>

![MCP Status Demo](../../../06-mcp-servers/images/mcp-status-demo.gif)

*데모 출력은 다를 수 있습니다. 사용하는 모델, 도구, 응답은 여기 표시된 것과 다를 수 있습니다.*

</details>

---

## MCP가 있으면 무엇이 달라집니까?

실제로 MCP가 만드는 차이는 다음과 같습니다:

**MCP 없이:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**MCP와 함께:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP는 Copilot이 여러분의 실제 개발 환경을 인식하도록 만들어 줍니다.

> 📚 **공식 문서**: GitHub Copilot에서 MCP가 어떻게 동작하는지 더 깊이 알아보려면 [About MCP](https://docs.github.com/copilot/concepts/context/mcp)를 참고하십시오.

---

# MCP 서버 구성하기

<img src="../../../06-mcp-servers/images/configuring-mcp-servers.png" alt="MCP 서버 구성을 나타내는 전문 오디오 믹싱 보드의 노브와 슬라이더를 조정하는 손" width="800"/>

이제 MCP가 동작하는 모습을 보았으니, 추가 서버를 설정해 봅시다. 서버를 추가하는 방법은 두 가지입니다: **내장 레지스트리에서 추가**(가장 쉬움 — CLI에서 가이드 설정)하거나 **구성 파일을 수동으로 편집**(더 유연함)하는 것입니다. 어떤 방법을 선택할지 모르겠다면 레지스트리 옵션부터 시작해 보십시오.

---

## 레지스트리에서 MCP 서버 설치하기

CLI에는 인기 있는 서버를 발견하고 가이드 설정으로 설치할 수 있는 내장 MCP 서버 레지스트리가 있습니다. JSON 편집이 필요 없습니다.

```bash
copilot

> /mcp search
```

Copilot이 사용 가능한 서버를 보여주는 인터랙티브 선택기를 엽니다. 하나를 선택하면 CLI가 필요한 구성(API 키, 경로 등)을 안내하고 자동으로 구성에 추가합니다.

> 💡 **레지스트리를 사용하는 이유?** 시작하기 가장 쉬운 방법입니다. npm 패키지 이름, 명령 인자, JSON 구조를 알 필요가 없습니다. CLI가 모두 처리해 줍니다.

---

## MCP 구성 파일

MCP 서버는 `~/.copilot/mcp-config.json`(사용자 수준, 모든 프로젝트에 적용) 또는 `.mcp.json`(프로젝트 수준, 프로젝트 루트에 위치)에서 구성됩니다. 위에서 `/mcp search`를 사용했다면 CLI가 이미 이 파일을 만들거나 업데이트했지만, 커스터마이징을 위해 형식을 이해해 두면 유용합니다.

> ⚠️ **참고**: `.vscode/mcp.json`은 더 이상 MCP 구성 소스로 지원되지 않습니다. 기존 `.vscode/mcp.json`이 있다면 프로젝트 루트의 `.mcp.json`으로 마이그레이션하십시오. CLI는 오래된 구성 파일을 감지하면 마이그레이션 힌트를 표시합니다.

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*대부분의 MCP 서버는 npm 패키지로 배포되며 `npx` 명령으로 실행됩니다.*

<details>
<summary>💡 <strong>JSON이 처음이십니까?</strong> 각 필드가 무엇을 의미하는지 보려면 클릭하십시오</summary>

| 필드 | 의미 |
|-------|---------------|
| `"mcpServers"` | 모든 MCP 서버 구성을 담는 컨테이너 |
| `"server-name"` | 직접 정하는 이름 (예: "github", "filesystem") |
| `"type": "local"` | 서버가 로컬 머신에서 실행됨 |
| `"command": "npx"` | 실행할 프로그램 (npx는 npm 패키지를 실행) |
| `"args": [...]` | 명령에 전달되는 인자 |
| `"tools": ["*"]` | 이 서버의 모든 도구 허용 |

**중요한 JSON 규칙:**
- 문자열에는 작은따옴표가 아닌 큰따옴표 `"`를 사용합니다
- 마지막 항목 뒤에 쉼표를 붙이지 않습니다
- 파일은 유효한 JSON이어야 합니다 (확신이 없다면 [JSON 검증기](https://jsonlint.com/)를 사용하십시오)

</details>

---

## MCP 서버 추가하기

GitHub MCP 서버는 내장되어 있어서 별도 설정이 필요 없습니다. 아래는 추가로 더할 수 있는 서버입니다. **관심 있는 것을 고르거나 순서대로 진행해 보십시오.**

| 하고 싶은 일... | 이동 |
|---|---|
| Copilot이 내 프로젝트 파일을 탐색하게 하기 | [Filesystem 서버](#filesystem-서버) |
| 최신 라이브러리 문서 가져오기 | [Context7 서버](#context7-서버-문서) |
| 선택적 추가 기능 살펴보기 (커스텀 서버, web_fetch) | [기본을 넘어서](#기본을-넘어서) |

<details>
<summary><strong>Filesystem 서버</strong> - Copilot이 프로젝트 파일을 탐색하게 하기</summary>
<a id="filesystem-server"></a>

### Filesystem 서버

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` 경로**: `.`은 "현재 디렉터리"를 의미합니다. Copilot은 실행한 위치를 기준으로 파일에 접근할 수 있습니다. Codespace에서는 작업 공간 루트입니다. 원한다면 `/workspaces/copilot-cli-for-beginners` 같은 절대 경로를 사용할 수도 있습니다.

이를 `~/.copilot/mcp-config.json`에 추가하고 Copilot을 재시작하십시오.

</details>

<details>
<summary><strong>Context7 서버</strong> - 최신 라이브러리 문서 가져오기</summary>
<a id="context7-server-documentation"></a>

### Context7 서버 (문서)

Context7은 Copilot에게 인기 있는 프레임워크와 라이브러리의 최신 문서에 대한 접근 권한을 제공합니다. 오래되었을 수 있는 학습 데이터에 의존하는 대신, Copilot이 실제 최신 문서를 가져옵니다.

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **API 키 불필요** 
- ✅ **계정 불필요** 
- ✅ **코드는 로컬에 유지됨**

이를 `~/.copilot/mcp-config.json`에 추가하고 Copilot을 재시작하십시오.

</details>

<details>
<summary><strong>기본을 넘어서</strong> - 커스텀 서버 및 웹 접근 (선택)</summary>
<a id="beyond-the-basics"></a>

위의 핵심 서버에 익숙해지면 시도해 볼 수 있는 선택적 추가 기능입니다.

### Microsoft Learn MCP 서버

지금까지 본 모든 MCP 서버(filesystem, Context7)는 로컬 머신에서 실행됩니다. 그러나 MCP 서버는 원격으로도 실행될 수 있습니다. 즉, Copilot CLI를 URL로 가리키기만 하면 나머지는 알아서 처리합니다. `npx`나 `python`이 필요 없고, 로컬 프로세스도 없으며, 설치할 종속성도 없습니다.

[Microsoft Learn MCP 서버](https://github.com/microsoftdocs/mcp)가 좋은 예시입니다. Copilot CLI가 공식 Microsoft 문서(Azure, Microsoft Foundry 및 기타 AI 주제, .NET, Microsoft 365 등)에 직접 접근하도록 해주어, 모델의 학습 데이터에 의존하는 대신 문서를 검색하고, 전체 페이지를 가져오고, 공식 코드 샘플을 찾을 수 있습니다.

- ✅ **API 키 불필요** 
- ✅ **계정 불필요** 
- ✅ **로컬 설치 불필요**

**`/plugin install`로 빠르게 설치:**

JSON 구성 파일을 수동으로 편집하는 대신 한 번의 명령으로 설치할 수 있습니다:

```bash
copilot

> /plugin install microsoftdocs/mcp
```

이렇게 하면 서버와 관련된 에이전트 스킬이 자동으로 추가됩니다. 설치되는 스킬은 다음과 같습니다:

- **microsoft-docs**: 개념, 튜토리얼, 사실 조회
- **microsoft-code-reference**: API 조회, 코드 샘플, 문제 해결
- **microsoft-skill-creator**: Microsoft 기술에 관한 커스텀 스킬을 생성하기 위한 메타 스킬

**사용법:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 자세한 내용: [Microsoft Learn MCP 서버 개요](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch`로 웹 접근하기

Copilot CLI에는 어떤 URL의 콘텐츠든 가져올 수 있는 내장 `web_fetch` 도구가 포함되어 있습니다. 터미널을 떠나지 않고도 README, API 문서, 릴리스 노트를 가져오는 데 유용합니다. MCP 서버가 필요 없습니다.

`~/.copilot/config.json`(일반 Copilot 설정)을 통해 어떤 URL에 접근할 수 있는지 제어할 수 있으며, 이는 `~/.copilot/mcp-config.json`(MCP 서버 정의)과는 별도입니다.

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**사용법:**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### 커스텀 MCP 서버 구축하기

Copilot을 자신의 API, 데이터베이스 또는 내부 도구에 연결하고 싶으십니까? Python으로 커스텀 MCP 서버를 구축할 수 있습니다. 사전 구축된 서버(GitHub, filesystem, Context7)가 대부분의 사용 사례를 다루므로 이는 완전히 선택 사항입니다.

📖 book app을 예시로 한 전체 워크스루는 [커스텀 MCP 서버 가이드](mcp-custom-server.md)를 참고하십시오.

📚 더 많은 배경 지식은 [MCP for Beginners 코스](https://github.com/microsoft/mcp-for-beginners)를 참고하십시오.

</details>

<a id="complete-configuration-file"></a>

### 전체 구성 파일

다음은 filesystem과 Context7 서버를 포함한 전체 `mcp-config.json`입니다:

> 💡 **참고:** GitHub MCP는 내장되어 있습니다. 구성 파일에 추가할 필요가 없습니다.

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

전역 접근을 위해 `~/.copilot/mcp-config.json`으로 저장하거나, 프로젝트별 구성을 위해 프로젝트 루트의 `.mcp.json`으로 저장하십시오.

---

# MCP 서버 사용하기

이제 MCP 서버를 구성했으니, 무엇을 할 수 있는지 살펴봅시다.

<img src="../../../06-mcp-servers/images/using-mcp-servers.png" alt="MCP 서버 사용하기 - 개발자 CLI가 GitHub, Filesystem, Context7, 커스텀/Web Fetch 서버에 연결된 허브 앤 스포크 다이어그램" width="800" />

---

## 서버 사용 예시

**탐색할 서버를 고르거나 순서대로 진행해 보십시오.**

| 시도해 보고 싶은 것... | 이동 |
|---|---|
| GitHub 저장소, 이슈, PR | [GitHub 서버](#github-서버-내장) |
| 프로젝트 파일 탐색 | [Filesystem 서버 사용](#filesystem-서버-1) |
| 라이브러리 문서 조회 | [Context7 서버 사용](#context7-서버) |
| 커스텀 서버, Microsoft Learn MCP 및 web_fetch 사용 | [기본을 넘어서 - 사용](#기본을-넘어서) |

<details>
<summary><strong>GitHub 서버 (내장)</strong> - 저장소, 이슈, PR 등에 접근</summary>
<a id="github-server-built-in"></a>

### GitHub 서버 (내장)

GitHub MCP 서버는 **내장되어 있습니다**. Copilot에 로그인했다면(초기 설정 중에 했을 것입니다), 이미 동작합니다. 구성이 필요 없습니다!

> 💡 **동작하지 않습니까?** `/login`을 실행하여 GitHub로 다시 인증하십시오.

<details>
<summary><strong>Dev Container에서의 인증</strong></summary>

- **GitHub Codespaces** (권장): 인증이 자동입니다. `gh` CLI가 Codespace 토큰을 상속받습니다. 별도의 작업이 필요 없습니다.
- **로컬 dev container (Docker)**: 컨테이너가 시작된 후 `gh auth login`을 실행한 다음 Copilot을 재시작하십시오.

**인증 문제 해결:**
```bash
# 인증되어 있는지 확인합니다
gh auth status

# 인증되어 있지 않다면 로그인합니다
gh auth login

# GitHub MCP가 연결되어 있는지 확인합니다
copilot
> /mcp show
```

</details>

| 기능 | 예시 |
|---------|----------|
| **저장소 정보** | 커밋, 브랜치, 기여자 보기 |
| **이슈** | 이슈 나열, 생성, 검색, 댓글 작성 |
| **풀 리퀘스트** | PR 보기, diff 확인, PR 생성, 상태 확인 |
| **코드 검색** | 저장소 전반에서 코드 검색 |
| **Actions** | 워크플로 실행 및 상태 조회 |

```bash
copilot

# 이 저장소의 최근 활동을 확인합니다
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# 저장소 구조를 탐색합니다
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# 저장소 전체에서 코드 패턴을 검색합니다
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **자신의 포크에서 작업 중이십니까?** 이 코스 저장소를 포크했다면 이슈와 풀 리퀘스트를 만드는 것 같은 쓰기 작업도 시도해 볼 수 있습니다. 아래 연습에서 함께 실습해 봅니다.

> ⚠️ **결과가 보이지 않습니까?** GitHub MCP는 로컬 파일이 아니라 저장소의 원격(github.com)을 대상으로 동작합니다. 저장소에 원격이 있는지 확인하십시오: `git remote -v`로 확인할 수 있습니다.

</details>

<details>
<summary><strong>Filesystem 서버</strong> - 프로젝트 파일 탐색 및 분석</summary>
<a id="filesystem-server-usage"></a>

### Filesystem 서버

구성이 완료되면 filesystem MCP는 Copilot이 자동으로 사용할 수 있는 도구를 제공합니다:

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7 서버</strong> - 라이브러리 문서 조회</summary>
<a id="context7-server-usage"></a>

### Context7 서버

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture는 인수로 자동 전달됩니다
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# 이제 Copilot은 공식 pytest 패턴을 알고 있습니다
# 그리고 이를 samples/book-app-project/tests/test_books.py에 적용할 수 있습니다
```

</details>

<details>
<summary><strong>기본을 넘어서</strong> - 커스텀 서버 및 web_fetch 사용</summary>
<a id="beyond-the-basics-usage"></a>

### 기본을 넘어서

**커스텀 MCP 서버**: [커스텀 MCP 서버 가이드](mcp-custom-server.md)를 보고 book-lookup 서버를 구축했다면, 책 컬렉션을 직접 조회할 수 있습니다:

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**: [Microsoft Learn MCP 서버](#microsoft-learn-mcp-서버)를 설치했다면 공식 Microsoft 문서를 직접 조회할 수 있습니다:

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**: 내장 `web_fetch` 도구를 사용하여 어떤 URL에서든 콘텐츠를 가져올 수 있습니다:

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## 다중 서버 워크플로

이 워크플로들은 개발자들이 "이제는 이거 없이는 일하고 싶지 않아"라고 말하는 이유를 보여줍니다. 각 예시는 단일 세션에서 여러 MCP 서버를 결합합니다.

<img src="../../../06-mcp-servers/images/issue-to-pr-workflow.png" alt="MCP를 사용한 이슈에서 PR까지 워크플로 - GitHub 이슈를 받는 것부터 풀 리퀘스트를 만드는 것까지의 전체 흐름을 보여줌" width="800"/>

*완전한 MCP 워크플로: GitHub MCP가 저장소 데이터를 가져오고, Filesystem MCP가 코드를 찾고, Context7 MCP가 모범 사례를 제공하며, Copilot이 분석을 처리합니다*

아래 각 예시는 독립적입니다. **관심 있는 것을 골라 보거나 모두 읽어 보십시오.**

| 보고 싶은 것... | 이동 |
|---|---|
| 여러 서버가 함께 동작하는 모습 | [다중 서버 탐색](#여러-mcp-서버로-book-app-탐색하기) |
| 한 세션에서 이슈에서 PR까지 진행 | [이슈에서 PR로 워크플로](#이슈에서-pr로-워크플로-자신의-저장소에서) |
| 빠른 프로젝트 상태 점검 | [상태 대시보드](#book-app-상태-대시보드) |

<details>
<summary><strong>다중 서버 탐색</strong> - 한 세션에서 filesystem, GitHub, Context7 결합</summary>
<a id="multi-server-exploration"></a>

#### 여러 MCP 서버로 Book App 탐색하기

```bash
copilot

# 1단계: filesystem MCP를 사용하여 book app을 탐색합니다
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# 2단계: GitHub MCP를 사용하여 최근 변경 사항을 확인합니다
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# 3단계: Context7 MCP를 사용하여 모범 사례를 확인합니다
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# 4단계: 권장 사항을 종합합니다
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 MCP 워크플로가 동작하는 모습 보기!</summary>

![MCP Workflow Demo](../../../06-mcp-servers/images/mcp-workflow-demo.gif)

*데모 출력은 다를 수 있습니다. 사용하는 모델, 도구, 응답은 여기 표시된 것과 다를 수 있습니다.*

</details>

**결과**: 코드 탐색 → 이력 검토 → 모범 사례 조회 → 개선 계획. **모두 하나의 터미널 세션에서, 세 개의 MCP 서버를 함께 사용합니다.**

</details>

<details>
<summary><strong>이슈에서 PR로 워크플로</strong> - 터미널을 떠나지 않고 GitHub 이슈에서 풀 리퀘스트까지 진행</summary>
<a id="issue-to-pr-workflow"></a>

#### 이슈에서 PR로 워크플로 (자신의 저장소에서)

쓰기 권한이 있는 자신의 포크나 저장소에서 가장 잘 동작합니다:

> 💡 **지금 시도해 볼 수 없어도 걱정하지 마세요.** 읽기 전용 클론에 있다면 과제에서 연습하게 됩니다. 지금은 흐름을 이해하기 위해 그냥 읽어 보십시오.

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**복사-붙여넣기 없음. 컨텍스트 전환 없음. 하나의 터미널 세션.**

</details>

<details>
<summary><strong>상태 대시보드</strong> - 여러 서버를 사용한 빠른 프로젝트 상태 점검</summary>
<a id="health-dashboard"></a>

#### Book App 상태 대시보드

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**결과**: 여러 데이터 소스를 몇 초 만에 집계합니다. 수동으로 한다면 grep을 실행하고, 줄을 세고, git log를 확인하고, 테스트 파일을 둘러봐야 합니다. 쉽게 15분 이상의 작업이 됩니다.

</details>

---

# 실습

<img src="../../../images/practice.png" alt="코드를 표시하는 모니터, 램프, 커피 컵, 헤드폰이 놓인 따뜻한 데스크 환경에서 실습 준비 완료" width="800"/>

**🎉 이제 핵심을 모두 이해하셨습니다!** MCP를 이해했고, 서버 구성 방법을 보았으며, 실제 워크플로가 동작하는 모습을 확인했습니다. 이제 직접 시도해 볼 시간입니다.

---

## ▶️ 직접 해보기

이제 여러분 차례입니다! 다음 연습을 완료하여 book app 프로젝트에서 MCP 서버를 사용하는 방법을 연습해 보십시오.

### 연습 1: MCP 상태 확인하기

먼저 어떤 MCP 서버가 사용 가능한지 확인해 봅시다:

```bash
copilot

> /mcp show
```

GitHub 서버가 활성화된 상태로 표시되어야 합니다. 그렇지 않다면 `/login`을 실행하여 인증하십시오.

---

### 연습 2: Filesystem MCP로 Book App 탐색하기

filesystem 서버를 구성했다면 이를 사용해 book app을 탐색해 보십시오:

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**기대 결과**: Copilot이 `book_app.py`, `books.py`, `utils.py`와 그 함수들을 나열합니다.

> 💡 **filesystem MCP를 아직 구성하지 않으셨습니까?** 위 [전체 구성](#전체-구성-파일) 섹션에서 구성 파일을 만드세요. 그런 다음 Copilot을 재시작하십시오.

---

### 연습 3: GitHub MCP로 저장소 이력 조회하기

내장 GitHub MCP를 사용하여 이 코스 저장소를 탐색해 보십시오:

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**기대 결과**: Copilot이 GitHub 원격에서 최근 커밋 메시지와 브랜치 이름을 보여줍니다.

> ⚠️ **Codespace에 있습니까?** 자동으로 동작합니다. 인증이 상속됩니다. 로컬 클론에서는 `gh auth status`로 로그인되어 있는지 확인하십시오.

---

### 연습 4: 여러 MCP 서버 결합하기

이제 단일 세션에서 filesystem과 GitHub MCP를 결합해 보십시오:

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**기대 결과**: Copilot이 JSON 파일을 읽고(filesystem MCP) "The Hobbit", "1984", "Dune", "To Kill a Mockingbird", "Mysterious Book" 등 5권의 책을 나열한 다음, GitHub에서 커밋 이력을 조회합니다.

**자가 점검**: 왜 "내 저장소의 커밋 이력 확인"이 수동으로 `git log`를 실행하고 그 출력을 프롬프트에 붙여넣는 것보다 나은지 설명할 수 있다면 MCP를 이해한 것입니다.

---

## 📝 과제

### 메인 챌린지: Book App MCP 탐색

book app 프로젝트에서 MCP 서버를 함께 사용하는 연습을 합니다. 단일 Copilot 세션에서 다음 단계를 완료하십시오:

1. **MCP 동작 확인**: `/mcp show`를 실행하고 최소한 GitHub 서버가 활성화되어 있는지 확인하십시오
2. **filesystem MCP 설정**(아직 안 했다면): filesystem 서버 구성으로 `~/.copilot/mcp-config.json`을 만드세요
3. **코드 탐색**: Copilot에게 filesystem 서버를 사용하도록 요청하십시오:
   - `samples/book-app-project/books.py`의 모든 함수 나열
   - `samples/book-app-project/utils.py`에서 타입 힌트가 없는 함수 확인
   - `samples/book-app-project/data.json`을 읽고 데이터 품질 문제 식별 (힌트: 마지막 항목을 보십시오)
4. **저장소 활동 확인**: Copilot에게 GitHub MCP를 사용하도록 요청하십시오:
   - `samples/book-app-project/`의 파일을 변경한 최근 커밋 나열
   - 열린 이슈나 풀 리퀘스트가 있는지 확인
5. **서버 결합**: 단일 프롬프트에서 Copilot에게 다음을 요청하십시오:
   - `samples/book-app-project/tests/test_books.py`의 테스트 파일 읽기
   - 테스트된 함수와 `books.py`의 모든 함수 비교
   - 누락된 테스트 커버리지 요약

**성공 기준**: 단일 Copilot 세션에서 filesystem과 GitHub MCP 데이터를 자연스럽게 결합할 수 있고, 각 MCP 서버가 응답에 무엇을 기여했는지 설명할 수 있습니다.

<details>
<summary>💡 힌트 (펼치려면 클릭)</summary>

**1단계: MCP 확인**
```bash
copilot
> /mcp show
# "github"가 활성화된 것으로 표시되어야 합니다
# 그렇지 않으면 실행합니다: /login
```

**2단계: 구성 파일 만들기**

위 [전체 구성](#전체-구성-파일) 섹션의 JSON을 사용하여 `~/.copilot/mcp-config.json`으로 저장하십시오.

**3단계: 찾아야 할 데이터 품질 문제**

`data.json`의 마지막 책은 다음과 같습니다:
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
저자는 비어 있고 연도가 0입니다. 그것이 데이터 품질 문제입니다!

**5단계: 테스트 커버리지 비교**

`test_books.py`의 테스트는 다음을 다룹니다: `add_book`, `mark_as_read`, `remove_book`, `get_unread_books`, `find_book_by_title`. `load_books`, `save_books`, `list_books` 같은 함수는 직접적인 테스트가 없습니다. `book_app.py`의 CLI 함수와 `utils.py`의 헬퍼는 전혀 테스트가 없습니다.

**MCP가 동작하지 않는다면:** 구성 파일을 편집한 후 Copilot을 재시작하십시오.

</details>

### 보너스 챌린지: 커스텀 MCP 서버 구축하기

더 깊이 들어갈 준비가 되셨습니까? [커스텀 MCP 서버 가이드](mcp-custom-server.md)를 따라 어떤 API에든 연결되는 자신만의 MCP 서버를 Python으로 구축해 보십시오.

---

<details>
<summary>🔧 <strong>흔한 실수 및 문제 해결</strong> (펼치려면 클릭)</summary>

### 흔한 실수

| 실수 | 결과 | 해결 |
|---------|--------------|-----|
| GitHub MCP가 내장임을 모름 | 수동으로 설치/구성하려 함 | GitHub MCP는 기본 포함입니다. 그냥 시도해 보십시오: "List the recent commits in this repo" |
| 잘못된 위치에서 구성 파일을 찾음 | MCP 설정을 찾거나 편집할 수 없음 | 사용자 수준 구성은 `~/.copilot/mcp-config.json`에, 프로젝트 수준은 프로젝트 루트의 `.mcp.json`에 있습니다 |
| 구성 파일의 잘못된 JSON | MCP 서버 로드 실패 | `/mcp show`로 구성을 확인하십시오. JSON 구문을 검증하십시오 |
| MCP 서버 인증을 잊음 | "Authentication failed" 오류 | 일부 MCP는 별도 인증이 필요합니다. 각 서버의 요구사항을 확인하십시오 |

### 문제 해결

**"MCP server not found"** - 다음을 확인하십시오:
1. npm 패키지가 존재하는지: `npm view @modelcontextprotocol/server-github`
2. 구성이 유효한 JSON인지
3. 서버 이름이 구성과 일치하는지

`/mcp show`로 현재 구성을 확인하십시오.

**"GitHub authentication failed"** - 내장 GitHub MCP는 `/login` 자격 증명을 사용합니다. 시도해 보십시오:

```bash
copilot
> /login
```

이는 GitHub로 다시 인증합니다. 문제가 지속되면 GitHub 계정이 접근하려는 저장소에 필요한 권한이 있는지 확인하십시오.

**"MCP server failed to start"** - 서버 로그를 확인하십시오:
```bash
# 오류를 확인하려면 서버 명령을 수동으로 실행합니다
npx -y @modelcontextprotocol/server-github
```

**MCP 도구가 사용 불가** - 서버가 활성화되어 있는지 확인하십시오:
```bash
copilot

> /mcp show
# 서버가 목록에 있고 활성화되어 있는지 확인합니다
```

서버가 비활성화된 경우 다시 활성화하는 방법은 아래의 [추가 `/mcp` 명령](#-추가-mcp-명령)을 참고하십시오.

</details>

---

<details>
<summary>📚 <strong>추가 MCP 명령</strong> (펼치려면 클릭)</summary>
<a id="-추가-mcp-명령"></a>

MCP 서버는 두 가지 방법으로 관리할 수 있습니다: **채팅 세션 내에서 슬래시 명령** 사용, 또는 터미널에서 직접 **`copilot mcp` 명령** 사용(채팅 세션 필요 없음).

### 옵션 1: 슬래시 명령 (채팅 세션 내에서)

이미 `copilot` 안에 있을 때 사용합니다:

| 명령 | 동작 |
|---------|--------------|
| `/mcp show` | 구성된 모든 MCP 서버와 상태 표시 |
| `/mcp add` | 새 서버 추가를 위한 인터랙티브 설정 |
| `/mcp edit <server-name>` | 기존 서버 구성 편집 |
| `/mcp enable <server-name>` | 비활성화된 서버 활성화 (세션 간 유지) |
| `/mcp disable <server-name>` | 서버 비활성화 (세션 간 유지) |
| `/mcp delete <server-name>` | 서버 영구 제거 |
| `/mcp auth <server-name>` | OAuth를 사용하는 MCP 서버로 다시 인증 (예: 계정 전환 후) |

### 옵션 2: `copilot mcp` 명령 (터미널에서)

채팅 세션을 먼저 시작하지 않고도 터미널에서 직접 MCP 서버를 관리할 수 있습니다:

```bash
# 구성된 모든 MCP 서버를 나열합니다
copilot mcp list

# 서버를 활성화합니다
copilot mcp enable filesystem

# 서버를 비활성화합니다
copilot mcp disable context7
```

> 💡 **언제 어느 것을 사용해야 합니까?** 이미 채팅 세션에 있을 때는 `/mcp` 슬래시 명령을 사용하십시오. 세션을 시작하기 전에 서버 설정을 빠르게 확인하거나 변경하고 싶을 때는 터미널에서 `copilot mcp`를 사용하십시오.

이 코스의 대부분에서 필요한 것은 `/mcp show`뿐입니다. 다른 명령들은 시간이 지나면서 더 많은 서버를 관리하게 될 때 유용해집니다.

</details>

---

# 요약

## 🔑 핵심 정리

1. **MCP**는 Copilot을 외부 서비스(GitHub, 파일 시스템, 문서)에 연결합니다
2. **GitHub MCP는 내장되어 있습니다** - 구성이 필요 없으며, `/login`만 하면 됩니다
3. **Filesystem과 Context7**은 `~/.copilot/mcp-config.json`을 통해 구성됩니다
4. **다중 서버 워크플로**는 단일 세션에서 여러 소스의 데이터를 결합합니다
5. **두 가지 방법으로 서버 관리**: 채팅 안에서 `/mcp` 슬래시 명령을 사용하거나, 터미널에서 `copilot mcp`를 사용하십시오
6. **커스텀 서버**는 어떤 API에든 연결할 수 있게 해줍니다 (선택, 부록 가이드에서 다룸)

> 📋 **빠른 참조**: 명령과 단축키의 전체 목록은 [GitHub Copilot CLI 명령 레퍼런스](https://docs.github.com/en/copilot/reference/cli-command-reference)를 참고하십시오.

---

## ➡️ 다음 단계

이제 모든 구성 요소를 갖추셨습니다: 모드, 컨텍스트, 워크플로, 에이전트, 스킬, MCP. 이제 모두 합쳐 볼 시간입니다.

[**챕터 07: 모두 합치기**](../07-putting-it-together/README.md)에서는 다음을 배웁니다:

- 통합된 워크플로에서 에이전트, 스킬, MCP 결합하기
- 아이디어부터 병합된 PR까지 완전한 기능 개발
- 훅을 통한 자동화
- 팀 환경을 위한 모범 사례

---

[**← 챕터 05로 돌아가기**](../05-skills/README.md) | [**챕터 07로 계속 →**](../07-putting-it-together/README.md)
