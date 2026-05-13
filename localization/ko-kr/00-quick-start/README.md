![챕터 00: 빠른 시작](../../../00-quick-start/images/chapter-header.png)

환영합니다! 이 챕터에서는 GitHub Copilot CLI(Command Line Interface)를 설치하고 GitHub 계정으로 로그인한 다음, 모든 것이 제대로 작동하는지 확인합니다. 빠른 설정 챕터이니 집중해 주세요. 설정이 완료되면 챕터 01에서 본격적인 데모가 시작됩니다!

## 🎯 학습 목표

이 챕터를 마치면:

- GitHub Copilot CLI가 설치됩니다
- GitHub 계정으로 로그인이 완료됩니다
- 간단한 테스트로 동작이 확인됩니다

> ⏱️ **예상 시간**: 약 10분 (읽기 5분 + 실습 5분)

---

## ✅ 사전 요건

- Copilot 액세스가 있는 **GitHub 계정**. [구독 옵션 보기](https://github.com/features/copilot/plans). 학생/교사는 [GitHub Education을 통해 무료로](https://education.github.com/pack) Copilot Pro를 이용할 수 있습니다.
- **터미널 기초**: `cd`, `ls` 같은 명령어에 익숙한 분

### "Copilot 액세스"란?

GitHub Copilot CLI를 사용하려면 활성화된 Copilot 구독이 필요합니다. [github.com/settings/copilot](https://github.com/settings/copilot)에서 현재 상태를 확인하세요. 다음 중 하나가 표시되어야 합니다:

- **Copilot Individual** - 개인 구독
- **Copilot Business** - 조직을 통한 구독
- **Copilot Enterprise** - 엔터프라이즈를 통한 구독
- **GitHub Education** - 인증된 학생/교사 무료 이용

"You don't have access to GitHub Copilot"이 표시된다면 무료 옵션을 사용하거나, 플랜을 구독하거나, 액세스를 제공하는 조직에 참여해야 합니다.

---

## 설치

> ⏱️ **시간 예상**: 설치는 2~5분이 걸립니다. 인증에는 1~2분이 추가됩니다.

### GitHub Codespaces (설정 없이 바로 시작)

사전 요건을 설치하고 싶지 않다면 GitHub Codespaces를 사용할 수 있습니다. GitHub Copilot CLI가 바로 사용 가능하며(로그인 필요), Python과 pytest도 미리 설치되어 있습니다.

1. 이 저장소를 GitHub 계정으로 [포크합니다](https://github.com/github/copilot-cli-for-beginners/fork)
2. **Code** > **Codespaces** > **Create codespace on main** 선택
3. 컨테이너가 빌드될 때까지 몇 분 기다립니다
4. 준비 완료! 터미널이 Codespace 환경에서 자동으로 열립니다.

> 💡 **Codespace에서 확인**: `cd samples/book-app-project && python book_app.py help`를 실행하여 Python과 샘플 앱이 작동하는지 확인하세요.

### 로컬 설치

로컬 머신에서 강의 샘플과 함께 Copilot CLI를 실행하려면 아래 단계를 따르세요.

1. 저장소를 클론하여 강의 샘플을 가져옵니다:

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 다음 옵션 중 하나를 사용하여 Copilot CLI를 설치합니다.

    > 💡 **어떤 방법을 선택할지 모르겠다면?** Node.js가 설치되어 있다면 `npm`을 사용하세요. 그렇지 않다면 시스템에 맞는 옵션을 선택하세요.

    ### 모든 플랫폼 (npm)

    ```bash
    # Node.js가 설치되어 있다면 빠르게 CLI를 가져오는 방법입니다
    npm install -g @github/copilot
    ```

    ### macOS/Linux (Homebrew)

    ```bash
    brew install copilot-cli
    ```

    ### Windows (WinGet)

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux (설치 스크립트)

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>선택 사항: 쉘 탭 완성 활성화</summary>

쉘 탭 완성을 사용하면 **Tab** 키를 눌러 `copilot` 서브커맨드, 옵션, 일부 옵션 값을 자동 완성할 수 있습니다. 선택 사항이지만 CLI에 익숙해지면 유용합니다.

Copilot CLI는 현재 Bash, Zsh, Fish의 완성 스크립트를 지원합니다:

```shell
# Bash, 현재 세션만
source <(copilot completion bash)

# Bash, Linux에서 영구 설정
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

영구 완성을 추가한 후 쉘을 재시작하세요. Windows에서 PowerShell로 Copilot CLI를 실행할 수 있지만, `copilot completion`은 현재 Bash, Zsh, Fish만 지원합니다.

</details>

---

## 인증

`copilot-cli-for-beginners` 저장소 루트에서 터미널을 열고 CLI를 시작하여 폴더 접근을 허용합니다.

```bash
copilot
```

저장소가 들어 있는 폴더를 신뢰할지 묻는 메시지가 표시됩니다(아직 신뢰하지 않은 경우). 한 번만 신뢰하거나 앞으로의 모든 세션에서 신뢰하도록 선택할 수 있습니다.

<img src="../../../00-quick-start/images/copilot-trust.png" alt="Copilot CLI로 폴더의 파일 신뢰하기" width="800"/>

폴더를 신뢰한 후 GitHub 계정으로 로그인할 수 있습니다.

```
> /login
```

**이후 진행 과정:**

1. Copilot CLI에 일회용 코드(예: `ABCD-1234`)가 표시됩니다
2. 브라우저가 GitHub 기기 인증 페이지로 열립니다. 아직 로그인하지 않았다면 GitHub에 로그인하세요.
3. 표시된 코드를 입력합니다
4. "Authorize"를 선택하여 GitHub Copilot CLI 액세스를 허가합니다
5. 터미널로 돌아옵니다 - 이제 로그인이 완료됩니다!

<img src="../../../00-quick-start/images/auth-device-flow.png" alt="기기 인증 플로우 - 터미널 로그인에서 로그인 완료까지 5단계 과정" width="800"/>

*기기 인증 플로우: 터미널에서 코드를 생성하고, 브라우저에서 확인하면 Copilot CLI 인증이 완료됩니다.*

**팁**: 로그인은 세션 간에 유지됩니다. 토큰이 만료되거나 명시적으로 로그아웃하지 않는 한 한 번만 하면 됩니다.

---

## 동작 확인

### 1단계: Copilot CLI 테스트

로그인이 완료되었으면 Copilot CLI가 올바르게 작동하는지 확인해 봅시다. 아직 CLI를 시작하지 않았다면 터미널에서 시작하세요:

```bash
> Say hello and tell me what you can help with
```

응답을 받은 후 CLI를 종료할 수 있습니다:

```bash
> /exit
```

---

<details>
<summary>🎬 실제 동작 보기!</summary>

![Hello Demo](../../../00-quick-start/images/hello-demo.gif)

*데모 출력은 다를 수 있습니다. 모델, 도구, 응답은 여기 표시된 것과 다를 수 있습니다.*

</details>

---

**예상 출력**: Copilot CLI의 기능을 나열하는 친절한 응답.

### 2단계: 샘플 도서 앱 실행

강의에는 CLI를 사용하여 전체 강의 과정에서 탐색하고 개선할 샘플 앱이 제공됩니다 *(코드는 /samples/book-app-project에서 확인할 수 있습니다)*. 시작 전에 *Python 도서 컬렉션 터미널 앱*이 올바르게 작동하는지 확인하세요. 시스템에 따라 `python` 또는 `python3`을 실행합니다.

> **참고:** 강의 전반에 걸쳐 Python(`samples/book-app-project`)을 기반으로 주요 예제를 보여 주므로, 로컬 설치를 선택한 경우 [Python 3.10+](https://www.python.org/downloads/)가 있어야 합니다(Codespace에는 이미 설치되어 있습니다). 원하는 언어가 다르다면 JavaScript(`samples/book-app-project-js`) 및 C#(`samples/book-app-project-cs`) 버전도 제공됩니다. 각 샘플에는 해당 언어로 앱을 실행하는 방법이 담긴 README가 있습니다.

```bash
cd samples/book-app-project
python book_app.py list
```

**예상 출력**: "The Hobbit", "1984", "Dune" 등 5권의 도서 목록.

### 3단계: 도서 앱으로 Copilot CLI 사용해 보기

2단계를 실행했다면 먼저 저장소 루트로 돌아오세요:

```bash
cd ../..   # 필요한 경우 저장소 루트로 돌아오기
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**예상 출력**: 도서 앱의 주요 기능과 명령어 요약.

오류가 발생하면 아래 [문제 해결 섹션](#troubleshooting)을 확인하세요.

완료되면 Copilot CLI를 종료할 수 있습니다:

```bash
> /exit
```

---

## ✅ 준비 완료!

설치가 끝났습니다. 챕터 01에서 본격적인 내용이 시작됩니다:

- AI가 도서 앱을 검토하며 코드 품질 문제를 즉시 발견하는 과정 확인
- Copilot CLI를 사용하는 세 가지 방식 학습
- 일반 영어 설명으로 동작하는 코드 생성

[**챕터 01로 계속: 첫걸음 →**](../01-setup-and-first-steps/README.md)

---

## 문제 해결

### "copilot: command not found"

CLI가 설치되지 않았습니다. 다른 설치 방법을 시도해 보세요:

```bash
# brew가 실패했다면 npm을 시도하세요:
npm install -g @github/copilot

# 또는 설치 스크립트:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. [github.com/settings/copilot](https://github.com/settings/copilot)에서 Copilot 구독을 확인하세요
2. 회사 계정을 사용 중이라면 조직에서 CLI 액세스를 허용하는지 확인하세요

### "Authentication failed"

다시 인증하세요:

```bash
copilot
> /login
```

### 브라우저가 자동으로 열리지 않는 경우

[github.com/login/device](https://github.com/login/device)를 수동으로 방문하고 터미널에 표시된 코드를 입력하세요.

### 토큰이 만료된 경우

`/login`을 다시 실행하면 됩니다:

```bash
copilot
> /login
```

### 여전히 막혔나요?

- [GitHub Copilot CLI 공식 문서](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)를 확인하세요
- [GitHub Issues](https://github.com/github/copilot-cli/issues)에서 검색해 보세요

---

## 🔑 핵심 요점

1. **GitHub Codespace는 빠르게 시작하는 방법입니다** - Python, pytest, GitHub Copilot CLI가 모두 미리 설치되어 바로 데모를 시작할 수 있습니다
2. **다양한 설치 방법** - 시스템에 맞는 방법을 선택하세요 (Homebrew, WinGet, npm, 또는 설치 스크립트)
3. **일회성 인증** - 토큰이 만료될 때까지 로그인이 유지됩니다
4. **도서 앱이 작동합니다** - 전체 강의 과정에서 `samples/book-app-project`를 사용합니다

> 📚 **공식 문서**: 설치 옵션 및 요구 사항은 [Copilot CLI 설치](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)를 참조하세요.

> 📋 **빠른 참조**: 전체 명령어 및 단축키 목록은 [GitHub Copilot CLI 명령어 참조](https://docs.github.com/en/copilot/reference/cli-command-reference)를 확인하세요.

---

[**챕터 01로 계속: 첫걸음 →**](../01-setup-and-first-steps/README.md)
