<!--
---
id: CopilotCLI-02
title: コンテキストと会話
description: GitHub Copilot CLI でファイルやディレクトリのコンテキストを使用し、以前のセッションを再開して、効果的な複数ターンの会話を作成します。
audience: Developers / Students / Terminal users
slug: context-and-conversations
weight: 3
---
-->

![Chapter 02: Context and Conversations](assets/chapter-header.png)

[English Version](./README.md)

> **もし AI が一度に一つのファイルだけでなく、コードベース全体を見ることができたらどうでしょうか？**

この章では、GitHub Copilot CLI の真の力である「コンテキスト（文脈）」を解き放ちます。`@` 構文を使ってファイルやディレクトリを参照し、Copilot CLI にコードベースへの深い理解を与える方法を学びます。また、セッションをまたいで会話を維持し、数日後に作業を中断したところから正確に再開する方法、そして単一ファイルのレビューでは見逃してしまうバグを複数ファイルの分析でキャッチする方法を発見します。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- `@` 構文を使用してファイル、ディレクトリ、画像を参照する
- `--resume` や `--continue` を使用して以前のセッションを再開する
- [コンテキストウィンドウ](../GLOSSARY.md#context-window)の仕組みを理解する
- 効果的な複数回のやり取り（マルチターン会話）を行う
- 複数プロジェクトのワークフローにおけるディレクトリ権限を管理する

> ⏱️ **推定所要時間**: 約50分（読みもの20分 ＋ 実践30分）

---

## 🧩 現実世界の例え：同僚との作業

<img src="assets/colleague-context-analogy.png" alt="コンテキストが違いを生む - コンテキストなし vs あり" width="800"/>

*同僚と同じように、Copilot CLI は心を読めるわけではありません。より多くの情報を提供することで、人間も Copilot も、より的を絞ったサポートを提供できるようになります！*

同僚にバグを説明する場面を想像してみてください：

> **コンテキストなし**: 「書籍アプリが動かないんだ。」

> **コンテキストあり**: 「`books.py` を見て。特に `find_book_by_title` 関数。大文字・小文字を区別しないマッチングができていないみたいなんだ。」

Copilot CLI にコンテキストを提供するには、*`@` 構文* を使って特定のファイルを指定します。

---

# 必須知識：基本のコンテキスト

<img src="assets/essential-basic-context.png" alt="Copilot CLI の会話を通じてコンテキストが流れる様子を表す、光の軌跡でつながれた光るコードブロック" width="800"/>

このセクションでは、コンテキストを効果的に扱うために必要なすべての知識をカバーします。まずはこれらの基本をマスターしましょう。

---

## @ 構文

`@` 記号は、プロンプト内でファイルやディレクトリを参照するために使用します。これは Copilot CLI に「このファイルを見て」と伝える方法です。

> 💡 **補足**: このコースのすべての例は、このリポジトリに含まれる `samples/` フォルダを使用しているため、すべてのコマンドを直接試すことができます。

### 今すぐ試す（セットアップ不要）

お使いのコンピュータにある任意のファイルで試すことができます：

```bash
copilot

# 手元にある任意のファイルを指定してみてください
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **手元にプロジェクトがない場合** は、簡単なテストファイルを作ってみましょう：
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本的な @ パターン

| パターン | 何をするか | 使用例 |
|---------|--------------|-------------|
| `@file.py` | 単一のファイルを参照 | `Review @samples/book-app-project/books.py` |
| `@folder/` | ディレクトリ内の全ファイルを参照 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 複数のファイルを参照 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 単一ファイルを参照する

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![File Context Demo](assets/file-context-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

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

## 複数ファイルにまたがるインテリジェンス

ここでコンテキストが「超能力」に変わります。単一ファイルの分析も有用ですが、複数ファイルの分析は劇的な変化をもたらします。

<img src="assets/cross-file-intelligence.png" alt="複数ファイルにまたがるインテリジェンス - 単一ファイル vs 複数ファイルの分析。ファイルを一緒に分析することで、単独では見えないバグやデータフロー、パターンが明らかになる様子" width="800"/>

### デモ：複数ファイルにまたがるバグを見つける

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```
（これらのファイルはどう連携している？データフローはどうなってる？）

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Multi-File Demo](assets/multi-file-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

**Copilot CLI が発見すること**:

```
モジュール間分析
=====================

1. データフローのパターン
   book_app.py が BookCollection インスタンスを作成してメソッドを呼び出す
   books.py が BookCollection クラスを定義し、データの永続化を管理する

   フロー: book_app.py (UI) → books.py (ビジネスロジック) → data.json (ストレージ)

2. 重複している表示関数
   book_app.py:9-21    show_books() 関数
   utils.py:28-36      print_books() 関数

   影響：ほぼ同一の関数が2つ存在します。一方を更新（形式の変更など）した場合、
   もう一方も忘れずに更新する必要があります。

3. 不整合なエラーハンドリング
   book_app.py は年の変換による ValueError を処理している
   books.py はエラー時に黙って None/False を返している

   パターン：モジュール間で統一されたエラーハンドリングのアプローチがない
```

**なぜこれが重要なのか**: 単一ファイルのレビューでは、全体像を見落としてしまいます。複数ファイルの分析だけが以下を明らかにできます：
- **重複コード**: 統合すべきコード
- **データフローのパターン**: コンポーネントがどのように相互作用しているか
- **設計（アーキテクチャ）上の問題**: 保守性に影響する問題

---

### デモ：60秒でコードベースを理解する

<img src="assets/codebase-understanding.png" alt="手動でのコードレビュー（1時間）とAI支援による分析（10秒）の比較画面" width="800" />

新しいプロジェクトに参加しましたか？Copilot CLI を使って素早く把握しましょう。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```
（このアプリは何をするもので、最大の品質問題は何？1段落で教えて。）

**得られる結果**:
```
これは、ユーザーが JSON ファイルに保存された本を追加、一覧表示、削除、
検索できる CLI 版の書籍コレクション管理ツールです。主な品質問題は以下の通りです：

1. 表示ロジックの重複 - show_books() と print_books() が同じことをしている
2. 不整合なエラーハンドリング - 例外を投げるものと False を返すものが混在している
3. 入力バリデーションの欠如 - 年が 0 になったり、タイトルや著者が空でも受け付けてしまう
4. テストの欠如 - find_book_by_title などの重要な関数のテストがない

優先すべき修正：重複している表示関数の統合と、入力バリデーションの追加。
```

**結果**: 1時間のコードリーディングが10秒に圧縮されます。どこに集中すべきかが明確になります。

---

## 実践的な例

### 例 1：コンテキストを用いたコードレビュー

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI はファイルの全内容を把握し、具体的なフィードバックを返します：
# 「49行目：大文字・小文字を区別する比較は本を見逃す可能性があります……」
# 「29行目：JSON デコードエラーはキャッチされていますが、データの破損はログに記録されていません……」

> What about @samples/book-app-project/book_app.py?

# books.py のコンテキストを維持したまま、book_app.py をレビューします
```

### 例 2：コードベースの理解

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI は books.py を読み、BookCollection クラスを理解します

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI はディレクトリをスキャンして要約します

> How does the app save and load books?

# Copilot CLI は、すでに見たコードを辿って説明できます
```

<details>
<summary>🎬 複数回のやり取り（マルチターン会話）を見てみよう！</summary>

![Multi-Turn Demo](assets/multi-turn-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

### 例 3：複数ファイルにまたがるリファクタリング

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.
```
（重複している表示関数 show_books と print_books があるね。これらを統合するのを手伝って。）

---

## セッション管理

作業を進めると、セッションは自動的に保存されます。以前のセッションを再開して、中断したところから続けることができます。

### セッションの自動保存

すべての会話は自動的に保存されます。通常通り終了するだけです：

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... 何らかの作業をする ...]

> /exit
```

### 直近のセッションを再開する

```bash
# 中断したところから再開
copilot --continue
```

### 特定のセッションを再開する

```bash
# セッションのリストから対話的に選択
copilot --resume

# -r は --resume のショートカットです（入力を節約できます！）
copilot -r

# またはセッション ID を指定して再開
copilot --resume=abc123

# またはセッションに付けた名前を指定して再開
copilot --resume="my book app review"
```

> 💡 **セッション ID はどうやって調べますか？** 覚える必要はありません。ID なしで `copilot --resume` を実行すると、以前のセッションの名前、ID、最終アクティブ日時がリスト形式で表示されます。そこから選ぶだけです。
>
> **複数のターミナルを使っている場合は？** 各ターミナルウィンドウは、それぞれ独自のコンテキストを持つ個別のセッションになります。3つのターミナルで Copilot CLI を開いていれば、それは3つの別々のセッションです。どのターミナルからでも `--resume` を実行すれば、それらすべてをブラウズできます。`--continue` フラグは、まず現在の作業ディレクトリのセッションを取得しようとし、そこにセッションが存在しない場合は、最後にアクティブだったセッションを選択します。
>
> **再起動せずにセッションを切り替えられますか？** はい。アクティブなセッション内から `/resume` スラッシュコマンドを使用してください：
> ```
> > /resume
> # 切り替え可能なセッションリストが表示されます
> ```

### セッションを整理する

後で見つけやすいように、セッションに意味のある名前を付けましょう。セッションの起動時に名前を指定することもできますし、セッションの中からいつでも名前を変更することができます：

```bash
# 起動時に直接セッション名を指定する
copilot --name book-app-review

# またはセッションの中から名前を変更する
copilot

> /rename book-app-review
# 識別しやすくするためにセッション名を変更
```

セッションに名前を付けると、リストから探すことなく名前を指定して直接再開できます：

```bash
copilot --resume=book-app-review
```

不要になったセッションを整理するには、セッション内から `/session delete` を使用します：

```bash
copilot

> /session delete            # 現在のセッションを削除
> /session delete abc123     # 指定した ID のセッションを削除
> /session delete-all        # すべてのセッションを削除（注意して使用してください！）
```

### セッション間の永続メモリ

セッションは会話履歴を保存しますが、**メモリ（Memory）**はさらに一歩進んで、単一のセッション内だけでなく、*すべてのセッション間で*設定や事実を Copilot CLI に記憶させることができます。

```bash
copilot

> /memory show
# Copilot CLI が現在あなたやプロジェクトについて記憶している内容を表示します

> /memory on
# メモリ機能を有効にします（アカウントが対応している場合、デフォルトでオンになっています）

> /memory off
# メモリ機能を無効にします（毎回クリーンな状態から始めたい場合に便利です）
```

たとえば、Copilot CLI に「Python のテストには常に pytest を好んで使用します」と伝えると、その設定が記憶され、将来のセッションで自動的に適用されます。毎回同じことを繰り返す必要はありません。

> 💡 **メモリとセッションの違い**: セッションは特定のタスクを再開できるように会話履歴を保存します。メモリは、Copilot が将来の作業で適用できる、再利用可能なリポジトリの事実やユーザー設定を保存します。セッションは「タスクごとのノート」、メモリは「セッションを越えて持ち運べる再利用可能なコンテキスト」と考えてください。

### コンテキストの確認と管理

ファイルや会話を追加していくと、Copilot CLI の[コンテキストウィンドウ](../GLOSSARY.md#context-window)がいっぱいになります。コントロールを維持するためにいくつかのコマンドが用意されています：

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 現在のセッションを破棄（履歴は保存されない）し、新しく開始

> /new
# 現在のセッションを終了（履歴に保存され、検索・再開が可能）し、新しく開始

> /rewind
# タイムラインピッカーを開き、会話の以前の時点までロールバック（巻き戻し）できる
```

> 💡 **`/clear` と `/new` の使い分け**: `books.py` のレビューを終えて `utils.py` の議論に移りたいときは、まず `/new`（または履歴が不要なら `/clear`）を実行してください。そうしないと、古いトピックの不要なコンテキストが回答を混乱させる可能性があります。

> 💡 **間違えた、あるいは別のアプローチを試したい？** `/rewind`（または Esc キーを2回押す）を使って **タイムラインピッカー** を開いてください。直近だけでなく、会話のどの時点にも戻ることができます。間違った方向に進んでしまったときに、最初からやり直すことなく戻るのに便利です。

---

### 中断したところから再開する

<img src="assets/session-persistence-timeline.png" alt="GitHub Copilot CLI のセッションが数日間にわたって持続する様子。月曜日に開始し、水曜日にフルコンテキストで再開するタイムライン" width="800"/>

*終了時にセッションは自動保存されます。数日後でも、ファイル、課題、進捗状況をすべて覚えた状態で再開できます。*

数日間にわたる次のようなワークフローを想像してみてください：

```bash
# 月曜日：起動時に名前を指定して書籍アプリのレビューを開始
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

発見された品質問題：
1. 表示関数の重複 (book_app.py と utils.py) - 中
2. 空文字列に対する入力バリデーションがない - 中
3. 年が 0 や負の数になる可能性がある - 低
4. すべての関数に型ヒントがない - 低
5. エラーログの欠如 - 低

> Fix issue #1 (duplicate functions)
# 修正作業を行う...

> /exit
```

```bash
# 水曜日：名前を指定して、中断したところから正確に再開
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?
（レビューで見つかった未修正の課題は何？）

book-app-review セッションの残りの課題：
2. 空文字列に対する入力バリデーションがない - 中
3. 年が 0 や負の数になる可能性がある - 低
4. すべての関数に型ヒントがない - 低
5. エラーログの欠如 - 低

課題 #1（関数の重複）は月曜日に修正済みです。

> Let's tackle issue #2 next
```

**なぜこれが強力なのか**: 数日後でも、Copilot CLI は以下を覚えています：
- 作業していた正確なファイル
- 番号付けされた課題リスト
- どれをすでに対処したか
- 会話の文脈（コンテキスト）

説明し直す必要も、ファイルを読み直す必要もありません。ただ作業を続けるだけです。

---

**🎉 これで基本はマスターです！** `@` 構文、セッション管理（`--name`/`--continue`/`--resume`/`/rename`）、およびコンテキストコマンド（`/context`/`/clear`）を知っていれば、十分に生産性を高めることができます。これ以降の内容はオプションです。準備ができたら戻ってきてください。

---

# オプション：さらに深く知る

<img src="assets/optional-going-deeper.png" alt="コンテキストの概念を深く探求することを表す、青と紫のトーンの抽象的なクリスタルの洞窟" width="800"/>

これらのトピックは、上記の基本を発展させたものです。**興味のあるものを選ぶか、[練習](#練習)へ進んでください。**

| 知りたい内容 | リンク |
|---|---|
| ワイルドカードパターンと高度なセッションコマンド | [追加の @ パターンとセッションコマンド](#additional-patterns) |
| 複数のプロンプトにわたるコンテキストの構築 | [コンテキストを意識した会話](#context-aware-conversations) |
| トークン制限と `/compact` | [コンテキストウィンドウを理解する](#understanding-context-windows) |
| 参照すべき適切なファイルの選び方 | [何を参照するか選ぶ](#choosing-what-to-reference) |
| スクリーンショットやモックアップの分析 | [画像を扱う](#working-with-images) |

<details>
<summary><strong>追加の @ パターンとセッションコマンド</strong></summary>
<a id="additional-patterns"></a>

### 追加の @ パターン

パワーユーザー向けに、Copilot CLI はワイルドカードパターンや画像参照もサポートしています：

| パターン | 何をするか |
|---------|--------------|
| `@folder/*.py` | フォルダ内のすべての .py ファイル |
| `@**/test_*.py` | 再帰的ワイルドカード：場所を問わずすべてのテストファイルを検索 |
| `@image.png` | UI レビュー用の画像ファイル |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### セッション情報の表示

```bash
copilot

> /session
# 現在のセッションの詳細とワークスペースの概要を表示

> /usage
# セッションのメトリクスと統計を表示
```

### セッションを共有する

```bash
copilot

> /share file ./my-session.md
# セッションを Markdown ファイルとしてエクスポート

> /share gist
# セッションを含む GitHub Gist を作成

> /share html
# セッションを、それだけで動作する対話型の HTML ファイルとしてエクスポート
# 磨き上げたセッションレポートをチームメイトと共有したり、参照用に保存したりするのに便利です
```

</details>

<details>
<summary><strong>コンテキストを意識した会話</strong></summary>
<a id="context-aware-conversations"></a>

### コンテキストを意識した会話

本当の魔法は、互いに積み重なっていくマルチターン会話（複数回のやり取り）で起こります。

#### 例：段階的な機能強化

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "機能的には問題なさそうですが、以下の点が気になります：
1. いくつかのメソッドに型ヒントがない
2. タイトルや著者が空の場合のバリデーションがない
3. より良いエラーハンドリングができる可能性がある"

> Add type hints to all methods

Copilot CLI: "完全な型ヒントを追加したクラスは以下の通りです……"
[型付きのバージョンを表示]

> Now improve error handling

Copilot CLI: "型付きバージョンに基づき、改善されたエラーハンドリングは以下の通りです……"
[バリデーションと適切な例外を追加]

> Generate tests for this final version

Copilot CLI: "型とエラーハンドリングが追加されたクラスに基づき……"
[包括的なテストを生成]
```

各プロンプトが前の作業に基づいていることに注目してください。これがコンテキストの力です。

</details>

<details>
<summary><strong>コンテキストウィンドウを理解する</strong></summary>
<a id="understanding-context-windows"></a>

### コンテキストウィンドウを理解する

基本セクションで `/context` と `/clear` について学びました。ここでは、コンテキストウィンドウの仕組みをより深く見ていきます。

すべての AI には「コンテキストウィンドウ」があります。これは一度に考慮できるテキストの量です。

<img src="assets/context-window-visualization.png" alt="コンテキストウィンドウの可視化" width="800"/>

*コンテキストウィンドウは机のようなものです。一度に乗せられる量には限りがあります。ファイル、会話履歴、システムプロンプトがすべてスペースを占有します。*

#### 制限に達すると何が起きるか

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# ファイルや会話を追加するにつれて、この数値が増えます

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 警告：コンテキスト制限に近づいています

> @another-large-file.py

Context limit reached. Older context will be summarized.
（コンテキスト制限に達しました。古い内容は要約されます。）
```

#### `/compact` コマンド

コンテキストがいっぱいになりつつあるけれど会話を失いたくない場合、`/compact` は履歴を要約してトークンを解放します：

```bash
copilot

> /compact
# 会話履歴を要約し、コンテキストのスペースを解放します
# 重要な発見や決定事項は維持されます
```

また、`/compact` にオプションでフォーカス指示（focus instructions）を与えて、要約で何を優先するかを指示することもできます：

```bash
copilot

> /compact focus on the list of bugs we found and decisions made
# 発見したバグの一覧と決定事項を重点的に残して、履歴を要約します
```

> 💡 **フォーカス指示はいつ使うべきか？**: 会話の中でさまざまなトピックを扱った場合、フォーカス指示を使用することで、次のステップに最も関連する部分を `/compact` に優先して保持させ、話の文脈を見失わないようにすることができます。

#### コンテキストを効率的に使うコツ

| 状況 | アクション | 理由 |
|-----------|--------|-----|
| 新しいトピックを始める | `/clear` | 無関係なコンテキストを削除 |
| 間違った方向に進んだ | `/rewind` | 以前の時点までロールバック |
| 長い会話 | `/compact` | 履歴を要約し、トークンを解放 |
| 特定のファイルが必要 | `@folder/` ではなく `@file.py` | 必要なものだけを読み込む |
| 制限に達した | `/new` または `/clear` | コンテキストをリフレッシュ |
| 複数のトピック | トピックごとに `/rename` | 正しいセッションを再開しやすい |

#### 大規模なコードベースでのベストプラクティス

1. **具体的に指定する**: `@samples/book-app-project/` ではなく `@samples/book-app-project/books.py` を使う
2. **トピックごとにコンテキストをクリアする**: 焦点を切り替えるときは `/new` または `/clear` を使う
3. **`/compact` を活用する**: 会話を要約してコンテキストを解放する
4. **複数のセッションを使い分ける**: 機能やトピックごとにセッションを分ける

</details>

<details>
<summary><strong>何を参照するか選ぶ</strong></summary>
<a id="choosing-what-to-reference"></a>

### 何を参照するか選ぶ

コンテキストに関しては、すべてのファイルが平等なわけではありません。賢く選ぶ方法は以下の通りです：

#### ファイルサイズの考慮事項

| ファイルサイズ | およその[トークン](../GLOSSARY.md#token)数 | 戦略 |
|-----------|-------------------|----------|
| 小 (<100 行) | 〜500-1,500 トークン | 自由に使用 |
| 中 (100-500 行) | 〜1,500-7,500 トークン | 特定のファイルを参照 |
| 大 (500+ 行) | 7,500+ トークン | 選択的に使用し、特定のファイルに絞る |
| 特大 (1000+ 行) | 15,000+ トークン | 分割するか、特定のセクションを狙うことを検討 |

**具体的な例:**
- 書籍アプリの4つの Python ファイルの合計 ≈ 2,000-3,000 トークン
- 一般的な Python モジュール (200 行) ≈ 3,000 トークン
- Flask API ファイル (400 行) ≈ 6,000 トークン
- `package.json` ≈ 200-500 トークン
- 短いプロンプト ＋ 回答 ≈ 500-1,500 トークン

> 💡 **コードの簡易見積もり**: コードの行数に約15を掛けると、およそのトークン数になります。あくまで目安です。

#### 含めるべきもの vs. 除外すべきもの

**価値が高い**（含めるべき）：
- エントリポイント (`book_app.py`, `main.py`, `app.py`)
- 質問している特定のファイル
- 対象ファイルから直接インポートされているファイル
- 設定ファイル (`requirements.txt`, `pyproject.toml`)
- データモデルや dataclass

**価値が低い**（除外を検討すべき）：
- 生成されたファイル（コンパイル後の出力、バンドルされたアセット）
- `node_modules` や vendor ディレクトリ
- 大きなデータファイルやフィクスチャ
- 質問に関係のないファイル

#### 具体性のスペクトラム

```
具体性が低い ────────────────────────► 具体性が高い
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ すべてをスキャンする                  └─ 必要な箇所だけ
        (コンテキストを多く消費)                   (コンテキストを節約)
```

**広範囲に指定する場合** (`@samples/book-app-project/`)：
- 初期段階のコードベース探索
- 多くのファイルにわたるパターンの検索
- アーキテクチャのレビュー

**具体的に指定する場合** (`@samples/book-app-project/books.py`)：
- 特定の課題のデバッグ
- 特定のファイルのコードレビュー
- 単一の関数についての質問

#### 実践例：段階的なコンテキストの読み込み

```bash
copilot

# ステップ 1：構造から始める
> @package.json What frameworks does this project use?

# ステップ 2：回答に基づいて絞り込む
> @samples/book-app-project/ Show me the project structure

# ステップ 3：重要な箇所に焦点を当てる
> @samples/book-app-project/books.py Review the BookCollection class

# ステップ 4：必要に応じて関連ファイルのみ追加する
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

この段階的なアプローチにより、コンテキストを焦点が絞られた効率的な状態に保つことができます。

</details>

<details>
<summary><strong>画像を扱う</strong></summary>
<a id="working-with-images"></a>

### 画像を扱う

`@` 構文を使用して、または単に**クリップボードから貼り付ける**（Cmd+V / Ctrl+V）ことで、会話に画像を含めることができます。Copilot CLI はスクリーンショット、モックアップ、図などを分析し、UI のデバッグ、デザインの実装、エラー分析をサポートできます。

```bash
copilot

> @assets/screenshot.png What is happening in this image?

> @assets/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **さらに詳しく**: サポートされている形式、実践的なユースケース、画像とコードを組み合わせるコツについては、[追加のコンテキスト機能](../appendices/additional-context.ja.md#working-with-images)を参照してください。

</details>

---

# 練習

<img src="../assets/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

コンテキストとセッション管理のスキルを応用してみましょう。

---

## ▶️ 自分で試してみる

### プロジェクト全体のレビュー

このコースには、直接レビューできるサンプルファイルが含まれています。Copilot を起動し、以下のプロンプトを実行してみてください：

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI は以下のような課題を特定します：
# - 表示関数の重複
# - 入力バリデーションの欠如
# - 不整合なエラーハンドリング
```

> 💡 **自分のファイルで試したい場合** は、小さな Python プロジェクト (`mkdir -p my-project/src`) を作成し、いくつか .py ファイルを追加してから、`@my-project/src/` を使ってレビューしてみてください。Copilot にサンプルコードを作らせることもできます！

### セッションのワークフロー

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI がバリデーションのアプローチを提案]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 後で - 中断したところから再開
copilot --continue

> Generate tests for the changes we made
```

---

デモが終わったら、次のようなバリエーションも試してみてください：

1. **複数ファイル・チャレンジ**: `book_app.py` と `books.py` がどう連携しているか分析しましょう：
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **セッション・チャレンジ**: セッションを開始し、`/rename my-first-session` で名前を付け、何か作業をして `/exit` で終了します。その後 `copilot --continue` を実行してください。何をしていたか覚えていますか？

3. **コンテキスト・チャレンジ**: セッションの途中で `/context` を実行します。トークンをどれくらい使っていますか？`/compact` を試してから再度確認してください。（`/compact` については「さらに深く知る」の「コンテキストウィンドウを理解する」を参照。）

**自己チェック**: なぜ各ファイルを個別に開くよりも `@folder/` の方が強力なのかを説明できれば、コンテキストを理解したと言えます。

---

## 📝 課題

### メインチャレンジ：データフローを追跡する

ハンズオンではコード品質のレビューや入力バリデーションに焦点を当てました。今度は、データがアプリ内をどう移動するかを追跡することで、同じコンテキストスキルを練習しましょう：

1. 対話型セッションを開始する：`copilot`
2. `books.py` と `book_app.py` を一緒に参照する：
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
   （ユーザー入力から data.json に保存されるまで、本がどう動くか辿って。各ステップでどの関数が関わっている？）
3. さらなるコンテキストとしてデータファイルを取り込む：
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
   （この JSON ファイルがなかったり壊れていたりしたら何が起きる？どの関数が失敗する？）
4. 複数ファイルにまたがる改善を求める：
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
   （両方のファイルで機能する、一貫したエラーハンドリング戦略を提案して。）
5. セッションの名前を変更する：`/rename data-flow-analysis`
6. `/exit` で終了し、`copilot --continue` で再開して、データフローに関する追加の質問をする。

**成功基準**: 複数のファイルにまたがってデータを追跡でき、名前付きセッションを再開し、複数ファイルに基づいた提案を得られること。

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**開始方法:**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

再開：`copilot --continue`

**便利なコマンド:**
- `@file.py` - 単一ファイルを参照
- `@folder/` - フォルダ内の全ファイルを参照（末尾の `/` を忘れずに）
- `/context` - コンテキストの使用量を確認
- `/rename <名前>` - 簡単に再開できるようにセッションに名前を付ける

</details>

### ボーナスチャレンジ：コンテキストの限界

1. `@samples/book-app-project/` を使って書籍アプリのすべてのファイルを一度に参照します。
2. 異なるファイル（`books.py`, `utils.py`, `book_app.py`, `data.json`）についていくつか詳細な質問をします。
3. `/context` を実行して使用量を確認します。どれくらい早くたまりますか？
4. `/compact` を使ってスペースを確保し、会話を続ける練習をします。
5. ディレクトリ全体ではなく、より具体的なファイル参照（例：`@samples/book-app-project/books.py`）を試してみて、コンテキストの使用量にどう影響するか確認します。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong> (クリックして展開)</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| ファイル名の前の `@` を忘れる | Copilot CLI は "books.py" をただのテキストとして扱います | ファイル参照には `@samples/book-app-project/books.py` を使います |
| セッションが自動的に引き継がれると思い込む | 単に `copilot` と始めると、以前のコンテキストは失われます | `--continue`（直近）または `--resume`（選択）を使います |
| カレントディレクトリ外のファイルを参照する | 「Permission denied」や「File not found」エラーが出ます | `/add-dir /パス/トウ/ディレクトリ` でアクセスを許可します |
| トピックを切り替えるときに `/clear` を使わない | 古いコンテキストが新しいトピックの回答を混乱させます | 別のタスクを始める前に `/clear` を実行します |

### トラブルシューティング

**「File not found」エラー** - 正しいディレクトリにいるか確認してください：

```bash
pwd  # 現在のディレクトリを確認
ls   # ファイルを一覧表示

# その後 Copilot を起動し、相対パスを使います
copilot

> Review @samples/book-app-project/books.py
```

**「Permission denied」** - 許可リストにディレクトリを追加してください：

```bash
copilot --add-dir /path/to/directory

# またはセッション内で：
> /add-dir /path/to/directory
```

**コンテキストがすぐにいっぱいになる場合**:
- より具体的なファイル参照を心がける
- トピックごとに `/clear` を使う
- 複数のセッションに作業を分ける

</details>

---

# まとめ

## 🔑 重要なポイント

1. **`@` 構文** は、Copilot CLI にファイル、ディレクトリ、画像に関するコンテキストを与えます。
2. **マルチターン会話** は、コンテキストが蓄積されるにつれて互いに積み重なっていきます。
3. **セッションは自動保存されます**: 起動時に `--name` で名前を指定したり、名前を指定して `--resume=<name>` で再開したり、`--continue` で直近のセッションを再開することができます。
4. **コンテキストウィンドウ** には制限があります：`/clear`, `/compact`, `/context`, `/new`, `/rewind` で管理しましょう。要約に残す内容を調整するには `/compact focus on <トピック>` を使用します。
5. **永続メモリ** (`/memory`) は、現在のセッションだけでなく、*すべての*セッション間で設定や事実を Copilot CLI に記憶させることができます。
6. **権限フラグ** (`--add-dir`, `--allow-all`) は、複数ディレクトリへのアクセスを制御します。賢く使いましょう！
7. **画像参照** (`@screenshot.png`) は、UI の問題を視覚的にデバッグするのに役立ちます。

> 📚 **公式ドキュメント**: コンテキスト、セッション、ファイルの扱いに関する完全なリファレンスは、[Use Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli)（英語）を参照してください。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## ➡️ 次は？

Copilot CLI にコンテキストを伝えられるようになったところで、次はそれを実際の開発タスクに活用しましょう。今学んだコンテキストのテクニック（ファイル参照、複数ファイル分析、セッション管理）は、次の章で学ぶ強力なワークフローの基礎となります。

**[第03章：開発ワークフロー](../03-development-workflows/README.ja.md)** では以下を学びます：

- コードレビューのワークフロー
- リファクタリングのパターン
- デバッグ支援
- テスト生成
- Git 連携

---

**[← 第01章に戻る](../01-setup-and-first-steps/README.ja.md)** | **[第03章へ進む →](../03-development-workflows/README.ja.md)**
