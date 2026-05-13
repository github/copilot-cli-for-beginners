![第 04 章: エージェントとカスタム指示](../../../04-agents-custom-instructions/images/chapter-header.png)

> **Python コードレビュアー、テストエキスパート、セキュリティレビュアーを 1 つのツールで雇えたら？**

第 03 章では、コードレビュー、リファクタリング、デバッグ、テスト生成、Git 統合という必須ワークフローをマスターしました。それらで GitHub Copilot CLI を使った生産性は十分高まります。さらに一歩進めましょう。

これまでは Copilot CLI を汎用アシスタントとして使ってきました。エージェントを使うと、型ヒントと PEP 8 を強制するコードレビュアーや、pytest ケースを書くテストヘルパーなど、組み込みの基準を持つ特定のペルソナを与えることができます。同じプロンプトが対象を絞った指示を持つエージェントに処理されると、明らかに良い結果が得られることがわかります。

## 🎯 学習目標

この章を終えると、以下ができるようになります。

- 組み込みエージェントを使う: プラン（`/plan`）、コードレビュー（`/review`）、自動エージェント（Explore、Task）を理解する
- エージェントファイル（`.agent.md`）を使って特化したエージェントを作成する
- ドメイン固有のタスクにエージェントを使う
- `/agent` と `--agent` を使ってエージェントを切り替える
- プロジェクト固有の標準のためのカスタム指示ファイルを書く

> ⏱️ **目安時間**: 約 55 分（20 分読む + 35 分ハンズオン）

---

## 🧩 現実世界のたとえ話: 専門家を雇う

家に問題があるとき、1 人の「汎用ヘルパー」を呼ぶわけではありません。専門家を呼びます。

| 問題 | 専門家 | 理由 |
|---------|------------|-----|
| 水漏れ | 配管工 | 配管規格を知り、専門ツールを持っている |
| 配線工事 | 電気工事士 | 安全要件を理解し、規格に準拠している |
| 屋根の葺き替え | 屋根工事業者 | 材料を知り、地域の気候を考慮している |

エージェントも同じように機能します。汎用 AI の代わりに、特定のタスクに集中して適切なプロセスを知っているエージェントを使います。指示を一度設定して、そのスペシャリティが必要なときにいつでも再利用します: コードレビュー、テスト、セキュリティ、ドキュメント。

<img src="../../../04-agents-custom-instructions/images/hiring-specialists-analogy.png" alt="専門家を雇うたとえ話 - 家の修理に専門の職人を呼ぶように、AI エージェントはコードレビュー、テスト、セキュリティ、ドキュメントなどの特定タスクに特化している" width="800" />

---

# エージェントを使う

組み込みおよびカスタムエージェントをすぐに始めましょう。

---

## *エージェントが初めてですか？* ここから始めましょう！
エージェントを使ったことも作ったこともない場合は、このコースを始めるために知っておくべきことがすべてここにあります。

1. **今すぐ*組み込み*エージェントを試してみましょう:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   これはプランエージェントを呼び出してステップバイステップの実装計画を作成します。

2. **カスタムエージェントの例を見てみましょう:** エージェントの指示を定義するのは簡単です。提供されている [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) ファイルを見てパターンを確認してください。

3. **コアコンセプトを理解する:** エージェントは汎用の専門家ではなく専門家に相談するようなものです。「フロントエンドエージェント」は自動的にアクセシビリティとコンポーネントパターンに集中します。エージェントの指示にすでに指定されているので、いちいち思い出させる必要はありません。


## 組み込みエージェント

**第 03 章の開発ワークフローですでにいくつかの組み込みエージェントを使っています！**
<br>`/plan` と `/review` は実際には組み込みエージェントです。ここで仕組みがわかります。完全なリストは以下のとおりです。

| エージェント | 呼び出し方 | 機能 |
|-------|---------------|--------------|
| **プラン** | `/plan` または `Shift+Tab`（モード切替） | コーディング前にステップバイステップの実装計画を作成する |
| **コードレビュー** | `/review` | ステージ済み/未ステージの変更を集中した実行可能なフィードバックでレビューする |
| **Init** | `/init` | プロジェクト設定ファイル（指示、エージェント）を生成する |
| **Explore** | *自動* | コードベースを探索・分析するよう Copilot に頼んだときに内部的に使用される |
| **Task** | *自動* | テスト、ビルド、リント、依存関係のインストールなどのコマンドを実行する |

<br>

**組み込みエージェントの動作例** - プラン、コードレビュー、Explore、Task の呼び出し例

```bash
copilot

# プランエージェントを呼び出して実装計画を作成する
> /plan Add input validation for book year in the book app

# コードレビューエージェントを変更に対して呼び出す
> /review

# Explore と Task エージェントは関連するときに自動的に呼び出される:
> Run the test suite        # Task エージェントを使用する

> Explore how book data is loaded    # Explore エージェントを使用する
```

Task エージェントについては？裏側で動作を管理・追跡し、明確でわかりやすい形式でレポートします。

| 結果 | 表示されるもの |
|---------|--------------|
| ✅ **成功** | 簡潔な概要（例:「All 247 tests passed」「Build succeeded」） |
| ❌ **失敗** | スタックトレース、コンパイラエラー、詳細なログを含む完全な出力 |


> 📚 **公式ドキュメント**: [GitHub Copilot CLI エージェント](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Copilot CLI にエージェントを追加する

ワークフローの一部として独自のエージェントを簡単に定義できます！一度定義すれば、指示するだけです！

<img src="../../../04-agents-custom-instructions/images/using-agents.png" alt="特化したエージェントの機能を表す異なるツールを持つ 4 体のカラフルな AI ロボット" width="800"/>

## 🗂️ エージェントを追加する

エージェントファイルは `.agent.md` 拡張子を持つ Markdown ファイルです。2 つの部分があります: YAML フロントマター（メタデータ）と Markdown 指示。

> 💡 **YAML フロントマターが初めてですか？** ファイルの先頭にある `---` マーカーで囲まれた設定の小さなブロックです。YAML は単なる `key: value` ペアです。ファイルの残りは通常の Markdown です。

最小限のエージェントの例:

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **必須対オプション**: `description` フィールドは必須です。`name`、`tools`、`model` などの他のフィールドはオプションです。

## エージェントファイルを置く場所

| 場所 | スコープ | 最適な用途 |
|----------|-------|----------|
| `.github/agents/` | プロジェクト固有 | プロジェクトの規約を共有するチーム向けエージェント |
| `~/.copilot/agents/` | グローバル（すべてのプロジェクト） | どこでも使う個人用エージェント |

**このプロジェクトには [.github/agents/](../../../.github/agents/) フォルダにサンプルエージェントファイルが含まれています**。独自に書くか、すでに提供されているものをカスタマイズできます。

<details>
<summary>📂 このコースのサンプルエージェントを見る</summary>

| ファイル | 説明 |
|------|-------------|
| `hello-world.agent.md` | 最小限の例 - ここから始める |
| `python-reviewer.agent.md` | Python コード品質レビュアー |
| `pytest-helper.agent.md` | pytest テスト専門家 |

```bash
# または個人エージェントフォルダにコピーする（すべてのプロジェクトで利用可能）
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

コミュニティエージェントは [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください

</details>


## 🚀 カスタムエージェントを使う 2 つの方法

### インタラクティブモード
インタラクティブモード内で、`/agent` を使ってエージェントをリストアップし、使用するエージェントを選択します。
エージェントを選択して会話を続けます。

```bash
copilot
> /agent
```

別のエージェントに切り替えるか、デフォルトモードに戻るには、再度 `/agent` コマンドを使います。

### プログラマティックモード

エージェントで直接新しいセッションを起動します。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **エージェントの切り替え**: `/agent` または `--agent` を再度使うことで、いつでも別のエージェントに切り替えられます。標準の Copilot CLI 体験に戻るには、`/agent` を使って**エージェントなし**を選択します。

---

# エージェントをさらに深く学ぶ

<img src="../../../04-agents-custom-instructions/images/creating-custom-agents.png" alt="コンポーネントとツールに囲まれた作業台でロボットが組み立てられており、カスタムエージェントの作成を表している" width="800"/>

> 💡 **このセクションはオプションです。** 組み込みエージェント（`/plan`、`/review`）はほとんどのワークフローに十分強力です。作業全体で一貫して適用される特化した専門知識が必要なときにカスタムエージェントを作成します。

以下の各トピックは独立しています。**興味のあるものを選んで - すべてを一度に読む必要はありません。**

| 目的... | ジャンプ先 |
|---|---|
| エージェントが汎用プロンプトより優れている理由を確認する | [専門家対汎用](#specialist-vs-generic-see-the-difference) |
| 機能でエージェントを組み合わせる | [複数エージェントで働く](#working-with-multiple-agents) |
| エージェントの整理、命名、共有 | [エージェントの整理と共有](#organizing--sharing-agents) |
| 常時オンのプロジェクトコンテキストを設定する | [Copilot のためのプロジェクト設定](#configuring-your-project-for-copilot) |
| YAML プロパティとツールを調べる | [エージェントファイルリファレンス](#agent-file-reference) |

以下のシナリオを選択して展開します。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>専門家対汎用: 違いを確認する</strong> - エージェントが汎用プロンプトより優れた出力を生成する理由</summary>

## 専門家対汎用: 違いを確認する

ここでエージェントがその価値を証明します。違いを見てみましょう。

### エージェントなし（汎用 Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
```

**汎用の出力**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基本的。動く。でも多くのものが欠けている。

---

### Python レビュアーエージェントで

```bash
copilot

> /agent
# "python-reviewer" を選択する

> Add a function to search books by year range in the book app
```

**専門家の出力**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewer エージェントが自動的に含めるもの**:
- ✅ すべてのパラメータと戻り値の型ヒント
- ✅ Args/Returns/Raises を含む包括的なドキュメント文字列
- ✅ 適切なエラーハンドリングを含む入力バリデーション
- ✅ より高いパフォーマンスのためのリスト内包表記
- ✅ エッジケースの処理（欠落/無効な年の値）
- ✅ PEP 8 準拠のフォーマット
- ✅ 防御的プログラミングの実践

**違い**: 同じプロンプトで、劇的に優れた出力。エージェントは尋ねるのを忘れていた専門知識をもたらします。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>複数エージェントで働く</strong> - 専門家の組み合わせ、セッション中の切り替え、ツールとしてのエージェント</summary>

## 複数エージェントで働く

本当の力は、専門家が機能について協力するときに発揮されます。

### 例: シンプルな機能を構築する

```bash
copilot

> I want to add a "search by year range" feature to the book app

# 設計に python-reviewer を使う
> /agent
# "python-reviewer" を選択する

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# テスト設計に pytest-helper に切り替える
> /agent
# "pytest-helper" を選択する

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# 両方の設計をまとめる
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**重要なポイント**: あなたが専門家を指示するアーキテクトです。彼らが詳細を処理し、あなたがビジョンを処理します。

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![Python レビュアーデモ](../../../04-agents-custom-instructions/images/python-reviewer-demo.gif)

*デモの出力は異なります - モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

### ツールとしてのエージェント

エージェントが設定されると、Copilot は複雑なタスク中にそれらをツールとして呼び出すこともできます。フルスタックの機能を求めると、Copilot は自動的に適切な専門エージェントに部分を委任することがあります。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>エージェントの整理と共有</strong> - 命名、ファイル配置、指示ファイル、チーム共有</summary>

## エージェントの整理と共有

### エージェントの命名

エージェントファイルを作成するとき、名前が重要です。それは `/agent` または `--agent` の後に入力するものであり、チームメートがエージェントリストで見るものです。

| ✅ 良い名前 | ❌ 避けるべき |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名規則:**
- ハイフン付き小文字を使う: `my-agent-name.agent.md`
- ドメインを含める: `frontend`、`backend`、`devops`、`security`
- 必要に応じて具体的にする: `react-typescript` vs 単に `frontend`

---

### チームと共有する

エージェントファイルを `.github/agents/` に置くとバージョン管理されます。リポジトリにプッシュすれば、すべてのチームメンバーが自動的に取得します。ただし、エージェントは Copilot がプロジェクトから読み込む 1 種類のファイルです。`/agent` を実行しなくても、すべてのセッションに自動的に適用される**指示ファイル**もサポートしています。

こう考えてください: エージェントは呼ぶ専門家で、指示ファイルは常に有効なチームルールです。

### ファイルを置く場所

2 つのメインの場所はすでに知っています（上記の[エージェントファイルを置く場所](#where-to-put-agent-files)を参照）。選択するためのディシジョンツリーです。

<img src="../../../04-agents-custom-instructions/images/agent-file-placement-decision-tree.png" alt="エージェントファイルを置く場所のディシジョンツリー: 実験中 → 現在のフォルダ、チームで使う → .github/agents/、どこでも → ~/.copilot/agents/" width="800"/>

**シンプルに始める:** プロジェクトフォルダに単一の `*.agent.md` ファイルを作成し、満足できたら恒久的な場所に移動します。

エージェントファイルの他にも、Copilot はプロジェクトレベルの**指示ファイル**を自動的に読み込みます（`/agent` は不要）。`AGENTS.md`、`.instructions.md`、`/init` については以下の[Copilot のためのプロジェクト設定](#configuring-your-project-for-copilot)を参照してください。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Copilot のためのプロジェクト設定</strong> - AGENTS.md、指示ファイル、/init セットアップ</summary>

## Copilot のためのプロジェクト設定

エージェントはオンデマンドで呼び出す専門家です。**プロジェクト設定ファイル**は異なります: Copilot はすべてのセッションで自動的に読み込んで、プロジェクトの規約、技術スタック、ルールを理解します。誰も `/agent` を実行する必要はありません; コンテキストはリポジトリで作業するすべての人に常に有効です。

### /init でのクイックセットアップ

始める最も早い方法は、Copilot に設定ファイルを生成させることです。

```bash
copilot
> /init
```

Copilot がプロジェクトをスキャンして、カスタマイズされた指示ファイルを作成します。後で編集できます。

### 指示ファイルフォーマット

| ファイル | スコープ | 注記 |
|------|-------|-------|
| `AGENTS.md` | プロジェクトルートまたはネスト | **クロスプラットフォーム標準** - Copilot と他の AI アシスタントで動作する |
| `.github/copilot-instructions.md` | プロジェクト | GitHub Copilot 固有 |
| `.github/instructions/*.instructions.md` | プロジェクト | 細かいトピック固有の指示 |
| `CLAUDE.md`、`GEMINI.md` | プロジェクトルート | 互換性のためにサポートされている |

> 🎯 **始めたばかりですか？** プロジェクトの指示には `AGENTS.md` を使いましょう。必要に応じて後で他のフォーマットを探索できます。

### AGENTS.md

`AGENTS.md` は推奨フォーマットです。Copilot と他の AI コーディングツールで機能する[オープン標準](https://agents.md/)です。リポジトリのルートに置くと Copilot が自動的に読み込みます。このプロジェクト自身の [AGENTS.md](../../../AGENTS.md) が動作例です。

典型的な `AGENTS.md` は、プロジェクトのコンテキスト、コードスタイル、セキュリティ要件、テスト標準を説明します。例のファイルのパターンに従って独自のものを書いてください。

### カスタム指示ファイル（.instructions.md）

より細かい制御を望むチームには、指示をトピック固有のファイルに分割しましょう。各ファイルが 1 つの関心事をカバーし、自動的に適用されます。

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **注意**: 指示ファイルはどの言語でも機能します。この例はコースプロジェクトに合わせて Python を使用していますが、チームが使用する TypeScript、Go、Rust、または他のテクノロジーに対して同様のファイルを作成できます。

**コミュニティ指示ファイルを見つける**: .NET、Angular、Azure、Python、Docker などの多くのテクノロジーをカバーするプリメイドの指示ファイルは [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

### カスタム指示を無効にする

Copilot にすべてのプロジェクト固有の設定を無視させる必要がある場合（デバッグや動作比較に便利）:

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>エージェントファイルリファレンス</strong> - YAML プロパティ、ツールエイリアス、完全な例</summary>

## エージェントファイルリファレンス

### より完全な例

上記で[最小限のエージェントフォーマット](#-add-your-agents)を見ました。`tools` プロパティを使ったより包括的なエージェントです。`~/.copilot/agents/python-reviewer.agent.md` を作成します:

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### YAML プロパティ

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | いいえ | 表示名（デフォルトはファイル名） |
| `description` | **はい** | エージェントが何をするか - Copilot がいつ提案するかを理解するのに役立つ |
| `tools` | いいえ | 許可されるツールのリスト（省略 = すべてのツールが利用可能）。以下のツールエイリアスを参照。 |
| `target` | いいえ | `vscode` または `github-copilot` のみに制限する |

### ツールエイリアス

`tools` リストでこれらの名前を使用します:
- `read` - ファイルの内容を読む
- `edit` - ファイルを編集する
- `search` - ファイルを検索する（grep/glob）
- `execute` - シェルコマンドを実行する（別名: `shell`、`Bash`）
- `agent` - 他のカスタムエージェントを呼び出す

> 📖 **公式ドキュメント**: [カスタムエージェントの設定](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Code のみ**: `model` プロパティ（AI モデルの選択用）は VS Code で動作しますが、GitHub Copilot CLI ではサポートされていません。クロスプラットフォームエージェントファイルのために安全に含めることができます。GitHub Copilot CLI はそれを無視します。

### その他のエージェントテンプレート

> 💡 **初心者向け注意**: 以下の例はテンプレートです。**特定のテクノロジーをプロジェクトが使うものに置き換えてください。** 重要なのはエージェントの*構造*であり、言及されている特定のテクノロジーではありません。

このプロジェクトには [.github/agents/](../../../.github/agents/) フォルダに動作例が含まれています:
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) - 最小限の例、ここから始める
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) - Python コード品質レビュアー
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) - pytest テスト専門家

コミュニティエージェントは [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>

---

# 練習

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

独自のエージェントを作成して動作を確認しましょう。

---

## ▶️ 自分で試してみよう

```bash

# エージェントディレクトリを作成する（存在しない場合）
mkdir -p .github/agents

# コードレビュアーエージェントを作成する
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# ドキュメントエージェントを作成する
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# 使ってみる
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# またはエージェントを切り替える
copilot
> /agent
# "documentor" を選択する
> Document @samples/book-app-project/books.py
```

---

## 📝 課題

### メインチャレンジ: 特化したエージェントチームを構築する

ハンズオン例は `reviewer` と `documentor` エージェントを作成しました。今度は異なるタスク、ブックアプリのデータバリデーションの改善のためにエージェントを作成・使用する練習をしましょう。

1. `.github/agents/` に配置した、エージェントごとに 1 ファイルの 3 つのエージェントファイル（`.agent.md`）を作成する
2. エージェント:
   - **data-validator**: `data.json` を欠落または不正なデータ（空の著者、year=0、欠落フィールド）でチェックする
   - **error-handler**: Python コードを一貫しないエラーハンドリングでレビューし、統一されたアプローチを提案する
   - **doc-writer**: ドキュメント文字列と README の内容を生成または更新する
3. ブックアプリで各エージェントを使う:
   - `data-validator` → `@samples/book-app-project/data.json` を監査する
   - `error-handler` → `@samples/book-app-project/books.py` と `@samples/book-app-project/utils.py` をレビューする
   - `doc-writer` → `@samples/book-app-project/books.py` にドキュメント文字列を追加する
4. コラボレーション: `error-handler` を使ってエラーハンドリングのギャップを特定し、`doc-writer` で改善されたアプローチをドキュメント化する

**成功基準**: 一貫した高品質の出力を生成する 3 つの動作するエージェントがあり、`/agent` で切り替えられます。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**: `.github/agents/` にエージェントごとに 1 ファイル作成します:

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**エージェントのテスト:**

> 💡 **注意:** このリポジトリのローカルコピーに `samples/book-app-project/data.json` がすでにあるはずです。なければ、ソースリポジトリからオリジナルバージョンをダウンロードしてください:
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# リストから "data-validator" を選択する
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**ヒント:** YAML フロントマターの `description` フィールドはエージェントが機能するために必須です。

</details>

### ボーナスチャレンジ: 指示ライブラリ

オンデマンドで呼び出すエージェントを構築しました。次はもう一方を試してみましょう: `/agent` なしで毎回のセッションで Copilot が自動的に読み込む**指示ファイル**。

`.github/instructions/` フォルダに少なくとも 3 つの指示ファイルを作成します:
- `python-style.instructions.md` - PEP 8 と型ヒントの規約を強制する
- `test-standards.instructions.md` - テストファイルの pytest 規約を強制する
- `data-quality.instructions.md` - JSON データエントリを検証する

ブックアプリのコードで各指示ファイルをテストしましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| エージェントフロントマターに `description` がない | エージェントが読み込まれないか発見できない | YAML フロントマターには常に `description:` を含める |
| エージェントのファイル場所が間違っている | 使おうとするとエージェントが見つからない | `~/.copilot/agents/`（個人用）または `.github/agents/`（プロジェクト）に置く |
| `.agent.md` の代わりに `.md` を使う | ファイルがエージェントとして認識されない可能性がある | `python-reviewer.agent.md` のようにファイルに名前を付ける |
| エージェントプロンプトが長すぎる | 30,000 文字の制限に達する可能性がある | エージェント定義を集中させ、詳細な指示にはスキルを使う |

### トラブルシューティング

**エージェントが見つからない** - 以下のいずれかの場所にエージェントファイルが存在することを確認する:
- `~/.copilot/agents/`
- `.github/agents/`

利用可能なエージェントをリストアップする:

```bash
copilot
> /agent
# 利用可能なすべてのエージェントを表示する
```

**エージェントが指示に従わない** - プロンプトをより明確にして、エージェントの定義に詳細を追加する:
- バージョン付きの特定のフレームワーク/ライブラリ
- チームの規約
- コードパターンの例

**カスタム指示が読み込まれない** - プロジェクトで `/init` を実行してプロジェクト固有の指示を設定する:

```bash
copilot
> /init
```

または無効になっているか確認する:
```bash
# 読み込みたい場合は --no-custom-instructions を使わない
copilot  # デフォルトでカスタム指示を読み込む
```

</details>

---

# まとめ

## 🔑 重要なポイント

1. **組み込みエージェント**: `/plan` と `/review` は直接呼び出す; Explore と Task は自動的に機能する
2. **カスタムエージェント**は `.agent.md` ファイルで定義された専門家である
3. **良いエージェント**は明確な専門知識、標準、出力フォーマットを持っている
4. **マルチエージェントのコラボレーション**は専門知識を組み合わせることで複雑な問題を解決する
5. **指示ファイル**（`.instructions.md`）はチーム標準を自動適用のためにコード化する
6. **一貫した出力**は適切に定義されたエージェント指示から生まれる

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次のステップ

エージェントは Copilot がコードに*どのようにアプローチして対象を絞ったアクションを取るか*を変えます。次は**スキル**について学びます - これは*どのステップ*に従うかを変えます。エージェントとスキルの違いが気になりますか？第 05 章でそれを正面から取り上げます。

**[第 05 章: スキルシステム](../05-skills/README.md)**では以下を学びます。

- スキルがプロンプトから自動的にトリガーされる方法（スラッシュコマンド不要）
- コミュニティスキルのインストール
- SKILL.md ファイルを使ったカスタムスキルの作成
- エージェント、スキル、MCP の違い
- それぞれをいつ使うか

---

**[← 第 03 章に戻る](../03-development-workflows/README.md)** | **[第 05 章に進む →](../05-skills/README.md)**
