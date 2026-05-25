![Chapter 01: First Steps](images/chapter-header.png)

> **AI が一瞬でバグを見つけ、難解なコードを説明し、動作するスクリプトを生成する様子をご覧ください。その後、GitHub Copilot CLI を使う3つの異なる方法を学びます。**

この章から、魔法が始まります！開発者が GitHub Copilot CLI を「シニアエンジニアにいつでも相談できるようなもの」と表現する理由を、あなた自身で体験することになります。AI がセキュリティ上のバグを数秒で見つけ、複雑なコードを平易な言葉で説明し、動作するスクリプトを即座に生成する様子を見ていきます。その後、3つのインタラクションモード（Interactive、Plan、Programmatic）をマスターし、どのタスクにどのモードを使うべきかを学びます。

> ⚠️ **前提条件**: まず **[第00章：クイックスタート](../00-quick-start/README.ja.md)** を完了していることを確認してください。以下のデモを実行するには、GitHub Copilot CLI がインストールされ、認証されている必要があります。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- 実践的なデモを通じて、GitHub Copilot CLI による生産性向上を体験する
- タスクに合わせて適切なモード（Interactive、Plan、または Programmatic）を選択する
- スラッシュコマンドを使用してセッションを制御する

> ⏱️ **推定所要時間**: 約45分（読みもの15分 ＋ 実践30分）

---

# はじめての Copilot CLI 体験

<img src="images/first-copilot-experience.png" alt="デスクに座る開発者。モニターにはコードが表示され、AIの支援を表す光の粒子が舞っている" width="800"/>

まずは、Copilot CLI に何ができるか見てみましょう。

---

## 基本に慣れる：最初のプロンプト

本格的なデモに入る前に、今すぐ試せる簡単なプロンプトから始めましょう。**コードリポジトリは不要です**！ターミナルを開いて Copilot CLI を起動するだけです：

```bash
copilot
```

これらの初心者向けのプロンプトを試してみてください：

```
> Explain what a dataclass is in Python in simple terms
（Python の dataclass とは何か、簡単に説明して）

> Write a function that sorts a list of dictionaries by a specific key
（辞書のリストを特定のキーでソートする関数を書いて）

> What's the difference between a list and a tuple in Python?
（Python のリストとタプルの違いは何？）

> Give me 5 best practices for writing clean Python code
（きれいな Python コードを書くためのベストプラクティスを5つ教えて）
```

Python を使っていませんか？問題ありません！お好きな言語について質問してみてください。

いかに自然に感じられるかに注目してください。同僚に質問するように聞くだけです。探索が終わったら、`/exit` と入力してセッションを終了します。

**重要な洞察**: GitHub Copilot CLI は対話型です。特別な構文を覚える必要はありません。普通の言葉で質問するだけです。

## 実際の動きを見る

では、なぜ開発者がこれを「シニアエンジニアへのホットライン」と呼ぶのか、その理由を見てみましょう。

> 📖 **例の読み方**: `>` で始まる行は、対話型の Copilot CLI セッション内で入力するプロンプトです。`>` がない行は、ターミナルで実行するシェルコマンドです。

> 💡 **出力例について**: このコースに掲載されている出力例はイメージです。Copilot CLI の回答は毎回変わるため、あなたの結果とは言葉遣いや形式、詳細が異なります。正確なテキストではなく、返される情報の *種類* に注目してください。

### デモ 1：数秒でコードレビュー

このコースには、意図的にコード品質の問題を含めたサンプルファイルが含まれています。ローカルマシンで作業していて、まだリポジトリをクローンしていない場合は、以下の `git clone` コマンドを実行し、`copilot-cli-for-beginners` フォルダに移動してから `copilot` コマンドを実行してください。

```bash
# ローカルで作業しており、まだの場合はリポジトリをクローンします
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Copilot を起動
copilot
```

対話型の Copilot CLI セッションに入ったら、以下を実行します：

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 記号は何に使うのですか？** `@` 記号は、Copilot CLI にファイルを読み込ませるためのものです。詳細は第02章で学びます。今は、表示されている通りにコマンドをコピーしてください。

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Code Review Demo](images/code-review-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

**まとめ**: 数秒でプロフェッショナルなコードレビューが完了します。手作業でのレビューなら……もっと時間がかかるはずです！

---

### デモ 2：難解なコードを解説

コードを見て「これ何をしてるんだ？」と思ったことはありませんか？Copilot CLI セッションでこれを試してみてください：

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Explain Code Demo](images/explain-code-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

**何が起きるか**: (出力は異なります) Copilot CLI がファイルを読み込み、コードを理解し、平易な言葉で説明してくれます。

```
これは Python の dataclass を使用した書籍コレクション管理モジュールです。

デジタルの本棚のようなものだと考えてください：
- Book は dataclass です。書籍情報（タイトル、著者、出版年、既読状態）を保存するためのシンプルな方法です。
- BookCollection はコレクション全体を管理し、保存や読み込みを担当します。

主な構成要素：

1. @dataclass デコレータ (8行目)
   - __init__ や __repr__ などを自動的に作成します。
   - Python でデータ構造を定義するきれいな方法です。

2. BookCollection クラス (16行目)
   - Book オブジェクトのリストを保持します。
   - JSON ファイルの入出力による永続化を処理します。
   - load_books() は data.json から読み込みます。
   - save_books() は asdict() を使って data.json に書き込みます。

3. 書籍の操作：
   - add_book() - 新しい本を作成して保存します。
   - find_book_by_title() - コレクション内を検索します。
   - mark_as_read() - 既読状態を更新します。
   - find_by_author() - 著者名でフィルタリングします。

共通パターン：JSON から読み込む → Python オブジェクトで作業する → JSON に書き戻す
```

**まとめ**: 複雑なコードも、根気強いメンターが教えてくれるように解説してくれます。

---

### デモ 3：動作するコードを生成

Google 検索で15分かかるような関数が必要ですか？セッションを続けたまま、こう聞いてみてください：

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```
（本のリストを受け取り、統計情報を返す Python 関数を書いて。合計数、既読数、未読数、最も古い本と新しい本を含めて。）

---

<details>
<summary>🎬 実際の動きを見てみよう！</summary>

![Generate Code Demo](images/generate-code-demo.gif)

*デモの出力は一例です。使用するモデルやツールによってレスポンスは異なります。*

</details>

---

**何が起きるか**: コピペしてすぐに使える、完成された関数が数秒で生成されます。

探索が終わったら、セッションを終了します：

```
> /exit
```

**まとめ**: 即座に成果が得られ、最初から最後まで一つのセッションで完結しました。

---

# モードとコマンド

<img src="images/modes-and-commands.png" alt="Copilot CLI のモードとコマンドを表す、光る画面やダイヤル、イコライザーを備えた未来的なコントロールパネル" width="800"/>

Copilot CLI に何ができるかを見てきました。次は、これらの機能をどうやって効果的に使うかを理解しましょう。鍵となるのは、状況に応じて3つのインタラクションモードを使い分けることです。

> 💡 **補足**: Copilot CLI には、ユーザーの入力を待たずにタスクを進める **Autopilot** モードもあります。非常に強力ですが、フル権限の付与が必要で、プレミアムリクエストを自律的に使用します。このコースでは、基本となる以下の3つのモードに焦点を当てます。基本に慣れたら Autopilot についてもご紹介します。

---

## 🧩 現実世界の例え：外食

GitHub Copilot CLI を使うのは、外食に行くようなものです。計画を立てるところから注文まで、状況に応じて異なるアプローチが必要です。

| モード | 外食に例えると | いつ使うか |
|------|----------------|-------------|
| **Plan** | レストランまでの GPS ルート | 複雑なタスク - ルートを確認し、立ち寄り場所に合意し、計画を固めてから出発する |
| **Interactive** | 店員さんとの会話 | 探索と試行錯誤 - 質問し、カスタマイズし、リアルタイムでフィードバックをもらう |
| **Programmatic** | ドライブスルーでの注文 | 素早く特定のタスクをこなす - 今の環境を離れず、すぐに結果を得る |

外食と同じように、どのアプローチが適切かは自然と身についていきます。

<img src="images/ordering-food-analogy.png" alt="GitHub Copilot CLI の3つの使い方 - Plan モード（GPSルート）、Interactive モード（店員との会話）、Programmatic モード（ドライブスルー）" width="800"/>

*タスクに合わせてモードを選びましょう：じっくり計画を立てるなら Plan、やり取りしながら協力するなら Interactive、一発で結果が欲しいなら Programmatic。*

### どのモードから始めればいいですか？

**Interactive モードから始めてください。** 
- 実験したり、追加の質問をしたりできます。
- 会話を通じて自然にコンテキスト（文脈）が積み重なります。
- 間違えても `/clear` で簡単にやり直せます。

慣れてきたら、以下を試してみてください：
- ぱっと答えが欲しいときは **Programmatic モード** (`copilot -p "<プロンプト>"`)
- コーディングの前に詳細な計画が必要なときは **Plan モード** (`/plan`)

---

## 3つのモード

### モード 1：Interactive（対話）モード (ここから開始)

<img src="images/interactive-mode.png" alt="Interactive モード - 質問に答えたり注文を調整したりしてくれる店員との会話のようなもの" width="250"/>

**最適**: 探索、試行錯誤、複数回のやり取り。質問に答え、フィードバックを受け取り、その場で注文を調整してくれる店員さんと話すようなものです。

対話型セッションを開始する：

```bash
copilot
```

これまで見てきたように、自然な言葉で入力できるプロンプトが表示されます。利用可能なコマンドのヘルプを見るには、次のように入力します：

```
> /help
```

**重要な洞察**: Interactive モードはコンテキストを維持します。実際の会話と同じように、各メッセージはそれまでの内容に基づいています。

#### Interactive モードの例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

各プロンプトが前の回答に基づいていることに注目してください。毎回最初から説明し直す必要はなく、会話を続けているのです。

---

### モード 2：Plan（計画）モード

<img src="images/plan-mode.png" alt="Plan モード - GPSを使って旅行前にルートを計画するようなもの" width="250"/>

**最適**: 実行前にアプローチを確認したい複雑なタスク。GPS を使って出発前にルートを計画するのに似ています。

Plan モードは、コードを書く前にステップバイステップの計画を作成するのに役立ちます。`/plan` コマンドを使うか、**Shift+Tab** を押して Plan モードに切り替えます：

> 💡 **ヒント**: **Shift+Tab** でモードを切り替えられます：Interactive → Plan → Autopilot。対話型セッション中ならいつでも、コマンドを打たずにモードを変更できます。

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

**Plan モードの出力例:** (出力は異なります)

```
📋 実装計画

ステップ 1: book_app.py のコマンドハンドラーを更新
  - "mark" コマンド用の新しい elif ブランチを追加
  - handle_mark_as_read() 関数を作成

ステップ 2: ハンドラー関数を実装
  - ユーザーに書籍タイトルの入力を促す
  - collection.mark_as_read(title) を呼び出す
  - 成功/失敗メッセージを表示

ステップ 3: ヘルプテキストを更新
  - 利用可能なコマンドリストに "mark" を追加
  - コマンドの使い方をドキュメント化

ステップ 4: フローをテスト
  - 本を追加する
  - それを既読にする
  - リスト出力でステータスが変わることを確認

実装を進めますか？ [Y/n]
```

**重要な洞察**: Plan モードでは、コードが書かれる前にアプローチをレビューし、修正することができます。計画が完了したら、Copilot CLI に指示してファイルに保存することも可能です。例えば「この計画を `mark_as_read_plan.md` に保存して」と言うと、詳細が記載された Markdown ファイルが作成されます。

> 💡 **もっと複雑なことを試したいですか？** 「/plan Add search and filter capabilities to the book app」と試してみてください。Plan モードは、シンプルな機能からアプリケーション全体まで対応できます。

> 📚 **Autopilot モード**: Shift+Tab で切り替わる3つ目のモード **Autopilot** に気づいたかもしれません。Autopilot モードでは、Copilot が各ステップであなたの入力を待たずに計画全体を進めます。同僚にタスクを任せて「終わったら教えて」と言うようなものです。一般的な流れは plan → 承認 → autopilot です。つまり、まず良い計画を書けるようになる必要があります。Interactive と Plan モードに慣れたら、[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)を見てみてください。

---

### モード 3：Programmatic（プログラム）モード

<img src="images/programmatic-mode.png" alt="Programmatic モード - 素早い注文のためにドライブスルーを使うようなもの" width="250"/>

**最適**: 自動化、スクリプト、CI/CD、一発のコマンド。店員と話す必要なく、ドライブスルーで素早く注文するようなものです。

やり取りが不要な一回限りのコマンドには `-p` フラグを使います：

```bash
# コードを生成
copilot -p "Write a function that checks if a number is even or odd"

# 素早くヘルプを得る
copilot -p "How do I read a JSON file in Python?"
```

**重要な洞察**: Programmatic モードは素早く回答を出して終了します。会話はなく、入力 → 出力のみです。

<details>
<summary>📚 <strong>さらに詳しく：スクリプトで Programmatic モードを使う</strong> (クリックして展開)</summary>

慣れてきたら、シェルスクリプト内で `-p` を活用できます：

```bash
#!/bin/bash

# コミットメッセージを自動生成
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# ファイルをレビュー
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **`--allow-all` について**: このフラグはすべての権限確認をスキップし、Copilot CLI が確認なしにファイルを読み、コマンドを実行し、URL にアクセスすることを許可します。Programmatic モード (`-p`) では対話的にアクションを承認できないため、これが必要になります。`--allow-all` は、自分で書いたプロンプトかつ信頼できるディレクトリでのみ使用してください。信頼できない入力や機密性の高いディレクトリでは決して使用しないでください。

</details>

---

## 必須のスラッシュコマンド

これらは Interactive モードで機能します。まずは**この6つだけ**覚えてください。日常的な使用の90%をカバーできます。

| コマンド | 何をするか | いつ使うか |
|---------|--------------|-------------|
| `/clear` | 会話をクリアして新しく始める | トピックを切り替えるとき |
| `/help` | 利用可能な全コマンドを表示 | コマンドを忘れたとき |
| `/model` | AI モデルを表示または切り替え | AI モデルを変更したいとき |
| `/plan` | コーディングの前に作業を計画 | より複雑な機能を作るとき |
| `/research` | GitHubやウェブから深く調査 | 実装前に詳しく調べる必要があるとき |
| `/exit` | セッションを終了 | 終わったとき |

まずはこれだけで十分です！慣れてきたら、他のコマンドも探検してみてください。

> 📚 **公式ドキュメント**: コマンドとフラグの完全なリストは [CLI command reference](https://docs.github.com/copilot/reference/cli-command-reference)（英語）を参照してください。

<details>
<summary>📚 <strong>その他のコマンド</strong> (クリックして展開)</summary>

> 💡 上記の必須コマンドで、日々の作業の多くをカバーできます。このリファレンスは、もっと詳しく知りたくなったときのために用意してあります。

### エージェント環境

| コマンド | 何をするか |
|---------|--------------|
| `/agent` | 利用可能なエージェントの一覧・選択 |
| `/env` | ロードされた環境の詳細（アクティブな指示、MCP サーバー、スキル、エージェント、プラグインなど）を表示 |
| `/init` | リポジトリ用の Copilot 指示ファイルを初期化 |
| `/mcp` | MCP サーバー設定の管理 |
| `/skills` | 拡張機能である「スキル」の管理 |

> 💡 エージェントは [第04章](../04-agents-custom-instructions/README.ja.md)、スキルは [第05章](../05-skills/README.ja.md)、MCP サーバーは [第06章](../06-mcp-servers/README.ja.md) で扱います。

### モデルとサブエージェント

| コマンド | 何をするか |
|---------|--------------|
| `/delegate` | タスクを GitHub Copilot クラウドエージェントに任せる |
| `/fleet` | 複雑なタスクを並列サブタスクに分割して高速化 |
| `/model` | AI モデルを表示または切り替え |
| `/tasks` | バックグラウンドのサブエージェントや切り離されたシェルセッションを表示 |

### コード

| コマンド | 何をするか |
|---------|--------------|
| `/diff` | 現在のディレクトリでの変更内容をレビュー |
| `/pr` | 現在のブランチのプルリクエストを操作 |
| `/research` | GitHub やウェブソースを使用して深く調査 |
| `/review` | コードレビューエージェントを実行して変更を分析 |
| `/terminal-setup` | 複数行入力のサポート（Shift+Enter, Ctrl+Enter）を有効化 |

### 権限

| コマンド | 何をするか |
|---------|--------------|
| `/add-dir <directory>` | 許可リストにディレクトリを追加 |
| `/allow-all [on\|off\|show]` | 全権限確認を自動承認。`on` で有効、`off` で無効、`show` で現在の状態を確認 |
| `/yolo` | `/allow-all on` のクイックエイリアス — 全権限確認を自動承認 |
| `/cwd`, `/cd [directory]` | 作業ディレクトリを表示または変更 |
| `/list-dirs` | 許可されている全ディレクトリを表示 |

> ⚠️ **注意**: `/allow-all` および `/yolo` は確認プロンプトをスキップします。信頼できるプロジェクトには便利ですが、信頼できないコードを扱う際は注意してください。

### セッション

| コマンド | 何をするか |
|---------|--------------|
| `/clear` | 現在のセッションを破棄（履歴は保存されない）し、新しく開始 |
| `/compact` | 会話を要約してコンテキスト使用量を削減 |
| `/context` | コンテキストウィンドウのトークン使用量と可視化を表示 |
| `/keep-alive` | Copilot CLI の有効時間中にシステムがスリープするのを防止 — ノート PC などで長時間かかるタスクを実行する際に便利 |
| `/new` | 現在のセッションを終了（履歴に保存される）し、新しく開始 |
| `/resume` | 別のセッションに切り替え（セッション ID または名前を指定可能） |
| `/rename` | 現在のセッションの名前を変更（名前を省略すると自動生成） |
| `/rewind` | タイムラインピッカーを開き、以前の時点にロールバック |
| `/usage` | セッションの使用状況メトリクスと統計を表示 |
| `/session` | セッション情報とワークスペースの概要を表示。`/session delete`、`/session delete <id>`、または `/session delete-all` を使用してセッションを削除可能 |
| `/share` | セッションを Markdown、GitHub Gist、または HTML ファイルとしてエクスポート |

### 表示

| コマンド | 何をするか |
|---------|--------------|
| `/statusline`（または `/footer`） | セッション下部のステータスバーに表示する項目をカスタマイズ（ディレクトリ、ブランチ、エフォート、コンテキストウィンドウ、クォータ） |
| `/theme` | ターミナルのテーマを表示または設定 |

### ヘルプとフィードバック

| コマンド | 何をするか |
|---------|--------------|
| `/changelog` | CLI バージョンの変更履歴を表示 |
| `/feedback` | GitHub にフィードバックを送信 |
| `/help` | 利用可能な全コマンドを表示 |

### クイックシェルコマンド

`!` を頭に付けることで、AI を介さずにシェルコマンドを直接実行できます：

```bash
copilot

> !git status
# AI をバイパスして git status を直接実行

> !python -m pytest tests/
# pytest を直接実行
```

### モデルの切り替え

Copilot CLI は、OpenAI、Anthropic、Google などの複数の AI モデルをサポートしています。利用可能なモデルは、サブスクリプションレベルや地域によって異なります。`/model` を使ってオプションを確認し、切り替えることができます：

```bash
copilot
> /model

# 利用可能なモデルが表示されます。Claude Sonnet 4.5 などを選択できます。
```

> 💡 **ヒント**: モデルによって「プレミアムリクエスト」の消費量が異なります。**1x** と表示されているモデル（Claude Sonnet 4.5 など）をデフォルトにするのがおすすめです。非常に有能で効率的です。より高い倍率のモデルはクォータを早く消費するため、本当に必要なときのために取っておきましょう。

> 💡 **どのモデルを選べばよいか迷ったら？** モデル選択画面で **`Auto`** を選択すると、セッションごとに最適な利用可能モデルが自動的に選択されます。どのモデルを使うべきか深く考えずにすぐに始めたい場合に最適なデフォルト設定です。

</details>

---

# 練習

<img src="../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが置かれた、実践練習の準備が整ったデスク" width="800"/>

学んだことを実際に応用してみましょう。

---

## ▶️ 自分で試してみる

### 対話型での探索

Copilot を起動し、追加のプロンプトを使って書籍アプリを段階的に改善してみましょう：

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 機能を計画する

コードを書く前に、`/plan` を使って実装方法を Copilot CLI にマッピングさせます：

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author
（書籍アプリに、タイトルや著者で本を検索できる機能を追加して）

# 計画をレビューする
# 承認または修正する
# ステップバイステップで実装されるのを見る
```

### Programmatic モードで自動化する

`-p` フラグを使うと、対話モードに入らずにターミナルから直接 Copilot CLI を実行できます。以下のスクリプトをリポジトリのルートでターミナルに貼り付けて（Copilot の中ではありません）、書籍アプリのすべての Python ファイルをレビューしてみましょう。

```bash
# 書籍アプリのすべての Python ファイルをレビュー
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# 書籍アプリのすべての Python ファイルをレビュー
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

デモが終わったら、次のようなバリエーションも試してみてください：

1. **Interactive チャレンジ**: `copilot` を起動して書籍アプリを探索します。`@samples/book-app-project/books.py` について質問し、3回連続で改善を求めてみてください。

2. **Plan モード チャレンジ**: `/plan Add rating and review features to the book app` を実行します。計画を注意深く読んでください。理にかなっていますか？

3. **Programmatic チャレンジ**: `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"` を実行します。一発でうまくいきましたか？

---

## 💡 ヒント：Web またはモバイルから CLI セッションをコントロールする

GitHub Copilot CLI は**リモートセッション**をサポートしており、ターミナルの前にいなくても、Web ブラウザ（PC またはモバイル）や GitHub Mobile アプリから実行中の CLI セッションを監視し、対話することができます。

`--remote` フラグを使用してリモートセッションを開始します：

```bash
copilot --remote
```

Copilot CLI にリンクが表示され、QR コードへのアクセスが提供されます。スマートフォンのカメラで読み取るか、PC のブラウザでそのリンクを開くと、セッションをリアルタイムで監視し、フォローアッププロンプトを送信し、計画を確認し、エージェントをリモートで操作できます。セッションはユーザー固有であるため、自身の Copilot CLI セッションにのみアクセスできます。

アクティブなセッションの内部から、いつでもリモートアクセスを有効にすることもできます：

```
> /remote
```

リモートセッションの詳細については、[Copilot CLI ドキュメント](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely)（英語）を参照してください。

---

## 📝 課題

### メインチャレンジ：書籍アプリのユーティリティを改善する

ハンズオンでは `book_app.py` のレビューとリファクタリングを行いました。今度は別のファイル `utils.py` で同じスキルを練習しましょう：

1. 対話型セッションを開始する：`copilot`
2. Copilot CLI にファイルの要約を求める：`"Summarize @samples/book-app-project/utils.py and explain what each function in this file does"`
3. 入力バリデーションを追加させる：「空の入力や数値以外の入力も処理できるように `get_user_choice()` にバリデーションを追加して」
4. エラーハンドリングを改善させる：「タイトルに空文字列が渡されたらどうなる？ガードを追加して」
5. ドキュメント（docstring）を追加させる：「パラメータの説明と戻り値を含めた包括的な docstring を `get_book_details()` に追加して」
6. プロンプト間でコンテキストがどのように引き継がれるか観察してください。各改善は前の状態に基づいています。
7. `/exit` で終了します。

**成功基準**: 入力バリデーション、エラーハンドリング、docstring が備わった、改善された `utils.py` が完成していること。これらはすべて複数回の会話を通じて構築してください。

<details>
<summary>💡 ヒント (クリックして展開)</summary>

**試してみるプロンプトの例:**
```bash
> Summarize @samples/book-app-project/utils.py and explain what each function in this file does
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**よくある問題:**
- Copilot CLI が確認の質問をしてきたら、自然に答えてください。
- コンテキストは引き継がれるため、各プロンプトは前の回答を前提としています。
- 最初からやり直したいときは `/clear` を使ってください。

</details>

### ボーナスチャレンジ：モードを比較する

これまでは、検索機能には `/plan`、バッチレビューには `-p` を使いました。今度は一つの新しいタスク（`BookCollection` クラスに `list_by_year()` メソッドを追加する）に対して、3つのモードすべてを試してみてください：

1. **Interactive**: `copilot` → ステップバイステップでメソッドを設計・構築させる
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**振り返り**: どのモードが一番自然に感じられましたか？それぞれどのような時に使いたいと思いますか？

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong> (クリックして展開)</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| `/exit` ではなく `exit` と打つ | Copilot CLI は "exit" をコマンドではなくプロンプト（AIへの質問）として扱います | スラッシュコマンドは必ず `/` で始めます |
| 複数回の会話に `-p` を使う | 各 `-p` の呼び出しは独立しており、前のやり取りの記憶はありません | コンテキストを積み重ねる会話には Interactive モード (`copilot`) を使います |
| `$` や `!` を含むプロンプトを引用符で囲むのを忘れる | Copilot CLI が受け取る前にシェルが特殊文字を解釈してしまいます | プロンプトを引用符で囲んでください：`copilot -p "What does $HOME mean?"` |
| 実行中のタスクをキャンセルするために Esc キーを 1 回だけ押す | 誤操作を防ぐため、Esc キーの 1 回押しでは処理中のタスクをキャンセルできなくなりました | Copilot CLI が処理中の場合は、**Esc キーを 2 回**押すことでキャンセルできます |

### トラブルシューティング

**「Model not available」** - あなたのサブスクリプションでは利用できないモデルかもしれません。`/model` で利用可能なものを確認してください。

**「Context too long」** - 会話がコンテキストウィンドウの制限に達しました。`/clear` でリセットするか、新しいセッションを開始してください。

**「Rate limit exceeded」** - 数分待ってから再度試してください。大量の操作を行う場合は、遅延を挟んだ Programmatic モードの検討も有効です。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **Interactive モード** は探索と試行錯誤のためのものです。コンテキストが引き継がれるため、これまでの話を覚えている相手と会話しているような感覚になります。
2. **Plan モード** は、通常より複雑なタスクに使います。実装前に計画をレビューします。
3. **Programmatic モード** は自動化のためのものです。やり取りは不要です。
4. **必須コマンド** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`) で日常的な使用のほとんどをカバーできます。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストについては、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)（英語）を参照してください。

---

## ➡️ 次は？

3つのモードを理解したところで、次は Copilot CLI にあなたのコードに関する「コンテキスト（背景情報）」を伝える方法を学びましょう。

**[第02章：コンテキストと対話](../02-context-conversations/README.ja.md)** では以下を学びます：

- ファイルやディレクトリを参照するための `@` 構文
- `--resume` や `--continue` を使ったセッション管理
- コンテキスト管理が Copilot CLI を真に強力にする理由

---

**[← コースのホームに戻る](../README.ja.md)** | **[第02章へ進む →](../02-context-conversations/README.ja.md)**
