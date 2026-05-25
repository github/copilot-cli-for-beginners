![Chapter 06: MCP Servers](images/chapter-header.png)

> **もし Copilot が GitHub の Issue を読み、データベースをチェックし、PR を作成できたら……しかもすべてターミナルからできたらどうでしょうか？**

これまで、Copilot はあなたが直接与えたもの（`@` で参照したファイル、会話履歴、および自身の学習データ）しか扱えませんでした。しかし、もし Copilot が自分から GitHub リポジトリを確認したり、プロジェクト内のファイルをブラウズしたり、ライブラリの最新ドキュメントを調べたりできたらどうなるでしょうか？

それを実現するのが MCP (Model Context Protocol) です。これは Copilot を外部サービスに接続し、現実のライブデータへのアクセスを可能にする仕組みです。Copilot が接続する各サービスは「MCP サーバー」と呼ばれます。この章では、いくつかの接続をセットアップし、それによって Copilot が劇的に便利になる様子を見ていきます。

> 💡 **すでに MCP に詳しいですか？** [クイックスタート](#-組み込みの-github-mcp-を使う)へジャンプして、動作確認とサーバー設定を開始してください。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- MCP とは何か、なぜ重要なのかを理解する
- `/mcp` コマンドを使用して MCP サーバーを管理する
- GitHub、ファイルシステム、ドキュメント用の MCP サーバーを設定する
- 書籍アプリプロジェクトで MCP を活用したワークフローを実践する
- カスタム MCP サーバーを構築するタイミングと方法を知る（オプション）

> ⏱️ **推定所要時間**: 約50分（読みもの15分 ＋ 実践35分）

---

## 🧩 現実世界の例え：ブラウザの拡張機能

<img src="images/browser-extensions-analogy.png" alt="MCP サーバーはブラウザの拡張機能のようなもの" width="800"/>

MCP サーバーはブラウザの拡張機能のようなものだと考えてください。ブラウザ単体でもウェブページを表示できますが、拡張機能によってさらなるサービスと繋がります：

| ブラウザ拡張機能 | 接続先 | MCP での対応例 |
|-------------------|---------------------|----------------|
| パスワードマネージャー | パスワード保管庫 | **GitHub MCP** → リポジトリ、Issue、PR |
| Grammarly | 文章校正サービス | **Context7 MCP** → ライブラリのドキュメント |
| ファイルマネージャー | クラウドストレージ | **Filesystem MCP** → ローカルプロジェクトファイル |

拡張機能がなくてもブラウザは便利ですが、あればさらに強力なツールになります。MCP サーバーも Copilot に対して同じ役割を果たします。現実のライブデータソースに接続することで、GitHub の Issue を読んだり、ファイルシステムを探索したり、最新のドキュメントを取得したりできるようになります。

***MCP サーバーは Copilot を外の世界（GitHub、リポジトリ、ドキュメントなど）に接続します***

> 💡 **重要な洞察**: MCP がなければ、Copilot はあなたが `@` で明示的に共有したファイルしか見ることができません。MCP があれば、Copilot は自ら能動的にプロジェクトを探索し、GitHub リポジトリをチェックし、ドキュメントを調べることができます。これらはすべて自動的に行われます。

---

<img src="images/quick-start-mcp.png" alt="MCP サーバー接続を表す、浮遊するテックアイコンに囲まれた明るい火花を散らす電源ケーブルの接続" width="800"/>

# クイックスタート：30秒で MCP を体験

## 組み込みの GitHub MCP サーバーを使う
何も設定する前に、まずは MCP の動きを見てみましょう。
GitHub MCP サーバーはデフォルトで含まれています。これを試してみてください：

```bash
copilot
> List the recent commits in this repository
（このリポジトリの最近のコミットを一覧表示して）
```

もし Copilot が実際のリポジトリのコミットデータを返してきたら、それが MCP の働きです。GitHub MCP サーバーがあなたに代わって GitHub にアクセスしたのです。しかし、GitHub は *数あるサーバーの一つ* に過ぎません。この章では、Copilot がさらに多くのことをこなせるよう、他のサーバー（ファイルシステムへのアクセス、最新ドキュメントの取得など）を追加する方法を学びます。

---

## `/mcp show` コマンド

どの MCP サーバーが設定されており、有効になっているかを確認するには `/mcp show` を使用します：

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub サーバーしか表示されませんか？** それで正常です！まだ追加の MCP サーバーを登録していなければ、GitHub だけが表示されます。次のセクションで追加していきます。

> 📚 **すべての MCP 管理コマンドを知りたいですか？** チャット内では `/mcp` スラッシュコマンドで、ターミナルからは `copilot mcp` コマンドでサーバーを管理できます。章の最後にある [追加の MCP コマンド](#-追加の-mcp-コマンド) を参照してください。

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![MCP Status Demo](images/mcp-status-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

## MCP で何が変わるのか？

MCP がある場合とない場合の実践的な違いは以下の通りです：

**MCP なし：**
```bash
> What's in GitHub issue #42?

「GitHub へのアクセス権がありません。Issue の内容をコピーして貼り付けてください。」
```

**MCP あり：**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
ステータス: オープン
ラベル: bug, priority-high
説明: ユーザーからの報告によると、パスワードに……が含まれていると……
```

MCP によって、Copilot はあなたの実際の開発環境を認識できるようになります。

> 📚 **公式ドキュメント**: GitHub Copilot で MCP がどのように機能するかを詳しく知るには、[About MCP](https://docs.github.com/copilot/concepts/context/mcp)（英語）を参照してください。

MCP の動作を確認できたところで、追加のサーバーをセットアップしましょう。サーバーの追加方法は2つあります：**組み込みレジストリから**（最も簡単 — CLI 内でガイド付きセットアップ）または、**設定ファイルを手動で編集する**（より柔軯）。どちらを選べばよいか迷ったら、レジストリから始めてください。

---

## レジストリから MCP サーバーをインストールする

CLI には組み込みの MCP サーバーレジストリがあり、人気のサーバーを発見し、ガイド付きセットアップでインストールできます — JSON の手動編集は不要です。

```bash
copilot

> /mcp search
```

Copilot は利用可能なサーバーを表示するインタラクティブなピッカーを開きます。1つを選択すると、CLI が必要な設定（API キー、パスなど）を順番に確認し、自動的に設定ファイルに追加します。

> 💡 **レジストリを使う理由？** これが最も簡単な始め方です — npm パッケージ名、コマンド引数、JSON の構造を知る必要がありません。CLI がすべてを代行してくれます。

---

# MCP サーバーの設定

<img src="images/configuring-mcp-servers.png" alt="MCP サーバー設定を表す、プロ仕様のオーディオミキシングボードのノブやスライダーを調整する手" width="800"/>

MCP の動きを確認できたところで、追加のサーバーをセットアップしましょう。このセクションでは、設定ファイルの形式と新しいサーバーの追加方法を説明します。

---

## MCP 設定ファイル

MCP サーバーは、`~/.copilot/mcp-config.json`（ユーザーレベル、すべてのプロジェクトに適用）または `.mcp.json`（プロジェクトレベル、プロジェクトのルートに配置）で設定します。上記で `/mcp search` を使用した場合、CLI はすでにこのファイルを作成または更新していますが、カスタマイズのために形式を理解しておくと役立ちます。

> ⚠️ **注意**: `.vscode/mcp.json` は MCP 設定ファイルとしてサポートされなくなりました。既存の `.vscode/mcp.json` がある場合は、プロジェクトのルートにある `.mcp.json` に移行してください。CLI は古い設定ファイルを検出した場合、移行のヒントを表示します。

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

*ほとんどの MCP サーバーは npm パッケージとして配布されており、`npx` コマンドを介して実行されます。*

<details>
<summary>💡 <strong>JSON は初めてですか？</strong> 各フィールドの意味についてはこちらをクリック</summary>

| フィールド | 意味 |
|-------|---------------|
| `"mcpServers"` | すべての MCP サーバー設定を格納するコンテナ |
| `"server-name"` | 自分で決める名前（例: "github", "filesystem"） |
| `"type": "local"` | サーバーがあなたのマシン上で動作することを示します |
| `"command": "npx"` | 実行するプログラム（npx は npm パッケージを実行します） |
| `"args": [...]` | コマンドに渡される引数 |
| `"tools": ["*"]` | このサーバーのすべてのツールの使用を許可します |

**JSON の重要なルール：**
- 文字列には二重引用符 `"` を使用してください（一重引用符は不可）
- 最後の項目の後にカンマを置かないでください
- ファイルは有効な JSON である必要があります（不安な場合は [JSON バリデーター](https://jsonlint.com/) を使ってください）

</details>

---

## MCP サーバーの追加

GitHub MCP サーバーは組み込み済みで、セットアップは不要です。以下は、追加できる代表的なサーバーです。**興味のあるものを選ぶか、順番に試してみてください。**

| やりたいこと | リンク |
|---|---|
| Copilot にプロジェクトファイル内をブラウズさせる | [ファイルシステム・サーバー](#filesystem-server) |
| 最新のライブラリドキュメントを取得する | [Context7 サーバー](#context7-server-documentation) |
| その他のオプション（カスタムサーバー、web_fetch） | [さらに先へ](#beyond-the-basics) |

<details>
<summary><strong>ファイルシステム・サーバー</strong> - Copilot にプロジェクトファイルを探索させる</summary>
<a id="filesystem-server"></a>

### ファイルシステム・サーバー (Filesystem Server)

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

> 💡 **パスとしての `.`**: `.` は「現在のディレクトリ」を意味します。Copilot は、自身を起動した場所からの相対パスでファイルにアクセスできるようになります。Codespace の場合は、ワークスペースのルートになります。`/workspaces/copilot-cli-for-beginners` のような絶対パスを指定することも可能です。

これを `~/.copilot/mcp-config.json` に追加し、Copilot を再起動してください。

</details>

<details>
<summary><strong>Context7 サーバー</strong> - 最新のドキュメントを取得する</summary>
<a id="context7-server-documentation"></a>

### Context7 サーバー (ドキュメント)

Context7 は、人気のフレームワークやライブラリの最新ドキュメントへのアクセスを Copilot に提供します。古くなっている可能性のある学習データに頼る代わりに、Copilot は実際の最新ドキュメントを取得してきます。

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
- ✅ **コードはローカルに維持されます**

これを `~/.copilot/mcp-config.json` に追加し、Copilot を再起動してください。

</details>

<details>
<summary><strong>さらに先へ</strong> - カスタムサーバーとウェブアクセス（オプション）</summary>
<a id="beyond-the-basics"></a>

これらは、上記のコアサーバーに慣れた後のためのオプションです。

### Microsoft Learn MCP サーバー

これまで見てきたサーバー（filesystem, Context7）は、あなたのマシン上でローカルに動作します。しかし、MCP サーバーはリモートで動作させることもできます。つまり、Copilot CLI に URL を指定するだけで、あとは Copilot が処理してくれます。`npx` も `python` も、ローカルプロセスも依存関係のインストールも不要です。

[Microsoft Learn MCP サーバー](https://github.com/microsoftdocs/mcp) はその好例です。これは Azure、Microsoft Foundry、AI トピック、.NET、Microsoft 365 などの公式ドキュメントへの直接アクセスを提供します。モデルの学習データに頼るのではなく、ドキュメントを検索し、ページ全体を取得し、公式のコードサンプルを見つけることができます。

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **ローカルインストール不要**

**`/plugin install` によるクイックインストール：**

JSON 設定ファイルを手動で編集する代わりに、一つのコマンドでインストールできます：

```bash
copilot

> /plugin install microsoftdocs/mcp
```

これにより、サーバーとそれに関連するエージェントスキルが自動的に追加されます。インストールされるスキルには以下が含まれます：

- **microsoft-docs**: 概念、チュートリアル、事実確認の検索
- **microsoft-code-reference**: API リファレンス、コードサンプル、トラブルシューティング
- **microsoft-skill-creator**: Microsoft テクノロジーに関するカスタムスキルを生成するためのメタスキル

**使用例：**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 詳細：[Microsoft Learn MCP サーバーの概要](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch` によるウェブアクセス

Copilot CLI には、任意の URL からコンテンツを取得できる組み込みツール `web_fetch` が含まれています。これは、ターミナルを離れることなく README や API ドキュメント、リリースノートなどを取り込むのに便利です。MCP サーバーは不要です。

アクセス可能な URL は `~/.copilot/config.json`（Copilot 全般の設定）で制御できます。これは `~/.copilot/mcp-config.json`（MCP サーバーの定義）とは別物です。

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

**使用例：**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### カスタム MCP サーバーの構築

Copilot を独自の API、データベース、あるいは内部ツールに接続したいですか？Python でカスタム MCP サーバーを構築できます。既成のサーバー（GitHub, filesystem, Context7）でほとんどのユースケースはカバーできるため、これは完全にオプションです。

📖 書籍アプリを例にした完全なガイドは、[カスタム MCP サーバーガイド](mcp-custom-server.md)（英語）を参照してください。

📚 背景知識については、[MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners) も役立ちます。

</details>

<a id="complete-configuration-file"></a>

### 設定ファイルの完成形

ファイルシステムと Context7 サーバーを含んだ、完全な `mcp-config.json` は以下の通りです：

> 💡 **補足：** GitHub MCP は組み込み済みです。設定ファイルに追加する必要はありません。

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

これをグローバルアクセスのために `~/.copilot/mcp-config.json` として、あるいはプロジェクト固有の設定のために `.mcp.json` として保存してください。

---

# MCP サーバーを使う

MCP サーバーの設定が完了したところで、何ができるかを見てみましょう。

<img src="images/using-mcp-servers.png" alt="MCP サーバーの使用 - 開発者CLIが GitHub、ファイルシステム、Context7、カスタム/Web Fetchサーバーに接続されている様子を示すハブ・アンド・スポーク図" width="800" />

---

## サーバーの使用例

**試してみたいサーバーを選ぶか、順番に見ていきましょう。**

| 試したい内容 | リンク |
|---|---|
| GitHub リポジトリ、Issue、PR | [GitHub サーバー](#github-server-built-in) |
| プロジェクトファイルのブラウズ | [ファイルシステム・サーバーの使用](#filesystem-server-usage) |
| ライブラリドキュメントの検索 | [Context7 サーバーの使用](#context7-server-usage) |
| カスタム、Microsoft Learn、web_fetch の使用 | [さらに先への活用例](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub サーバー (組み込み)</strong> - リポジトリ、Issue、PR などへのアクセス</summary>
<a id="github-server-built-in"></a>

### GitHub サーバー (組み込み)

GitHub MCP サーバーは **組み込み済み** です。Copilot にログインしていれば（初期セットアップで完了しています）、すでに動作します。設定は不要です！

> 💡 **動かない場合** は、`/login` を実行して GitHub との再認証を行ってください。

<details>
<summary><strong>Dev Container での認証</strong></summary>

- **GitHub Codespaces** (推奨): 認証は自動的に行われます。`gh` CLI は Codespace のトークンを継承します。操作は不要です。
- **ローカルの Dev Container (Docker)**: コンテナ起動後に `gh auth login` を実行し、その後 Copilot を再起動してください。

**認証のトラブルシューティング：**
```bash
# 認証状態の確認
gh auth status

# 認証されていない場合はログイン
gh auth login

# GitHub MCP が接続されているか確認
copilot
> /mcp show
```

</details>

| 機能 | 例 |
|---------|----------|
| **リポジトリ情報** | コミット、ブランチ、コントリビューターの表示 |
| **Issue** | 一覧表示、作成、検索、コメント投稿 |
| **プルリクエスト** | 表示、差分確認、作成、ステータスチェック |
| **コード検索** | リポジトリ間でのコード検索 |
| **Actions** | ワークフローの実行状況やステータスのクエリ |

```bash
copilot

# このリポジトリの最近の活動を見る
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

> 💡 **自身のフォークで作業している場合** は、Issue やプルリクエストの作成といった書き込み操作も試せます。あとの演習で練習します。

> ⚠️ **結果が表示されませんか？** GitHub MCP は（ローカルファイルだけでなく）github.com 上のリモートリポジトリに対して動作します。リポジトリにリモートが設定されているか `git remote -v` で確認してください。

</details>

<details>
<summary><strong>ファイルシステム・サーバー</strong> - プロジェクトファイルのブラウズと分析</summary>
<a id="filesystem-server-usage"></a>

### ファイルシステム・サーバー

設定が完了すると、Copilot はファイルシステムのツールを自動的に使えるようになります：

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
<summary><strong>Context7 サーバー</strong> - ライブラリドキュメントの検索</summary>
<a id="context7-server-usage"></a>

### Context7 サーバー

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - テストの固定されたベースラインを提供するためにフィクスチャを使用します：

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # フィクスチャは自動的に引数として渡されます
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

ベストプラクティス：
- setup/teardown メソッドの代わりにフィクスチャを使用する
- 一時ファイルには tmp_path フィクスチャを使用する
- 環境の修正には monkeypatch を使用する
- フィクスチャのスコープ（function, class, module, session）を適切に設定する

> How can I apply this to the book app's test file?

# Copilot は公式の pytest パターンを知っているため、
# それを samples/book-app-project/tests/test_books.py に適用できます
```

</details>

<details>
<summary><strong>さらに先への活用例</strong> - カスタムサーバー、Microsoft Learn、web_fetch の使用</summary>
<a id="beyond-the-basics-usage"></a>

### さらに先へ

**カスタム MCP サーバー**：もし [カスタム MCP サーバーガイド](mcp-custom-server.md)（英語）に従って book-lookup サーバーを構築したなら、書籍コレクションを直接クエリできます：

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**：[Microsoft Learn MCP サーバー](#microsoft-learn-mcp-サーバー) をインストールしたなら、公式の Microsoft ドキュメントを直接検索できます：

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**：組み込みの `web_fetch` ツールを使って、任意の URL からコンテンツを取り込めます：

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## 複数サーバーのワークフロー

これらのワークフローは、開発者が「もうこれなしでは仕事をしたくない」と言う理由を物語っています。各例では、一つのセッションで複数の MCP サーバーを組み合わせています。

<img src="images/issue-to-pr-workflow.png" alt="MCP を使った Issue から PR へのワークフロー - GitHub Issue の取得からプルリクエストの作成までの完全な流れを示している" width="800"/>

*完全な MCP ワークフロー：GitHub MCP がリポジトリデータを取得し、Filesystem MCP がコードを見つけ、Context7 MCP がベストプラクティスを提供し、Copilot が分析を担当します。*

各例は独立しています。**興味のあるものを選ぶか、すべて読んでみてください。**

| 知りたい内容 | リンク |
|---|---|
| 複数のサーバーが連携する様子 | [複数サーバーによる探索](#multi-server-exploration) |
| 一つのセッションで Issue から PR まで進める | [Issue から PR へのワークフロー](#issue-to-pr-workflow) |
| プロジェクトの健康診断 | [ヘルス・ダッシュボード](#health-dashboard) |

<details>
<summary><strong>複数サーバーによる探索</strong> - ファイルシステム、GitHub、Context7 を一回のセッションで組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数の MCP サーバーを使って書籍アプリを探索する

```bash
copilot

# ステップ 1: Filesystem MCP を使って書籍アプリを探索
> List all Python files in samples/book-app-project/ and summarize
> what each file does

3つの Python ファイルが見つかりました：
- book_app.py: コマンドルーティング（list, add, remove, find）を備えた CLI エントリポイント
- books.py: JSON を介したデータ永続化を行う BookCollection クラス
- utils.py: ユーザー入力と表示のためのヘルパー関数

# ステップ 2: GitHub MCP を使って最近の変更をチェック
> What were the last 3 commits that touched files in samples/book-app-project/?

書籍アプリに影響した最近のコミット：
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# ステップ 3: Context7 MCP でベストプラクティスを調べる
> What are Python best practices for JSON data persistence?

Python ドキュメントより：
- ファイル入出力にはコンテキストマネージャ (with 文) を使う
- 破損したファイルのために JSONDecodeError を処理する
- 構造化データには dataclasses を使う
- データ破損を防ぐためにアトミックな書き込みを検討する

# ステップ 4: 提案を統合する
> Based on the book app code and these best practices,
> what improvements would you suggest?

提案：
1. add_book() に空文字列や無効な年のための入力バリデーションを追加する
2. save_books() でアトミックな書き込みを検討し、データ破損を防ぐ
3. utils.py の関数（get_user_choice, get_book_details）に型ヒントを追加する
```

<details>
<summary>🎬 MCP ワークフローの実際の動きを見てみよう！</summary>

![MCP Workflow Demo](images/mcp-workflow-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

**結果**: コード探索 → 履歴の確認 → ベストプラクティスの検索 → 改善計画の作成。**すべて一つのターミナルセッションで、3つの MCP サーバーを連携させて実現しました。**

</details>

<details>
<summary><strong>Issue から PR へのワークフロー</strong> - ターミナルを離れずに GitHub Issue からプルリクエストまで進める</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue から PR へのワークフロー（自身のプロジェクトで）

これは、書き込み権限のある自身のフォークやリポジトリで最も効果を発揮します：

> 💡 **今すぐ試せなくても大丈夫です。** 読み取り専用のクローンを使っている場合は、課題で練習します。今は流れを理解するために読んでください。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
ステータス: オープン
説明: add_book 関数があらゆる年の値を受け付けてしまいます……

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot が add_book() 内に年のバリデーションを実装します]

> Run the tests to make sure the fix works

8つのテストすべてに合格しました ✓

> Create a pull request titled "Add year validation to book app"

✓ PR #2 を作成しました：Add year validation to book app
```

**コピー＆ペーストなし。コンテキストの切り替えなし。一つのターミナルセッションで完結します。**

</details>

<details>
<summary><strong>ヘルス・ダッシュボード</strong> - 複数のサーバーを使ってプロジェクトの健全性を素早くチェックする</summary>
<a id="health-dashboard"></a>

#### 書籍アプリ・ヘルスダッシュボード

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

書籍アプリ・ヘルスレポート
======================

📊 見つかった関数：
- books.py: BookCollection 内の 8 つのメソッド（すべて型ヒントあり ✓）
- book_app.py: 6 つの関数（4 つに型ヒントあり、2 つに欠落）
- utils.py: 3 つの関数（1 つに型ヒントあり、2 つに欠落）

🧪 テストカバレッジ：
- test_books.py: BookCollection をカバーする 8 つのテスト関数
- 欠落: book_app.py の CLI 関数に対するテストなし
- 欠落: utils.py のヘルパー関数に対するテストなし

📝 最近の活動：
- 先週に 3 つのコミットあり
- 直近：テスト用フィクスチャを追加

推奨事項：
- utils.py の関数に型ヒントを追加する
- book_app.py の CLI ハンドラーに対するテストを追加する
- すべてのファイルが適切なサイズ（100行未満）で、良好な構造です！
```

**結果**: 複数のデータソースが数秒で集計されました。手動で行う場合、grep の実行、行数のカウント、git log の確認、テストファイルのブラウズが必要になり、15分以上かかる作業です。

</details>

---

# 練習

<img src="../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

**🎉 これで基本はマスターです！** MCP を理解し、サーバーの設定方法を知り、実際のワークフローを目にしました。次はあなたの番です。

---

## ▶️ 自分で試してみる

書籍アプリプロジェクトで MCP サーバーを使う練習をしましょう。

### 演習 1：MCP のステータスを確認する

まず、利用可能な MCP サーバーを確認します：

```bash
copilot

> /mcp show
```

GitHub サーバーが「enabled（有効）」としてリストされているはずです。表示されない場合は、`/login` を実行して認証してください。

---

### 演習 2：Filesystem MCP で書籍アプリを探索する

ファイルシステム・サーバーを設定済みなら、それを使って書籍アプリを探索しましょう：

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**期待される結果**: Copilot が `book_app.py`, `books.py`, `utils.py` とそれぞれの関数を一覧表示します。

> 💡 **まだファイルシステム MCP を設定していませんか？** 上記の [設定ファイルの完成形](#complete-configuration-file) セクションから JSON をコピーして作成してください。その後、Copilot を再起動します。

---

### 演習 3：GitHub MCP でリポジトリ履歴をクエリする

組み込みの GitHub MCP を使って、このコースのリポジトリを探索しましょう：

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**期待される結果**: GitHub リモートから最近のコミットメッセージとブランチ名が表示されます。

> ⚠️ **Codespace を使用中ですか？** 自動的に動作します。認証は継承されています。ローカルのクローンの場合は、`gh auth status` でログイン済みか確認してください。

---

### 演習 4：複数の MCP サーバーを組み合わせる

ファイルシステムと GitHub MCP を一つのセッションで組み合わせてみましょう：

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```
（`data.json` を読んでどんな本があるか教えて。それから最近のコミットを確認して、このファイルがいつ最後に修正されたか教えて。）

**期待される結果**: Copilot が JSON ファイルを読み取り（filesystem MCP）、"The Hobbit" や "1984" などを含む 5 冊の本をリストアップし、その後 GitHub にコミット履歴を問い合わせます。

**自己チェック**: なぜ「リポジトリのコミット履歴を確認して」という指示が、手動で `git log` を実行してその出力を貼り付けるよりも優れているのかを説明できれば、MCP を理解したと言えます。

---

## 📝 課題

### メインチャレンジ：書籍アプリの MCP 探索

書籍アプリプロジェクトで複数の MCP サーバーを組み合わせて使ってみましょう。以下のステップを**一つの Copilot セッション**で完了させてください：

1. **MCP が動作しているか確認**: `/mcp show` を実行し、少なくとも GitHub サーバーが有効であることを確認する。
2. **ファイルシステム MCP を設定する**（まだの場合）: `~/.copilot/mcp-config.json` を作成し、ファイルシステム・サーバーを設定する。
3. **コードを探索する**: ファイルシステム・サーバーを使って以下を Copilot に依頼する：
   - `samples/book-app-project/books.py` にあるすべての関数をリストアップさせる。
   - `samples/book-app-project/utils.py` のどの関数に型ヒントが欠けているかチェックさせる。
   - `samples/book-app-project/data.json` を読み取り、データの品質に問題がないか特定させる（ヒント：最後のエントリに注目）。
4. **リポジトリの活動をチェックする**: GitHub MCP を使って以下を Copilot に依頼する：
   - `samples/book-app-project/` 内のファイルに触れた最近のコミットをリストアップさせる。
   - オープンな Issue やプルリクエストがあるかチェックさせる。
5. **サーバーを組み合わせる**: 一つのプロンプトで以下を依頼する：
   - `samples/book-app-project/tests/test_books.py` にあるテストファイルを読み取らせる。
   - テストされている関数と `books.py` にある全関数を比較させる。
   - 不足しているテストカバレッジを要約させる。

**成功基準**: 一つのセッションでファイルシステムと GitHub の MCP データをシームレスに組み合わせることができ、それぞれの MCP サーバーが回答にどのように貢献したかを説明できること。

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**ステップ 1: MCP の確認**
```bash
copilot
> /mcp show
# "github" が enabled と表示されるはずです
# 表示されない場合は：/login を実行
```

**ステップ 2: 設定ファイルの作成**

上記の [設定ファイルの完成形](#complete-configuration-file) セクションの JSON を使い、`~/.copilot/mcp-config.json` として保存してください。

**ステップ 3: 探すべきデータ品質の問題**

`data.json` の最後のエントリは以下の通りです：
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
著者が空で、年が 0 です。これがデータ品質の問題です！

**ステップ 5: テストカバレッジの比較**

`test_books.py` のテストは、`add_book`, `mark_as_read`, `remove_book`, `get_unread_books`, `find_book_by_title` をカバーしています。`load_books`, `save_books`, `list_books` には直接的なテストがありません。また、`book_app.py` の CLI 関数や `utils.py` のヘルパーには全くテストがありません。

**MCP が動かない場合：** 設定ファイルを編集した後は Copilot を再起動してください。

</details>

### ボーナスチャレンジ：カスタム MCP サーバーの構築

さらに深く知りたいですか？[カスタム MCP サーバーガイド](mcp-custom-server.md)（英語）に従って、任意の API に接続する独自の MCP サーバーを Python で構築してみましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong> (クリックして展開)</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| GitHub MCP が組み込みであることを知らない | 手動でインストールや設定をしようとしてしまう | GitHub MCP はデフォルトで含まれています。試しに「このリポジトリの最近のコミットを見せて」と聞いてみてください |
| 設定ファイルの場所を間違える | MCP の設定が見つからない、または編集できない | ユーザーレベルの設定は `~/.copilot/mcp-config.json`、プロジェクトレベルは `.mcp.json（プロジェクトのルート）` です |
| 設定ファイルが不正な JSON 形式 | MCP サーバーの読み込みに失敗する | `/mcp show` で設定を確認し、JSON の構文を検証してください |
| MCP サーバーの認証を忘れる | 「Authentication failed」エラーが出る | 一部の MCP は別途認証が必要です。各サーバーの要件を確認してください |

### トラブルシューティング

**「MCP server not found」** - 以下を確認してください：
1. npm パッケージが存在するか：`npm view @modelcontextprotocol/server-github`
2. 設定が有効な JSON か
3. サーバー名が設定と一致しているか

現在の設定を確認するには `/mcp show` を使用します。

**「GitHub authentication failed」** - 組み込みの GitHub MCP は `/login` 時の認証情報を使用します。以下を試してください：

```bash
copilot
> /login
```

これにより GitHub と再認証されます。問題が解決しない場合は、GitHub アカウントに対象リポジトリへの必要な権限があるか確認してください。

**「MCP server failed to start」** - サーバーログを確認してください：
```bash
# サーバーコマンドを手動で実行してエラーを確認
npx -y @modelcontextprotocol/server-github
```

**MCP ツールが利用不可** - サーバーが有効（enabled）になっているか確認してください：
```bash
copilot

> /mcp show
# サーバーがリストにあり、enabled になっているか確認
```

サーバーが「disabled（無効）」になっている場合は、以下の [追加の `/mcp` コマンド](#-追加の-mcp-コマンド) を参照して有効化してください。

</details>

---

<details>
<summary>📚 <strong>追加の MCP コマンド</strong> (クリックして展開)</summary>
<a id="-追加の-mcp-コマンド"></a>

MCP サーバーの管理には2つの方法があります：**チャットセッション内でのスラッシュコマンド**、または**ターミナルでの `copilot mcp` コマンド**（チャットセッション不要）です。

### 方法 1：スラッシュコマンド（チャットセッション内）

`copilot` の内側で動作します：

| コマンド | 何をするか |
|---------|--------------|
| `/mcp show` | 設定済みの全 MCP サーバーとそのステータスを表示 |
| `/mcp add` | 対話形式で新しいサーバーを追加 |
| `/mcp edit <server-name>` | 既存のサーバー設定を編集 |
| `/mcp enable <server-name>` | 無効化されているサーバーを有効化（セッションをまたいで維持） |
| `/mcp disable <server-name>` | サーバーを無効化（セッションをまたいで維持） |
| `/mcp delete <server-name>` | サーバーを恒久的に削除 |
| `/mcp auth <server-name>` | OAuth を使用する MCP サーバーと再認証（アカウント切り替え後など） |

### 方法 2：`copilot mcp` コマンド（ターミナルから）

チャットセッションを開始せずに、ターミナルから直接管理できます：

```bash
# 設定済みの全 MCP サーバーをリストアップ
copilot mcp list

# サーバーを有効化
copilot mcp enable filesystem

# サーバーを無効化
copilot mcp disable context7
```

> 💡 **使い分けのコツ**: すでにチャット中の場合は `/mcp` スラッシュコマンドを使います。セッションを始める前に設定を素早く確認・変更したい場合は、ターミナルから `copilot mcp` を使います。

このコースのほとんどの場面では、`/mcp show` だけで十分です。他のコマンドは、管理するサーバーが増えてきたときに役立ちます。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **MCP** は、Copilot を外部サービス（GitHub、ファイルシステム、ドキュメントなど）に接続します。
2. **GitHub MCP は組み込み済み** です。設定不要で、`/login` するだけで使えます。
3. **ファイルシステムや Context7** は `~/.copilot/mcp-config.json` で設定します。
4. **複数サーバーのワークフロー** では、一つのセッションで複数のソースからのデータを組み合わせることができます。
5. **サーバー管理は2通り**: チャット内の `/mcp` スラッシュコマンド、またはターミナルの `copilot mcp` コマンドを使います。
6. **カスタムサーバー** を使えば、任意の API を接続できます（オプション、付録ガイドで解説）。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## ➡️ 次は？

これで、モード、コンテキスト、ワークフロー、エージェント、スキル、MCP というすべての構成要素が揃いました。いよいよこれらをすべて組み合わせる時です。

**[第07章：まとめ](../07-putting-it-together/README.ja.md)** では以下を学びます：

- エージェント、スキル、MCP を統合したワークフローの構築
- アイデアから PR マージまでの完全な機能開発
- フック（hooks）による自動化
- チーム環境でのベストプラクティス

---

**[← 第05章に戻る](../05-skills/README.ja.md)** | **[第07章へ進む →](../07-putting-it-together/README.ja.md)**
