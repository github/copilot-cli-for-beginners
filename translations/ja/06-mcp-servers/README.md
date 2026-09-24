![第 06 章: MCP サーバー](../../../06-mcp-servers/images/chapter-header.png)

> **Copilot がターミナルから GitHub のイシューを読んで、データベースをチェックして、PR を作成できたら？**

これまで Copilot は直接渡すもの: `@` で参照するファイル、会話履歴、自分のトレーニングデータしか使えませんでした。でも、GitHub リポジトリを確認したり、プロジェクトファイルを参照したり、ライブラリの最新ドキュメントを調べたりできたら？

それが MCP（Model Context Protocol）の役割です。Copilot を外部サービスに接続して、実際のライブデータにアクセスできるようにする方法です。Copilot が接続する各サービスは「MCP サーバー」と呼ばれます。この章では、いくつかの接続を設定して、Copilot が劇的に便利になる様子を見ていきます。

> 💡 **MCP を既に知っていますか？** [クイックスタート](#-use-the-built-in-github-mcp)にジャンプして動作を確認し、サーバーの設定を始めましょう。

## 🎯 学習目標

この章を終えると、以下ができるようになります。

- MCP とは何か、なぜ重要かを理解する
- `/mcp` コマンドを使って MCP サーバーを管理する
- GitHub、ファイルシステム、ドキュメント向けに MCP サーバーを設定する
- ブックアプリプロジェクトで MCP を活用したワークフローを使う
- カスタム MCP サーバーをいつ・どう構築するかを知る（オプション）

> ⏱️ **目安時間**: 約 50 分（15 分読む + 35 分ハンズオン）

---

## 🧩 現実世界のたとえ話: ブラウザの拡張機能

<img src="../../../06-mcp-servers/images/browser-extensions-analogy.png" alt="MCP サーバーはブラウザの拡張機能のようなもの" width="800"/>

MCP サーバーをブラウザの拡張機能と考えてください。ブラウザ単体でも Web ページを表示できますが、拡張機能で追加サービスに接続できます。

| ブラウザ拡張機能 | 接続先 | MCP の対応 |
|-------------------|---------------------|----------------|
| パスワードマネージャー | パスワード保管庫 | **GitHub MCP** → リポジトリ、イシュー、PR |
| Grammarly | 文章解析サービス | **Context7 MCP** → ライブラリドキュメント |
| ファイルマネージャー | クラウドストレージ | **Filesystem MCP** → ローカルプロジェクトファイル |

拡張機能なしでもブラウザは便利ですが、拡張機能があると強力なツールになります。MCP サーバーは Copilot に同じことをします。Copilot を実際のライブデータソースに接続して、GitHub のイシューを読んだり、ファイルシステムを探索したり、最新のドキュメントを取得したりできます。

***MCP サーバーは Copilot を外の世界に接続します: GitHub、リポジトリ、ドキュメントなど***

> 💡 **重要なポイント**: MCP なしでは、Copilot は `@` で明示的に共有したファイルしか見られません。MCP があると、プロジェクトを積極的に探索し、GitHub リポジトリを確認し、ドキュメントを調べることができます。すべて自動的に。

---

<img src="../../../06-mcp-servers/images/quick-start-mcp.png" alt="浮かぶテックアイコンに囲まれた明るい電気スパークとともに接続する電源ケーブル、MCP サーバー接続を表す" width="800"/>

# クイックスタート: 30 秒で MCP を使う

## 組み込みの GitHub MCP を使い始める
何も設定せずに今すぐ MCP を実際に見てみましょう。
GitHub MCP サーバーはデフォルトで含まれています。試してみてください。

```bash
copilot
> List the recent commits in this repository
```

Copilot が実際のコミットデータを返したら、MCP の動作を見たことになります。それが GitHub MCP サーバーがあなたの代わりに GitHub に接続している様子です。しかし GitHub は*1 つ*のサーバーに過ぎません。この章では、さらに多く（ファイルシステムアクセス、最新ドキュメントなど）を追加する方法を示します。

---

## `/mcp show` コマンド

`/mcp show` を使って、設定されている MCP サーバーと有効かどうかを確認します。

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub サーバーしか表示されない？** それで正常です！まだ追加の MCP サーバーを追加していない場合、GitHub だけがリストされます。次のセクションでさらに追加します。

> 📚 **すべての MCP 管理コマンドを見たいですか？** チャット内の `/mcp` スラッシュコマンド、またはターミナルから直接 `copilot mcp` でサーバーを管理できます。この章の末尾にある[コマンドリファレンス全体](#-additional-mcp-commands)を参照してください。

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![MCP ステータスデモ](../../../06-mcp-servers/images/mcp-status-demo.gif)

*デモの出力は異なります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

## MCP で何が変わるか？

MCP が実際にどんな違いをもたらすかです。

**MCP なし:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**MCP あり:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP により Copilot が実際の開発環境を把握できます。

> 📚 **公式ドキュメント**: [MCP について](https://docs.github.com/copilot/concepts/context/mcp) - GitHub Copilot での MCP の仕組みの詳しい説明。

---

# MCP サーバーの設定

<img src="../../../06-mcp-servers/images/configuring-mcp-servers.png" alt="MCP サーバーの設定を表すプロフェッショナルなオーディオミキシングボードのノブとスライダーを調整する手" width="800"/>

MCP の動作を確認したので、追加のサーバーを設定しましょう。サーバーを追加する方法は 2 つあります: **組み込みレジストリから**（最も簡単 — CLI 内でガイドされたセットアップ）または**設定ファイルを手動で編集**（より柔軟）。どちらを選ぶか確信がない場合はレジストリオプションから始めましょう。

---

## レジストリから MCP サーバーをインストールする

CLI には、人気のサーバーをガイドされたセットアップで発見してインストールできる組み込みの MCP サーバーレジストリがあります — JSON の編集は不要です。

```bash
copilot

> /mcp search
```

Copilot が利用可能なサーバーを示すインタラクティブなピッカーを開きます。1 つを選択すると、CLI が必要な設定（API キー、パスなど）を案内して、設定に自動的に追加します。

> 💡 **なぜレジストリを使うのですか？** 最も簡単に始める方法です — npm パッケージ名、コマンド引数、JSON 構造を知る必要がありません。CLI がすべてを処理します。

---

## MCP 設定ファイル

MCP サーバーは `~/.copilot/mcp-config.json`（ユーザーレベル、すべてのプロジェクトに適用）または `.mcp.json`（プロジェクトレベル、プロジェクトのルートに配置）で設定されます。上記で `/mcp search` を使用した場合、CLI はすでにこのファイルを作成または更新しています。ただし、カスタマイズのためにフォーマットを理解しておくと便利です。

> ⚠️ **注意**: `.vscode/mcp.json` は MCP 設定ソースとしてサポートされなくなりました。既存の `.vscode/mcp.json` がある場合は、プロジェクトルートの `.mcp.json` に移行してください。古い設定ファイルを検出すると CLI が移行ヒントを表示します。

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

*ほとんどの MCP サーバーは npm パッケージとして配布され、`npx` コマンドで実行されます。*

<details>
<summary>💡 <strong>JSON が初めてですか？</strong> クリックして各フィールドの意味を学ぶ</summary>

| フィールド | 意味 |
|-------|---------------|
| `"mcpServers"` | すべての MCP サーバー設定のコンテナ |
| `"server-name"` | 選択した名前（例: "github"、"filesystem"） |
| `"type": "local"` | サーバーはマシン上で動作する |
| `"command": "npx"` | 実行するプログラム（npx は npm パッケージを実行する） |
| `"args": [...]` | コマンドに渡す引数 |
| `"tools": ["*"]` | このサーバーのすべてのツールを許可する |

**重要な JSON のルール:**
- 文字列にはダブルクォート `"` を使う（シングルクォートではない）
- 最後の項目の後にトレーリングカンマをつけない
- ファイルは有効な JSON でなければならない（不確かな場合は [JSON バリデーター](https://jsonlint.com/)を使う）

</details>

---

## MCP サーバーを追加する

GitHub MCP サーバーは組み込みで設定は不要です。以下は追加できるサーバーです。**興味のあるものを選ぶか、順番に進めてください。**

| 目的... | ジャンプ先 |
|---|---|
| Copilot にプロジェクトファイルを参照させる | [Filesystem サーバー](#filesystem-サーバー) |
| 最新のライブラリドキュメントを取得する | [Context7 サーバー](#context7-サーバー-ドキュメント) |
| オプションの追加機能（カスタムサーバー、web_fetch）を探る | [基本を超えて](#基本を超えて) |

<details>
<summary><strong>Filesystem サーバー</strong> - Copilot がプロジェクトファイルを探索できるようにする</summary>
<a id="filesystem-server"></a>

### Filesystem サーバー

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

> 💡 **`.` パスについて**: `.` は「カレントディレクトリ」を意味します。Copilot は起動した場所に対して相対的にファイルにアクセスできます。Codespace では、ワークスペースのルートです。好みに応じて `/workspaces/copilot-cli-for-beginners` のような絶対パスも使えます。

これを `~/.copilot/mcp-config.json` に追加して Copilot を再起動します。

</details>

<details>
<summary><strong>Context7 サーバー</strong> - 最新のライブラリドキュメントを取得する</summary>
<a id="context7-server-documentation"></a>

### Context7 サーバー（ドキュメント）

Context7 は人気のフレームワークとライブラリの最新ドキュメントへのアクセスを Copilot に提供します。古くなっているかもしれないトレーニングデータに頼るのではなく、Copilot が実際の現在のドキュメントを取得します。

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

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **コードはローカルに留まる**

これを `~/.copilot/mcp-config.json` に追加して Copilot を再起動します。

</details>

<details>
<summary><strong>基本を超えて</strong> - カスタムサーバーと Web アクセス（オプション）</summary>
<a id="beyond-the-basics"></a>

これらは上記のコアサーバーに慣れた後のオプションの追加機能です。

### Microsoft Learn MCP サーバー

これまで見てきた MCP サーバー（filesystem、Context7）はすべてローカルマシンで動作します。しかし MCP サーバーはリモートでも動作できます。つまり、Copilot CLI を URL に向けるだけで残りは自動処理されます。`npx` も `python` も、ローカルプロセスも、インストールする依存関係も不要です。

[Microsoft Learn MCP サーバー](https://github.com/microsoftdocs/mcp)はその良い例です。Copilot CLI に公式 Microsoft ドキュメント（Azure、Microsoft Foundry などの AI トピック、.NET、Microsoft 365 など多数）への直接アクセスを提供し、モデルのトレーニングデータに頼る代わりにドキュメントを検索し、完全なページを取得し、公式コードサンプルを見つけられます。

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **ローカルインストール不要**

**`/plugin install` でのクイックインストール:**

JSON 設定ファイルを手動で編集する代わりに、1 つのコマンドでインストールできます。

```bash
copilot

> /plugin install microsoftdocs/mcp
```

これでサーバーとそれに関連するエージェントスキルが自動的に追加されます。インストールされるスキルには以下が含まれます。

- **microsoft-docs**: コンセプト、チュートリアル、事実の検索
- **microsoft-code-reference**: API の検索、コードサンプル、トラブルシューティング
- **microsoft-skill-creator**: Microsoft テクノロジーに関するカスタムスキルを生成するメタスキル

**使用方法:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 詳細: [Microsoft Learn MCP サーバーの概要](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch` で Web アクセス

Copilot CLI には任意の URL からコンテンツを取得できる組み込みの `web_fetch` ツールが含まれています。ターミナルを離れずに README、API ドキュメント、リリースノートを引き込むのに便利です。MCP サーバーは不要です。

アクセス可能な URL を `~/.copilot/config.json`（一般的な Copilot 設定）で制御できます。これは `~/.copilot/mcp-config.json`（MCP サーバー定義）とは別です。

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

**使用方法:**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### カスタム MCP サーバーを構築する

独自の API、データベース、内部ツールに Copilot を接続したいですか？Python でカスタム MCP サーバーを構築できます。これは完全にオプションです。プリビルドのサーバー（GitHub、filesystem、Context7）がほとんどのユースケースをカバーします。

📖 ブックアプリを例として使った完全なウォークスルーは [カスタム MCP サーバーガイド](mcp-custom-server.md)を参照してください。

📚 さらなる背景については [MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners)を参照してください。

</details>

<a id="complete-configuration-file"></a>

### 完全な設定ファイル

filesystem と Context7 サーバーを含む完全な `mcp-config.json` です。

> 💡 **注意:** GitHub MCP は組み込みです。設定ファイルに追加する必要はありません。

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

グローバルアクセスには `~/.copilot/mcp-config.json` として保存するか、プロジェクト固有の設定にはプロジェクトルートの `.mcp.json` として保存します。

---

# MCP サーバーを使う

MCP サーバーを設定したので、何ができるかを見てみましょう。

<img src="../../../06-mcp-servers/images/using-mcp-servers.png" alt="MCP サーバーを使う - GitHub、Filesystem、Context7、カスタム/Web Fetch サーバーに接続された開発者 CLI を示すハブアンドスポーク図" width="800" />

---

## サーバーの使用例

**探索するサーバーを選ぶか、順番に進めてください。**

| 試したいこと... | ジャンプ先 |
|---|---|
| GitHub のリポジトリ、イシュー、PR | [GitHub サーバー](#github-サーバー-組み込み) |
| プロジェクトファイルの参照 | [Filesystem サーバーの使用方法](#filesystem-server-usage) |
| ライブラリドキュメントの検索 | [Context7 サーバーの使用方法](#context7-server-usage) |
| カスタムサーバー、Microsoft Learn MCP、web_fetch の使用 | [基本を超えての使用方法](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub サーバー（組み込み）</strong> - リポジトリ、イシュー、PR などにアクセスする</summary>
<a id="github-server-built-in"></a>

### GitHub サーバー（組み込み）

GitHub MCP サーバーは**組み込み**です。Copilot にログインした（初期設定時に行った）場合、すでに動作しています。設定は不要！

> 💡 **動作しない場合？** `/login` を実行して GitHub で再認証してください。

<details>
<summary><strong>開発コンテナでの認証</strong></summary>

- **GitHub Codespaces**（推奨）: 認証は自動的です。`gh` CLI は Codespace トークンを継承します。操作は不要です。
- **ローカル開発コンテナ（Docker）**: コンテナ起動後に `gh auth login` を実行して、Copilot を再起動します。

**認証のトラブルシューティング:**
```bash
# 認証されているか確認する
gh auth status

# されていない場合はログインする
gh auth login

# GitHub MCP が接続されているか確認する
copilot
> /mcp show
```

</details>

| 機能 | 例 |
|---------|----------|
| **リポジトリ情報** | コミット、ブランチ、コントリビューターを表示する |
| **イシュー** | イシューをリストアップ、作成、検索、コメントする |
| **プルリクエスト** | PR、差分、PR 作成、ステータス確認 |
| **コード検索** | リポジトリ全体でコードを検索する |
| **Actions** | ワークフロー実行とステータスを照会する |

```bash
copilot

# このリポジトリの最近のアクティビティを確認する
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# リポジトリ構造を探索する
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# リポジトリ全体でコードパターンを検索する
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **自分のフォークで作業していますか？** このコースリポジトリをフォークした場合、イシューの作成やプルリクエストなどの書き込み操作も試せます。以下の演習で練習します。

> ⚠️ **結果が表示されない？** GitHub MCP はローカルファイルだけでなく、リポジトリのリモート（github.com 上）で動作します。リポジトリにリモートがあることを確認してください: `git remote -v` で確認します。

</details>

<details>
<summary><strong>Filesystem サーバー</strong> - プロジェクトファイルを参照・分析する</summary>
<a id="filesystem-server-usage"></a>

### Filesystem サーバー

設定すると、filesystem MCP は Copilot が自動的に使えるツールを提供します。

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
<summary><strong>Context7 サーバー</strong> - ライブラリドキュメントを検索する</summary>
<a id="context7-server-usage"></a>

### Context7 サーバー

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
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot は公式の pytest パターンを知っており
# samples/book-app-project/tests/test_books.py に適用できる
```

</details>

<details>
<summary><strong>基本を超えて</strong> - カスタムサーバーと web_fetch の使用方法</summary>
<a id="beyond-the-basics-usage"></a>

### 基本を超えて

**カスタム MCP サーバー**: [カスタム MCP サーバーガイド](mcp-custom-server.md)から book-lookup サーバーを構築した場合、書籍コレクションを直接照会できます。

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**: [Microsoft Learn MCP サーバー](#microsoft-learn-mcp-サーバー)をインストールした場合、公式 Microsoft ドキュメントを直接検索できます。

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**: 組み込みの `web_fetch` ツールを使って任意の URL からコンテンツを取得できます。

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## マルチサーバーワークフロー

これらのワークフローは、開発者が「もうこれなしでは働きたくない」と言う理由を示しています。各例は 1 つのセッションで複数の MCP サーバーを組み合わせています。

<img src="../../../06-mcp-servers/images/issue-to-pr-workflow.png" alt="MCP を使った issue から PR へのワークフロー - GitHub イシューの取得からプルリクエスト作成までの完全なフローを示す" width="800"/>

*完全な MCP ワークフロー: GitHub MCP がリポジトリデータを取得し、Filesystem MCP がコードを見つけ、Context7 MCP がベストプラクティスを提供し、Copilot が分析を処理する*

以下の各例は独立しています。**興味のあるものを選ぶか、すべて読んでください。**

| 見たいこと... | ジャンプ先 |
|---|---|
| 複数のサーバーが連携して動作する | [マルチサーバー探索](#multi-server-exploration) |
| 1 つのセッションでイシューから PR へ | [Issue-to-PR ワークフロー](#issue-to-pr-workflow) |
| クイックプロジェクト健全性チェック | [ヘルスダッシュボード](#health-dashboard) |

<details>
<summary><strong>マルチサーバー探索</strong> - filesystem、GitHub、Context7 を 1 つのセッションで組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数の MCP サーバーでブックアプリを探索する

```bash
copilot

# ステップ 1: filesystem MCP を使ってブックアプリを探索する
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# ステップ 2: GitHub MCP を使って最近の変更を確認する
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# ステップ 3: Context7 MCP でベストプラクティスを取得する
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# ステップ 4: 推奨事項をまとめる
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 MCP ワークフローを実際に見てみましょう！</summary>

![MCP ワークフローデモ](../../../06-mcp-servers/images/mcp-workflow-demo.gif)

*デモの出力は異なります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

**結果**: コード探索 → 履歴確認 → ベストプラクティス検索 → 改善計画。**3 つの MCP サーバーを使って、すべて 1 つのターミナルセッションから。**

</details>

<details>
<summary><strong>Issue-to-PR ワークフロー</strong> - ターミナルを離れずに GitHub イシューからプルリクエストへ</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue-to-PR ワークフロー（自分のリポジトリで）

これは書き込みアクセスを持つ自分のフォークやリポジトリで最もよく機能します。

> 💡 **今すぐ試せなくても大丈夫です。** 読み取り専用クローンの場合、課題でこれを練習します。今はフローを理解するために読み進めてください。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot が add_book() に年バリデーションを実装する]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**コピー&ペーストなし。コンテキスト切り替えなし。1 つのターミナルセッション。**

</details>

<details>
<summary><strong>ヘルスダッシュボード</strong> - 複数のサーバーを使ってクイックプロジェクト健全性チェックを行う</summary>
<a id="health-dashboard"></a>

#### ブックアプリヘルスダッシュボード

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

**結果**: 複数のデータソースが数秒で集約されます。手動では、grep の実行、行数のカウント、git log の確認、テストファイルの参照が必要でした。軽く 15 分以上の作業です。

</details>

---

# 練習

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

**🎉 必要な基礎を学びました！** MCP を理解し、サーバーの設定方法を確認し、実際のワークフローを見てきました。今度は自分で試す時間です。

---

## ▶️ 自分で試してみよう

これらの演習を完了してブックアプリプロジェクトで MCP サーバーを使う練習をしましょう。

### 演習 1: MCP ステータスを確認する

まず、利用可能な MCP サーバーを確認します。

```bash
copilot

> /mcp show
```

GitHub サーバーが有効としてリストされているはずです。なければ、`/login` を実行して認証します。

---

### 演習 2: Filesystem MCP でブックアプリを探索する

filesystem サーバーを設定した場合は、ブックアプリを探索するために使います。

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**期待される結果**: Copilot が `book_app.py`、`books.py`、`utils.py` とその関数をリストアップします。

> 💡 **filesystem MCP をまだ設定していませんか？** 上記の[完全な設定](#完全な設定ファイル)セクションから設定ファイルを作成してください。そして Copilot を再起動します。

---

### 演習 3: GitHub MCP でリポジトリ履歴を照会する

組み込みの GitHub MCP を使ってこのコースリポジトリを探索します。

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**期待される結果**: Copilot が GitHub リモートから最近のコミットメッセージとブランチ名を表示します。

> ⚠️ **Codespace にいますか？** これは自動的に機能します。認証は継承されます。ローカルクローンの場合は、`gh auth status` でログインしていることを確認してください。

---

### 演習 4: 複数の MCP サーバーを組み合わせる

filesystem と GitHub MCP を 1 つのセッションで組み合わせます。

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**期待される結果**: Copilot が JSON ファイルを読み込み（filesystem MCP）、「The Hobbit」、「1984」、「Dune」、「To Kill a Mockingbird」、「Mysterious Book」を含む 5 冊の本をリストアップし、コミット履歴を GitHub に照会します。

**自己確認**: 「`git log` を手動で実行してプロンプトに出力を貼り付けるより、『リポジトリのコミット履歴を確認して』の方がなぜ良いか」を説明できれば MCP を理解しています。

---

## 📝 課題

### メインチャレンジ: ブックアプリ MCP 探索

ブックアプリプロジェクトで MCP サーバーを一緒に使う練習をしましょう。1 つの Copilot セッションでこれらのステップを完了します。

1. **MCP が動作していることを確認する**: `/mcp show` を実行して少なくとも GitHub サーバーが有効になっていることを確認する
2. **filesystem MCP を設定する**（まだの場合）: filesystem サーバーの設定で `~/.copilot/mcp-config.json` を作成する
3. **コードを探索する**: filesystem サーバーを使って Copilot に以下を依頼する:
   - `samples/book-app-project/books.py` のすべての関数をリストアップする
   - `samples/book-app-project/utils.py` で型ヒントが欠けている関数を確認する
   - `samples/book-app-project/data.json` を読んでデータ品質の問題を特定する（ヒント: 最後のエントリを確認する）
4. **リポジトリアクティビティを確認する**: GitHub MCP を使って Copilot に以下を依頼する:
   - `samples/book-app-project/` のファイルに触れた最近のコミットをリストアップする
   - オープンなイシューやプルリクエストがあるか確認する
5. **サーバーを組み合わせる**: 1 つのプロンプトで Copilot に以下を依頼する:
   - `samples/book-app-project/tests/test_books.py` のテストファイルを読む
   - テストされた関数を `books.py` のすべての関数と比較する
   - 欠けているテストカバレッジをまとめる

**成功基準**: 1 つの Copilot セッションで filesystem と GitHub MCP データをシームレスに組み合わせ、各 MCP サーバーがレスポンスに何を貢献したかを説明できます。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**ステップ 1: MCP を確認する**
```bash
copilot
> /mcp show
# "github" が有効として表示されるはず
# 表示されない場合は実行: /login
```

**ステップ 2: 設定ファイルを作成する**

上記の[完全な設定](#完全な設定ファイル)セクションの JSON を使って `~/.copilot/mcp-config.json` として保存します。

**ステップ 3: 探すデータ品質の問題**

`data.json` の最後の本は以下です:
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
著者が空で年が 0 です。それがデータ品質の問題です！

**ステップ 5: テストカバレッジの比較**

`test_books.py` のテストがカバーするもの: `add_book`、`mark_as_read`、`remove_book`、`get_unread_books`、`find_book_by_title`。`load_books`、`save_books`、`list_books` のような関数には直接のテストがありません。`book_app.py` の CLI 関数と `utils.py` のヘルパーはテストが全くありません。

**MCP が動作しない場合:** 設定ファイルを編集した後に Copilot を再起動してください。

</details>

### ボーナスチャレンジ: カスタム MCP サーバーを構築する

さらに深く掘り下げる準備ができましたか？[カスタム MCP サーバーガイド](mcp-custom-server.md)に従って、任意の API に接続する Python の独自 MCP サーバーを構築してください。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| GitHub MCP が組み込みであることを知らない | 手動でインストール/設定しようとする | GitHub MCP はデフォルトで含まれている。試してみてください: 「List the recent commits in this repo」 |
| 設定が間違った場所にある | MCP 設定を見つけたり編集できない | ユーザーレベルの設定は `~/.copilot/mcp-config.json`、プロジェクトレベルはプロジェクトルートの `.mcp.json` |
| 設定ファイルの JSON が無効 | MCP サーバーが読み込まれない | `/mcp show` で設定を確認し、JSON 構文を検証する |
| MCP サーバーの認証を忘れる | 「Authentication failed」エラー | 一部の MCP は個別の認証が必要。各サーバーの要件を確認する |

### トラブルシューティング

**「MCP server not found」** - 以下を確認する:
1. npm パッケージが存在する: `npm view @modelcontextprotocol/server-github`
2. 設定が有効な JSON である
3. サーバー名が設定と一致している

`/mcp show` を使って現在の設定を確認します。

**「GitHub authentication failed」** - 組み込みの GitHub MCP は `/login` の認証情報を使います。試してみてください:

```bash
copilot
> /login
```

これで GitHub で再認証されます。問題が続く場合は、GitHub アカウントがアクセスしているリポジトリに必要な権限を持っているか確認してください。

**「MCP server failed to start」** - サーバーログを確認する:
```bash
# サーバーコマンドを手動で実行してエラーを確認する
npx -y @modelcontextprotocol/server-github
```

**MCP ツールが利用できない** - サーバーが有効になっていることを確認する:
```bash
copilot

> /mcp show
# サーバーがリストされて有効になっているか確認する
```

サーバーが無効の場合、再有効化の方法は以下の[追加の `/mcp` コマンド](#-additional-mcp-commands)を参照してください。

</details>

---

<details>
<summary>📚 <strong>追加の MCP コマンド</strong>（クリックして展開）</summary>
<a id="-additional-mcp-commands"></a>

MCP サーバーを管理する方法は 2 つあります: **チャットセッション内のスラッシュコマンド**を使うか、**ターミナルから直接 `copilot mcp` コマンド**を使います（チャットセッション不要）。

### オプション 1: スラッシュコマンド（チャットセッション内）

`copilot` 内にいるときに機能します:

| コマンド | 機能 |
|---------|--------------|
| `/mcp show` | 設定されたすべての MCP サーバーとそのステータスを表示する |
| `/mcp add` | 新しいサーバーを追加するためのインタラクティブなセットアップ |
| `/mcp edit <server-name>` | 既存のサーバー設定を編集する |
| `/mcp enable <server-name>` | 無効なサーバーを有効にする（セッション間で持続する） |
| `/mcp disable <server-name>` | サーバーを無効にする（セッション間で持続する） |
| `/mcp delete <server-name>` | サーバーを恒久的に削除する |
| `/mcp auth <server-name>` | OAuth を使う MCP サーバーで再認証する（例: アカウントを切り替えた後） |

### オプション 2: `copilot mcp` コマンド（ターミナルから）

チャットセッションを開始せずにターミナルから直接 MCP サーバーを管理することもできます:

```bash
# 設定されたすべての MCP サーバーをリストアップする
copilot mcp list

# サーバーを有効にする
copilot mcp enable filesystem

# サーバーを無効にする
copilot mcp disable context7
```

> 💡 **どちらをいつ使うか？** チャットセッション中はすでにいる場合は `/mcp` スラッシュコマンドを使います。セッションを始める前にサーバー設定を素早く確認・変更したい場合はターミナルから `copilot mcp` を使います。

このコースのほとんどでは、`/mcp show` があれば十分です。他のコマンドは時間をかけてより多くのサーバーを管理するにつれて便利になります。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **MCP** は Copilot を外部サービス（GitHub、filesystem、ドキュメント）に接続する
2. **GitHub MCP は組み込み** - 設定は不要、`/login` だけ
3. **Filesystem と Context7** は `~/.copilot/mcp-config.json` で設定する
4. **マルチサーバーワークフロー**は 1 つのセッションで複数のソースからデータを組み合わせる
5. **サーバーを管理する 2 つの方法**: チャット内の `/mcp` スラッシュコマンド、またはターミナルからの `copilot mcp` を使う
6. **カスタムサーバー**はどの API にも接続できる（オプション、付録ガイドでカバー）

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次のステップ

これですべてのビルディングブロックが揃いました: モード、コンテキスト、ワークフロー、エージェント、スキル、MCP。すべてを組み合わせる時間です。

[**第 07 章: すべてをまとめる**](../07-putting-it-together/README.md)では以下を学びます。

- エージェント、スキル、MCP を統合ワークフローで組み合わせる
- アイデアからマージされた PR までの完全な機能開発
- フックによる自動化
- チーム環境でのベストプラクティス

---

[**← 第 05 章に戻る**](../05-skills/README.md) | [**第 07 章に進む →**](../07-putting-it-together/README.md)
