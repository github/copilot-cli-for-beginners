![第04章: Agents and Custom Instructions](images/chapter-header.png)

> **Python code reviewer や testing expert、security reviewer を、1 つの tool の中で使い分けられるとしたらどうでしょうか？**

Chapter 03 では、code review、refactoring、debugging、test generation、git integration といった基本 workflow を学びました。ここからは、それをさらに一歩進めます。

これまでは Copilot CLI を汎用 assistant として使ってきました。Agents を使うと、「type hints と PEP 8 を重視する code reviewer」や「pytest を得意とする testing helper」のように、特定の役割と基準を持った specialist として振る舞わせることができます。同じ prompt でも、agent の指示が入ることで結果の質が大きく変わることを体感できます。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- built-in agents（Plan `/plan`、Code-review `/review`）を使い、automatic agents（Explore、Task）の役割を理解する
- agent files（`.agent.md`）で specialized agent を作成する
- domain-specific な task に agents を使う
- `/agent` や `--agent` で agent を切り替える
- project 固有の standards を custom instruction files にまとめる

> ⏱️ **想定時間**: 約55分（読む時間 20分 + ハンズオン 35分）

---

## 🧩 現実世界のたとえ: 専門家を呼ぶ

家のトラブルを解決するとき、毎回「何でも屋」を呼ぶわけではありません。内容に応じて specialist を選びます。

| 問題 | 呼ぶ specialist | 理由 |
|---------|------------|-----|
| 水漏れ | Plumber | 配管の知識と専用 tool がある |
| 配線のやり直し | Electrician | safety 要件や規格に詳しい |
| 屋根の交換 | Roofer | 材料や気候条件の知識がある |

Agents も同じです。generic な AI を毎回使うのではなく、task に合った specialist を使い分けます。code review、testing、security、documentation など、必要な expertise を一度定義すれば何度でも再利用できます。

<img src="images/hiring-specialists-analogy.png" alt="Hiring Specialists Analogy - Just as you call specialized tradespeople for house repairs, AI agents are specialized for specific tasks like code review, testing, security, and documentation" width="800" />

---

# Using Agents

built-in agents と custom agents を、まずは気軽に触ってみましょう。

---

## *Agents が初めてなら* ここから！

agent をまだ使ったことがなくても大丈夫です。このコースで必要な starting point は次の 3 つです。

1. **まず built-in agent を試す:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   これは Plan agent を呼び出し、step-by-step の implementation plan を作ります。

2. **custom agent の実例を見る:** 専用の instructions を書くだけで agent を定義できます。まずは [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) を見てみましょう。

3. **考え方をつかむ:** agents は「generalist に相談する」のではなく「specialist に相談する」イメージです。たとえば frontend agent なら accessibility や component pattern を自然に重視してくれます。


## Built-in Agents

**Chapter 03 で使っていた `/plan` と `/review` は、実は built-in agents です。** ここではその全体像を見てみましょう。

| Agent | 呼び出し方 | できること |
|-------|---------------|--------------|
| **Plan** | `/plan` または `Shift+Tab` | coding 前に step-by-step の implementation plan を作る |
| **Code-review** | `/review` | staged / unstaged changes を review して、実用的な feedback を返す |
| **Init** | `/init` | project 用の configuration files（instructions や agents）を生成する |
| **Explore** | *Automatic* | codebase を探索・分析する task で内部的に使われる |
| **Task** | *Automatic* | tests、build、lint、dependency install などの command 実行を担当する |

<br>

**built-in agents の例** - Plan、Code-review、Explore、Task がどのように使われるか

```bash
copilot

# Invoke the Plan agent to create an implementation plan
> /plan Add input validation for book year in the book app

# Invoke the Code-review agent on your changes
> /review

# Explore and Task agents are invoked automatically when relevant:
> Run the test suite        # Uses Task agent

> Explore how book data is loaded    # Uses Explore agent
```

Task Agent は裏側で進行を管理し、結果をわかりやすく返してくれます。

| Outcome | 表示されるもの |
|---------|--------------|
| ✅ **Success** | 短い summary（例: "All 247 tests passed", "Build succeeded"） |
| ❌ **Failure** | stack trace、compiler error、detailed logs などを含む完全な出力 |


> 📚 **Official Documentation**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Copilot CLI に Agents を追加する

自分の workflow に合わせて、独自の agent を追加することもできます。定義は 1 回、活用は何度でも、です。

<img src="images/using-agents.png" alt="Four colorful AI robots standing together, each with different tools representing specialized agent capabilities" width="800"/>

## 🗂️ Agent を追加する

Agent file は `.agent.md` extension を持つ markdown file です。構成は 2 つだけです。YAML frontmatter（metadata）と markdown instructions です。

> 💡 **YAML frontmatter が初めてでも大丈夫**: file の先頭に `---` で囲まれた設定ブロックを書き、その下に普通の markdown を続けるだけです。

最小構成の例はこちらです。

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

> 💡 **必須と任意**: `description` は必須です。`name`、`tools`、`model` などは任意です。

## Agent file の置き場所

| Location | Scope | 向いている用途 |
|----------|-------|----------|
| `.github/agents/` | project-specific | team で共有したい agent |
| `~/.copilot/agents/` | global（全 project） | 自分専用でどこでも使いたい agent |

**この project には [.github/agents/](../.github/agents/) に sample agent files が入っています。** そのまま使っても、カスタマイズしても構いません。

<details>
<summary>📂 このコースに含まれる sample agents</summary>

| File | 説明 |
|------|-------------|
| `hello-world.agent.md` | 最小構成の example - まずはここから |
| `python-reviewer.agent.md` | Python code quality reviewer |
| `pytest-helper.agent.md` | Pytest testing specialist |

```bash
# Or copy one to your personal agents folder (available in every project)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

より多くの community agents は [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>


## 🚀 custom agents の 2 つの使い方

### Interactive mode

interactive mode の中では `/agent` で利用可能な agent 一覧を出し、選んで会話を続けられます。

```bash
copilot
> /agent
```

別の agent に切り替えたいときや default に戻したいときも、もう一度 `/agent` を使います。

### Programmatic mode

最初から特定の agent を指定して新しい session を始めることもできます。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **agent の切り替え**: `/agent` や `--agent` を使えば、いつでも別の agent に変更できます。標準の Copilot CLI に戻したい場合は `/agent` を開いて **no agent** を選んでください。

---

# Agents をさらに深く使う

<img src="images/creating-custom-agents.png" alt="Robot being assembled on a workbench surrounded by components and tools representing custom agent creation" width="800"/>

> 💡 **この section は optional です。** built-in agents（`/plan`, `/review`）だけでも多くの workflow には十分対応できます。特定の expertise を継続的に適用したいときに custom agents が効いてきます。

以下の topic はそれぞれ独立しています。**興味のあるものから読めば OK です。**

| やりたいこと | 該当セクション |
|---|---|
| generic prompt と agent の差を見たい | [Specialist vs Generic](#specialist-vs-generic-see-the-difference) |
| 1 つの feature で複数 agent を使いたい | [Working with Multiple Agents](#working-with-multiple-agents) |
| agent の名前付けや共有方法を知りたい | [Organizing & Sharing Agents](#organizing--sharing-agents) |
| always-on の project context を設定したい | [Configuring Your Project for Copilot](#configuring-your-project-for-copilot) |
| YAML property や tools の指定を調べたい | [Agent File Reference](#agent-file-reference) |

下の scenario を必要に応じて開いてください。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>Specialist vs Generic: 差を見てみる</strong> - なぜ agent の方が generic prompt より良い出力になるのか</summary>

## Specialist vs Generic: 差を見てみる

ここで agents の価値がよく分かります。同じ prompt でも、扱う agent が違うと結果が変わります。

### Agent なし（Generic Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
```

**Generic output**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

動きますが、考慮が足りない部分もあります。

---

### Python Reviewer Agent を使う場合

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
```

**Specialist output**:
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

**python-reviewer agent が自動的に含めてくれるもの:**
- ✅ parameter と return value の type hints
- ✅ Args / Returns / Raises を含む丁寧な docstring
- ✅ input validation と error handling
- ✅ より読みやすい list comprehension
- ✅ edge case の考慮（無効な year など）
- ✅ PEP 8 に沿った format
- ✅ defensive programming の考え方

**違い**: prompt は同じでも、agent の expertise が入るだけで出力の完成度が一段上がります。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>Working with Multiple Agents</strong> - specialist を組み合わせ、途中で切り替え、tool のように使う</summary>

## Working with Multiple Agents

本当に便利なのは、複数の specialist を feature ごとに使い分けるときです。

### Example: シンプルな Feature を作る

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Use python-reviewer for design
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Switch to pytest-helper for test design
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Synthesize both designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**重要ポイント**: 自分が architect となって specialist を動かすイメージです。vision は自分が持ち、細部は agent に助けてもらいます。

<details>
<summary>🎬 動作例を見る</summary>

![Python Reviewer Demo](images/python-reviewer-demo.gif)

*Demo output varies - your model, tools, and responses will differ from what's shown here.*

</details>

### Agent as Tools

agent が設定されていると、複雑な task の中で Copilot がそれらを tool のように呼び出すこともあります。full-stack な feature の一部を、適切な specialist に自動で振り分けてくれるイメージです。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>Organizing & Sharing Agents</strong> - 名前付け、配置、instruction files、team 共有</summary>

## Organizing & Sharing Agents

### Agent の名前をどう付けるか

agent file を作ると、その name は `/agent` や `--agent` で使うことになります。team にも見えるので、分かりやすい名前が大切です。

| ✅ 良い例 | ❌ 避けたい例 |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名ルールのおすすめ:**
- lowercase + hyphen にする: `my-agent-name.agent.md`
- domain を含める: `frontend`, `backend`, `devops`, `security`
- 必要ならより具体的に: `react-typescript` など

---

### Team で共有する

agent files を `.github/agents/` に置けば、git 管理され、push した時点で team 全員が同じものを使えます。ただし、Copilot が読む project file は agent だけではありません。**instruction files** を使えば、毎回 `/agent` を選ばなくても session 全体に自動適用できます。

つまり、agents は「必要なときに呼ぶ specialist」、instruction files は「常に効いている team rule」です。

### Files をどこに置くか

上で紹介した 2 つの配置先（project / global）を基本に、まずは簡単に始めるのがよいです。

<img src="images/agent-file-placement-decision-tree.png" alt="Decision tree for where to put agent files: experimenting → current folder, team use → .github/agents/, everywhere → ~/.copilot/agents/" width="800"/>

**まずはシンプルに:** project folder に 1 つ `*.agent.md` を作り、うまくいったら恒久的な場所へ移しましょう。

project-level instruction files については、下の [Configuring Your Project for Copilot](#configuring-your-project-for-copilot) を参照してください。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Configuring Your Project for Copilot</strong> - AGENTS.md、instruction files、/init setup</summary>

## Configuring Your Project for Copilot

agents は必要なときに呼ぶ specialist です。これとは別に、**project configuration files** はすべての session で自動的に読み込まれ、project の conventions、tech stack、rule を Copilot に伝えます。

### `/init` で素早く始める

最も簡単なのは、Copilot に configuration files を生成してもらう方法です。

```bash
copilot
> /init
```

Copilot が project を scan して、合った instruction files を作成します。あとから手で調整しても構いません。

### Instruction File の形式

| File | Scope | Notes |
|------|-------|-------|
| `AGENTS.md` | project root または nested | **cross-platform standard** - Copilot 以外の AI assistant でも使いやすい |
| `.github/copilot-instructions.md` | project | GitHub Copilot 専用 |
| `.github/instructions/*.instructions.md` | project | topic ごとに分けた granular な instructions |
| `CLAUDE.md`, `GEMINI.md` | project root | 互換性のためにサポート |

> 🎯 **まず始めるなら** `AGENTS.md` がおすすめです。必要に応じて他の形式も追加してください。

### AGENTS.md

`AGENTS.md` は推奨 format です。[open standard](https://agents.md/) であり、Copilot と他の AI coding tools の両方で使いやすいのが特徴です。この project の [AGENTS.md](../AGENTS.md) も実例として参考になります。

### Custom Instruction Files（.instructions.md）

さらに細かく管理したい team は、topic ごとに instruction file を分けることもできます。

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **Note**: Python の例を載せていますが、TypeScript、Go、Rust など他の tech stack でも同じ考え方で使えます。

community の instruction files を探したいときは [github/awesome-copilot](https://github.com/github/awesome-copilot) を見てみてください。

### Custom Instructions を無効にする

project 固有の configuration をいったん無視したい場合は、次を使います。

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>Agent File Reference</strong> - YAML properties、tool aliases、完全な example</summary>

## Agent File Reference

### もう少し完全な Example

上では [minimal agent format](#-add-your-agents) を見ました。ここでは `tools` property を使った、もう少し実践的な example を示します。`~/.copilot/agents/python-reviewer.agent.md` を作る想定です。

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

### YAML Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | No | 表示名（省略時は filename 由来） |
| `description` | **Yes** | その agent が何をするか。Copilot が提案タイミングを理解する助けになる |
| `tools` | No | 利用を許可する tools 一覧（省略時は使えるものをすべて許可） |
| `target` | No | `vscode` または `github-copilot` に限定する |

### Tool Aliases

`tools` list では次の名前を使います。
- `read` - file contents を読む
- `edit` - files を編集する
- `search` - files を検索する（grep / glob）
- `execute` - shell command を実行する（`shell`, `Bash` でも可）
- `agent` - 他の custom agents を呼び出す

> 📖 **Official docs**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Code Only**: `model` property は VS Code では使えますが、GitHub Copilot CLI ではサポートされません。cross-platform file として入っていても CLI 側では無視されるので問題ありません。

### More Agent Templates

> 💡 **beginner 向け Note**: 下の examples は template です。**自分の project で使う tech stack に置き換えて大丈夫です。** 大切なのは具体例の技術名より、agent の *構造* です。

この project には、[.github/agents/](../.github/agents/) にすぐ使える example が入っています。
- [hello-world.agent.md](../.github/agents/hello-world.agent.md) - 最小 example
- [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) - Python code quality reviewer
- [pytest-helper.agent.md](../.github/agents/pytest-helper.agent.md) - Pytest testing specialist

community agents は [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>

---

# Practice

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

自分の agents を作り、実際に動かしてみましょう。

---

## ▶️ Try It Yourself

まずは自分で 2 つの simple agent を作って動かしてみましょう。

```bash
# Create the agents directory (if it doesn't exist)
mkdir -p .github/agents

# Create a code reviewer agent
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

# Create a documentation agent
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

# Now use them
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# Or switch agents
copilot
> /agent
# Select "documentor"
> Document @samples/book-app-project/books.py
```

---

## 📝 Assignment

### Main Challenge: Build a Specialized Agent Team

ハンズオンでは `reviewer` と `documentor` を作りました。次は book app 向けに、より具体的な agent team を作ってみましょう。

1. `.github/agents/` に 3 つの `.agent.md` files を作る
2. それぞれの役割:
   - **data-validator**: `data.json` の欠損や不正値を確認する
   - **error-handler**: Python code の error handling の一貫性を review する
   - **doc-writer**: docstring や README の説明を整える
3. 各 agent を book app に対して使ってみる
4. 最後に agent を切り替えながら、改善 → 文書化までつなげる

**成功条件**: 3 つの agent がそれぞれ一貫した output を返し、`/agent` で切り替えながら使えることです。

<details>
<summary>💡 Hints（クリックして展開）</summary>

**Starter templates:**

`data-validator.agent.md`
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

`error-handler.agent.md`
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

`doc-writer.agent.md`
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

</details>

### Bonus Challenge: Instruction Library

agents を on-demand で呼ぶだけでなく、**instruction files** を使って project 全体のルールを自動適用してみましょう。

- `python-style.instructions.md`
- `test-standards.instructions.md`
- `data-quality.instructions.md`

これらを `.github/instructions/` に置き、book app code にどのような影響が出るか試してみてください。

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong>（クリックして展開）</summary>

### Common Mistakes

| Mistake | 起きること | Fix |
|---------|--------------|-----|
| `description` を書き忘れる | agent が見つからない / 認識されない | YAML frontmatter に `description:` を必ず入れる |
| file の置き場所が違う | `/agent` に出てこない | `~/.copilot/agents/` または `.github/agents/` に置く |
| `.agent.md` ではなく `.md` にする | agent として認識されない | filename を `something.agent.md` にする |
| 指示を盛り込みすぎる | 読みづらくなり効果が落ちる | 専門性を絞ってシンプルに書く |

### Troubleshooting

**Agent not found** - file の場所、extension、frontmatter を確認します。

**Agent not following instructions** - prompt 側でも目的を少し具体的に補足します。

**Custom instructions not loading** - `/init` を使って project instructions を初期化してみてください。

</details>

---

# Summary

## 🔑 Key Takeaways

1. **built-in agents**: `/plan` や `/review` はすぐ使える specialist
2. **custom agents**: `.agent.md` files で自分や team の専門家を作れる
3. **良い agent**: expertise、standards、output format が明確
4. **multi-agent collaboration**: 複雑な task を役割分担で進められる
5. **instruction files**: team rule を毎回自動で反映できる

> 📋 **Quick Reference**: コマンドやショートカットの一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次は？

agents は *どう考えて進めるか* を強化します。次の Chapter 05 では、**skills** を使って *どんな手順を踏むか* をより具体的に整えていきます。

**[Chapter 05: Skills System](../05-skills/README.md)** では、次のことを学びます。

- prompt に応じて skill が auto-trigger される仕組み
- community skills の使い方
- `SKILL.md` files を使った custom skills の作り方
- agents、skills、MCP の違い

---

**[← Chapter 03 に戻る](../03-development-workflows/README.md)** | **[Chapter 05 へ進む →](../05-skills/README.md)**
