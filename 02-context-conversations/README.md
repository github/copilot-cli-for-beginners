![第02章: Context and Conversations](images/chapter-header.png)

> **AI が 1 つの file だけでなく、コードベース全体を見られるとしたらどうでしょうか？**

この章では、GitHub Copilot CLI の本当の強みである context を使いこなします。`@` syntax を使って files や directories を参照し、Copilot CLI にコードベースの深い理解を与える方法を学びます。さらに、session をまたいで会話を続けたり、数日後に前回の続きから再開したり、single-file review では見つからない cross-file analysis の強さを体験します。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- `@` syntax を使って files、directories、images を参照できる
- `--resume` と `--continue` で前回の session を再開できる
- [context windows](../GLOSSARY.md#context-window) の考え方を理解できる
- 効果的な multi-turn conversation を書ける
- 複数 project をまたぐときの directory permissions を管理できる

> ⏱️ **想定時間**: 約50分（読む時間 20分 + ハンズオン 30分）

---

## 🧩 現実世界のたとえ: 同僚に相談する場面

<img src="images/colleague-context-analogy.png" alt="Context Makes the Difference - Without vs With Context" width="800"/>

*Copilot CLI も同僚と同じで、何も見えないままでは的確な助けができません。必要な情報を渡すほど、より具体的な支援が返ってきます。*

たとえば、同僚に bug を説明するときも次のような違いがあります。

> **Without context**: "The book app doesn't work."

> **With context**: "Look at `books.py`, especially the `find_book_by_title` function. It's not doing case-insensitive matching."

Copilot CLI に context を渡すには、*`@` syntax* を使って対象の file や directory を示します。

---

# 必須: 基本の Context

<img src="images/essential-basic-context.png" alt="Glowing code blocks connected by light trails representing how context flows through Copilot CLI conversations" width="800"/>

この section では、context を使って実用的に作業するための基本を学びます。まずはここをしっかり押さえましょう。

---

## The @ Syntax

`@` symbol は、prompt の中で files や directories を参照するための記法です。つまり Copilot CLI に「この file を見て」と伝える方法です。

> 💡 **Note**: このコースの例はすべて、この repository に含まれている `samples/` folder を使っています。そのままコピーして試せます。

### 今すぐ試す（特別な準備は不要）

手元にある任意の file で試せます。

```bash
copilot

# Point at any file you have
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **すぐ試せる file がない場合** は、簡単な test file を作ってみましょう。
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本的な @ パターン

| Pattern | できること | 使い方の例 |
|---------|--------------|-------------|
| `@file.py` | 1 つの file を参照する | `Review @samples/book-app-project/books.py` |
| `@folder/` | directory 内の files 全体を参照する | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 複数 file を同時に参照する | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 1 つの File を参照する

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 動作例を見る</summary>

![File Context Demo](images/file-context-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

### 複数 File を参照する

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### Directory 全体を参照する

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## Cross-File Intelligence

ここから context が本当に強力になります。single-file analysis も便利ですが、cross-file analysis はそれ以上に大きな価値があります。

<img src="images/cross-file-intelligence.png" alt="Cross-File Intelligence - comparing single-file vs cross-file analysis showing how analyzing files together reveals bugs, data flow, and patterns invisible in isolation" width="800"/>

### Demo: 複数 File にまたがる Bug を見つける

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **Advanced Option**: security に注目した cross-file analysis を試したい場合は、Python の security sample でも試せます。
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 動作例を見る</summary>

![Multi-File Demo](images/multi-file-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

**Copilot CLI が見つけられること:**

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

**なぜ重要なのか**: 1 file だけの review では全体像を見落としがちです。cross-file analysis だからこそ、次のような点が見えてきます。
- **重複コード** - まとめるべき部分が分かる
- **data flow の流れ** - component 同士がどう連携しているか見える
- **設計上の課題** - 保守性に影響する問題を把握できる

---

### Demo: 60 秒でコードベースを理解する

<img src="images/codebase-understanding.png" alt="Split-screen comparison showing manual code review taking 1 hour versus AI-assisted analysis taking 10 seconds" width="800" />

新しい project に入ったときでも、Copilot CLI なら短時間で全体像をつかめます。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**得られるもの:**
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**結果**: 1 時間かけて読み込むような作業を、10 秒ほどで方向づけできます。どこから手を付けるべきかがすぐ分かります。

---

## Practical Examples

### Example 1: Context 付き Code Review

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI now has the full file content and can give specific feedback:
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# Now reviewing book_app.py, but still aware of books.py context
```

### Example 2: コードベースを理解する

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI reads books.py and understands the BookCollection class

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI scans the directory and summarizes

> How does the app save and load books?

# Copilot CLI can trace through the code it's already seen
```

<details>
<summary>🎬 multi-turn conversation の例を見る</summary>

![Multi-Turn Demo](images/multi-turn-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

### Example 3: 複数 File の Refactoring

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI sees both files and can suggest how to merge the duplicate code
```

---

## Session Management

作業中の session は自動保存されます。前回の続きを開いて、同じ context のまま作業を再開できます。

### Session は自動保存される

通常どおり終了するだけで大丈夫です。

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... do some work ...]

> /exit
```

### 直近の Session を再開する

```bash
# Continue where you left off
copilot --continue
```

### 特定の Session を再開する

```bash
# Pick from a list of sessions interactively
copilot --resume

# Or resume a specific session by ID
copilot --resume abc123
```

> 💡 **session ID はどう探すの？** 覚えておく必要はありません。`copilot --resume` を ID なしで実行すると、過去の session 名、ID、最終更新時刻の一覧が表示されます。その中から選ぶだけです。
>
> **複数 terminal を開いている場合は？** 各 terminal window はそれぞれ独立した session です。3 つ terminal を開いていれば 3 つの別 session があるということです。`--resume` はそれらを一覧から選べますし、`--continue` は最後に閉じたものを再開します。
>
> **再起動せずに session を切り替えられる？** はい。active session の中から `/resume` slash command を使えます。
> ```
> > /resume
> # Shows a list of sessions to switch to
> ```

### Session を整理する

後で見つけやすいように、わかりやすい名前を付けておきましょう。

```bash
copilot

> /rename book-app-review
# Session renamed for easier identification
```

### Context の確認と管理

files や conversation を重ねると、Copilot CLI の [context window](../GLOSSARY.md#context-window) は少しずつ埋まっていきます。次の command で状況を管理できます。

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandons the current session (no history saved) and starts a fresh conversation

> /new
# Ends the current session (saving it to history for search/resume) and starts a fresh conversation

> /rewind
# Opens a timeline picker allowing you to roll back to an earlier point in your conversation
```

> 💡 **`/clear` や `/new` を使うタイミング**: たとえば books.py の review から utils.py の話題へ切り替えたいなら、先に `/new` を実行しましょう（履歴が不要なら `/clear` でも OK）。古い topic の context が残っていると、返答が少しずれることがあります。

> 💡 **やり直したいときは？** `/rewind`（または Esc を 2 回）で **timeline picker** を開くと、直前だけでなく以前の任意の時点まで戻れます。別の進め方を試したいときに便利です。

---

### 途中から再開する

<img src="images/session-persistence-timeline.png" alt="Timeline showing how GitHub Copilot CLI sessions persist across days - start on Monday, resume on Wednesday with full context restored" width="800"/>

*session は終了時に自動保存されます。数日後でも、files・issues・進捗を含む context ごと再開できます。*

たとえば次のような workflow が可能です。

```bash
# Monday: Start book app review
copilot

> /rename book-app-review
> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# Work on the fix...

> /exit
```

```bash
# Wednesday: Resume exactly where you left off
copilot --continue

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**この flow が強い理由**: 数日経っても、Copilot CLI は次の情報を覚えています。
- どの file を見ていたか
- issue の一覧と優先度
- どこまで対応済みか
- 会話の context

説明し直したり、また最初から files を読み直したりせず、そのまま作業を再開できます。

---

**🎉 ここまでで essentials は十分です！** `@` syntax、session management（`--continue` / `--resume` / `/rename`）、context commands（`/context` / `/clear`）だけでもかなり実用的です。以下は optional なので、必要になったときに戻ってきてください。

---

# Optional: Going Deeper

<img src="images/optional-going-deeper.png" alt="Abstract crystal cave in blue and purple tones representing deeper exploration of context concepts" width="800"/>

ここから先は essentials を土台にした発展編です。**興味のあるところだけ選んで読めます。**

| 学びたいこと | 該当セクション |
|---|---|
| wildcard pattern や advanced session command | [Additional @ Patterns & Session Commands](#additional-patterns) |
| 複数 prompt をつなげる会話術 | [Context-Aware Conversations](#context-aware-conversations) |
| token 制限と `/compact` | [Understanding Context Windows](#understanding-context-windows) |
| どの files を参照すべきか | [Choosing What to Reference](#choosing-what-to-reference) |
| screenshot や mockup を使う方法 | [Working with Images](#working-with-images) |

<details>
<summary><strong>Additional @ Patterns & Session Commands</strong></summary>
<a id="additional-patterns"></a>

### Additional @ Patterns

power users 向けに、Copilot CLI は wildcard patterns や image references にも対応しています。

| Pattern | できること |
|---------|--------------|
| `@folder/*.py` | folder 内の .py files をまとめて参照 |
| `@**/test_*.py` | 再帰的に test files を探す |
| `@image.png` | UI review 用に image file を渡す |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### View Session Info

```bash
copilot

> /session
# Shows current session details and workspace summary

> /usage
# Shows session metrics and statistics
```

### Share Your Session

```bash
copilot

> /share file ./my-session.md
# Exports session as a markdown file

> /share gist
# Creates a GitHub gist with the session

> /share html
# Exports session as a self-contained interactive HTML file
```

</details>

<details>
<summary><strong>Context-Aware Conversations</strong></summary>
<a id="context-aware-conversations"></a>

### Context-Aware Conversations

本領を発揮するのは、multi-turn conversation で文脈を積み上げるときです。

#### Example: Progressive Enhancement

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

> Now improve error handling

> Generate tests for this final version
```

各 prompt が前の内容を土台にして前進していくのが、context の強みです。

</details>

<details>
<summary><strong>Understanding Context Windows</strong></summary>
<a id="understanding-context-windows"></a>

### Understanding Context Windows

AI には一度に扱える text 量に上限があり、それを context window と呼びます。

<img src="images/context-window-visualization.png" alt="Context Window Visualization" width="800"/>

*context window は机の広さのようなものです。files、会話履歴、system prompts がその中に並びます。*

#### What Happens at the Limit

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### The `/compact` Command

context を保ちながら token を節約したいときは `/compact` が便利です。

```bash
copilot

> /compact
# Summarizes conversation history, freeing up context space
```

#### Context Efficiency Tips

| 状況 | 取る行動 | 理由 |
|-----------|--------|-----|
| 新しい topic を始める | `/clear` | 不要な context を消す |
| 間違った方向に進んだ | `/rewind` | 以前の時点まで戻れる |
| 会話が長くなった | `/compact` | 履歴を要約して space を空ける |
| 特定 file だけ見たい | `@file.py` | 必要な分だけ読み込む |
| 上限に近い | `/new` or `/clear` | 新しい context で再開 |

</details>

<details>
<summary><strong>Choosing What to Reference</strong></summary>
<a id="choosing-what-to-reference"></a>

### Choosing What to Reference

context では「何を見せるか」が重要です。いつも folder 全体を渡せばよいわけではありません。

#### File Size Considerations

| File Size | おおよその Tokens | Strategy |
|-----------|-------------------|----------|
| Small (<100 lines) | ~500-1,500 tokens | 気軽に参照してよい |
| Medium (100-500 lines) | ~1,500-7,500 tokens | specific file を選ぶ |
| Large (500+ lines) | 7,500+ tokens | 必要箇所に絞る |
| Very Large (1000+ lines) | 15,000+ tokens | section 単位で考える |

#### What to Include vs. Exclude

**高い価値があるもの**:
- entry point files（`main.py`, `app.py` など）
- いま質問したい対象 file
- 関連する config files
- data model や dataclass 定義

**除外を考えてよいもの**:
- generated files
- dependency directories
- 巨大な fixture や無関係な data files

</details>

<details>
<summary><strong>Working with Images</strong></summary>
<a id="working-with-images"></a>

### Working with Images

`@` syntax で image を渡したり、clipboard から貼り付けたりして、screenshot や mockup を分析できます。

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design.
```

> 📖 **Learn more**: 詳しくは [Additional Context Features](../appendices/additional-context.md#working-with-images) を参照してください。

</details>

---

# Practice

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

ここまで学んだ context と session management を実際に試してみましょう。

---

## ▶️ Try It Yourself

### Full Project Review

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project
```

### Session Workflow

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles
> Implement that fix
> /exit

copilot --continue
> Generate tests for the changes we made
```

デモのあとには次も試してみてください。

1. **Cross-File Challenge**: `book_app.py` と `books.py` の関係を分析する
2. **Session Challenge**: `/rename` → `/exit` → `copilot --continue` で本当に続きから始まるか確認する
3. **Context Challenge**: `/context` や `/compact` を試して token usage を比べる

**Self-Check**: `@folder/` が、files を 1 つずつ開くより強力な理由を自分の言葉で説明できれば OK です。

---

## 📝 Assignment

### Main Challenge: Trace the Data Flow

今回は code quality review ではなく、app の中で data がどう流れているかを追ってみましょう。

1. interactive session を開始する: `copilot`
2. `books.py` と `book_app.py` を一緒に参照する
3. `data.json` も加えて、壊れていた場合にどこが失敗するか聞く
4. cross-file な error-handling strategy を提案してもらう
5. `/rename data-flow-analysis` で session 名を付ける
6. `/exit` 後、`copilot --continue` で再開して follow-up question を投げる

**成功条件**: 複数 file をまたぐ data flow を追え、session を再開し、cross-file suggestion を得られれば達成です。

<details>
<summary>💡 Hints（クリックして展開）</summary>

```bash
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

その後、`copilot --continue` で再開します。

</details>

### Bonus Challenge: Context Limits

1. `@samples/book-app-project/` で folder 全体を参照する
2. いくつか詳しい質問を重ねる
3. `/context` で usage を確認する
4. `/compact` を使って差を見てみる
5. file 単位で参照したときとの違いを比べる

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong>（クリックして展開）</summary>

### Common Mistakes

| Mistake | 起きること | Fix |
|---------|--------------|-----|
| file 名の前に `@` を付け忘れる | plain text として扱われる | `@samples/book-app-project/books.py` のように書く |
| session が自動で続くと思い込む | fresh session になってしまう | `--continue` や `--resume` を使う |
| topic を変えるのに `/clear` を使わない | 古い context が混ざる | topic 切り替え時に `/clear` を使う |

### Troubleshooting

**"File not found"** - current directory を確認し、relative path を見直します。

**"Permission denied"** - `/add-dir /path/to/directory` で許可を追加します。

**context がすぐ埋まる** - より specific な file reference を使い、topic ごとに session を分けます。

</details>

---

# Summary

## 🔑 Key Takeaways

1. **`@` syntax** を使うと、files・directories・images の context を Copilot CLI に渡せる
2. **multi-turn conversations** は context が積み上がるほど強くなる
3. **session は自動保存** されるので、`--continue` や `--resume` で続きから再開できる
4. **context windows** には上限があるので、`/clear`、`/compact`、`/context`、`/new`、`/rewind` で管理する
5. **permission flags**（`--add-dir`, `--allow-all`）で複数 directory への access を制御できる
6. **image references**（`@screenshot.png`）は UI の debug にも役立つ

> 📚 **Official Documentation**: context、sessions、files の扱いについては [Use Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) を参照してください。

> 📋 **Quick Reference**: コマンドやショートカットの一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次は？

Copilot CLI に context を渡せるようになったので、次はそれを実際の開発作業で活かしていきます。ここで学んだ file 参照、cross-file analysis、session management は、次章の powerful な workflow の土台になります。

**[Chapter 03: Development Workflows](../03-development-workflows/README.md)** では、次のことを学びます。

- code review workflows
- refactoring patterns
- debugging support
- test generation
- git integration

---

**[← Chapter 01 に戻る](../01-setup-and-first-steps/README.md)** | **[Chapter 03 へ進む →](../03-development-workflows/README.md)**
