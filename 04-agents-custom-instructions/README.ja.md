<!--
---
id: CopilotCLI-04
title: エージェントとカスタム指示
description: 指示とカスタムプロンプトのルールを設定して、専門的な AI エージェントを構成します。
audience: Developers / Students / Terminal users
slug: agents-and-custom-instructions
weight: 5
---
-->

![Chapter 04: Agents and Custom Instructions](assets/chapter-header.png)

[English Version](./README.md)

> **Python のコードレビュアー、テストの専門家、セキュリティのレビュアー……これらをすべて一つのツールで雇えるとしたらどうでしょうか？**

第03章では、コードレビュー、リファクタリング、デバッグ、テスト生成、Git 連携という必須のワークフローをマスターしました。これらだけでも GitHub Copilot CLI での生産性は飛躍的に向上します。ここからは、さらに一歩進んでみましょう。

これまでは、Copilot CLI を汎用的なアシスタントとして使ってきました。「エージェント」を使えば、特定の基準を持った「ペルソナ」を与えることができます。例えば、型ヒントや PEP 8 を遵守させるコードレビュアーや、pytest のケースを書くテストヘルパーなどです。ターゲットを絞った指示を持つエージェントが処理することで、同じプロンプトでも結果が目に見えて向上することを実感できるはずです。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- 組み込みエージェント（Plan (`/plan`)、Code-review (`/review`)）および自動エージェント（Explore、Task）の使用
- エージェントファイル (`.agent.md`) を使用した特化型エージェントの作成
- 特定ドメインのタスクへのエージェントの活用
- `/agent` コマンドや `--agent` フラグによるエージェントの切り替え
- プロジェクト固有の標準のためのカスタム指示ファイルの作成

> ⏱️ **推定所要時間**: 約55分（読みもの20分 ＋ 実践35分）

---

## 🧩 現実世界の例え：専門家の雇用

家に問題が起きたとき、単なる「何でも屋さん」は呼びません。専門家を呼びます：

| 問題 | 専門家 | 理由 |
|---------|------------|-----|
| 水漏れ | 配管工 | 配管の規約を知っており、専用の道具を持っている |
| 配線直し | 電気技師 | 安全要件を理解し、法規に準拠している |
| 屋根の修理 | 屋根職人 | 材料や地元の気候条件を熟知している |

エージェントも同じ仕組みです。汎用的な AI ではなく、特定のタスクに集中し、従うべき正しいプロセスを知っているエージェントを使いましょう。一度指示を設定すれば、コードレビュー、テスト、セキュリティ、ドキュメント作成など、その専門知識が必要なときにいつでも再利用できます。

<img src="assets/hiring-specialists-analogy.png" alt="専門家の雇用に例えると - 家の修理に専門職を呼ぶのと同じように、AIエージェントもコードレビュー、テスト、セキュリティ、ドキュメント作成などの特定のタスクに特化しています" width="800" />

---

# エージェントを使う

組み込みエージェントやカスタムエージェントをすぐに使い始めてみましょう。

---

## *エージェント初心者の方へ* まずはこちらから！
エージェントを使ったことも作ったこともありませんか？このコースを始めるために必要な知識はこれだけです。

1. **今すぐ *組み込み* エージェントを試す：**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   これは Plan エージェントを呼び出し、ステップバイステップの実装計画を作成させます。

2. **カスタムエージェントの例を見る：** エージェントの指示を定義するのは簡単です。用意されている [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) ファイルを見てパターンを確認してください。

3. **核心となる概念を理解する：** エージェントを使うのは、汎用的なアシスタントではなく専門家に相談するようなものです。「フロントエンド・エージェント」は、アクセシビリティやコンポーネントのパターンに自動的に注目します。エージェントの指示にすでに明記されているため、あなたがわざわざ思い出させる必要はありません。


## 組み込みエージェント

**第03章の「開発ワークフロー」ですでにいくつかの組み込みエージェントを使っています！**
<br>`/plan` と `/review` は、実は組み込みのエージェントなのです。舞台裏で何が起きているかがわかったところで、全リストを見てみましょう：

| エージェント | 呼び出し方 | 何をするか |
|-------|---------------|--------------|
| **Plan** | `/plan` または `Shift+Tab` | コーディング前にステップバイステップの実装計画を作成する |
| **Code-review** | `/review` | ステージング済み/未ステージングの変更をレビューし、実行可能なフィードバックを提供 |
| **Init** | `/init` | プロジェクト設定ファイル（指示、エージェント）を生成する |
| **Explore** | *自動実行* | コードベースの探索や分析を依頼したときに内部的に使用される |
| **Task** | *自動実行* | テスト、ビルド、リンター、依存関係のインストールなどのコマンドを実行する |

<br>

**組み込みエージェントの活用例** - Plan、Code-review、Explore、Task の呼び出し：

```bash
copilot

# Plan エージェントを呼び出して実装計画を作成
> /plan Add input validation for book year in the book app

# 変更内容に対して Code-review エージェントを実行
> /review

# Explore や Task エージェントは、必要に応じて自動的に呼び出されます：
> Run the test suite        # Task エージェントを使用

> Explore how book data is loaded    # Explore エージェントを使用
```

Task エージェントはどうでしょうか？これは舞台裏で何が起きているかを管理・追跡し、クリーンで明確な形式で報告します：

| 結果 | 表示内容 |
|---------|--------------|
| ✅ **成功** | 短い要約（例：「247個のテストすべてに合格」、「ビルド成功」） |
| ❌ **失敗** | スタックトレース、コンパイラエラー、詳細ログを含む完全な出力 |


> 📚 **公式ドキュメント**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)（英語）

---

# Copilot CLI にエージェントを追加する

自分自身のエージェントを定義してワークフローに組み込むことができます！一度定義すれば、あとは指示するだけです。

<img src="assets/using-agents.png" alt="4台のカラフルなAIロボット。それぞれが特化型エージェントの能力を表す異なる道具を持っている" width="800"/>

## 🗂️ エージェントを追加する

エージェントファイルは `.agent.md` という拡張子を持つ Markdown ファイルです。YAML フロントマター（メタデータ）と Markdown 形式の指示の2つの部分で構成されます。

> 💡 **YAML フロントマターとは？** ファイルの先頭にある `---` で囲まれた設定ブロックのことです。YAML は単純な `キー: 値` のペアです。それ以外の部分は通常の Markdown です。

最小限のエージェントの例：

```markdown
---
name: my-reviewer
description: バグやセキュリティ問題に焦点を当てたコードレビュアー
---

# コードレビュアー

あなたはバグやセキュリティ問題の発見に特化したコードレビュアーです。

コードをレビューする際は、常に以下の点を確認してください：
- SQL インジェクションの脆弱性
- エラーハンドリングの欠如
- ハードコードされたシークレット
```

> 💡 **必須とオプション**: `description` フィールドは必須です。`name`、`tools`、`model` などの他のフィールドはオプションです。

## エージェントファイルの置き場所

| 場所 | 範囲 | 最適な用途 |
|----------|-------|----------|
| `.github/agents/` | プロジェクト固有 | プロジェクトの規約をチームで共有するエージェント |
| `~/.copilot/agents/` | グローバル（全プロジェクト） | どこでも使う自分専用のエージェント |

**このプロジェクトには、[.github/agents/](../.github/agents/) フォルダにサンプルのエージェントファイルが含まれています。** これらを自分で書いたり、カスタマイズしたりできます。

<details>
<summary>📂 このコースに含まれるサンプルエージェントを見る</summary>

| ファイル | 説明 |
|------|-------------|
| `hello-world.agent.md` | 最小限の例 - まずはこちらから |
| `python-reviewer.agent.md` | Python コード品質レビュアー |
| `pytest-helper.agent.md` | Pytest テスト専門家 |

```bash
# いずれかを個人用エージェントフォルダにコピー（すべてのプロジェクトで利用可能になります）
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

その他のコミュニティ製エージェントについては、[github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>


## 🚀 カスタムエージェントを使う2つの方法

### 対話型（Interactive）モード
対話型モード内で `/agent` と入力してエージェントを一覧表示し、使用したいエージェントを選択します。選択したエージェントとの会話が続きます。

```bash
copilot
> /agent
```

別のエージェントに変更したり、デフォルトモードに戻ったりするには、再度 `/agent` コマンドを使用します。

### プログラム（Programmatic）モード

最初からエージェントを指定してセッションを開始します。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **エージェントの切り替え**: `/agent` や `--agent` を再度使用することで、いつでも別のエージェントに切り替えることができます。標準の Copilot CLI 体験に戻るには、`/agent` を使い、**no agent** を選択してください。

---

# エージェントをさらに使いこなす

<img src="assets/creating-custom-agents.png" alt="作業台で組み立てられているロボット。カスタムエージェント作成を表す部品や道具に囲まれている" width="800"/>

> 💡 **このセクションはオプションです。** ほとんどのワークフローには、組み込みエージェント (`/plan`, `/review`) で十分です。カスタムエージェントは、作業全体で一貫して適用したい特定の専門知識が必要な場合に作成してください。

以下の各トピックは独立しています。**興味のあるものを選んでください。一度にすべて読む必要はありません。**

| やりたいこと | リンク |
|---|---|
| エージェントが汎用プロンプトより優れている理由を見る | [専門家 vs 汎用アシスタント](#specialist-vs-generic-see-the-difference) |
| 一つの機能に対してエージェントを組み合わせる | [複数のエージェントとの作業](#working-with-multiple-agents) |
| エージェントの整理、命名、共有 | [エージェントの整理と共有](#organizing--sharing-agents) |
| 常に有効なプロジェクトコンテキストを設定する | [プロジェクトの Copilot 設定](#configuring-your-project-for-copilot) |
| YAML プロパティとツールのリファレンス | [エージェントファイル・リファレンス](#agent-file-reference) |

詳細を見るには、以下のシナリオを選択して展開してください。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>専門家 vs 汎用アシスタント：違いを見る</strong> - エージェントが汎用プロンプトよりも優れた出力を生成する理由</summary>

## 専門家 vs 汎用アシスタント：違いを見る

ここでエージェントの価値が証明されます。この違いに注目してください：

### エージェントなし（通常の Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
```
（書籍アプリに、出版年の範囲で本を検索する関数を追加して）

**汎用アシスタントの出力例**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基本的です。動きます。しかし、多くのことが欠けています。

---

### Python Reviewer エージェントを使用

```bash
copilot

> /agent
# "python-reviewer" を選択

> Add a function to search books by year range in the book app
```

**専門家の出力例**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    指定された出版年の範囲内の本を検索します。

    Args:
        books: 書籍情報の辞書のリスト
        start_year: 開始年（この年を含む）
        end_year: 終了年（この年を含む）

    Returns:
        出版年が範囲内にある本のリスト

    Raises:
        ValueError: 開始年が終了年より大きい場合
        TypeError: 年の値が整数でない場合
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("出版年の値は整数である必要があります")

    if start_year > end_year:
        raise ValueError(f"開始年 ({start_year}) は終了年 ({end_year}) より大きくすることはできません")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewer エージェントが自動的に含めたもの**:
- ✅ すべてのパラメータと戻り値に対する型ヒント
- ✅ Args/Returns/Raises を含む包括的な docstring
- ✅ 適切なエラーハンドリングを伴う入力バリデーション
- ✅ パフォーマンス向上のためのリスト内包表記
- ✅ エッジケースの処理（年の値が欠落している、無効である等）
- ✅ PEP 8 準拠のフォーマット
- ✅ 防御的プログラミングの実践

**違い**: プロンプトは同じですが、出力は劇的に向上しています。エージェントは、あなたが聞き忘れてしまうような専門知識を自動的に補ってくれます。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>複数のエージェントとの作業</strong> - 専門家の組み合わせ、セッション途中での切り替え、ツールとしてのエージェント</summary>

## 複数のエージェントとの作業

本当の力は、専門家たちが一つの機能に対して協力するときに発揮されます。

### 例：シンプルな機能の構築

```bash
copilot

> I want to add a "search by year range" feature to the book app

# 設計には python-reviewer を使う
> /agent
# "python-reviewer" を選択

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# テスト設計には pytest-helper に切り替える
> /agent
# "pytest-helper" を選択

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# 両方の設計を統合する
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**重要な洞察**: あなたは専門家たちを指揮する建築家（アーキテクト）です。彼らが詳細を担当し、あなたはビジョンを担当します。

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Python Reviewer Demo](assets/python-reviewer-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

### ツールとしてのエージェント

エージェントが設定されていると、Copilot は複雑なタスクの最中にそれらを「ツール」として呼び出すこともできます。フルスタックの機能を依頼した場合、Copilot は自動的に適切な専門エージェントに一部の作業を委託することがあります。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>エージェントの整理と共有</strong> - 命名、ファイルの配置、指示ファイル、チーム共有</summary>

## エージェントの整理と共有

### エージェントの命名

エージェントファイルを作成する際、名前は重要です。それは `/agent` や `--agent` の後に入力する名前であり、チームメイトがエージェントリストで目にする名前でもあります。

| ✅ 良い名前 | ❌ 避けるべき名前 |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名規則:**
- 小文字とハイフンを使用する: `my-agent-name.agent.md`
- ドメイン（領域）を含める: `frontend`, `backend`, `devops`, `security`
- 必要に応じて具体的にする: 単なる `frontend` よりも `react-typescript`

---

### チームとの共有

エージェントファイルを `.github/agents/` に置けば、バージョン管理の対象となります。リポジトリにプッシュすれば、チームメンバー全員が自動的にそれらを利用できるようになります。しかし、エージェントは Copilot がプロジェクトから読み取るファイルの一種に過ぎません。Copilot は、誰かが `/agent` を実行しなくても、すべてのセッションに自動的に適用される **指示ファイル（instruction files）** もサポートしています。

このように考えてください：エージェントは必要に応じて呼び出す専門家であり、指示ファイルは常に有効なチームのルールです。

### ファイルの置き場所

すでに2つの主要な場所を知っています（上記の「エージェントファイルの置き場所」を参照）。選択にはこの意思決定ツリーを使用してください：

<img src="assets/agent-file-placement-decision-tree.png" alt="エージェントファイルの置き場所の決定ツリー：実験中ならカレントフォルダ、チームで使用するなら .github/agents/、どこでも使うなら ~/.copilot/agents/" width="800"/>

**まずはシンプルに:** プロジェクトフォルダに `*.agent.md` ファイルを一つ作成してみましょう。気に入ったら、恒久的な場所に移動させてください。

エージェントファイル以外にも、Copilot は **プロジェクトレベルの指示ファイル** を自動的に読み取ります（`/agent` は不要）。詳細は以下の「プロジェクトの Copilot 設定」にある `AGENTS.md`、`.instructions.md`、`/init` を参照してください。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>プロジェクトの Copilot 設定</strong> - AGENTS.md、指示ファイル、/init によるセットアップ</summary>

## プロジェクトの Copilot 設定

エージェントはオンデマンドで呼び出す専門家です。**プロジェクト設定ファイル**は異なります。Copilot はこれらをすべてのセッションで自動的に読み込み、プロジェクトの規約、技術スタック、ルールを理解します。誰かが `/agent` を実行する必要はありません。リポジトリで作業する全員に対して、その文脈（コンテキスト）が常に有効になります。

### /init によるクイックセットアップ

最も簡単な開始方法は、Copilot に設定ファイルを生成させることです：

```bash
copilot
> /init
```

Copilot がプロジェクトをスキャンし、カスタマイズされた指示ファイルを生成します。その後、必要に応じて編集できます。

### 指示ファイルの形式

| ファイル | 範囲 | 補足 |
|------|-------|-------|
| `AGENTS.md` | プロジェクトルートまたはネスト | **クロスプラットフォーム標準** - Copilot 以外の AI アシスタントでも動作します |
| `.github/copilot-instructions.md` | プロジェクト | GitHub Copilot 専用 |
| `.github/instructions/*.instructions.md` | プロジェクト | きめ細かなトピック別の指示 |
| `CLAUDE.md`, `GEMINI.md` | プロジェクトルート | 互換性のためにサポートされています |

> 🎯 **始めたばかりですか？** プロジェクトの指示には `AGENTS.md` を使ってください。他の形式は必要に応じて後で試せます。

### AGENTS.md

`AGENTS.md` は推奨される形式です。これは Copilot や他の AI コーディングツールで共通して動作する [オープン標準](https://agents.md/) です。リポジトリのルートに置くと、Copilot が自動的に読み取ります。このプロジェクト自身の [AGENTS.md](../AGENTS.md) が動作する例となっています。

一般的な `AGENTS.md` には、プロジェクトの文脈、コードスタイル、セキュリティ要件、テスト標準などが記載されます。サンプルのパターンに従って自分で作成してください。

### カスタム指示ファイル (.instructions.md)

より細かく制御したいチームは、トピック別のファイルに指示を分けることができます。各ファイルが一つの懸念事項をカバーし、自動的に適用されます：

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **注意**: 指示ファイルはどの言語でも動作します。この例ではコースに合わせて Python を使っていますが、TypeScript, Go, Rust など、チームが使用するあらゆる技術に対して同様のファイルを作成できます。

#### `applyTo` を使用した指示の適用範囲の限定

デフォルトでは、指示ファイルはすべての会話に適用されます。特定のファイルタイプのみに制限するには、ファイルの最上部（`---` マーカーで囲まれたブロック）の YAML フロントマターに `applyTo` フィールドを追加します：

```markdown
---
applyTo: "**/*.py"
---
# Python の標準
常に PEP 8 スタイル規約に従ってください。
すべての関数シグネチャで型ヒントを使用してください。
```

`applyTo: "**/*.py"` を指定すると、Copilot は Python ファイルを扱っているときのみ、その指示ファイルをロードします。これにより、例えば Dockerfile や SQL クエリに関する会話の際に、Python スタイルに関する無関係な指示が会話を邪魔する（コンテキストを圧迫する）のを防ぐことができます。

一般的なパターンは以下の通りです：

| `applyTo` の値 | 適用されるタイミング |
|---|---|
| `"**/*.py"` | すべての Python ファイル |
| `"**/*.{ts,tsx}"` | TypeScript および TSX ファイル |
| `"tests/**"` | `tests/` フォルダ内のすべてのファイル |
| （フロントマターなし） | すべての会話 — デフォルト設定 |

> 💡 **ヒント**: すべてのオペレーティングシステムやシェルで正しく解釈されるように、グロブパターンは引用符で囲んでください（例: `"**/*.py"`）。

**コミュニティ製指示ファイルを探す**: [github/awesome-copilot](https://github.com/github/awesome-copilot) では、.NET, Angular, Azure, Python, Docker など、多くの技術をカバーする既成の指示ファイルをブラウズできます。

### カスタム指示の無効化

デバッグや動作比較のために、プロジェクト固有の設定をすべて無視させたい場合：

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>エージェントファイル・リファレンス</strong> - YAML プロパティ、ツールエイリアス、完全な例</summary>

## エージェントファイル・リファレンス

### より完全な例

これまでに[最小限の形式](#エージェントを追加する)を見てきました。ここでは `tools` プロパティを使用した、より包括的なエージェントの例を示します。`~/.copilot/agents/python-reviewer.agent.md` を作成してみてください：

```markdown
---
name: python-reviewer
description: Python プロジェクトのレビューに特化した Python コード品質の専門家
tools: ["read", "edit", "search", "execute"]
---

# Python コードレビュアー

あなたはコードの品質とベストプラクティスに焦点を当てた Python の専門家です。

**重点分野：**
- コード品質 (PEP 8, 型ヒント, docstrings)
- パフォーマンス最適化 (リスト内包表記, ジェネレータ)
- エラーハンドリング (適切な例外処理)
- 保守性 (DRY 原則, 明確な命名)

**コードスタイルの要件：**
- Python 3.10+ の機能を使用 (dataclasses, type hints, pattern matching)
- PEP 8 の命名規則に従う
- ファイルの入出力にはコンテキストマネージャを使用する
- すべての関数に型ヒントと docstring を付ける

**レビュー時の必須チェック項目：**
- 関数シグネチャの型ヒントの欠如
- ミュータブル（変更可能）なデフォルト引数
- 適切なエラーハンドリング (bare except は禁止)
- 入力バリデーションの網羅性
```

### YAML プロパティ

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | いいえ | 表示名（デフォルトはファイル名） |
| `description` | **はい** | エージェントの役割。Copilot がいつ提案すべきかを判断するのに役立ちます。 |
| `tools` | いいえ | 許可されるツールのリスト（省略した場合はすべてのツールが使用可能）。以下のツールエイリアスを参照。 |
| `target` | いいえ | `vscode` または `github-copilot` のみに制限する |

### ツールエイリアス

`tools` リストで使用できる名前：
- `read` - ファイル内容の読み取り
- `edit` - ファイルの編集
- `search` - ファイルの検索 (grep/glob)
- `execute` - シェルコマンドの実行（`shell`, `Bash` も可）
- `agent` - 他のカスタムエージェントの呼び出し

> 📖 **公式ドキュメント**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)（英語）
>
> ⚠️ **VS Code 専用**: `model` プロパティ（AI モデルの選択）は VS Code では動作しますが、GitHub Copilot CLI ではサポートされていません。クロスプラットフォームでエージェントファイルを使う場合は含めても問題ありません。GitHub Copilot CLI はそれを無視します。

### エージェントのテンプレート

> 💡 **初心者の方への注意**: 以下の例はテンプレートです。**ご自身のプロジェクトで使用している技術に合わせて書き換えてください。** 重要なのは、特定の技術ではなく「エージェントの構造」です。

このプロジェクトの [.github/agents/](../.github/agents/) フォルダに動作する例が含まれています：
- [hello-world.agent.md](../.github/agents/hello-world.agent.md) - 最小限の例、まずはここから
- [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) - Python コード品質レビュアー
- [pytest-helper.agent.md](../.github/agents/pytest-helper.agent.md) - Pytest テスト専門家

その他のエージェントについては、[github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>

---

# 練習

<img src="../assets/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

自分自身のエージェントを作成し、動作を確認してみましょう。

---

## ▶️ 自分で試してみる

```bash

# エージェント用ディレクトリを作成（まだの場合）
mkdir -p .github/agents

# コードレビュアー・エージェントを作成
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: セキュリティとベストプラクティスに焦点を当てたシニアコードレビュアー
---

# コードレビュアー・エージェント

あなたはコードの品質に焦点を当てたシニアコードレビュアーです。

**レビューの優先順位：**
1. セキュリティの脆弱性
2. パフォーマンスの問題
3. 保守性に関する懸念
4. ベストプラクティスの違反

**出力形式：**
問題点を、以下の重要度タグを付けた番号付きリストで提供してください：
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# ドキュメント作成エージェントを作成
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: 明確で完全なドキュメントを作成するテクニカルライター
---

# ドキュメント作成エージェント

あなたは明確なドキュメントを作成するテクニカルライターです。

**ドキュメント標準：**
- 1文の要約から始める
- 使用例を含める
- パラメータと戻り値を記述する
- 注意点や制限事項を記す
EOF

# 使ってみる
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# エージェントを切り替える
copilot
> /agent
# "documentor" を選択
> Document @samples/book-app-project/books.py
```

---

## 📝 課題

### メインチャレンジ：特化型エージェントチームの構築

ハンズオンでは `reviewer` と `documentor` エージェントを作成しました。今度は別のタスク、つまり書籍アプリのデータバリデーションを改善するために、エージェントを作成して使ってみましょう：

1. 書籍アプリ向けにカスタマイズされた3つのエージェントファイル (`.agent.md`) を作成し、`.github/agents/` に配置してください。
2. 作成するエージェント：
   - **data-validator**: `data.json` をスキャンし、データの欠落や不正（空の著者、出版年が 0、フィールドの欠落など）をチェックします。
   - **error-handler**: Python コードをレビューし、エラーハンドリングの不整合を指摘して、統一された手法を提案します。
   - **doc-writer**: docstring や README の内容を生成・更新します。
3. 各エージェントを書籍アプリに対して使用してください：
   - `data-validator` → `@samples/book-app-project/data.json` を監査する
   - `error-handler` → `@samples/book-app-project/books.py` と `@samples/book-app-project/utils.py` をレビューする
   - `doc-writer` → `@samples/book-app-project/books.py` に docstring を追加する
4. 連携させる：`error-handler` でエラーハンドリングの不備を特定し、その後 `doc-writer` で改善されたアプローチをドキュメント化させます。

**成功基準**: 3つの動作するエージェントがあり、それぞれが一貫した高品質な出力を生成し、`/agent` でそれらを切り替えられること。

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**テンプレート**: `.github/agents/` に各エージェント用のファイルを作成します：

`data-validator.agent.md`:
```markdown
---
description: JSON データファイルをスキャンし、データの欠落や不正を分析します
---

あなたは JSON データファイルを分析し、データの欠落や不正をチェックします。

**重点分野：**
- 著者フィールドの空欄や欠落
- 無効な年（0年、未来の年、負の数）
- 必須フィールド（title, author, year, read）の欠落
- 重複するエントリ
```

`error-handler.agent.md`:
```markdown
---
description: Python コードのエラーハンドリングの一貫性をレビューします
---

あなたは Python コードのエラーハンドリングの一貫性をレビューします。

**標準：**
- bare except 句は使用しない
- 適宜カスタム例外を使用する
- すべてのファイル操作でコンテキストマネージャを使用する
- 成功/失敗に対して一貫した戻り値の型を使う
```

`doc-writer.agent.md`:
```markdown
---
description: 明確な Python ドキュメントを作成するテクニカルライター
---

あなたは明確な Python ドキュメントを作成するテクニカルライターです。

**標準：**
- Google スタイルの docstring
- パラメータの型と戻り値を含める
- 公開メソッドには使用例を追加する
- 発生する可能性のある例外を記す
```

**エージェントをテストする：**

> 💡 **補足:** ローカルに `samples/book-app-project/data.json` があるはずです。もしない場合は、元のリポジトリからダウンロードしてください：
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# リストから "data-validator" を選択
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**ヒント:** YAML フロントマターの `description` フィールドは、エージェントを動作させるために必須です。

</details>

### ボーナスチャレンジ：指示ライブラリ

オンデマンドで呼び出すエージェントを作成しました。今度は反対に、`/agent` を実行しなくてもすべてのセッションで Copilot が自動的に読み取る **指示ファイル（instruction files）** を試してみましょう。

`.github/instructions/` フォルダを作成し、少なくとも3つの指示ファイルを作成してください：
- `python-style.instructions.md`: PEP 8 と型ヒントの規約を遵守させるため
- `test-standards.instructions.md`: テストファイルで pytest の規約を遵守させるため
- `data-quality.instructions.md`: JSON データエントリをバリデーションするため

各指示ファイルを書籍アプリのコードでテストしてみてください。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong> (クリックして展開)</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| フロントマターに `description` がない | エージェントがロードされない、または見つからない | 常に YAML フロントマターに `description:` を含めてください |
| ファイルの置き場所が間違っている | 使用しようとしてもエージェントが見つからない | `~/.copilot/agents/` (個人用) または `.github/agents/` (プロジェクト用) に置いてください |
| 拡張子が `.md` になっている（`.agent.md` ではない） | エージェントとして認識されない可能性があります | `python-reviewer.agent.md` のような名前にしてください |
| エージェントの指示が長すぎる | 30,000 文字の制限に達する可能性があります | 指示は焦点を絞り、詳細な内容は「スキル」を併用してください |

### トラブルシューティング

**エージェントが見つからない** - 以下のいずれかの場所にエージェントファイルがあるか確認してください：
- `~/.copilot/agents/`
- `.github/agents/`

利用可能なエージェントの一覧を表示：

```bash
copilot
> /agent
# すべての利用可能なエージェントが表示されます
```

**エージェントが指示に従わない** - プロンプトで明示的に指示し、エージェントの定義に詳細を追加してください：
- バージョンを含む特定のフレームワーク/ライブラリ
- チームの規約
- コードパターンの例

**カスタム指示がロードされない** - プロジェクト内で `/init` を実行し、プロジェクト固有の指示をセットアップしてください：

```bash
copilot
> /init
```

または、無効化されていないか確認してください：
```bash
# ロードしたい場合は --no-custom-instructions を使わないでください
copilot  # デフォルトでカスタム指示をロードします
```

</details>

---

# まとめ

## 🔑 重要なポイント

1. **組み込みエージェント**: `/plan` と `/review` は直接呼び出し、Explore と Task は自動的に動作します。
2. **カスタムエージェント**は `.agent.md` ファイルで定義される専門家です。
3. **優れたエージェント**は、明確な専門分野、基準、出力形式を持っています。
4. **マルチエージェント連携**は、専門知識を組み合わせることで複雑な問題を解決します。
5. **指示ファイル** (`.instructions.md`) は、自動的に適用されるチーム標準を定義します。
6. **一貫した出力**は、明確に定義されたエージェントの指示によって得られます。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## ➡️ 次は？

エージェントは、Copilot がコードに対してどのように考え、的を絞ったアクションを取るかを変えるものでした。次は、どのような手順でタスクをこなすかを変える **スキル（Skills）** について学びます。エージェントとスキルの違いは何でしょうか？第05章でその疑問に正面から答えます。

**[第05章：スキルシステム](../05-skills/README.ja.md)** では以下を学びます：

- プロンプトからスキルが自動的にトリガーされる仕組み（スラッシュコマンド不要）
- コミュニティ製スキルのインストール
- `SKILL.md` ファイルによるカスタムスキルの作成
- エージェント、スキル、MCP の違い
- それぞれの使い分け

---

**[← 第03章に戻る](../03-development-workflows/README.ja.md)** | **[第05章へ進む →](../05-skills/README.ja.md)**
