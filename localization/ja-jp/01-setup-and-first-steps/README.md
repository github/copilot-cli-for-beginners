![第 01 章: はじめの一歩](../../../01-setup-and-first-steps/images/chapter-header.png)

> **AI がバグを即座に発見し、わかりにくいコードを説明し、動作するスクリプトを生成する様子をご覧ください。そして GitHub Copilot CLI の 3 つの使い方を学びましょう。**

この章から本当の楽しさが始まります！GitHub Copilot CLI を「シニアエンジニアをスピードダイヤルに登録している」と表現する開発者の理由を、実際に体験していただきます。AI がセキュリティバグを数秒で見つけ、複雑なコードを平易な言葉で説明し、動作するスクリプトを即座に生成する様子を見た後、3 つのインタラクションモード（インタラクティブ、プラン、プログラマティック）をマスターして、どのタスクにどのモードを使えばよいか正確に理解しましょう。

> ⚠️ **前提条件**: 先に **[第 00 章: クイックスタート](../00-quick-start/README.md)** を完了していることを確認してください。以下のデモを実行するには、GitHub Copilot CLI がインストールされ、認証済みである必要があります。

## 🎯 学習目標

この章を終えると、以下ができるようになります。

- ハンズオンデモを通じて GitHub Copilot CLI が提供する生産性向上を体験する
- タスクに応じて適切なモード（インタラクティブ、プラン、プログラマティック）を選択する
- スラッシュコマンドでセッションを制御する

> ⏱️ **目安時間**: 約 45 分（15 分読む + 30 分ハンズオン）

---

# はじめての Copilot CLI 体験

<img src="../../../01-setup-and-first-steps/images/first-copilot-experience.png" alt="モニターにコードを映し AI 支援を表す輝く粒子に囲まれてデスクに座る開発者" width="800"/>

Copilot CLI が何をできるか、すぐに試してみましょう。

---

## まず慣れる: 最初のプロンプト

インパクトのあるデモに入る前に、今すぐ試せるシンプルなプロンプトから始めましょう。**コードリポジトリは不要です**！ターミナルを開いて Copilot CLI を起動するだけです。

```bash
copilot
```

初心者向けのプロンプトを試してみましょう。

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Python を使っていない場合も大丈夫！使いたい言語について質問するだけです。

どれほど自然に感じるか気づいてください。同僚に話しかけるように質問するだけです。探索し終わったら `/exit` と入力してセッションを終了しましょう。

**重要なポイント**: GitHub Copilot CLI は会話型です。始めるのに特別な構文は必要ありません。平易な言葉で質問するだけです。

## 実際の動作を見てみる

開発者が「シニアエンジニアをスピードダイヤルに登録している」と表現する理由を見てみましょう。

> 📖 **例の読み方**: `>` で始まる行は、インタラクティブな Copilot CLI セッション内で入力するプロンプトです。`>` プレフィックスのない行は、ターミナルで実行するシェルコマンドです。

> 💡 **出力例について**: このコース全体で示すサンプル出力はあくまで例示用です。Copilot CLI のレスポンスは毎回異なるため、文言、フォーマット、詳細度は異なります。正確なテキストではなく、返される*情報の種類*に注目してください。

### デモ 1: 数秒でコードレビュー

コースには、意図的にコード品質の問題が含まれたサンプルファイルが含まれています。ローカルマシンで作業していてまだリポジトリをクローンしていない場合は、以下の `git clone` コマンドを実行し、`copilot-cli-for-beginners` フォルダに移動してから `copilot` コマンドを実行してください。

```bash
# ローカルで作業していてまだクローンしていない場合
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Copilot を起動する
copilot
```

インタラクティブな Copilot CLI セッションに入ったら、以下を実行します。

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 記号は何に使うのか？** `@` 記号は Copilot CLI にファイルを読むよう指示します。これについては第 02 章で詳しく学びます。今はコマンドをそのままコピーするだけで大丈夫です。

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![コードレビューデモ](../../../01-setup-and-first-steps/images/code-review-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

**ポイント**: 数秒でプロフェッショナルなコードレビューが完成。手動レビューではもっと時間がかかります！

---

### デモ 2: わかりにくいコードを説明する

コードを見てもよくわからないことがありますか？Copilot CLI セッションで試してみましょう。

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![コード説明デモ](../../../01-setup-and-first-steps/images/explain-code-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

**何が起こるか**（出力は異なります）: Copilot CLI がファイルを読み込み、コードを理解し、平易な言葉で説明します。

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**ポイント**: 複雑なコードを、丁寧に説明してくれるメンターのように解説してくれます。

---

### デモ 3: 動作するコードを生成する

15 分かけて検索しなければならないような関数が必要ですか？セッションを続けて試してみましょう。

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![コード生成デモ](../../../01-setup-and-first-steps/images/generate-code-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

**何が起こるか**: 数秒で完全な動作するコードが生成され、コピーして実行できます。

探索し終わったら、セッションを終了しましょう。

```
> /exit
```

**ポイント**: 即座に結果が得られ、一つのセッションを通じて作業が完了しました。

---

# モードとコマンド

<img src="../../../01-setup-and-first-steps/images/modes-and-commands.png" alt="Copilot CLI のモードとコマンドを表す光るスクリーン、ダイヤル、イコライザーを備えた未来的なコントロールパネル" width="800"/>

Copilot CLI でできることを体験しました。次は、これらの機能を効果的に使う*方法*を理解しましょう。重要なのは、状況に応じて 3 つのインタラクションモードのどれを使うかを知ることです。

> 💡 **注意**: Copilot CLI には、入力を待たずにタスクを進める**オートパイロット**モードもあります。強力ですが、フルアクセス権の付与が必要で、プレミアムリクエストを自律的に使用します。このコースでは下記の 3 つのモードに焦点を当てます。基本に慣れてからオートパイロットを紹介します。

---

## 🧩 現実世界のたとえ話: 外食する

GitHub Copilot CLI の使い方を、外食に例えてみましょう。計画から注文まで、状況によって適したアプローチが異なります。

| モード | 外食のたとえ | 使う場面 |
|------|----------------|-------------|
| **プラン** | レストランへの GPS ルート | 複雑なタスク - ルートを確認し、経由地をチェックし、計画に合意してから出発 |
| **インタラクティブ** | ウェイターと話す | 探索と反復 - 質問し、カスタマイズし、リアルタイムフィードバックを得る |
| **プログラマティック** | ドライブスルーで注文 | 素早い特定タスク - 環境から離れずに素早く結果を得る |

外食のように、どのアプローチが適切か自然にわかるようになります。

<img src="../../../01-setup-and-first-steps/images/ordering-food-analogy.png" alt="GitHub Copilot CLI の 3 つの使い方 - プランモード（GPS ルート）、インタラクティブモード（ウェイターと話す）、プログラマティックモード（ドライブスルー）" width="800"/>

*タスクに応じてモードを選択: まず計画するならプラン、対話型の共同作業ならインタラクティブ、素早い一発勝負ならプログラマティック*

### どのモードから始めればよい？

**インタラクティブモードから始めましょう。**
- 実験して追加質問ができます
- 会話を通じてコンテキストが自然に積み上がります
- ミスは `/clear` で簡単に修正できます

慣れてきたら試してみましょう。
- **プログラマティックモード** (`copilot -p "<プロンプト>"`) - 素早い一発の質問に
- **プランモード** (`/plan`) - コーディング前に詳細な計画が必要な場合に

---

## 3 つのモード

### モード 1: インタラクティブモード（まずここから）

<img src="../../../01-setup-and-first-steps/images/interactive-mode.png" alt="インタラクティブモード - 質問に答えて注文を調整できるウェイターと話すような感覚" width="250"/>

**最適な用途**: 探索、反復、複数ターンの会話。質問に答え、フィードバックを受け取り、注文をその場で調整できるウェイターと話すような感覚です。

インタラクティブセッションを開始する:

```bash
copilot
```

ここまで見てきたように、自然にタイプできるプロンプトが表示されます。利用可能なコマンドのヘルプを表示するには:

```
> /help
```

**重要なポイント**: インタラクティブモードはコンテキストを維持します。各メッセージは前のメッセージを積み上げます。まさに本物の会話のようです。

#### インタラクティブモードの例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

各プロンプトが前の回答を積み上げていることに注目してください。毎回最初からやり直すのではなく、会話をしているのです。

---

### モード 2: プランモード

<img src="../../../01-setup-and-first-steps/images/plan-mode.png" alt="プランモード - GPS を使って旅行前にルートを計画するような感覚" width="250"/>

**最適な用途**: 実行前にアプローチを確認したい複雑なタスク。GPS を使って旅行前にルートを計画するような感覚です。

プランモードは、コードを書く前にステップバイステップの計画を作成するのに役立ちます。`/plan` コマンドを使うか、**Shift+Tab** を押してプランモードに切り替えます。

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **ヒント**: **Shift+Tab** でモードが切り替わります: インタラクティブ → プラン → オートパイロット。インタラクティブセッション中にいつでも押してコマンドを入力せずにモードを切り替えられます。

`--plan` フラグを使って Copilot CLI をプランモードで直接起動することもできます。

```bash
copilot --plan
```

**プランモードの出力:**（実際の出力は異なる場合があります）

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**重要なポイント**: プランモードを使うと、コードが書かれる前にアプローチを確認・修正できます。計画が完成したら、後で参照するためにファイルに保存するよう Copilot CLI に指示することもできます。たとえば「Save this plan to `mark_as_read_plan.md`」と言えば、計画の詳細が含まれた Markdown ファイルが作成されます。

> 💡 **もっと複雑なことを試したいですか？** `/plan Add search and filter capabilities to the book app` を試してみましょう。プランモードは、シンプルな機能からフルアプリケーションまでスケールします。

> 📚 **オートパイロットモード**: Shift+Tab で **オートパイロット**という 3 番目のモードに切り替わることに気づいたかもしれません。オートパイロットモードでは、各ステップの後に入力を待たずに計画全体を実行します。これは「タスクをお願いして、終わったら教えて」と同僚に伝えるようなものです。典型的なワークフローは「計画 → 承認 → オートパイロット」で、まず計画を上手に書く必要があります。`copilot --autopilot` でオートパイロットに直接起動することもできます。まずインタラクティブモードとプランモードに慣れてから、準備ができたら[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)を参照してください。

---

### モード 3: プログラマティックモード

<img src="../../../01-setup-and-first-steps/images/programmatic-mode.png" alt="プログラマティックモード - ウェイターと話さずに素早く注文するドライブスルーのような感覚" width="250"/>

**最適な用途**: 自動化、スクリプト、CI/CD、一発のコマンド。ウェイターと話さずに素早く注文するドライブスルーのような感覚です。

インタラクションが不要な一発コマンドには `-p` フラグを使います。

```bash
# コードを生成する
copilot -p "Write a function that checks if a number is even or odd"

# 素早いヘルプを得る
copilot -p "How do I read a JSON file in Python?"
```

**重要なポイント**: プログラマティックモードは素早く回答して終了します。会話なし、入力 → 出力のみです。

<details>
<summary>📚 <strong>さらに進む: スクリプトでのプログラマティックモードの使用</strong>（クリックして展開）</summary>

慣れてきたら、シェルスクリプトで `-p` を使えます。

```bash
#!/bin/bash

# コミットメッセージを自動生成する
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# ファイルをレビューする
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **`--allow-all` について**: このフラグはすべてのアクセス許可プロンプトをスキップし、Copilot CLI がファイルを読んだり、コマンドを実行したり、URL にアクセスしたりするのを確認なしで行えるようにします。これは、インタラクティブなセッションがないプログラマティックモード（`-p`）で必要です。`--allow-all` は自分で書いたプロンプトに対して、信頼できるディレクトリでのみ使用してください。信頼できない入力や機密性の高いディレクトリでは絶対に使用しないでください。

</details>

---

## 主要なスラッシュコマンド

Copilot CLI を使い始める際にまず覚えておくべきコマンドです。

| コマンド | 機能 | 使う場面 |
|---------|--------------|-------------|
| `/ask` | 会話履歴に影響を与えずに素早く質問する | 現在のタスクを中断せずに素早く答えが欲しいとき |
| `/clear` | 会話をクリアして最初からやり直す | 話題を切り替えるとき |
| `/help` | 利用可能なコマンドをすべて表示する | コマンドを忘れたとき |
| `/model` | AI モデルを表示または切り替える | AI モデルを変更したいとき |
| `/plan` | コーディング前に作業を計画する | 複雑な機能の場合 |
| `/research` | GitHub とウェブソースを使って深い調査をする | コーディング前にトピックを調査する必要があるとき |
| `/exit` | セッションを終了する | 作業が終わったとき |

> 💡 **`/ask` と通常のチャットの違い**: 通常、送るすべてのメッセージは継続的な会話の一部となり、将来のレスポンスに影響します。`/ask` は「オフレコード」のショートカットで、`/ask What does YAML mean?` のような一発の質問に最適です。セッションのコンテキストを汚染しません。

> 💡 **タブ補完**: スラッシュコマンドを入力するときに **Tab** を押すと、コマンド名の自動補完や利用可能なサブコマンドと引数のサイクルができます。コマンドの正確な名前を覚えていないときに特に便利です。

これで始め方はわかりました！慣れてきたら、追加のコマンドを探索してみましょう。

> 📚 **公式ドキュメント**: コマンドとフラグの完全なリストは [CLI コマンドリファレンス](https://docs.github.com/copilot/reference/cli-command-reference)をご覧ください。

<details>
<summary>📚 <strong>追加コマンド</strong>（クリックして展開）</summary>

> 💡 上記の主要コマンドは日常的な使用の多くをカバーします。このリファレンスは、さらに探索したいときのためにあります。

### エージェント環境

| コマンド | 機能 |
|---------|--------------|
| `/agent` | 利用可能なエージェントを閲覧・選択する |
| `/env` | 読み込まれた環境の詳細を表示する（有効な指示、MCP サーバー、スキル、エージェント、プラグイン） |
| `/init` | リポジトリの Copilot 指示を初期化する |
| `/mcp` | MCP サーバーの設定を管理する |
| `/skills` | 機能強化のためのスキルを管理する |

> 💡 エージェントは[第 04 章](../04-agents-custom-instructions/README.md)、スキルは[第 05 章](../05-skills/README.md)、MCP サーバーは[第 06 章](../06-mcp-servers/README.md)で説明します。

### モデルとサブエージェント

| コマンド | 機能 |
|---------|--------------|
| `/delegate` | GitHub Copilot クラウドエージェントにタスクを委任する |
| `/fleet` | 複雑なタスクを並列サブタスクに分割して高速化する |
| `/model` | AI モデルを表示または切り替える |
| `/tasks` | バックグラウンドのサブエージェントとデタッチされたシェルセッションを表示する |

### コード

| コマンド | 機能 |
|---------|--------------|
| `/diff` | 現在のディレクトリで行われた変更をレビューする |
| `/pr` | 現在のブランチのプルリクエストを操作する |
| `/research` | GitHub とウェブソースを使って深い調査を実行する |
| `/review` | コードレビューエージェントを実行して変更を分析する |
| `/terminal-setup` | 複数行入力サポートを有効にする（shift+enter と ctrl+enter） |

### アクセス許可

| コマンド | 機能 |
|---------|--------------|
| `/add-dir <ディレクトリ>` | 許可リストにディレクトリを追加する |
| `/allow-all [on\|off\|show]` | すべてのアクセス許可プロンプトを自動承認する。`on` で有効化、`off` で無効化、`show` で現在の状態を確認 |
| `/yolo` | `/allow-all on` のクイックエイリアス — すべてのアクセス許可プロンプトを自動承認する |
| `/cwd`、`/cd [ディレクトリ]` | 作業ディレクトリを表示または変更する |
| `/list-dirs` | すべての許可ディレクトリを表示する |

> ⚠️ **注意して使う**: `/allow-all` と `/yolo` は確認プロンプトをスキップします。信頼できるプロジェクトには便利ですが、信頼できないコードには注意してください。

### セッション

| コマンド | 機能 |
|---------|--------------|
| `/clear` | 現在のセッションを破棄（履歴は保存されない）して新しい会話を開始する |
| `/compact` | コンテキストの使用量を削減するために会話を要約する |
| `/context` | コンテキストウィンドウのトークン使用量と可視化を表示する |
| `/keep-alive` | Copilot CLI がアクティブな間はシステムのスリープを防ぐ — ノートパソコンでの長時間タスクに便利 |
| `/new` | 現在のセッションを終了（履歴に保存して検索・再開可能）して新しい会話を開始する |
| `/resume` | 別のセッションに切り替える（セッション ID または名前を指定可） |
| `/rename` | 現在のセッションの名前を変更する（名前を省略すると自動生成） |
| `/rewind` | タイムラインピッカーを開いて会話の以前の任意の時点にロールバックする |
| `/usage` | セッションの使用メトリクスと統計を表示する |
| `/session` | セッション情報とワークスペースの概要を表示する。`/session delete`、`/session delete <id>`、または `/session delete-all` でセッションを削除 |
| `/share` | セッションを Markdown ファイル、GitHub Gist、またはスタンドアロン HTML ファイルとしてエクスポートする |

### 表示

| コマンド | 機能 |
|---------|--------------|
| `/statusline`（または `/footer`） | セッション下部のステータスバーに表示する項目をカスタマイズする（ディレクトリ、ブランチ、労力、コンテキストウィンドウ、クォータ） |
| `/theme` | ターミナルテーマを表示または設定する |

### ヘルプとフィードバック

| コマンド | 機能 |
|---------|--------------|
| `/changelog` | CLI バージョンの変更ログを表示する |
| `/feedback` | GitHub にフィードバックを送信する |
| `/help` | 利用可能なコマンドをすべて表示する |

### クイックシェルコマンド

`!` をプレフィックスとして付けることで、AI を介さずにシェルコマンドを直接実行できます。

```bash
copilot

> !git status
# git status を直接実行する（AI をバイパス）

> !python -m pytest tests/
# pytest を直接実行する
```

### モデルの切り替え

Copilot CLI は OpenAI、Anthropic、Google などの複数の AI モデルをサポートしています。利用可能なモデルはサブスクリプションのレベルと地域によって異なります。`/model` を使ってオプションを確認し、モデルを切り替えます。

```bash
copilot
> /model

# 利用可能なモデルを表示してを選択できます。Sonnet 4.5 を選択しましょう。
```

> 💡 **ヒント**: モデルによって消費する「プレミアムリクエスト」の量が異なります。**1x** マーク付きのモデル（Claude Sonnet 4.5 など）は優れたデフォルトです。高性能で効率的です。高い倍率のモデルはプレミアムリクエストのクォータをより速く消費するので、本当に必要な場合のために取っておきましょう。

> 💡 **どのモデルを選べばいいかわからない場合?** モデルピッカーで **`Auto`** を選択すると、Copilot が各セッションに最適なモデルを自動的に選択します。始めたばかりでモデル選択について考えたくない場合に最適なデフォルトです。

</details>

---

# 練習

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

学んだことを実践する時間です。

---

## ▶️ 自分で試してみよう

### インタラクティブな探索

Copilot を起動して、フォローアッププロンプトを使ってブックアプリを段階的に改善しましょう。

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 機能を計画する

`/plan` を使って、コードを書く前に Copilot CLI に実装を計画させましょう。

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# 計画を確認する
# 承認または修正する
# ステップバイステップで実装される様子を見る
```

### プログラマティックモードで自動化する

`-p` フラグを使うと、インタラクティブモードに入らずにターミナルから Copilot CLI を直接実行できます。リポジトリのルートから以下のスクリプトをターミナル（Copilot の中ではなく）にコピーして実行し、ブックアプリのすべての Python ファイルをレビューしましょう。

```bash
# ブックアプリのすべての Python ファイルをレビューする
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell（Windows）:**

```powershell
# ブックアプリのすべての Python ファイルをレビューする
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

デモを完了した後、これらのバリエーションを試してみましょう。

1. **インタラクティブチャレンジ**: `copilot` を起動してブックアプリを探索する。`@samples/book-app-project/books.py` について質問し、改善を 3 回続けてリクエストする。

2. **プランモードチャレンジ**: `/plan Add rating and review features to the book app` を実行する。計画を注意深く読む。意味があるか確認する。

3. **プログラマティックチャレンジ**: `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"` を実行する。最初の試みで動作したか確認する。

---

## 💡 ヒント: ウェブまたはモバイルから CLI セッションを制御する

GitHub Copilot CLI は**リモートセッション**をサポートしており、ターミナルにいなくても Web ブラウザ（デスクトップまたはモバイル）や GitHub Mobile アプリから実行中の CLI セッションを監視・操作できます。

`--remote` フラグでリモートセッションを開始します。

```bash
copilot --remote
```

Copilot CLI がリンクを表示し、QR コードへのアクセスを提供します。スマートフォンまたはデスクトップのブラウザタブでリンクを開くと、セッションをリアルタイムで確認し、フォローアッププロンプトを送信し、計画を確認し、リモートでエージェントを操作できます。セッションはユーザー固有なので、自分の Copilot CLI セッションにのみアクセスできます。

アクティブなセッション内からいつでもリモートアクセスを有効にすることもできます。

```
> /remote
```

リモートセッションの詳細は [Copilot CLI ドキュメント](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely)をご覧ください。

---

## 📝 課題

### メインチャレンジ: ブックアプリのユーティリティを改善する

ハンズオン例は `book_app.py` のレビューとリファクタリングに焦点を当てていました。今度は別のファイル `utils.py` で同じスキルを練習しましょう。

1. インタラクティブセッションを開始する: `copilot`
2. ファイルの概要を Copilot CLI に頼む: "Summarize @samples/book-app-project/utils.py and explain what each function in this file does"
3. 入力バリデーションの追加を頼む: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. エラーハンドリングの改善を頼む: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. ドキュメント文字列の追加を頼む: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. コンテキストがプロンプト間でどのように引き継がれるかを観察する。各改善は前のものを積み上げる
7. `/exit` で終了する

**成功基準**: 入力バリデーション、エラーハンドリング、ドキュメント文字列が追加された改善された `utils.py` ができており、すべてが複数ターンの会話で構築されています。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**試してみるサンプルプロンプト:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**よくある問題:**
- Copilot CLI が確認の質問をしてきたら、自然に答えましょう
- コンテキストは引き継がれるので、各プロンプトは前のプロンプトを積み上げます
- やり直したい場合は `/clear` を使います

</details>

### ボーナスチャレンジ: モードを比較する

例では検索機能に `/plan` を、バッチレビューに `-p` を使いました。次は、`BookCollection` クラスに `list_by_year()` メソッドを追加するという単一の新しいタスクで 3 つのモードすべてを試してみましょう。

1. **インタラクティブ**: `copilot` → ステップバイステップでメソッドを設計・構築するよう頼む
2. **プラン**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **プログラマティック**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**振り返り**: どのモードが最も自然に感じましたか？それぞれいつ使いますか？

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| `/exit` の代わりに `exit` と入力する | Copilot CLI が "exit" をコマンドではなくプロンプトとして扱う | スラッシュコマンドは常に `/` で始まります |
| 複数ターンの会話に `-p` を使う | 各 `-p` 呼び出しは独立していて前の呼び出しの記憶がない | コンテキストを積み上げる会話にはインタラクティブモード（`copilot`）を使う |
| `$` や `!` を含むプロンプトを引用符なしで使う | Copilot CLI が見る前にシェルが特殊文字を解釈する | プロンプトを引用符で囲む: `copilot -p "What does $HOME mean?"` |
| 実行中のタスクをキャンセルするために Esc を 1 回押す | 単一の Esc は実行中の作業をキャンセルしなくなった（誤操作防止のため） | Copilot CLI が処理中にキャンセルするには **Esc を 2 回**押す |

### トラブルシューティング

**「Model not available」** - サブスクリプションにすべてのモデルが含まれていない場合があります。`/model` で利用可能なものを確認してください。

**「Context too long」** - 会話がコンテキストウィンドウをすべて使い切りました。`/clear` でリセットするか、新しいセッションを開始してください。

**「Rate limit exceeded」** - 数分待ってから再試行してください。バッチ操作には遅延を入れたプログラマティックモードの使用を検討してください。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **インタラクティブモード**は探索と反復のためのものです - コンテキストは引き継がれます。これまで言ったことを覚えている相手と会話しているようなものです。
2. **プランモード**は通常、より複雑なタスクのためのものです。実装前にレビューしましょう。
3. **プログラマティックモード**は自動化のためのものです。インタラクションは不要です。
4. **主要コマンド**（`/ask`、`/help`、`/clear`、`/plan`、`/research`、`/model`、`/exit`）は日常的な使用のほとんどをカバーします。

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次のステップ

3 つのモードを理解したので、次はコードについて Copilot CLI にコンテキストを提供する方法を学びましょう。

**[第 02 章: コンテキストと会話](../02-context-conversations/README.md)**では以下を学びます。

- ファイルとディレクトリを参照するための `@` 構文
- `--resume` と `--continue` を使ったセッション管理
- コンテキスト管理が Copilot CLI を本当に強力にする仕組み

---

**[← コースホームに戻る](../README.md)** | **[第 02 章に進む →](../02-context-conversations/README.md)**
