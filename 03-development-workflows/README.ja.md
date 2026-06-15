<!--
---
id: CopilotCLI-03
title: 開発ワークフロー
description: CLIによる支援を活用した Git 操作、コードのリファクタリング、テスト作成、デバッグによって、開発を合理化します。
audience: Developers / Students / Terminal users
slug: development-workflows
weight: 4
---
-->

![Chapter 03: Development Workflows](assets/chapter-header.png)

[English Version](./README.md)

> **もし AI が、あなたが気づかなかったバグを見つけることができたらどうでしょうか？**

この章では、GitHub Copilot CLI を日々の開発のメインツールとして活用していきます。テスト、リファクタリング、デバッグ、Git など、毎日行うワークフローの中で Copilot CLI を使いこなせるようになりましょう。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- Copilot CLI を使って包括的なコードレビューを実行する
- レガシーコードを安全にリファクタリングする
- AI の支援を受けて問題をデバッグする
- テストを自動生成する
- Copilot CLI を git ワークフローに統合する

> ⏱️ **推定所要時間**: 約60分（読みもの15分 ＋ 実践45分）

---

## 🧩 現実世界の例え：大工のワークフロー

大工はただ道具の使い方を知っているだけでなく、仕事の種類に応じた *ワークフロー* を持っています：

<img src="assets/carpenter-workflow-steps.png" alt="職人の作業場。3つのワークフローレーンが表示されている：家具の製作（計測、切断、組み立て、仕上げ）、損傷の修復（評価、取り外し、修理、調整）、品質チェック（検査、接合部のテスト、アライメントの確認）" width="800"/>

同様に、開発者にもタスクに応じたワークフローがあります。GitHub Copilot CLI は、それぞれのワークフローを強化し、日々のコーディングタスクをより効率的かつ効果的なものにします。

---

# 5つのワークフロー

<img src="assets/five-workflows.png" alt="コードレビュー、テスト、デバッグ、リファクタリング、git 連携のワークフローを表す5つの光るネオンアイコン" width="800"/>

以下の各ワークフローは独立しています。現在のニーズに合ったものを選ぶか、すべて順に試してみてください。

---

## 自分の進め方を選ぶ

この章では、開発者が一般的に使用する5つのワークフローを扱います。**しかし、一度にすべてを読む必要はありません！** 各ワークフローは、以下の折りたたみセクションにまとめられています。あなたのプロジェクトに最も適したもの、あるいは今必要なものを選んでください。いつでも戻って他のワークフローを探索できます。

<img src="assets/five-workflows-swimlane.png" alt="5つの開発ワークフロー：コードレビュー、リファクタリング、デバッグ、テスト生成、Git 連携が水平なレーンとして表示されている" width="800"/>

| やりたいこと | リンク |
|---|---|
| マージ前にコードをレビューする | [ワークフロー 1: コードレビュー](#workflow-1-code-review) |
| 散らかったコードやレガシーコードを整理する | [ワークフロー 2: リファクタリング](#workflow-2-refactoring) |
| バグを追跡して修正する | [ワークフロー 3: デバッグ](#workflow-3-debugging) |
| コードのテストを生成する | [ワークフロー 4: テスト生成](#workflow-4-test-generation) |
| より良いコミットメッセージや PR を書く | [ワークフロー 5: Git 連携](#workflow-5-git-integration) |
| コーディング前に調査する | [クイックヒント：計画や実装の前に調査する](#quick-tip-research-before-you-plan-or-code) |
| バグ修正ワークフローを最初から最後まで見る | [まとめ：バグ修正ワークフロー](#putting-it-together-bug-fix-workflow) |

**以下のワークフローを選択して展開**し、GitHub Copilot CLI が各分野の開発プロセスをどのように強化できるかを確認してください。

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>ワークフロー 1: コードレビュー</strong> - ファイルのレビュー、/review エージェントの使用、重要度別のチェックリスト作成</summary>

<img src="assets/code-review-swimlane-single.png" alt="コードレビューのワークフロー：レビュー、問題の特定、優先順位付け、チェックリストの生成。" width="800"/>

### 基本的なレビュー

`@` 記号を使ってファイルを参照し、Copilot CLI にその内容を直接レビューさせます。

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Code Review Demo](assets/code-review-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

### 入力バリデーションのレビュー

プロンプトに関心の対象をリストアップすることで、特定の懸念事項（ここでは入力バリデーション）に焦点を当てたレビューを依頼できます。

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```

### プロジェクト全体のクロスファイルレビュー

ディレクトリ全体を `@` で参照することで、プロジェクト内のすべてのファイルを一度にスキャンさせることができます。

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### 対話型コードレビュー

複数回のやり取りを使って、より深く掘り下げます。まず広範なレビューから始め、セッションを中断せずに追加の質問をします。

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI が詳細なレビューを提供します

> The user input handling - are there any edge cases I'm missing?
（ユーザー入力の処理について、見落としているエッジケースはある？）

# Copilot CLI が空文字列や特殊文字に関する潜在的な問題を指摘します

> Create a checklist of all issues found, prioritized by severity
（見つかったすべての問題のチェックリストを、重要度順に作成して）

# Copilot CLI が優先順位付けされたアクション項目を生成します
```

### レビューチェックリストのテンプレート

特定の形式（ここでは Issue に貼り付けられる重要度別の Markdown チェックリスト）で出力を指定します。

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Git の変更を理解する (/review に重要)

`/review` コマンドを使う前に、git における2種類の変更を理解しておく必要があります：

| 変更の種類 | 意味 | 確認方法 |
|-------------|---------------|------------|
| **ステージング済み (Staged)** | `git add` で次のコミット用にマークされたファイル | `git diff --staged` |
| **未ステージング (Unstaged)** | 変更したけれど、まだ `git add` していないファイル | `git diff` |

```bash
# クイックリファレンス
git status           # 両方の状態を表示
git add file.py      # ファイルをコミット用にステージング
git diff             # 未ステージングの変更を表示
git diff --staged    # ステージング済みの変更を表示
```

### /review コマンドの使用

`/review` コマンドは、組み込みの **code-review エージェント**を呼び出します。これは、ステージング済みおよび未ステージングの変更を分析し、ノイズの少ない有益な出力を出すように最適化されています。自由なプロンプトを書く代わりに、スラッシュコマンドを使って専用の組み込みエージェントを起動しましょう。

```bash
copilot

> /review
# ステージング済み/未ステージングの変更に対してコードレビューエージェントを実行
# 焦点を絞った、実行可能なフィードバックを提供

> /review Check for security issues in authentication
# 特定の重点分野を指定してレビューを実行
```

> 💡 **ヒント**: コードレビューエージェントは、保留中の変更があるときに最も効果的に機能します。より的を絞ったレビューのために、`git add` でファイルをステージングしてから実行してください。

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>ワークフロー 2: リファクタリング</strong> - コードの再構成、関心の分離、エラーハンドリングの改善</summary>

<img src="assets/refactoring-swimlane-single.png" alt="リファクタリングのワークフロー：コードの評価、変更の計画、実装、動作の検証。" width="800"/>

### シンプルなリファクタリング

> **まずはこれを試して:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

まずは単純な改善から始めましょう。書籍アプリでこれらを試してみてください。各プロンプトでは、`@` によるファイル参照と具体的なリファクタリング指示を組み合わせることで、Copilot CLI が何をどこに変更すべきかを正確に把握できるようにします。

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **リファクタリングが初めてですか？** 複雑な変換に取り組む前に、型ヒントの追加や変数名の改善といった簡単な依頼から始めてみてください。

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Refactor Demo](assets/refactor-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

### 関心の分離 (Separation of Concerns)

一つのプロンプトで複数のファイルを `@` で参照すると、Copilot CLI はリファクタリングの一環としてファイル間でコードを移動させることができます。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### エラーハンドリングの改善

関連する2つのファイルを提供し、横断的な懸念事項を説明することで、Copilot CLI は両方のファイルに対して一貫した修正を提案できます。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### ドキュメントの追加

詳細な箇条書きを使って、各 docstring に含めるべき内容を正確に指定します。

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### テストを活用した安全なリファクタリング

複数回のやり取りで、関連する2つのリクエストを繋げます。まずテストを生成し、そのテストを安全網としてリファクタリングを行います。

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# まずテストを入手

> Now refactor the BookCollection class to use a context manager for file operations

# 自信を持ってリファクタリング - テストが動作の維持を検証します
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>ワークフロー 3: デバッグ</strong> - バグの追跡、セキュリティ監査、ファイル間を跨いだ問題の追跡</summary>

<img src="assets/debugging-swimlane-single.png" alt="デバッグのワークフロー：エラーの理解、根本原因の特定、修正、テスト。" width="800"/>

### シンプルなデバッグ

> **まずはこれを試して:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

まずは何が問題なのかを説明することから始めます。バグのある書籍アプリで試せる、一般的なデバッグパターンを以下に示します。各プロンプトでは、`@` ファイル参照と明確な症状の説明を組み合わせることで、Copilot CLI がバグの場所を特定し、診断できるようにします。

```bash
copilot

# パターン：「期待値は X ですが、実際の結果は Y です」
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# パターン：「予期しない動作」
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# パターン：「間違った結果」
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **デバッグのヒント**: *症状*（何が起きているか）と *期待値*（どうなるべきか）を説明してください。Copilot CLI が残りの部分を解明します。

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Fix Bug Demo](assets/fix-bug-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

### 「バグ探偵」 - AI が関連するバグを見つける

ここでコンテキストを意識したデバッグが威力を発揮します。バグのある書籍アプリで、ファイル全体を `@` で提供し、ユーザーから報告された症状のみを伝えてください。Copilot CLI は根本原因を突き止め、近くにある追加のバグも見つけてくれるかもしれません。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI が行うこと**:
```
根本原因：80行目で、部分一致 (in) ではなく完全一致 (==) を使用しています。

80行目: return [b for b in self.books if b.author == author]

find_by_author 関数は完全一致を必要とします。そのため "Tolkien" で検索しても
"J.R.R. Tolkien" の本は見つかりません。

修正案：大文字・小文字を区別しない部分一致に変更します：
return [b for b in self.books if author.lower() in b.author.lower()]
```

**なぜこれが重要なのか**: Copilot CLI はファイル全体を読み、バグ報告の文脈を理解し、明確な説明とともに具体的な修正案を提示します。

> 💡 **おまけ**: Copilot CLI はファイル全体を分析するため、聞いていない *他の* 問題を発見することもよくあります。例えば、著者の検索を修正している最中に、`find_book_by_title` にある大文字・小文字の区別のバグにも気づくかもしれません！

### 現実世界のセキュリティに関する余談

自分のコードをデバッグすることも重要ですが、本番アプリケーションのセキュリティ脆弱性を理解することは極めて重要です。この例を試してみてください：Copilot CLI に馴染みのないファイルを指定し、セキュリティ上の問題がないか監査（オーディット）させます。

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

このファイルには、本番アプリで遭遇する可能性のある現実的なセキュリティパターンが含まれています。

> 💡 **よく目にするセキュリティ用語:**
> - **SQL インジェクション (SQL Injection)**: ユーザー入力が直接データベースクエリに入れられ、攻撃者が悪意のあるコマンドを実行できてしまうこと。
> - **プリペアドステートメント / パラメータ化クエリ**: 安全な代替手段。プレースホルダー (`?`) を使うことで、ユーザーデータと SQL コマンドを分離します。
> - **レースコンディション (Race condition)**: 2つの操作が同時に発生し、互いに干渉し合ってしまうこと。
> - **XSS (クロスサイトスクリプティング)**: 攻撃者がウェブページに悪意のあるスクリプトを注入すること。

---

### エラーを理解する

スタックトレースをプロンプトに直接貼り付け、`@` ファイル参照を添えることで、Copilot CLI にエラーとソースコードを紐付けさせます。

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### テストケースを使ったデバッグ

正確な入力と観察された出力を説明することで、Copilot CLI が推論するための具体的で再現可能なテストケースを提供します。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### コードを通じた問題の追跡

複数のファイルを参照し、ファイル間のデータフローを追跡して問題の発生源を特定するように Copilot CLI に依頼します。

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### データの問題を理解する

コードと一緒に読み込み対象のデータファイルを含めることで、エラーハンドリングの改善提案を受ける際に Copilot CLI が全体像を理解できるようにします。

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>ワークフロー 4: テスト生成</strong> - 包括的なテストとエッジケースを自動生成</summary>

<img src="assets/test-gen-swimlane-single.png" alt="テスト生成のワークフロー：関数の分析、テストの生成、エッジケースの追加、実行。" width="800"/>

> **まずはこれを試して:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### 「テストの爆発」 - 2 つのテスト vs 15 以上のテスト

手動でテストを書く場合、開発者は通常 2〜3 個の基本的なテストを作成します：
- 有効な入力のテスト
- 無効な入力のテスト
- エッジケースのテスト 1 つ

Copilot CLI に包括的なテストを生成させるとどうなるか見てみましょう！このプロンプトでは、`@` ファイル参照とともに構造化された箇条書きを使用して、徹底的なテストカバレッジをガイドします：

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Test Generation Demo](assets/test-gen-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

**得られる結果**: 次のような、15 以上の包括的なテストが生成されます：

```python
class TestBookCollection:
    # 正常系 (Happy path)
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # 検索操作
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # エッジケース
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # データの永続化
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # 特殊文字
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**結果**: 自分で考えたり書いたりすると 1 時間かかるエッジケースのテストが、30 秒で手に入ります。

---

### ユニットテスト

特定の関数を対象にし、テストしたい入力カテゴリを列挙することで、焦点の絞られた徹底的なユニットテストを生成させます。

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### テストの実行

ツールチェーンに関する普通の質問を投げれば、Copilot CLI が正しいシェルコマンドを生成してくれます。

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI の回答例：
# cd samples/book-app-project && python -m pytest tests/
# 詳細表示の場合：python -m pytest tests/ -v
# print 文を表示したい場合：python -m pytest tests/ -s
```

### 特定のシナリオに対するテスト

網羅してほしい高度な、あるいはトリッキーなシナリオをリストアップすることで、Copilot CLI に正常系以外のテストも書かせます。

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 既存のファイルにテストを追加する

特定の関数に対する *追加の* テストを依頼することで、既存のケースを補完する新しいケースを生成させます。

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>ワークフロー 5: Git 連携</strong> - コミットメッセージ、PR の説明、/pr、/delegate、および /diff</summary>

<img src="assets/git-integration-swimlane-single.png" alt="Git 連携のワークフロー：変更のステージング、メッセージの生成、コミット、PR の作成。" width="800"/>

> 💡 **このワークフローは、git の基本的な知識**（ステージング、コミット、ブランチなど）があることを前提としています。git が初めての方は、まず他の4つのワークフローを試してみてください。

### コミットメッセージの生成

> **まずはこれを試して:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — いくつか変更をステージングしてからこれを実行し、Copilot CLI がコミットメッセージを書く様子を見てみましょう。

この例では、`-p` インラインプロンプトフラグと、`git diff` の出力を直接 Copilot CLI に渡すためのシェルコマンド置換を使用しています。`$(...)` 構文は、括弧内のコマンドを実行し、その出力を外側のコマンドに挿入します。

```bash

# 変更内容を確認
git diff --staged

# [Conventional Commit](../GLOSSARY.md#conventional-commit) 形式でコミットメッセージを生成
# ("feat(books): add search" や "fix(data): handle empty input" のような構造化された形式)
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# 出力例: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Git Integration Demo](assets/git-integration-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

### 変更内容を説明する

`git show` の出力を `-p` プロンプトに渡して、最後のコミットの内容を平易な言葉で要約させます。

```bash
# このコミットは何を変更した？
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR (プルリクエスト) の説明文

`git log` の出力と構造化されたプロンプトテンプレートを組み合わせて、完全なプルリクエストの説明文を自動生成します。

```bash
# ブランチの変更から PR の説明文を生成
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### 対話モードで現在のブランチに対して /pr を使う

Copilot CLI の対話モードでブランチ作業をしている場合、`/pr` コマンドを使ってプルリクエストを操作できます。PR の表示、新規作成、修正、あるいはブランチの状態に基づいた自動判断を指示できます。

```bash
copilot

> /pr [view|create|fix|auto]
```

### プッシュ前のレビュー

`-p` プロンプト内で `git diff main..HEAD` を使い、ブランチのすべての変更に対してプッシュ前の最終チェックを行います。

```bash
# プッシュ前の最終チェック
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### バックグラウンドタスクに /delegate を使う

`/delegate` コマンドは、作業を GitHub Copilot クラウドエージェントに委託します。`/delegate` スラッシュコマンド（または `&` ショートカット）を使って、明確に定義されたタスクをバックグラウンドエージェントに任せることができます。

```bash
copilot

> /delegate Add input validation to the login form

# あるいは & プリフィックスショートカットを使用：
> & Fix the typo in the README header

# Copilot CLI が以下のことを行います：
# 1. 変更を新しいブランチにコミット
# 2. ドラフトプルリクエストを開く
# 3. GitHub 上でバックグラウンド作業を行う
# 4. 完了したらあなたにレビューを求める
```

これは、自分は他の作業に集中したいときに、明確なタスクを片付けるのに最適です。

### セッションの変更を確認する /diff

`/diff` コマンドは、現在のセッション中に行われたすべての変更を表示します。コミットする前に、Copilot CLI が修正したすべての内容を視覚的に確認するためにこのコマンドを使いましょう。

```bash
copilot

# いくつか変更を加えた後……
> /diff

# このセッションで変更されたすべてのファイルの差分を表示
# コミット前のレビューに最適
```

</details>

---

## クイックヒント：計画や実装の前に調査する

ライブラリを調べたり、ベストプラクティスを理解したり、不慣れなトピックを探索したりする必要がある場合は、コードを書く前に `/research` を使って深い調査を実行しましょう：

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot は GitHub リポジトリやウェブソースを検索し、参照付きの要約を返します。これは新しい機能を始める際、事前に情報に基づいた決定を下したいときに便利です。結果は `/share` で共有できます。

> 💡 **ヒント**: `/research` は `/plan` の *前* に使うと効果的です。アプローチを調査してから、実装を計画しましょう。

---

## まとめ：バグ修正ワークフロー

報告されたバグを修正するための完全なワークフローは以下の通りです：

```bash

# 1. バグ報告を理解する
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. 問題をデバッグして修正（同じセッションを継続）
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. 修正のためのテストを生成
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# 対話型セッションを終了
> /exit

# 4. git add の実行
# git diff --staged で差分を比較できるよう、変更をステージングします
git add .

# 5. コミットメッセージを生成
copilot -p "Generate commit message for: $(git diff --staged)"

# 出力例: "fix(books): support partial author name search"

# 6. 変更をコミット（任意）
git commit -m "<生成されたメッセージを貼り付け>"
```

### バグ修正ワークフローの要約

| ステップ | アクション | Copilot コマンド |
|------|--------|-----------------|
| 1 | バグを理解する | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | 分析と修正 | `> Show me the function and fix the issue` |
| 3 | テストを生成する | `> Generate tests for [specific scenarios]` |
| 4 | 変更をステージングする | `git add .` |
| 5 | コミットメッセージを生成する | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | 変更をコミットする | `git commit -m "<paste generated message>"` |

---

# 練習

<img src="../assets/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

学んだワークフローを実際に適用してみましょう。

---

## ▶️ 自分で試してみる

デモが終わったら、次のようなバリエーションも試してみてください：

1. **バグ探偵チャレンジ**: `samples/book-app-buggy/books_buggy.py` の `mark_as_read` 関数のデバッグを依頼してください。なぜ一冊だけでなく「すべて」の本が既読になってしまうのか、AI は説明してくれましたか？

2. **テスト・チャレンジ**: 書籍アプリの `add_book` 関数のテストを生成してください。あなたが思いつかなかったエッジケースがいくつ含まれているか数えてみましょう。

3. **コミットメッセージ・チャレンジ**: 書籍アプリのファイルに何か小さな変更を加え、ステージングし (`git add .`)、以下を実行してください：
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   急いで書いた場合よりも良いメッセージになりましたか？

**自己チェック**: 「バグを探して」よりも「このバグをデバッグして」の方が強力である理由（コンテキストの重要性！）を説明できれば、開発ワークフローを理解したと言えます。

---

## 📝 課題

### メインチャレンジ：リファクタリング、テスト、そしてコミット

ハンズオンでは `find_book_by_title` やコードレビューに焦点を当てました。今度は `book-app-project` の別の関数で同じワークフローのスキルを練習しましょう：

1. **レビュー**: `books.py` の `remove_book()` について、エッジケースや潜在的な問題をレビューさせます：
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **リファクタリング**: `remove_book()` を改善させます。大文字・小文字を区別しないマッチングを行い、本が見つからなかった場合に役立つフィードバックを返すように依頼してください。
3. **テスト**: 改善された `remove_book()` 関数専用の pytest テストを生成させます。以下を網羅してください：
   - 存在する本を削除する
   - 大文字・小文字を区別しないタイトルマッチング（"dune" で "Dune" を削除できる）
   - 本が見つからない場合に適切なレスポンスが返ること
   - 空のコレクションから削除しようとした場合
4. **レビュー**: 変更をステージングし、`/review` を実行して、残っている問題がないかチェックします。
5. **コミット**: コンベンショナルコミットメッセージを生成します：
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**各ステップのプロンプト例:**

```bash
copilot

# ステップ 1: レビュー
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# ステップ 2: リファクタリング
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# ステップ 3: テスト
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# ステップ 4: レビュー
> /review

# ステップ 5: コミット
> Generate a conventional commit message for this refactor
```

**ヒント:** `remove_book()` を改善した後、Copilot CLI にこう聞いてみてください：「このファイルにある他の関数でも、同じような改善ができるものはある？」。`find_book_by_title()` や `find_by_author()` にも同様の変更を提案してくれるかもしれません。

</details>

### ボーナスチャレンジ：Copilot CLI でアプリケーションを作成する

> 💡 **補足**: この GitHub Skills の演習では、Python ではなく **Node.js** を使用します。ただし、Issue の作成、コード生成、ターミナルからの共同作業といった GitHub Copilot CLI のテクニックは、どの言語にも応用できます。

この演習では、Node.js の電卓アプリを構築しながら、GitHub Copilot CLI を使って Issue を作成し、コードを生成し、ターミナルから共同作業する方法を学びます。CLI をインストールし、テンプレートやエージェントを使い、対話的なコマンドライン主導の開発を練習します。

##### <img src="../assets/github-skills-logo.png" width="28" align="center" /> [GitHub Skills 演習を開始：「Create applications with the Copilot CLI」](https://github.com/skills/create-applications-with-the-copilot-cli)（英語）

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong> (クリックして展開)</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| 「このコードをレビューして」のような曖昧なプロンプト | 特定の問題を見逃した一般的なフィードバックになります | 具体的に指定する：「SQL インジェクション、XSS、認証の問題がないかレビューして」 |
| コードレビューに `/review` を使わない | 最適化されたコードレビューエージェントの恩恵を受けられません | ノイズの少ない有益な出力を出す `/review` を使いましょう |
| コンテキストなしで「バグを探して」と聞く | Copilot CLI はあなたがどのようなバグを経験しているか知りません | 症状を説明する：「Y のときに X が起きるという報告がある」 |
| フレームワークを指定せずにテストを生成する | 間違った構文やアサーションライブラリが使われる可能性があります | 指定する：「Jest を使ってテストを生成して」や「pytest を使って」 |

### トラブルシューティング

**レビューが不完全に感じる** - 何を探すべきか、より具体的に指示してください：

```bash
copilot

# こうではなく：
> Review @samples/book-app-project/book_app.py

# こう試す：
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**テストが自分のフレームワークと合わない** - フレームワークを明示してください：

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**リファクタリングで動作が変わってしまう** - 動作を維持するように依頼してください：

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# まとめ

## 🔑 重要なポイント

<img src="assets/specialized-workflows.png" alt="あらゆるタスクのための特化型ワークフロー：コードレビュー、リファクタリング、デバッグ、テスト、Git 連携" width="800"/>

1. **コードレビュー**は、具体的なプロンプトによって包括的なものになります。
2. **リファクタリング**は、まずテストを生成しておくことで安全になります。
3. **デバッグ**は、Copilot CLI にエラー内容とコードの両方を見せることで効果が高まります。
4. **テスト生成**には、エッジケースやエラーシナリオを含めるべきです。
5. **Git 連携**は、コミットメッセージや PR の説明文作成を自動化します。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## ✅ チェックポイント：基本をマスターしました

**おめでとうございます！** GitHub Copilot CLI を使いこなすためのコアスキルをすべて習得しました：

| スキル | 章 | できるようになったこと |
|-------|---------|----------------|
| 基本コマンド | 第01章 | Interactive, Plan, Programmatic (-p) モードとスラッシュコマンドの使用 |
| コンテキスト | 第02章 | `@` によるファイル参照、セッション管理、コンテキストウィンドウの理解 |
| ワークフロー | 第03章 | コードレビュー、リファクタリング、デバッグ、テスト生成、Git 連携 |

第04〜06章では、さらなるパワーを追加する追加機能を扱います。学ぶ価値は十分にあります。

---

## 🛠️ 自分自身のワークフローを構築する

GitHub Copilot CLI の使い方に、唯一の「正解」はありません。あなた自身のパターンを開発するためのヒントをいくつか紹介します：

> 📚 **公式ドキュメント**: GitHub が推奨するワークフローやヒントについては、[Copilot CLI best practices](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices)（英語）を参照してください。

- **些細でない作業にはまず `/plan` を使う**。実行前に計画を洗練させましょう。良い計画が良い結果を導きます。
- **うまくいったプロンプトは保存しておく**。Copilot CLI が間違えたときは、何が悪かったのかメモしましょう。時間の経過とともに、それがあなた専用のプレイブックになります。
- **自由に実験する**。長く詳細なプロンプトを好む開発者もいれば、短いプロンプトと追加のやり取りを好む開発者もいます。いろいろなアプローチを試して、自分にとって自然な方法を見つけてください。

> 💡 **この先の内容**: 第04章と第05章では、ベストプラクティスを「カスタム指示」や「スキル」として体系化し、Copilot CLI が自動的に読み込めるようにする方法を学びます。

---

## ➡️ 次は？

残りの章では、Copilot CLI の能力を拡張する追加機能をカバーします：

| 章 | 内容 | 必要になる場面 |
|---------|----------------|---------------------|
| 第04章: エージェント | 特化型 AI ペルソナの作成 | ドメインエキスパート（フロントエンド、セキュリティ）が必要なとき |
| 第05章: スキル | タスク用指示の自動ロード | 同じプロンプトを何度も繰り返すとき |
| 第06章: MCP | 外部サービスへの接続 | GitHub やデータベースからライブデータが必要なとき |

**おすすめ**: 1週間ほどコアワークフローを試してみて、具体的なニーズが出てきたら第04〜06章に戻ってきてください。

---

## 追加トピックへ進む

**[第04章：エージェントとカスタム指示](../04-agents-custom-instructions/README.ja.md)** では以下を学びます：

- 組み込みエージェント (`/plan`, `/review`) の使用
- `.agent.md` ファイルによる特化型エージェント（フロントエンド専門家、セキュリティ監査員など）の作成
- マルチエージェントによるコラボレーションパターン
- プロジェクト標準のためのカスタム指示ファイル

---

**[← 第02章に戻る](../02-context-conversations/README.ja.md)** | **[第04章へ進む →](../04-agents-custom-instructions/README.ja.md)**
