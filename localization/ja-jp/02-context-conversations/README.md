![第 02 章: コンテキストと会話](../../../02-context-conversations/images/chapter-header.png)

> **AI がファイルを 1 つずつではなく、コードベース全体を把握できたら？**

この章では、GitHub Copilot CLI の真の力、「コンテキスト」を解き放ちます。`@` 構文を使ってファイルやディレクトリを参照し、Copilot CLI にコードベースの深い理解を与える方法を学びます。セッションをまたいで会話を維持する方法、数日後に正確に中断した場所から再開する方法、そして複数ファイルにわたる分析が単一ファイルのレビューでは見落とすバグをどのように発見するかを確認します。

## 🎯 学習目標

この章を終えると、以下ができるようになります。

- `@` 構文を使ってファイル、ディレクトリ、画像を参照する
- `--resume` と `--continue` で前のセッションを再開する
- [コンテキストウィンドウ](../../../GLOSSARY.md#context-window)の仕組みを理解する
- 効果的な複数ターンの会話を書く
- マルチプロジェクトワークフローのためのディレクトリアクセス許可を管理する

> ⏱️ **目安時間**: 約 50 分（20 分読む + 30 分ハンズオン）

---

## 🧩 現実世界のたとえ話: 同僚と働く

<img src="../../../02-context-conversations/images/colleague-context-analogy.png" alt="コンテキストが違いをもたらす - コンテキストなしとコンテキストありの比較" width="800"/>

*同僚と同様に、Copilot CLI は読心術師ではありません。より多くの情報を提供することで、人間も Copilot も的を絞ったサポートができます！*

同僚にバグを説明する場面を想像してください。

> **コンテキストなし**: 「ブックアプリが動かない。」

> **コンテキストあり**: 「`books.py` の `find_book_by_title` 関数を見てみて。大文字小文字を区別しないマッチングをしていないんだ。」

Copilot CLI にコンテキストを提供するには、*`@` 構文*を使って特定のファイルを指定します。

---

# 必須: 基本的なコンテキスト

<img src="../../../02-context-conversations/images/essential-basic-context.png" alt="Copilot CLI の会話でコンテキストが流れる様子を表す光のトレイルで結ばれた輝くコードブロック" width="800"/>

このセクションでは、コンテキストを効果的に使うために必要なすべてをカバーします。まずこの基礎をマスターしましょう。

---

## @ 構文

`@` 記号はプロンプト内でファイルやディレクトリを参照します。Copilot CLI に「このファイルを見て」と伝える方法です。

> 💡 **注意**: このコースのすべての例はこのリポジトリに含まれる `samples/` フォルダを使用しているので、すべてのコマンドを直接試すことができます。

### 今すぐ試してみる（セットアップ不要）

パソコン上の任意のファイルで試せます。

```bash
copilot

# 手持ちのファイルを指定する
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **手元にプロジェクトがない場合？** クイックテストファイルを作成しましょう:
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本的な @ パターン

| パターン | 機能 | 使用例 |
|---------|--------------|-------------|
| `@file.py` | 単一ファイルを参照 | `Review @samples/book-app-project/books.py` |
| `@folder/` | ディレクトリ内のすべてのファイルを参照 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 複数ファイルを参照 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 単一ファイルを参照する

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![ファイルコンテキストデモ](../../../02-context-conversations/images/file-context-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

### 複数ファイルを参照する

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### ディレクトリ全体を参照する

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## クロスファイルインテリジェンス

ここでコンテキストがスーパーパワーになります。単一ファイルの分析は有用です。クロスファイルの分析は変革的です。

<img src="../../../02-context-conversations/images/cross-file-intelligence.png" alt="クロスファイルインテリジェンス - 単一ファイルとクロスファイル分析の比較、一緒に分析することで単独では見えないバグ、データフロー、パターンが明らかになる" width="800"/>

### デモ: 複数ファイルにまたがるバグを見つける

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **高度なオプション**: セキュリティに焦点を当てたクロスファイル分析には、Python セキュリティの例を試してみましょう:
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![マルチファイルデモ](../../../02-context-conversations/images/multi-file-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

**Copilot CLI が発見すること**:

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**なぜこれが重要か**: 単一ファイルのレビューでは全体像を見落とします。クロスファイル分析だけが以下を明らかにします。
- **重複コード**: 統合すべきもの
- **データフローパターン**: コンポーネントがどのように相互作用するか
- **アーキテクチャの問題**: 保守性に影響するもの

---

### デモ: コードベースを 60 秒で理解する

<img src="../../../02-context-conversations/images/codebase-understanding.png" alt="手動コードレビューが 1 時間かかるのに対し、AI 支援分析が 10 秒で完了する比較を示す分割画面" width="800" />

プロジェクトが初めてですか？Copilot CLI を使って素早く理解しましょう。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**得られるもの**:
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**結果**: コードを読むのに 1 時間かかることが 10 秒に圧縮されます。どこに集中すべきか正確にわかります。

---

## 実践的な例

### 例 1: コンテキスト付きコードレビュー

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI は全ファイルの内容を持ち、具体的なフィードバックを提供できます:
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# 今度は book_app.py をレビューするが、books.py のコンテキストはまだ意識している
```

### 例 2: コードベースの理解

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI が books.py を読んで BookCollection クラスを理解する

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI がディレクトリをスキャンして要約する

> How does the app save and load books?

# Copilot CLI はすでに見たコードをトレースできる
```

<details>
<summary>🎬 複数ターンの会話の実際の動作を見てみましょう！</summary>

![複数ターンデモ](../../../02-context-conversations/images/multi-turn-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

### 例 3: マルチファイルリファクタリング

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI は両方のファイルを見て、重複コードを統合する方法を提案できる
```

---

## セッション管理

セッションは作業中に自動保存されます。前のセッションを再開して中断した場所から続けることができます。

### セッションの自動保存

すべての会話は自動的に保存されます。通常通り終了するだけです。

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... 作業する ...]

> /exit
```

### 最近のセッションを再開する

```bash
# 中断した場所から続ける
copilot --continue
```

### 特定のセッションを再開する

```bash
# セッションのリストからインタラクティブに選ぶ
copilot --resume

# または ID で特定のセッションを再開する
copilot --resume=abc123

# またはセッションに付けた名前で再開する
copilot --resume="my book app review"
```

> 💡 **セッション ID はどうやって確認するの？** 覚える必要はありません。ID なしで `copilot --resume` を実行すると、前のセッションの名前、ID、最後のアクティブ時間が一覧表示されます。好きなものを選ぶだけです。
>
> **複数のターミナルがある場合は？** 各ターミナルウィンドウはそれぞれのコンテキストを持つ独立したセッションです。3 つのターミナルで Copilot CLI を開いていれば、それは 3 つの別々のセッションです。どのターミナルからも `--resume` を実行するとすべてを閲覧できます。`--continue` フラグは最初に現在の作業ディレクトリのセッションを取得し、なければ最近アクティブだったセッションを取得します。
>
> **再起動せずにセッションを切り替えられる？** はい。アクティブなセッション内から `/resume` スラッシュコマンドを使います:
> ```
> > /resume
> # 切り替えるセッションのリストを表示する
> ```

### セッションを整理する

後で見つけやすいように、セッションに意味のある名前を付けましょう。セッションの開始時に名前を付けるか、セッション内でいつでも名前を変更できます。

```bash
# セッションを開始するときに名前を付ける
copilot --name book-app-review

# またはセッション内から名前を変更する
copilot

> /rename book-app-review
# セッションが名前付けられて見つけやすくなる
```

セッションに名前が付いたら、リストを参照せずに直接名前で再開できます。

```bash
copilot --resume=book-app-review
```

不要になったセッションを整理するには、セッション内から `/session delete` を使います。

```bash
copilot

> /session delete            # 現在のセッションを削除する
> /session delete abc123     # 特定のセッションを ID で削除する
> /session delete-all        # すべてのセッションを削除する（注意して使う！）
```

### コンテキストの確認と管理

ファイルや会話を追加するにつれて、Copilot CLI の[コンテキストウィンドウ](../../../GLOSSARY.md#context-window)が埋まっていきます。コントロールを保つためのコマンドがいくつかあります。

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 現在のセッションを破棄（履歴は保存されない）して新しい会話を開始する

> /new
# 現在のセッションを終了（履歴に保存して検索・再開可能）して新しい会話を開始する

> /rewind
# タイムラインピッカーを開いて会話の以前の時点にロールバックできる
```

> 💡 **`/clear` または `/new` をいつ使うか**: `books.py` をレビューしていて `utils.py` の話に切り替えたい場合は、まず `/new` を実行してください（セッション履歴が不要なら `/clear`）。そうしないと古いトピックの古いコンテキストがレスポンスを混乱させることがあります。

> 💡 **間違えた、または別のアプローチを試したい？** `/rewind`（または Esc を 2 回押す）を使うと、最後のものだけでなく会話の任意の以前の時点にロールバックできる**タイムラインピッカー**が開きます。間違った方向に進んだが、完全にやり直すことなく引き返したいときに便利です。

---

### 中断した場所から再開する

<img src="../../../02-context-conversations/images/session-persistence-timeline.png" alt="GitHub Copilot CLI のセッションが数日間どのように持続するかを示すタイムライン - 月曜日に開始し、水曜日に完全なコンテキストが復元された状態で再開" width="800"/>

*セッションは終了時に自動保存されます。数日後にファイル、問題、進捗がすべて記憶された状態で再開できます。*

複数日にわたるワークフローを想像してください。

```bash
# 月曜日: 最初から名前付きでブックアプリのレビューを開始する
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# 修正の作業...

> /exit
```

```bash
# 水曜日: 名前で正確に中断した場所から再開する
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**なぜこれが強力か**: 数日後、Copilot CLI は以下を覚えています。
- 作業していた正確なファイル
- 問題の番号付きリスト
- すでに対処したもの
- 会話のコンテキスト

再説明不要。ファイルの再読み込み不要。ただ作業を続けるだけです。

---

**🎉 これで必須事項を理解しました！** `@` 構文、セッション管理（`--name`/`--continue`/`--resume`/`/rename`）、コンテキストコマンド（`/context`/`/clear`）で十分に生産的に働けます。以下はオプションです。準備ができたら戻ってきましょう。

---

# オプション: さらに深く学ぶ

<img src="../../../02-context-conversations/images/optional-going-deeper.png" alt="深いコンテキストの概念の探求を表す青と紫のトーンの抽象的な水晶洞窟" width="800"/>

これらのトピックは上記の必須事項を基に構築されています。**興味のあるものを選んで、または[練習](#練習-practice)に進んでください。**

| 学びたいこと... | ジャンプ先 |
|---|---|
| ワイルドカードパターンと高度なセッションコマンド | [追加の @ パターンとセッションコマンド](#追加の-パターン) |
| 複数のプロンプトにわたるコンテキストの積み上げ | [コンテキスト対応の会話](#コンテキスト対応の会話) |
| トークン制限と `/compact` | [コンテキストウィンドウを理解する](#コンテキストウィンドウを理解する) |
| 参照するファイルの選び方 | [何を参照するかを選ぶ](#何を参照するかを選ぶ) |
| スクリーンショットやモックアップの分析 | [画像を使う](#画像を使う) |

<details>
<summary><strong>追加の @ パターンとセッションコマンド</strong></summary>
<a id="additional-patterns"></a>

### 追加の @ パターン

パワーユーザー向けに、Copilot CLI はワイルドカードパターンと画像参照をサポートしています。

| パターン | 機能 |
|---------|--------------|
| `@folder/*.py` | フォルダ内のすべての .py ファイル |
| `@**/test_*.py` | 再帰ワイルドカード: どこにでもあるすべてのテストファイルを検索 |
| `@image.png` | UI レビュー用の画像ファイル |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### セッション情報を表示する

```bash
copilot

> /session
# 現在のセッションの詳細とワークスペースの概要を表示する

> /usage
# セッションのメトリクスと統計を表示する
```

### セッションを共有する

```bash
copilot

> /share file ./my-session.md
# セッションを Markdown ファイルとしてエクスポートする

> /share gist
# セッションで GitHub Gist を作成する

> /share html
# セッションをスタンドアロンのインタラクティブ HTML ファイルとしてエクスポートする
# チームメートと洗練されたセッションレポートを共有したり、参考用に保存したりするのに便利
```

</details>

<details>
<summary><strong>コンテキスト対応の会話</strong></summary>
<a id="context-aware-conversations"></a>

### コンテキスト対応の会話

魔法は、互いに積み上がる複数ターンの会話をするときに起こります。

#### 例: 段階的な改善

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[型付きバージョンを表示]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[バリデーションと適切な例外を追加]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[包括的なテストを生成]
```

各プロンプトが前の作業をどのように積み上げているかに注目してください。これがコンテキストの力です。

</details>

<details>
<summary><strong>コンテキストウィンドウを理解する</strong></summary>
<a id="understanding-context-windows"></a>

### コンテキストウィンドウを理解する

必須事項から `/context` と `/clear` はすでに知っています。コンテキストウィンドウがどのように機能するかの詳細です。

すべての AI には「コンテキストウィンドウ」があります。これは一度に考慮できるテキストの量です。

<img src="../../../02-context-conversations/images/context-window-visualization.png" alt="コンテキストウィンドウの可視化" width="800"/>

*コンテキストウィンドウはデスクのようなもの: 一度に保持できる量が限られています。ファイル、会話履歴、システムプロンプトがすべてスペースを占有します。*

#### 制限に達するとどうなるか

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# ファイルや会話を追加するにつれて増える

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 警告: コンテキスト制限に近づいています

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` コマンド

コンテキストがいっぱいになってきたが会話を失いたくない場合、`/compact` は履歴を要約してトークンを解放します。

```bash
copilot

> /compact
# 会話履歴を要約してコンテキストスペースを解放する
# 主要な発見と決定は保持される
```

#### コンテキスト効率のヒント

| 状況 | アクション | 理由 |
|-----------|--------|-----|
| 新しいトピックを開始する | `/clear` | 無関係なコンテキストを削除する |
| 間違った方向に進んだ | `/rewind` | 任意の以前の時点にロールバックする |
| 長い会話 | `/compact` | 履歴を要約してトークンを解放する |
| 特定のファイルが必要 | `@folder/` ではなく `@file.py` | 必要なものだけを読み込む |
| 制限に達する | `/new` または `/clear` | 新しいコンテキスト |
| 複数のトピック | トピックごとに `/rename` を使う | 適切なセッションに簡単に再開 |

#### 大規模コードベースのベストプラクティス

1. **具体的にする**: `@samples/book-app-project/` の代わりに `@samples/book-app-project/books.py`
2. **トピック間でコンテキストをクリアする**: フォーカスを切り替えるときは `/new` または `/clear` を使う
3. **`/compact` を使う**: 会話を要約してコンテキストを解放する
4. **複数のセッションを使う**: 機能やトピックごとに 1 つのセッション

</details>

<details>
<summary><strong>何を参照するかを選ぶ</strong></summary>
<a id="choosing-what-to-reference"></a>

### 何を参照するかを選ぶ

コンテキストに関しては、すべてのファイルが同じではありません。賢い選択の方法です。

#### ファイルサイズの考慮事項

| ファイルサイズ | 概算[トークン](../../../GLOSSARY.md#token) | 戦略 |
|-----------|-------------------|----------|
| 小（100 行未満） | 約 500〜1,500 トークン | 自由に参照する |
| 中（100〜500 行） | 約 1,500〜7,500 トークン | 特定のファイルを参照する |
| 大（500 行以上） | 7,500 トークン以上 | 選択的に、特定のファイルを使う |
| 非常に大（1,000 行以上） | 15,000 トークン以上 | 分割またはセクションを対象にすることを検討する |

**具体的な例:**
- ブックアプリの 4 つの Python ファイルを合わせると約 2,000〜3,000 トークン
- 典型的な Python モジュール（200 行）≈ 3,000 トークン
- Flask API ファイル（400 行）≈ 6,000 トークン
- `package.json` ≈ 200〜500 トークン
- 短いプロンプトとレスポンス ≈ 500〜1,500 トークン

> 💡 **コードの簡単な見積もり:** コードの行数に約 15 を掛けると概算トークン数が得られます。これはあくまで推計です。

#### 含めるべきもの vs. 除外すべきもの

**高い価値**（含める）:
- エントリーポイント（`book_app.py`、`main.py`、`app.py`）
- 質問の対象となる特定のファイル
- 対象ファイルによって直接インポートされるファイル
- 設定ファイル（`requirements.txt`、`pyproject.toml`）
- データモデルまたはデータクラス

**低い価値**（除外を検討する）:
- 生成されたファイル（コンパイル済み出力、バンドルされたアセット）
- Node modules またはベンダーディレクトリ
- 大規模なデータファイルまたはフィクスチャ
- 質問と無関係なファイル

#### 特定性のスペクトラム

```
あまり具体的でない ────────────────────────► より具体的
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ すべてをスキャン                     └─ 必要なものだけ
        （より多くのコンテキストを使用）         （コンテキストを節約）
```

**広く参照する場合**（`@samples/book-app-project/`）:
- 初期のコードベース探索
- 多くのファイルにまたがるパターンの検索
- アーキテクチャレビュー

**具体的に参照する場合**（`@samples/book-app-project/books.py`）:
- 特定の問題のデバッグ
- 特定ファイルのコードレビュー
- 単一の関数について質問する

#### 実践的な例: 段階的なコンテキスト読み込み

```bash
copilot

# ステップ 1: 構造から始める
> @package.json What frameworks does this project use?

# ステップ 2: 回答に基づいて絞り込む
> @samples/book-app-project/ Show me the project structure

# ステップ 3: 重要なものにフォーカスする
> @samples/book-app-project/books.py Review the BookCollection class

# ステップ 4: 必要に応じて関連ファイルのみ追加する
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

この段階的なアプローチでコンテキストを集中させ効率的に保ちます。

</details>

<details>
<summary><strong>画像を使う</strong></summary>
<a id="working-with-images"></a>

### 画像を使う

`@` 構文を使って会話に画像を含めたり、単純に**クリップボードから貼り付ける**（Cmd+V / Ctrl+V）ことができます。Copilot CLI はスクリーンショット、モックアップ、ダイアグラムを分析して UI デバッグ、デザイン実装、エラー分析に役立てることができます。

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **詳細**: サポートされているフォーマット、実践的なユースケース、画像とコードを組み合わせるヒントについては、[追加コンテキスト機能](../appendices/additional-context.md#画像の操作)を参照してください。

</details>

---

# 練習 {#practice}

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

コンテキストとセッション管理のスキルを適用する時間です。

---

## ▶️ 自分で試してみよう

### フルプロジェクトレビュー

コースには直接レビューできるサンプルファイルが含まれています。Copilot を起動して次のプロンプトを実行しましょう。

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI は次のような問題を特定します:
# - 重複した表示関数
# - 入力バリデーションの欠如
# - 一貫しないエラーハンドリング
```

> 💡 **自分のファイルで試してみたいですか？** 小さな Python プロジェクトを作成し（`mkdir -p my-project/src`）、いくつかの .py ファイルを追加して、`@my-project/src/` でレビューしましょう。copilot にサンプルコードを作成してもらうこともできます！

### セッションワークフロー

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI がバリデーションのアプローチを提案する]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 後で - 中断した場所から再開する
copilot --continue

> Generate tests for the changes we made
```

---

デモを完了した後、これらのバリエーションを試してみましょう。

1. **クロスファイルチャレンジ**: `book_app.py` と `books.py` がどのように連携するかを分析する:
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **セッションチャレンジ**: セッションを開始して `/rename my-first-session` で名前を付け、何かを作業して `/exit` で終了し、`copilot --continue` を実行する。何をしていたか覚えていますか？

3. **コンテキストチャレンジ**: セッション中に `/context` を実行する。どれだけのトークンを使用していますか？`/compact` を試して再確認しましょう。（`/compact` の詳細については「さらに深く学ぶ」の[コンテキストウィンドウを理解する](#コンテキストウィンドウを理解する)を参照。）

**自己確認**: `@folder/` が各ファイルを個別に開くより強力な理由を説明できればコンテキストを理解しています。

---

## 📝 課題

### メインチャレンジ: データフローをトレースする

ハンズオン例はコード品質レビューと入力バリデーションに焦点を当てていました。今度は同じコンテキストスキルを別のタスク、アプリを通じてデータがどのように移動するかのトレースで練習しましょう。

1. インタラクティブセッションを開始する: `copilot`
2. `books.py` と `book_app.py` を一緒に参照する:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. 追加のコンテキストのためにデータファイルを取り込む:
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. クロスファイルの改善を求める:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. セッションの名前を変更する: `/rename data-flow-analysis`
6. `/exit` で終了し、`copilot --continue` で再開して、データフローについてフォローアップの質問をする

**成功基準**: 複数のファイルにわたるデータをトレースし、名前付きセッションを再開し、クロスファイルの提案を得ることができています。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**始め方:**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

次に再開する: `copilot --continue`

**便利なコマンド:**
- `@file.py` - 単一ファイルを参照する
- `@folder/` - フォルダ内のすべてのファイルを参照する（末尾の `/` に注意）
- `/context` - 使用中のコンテキスト量を確認する
- `/rename <名前>` - 簡単な再開のためにセッションに名前を付ける

</details>

### ボーナスチャレンジ: コンテキスト制限

1. `@samples/book-app-project/` でブックアプリのすべてのファイルを一度に参照する
2. 異なるファイル（`books.py`、`utils.py`、`book_app.py`、`data.json`）について詳細な質問をいくつかする
3. `/context` を実行して使用量を確認する。どれだけ早く埋まるか？
4. `/compact` を使ってスペースを回収し、会話を続ける練習をする
5. ファイル参照をより具体的にして（例: フォルダ全体の代わりに `@samples/book-app-project/books.py`）、コンテキスト使用量にどう影響するかを確認する

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| ファイル名の前に `@` を忘れる | Copilot CLI が "books.py" を平文として扱う | `@samples/book-app-project/books.py` を使ってファイルを参照する |
| セッションが自動的に持続することを期待する | 新しく `copilot` を起動すると前のコンテキストがすべて失われる | `--continue`（最後のセッション）または `--resume`（セッションを選ぶ）を使う |
| 現在のディレクトリ外のファイルを参照する | 「Permission denied」または「File not found」エラー | `/add-dir /path/to/directory` でアクセスを許可する |
| トピックを切り替えるときに `/clear` を使わない | 古いコンテキストが新しいトピックについてのレスポンスを混乱させる | 別のタスクを開始する前に `/clear` を実行する |

### トラブルシューティング

**「File not found」エラー** - 正しいディレクトリにいることを確認する:

```bash
pwd  # 現在のディレクトリを確認する
ls   # ファイルを一覧表示する

# Copilot を起動して相対パスを使う
copilot

> Review @samples/book-app-project/books.py
```

**「Permission denied」** - ディレクトリを許可リストに追加する:

```bash
copilot --add-dir /path/to/directory

# またはセッション内で:
> /add-dir /path/to/directory
```

**コンテキストの埋まりが早すぎる**:
- ファイル参照をより具体的にする
- 異なるトピック間で `/clear` を使う
- 複数のセッションに作業を分割する

</details>

---

# まとめ

## 🔑 重要なポイント

1. **`@` 構文**はファイル、ディレクトリ、画像についてのコンテキストを Copilot CLI に提供する
2. **複数ターンの会話**は、コンテキストが蓄積するにつれて互いに積み上がる
3. **セッションの自動保存**: 起動時に `--name` で名前を付け、`--resume=<名前>` で名前で再開するか、`--continue` で最近のセッションを再開する
4. **コンテキストウィンドウ**には制限がある: `/clear`、`/compact`、`/context`、`/new`、`/rewind` で管理する
5. **アクセス許可フラグ**（`--add-dir`、`--allow-all`）はマルチディレクトリアクセスを制御する。賢く使おう！
6. **画像参照**（`@screenshot.png`）は UI の問題を視覚的にデバッグするのに役立つ

> 📚 **公式ドキュメント**: コンテキスト、セッション、ファイルを使った作業の完全なリファレンスは [Copilot CLI の使い方](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli)をご覧ください。

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次のステップ

Copilot CLI にコンテキストを提供できるようになったので、実際の開発タスクに活用しましょう。今学んだコンテキスト技術（ファイル参照、クロスファイル分析、セッション管理）は次の章の強力なワークフローの基礎となります。

[**第 03 章: 開発ワークフロー**](../03-development-workflows/README.md)では以下を学びます。

- コードレビューワークフロー
- リファクタリングパターン
- デバッグ支援
- テスト生成
- Git 統合

---

[**← 第 01 章に戻る**](../01-setup-and-first-steps/README.md) | [**第 03 章に進む →**](../03-development-workflows/README.md)
