![第 03 章: 開発ワークフロー](../../../03-development-workflows/images/chapter-header.png)

> **AI が質問されてもいないバグを見つけてくれたら？**

この章では、GitHub Copilot CLI が日常的なドライバーになります。すでに毎日頼りにしているワークフロー、テスト、リファクタリング、デバッグ、Git の中で使いましょう。

## 🎯 学習目標

この章を終えると、以下ができるようになります。

- Copilot CLI で包括的なコードレビューを実行する
- レガシーコードを安全にリファクタリングする
- AI の支援でバグをデバッグする
- テストを自動的に生成する
- Copilot CLI を Git ワークフローに統合する

> ⏱️ **目安時間**: 約 60 分（15 分読む + 45 分ハンズオン）

---

## 🧩 現実世界のたとえ話: 大工のワークフロー

大工はツールの使い方を知っているだけでなく、異なる作業に対する*ワークフロー*を持っています。

<img src="../../../03-development-workflows/images/carpenter-workflow-steps.png" alt="職人のワークショップ: 3 つのワークフローレーン、家具制作（計測、切断、組立、仕上げ）、損傷修復（評価、除去、修理、マッチング）、品質チェック（点検、継手テスト、整合確認）" width="800"/>

同様に、開発者も異なるタスクに対するワークフローを持っています。GitHub Copilot CLI はこれらのワークフローを強化し、日常的なコーディングタスクをより効率的かつ効果的にします。

---

# 5 つのワークフロー

<img src="../../../03-development-workflows/images/five-workflows.png" alt="コードレビュー、テスト、デバッグ、リファクタリング、Git 統合ワークフローを表す 5 つの輝くネオンアイコン" width="800"/>

以下の各ワークフローは独立しています。現在のニーズに合ったものを選ぶか、すべて進めましょう。

---

## 自分のペースで選ぶ

この章では開発者が通常使う 5 つのワークフローをカバーします。**すべてを一度に読む必要はありません！** 以下の折りたたみセクションの中に各ワークフローが独立して含まれています。現在のニーズに合うものを選び、現在のプロジェクトに最適なものを探してください。いつでも戻って他のものを探索できます。

<img src="../../../03-development-workflows/images/five-workflows-swimlane.png" alt="5 つの開発ワークフロー: コードレビュー、リファクタリング、デバッグ、テスト生成、Git 統合が水平のスイムレーンとして表示" width="800"/>

| 目的... | ジャンプ先 |
|---|---|
| マージ前にコードをレビューする | [ワークフロー 1: コードレビュー](#workflow-1-code-review) |
| ゴチャゴチャしたまたはレガシーコードを整理する | [ワークフロー 2: リファクタリング](#workflow-2-refactoring) |
| バグを追跡して修正する | [ワークフロー 3: デバッグ](#workflow-3-debugging) |
| コードのテストを生成する | [ワークフロー 4: テスト生成](#workflow-4-test-generation) |
| より良いコミットと PR を書く | [ワークフロー 5: Git 統合](#workflow-5-git-integration) |
| コーディング前に調査する | [クイックヒント: 計画やコーディング前に調査する](#quick-tip-research-before-you-plan-or-code) |
| バグ修正ワークフロー全体を見る | [すべてをまとめる](#putting-it-all-together-bug-fix-workflow) |

**以下のワークフローを選択して展開し**、その分野で GitHub Copilot CLI が開発プロセスをどのように強化できるかを確認しましょう。

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>ワークフロー 1: コードレビュー</strong> - ファイルのレビュー、/review エージェントの使用、深刻度チェックリストの作成</summary>

<img src="../../../03-development-workflows/images/code-review-swimlane-single.png" alt="コードレビューワークフロー: レビュー、問題特定、優先順位付け、チェックリスト生成" width="800"/>

### 基本的なレビュー

この例では `@` 記号を使ってファイルを参照し、Copilot CLI がレビュー用にその内容に直接アクセスできるようにします。

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![コードレビューデモ](../../../03-development-workflows/images/code-review-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

### 入力バリデーションのレビュー

プロンプトに関心のあるカテゴリを列挙して、Copilot CLI のレビューを特定の懸念事項（ここでは入力バリデーション）に集中させましょう。

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### クロスファイルプロジェクトレビュー

`@` でディレクトリ全体を参照して、Copilot CLI がプロジェクト内のすべてのファイルを一度にスキャンできるようにします。

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### インタラクティブコードレビュー

複数ターンの会話を使ってより深く掘り下げましょう。広いレビューから始め、再起動せずにフォローアップの質問をします。

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI が詳細なレビューを提供する

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI が空文字列や特殊文字の潜在的な問題を表示する

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI が優先順位付けされたアクションアイテムを生成する
```

### レビューチェックリストテンプレート

Copilot CLI に特定のフォーマット（ここでは Issue に貼り付けられる深刻度分類された Markdown チェックリスト）で出力を構造化するよう頼みましょう。

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Git の変更を理解する（/review に重要）

`/review` コマンドを使う前に、Git の 2 種類の変更を理解する必要があります。

| 変更の種類 | 意味 | 確認方法 |
|-------------|---------------|------------|
| **ステージ済みの変更** | `git add` で次のコミット用にマークしたファイル | `git diff --staged` |
| **未ステージの変更** | 変更したがまだ追加していないファイル | `git diff` |

```bash
# クイックリファレンス
git status           # ステージ済みと未ステージの両方を表示する
git add file.py      # コミット用にファイルをステージする
git diff             # 未ステージの変更を表示する
git diff --staged    # ステージ済みの変更を表示する
```

### /review コマンドの使用

`/review` コマンドは組み込みの**コードレビューエージェント**を呼び出します。これはステージ済みおよび未ステージの変更を高い信号対雑音比で分析するように最適化されています。自由形式のプロンプトを書く代わりに、スラッシュコマンドを使って特化した組み込みエージェントをトリガーします。

```bash
copilot

> /review
# ステージ済み/未ステージの変更に対してコードレビューエージェントを呼び出す
# 集中した実行可能なフィードバックを提供する

> /review Check for security issues in authentication
# 特定のフォーカス領域でレビューを実行する
```

> 💡 **ヒント**: コードレビューエージェントは変更が保留中のときに最もよく機能します。より集中したレビューのために `git add` でファイルをステージしましょう。

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>ワークフロー 2: リファクタリング</strong> - コードの再構築、懸念事項の分離、エラーハンドリングの改善</summary>

<img src="../../../03-development-workflows/images/refactoring-swimlane-single.png" alt="リファクタリングワークフロー: コードの評価、変更の計画、実装、動作の確認" width="800"/>

### シンプルなリファクタリング

> **まずこれを試す:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

シンプルな改善から始めましょう。ブックアプリで試してみてください。各プロンプトは `@` ファイル参照と特定のリファクタリング指示を組み合わせているので、Copilot CLI は何を変更すべきか正確に理解します。

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **リファクタリングが初めてですか？** 複雑な変換に取り組む前に、型ヒントの追加や変数名の改善などのシンプルなリクエストから始めましょう。

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![リファクタリングデモ](../../../03-development-workflows/images/refactor-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

### 懸念事項を分離する

単一のプロンプトで複数のファイルを `@` で参照し、Copilot CLI がリファクタリングの一部としてそれらの間でコードを移動できるようにします。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### エラーハンドリングを改善する

2 つの関連ファイルを提供し、横断的な関心事を説明して、Copilot CLI が両方に一貫した修正を提案できるようにします。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### ドキュメントを追加する

各ドキュメント文字列に含めるべき内容の詳細なリストを提供して、Copilot CLI が具体的に何を変更すべきか正確に理解できるようにします。

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### テストを使った安全なリファクタリング

複数ターンの会話で 2 つの関連するリクエストを連鎖させます。まずテストを生成し、そのテストを安全網としてリファクタリングします。

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# まずテストを取得する

> Now refactor the BookCollection class to use a context manager for file operations

# テストがあれば自信を持ってリファクタリングできる
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>ワークフロー 3: デバッグ</strong> - バグの追跡、セキュリティ監査、ファイルをまたいだ問題のトレース</summary>

<img src="../../../03-development-workflows/images/debugging-swimlane-single.png" alt="デバッグワークフロー: エラーの理解、根本原因の特定、修正、テスト" width="800"/>

### シンプルなデバッグ

> **まずこれを試す:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

何が問題かを説明するところから始めましょう。バグのあるブックアプリで試せる一般的なデバッグパターンです。各プロンプトは `@` ファイル参照と明確な症状の説明を組み合わせているので、Copilot CLI がバグを特定して診断できます。

```bash
copilot

# パターン: 「X を期待したが Y を得た」
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# パターン: 「予期しない動作」
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# パターン: 「間違った結果」
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **デバッグのヒント**: *症状*（見えていること）と*期待値*（起こるべきこと）を説明しましょう。Copilot CLI が残りを解決します。

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![バグ修正デモ](../../../03-development-workflows/images/fix-bug-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

### 「バグ探偵」- AI が関連するバグを発見する

コンテキスト対応デバッグが輝く場面です。バグのあるブックアプリでこのシナリオを試してみましょう。`@` でファイル全体を提供し、ユーザーが報告した症状だけを説明します。Copilot CLI が根本原因をトレースし、近くの追加バグを発見することもあります。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI が行うこと**:
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**なぜこれが重要か**: Copilot CLI はファイル全体を読み込み、バグレポートのコンテキストを理解し、明確な説明とともに具体的な修正を提供します。

> 💡 **ボーナス**: Copilot CLI はファイル全体を分析するため、尋ねなかった*他の*問題も発見することがよくあります。例えば、著者検索を修正している間に、`find_book_by_title` の大文字小文字区別バグも気づくかもしれません！

### 現実世界のセキュリティサイドバー

自分のコードのデバッグも重要ですが、本番アプリケーションのセキュリティ脆弱性を理解することは非常に重要です。この例を試してみましょう: 知らないファイルに Copilot CLI を向けてセキュリティ問題の監査を頼みます。

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

このファイルは本番アプリで遭遇する現実世界のセキュリティパターンを示しています。

> 💡 **遭遇する一般的なセキュリティ用語:**
> - **SQL インジェクション**: ユーザーの入力が直接データベースクエリに入れられ、攻撃者が悪意のあるコマンドを実行できるとき
> - **パラメータ化クエリ**: 安全な代替方法 - プレースホルダー（`?`）がユーザーデータを SQL コマンドから分離する
> - **レースコンディション**: 2 つの操作が同時に発生し互いに干渉するとき
> - **XSS（クロスサイトスクリプティング）**: 攻撃者が Web ページに悪意のあるスクリプトを注入するとき

---

### エラーを理解する

スタックトレースを `@` ファイル参照と一緒に直接プロンプトに貼り付けて、Copilot CLI がエラーをソースコードにマッピングできるようにします。

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### テストケースを使ったデバッグ

正確な入力と観察された出力を説明して、Copilot CLI が推論できる具体的な再現可能なテストケースを提供します。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### コードを通じて問題をトレースする

複数のファイルを参照して、Copilot CLI にそれらをまたいでデータフローを追跡し、問題の発生源を特定させます。

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### データの問題を理解する

コードがデータを読み込む際に、一緒にデータファイルを含めることで、Copilot CLI がエラーハンドリングの改善を提案する際に全体像を理解できるようにします。

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>ワークフロー 4: テスト生成</strong> - 包括的なテストとエッジケースを自動的に生成する</summary>

<img src="../../../03-development-workflows/images/test-gen-swimlane-single.png" alt="テスト生成ワークフロー: 関数の分析、テストの生成、エッジケースの含む、実行" width="800"/>

> **まずこれを試す:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### 「テスト爆発」- 2 テスト対 15 以上のテスト

手動でテストを書く場合、開発者は通常 2〜3 の基本的なテストを作成します。
- 有効な入力をテストする
- 無効な入力をテストする
- エッジケースをテストする

Copilot CLI に包括的なテストを生成するよう頼むと何が起こるか見てみましょう！このプロンプトは `@` ファイル参照と構造化された箇条書きリストを使って、Copilot CLI を徹底的なテストカバレッジに向けます。

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
<summary>🎬 実際の動作を見てみましょう！</summary>

![テスト生成デモ](../../../03-development-workflows/images/test-gen-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

**得られるもの**: 以下を含む 15 以上の包括的なテスト:

```python
class TestBookCollection:
    # ハッピーパス
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

    # データ永続性
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

**結果**: 30 秒で、考えるのに 1 時間かかるエッジケーステストが完成します。

---

### ユニットテスト

単一の関数を対象として、テストしたい入力カテゴリを列挙し、Copilot CLI が集中した徹底的なユニットテストを生成できるようにします。

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

ツールチェーンについて平易な言葉で Copilot CLI に質問しましょう。適切なシェルコマンドを生成できます。

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI が応答する:
# cd samples/book-app-project && python -m pytest tests/
# または詳細な出力: python -m pytest tests/ -v
# print 文を見る: python -m pytest tests/ -s
```

### 特定のシナリオのテスト

網羅したい高度なトリッキーなシナリオをリストアップして、Copilot CLI がハッピーパスを超えるようにします。

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 既存ファイルにテストを追加する

単一の関数に対して*追加の*テストを求めて、Copilot CLI がすでに持っているものを補完する新しいケースを生成するようにします。

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
<summary><strong>ワークフロー 5: Git 統合</strong> - コミットメッセージ、PR 説明、/pr、/delegate、/diff</summary>

<img src="../../../03-development-workflows/images/git-integration-swimlane-single.png" alt="Git 統合ワークフロー: 変更のステージング、メッセージの生成、コミット、PR の作成" width="800"/>

> 💡 **このワークフローは基本的な Git の知識を前提としています**（ステージング、コミット、ブランチ）。Git が初めての場合は、まず他の 4 つのワークフローを試してください。

### コミットメッセージを生成する

> **まずこれを試す:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — 変更をステージしてからこれを実行し、Copilot CLI がコミットメッセージを書くのを見てみましょう。

この例では `-p` インラインプロンプトフラグとシェルコマンド置換を使って、`git diff` の出力を直接 Copilot CLI に渡して一発でコミットメッセージを生成します。`$(...)` の構文は括弧内のコマンドを実行し、その出力を外側のコマンドに挿入します。

```bash

# 何が変わったか確認する
git diff --staged

# [Conventional Commit](../../../GLOSSARY.md#conventional-commit) フォーマット（"feat(books): add search" や "fix(data): handle empty input" のような構造化メッセージ）でコミットメッセージを生成する
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# 出力: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![Git 統合デモ](../../../03-development-workflows/images/git-integration-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

### 変更を説明する

`git show` の出力を `-p` プロンプトに渡して、最後のコミットの平易な言葉による概要を取得します。

```bash
# このコミットは何を変更したか？
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR の説明

`git log` の出力と構造化プロンプトテンプレートを組み合わせて、完全なプルリクエストの説明を自動生成します。

```bash
# ブランチの変更から PR の説明を生成する
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### 現在のブランチに対してインタラクティブモードで /pr を使用する

Copilot CLI のインタラクティブモードでブランチを操作している場合、`/pr` コマンドを使ってプルリクエストを操作できます。`/pr` を使って PR を表示したり、新しい PR を作成したり、既存の PR を修正したり、ブランチの状態に基づいて Copilot CLI に自動決定させたりできます。

```bash
copilot

> /pr [view|create|fix|auto]
```

### プッシュ前にレビューする

`-p` プロンプト内で `git diff main..HEAD` を使ってすべてのブランチ変更にわたる素早いプッシュ前の最終チェックを行います。

```bash
# プッシュ前の最後の確認
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### バックグラウンドタスクに /delegate を使用する

`/delegate` コマンドは GitHub Copilot クラウドエージェントに作業を引き渡します。`/delegate` スラッシュコマンド（または `&` ショートカット）を使って、明確に定義されたタスクをバックグラウンドエージェントにオフロードします。

```bash
copilot

> /delegate Add input validation to the login form

# または & プレフィックスショートカットを使う:
> & Fix the typo in the README header

# Copilot CLI が:
# 1. 変更を新しいブランチにコミットする
# 2. ドラフトプルリクエストを開く
# 3. GitHub でバックグラウンドで作業する
# 4. 完了したらレビューをリクエストする
```

これは他の作業に集中している間に完了させたい明確に定義されたタスクに最適です。

### /diff を使ってセッションの変更をレビューする

`/diff` コマンドは現在のセッション中に行われたすべての変更を表示します。コミットする前に Copilot CLI が変更したすべてを視覚的な差分で確認するためにこのスラッシュコマンドを使います。

```bash
copilot

# 変更を加えた後...
> /diff

# このセッションで変更されたすべてのファイルの視覚的な差分を表示する
# コミット前のレビューに最適
```

</details>

---

## クイックヒント: 計画やコーディング前に調査する {#quick-tip-research-before-you-plan-or-code}

ライブラリを調査したり、ベストプラクティスを理解したり、不慣れなトピックを探索したりする必要がある場合は、コードを書く前に `/research` を使って深い調査を実行しましょう。

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot は GitHub リポジトリとウェブソースを検索し、参照付きの概要を返します。新しい機能を始めようとしているときに、まず情報に基づいた決定をするのに役立ちます。`/share` を使って結果を共有できます。

> 💡 **ヒント**: `/research` は `/plan` の*前に*使うとよく機能します。アプローチを調査して、実装を計画しましょう。

---

## すべてをまとめる: バグ修正ワークフロー {#putting-it-all-together-bug-fix-workflow}

報告されたバグを修正するための完全なワークフローです。

```bash

# 1. バグレポートを理解する
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. 問題をデバッグして修正する（同じセッションで続ける）
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. 修正のテストを生成する
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# インタラクティブセッションを終了する

> /exit

# 4. git add を実行する

# git diff --staged に何かを入れるために変更をステージする
git add .

# 5. コミットメッセージを生成する
copilot -p "Generate commit message for: $(git diff --staged)"

# 出力例: "fix(books): support partial author name search"

# 6. 変更をコミットする（オプション）

git commit -m "<生成されたメッセージを貼り付ける>"
```

### バグ修正ワークフローのまとめ

| ステップ | アクション | Copilot コマンド |
|------|--------|-----------------|
| 1 | バグを理解する | `> [バグを説明する] @relevant-file.py Analyze the likely cause` |
| 2 | 分析と修正 | `> Show me the function and fix the issue` |
| 3 | テストを生成する | `> Generate tests for [特定のシナリオ]` |
| 4 | 変更をステージする | `git add .` |
| 5 | コミットメッセージを生成する | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | 変更をコミットする | `git commit -m "<生成されたメッセージを貼り付ける>"` |

---

# 練習

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

これらのワークフローを適用する番です。

---

## ▶️ 自分で試してみよう

デモを完了した後、これらのバリエーションを試してみましょう。

1. **バグ探偵チャレンジ**: `samples/book-app-buggy/books_buggy.py` の `mark_as_read` 関数をデバッグするよう Copilot CLI に頼む。1 冊ではなくすべての本が既読としてマークされる理由を説明しましたか？

2. **テストチャレンジ**: ブックアプリの `add_book` 関数のテストを生成する。Copilot CLI が含めたエッジケースで自分では思いつかなかったものはいくつありましたか？

3. **コミットメッセージチャレンジ**: ブックアプリのファイルに小さな変更を加え、ステージし（`git add .`）、次を実行する:
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   自分が素早く書いたメッセージよりも良いですか？

**自己確認**: 「バグを見つける」より「このバグをデバッグする」の方が強力な理由を説明できれば開発ワークフローを理解しています（コンテキストが重要！）。

---

## 📝 課題

### メインチャレンジ: リファクタリング、テスト、そして出荷

ハンズオン例は `find_book_by_title` とコードレビューに焦点を当てていました。今度は `book-app-project` の異なる関数で同じワークフロースキルを練習しましょう。

1. **レビュー**: `books.py` の `remove_book()` をエッジケースと潜在的な問題についてレビューするよう Copilot CLI に頼む:
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **リファクタリング**: 大文字小文字を区別しないマッチングや本が見つからなかったときの有用なフィードバックを返すなど、エッジケースを処理するよう `remove_book()` を改善するよう Copilot CLI に頼む
3. **テスト**: 改善された `remove_book()` 関数のための pytest テストを生成する（以下をカバー）:
   - 存在する本を削除する
   - 大文字小文字を区別しないタイトルマッチング
   - 存在しない本は適切なフィードバックを返す
   - 空のコレクションから削除する
4. **レビュー**: 変更をステージして `/review` を実行し、残りの問題を確認する
5. **コミット**: 規約に沿ったコミットメッセージを生成する:
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**各ステップのサンプルプロンプト:**

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

**ヒント:** `remove_book()` を改善した後、Copilot CLI に「Are there any other functions in this file that could benefit from the same improvements?」と聞いてみてください。`find_book_by_title()` や `find_by_author()` への同様の変更を提案するかもしれません。

</details>

### ボーナスチャレンジ: Copilot CLI でアプリケーションを作成する

> 💡 **注意**: この GitHub Skills 演習は Python ではなく **Node.js** を使用します。練習する GitHub Copilot CLI のテクニック（Issue の作成、コードの生成、ターミナルからのコラボレーション）はどの言語にも適用できます。

この演習では、GitHub Copilot CLI を使って Issue を作成し、コードを生成し、Node.js 計算機アプリを構築しながらターミナルからコラボレーションする方法を開発者に示します。CLI のインストール、テンプレートとエージェントの使用、反復的なコマンドライン駆動開発を練習します。

##### <img src="../../../images/github-skills-logo.png" width="28" align="center" /> [「Copilot CLI でアプリケーションを作成する」Skills 演習を開始する](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| 「Review this code」のような曖昧なプロンプトを使う | 特定の問題を見落とす一般的なフィードバック | 具体的に: 「Review for SQL injection, XSS, and auth issues」 |
| コードレビューに `/review` を使わない | 最適化されたコードレビューエージェントを見逃す | 高い信号対雑音比の出力に調整された `/review` を使う |
| コンテキストなしで「バグを見つける」と頼む | Copilot CLI は経験しているバグを知らない | 症状を説明する: 「Users report X happens when Y」 |
| フレームワークを指定せずにテストを生成する | テストが間違った構文またはアサーションライブラリを使用する可能性がある | 指定する: 「Generate tests using Jest」または「using pytest」 |

### トラブルシューティング

**レビューが不完全に見える** - 何を探すかをより具体的にする:

```bash
copilot

# 代わりに:
> Review @samples/book-app-project/book_app.py

# 試してみる:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**テストがフレームワークに合わない** - フレームワークを指定する:

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**リファクタリングが動作を変える** - Copilot CLI に動作を保持するよう頼む:

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# まとめ

## 🔑 重要なポイント

<img src="../../../03-development-workflows/images/specialized-workflows.png" alt="すべてのタスクに特化したワークフロー: コードレビュー、リファクタリング、デバッグ、テスト、Git 統合" width="800"/>

1. **コードレビュー**は具体的なプロンプトで包括的になる
2. **リファクタリング**はまずテストを生成することでより安全になる
3. **デバッグ**はエラーとコードの両方を Copilot CLI に見せることで恩恵を受ける
4. **テスト生成**はエッジケースとエラーシナリオを含めるべき
5. **Git 統合**はコミットメッセージと PR の説明を自動化する

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ✅ チェックポイント: 必須スキルをマスターしました

**おめでとうございます！** GitHub Copilot CLI で生産的になるためのコアスキルをすべて身につけました。

| スキル | 章 | できるようになったこと |
|-------|---------|----------------|
| 基本コマンド | 第 01 章 | インタラクティブモード、プランモード、プログラマティックモード（-p）、スラッシュコマンドを使う |
| コンテキスト | 第 02 章 | `@` でファイルを参照し、セッションを管理し、コンテキストウィンドウを理解する |
| ワークフロー | 第 03 章 | コードをレビューし、リファクタリングし、デバッグし、テストを生成し、Git と統合する |

第 04〜06 章では、さらなるパワーを追加する追加機能をカバーします。

---

## 🛠️ 個人的なワークフローを構築する

GitHub Copilot CLI を使う唯一の「正しい」方法はありません。自分のパターンを開発する際のヒントです。

> 📚 **公式ドキュメント**: GitHub からの推奨ワークフローとヒントについては [Copilot CLI のベストプラクティス](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices)をご覧ください。

- **些細でないことには `/plan` から始める。** 実行前に計画を洗練させましょう — 良い計画はより良い結果につながります。
- **うまく機能するプロンプトを保存する。** Copilot CLI が間違えたとき、何が悪かったかをメモしましょう。時間が経つと、これが個人的なプレイブックになります。
- **自由に実験する。** 長くて詳細なプロンプトを好む開発者もいれば、フォローアップ付きの短いプロンプトを好む開発者もいます。さまざまなアプローチを試して、何が自然に感じるかを確認しましょう。

> 💡 **次のステップ**: 第 04 章と第 05 章では、ベストプラクティスを Copilot CLI が自動的に読み込むカスタム指示とスキルにコード化する方法を学びます。

---

## ➡️ 次のステップ

残りの章では Copilot CLI の機能を拡張する追加機能をカバーします。

| 章 | カバーする内容 | 必要になるとき |
|---------|----------------|---------------------|
| 第 04 章: エージェント | 特化した AI ペルソナを作成する | ドメインエキスパート（フロントエンド、セキュリティ）が必要なとき |
| 第 05 章: スキル | タスクの指示を自動読み込みする | 同じプロンプトを何度も繰り返すとき |
| 第 06 章: MCP | 外部サービスを接続する | GitHub、データベースからライブデータが必要なとき |

**推奨**: コアワークフローを 1 週間試してから、特定のニーズがあるときに第 04〜06 章に戻りましょう。

---

## 追加トピックに進む

[**第 04 章: エージェントとカスタム指示**](../04-agents-custom-instructions/README.md)では以下を学びます。

- 組み込みエージェント（`/plan`、`/review`）の使用
- `.agent.md` ファイルを使った特化したエージェントの作成（フロントエンドエキスパート、セキュリティ監査員）
- マルチエージェントのコラボレーションパターン
- プロジェクト標準のカスタム指示ファイル

---

[**← 第 02 章に戻る**](../02-context-conversations/README.md) | [**第 04 章に進む →**](../04-agents-custom-instructions/README.md)
