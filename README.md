![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [学べること](#what-youll-learn) &ensp; ✅ [前提条件](#prerequisites) &ensp; 🤖 [Copilot ファミリー](#understanding-the-github-copilot-family) &ensp; 📚 [コース構成](#course-structure) &ensp; 📋 [コマンドリファレンス](#-github-copilot-cli-command-reference)

# GitHub Copilot CLI for Beginners

> **✨ AI を活用した command-line 支援で、開発 workflow を大きく強化しましょう。**

GitHub Copilot CLI は、AI 支援を terminal に直接届けてくれます。browser や code editor に移動しなくても、質問、フル機能の application 生成、code review、test 生成、issue の debug を command line 上で行えます。

まるで、あなたの code を読んで難しい pattern を説明し、作業をスピードアップしてくれる詳しい同僚が 24 時間いつでもそばにいるような感覚です。

> 📘 **web で見たいですか？** このコースは GitHub 上でそのまま進められますし、より一般的な閲覧体験を好む場合は [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) でも確認できます。

このコースは、次のような人向けに作られています。

- **開発者**: command line から AI を使いたい人
- **terminal 利用者**: IDE integration より keyboard 中心の workflow を好む人
- **team**: AI を活用した code review や開発プラクティスを標準化したい人たち

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="./images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - Find or host an event" width="100%" />
  </picture>
</a>

<a id="what-youll-learn"></a>
## 🎯 学べること

この hands-on コースでは、GitHub Copilot CLI をゼロから実務で使える状態まで学べます。全 chapter を通して、ひとつの Python 製の book collection app を題材にし、AI 支援 workflow を使って少しずつ改善していきます。最終的には、terminal から AI を使って code review、test 生成、debug、workflow の自動化を自信を持って行えるようになります。

**AI の経験は不要です。** terminal が使えれば学べます。

**おすすめの対象者:** Developers、学生、そして software development の経験があるすべての人。

<a id="prerequisites"></a>
## ✅ 前提条件

始める前に、次を用意してください。

- **GitHub account**: [無料で作成](https://github.com/signup)<br>
- **GitHub Copilot access**: [Free offering](https://github.com/features/copilot/plans)、[Monthly subscription](https://github.com/features/copilot/plans)、または [学生・教職員向け無料プラン](https://education.github.com/pack)<br>
- **Terminal の基本操作**: `cd`、`ls`、command の実行に慣れていること

<a id="understanding-the-github-copilot-family"></a>
## 🤖 GitHub Copilot ファミリーを理解する

GitHub Copilot は、AI を活用した複数の tool 群へと進化しています。それぞれが使われる場所は次のとおりです。

| 製品 | 使う場所 | 説明 |
|---------|----------|------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（このコース） | あなたの terminal | Terminal ネイティブな AI coding assistant |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains など | Agent mode、chat、inline suggestions |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | repository について深く対話できる chat、agent 作成など |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | issue を agent に割り当て、PR を受け取る |

このコースでは **GitHub Copilot CLI** に焦点を当て、AI 支援を terminal に直接取り込みます。

<a id="course-structure"></a>
## 📚 コース構成

![GitHub Copilot CLI Learning Path](images/learning-path.png)

| 章 | タイトル | 学べる内容 |
|:-------:|----------|------------|
| 00 | 🚀 [Quick Start](./00-quick-start/README.md) | installation と動作確認 |
| 01 | 👋 [First Steps](./01-setup-and-first-steps/README.md) | live demo と 3 つの対話モード |
| 02 | 🔍 [Context and Conversations](./02-context-conversations/README.md) | 複数 file をまたぐ project 分析 |
| 03 | ⚡ [Development Workflows](./03-development-workflows/README.md) | code review、debug、test 生成 |
| 04 | 🤖 [Create Specialized AI Assistants](./04-agents-custom-instructions/README.md) | workflow に合わせた custom agent |
| 05 | 🛠️ [Automate Repetitive Tasks](./05-skills/README.md) | 自動で読み込まれる skill |
| 06 | 🔌 [Connect to GitHub, Databases & APIs](./06-mcp-servers/README.md) | MCP server integration |
| 07 | 🎯 [Putting It All Together](./07-putting-it-together/README.md) | 完全な feature workflow |

## 📖 このコースの進め方

各 chapter は同じ流れで構成されています。

1. **たとえ話**: 身近な例で concept を理解する
2. **基本概念**: 必要な知識の土台を学ぶ
3. **実践例**: 実際に command を実行して結果を見る
4. **課題**: 学んだ内容を自分で試す
5. **次に学ぶこと**: 次の chapter の内容を先取りする

**Code example はそのまま実行できます。** このコース内の Copilot 用 text block は、terminal にコピーして実行できます。

<a id="-github-copilot-cli-command-reference"></a>
## 📋 GitHub Copilot CLI コマンドリファレンス

**[GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)** では、Copilot CLI を効果的に使うための command や keyboard shortcut を確認できます。

## 🙋 ヘルプ

- 🐛 **bug を見つけた場合**: [Issue を作成](https://github.com/github/copilot-cli-for-beginners/issues)
- 🤝 **contribute したい場合**: PR を歓迎します
- 📚 **公式 Docs**: [GitHub Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## ライセンス

この project は MIT open source license の条件で提供されています。詳細は [LICENSE](./LICENSE) を参照してください。

