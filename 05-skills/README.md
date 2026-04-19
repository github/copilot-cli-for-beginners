![第05章: Skills System](images/chapter-header.png)

> **毎回長い説明を書かなくても、team の best practices を Copilot が自動で適用してくれるとしたらどうでしょうか？**

この章では Agent Skills について学びます。skills は、task に関連するときに Copilot が自動で読み込む instructions の folder です。agents が *どう考えるか* を変えるのに対し、skills は *どうやって task を進めるか* を教えます。security audit skill や team 標準の review checklist を作ることで、GitHub Copilot CLI、VS Code、GitHub Copilot cloud agent 全体で一貫した品質を保てるようになります。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- Agent Skills の仕組みと使いどころを理解する
- SKILL.md files を使って custom skills を作る
- shared repositories の community skills を使う
- skills / agents / MCP の使い分けを理解する

> ⏱️ **想定時間**: 約55分（読む時間 20分 + ハンズオン 35分）

---

## 🧩 現実世界のたとえ: Power Tools

汎用 drill だけでも便利ですが、専用 attachment があると作業の幅が一気に広がります。
<img src="images/power-tools-analogy.png" alt="Power Tools - Skills Extend Copilot's Capabilities" width="800"/>

skills も同じです。drill bit を交換するように、task ごとに Copilot の能力を拡張できます。

| Skill Attachment | Purpose |
|------------|---------|
| `commit` | 一貫した commit message を生成する |
| `security-audit` | OWASP vulnerability を確認する |
| `generate-tests` | 包括的な pytest tests を作る |
| `code-checklist` | team の code quality standard を適用する |

*skills は、Copilot ができることを広げる specialized attachment です。*

---

# How Skills Work

<img src="images/how-skills-work.png" alt="Glowing RPG-style skill icons connected by light trails on a starfield background representing Copilot skills" width="800"/>

skills が何か、なぜ重要なのか、agents や MCP とどう違うのかを見ていきます。

---

## *Skills が初めてなら* ここから！

1. **まず available skills を確認する:**
   ```bash
   copilot
   > /skills list
   ```
   これで、CLI に built-in で入っている skills と、project / personal folder の skills を一覧できます。

   > 💡 **built-in skills**: Copilot CLI には最初から skill がいくつか含まれています。追加インストールなしで使えるものもあります。

2. **実際の skill file を見る:** [code-checklist SKILL.md](../.github/skills/code-checklist/SKILL.md) は、frontmatter + markdown instructions の分かりやすい例です。

3. **考え方をつかむ:** skills は、prompt が description に合うと *自動的に* 読み込まれます。毎回手動で有効化する必要はありません。

## Understanding Skills

Agent Skills は、instructions、scripts、resources をまとめた folder で、**relevant な task に対して Copilot が自動で読み込む** 仕組みです。Copilot は prompt を読み、match する skill があればその instructions を裏側で適用します。

```bash
copilot

> Check books.py against our quality checklist
# Copilot detects this matches your "code-checklist" skill
# and automatically applies its Python quality checklist

> Generate tests for the BookCollection class
# Copilot loads your "pytest-gen" skill
# and applies your preferred test structure

> What are the code quality issues in this file?
# Copilot loads your "code-checklist" skill
# and checks against your team's standards
```

> 💡 **Key Insight**: skills は **prompt の内容に応じて自動発火** します。自然に頼むだけで、Copilot が relevant な skill を裏側で適用します。必要なら direct invocation も可能です。

> 🧰 **すぐ試せる templates**: [.github/skills](../.github/skills/) folder に sample skills が入っています。

### Slash Command で直接呼ぶ

auto-trigger が基本ですが、skill 名を slash command として直接使うこともできます。

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

この方法なら、「この skill を明示的に使いたい」ときに便利です。

> 📝 **Skills と Agents の違い**:
> - **Skills**: `/skill-name <prompt>` 例: `/code-checklist Check this file`
> - **Agents**: `/agent` で選択、または `copilot --agent <name>`
>
> 同じ名前の skill と agent が両方ある場合、`/name` は **skill** を呼び出します。

### Skill が使われたかどうか知るには？

Copilot にそのまま質問できます。

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### Skills vs Agents vs MCP

skills は GitHub Copilot の extensibility model の一部です。agents や MCP と比べると、役割の違いは次のとおりです。

> *MCP は次章の [Chapter 06](../06-mcp-servers/) で詳しく扱います。ここでは位置づけだけ分かれば十分です。*

<img src="images/skills-agents-mcp-comparison.png" alt="Comparison diagram showing the differences between Agents, Skills, and MCP Servers and how they combine into your workflow" width="800"/>

| Feature | できること | 使う場面 |
|---------|--------------|-------------|
| **Agents** | AI の考え方を変える | 幅広い task で専門性が欲しいとき |
| **Skills** | task-specific な instructions を与える | 特定の手順を標準化したいとき |
| **MCP** | 外部 service と接続する | API や live data が必要なとき |

broad な expertise には agents、細かい作業手順には skills、external data には MCP、という使い分けです。

> 📚 **Learn More**: 詳細は [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) を参照してください。

---

## Manual Prompt から Automatic Expertise へ

skill をどう作るかに入る前に、*なぜ* 便利なのかを見ておきましょう。

### Skills なし: Review が毎回ぶれやすい

```bash
copilot

> Review this code for issues
# Generic review - might miss your team's specific concerns
```

または、毎回長い prompt を書く必要があります。

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

時間: **30 秒以上**。一貫性: **自分の記憶次第**。

### Skills あり: Best Practices を自動適用

`code-checklist` skill が入っていれば、自然な prompt だけで済みます。

```bash
copilot

> Check the book collection code for quality issues
```

**裏側で起きていること:**
1. Copilot が prompt 内の phrase を読む
2. 合いそうな skill の description を探す
3. relevant な skill を読み込む
4. その checklist を適用して output を返す

<img src="images/skill-auto-discovery-flow.png" alt="How Skills Auto-Trigger - 4-step flow showing how Copilot automatically matches your prompt to the right skill" width="800"/>

*自然に頼むだけで、Copilot が適切な skill を見つけて使ってくれます。*

**出力例**:
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**違い**: team の標準が、毎回・自動で・漏れなく適用されることです。

---

<details>
<summary>🎬 動作例を見る</summary>

![Skill Trigger Demo](images/skill-trigger-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

## Team PR Review Skill で一貫性を出す

team に 10 項目の PR checklist があると想像してください。skill がなければ、毎回だれかが見落とします。`pr-review` skill があれば、review 基準を team 全体でそろえられます。

```bash
copilot

> Can you review this PR?
```

Copilot が team の `pr-review` skill を自動で読み込み、全項目を確認します。

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**強み**: new team member でも、同じ基準で review を進められます。

---

# Creating Custom Skills

<img src="images/creating-managing-skills.png" alt="Human and robotic hands building a wall of glowing LEGO-like blocks representing skill creation and management" width="800"/>

SKILL.md files を使って、自分用・team 用の skills を作りましょう。

---

## Skill Locations

skills は `.github/skills/`（project-specific）または `~/.copilot/skills/`（user-level）に置きます。

### Copilot が Skills を探す場所

| Location | Scope |
|----------|-------|
| `.github/skills/` | project-specific（git で team 共有） |
| `~/.copilot/skills/` | user-specific（個人用） |

### Skill Structure

各 skill は専用 folder の中に `SKILL.md` を持ちます。必要に応じて examples や scripts を同梱できます。

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Required: Skill definition and instructions
    ├── examples/          # Optional: Example files Copilot can reference
    │   └── sample.py
    └── scripts/           # Optional: Scripts the skill can use
        └── validate.sh
```

> 💡 **Tip**: directory 名は `name` と合わせるのがおすすめです（lowercase + hyphens）。

### SKILL.md Format

skills では、YAML frontmatter + markdown を使います。

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML Properties:**

| Property | Required | Description |
|----------|----------|-------------|
| `name` | **Yes** | 一意の identifier |
| `description` | **Yes** | 何をする skill か、いつ使うか |
| `license` | No | skill に適用する license |

> 📖 **Official docs**: [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### 最初の Skill を作る

OWASP Top 10 vulnerabilities を確認する security audit skill を作る例です。

```bash
# Create skill directory
mkdir -p .github/skills/security-audit

# Create the SKILL.md file
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Test your skill (skills load automatically based on your prompt)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot detects "security vulnerabilities" matches your skill
# and automatically applies its OWASP checklist
```

**期待される出力**（実際の結果は変わります）:

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## 良い Skill Description の書き方

`description` field はとても重要です。Copilot が skill を自動発見する主な手がかりだからです。

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **Tip**: 自分が自然に使う言い回しを description に入れてください。たとえば "security review" と聞くことが多いなら、その語を含めます。

### Skills と Agents を組み合わせる

agents と skills は一緒に使えます。agent が broad な expertise を持ち、skill が具体的な手順を補う形です。

```bash
# Start with a code-reviewer agent
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer agent's expertise combines
# with your code-checklist skill's checklist
```

---

# Managing and Sharing Skills

インストール済み skills の確認、community skills の導入、共有方法を見ていきます。

<img src="images/managing-sharing-skills.png" alt="Managing and Sharing Skills - showing the discover, use, create, and share cycle for CLI skills" width="800" />

---

## `/skills` Command で管理する

インストール済み skill の確認や再読み込みには `/skills` command を使います。

| Command | できること |
|---------|--------------|
| `/skills list` | インストール済み skills を一覧する |
| `/skills info <name>` | 特定の skill の詳細を見る |
| `/skills add <name>` | skill を有効化する |
| `/skills remove <name>` | skill を無効化 / uninstall する |
| `/skills reload` | SKILL.md 編集後に再読み込みする |

> 💡 **Remember**: 毎 prompt ごとに「activate」する必要はありません。install 済み skills は、description に合う prompt に対して **自動で発火** します。

### Example: skills を表示する

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>動作例を見る</summary>

![List Skills Demo](images/list-skills-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

### `/skills reload` を使うタイミング

SKILL.md を作成または編集したあとは、Copilot を再起動しなくても `/skills reload` で変更を取り込めます。

```bash
# Edit your skill file
# Then in Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **Good to know**: `/compact` で会話履歴を要約しても、skills は引き続き有効です。

---

## Community Skills を探して使う

### Plugins で Skills を入れる

> 💡 **plugins とは？** plugins は、skills、agents、MCP server configurations をまとめて配布できる installable package です。Copilot CLI の拡張パックのようなものです。

`/plugin` command を使うと browse / install できます。

```bash
copilot

> /plugin list
# Shows installed plugins

> /plugin marketplace
# Browse available plugins

> /plugin install <plugin-name>
# Install a plugin from the marketplace
```

plugin catalog を最新にするには、次を実行します。

```bash
copilot plugin marketplace update
```

### Community Skill Repositories

ready-made skill は community repositories でも公開されています。

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - official resources と skill examples をまとめた repository

### GitHub CLI で Community Skill を入れる

GitHub repository から skill を入れる最も簡単な方法は、`gh skill install` command を使うことです。

```bash
# Browse and interactively select a skill from awesome-copilot
gh skill install github/awesome-copilot

# Or install a specific skill directly
gh skill install github/awesome-copilot code-checklist

# Install for personal use across all projects (user scope)
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **install 前に review する**: どんな skill でも、install 前に `SKILL.md` を読んで安全性を確認してください。

---

# Practice

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

自分で skills を作って試してみましょう。

---

## ▶️ Try It Yourself

### さらに Skills を作る

以下は別パターンの skill 例です。上の「Creating Your First Skill」と同じ `mkdir` + `cat` の流れで作れます。詳しい例は [.github/skills](../.github/skills) にもあります。

### pytest Test Generation Skill

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### Team PR Review Skill

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### Go Further

1. **Skill Creation Challenge**: 次の 3 点を確認する `quick-review` skill を作ってみましょう。
   - bare except clauses
   - missing type hints
   - unclear variable names

2. **Skill Comparison**: 自分で detail な security review prompt を書く場合と、「Check for security issues in this file」と自然に頼む場合を比べてみてください。skill がどれだけ時短になるか分かります。

3. **Team Skill Challenge**: team の code review checklist を思い出し、skill にするなら必ず確認したい 3 点を書き出してみてください。

**Self-Check**: `description` field がなぜ重要か説明できれば、skills の本質を理解できています。

---

## 📝 Assignment

### Main Challenge: Book Summary Skill を作る

上の examples では `pytest-gen` と `pr-review` を作りました。今度は、**データを整った markdown summary に変換する skill** を作ってみましょう。

1. 現在の skills を確認します: `/skills list`、または `ls .github/skills/` / `ls ~/.copilot/skills/`
2. `.github/skills/book-summary/SKILL.md` に `book-summary` skill を作ります
3. この skill には次を入れます。
   - 明確な name と description
   - formatting rules（markdown table、title、author、year、read status など）
   - output conventions（✅/❌、year 順 sort など）
4. skill を試します: `@samples/book-app-project/data.json Summarize the books in this collection`
5. `/skills list` や挙動で auto-trigger を確認します
6. `/book-summary Summarize the books in this collection` で direct invocation も試します

**成功条件**: book collection について聞いたときに、自動で効く `book-summary` skill が動作することです。

<details>
<summary>💡 Hints（クリックして展開）</summary>

**starter template**:

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)
```

**試し方:**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
```

**発火しない場合:** `/skills reload` を実行してから再試行します。

</details>

### Bonus Challenge: Commit Message Skill

1. conventional commit message を一貫した format で生成する `commit-message` skill を作る
2. 変更を stage してから「Generate a commit message for my staged changes」と聞いて試す
3. 説明を整えて GitHub で共有する

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong>（クリックして展開）</summary>

### Common Mistakes

| Mistake | 起きること | Fix |
|---------|--------------|-----|
| file 名が `SKILL.md` ではない | skill が認識されない | file 名は必ず `SKILL.md` |
| `description` が曖昧 | 自動発火しない | trigger words を含めた具体的な説明にする |
| `name` / `description` がない | skill が読み込まれない | YAML frontmatter に両方入れる |
| folder の場所が違う | skill が見つからない | `.github/skills/skill-name/` または `~/.copilot/skills/skill-name/` を使う |

### Troubleshooting

**skill が使われない** - まず次を確認します。

1. **description が自分の聞き方に合っているか**
2. **file location が正しいか**
3. **SKILL.md format が正しいか**
4. **`/skills reload` を実行したか**

**本当に効いているか確かめる方法:**
- output format に skill らしい特徴が出ているか見る
- 「Did you use any skills for that?」と直接聞く
- `--no-custom-instructions` あり / なしで比較する

</details>

---

# Summary

## 🔑 Key Takeaways

1. **skills は自動で使われる**: prompt が description に合うと Copilot が読み込む
2. **direct invocation も可能**: `/skill-name` 形式で明示的に呼べる
3. **SKILL.md format**: YAML frontmatter + markdown instructions
4. **置き場所が重要**: `.github/skills/` は project / team 共有、`~/.copilot/skills/` は個人用
5. **description が要**: 自然な聞き方に合う言葉を含めて書く

> 📋 **Quick Reference**: コマンドやショートカットの一覧は [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次は？

skills は auto-loaded instructions によって Copilot の作業を広げます。では、外部 service とつなぐにはどうするのでしょうか？ そこで MCP の出番です。

**[Chapter 06: MCP Servers](../06-mcp-servers/README.md)** では、次のことを学びます。

- MCP（Model Context Protocol）とは何か
- GitHub、filesystem、documentation services と接続する方法
- MCP server の設定方法
- multi-server workflow

---

**[← Chapter 04 に戻る](../04-agents-custom-instructions/README.md)** | **[Chapter 06 へ進む →](../06-mcp-servers/README.md)**
