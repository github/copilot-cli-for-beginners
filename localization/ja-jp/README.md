![GitHub Copilot CLI for Beginners](../../images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [学習内容](#what-youll-learn) &ensp; ✅ [前提条件](#prerequisites) &ensp; 🤖 [Copilot ファミリー](#understanding-the-github-copilot-family) &ensp; 📚 [コース構成](#course-structure) &ensp; 📋 [コマンドリファレンス](#-github-copilot-cli-command-reference)

# GitHub Copilot CLI for Beginners

> **✨ AI を活用したコマンドライン支援で、開発ワークフローを超強化する方法を学びましょう。**

GitHub Copilot CLI は、AI 支援機能をターミナルに直接提供します。ブラウザやコードエディタに切り替えることなく、コマンドラインを離れずに質問したり、フル機能のアプリケーションを生成したり、コードをレビューしたり、テストを生成したり、問題をデバッグしたりできます。

24 時間 365 日利用可能な知識豊富な同僚のようなもので、コードを読んで複雑なパターンを説明し、より速く作業できるよう手伝ってくれます！

> 📘 **Web 体験をご希望ですか？** このコースは GitHub 上でそのまま進めることも、[Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) で従来のブラウジング体験として閲覧することもできます。

このコースは以下の方を対象としています。

- コマンドラインから AI を活用したい**ソフトウェア開発者**
- IDE 統合よりキーボード主体のワークフローを好む**ターミナルユーザー**
- AI を活用したコードレビューと開発プラクティスを標準化したい**チーム**

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="../../images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - イベントを見つけるか開催しましょう" width="100%" />
  </picture>
</a>

## 🎯 学習内容 {#what-youll-learn}

このハンズオンコースは、GitHub Copilot CLI をゼロから実践的に使いこなせるようになることを目的としています。すべての章を通して 1 つの Python 製ブックコレクションアプリを使用し、AI 支援ワークフローで段階的に改善します。最終的には、ターミナルからコードのレビュー、テスト生成、バグのデバッグ、ワークフローの自動化を自信を持って行えるようになります。

**AI 経験は不要です。** ターミナルが使えれば、このコースを学ぶことができます。

**最適な対象者:** 開発者、学生、ソフトウェア開発の経験がある方。

## ✅ 前提条件 {#prerequisites}

開始前に、以下を準備してください。

- **GitHub アカウント**: [無料で作成する](https://github.com/signup)<br>
- **GitHub Copilot へのアクセス**: [無料プラン](https://github.com/features/copilot/plans)、[月次サブスクリプション](https://github.com/features/copilot/plans)、または[学生・教員向け無料プラン](https://education.github.com/pack)<br>
- **ターミナルの基礎**: `cd`、`ls`、コマンドの実行に慣れていること

## 🤖 GitHub Copilot ファミリーを理解する {#understanding-the-github-copilot-family}

GitHub Copilot は AI を活用したツールのファミリーへと進化しています。各ツールの位置づけは次のとおりです。

| 製品 | 実行環境 | 説明 |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（このコース） | ターミナル | ターミナルネイティブの AI コーディングアシスタント |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains など | エージェントモード、チャット、インライン提案 |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | リポジトリに関する本格的なチャット、エージェント作成など |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | Issue をエージェントに割り当て、PR を受け取る |

このコースは **GitHub Copilot CLI** に焦点を当て、AI 支援機能をターミナルに直接提供します。

## 📚 コース構成 {#course-structure}

![GitHub Copilot CLI 学習パス](../../images/learning-path.png)

| 章 | タイトル | 作るもの |
|:-------:|-------|-------------------|
| 00 | 🚀 [クイックスタート](./00-quick-start/README.md) | インストールと動作確認 |
| 01 | 👋 [はじめの一歩](./01-setup-and-first-steps/README.md) | ライブデモと 3 つのインタラクションモード |
| 02 | 🔍 [コンテキストと会話](./02-context-conversations/README.md) | マルチファイルプロジェクト分析 |
| 03 | ⚡ [開発ワークフロー](./03-development-workflows/README.md) | コードレビュー、デバッグ、テスト生成 |
| 04 | 🤖 [特化型 AI アシスタントの作成](./04-agents-custom-instructions/README.md) | ワークフロー向けカスタムエージェント |
| 05 | 🛠️ [繰り返し作業の自動化](./05-skills/README.md) | 自動的に読み込まれるスキル |
| 06 | 🔌 [GitHub・データベース・API との連携](./06-mcp-servers/README.md) | MCP サーバーの統合 |
| 07 | 🎯 [すべてを組み合わせる](./07-putting-it-together/README.md) | 完全な機能ワークフロー |

## 📖 このコースの進め方

各章は同じパターンで構成されています。

1. **現実世界のたとえ話**: 身近な比較でコンセプトを理解する
2. **コアコンセプト**: 必須知識を学ぶ
3. **ハンズオン例**: 実際のコマンドを実行して結果を確認する
4. **課題**: 学んだことを実践する
5. **次のステップ**: 次の章のプレビュー

**コード例は実行可能です。** このコースのすべての copilot テキストブロックは、コピーしてターミナルで実行できます。

## 📋 GitHub Copilot CLI コマンドリファレンス {#-github-copilot-cli-command-reference}

**[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)** では、Copilot CLI を効果的に使うためのコマンドやキーボードショートカットを確認できます。

## 🙋 ヘルプを得るには

- 🐛 **バグを見つけた場合？** [Issue を開く](https://github.com/github/copilot-cli-for-beginners/issues)
- 📚 **公式ドキュメント:** [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## コントリビュート

> **注意**: コースで使用されているコードは、レビュー・説明・デバッグ中に特定の種類の出力を生成するよう設計されているため、既存のコードを変更する PR は受け付けられません。

**コントリビュートの方法:**

1. このリポジトリをフォークして自分のマシンにクローンする
2. フィーチャーブランチを作成する (`git checkout -b my-improvement`)
3. 変更を加える
4. プルリクエストを提出する

## ライセンス

このプロジェクトは MIT オープンソースライセンスの条件のもとでライセンスされています。詳細な条件については [LICENSE](../../LICENSE) ファイルを参照してください。
