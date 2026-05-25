![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

[English Version](./README.md)

🎯 [学習内容](#-学習内容) &ensp; ✅ [前提条件](#-前提条件) &ensp; 🤖 [Copilot ファミリー](#-github-copilot-ファミリーを理解する) &ensp; 📚 [コース構成](#-コース構成) &ensp; 📋 [コマンドリファレンス](#-github-copilot-cli-コマンドリファレンス)

# 初心者のための GitHub Copilot CLI

> **✨ AI を活用したコマンドライン・アシスタンスで、開発ワークフローを加速させましょう。**

GitHub Copilot CLI は、AI によるサポートをターミナルに直接提供します。ブラウザやコードエディタに切り替える代わりに、コマンドラインを離れることなく、質問をしたり、フル機能のアプリケーションを生成したり、コードレビュー、テスト生成、デバッグを行ったりすることができます。

これは、あなたのコードを読み、混乱しやすいパターンを説明し、作業をスピードアップさせてくれる、24時間365日いつでも相談できる物知りな同僚がいるようなものです。

> 📘 **ウェブで体験したいですか？** このコースは、このまま GitHub 上で進めることもできますし、[Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) でより一般的なブラウジング体験として見ることもできます。

このコースは以下の方を対象としています：

- コマンドラインから AI を活用したい **ソフトウェア開発者**
- IDE よりもキーボード駆動のワークフローを好む **ターミナルユーザー**
- AI を活用したコードレビューや開発手法を標準化したい **チーム**

## 🎯 学習内容

この実践的なコースでは、GitHub Copilot CLI を全く知らない状態から、使いこなせるようになるまでをガイドします。全章を通して一つの Python 製書籍コレクションアプリを扱い、AI を活用したワークフローで段階的に改善していきます。終了する頃には、ターミナルから自信を持ってコードレビュー、テスト生成、デバッグ、ワークフローの自動化を行えるようになります。

**AI の経験は不要です。** ターミナルが使えれば、誰でも学べます。

**以下の方に最適:** 開発者、学生、およびソフトウェア開発の経験があるすべての方。

## ✅ 前提条件

始める前に、以下が準備されていることを確認してください：

- **GitHub アカウント**: [無料で作成](https://github.com/signup)<br>
- **GitHub Copilot へのアクセス**: [無料プラン](https://github.com/features/copilot/plans)、[月額サブスクリプション](https://github.com/features/copilot/plans)、または [学生・教職員向けの無料提供](https://education.github.com/pack)<br>
- **ターミナルの基本知識**: `cd`、`ls`、コマンドの実行に慣れていること

## 🤖 GitHub Copilot ファミリーを理解する

GitHub Copilot は、AI を活用したツールのファミリーへと進化しました。それぞれの役割は以下の通りです：

| 製品 | 動作場所 | 説明 |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>(このコース) | あなたのターミナル | ターミナルネイティブな AI コーディングアシスタント |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code, Visual Studio, JetBrains など | エージェントモード、チャット、インライン補完 |
| [**GitHub.com 上の Copilot**](https://github.com/copilot) | GitHub | リポジトリに関する没入型チャット、エージェント作成など |
| [**GitHub Copilot クラウドエージェント**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | Issue をエージェントに割り当て、PR を作成 |

このコースでは、AI アシスタンスをターミナルに直接もたらす **GitHub Copilot CLI** に焦点を当てます。

## 📚 コース構成

![GitHub Copilot CLI 学習パス](images/learning-path.png)

| 章 | タイトル | 作成するもの |
|:-------:|-------|-------------------|
| 00 | 🚀 [クイックスタート](./00-quick-start/README.ja.md) | インストールと確認 |
| 01 | 👋 [はじめの一歩](./01-setup-and-first-steps/README.ja.md) | ライブデモ ＋ 3つのインタラクションモード |
| 02 | 🔍 [コンテキストと対話](./02-context-conversations/README.ja.md) | 複数ファイルプロジェクトの分析 |
| 03 | ⚡ [開発ワークフロー](./03-development-workflows/README.ja.md) | コードレビュー、デバッグ、テスト生成 |
| 04 | 🤖 [特化型 AI アシスタントの作成](./04-agents-custom-instructions/README.ja.md) | 自分のワークフローに合わせたカスタムエージェント |
| 05 | 🛠️ [反復タスクの自動化](./05-skills/README.ja.md) | 自動的にロードされる「スキル」 |
| 06 | 🔌 [GitHub、データベース、API への接続](./06-mcp-servers/README.ja.md) | MCP サーバーの統合 |
| 07 | 🎯 [まとめ](./07-putting-it-together/README.ja.md) | 完全な機能開発ワークフロー |

## 📖 このコースの進め方

各章は同じパターンで構成されています：

1. **現実世界の例え**: 身近な比較を通じて概念を理解する
2. **主要な概念**: 基本的な知識を学ぶ
3. **ハンズオン例**: 実際のコマンドを実行して結果を確認する
4. **課題**: 学んだことを実践する
5. **次は？**: 次の章の予告

**コード例はそのまま実行可能です。** このコース内の `copilot` で始まるテキストブロックはすべて、コピーしてターミナルで実行できます。

## 📋 GitHub Copilot CLI コマンドリファレンス

**[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)**（英語）では、Copilot CLI を効果的に使用するためのコマンドやキーボードショートカットを確認できます。

## 🙋 ヘルプが必要な場合

- 🐛 **バグを見つけた？** [Issue を開く](https://github.com/github/copilot-cli-for-beginners/issues)
- 📚 **公式ドキュメント:** [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## コントリビューション

> **注意**: コース内で使用されているコードは、レビュー、説明、デバッグ中に特定の出力を生成するように設計されているため、既存のコードを変更するプルリクエストは受け付けることができません。

**コントリビューション方法:**

1. このリポジトリをフォークし、ローカルマシンにクローンします
2. フィーチャーブランチを作成します (`git checkout -b my-improvement`)
3. 変更を加えます
4. プルリクエストを送信します

## ライセンス

このプロジェクトは MIT オープンソースライセンスの条件の下でライセンスされています。詳細は [LICENSE](./LICENSE) ファイルを参照してください。

*このドキュメントは元の英語版（Copyright GitHub, Inc.）を日本語に翻訳したものです。*
