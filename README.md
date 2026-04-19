![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [学べること](#what-youll-learn) &ensp; ✅ [前提条件](#prerequisites) &ensp; 🤖 [Copilot ファミリー](#understanding-the-github-copilot-family) &ensp; 📚 [コース構成](#course-structure) &ensp; 📋 [コマンドリファレンス](#command-reference)

# GitHub Copilot CLI for Beginners

> **✨ AI を活用した command-line 支援で、開発ワークフローをより強力にしましょう。**

GitHub Copilot CLI は、AI 支援を terminal へ直接届けます。ブラウザーや code editor に切り替えなくても、質問、アプリケーション生成、code review、test 生成、debug などを command line 上でそのまま行えます。

まるで、あなたの code を読み取り、分かりにくいパターンを説明し、より素早く作業できるよう助けてくれる詳しい同僚が、24 時間いつでもそばにいるような感覚です。

> 📘 **Web で読みたい方へ** GitHub 上でこのコースを進めることもできますし、より一般的な閲覧体験をしたい場合は [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) でも見ることができます。

このコースは、次のような方を対象にしています。

- **Software Developers**: command line から AI を活用したい方
- **Terminal users**: IDE 統合よりもキーボード中心のワークフローを好む方
- **Teams looking to standardize**: AI 支援による code review や開発プラクティスを標準化したいチーム

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="./images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - Find or host an event" width="100%" />
  </picture>
</a>

<a id="what-youll-learn"></a>
## 🎯 学べること

このハンズオンコースでは、GitHub Copilot CLI をゼロから実用レベルまで段階的に学べます。すべての章を通して 1 つの Python 製 book collection app を扱い、AI 支援ワークフローを使いながら少しずつ改善していきます。最終的には、terminal から AI を使って code review、test 生成、debug、workflow の自動化を自信を持って進められるようになります。

**AI の経験は不要です。** terminal の基本操作ができれば学習を始められます。

**こんな方に最適です:** Developers、学生、そして software development の経験があるすべての方。

<a id="prerequisites"></a>
## ✅ 前提条件

開始前に、次のものを用意してください。

- **GitHub account**: [無料で作成](https://github.com/signup)<br>
- **GitHub Copilot access**: [Free offering](https://github.com/features/copilot/plans)、[Monthly subscription](https://github.com/features/copilot/plans)、または [学生・教職員向け無料プラン](https://education.github.com/pack)<br>
- **Terminal の基本操作**: `cd`、`ls`、コマンド実行に慣れていること

<a id="understanding-the-github-copilot-family"></a>
## 🤖 GitHub Copilot ファミリーを理解する

GitHub Copilot は、AI を活用した複数のツール群へと進化しています。以下は、それぞれがどこで使われるかの一覧です。

| Product | 利用場所 | 説明 |
|---------|---------------|------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（このコース） | terminal | terminal-native な AI coding assistant |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains など | Agent mode、chat、inline suggestions |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | repository について深く対話できる immersive chat、agent 作成など |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | issue を agent に割り当てて、PR を受け取ることが可能 |

このコースでは **GitHub Copilot CLI** に焦点を当て、AI 支援を terminal に直接取り込む方法を学びます。

<a id="course-structure"></a>
## 📚 コース構成

![GitHub Copilot CLI Learning Path](images/learning-path.png)

| Chapter | Title | 内容 |
|:-------:|-------|------|
| 00 | 🚀 [Quick Start](./00-quick-start/README.md) | インストールと動作確認 |
| 01 | 👋 [First Steps](./01-setup-and-first-steps/README.md) | Live demo と 3 つの操作モード |
| 02 | 🔍 [Context and Conversations](./02-context-conversations/README.md) | 複数ファイルの project 分析 |
| 03 | ⚡ [Development Workflows](./03-development-workflows/README.md) | code review、debug、test 生成 |
| 04 | 🤖 [Create Specialized AI Assistants](./04-agents-custom-instructions/README.md) | workflow 向けの custom agent 作成 |
| 05 | 🛠️ [Automate Repetitive Tasks](./05-skills/README.md) | 自動で読み込まれる skill |
| 06 | 🔌 [Connect to GitHub, Databases & APIs](./06-mcp-servers/README.md) | MCP server 連携 |
| 07 | 🎯 [Putting It All Together](./07-putting-it-together/README.md) | 一連の feature workflow の実践 |

## 📖 このコースの進め方

各 chapter は、次の同じ流れで構成されています。

1. **Real-World Analogy**: 身近な例えで概念を理解する
2. **Core Concepts**: 必要な基礎知識を学ぶ
3. **Hands-On Examples**: 実際にコマンドを実行して結果を見る
4. **Assignment**: 学んだ内容を自分で試す
5. **What's Next**: 次の chapter の内容を先取りする

**Code examples はそのまま実行できます。** このコース内の copilot テキストブロックは、terminal にコピーして実行できる形になっています。

<a id="command-reference"></a>
## 📋 GitHub Copilot CLI コマンドリファレンス

**[GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)** では、Copilot CLI をより効果的に使うためのコマンドや keyboard shortcut を確認できます。

## 🙋 サポートが必要な場合

- 🐛 **バグを見つけましたか？** [Issue を作成](https://github.com/github/copilot-cli-for-beginners/issues)
- 🤝 **貢献したいですか？** PR は歓迎です
- 📚 **公式ドキュメント:** [GitHub Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## ライセンス

この project は MIT open source license の条件の下で提供されています。詳細は [LICENSE](./LICENSE) ファイルを参照してください。

