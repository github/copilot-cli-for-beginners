![GitHub Copilot CLI for Beginners](../../images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [학습 목표](#-학습-목표) &ensp; ✅ [사전 요건](#-사전-요건) &ensp; 🤖 [Copilot 제품군](#-github-copilot-제품군-이해하기) &ensp; 📚 [강의 구성](#-강의-구성) &ensp; 📋 [명령어 참조](#-github-copilot-cli-명령어-참조) &ensp; 🌐 [내 언어](#-선호하는-언어로-보기)

# GitHub Copilot CLI for Beginners

> **✨ AI 기반 커맨드라인 어시스턴트로 개발 워크플로우를 강화하는 방법을 배워 보세요.**

GitHub Copilot CLI는 AI 어시스턴트를 터미널로 직접 가져옵니다. 브라우저나 코드 에디터로 전환하지 않고도, 커맨드라인을 떠나지 않고 질문하고, 완전한 기능의 애플리케이션을 생성하고, 코드를 검토하고, 테스트를 생성하고, 문제를 디버그할 수 있습니다.

24시간 7일 내내 코드를 읽고, 혼란스러운 패턴을 설명하고, 더 빠르게 작업할 수 있도록 도와주는 지식이 풍부한 동료가 항상 곁에 있는 것과 같습니다!

> 📘 **웹 환경을 선호하시나요?** 이 강의를 GitHub에서 바로 따라가거나, [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/)에서 더 일반적인 브라우징 환경으로 볼 수 있습니다.

이 강의는 다음 분들을 대상으로 합니다:

- **커맨드라인에서 AI를 활용하려는 소프트웨어 개발자**
- **IDE 통합보다 키보드 중심 워크플로우를 선호하는 터미널 사용자**
- **AI 기반 코드 리뷰 및 개발 관행을 표준화하려는 팀**

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="../../images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - 이벤트 찾기 또는 개최하기" width="100%" />
  </picture>
</a>

## 🎯 학습 목표

이 실습 강의는 GitHub Copilot CLI를 처음부터 생산적으로 사용할 수 있게 안내합니다. 모든 챕터에 걸쳐 하나의 Python 도서 컬렉션 앱을 사용하며, AI 지원 워크플로우를 활용해 점진적으로 개선해 나갑니다. 강의를 마치면 터미널에서 AI를 자신 있게 사용하여 코드를 검토하고, 테스트를 생성하고, 문제를 디버그하고, 워크플로우를 자동화할 수 있게 됩니다.

**AI 경험이 전혀 없어도 됩니다.** 터미널을 사용할 수 있다면 누구나 배울 수 있습니다.

**이런 분께 적합합니다:** 개발자, 학생, 소프트웨어 개발 경험이 있는 모든 분.

## ✅ 사전 요건

시작 전에 다음을 준비해 주세요:

- **GitHub 계정**: [무료로 만들기](https://github.com/signup)<br>
- **GitHub Copilot 액세스**: [무료 플랜](https://github.com/features/copilot/plans), [월간 구독](https://github.com/features/copilot/plans), 또는 [학생/교사 무료 사용](https://education.github.com/pack)<br>
- **터미널 기초**: `cd`, `ls`, 명령어 실행에 익숙한 분

## 🤖 GitHub Copilot 제품군 이해하기

GitHub Copilot은 AI 기반 도구의 제품군으로 발전했습니다. 각 제품이 어디에서 동작하는지 알아보세요:

| 제품 | 실행 환경 | 설명 |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>(이 강의) | 터미널 |  터미널 네이티브 AI 코딩 어시스턴트  |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code, Visual Studio, JetBrains 등 | 에이전트 모드, 채팅, 인라인 제안  |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | 저장소에 대한 몰입형 채팅, 에이전트 생성 등 |
| [**GitHub Copilot 클라우드 에이전트**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub  | 에이전트에게 이슈를 할당하면 PR을 받아볼 수 있습니다 |

이 강의는 **GitHub Copilot CLI**에 집중하여, AI 어시스턴트를 터미널로 직접 가져옵니다.

## 📚 강의 구성

![GitHub Copilot CLI 학습 경로](../../images/learning-path.png)

| 챕터 | 제목 | 학습 내용 |
|:-------:|-------|-------------------|
| 00 | 🚀 [빠른 시작](./00-quick-start/README.md) | 설치 및 확인 |
| 01 | 👋 [첫걸음](./01-setup-and-first-steps/README.md) | 라이브 데모 + 세 가지 상호작용 모드 |
| 02 | 🔍 [컨텍스트와 대화](./02-context-conversations/README.md) | 멀티 파일 프로젝트 분석 |
| 03 | ⚡ [개발 워크플로우](./03-development-workflows/README.md) | 코드 리뷰, 디버그, 테스트 생성 |
| 04 | 🤖 [특화된 AI 어시스턴트 만들기](./04-agents-custom-instructions/README.md) | 워크플로우에 맞는 커스텀 에이전트 |
| 05 | 🛠️ [반복 작업 자동화](./05-skills/README.md) | 자동으로 로드되는 스킬 |
| 06 | 🔌 [GitHub, 데이터베이스 & API 연결](./06-mcp-servers/README.md) | MCP 서버 통합 |
| 07 | 🎯 [모든 것을 합쳐서](./07-putting-it-together/README.md) | 완전한 기능 워크플로우 |

## 📖 강의 진행 방식

각 챕터는 동일한 패턴을 따릅니다:

1. **실생활 비유**: 친숙한 비교를 통해 개념 이해
2. **핵심 개념**: 필수 지식 학습
3. **실습 예제**: 실제 명령어 실행 및 결과 확인
4. **과제**: 배운 내용 실습
5. **다음 단계**: 다음 챕터 미리 보기

**코드 예제는 직접 실행할 수 있습니다.** 이 강의의 모든 copilot 텍스트 블록은 터미널에서 복사하여 실행할 수 있습니다.

## 📋 GitHub Copilot CLI 명령어 참조

[**GitHub Copilot CLI 명령어 참조**](https://docs.github.com/en/copilot/reference/cli-command-reference)에서 Copilot CLI를 효과적으로 사용하는 데 도움이 되는 명령어와 키보드 단축키를 찾아볼 수 있습니다.

## 🌐 선호하는 언어로 보기

이 자료는 다음 언어로 제공됩니다.

[English](../../README.md) | [Español](../es/README.md) | [日本語](../ja/README.md) | [한국어](./README.md) | [Português](../pt-br/README.md) | [中文(简体)](../zh-cn/README.md)

## 🙋 도움 받기

- 🐛 **버그를 발견하셨나요?** [이슈 열기](https://github.com/github/copilot-cli-for-beginners/issues)
- 📚 **공식 문서:** [GitHub Copilot CLI 문서](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## 기여하기

> **참고**: 강의에 사용된 코드는 리뷰, 설명, 디버깅 중 특정 유형의 출력을 생성하도록 설계되었으므로, 기존 코드를 변경하는 PR은 수락할 수 없습니다.

**기여 방법:**

1. 이 저장소를 포크하고 로컬 머신에 클론합니다
2. 기능 브랜치를 만듭니다 (`git checkout -b my-improvement`)
3. 변경 사항을 적용합니다
4. 풀 리퀘스트를 제출합니다

## 라이선스

이 프로젝트는 MIT 오픈 소스 라이선스 조건에 따라 라이선스가 부여됩니다. 전체 조건은 [LICENSE](../../LICENSE) 파일을 참조해 주세요.
