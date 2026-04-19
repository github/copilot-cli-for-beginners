![第01章: First Steps](images/chapter-header.png)

> **AI がバグをすばやく見つけ、わかりにくいコードを説明し、動く script を生成する様子を体験しましょう。その後、GitHub Copilot CLI の 3 つの使い方を学びます。**

この章から、いよいよ GitHub Copilot CLI の「すごさ」を実感できます。開発者が「熟練エンジニアにいつでも相談できるようだ」と表現する理由を、実際のデモで体験していきます。AI が数秒で security bug を見つけたり、複雑なコードをやさしい言葉で説明したり、その場で動く script を生成したりします。さらに、3 つの interaction mode（Interactive、Plan、Programmatic）を学び、どの場面で何を使うべきかが分かるようになります。

> ⚠️ **前提条件**: 先に **[Chapter 00: Quick Start](../00-quick-start/README.md)** を終えておいてください。以下のデモを試すには、GitHub Copilot CLI のインストールと認証が必要です。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- ハンズオンデモを通じて GitHub Copilot CLI の生産性向上を体感できる
- 目的に応じて適切な mode（Interactive、Plan、Programmatic）を選べる
- slash command を使ってセッションをコントロールできる

> ⏱️ **想定時間**: 約45分（読む時間 15分 + ハンズオン 30分）

---

# はじめての Copilot CLI 体験

<img src="images/first-copilot-experience.png" alt="Developer sitting at a desk with code on the monitor and glowing particles representing AI assistance" width="800"/>

まずは GitHub Copilot CLI が何をしてくれるのかを、気軽に試してみましょう。

---

## まず慣れてみる: 最初の prompts

印象的なデモに入る前に、今すぐ試せるシンプルな prompt から始めましょう。**コード repository は不要です**。terminal を開いて Copilot CLI を起動してください。

```bash
copilot
```

次のような beginner-friendly な prompt を試してみてください。

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Python を使っていなくても大丈夫です。自分の使っている言語について自然に質問してみてください。

大事なのは、このやり取りがとても自然だということです。同僚に話しかけるように質問できます。探索が終わったら、`/exit` でセッションを終了します。

**ここでのポイント**: GitHub Copilot CLI は conversational です。特別な記法を覚えなくても、まずは plain English で質問するだけで始められます。

## 実際の動きを見てみる

ここからは、開発者が「いつでも相談できる senior engineer みたいだ」と感じる理由を見ていきます。

> 📖 **例の読み方**: `>` で始まる行は、interactive な Copilot CLI セッション内で入力する prompt です。`>` が付いていない行は、terminal で実行する shell command です。

> 💡 **サンプル出力について**: このコースに載っている出力例はイメージです。Copilot CLI の返答は毎回変わるため、実際の表現やフォーマット、詳細さは異なります。まったく同じ文面になるかではなく、*どんな情報が返るか* に注目してください。

### Demo 1: 数秒で code review

このコースには、意図的に code quality の問題を含めた sample file が入っています。ローカル環境で作業していて、まだ repo を clone していない場合は、次の `git clone` を実行し、`copilot-cli-for-beginners` フォルダーに移動してから `copilot` を起動してください。

```bash
# Clone the course repository if you're working locally and haven't already
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Start Copilot
copilot
```

interactive な Copilot CLI セッションに入ったら、次を実行します。

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 記号は何に使うの？** `@` は Copilot CLI に「この file を読んで」と伝える記法です。詳しくは第02章で扱います。ここではまず、表示どおりにそのまま実行してみてください。

---

<details>
<summary>🎬 動作例を見る</summary>

![Code Review Demo](images/code-review-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

**ここでの学び**: 数秒で professional な code review が得られます。手作業の review と比べると、かなりの時間短縮になります。

---

### Demo 2: わかりにくいコードを説明してもらう

「このコード、結局何をしているんだろう？」と止まってしまうことはありませんか。Copilot CLI セッションで次を試してください。

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 動作例を見る</summary>

![Explain Code Demo](images/explain-code-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

**何が起きるか**: （実際の出力は異なりますが）Copilot CLI が file を読み取り、コードを理解し、plain English で説明してくれます。

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

**ここでの学び**: 複雑なコードでも、丁寧な mentor が隣で説明してくれるような感覚で理解できます。

---

### Demo 3: 動くコードを生成する

本来なら検索や試行錯誤に 15 分くらいかかりそうな関数も、セッションを続けたまま頼めます。

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 動作例を見る</summary>

![Generate Code Demo](images/generate-code-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

**何が起きるか**: そのまま copy-paste して試せる、完成度の高い関数が数秒で返ってきます。

試し終わったら、次でセッションを終了します。

```
> /exit
```

**ここでの学び**: すぐ結果が返ってきて、しかも 1 つの連続したセッションのまま進められます。

---

# Modes and Commands

<img src="images/modes-and-commands.png" alt="Futuristic control panel with glowing screens, dials, and equalizers representing Copilot CLI modes and commands" width="800"/>

Copilot CLI が何をできるかを見たので、次は *どう使い分けるか* を理解しましょう。大切なのは、状況に応じて 3 つの interaction mode を選べるようになることです。

> 💡 **Note**: Copilot CLI には **Autopilot** mode もあり、ユーザー入力を毎回待たずにタスクを進められます。強力ですが、広い権限付与と premium requests の自動利用が必要です。このコースでは、まず下記の 3 つに集中します。Autopilot は basics に慣れてから使うのがおすすめです。

---

## 🧩 現実世界のたとえ: 外食するときの選び方

GitHub Copilot CLI の使い分けは、外食の進め方に少し似ています。どこに行くか考える段階から注文する段階まで、場面ごとに向いた方法があります。

| Mode | たとえ | 使う場面 |
|------|----------------|-------------|
| **Plan** | お店までの GPS ルート | 複雑なタスク - 道順を整理して確認し、合意してから進む |
| **Interactive** | 店員さんと会話する | 探索や反復 - 質問したり調整したり、その場でフィードバックを得る |
| **Programmatic** | ドライブスルー注文 | すばやく具体的に済ませたいとき - 今の環境のまま結果を得る |

外食のときに自然と使い分けるように、Copilot CLI も目的に応じて mode を選べるようになります。

<img src="images/ordering-food-analogy.png" alt="Three Ways to Use GitHub Copilot CLI - Plan Mode (GPS route to restaurant), Interactive Mode (talking to waiter), Programmatic Mode (drive-through)" width="800"/>

*タスクに合わせて mode を選びましょう。まず道筋を整理するなら Plan、対話的に進めるなら Interactive、1 回で答えが欲しいなら Programmatic です。*

### 最初はどの Mode から始めるべき？

**まずは Interactive mode から始めるのがおすすめです。**
- 気軽に試して follow-up question を重ねられる
- 会話の流れの中で context が自然に積み上がる
- もし迷っても `/clear` でやり直しやすい

慣れてきたら、次も試してみてください。
- **Programmatic mode** (`copilot -p "<your prompt>"`) - 単発の素早い質問向け
- **Plan mode** (`/plan`) - コーディング前に流れを整理したいとき向け

---

## 3 つの Modes

### Mode 1: Interactive Mode（まずはここから）

<img src="images/interactive-mode.png" alt="Interactive Mode - Like talking to a waiter who can answer questions and adjust the order" width="250"/>

**向いている用途**: 探索、反復、multi-turn conversation。質問に答えたり、フィードバックを受けて調整したりできる店員さんとの会話のような感覚です。

interactive session の始め方:

```bash
copilot
```

ここまでの例のように、自然な言葉で入力できる prompt が表示されます。使える command を確認したいときは次を入力します。

```
> /help
```

**重要ポイント**: Interactive mode では context が保持されます。前のメッセージを踏まえて会話が続くので、本当に対話している感覚で進められます。

#### Interactive Mode の例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

各 prompt が前の返答を踏まえてつながっていることに注目してください。毎回やり直すのではなく、会話を積み上げています。

---

### Mode 2: Plan Mode

<img src="images/plan-mode.png" alt="Plan Mode - Like planning a route before a trip using GPS" width="250"/>

**向いている用途**: 実行前に進め方を確認したい、少し複雑な task。旅行前に GPS でルートを決めるのと似ています。

Plan mode は、コードを書く前に step-by-step の plan を作るのに役立ちます。`/plan` command を使うか、**Shift+Tab** で Plan Mode に切り替えます。

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Tip**: **Shift+Tab** で mode を切り替えられます: Interactive → Plan → Autopilot。interactive session の途中でも、command を打たずに切り替え可能です。

`--plan` flag を付けて、最初から plan mode で起動することもできます。

```bash
copilot --plan
```

**Plan mode の出力例:** （実際の出力は異なります）

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

**重要ポイント**: Plan mode では、コードが書かれる前に方針を review・修正できます。plan が完成したら、あとで参照できるように file に保存してもらうこともできます。たとえば「Save this plan to `mark_as_read_plan.md`」と伝えれば、plan の詳細を markdown file にしてくれます。

> 💡 **もう少し複雑な例を試すなら**: `/plan Add search and filter capabilities to the book app`。Plan mode は、小さな機能追加から app 全体の設計まで対応できます。

> 📚 **Autopilot mode**: Shift+Tab で 3 つ目の mode として **Autopilot** が出てくることに気づいたかもしれません。autopilot mode では、各 step ごとに止まらず、plan 全体をまとめて進めます。イメージとしては「終わったら教えて」と同僚に任せる感じです。基本の流れは plan → accept → autopilot なので、まずは plan を上手に書けることが大切です。`copilot --autopilot` で直接起動することもできます。まずは Interactive と Plan に慣れてから、必要になったら [official docs](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) を見てください。

---

### Mode 3: Programmatic Mode

<img src="images/programmatic-mode.png" alt="Programmatic Mode - Like using a drive-through for a quick order" width="250"/>

**向いている用途**: automation、scripts、CI/CD、単発 command。店員さんとやり取りせずに素早く注文するドライブスルーのイメージです。

対話が不要な 1 回限りの command には `-p` flag を使います。

```bash
# Generate code
copilot -p "Write a function that checks if a number is even or odd"

# Get quick help
copilot -p "How do I read a JSON file in Python?"
```

**重要ポイント**: Programmatic mode は、すぐ答えを返して終了します。会話を続けるのではなく、input → output を素早く処理したいときに便利です。

<details>
<summary>📚 <strong>さらに活用する: Scripts で Programmatic Mode を使う</strong>（クリックして展開）</summary>

慣れてきたら、shell script の中でも `-p` を使えます。

```bash
#!/bin/bash

# Generate commit messages automatically
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Review a file
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **`--allow-all` について**: この flag は permission prompt をすべてスキップし、Copilot CLI が file の読み取り、command の実行、URL へのアクセスを確認なしで行えるようにします。programmatic mode (`-p`) では interactive に承認できないため必要になります。自分で書いた prompt と、信頼できる directory でのみ使ってください。信頼していない input や敏感な directory では使わないでください。

</details>

---

## まず覚えたい Essential Slash Commands

Copilot CLI を使い始めたばかりの段階では、まず次の command を覚えると十分です。

| Command | できること | 使う場面 |
|---------|--------------|-------------|
| `/ask` | 会話履歴に影響させずに短い質問をする | 今の task を崩さずに quick answer が欲しいとき |
| `/clear` | 会話を消して fresh に始める | 話題を切り替えるとき |
| `/help` | 利用可能な command を表示する | command を忘れたとき |
| `/model` | AI model を表示・切り替えする | model を変えたいとき |
| `/plan` | coding 前に作業 plan を立てる | やや複雑な feature のとき |
| `/research` | GitHub と web sources を使って deep research する | 実装前に調査したいとき |
| `/exit` | セッションを終了する | 作業を終えるとき |

> 💡 **`/ask` と通常の chat の違い**: 普通は送ったメッセージが会話の一部として残り、後続の返答にも影響します。`/ask` は「記録に残さず聞く」ための shortcut です。たとえば `/ask What does YAML mean?` のように、セッションの context を汚さずに軽く確認できます。

ここまでで、使い始めに必要な基本は十分です。慣れてきたら、追加 command も見ていきましょう。

> 📚 **Official Documentation**: command や flag の一覧は [CLI command reference](https://docs.github.com/copilot/reference/cli-command-reference) を参照してください。

<details>
<summary>📚 <strong>Additional Commands</strong>（クリックして展開）</summary>

> 💡 上で紹介した基本 command だけでも、日常的な作業のかなりの部分をカバーできます。ここから先は、もっと広く使いたくなったときの参考用です。

### Agent Environment

| Command | できること |
|---------|--------------|
| `/agent` | 利用可能な agent を一覧表示して選ぶ |
| `/env` | 読み込まれている instructions、MCP servers、skills、agents、plugins などの環境情報を表示する |
| `/init` | repository 用の Copilot instructions を初期化する |
| `/mcp` | MCP server の設定を管理する |
| `/skills` | skills を管理して機能を拡張する |

> 💡 agents は [Chapter 04](../04-agents-custom-instructions/README.md)、skills は [Chapter 05](../05-skills/README.md)、MCP servers は [Chapter 06](../06-mcp-servers/README.md) で扱います。

### Models and Subagents

| Command | できること |
|---------|--------------|
| `/delegate` | task を GitHub Copilot cloud agent に引き渡す |
| `/fleet` | 複雑な task を並列の subtasks に分割して高速化する |
| `/model` | AI model を表示または切り替える |
| `/tasks` | background subagents や detached shell sessions を確認する |

### Code

| Command | できること |
|---------|--------------|
| `/diff` | 現在の directory での変更を review する |
| `/pr` | 現在の branch に対する pull request を操作する |
| `/research` | GitHub や web sources を使って deep research を行う |
| `/review` | code-review agent を実行して変更を分析する |
| `/terminal-setup` | multiline input support（shift+enter や ctrl+enter）を有効にする |

### Permissions

| Command | できること |
|---------|--------------|
| `/add-dir <directory>` | 許可済み list に directory を追加する |
| `/allow-all [on|off|show]` | すべての permission prompt を自動承認する。`on` で有効、`off` で無効、`show` で状態確認 |
| `/yolo` | `/allow-all on` のクイック alias |
| `/cwd`, `/cd [directory]` | working directory を表示または変更する |
| `/list-dirs` | 許可されている directory 一覧を表示する |

> ⚠️ **注意して使いましょう**: `/allow-all` と `/yolo` は確認を省略します。信頼できる project では便利ですが、信頼していない code に対しては慎重に使ってください。

### Session

| Command | できること |
|---------|--------------|
| `/clear` | 現在の session を破棄（履歴保存なし）して fresh な会話を始める |
| `/compact` | 会話を要約して context 使用量を減らす |
| `/context` | context window の token 使用量と可視化を表示する |
| `/new` | 現在の session を履歴保存して終了し、新しい会話を始める |
| `/resume` | 別の session に切り替える（必要なら session ID 指定も可能） |
| `/rename` | 現在の session 名を変更する（名前省略で自動生成も可） |
| `/rewind` | conversation の以前の時点に戻るための timeline picker を開く |
| `/usage` | session の usage metrics や統計を表示する |
| `/session` | session 情報と workspace summary を表示する |
| `/share` | session を markdown file、GitHub gist、または self-contained HTML として出力する |

### Display

| Command | できること |
|---------|--------------|
| `/statusline` (or `/footer`) | session 下部の status bar に表示する項目を調整する |
| `/theme` | terminal theme を表示または設定する |

### Help and Feedback

| Command | できること |
|---------|--------------|
| `/changelog` | CLI version の changelog を表示する |
| `/feedback` | GitHub に feedback を送る |
| `/help` | 利用可能な command を表示する |

### Quick Shell Commands

AI を介さずに shell command をそのまま実行したい場合は、先頭に `!` を付けます。

```bash
copilot

> !git status
# Runs git status directly, bypassing the AI

> !python -m pytest tests/
# Runs pytest directly
```

### モデルの切り替え

Copilot CLI は OpenAI、Anthropic、Google など複数の AI model をサポートしています。利用できる model はサブスクリプションや地域によって変わります。`/model` を使って選択肢を確認し、切り替えてみましょう。

```bash
copilot
> /model

# Shows available models and lets you pick one. Select Sonnet 4.5.
```

> 💡 **Tip**: model によって消費する "premium requests" の量が異なります。**1x** と表示される model（例: Claude Sonnet 4.5）は、能力と効率のバランスが良いので、最初の default としておすすめです。倍率の高い model は premium quota を早く消費するため、本当に必要な場面で使うのが実用的です。

</details>

---

# Practice

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

ここからは、自分で手を動かして試してみましょう。

---

## ▶️ Try It Yourself

### Interactive Exploration

Copilot を起動し、follow-up prompt を重ねながら book app を少しずつ改善してみてください。

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### Plan a Feature

`/plan` を使うと、コードを書く前に実装の流れを整理できます。

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Review the plan
# Approve or modify
# Watch it implement step by step
```

### Programmatic Mode で自動化する

`-p` flag を使うと、interactive mode に入らず terminal から直接 Copilot CLI を実行できます。repository のルートで、次の script を Copilot の中ではなく terminal にそのまま貼り付けて、book app の全 Python file を review してみてください。

```bash
# Review all Python files in the book app
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# Review all Python files in the book app
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

デモを終えたら、次の variation も試してみてください。

1. **Interactive Challenge**: `copilot` を起動し、book app を探索します。`@samples/book-app-project/books.py` について質問し、3 回連続で改善案を求めてみてください。

2. **Plan Mode Challenge**: `/plan Add rating and review features to the book app` を実行します。plan をよく読んで、筋が通っているか確かめてください。

3. **Programmatic Challenge**: `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"` を実行します。1 回でうまくいきましたか？

---

## 💡 Tip: Web や Mobile から CLI Session を操作する

GitHub Copilot CLI は **remote sessions** をサポートしており、実行中の CLI session を web browser（desktop / mobile）や GitHub Mobile app から確認・操作できます。terminal の前にいなくても、状況確認や follow-up prompt の送信ができます。

`--remote` flag を付けて remote session を始めます。

```bash
copilot --remote
```

Copilot CLI が link と QR code を表示します。スマートフォンや desktop browser でその link を開くと、session をリアルタイムで見たり、follow-up prompt を送ったり、plan を review したり、遠隔で agent の進行を調整したりできます。session はユーザー単位なので、自分の Copilot CLI session のみアクセス可能です。

すでに session を開いている場合でも、途中から remote access を有効にできます。

```
> /remote
```

remote session の詳しい説明は [Copilot CLI docs](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely) を参照してください。

---

## 📝 Assignment

### Main Challenge: Book App Utilities を改善する

ハンズオン例では `book_app.py` の review と refactor を扱いました。今度は別の file、`utils.py` で同じ流れを練習してみましょう。

1. interactive session を開始します: `copilot`
2. Copilot CLI に file の要約を頼みます: `@samples/book-app-project/utils.py What does each function in this file do?`
3. input validation を追加してもらいます: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. error handling を改善してもらいます: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. docstring を追加してもらいます: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. prompt を重ねるほど context が引き継がれることを確認します
7. `/exit` で終了します

**成功条件**: input validation、error handling、docstring が追加された、より良い `utils.py` を multi-turn conversation で作れれば成功です。

<details>
<summary>💡 Hints（クリックして展開）</summary>

**試せる sample prompt:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**よくあるポイント:**
- Copilot CLI が確認質問をしてきたら、自然に答えれば大丈夫です
- context は引き継がれるので、各 prompt が前の内容を土台に進みます
- 最初からやり直したい場合は `/clear` を使います

</details>

### Bonus Challenge: 3 つの Modes を比べる

例では search feature に `/plan` を使い、batch review に `-p` を使いました。次は 1 つの新しい task について、3 つの mode をすべて試してみてください。`BookCollection` class に `list_by_year()` method を追加する、という task です。

1. **Interactive**: `copilot` を起動し、step by step で method の設計と実装を相談する
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**ふりかえり**: どの mode がいちばん自然に感じましたか？ それぞれをどんな場面で使いたいですか？

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong>（クリックして展開）</summary>

### Common Mistakes

| Mistake | 起きること | 対処 |
|---------|--------------|-----|
| `exit` と入力してしまい `/exit` を忘れる | Copilot CLI は "exit" を command ではなく prompt として扱う | slash command は常に `/` で始まります |
| multi-turn conversation に `-p` を使う | 各 `-p` 呼び出しが独立し、前回の記憶を持たない | context を積み上げたいなら interactive mode (`copilot`) を使う |
| `$` や `!` を含む prompt を quote しない | Copilot CLI に渡る前に shell が特殊文字を解釈してしまう | `copilot -p "What does $HOME mean?"` のように quote で囲む |

### Troubleshooting

**"Model not available"** - 利用中のサブスクリプションでは一部 model が使えない場合があります。`/model` で確認してください。

**"Context too long"** - 会話が context window の上限に達しています。`/clear` でリセットするか、新しい session を始めてください。

**"Rate limit exceeded"** - 数分待ってから再試行してください。batch operation では、間隔をあけた programmatic mode が役立つことがあります。

</details>

---

# Summary

## 🔑 Key Takeaways

1. **Interactive mode** は探索と反復向け - context が会話の中で引き継がれます
2. **Plan mode** は少し複雑な task 向け - 実装前に review できます
3. **Programmatic mode** は automation 向け - 対話なしで結果を返します
4. **基本 command**（`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`）だけでも日常利用の大半をカバーできます

> 📋 **Quick Reference**: コマンドやショートカットの一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次は？

3 つの mode を理解したので、次は Copilot CLI にコードの context を渡す方法を学びましょう。

**[Chapter 02: Context and Conversations](../02-context-conversations/README.md)** では、次のことを学びます。

- file や directory を参照するための `@` syntax
- `--resume` と `--continue` を使った session management
- context management によって Copilot CLI が本当に強力になる理由

---

**[← コース Home に戻る](../README.md)** | **[Chapter 02 へ進む →](../02-context-conversations/README.md)**
