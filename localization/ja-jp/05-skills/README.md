![第 05 章: スキルシステム](../../../images/chapter-header.png)

> **チームのベストプラクティスを毎回説明しなくても Copilot が自動的に適用してくれたら？**

この章では、エージェントスキルについて学びます。スキルはタスクに関連するときに Copilot が自動的に読み込む指示のフォルダです。エージェントが Copilot の*思考方法*を変えるのに対して、スキルは Copilot に*タスクを完了する具体的な方法*を教えます。セキュリティについて質問するたびに Copilot が適用するセキュリティ監査スキルを作成し、一貫したコード品質を確保するチーム標準のレビュー基準を構築し、スキルが Copilot CLI、VS Code、GitHub Copilot クラウドエージェント全体でどのように機能するかを学びます。


## 🎯 学習目標

この章を終えると、以下ができるようになります。

- エージェントスキルがどのように機能し、いつ使うべきかを理解する
- SKILL.md ファイルでカスタムスキルを作成する
- 共有リポジトリからコミュニティスキルを使用する
- スキル対エージェント対 MCP をいつ使うかを知る

> ⏱️ **目安時間**: 約 55 分（20 分読む + 35 分ハンズオン）

---

## 🧩 現実世界のたとえ話: 電動工具

汎用ドリルは便利ですが、特化したアタッチメントで強力になります。
<img src="../../../images/power-tools-analogy.png" alt="電動工具 - スキルが Copilot の機能を拡張する" width="800"/>


スキルも同様に機能します。ドリルビットを異なる作業に交換するように、異なるタスクのために Copilot にスキルを追加できます。

| スキルアタッチメント | 目的 |
|------------|---------|
| `commit` | 一貫したコミットメッセージを生成する |
| `security-audit` | OWASP の脆弱性をチェックする |
| `generate-tests` | 包括的な pytest テストを作成する |
| `code-checklist` | チームのコード品質基準を適用する |



*スキルは Copilot ができることを拡張する特化したアタッチメントです*

---

# スキルの仕組み

<img src="../../../images/how-skills-work.png" alt="Copilot スキルを表す星空を背景に光のトレイルで繋がれた輝く RPG スタイルのスキルアイコン" width="800"/>

スキルとは何か、なぜ重要か、エージェントや MCP とどう違うかを学びましょう。

---

## *スキルが初めてですか？* ここから始めましょう！

1. **すでに利用可能なスキルを確認する:**
   ```bash
   copilot
   > /skills list
   ```
   これは Copilot が見つけることができるすべてのスキルを表示します。CLI 自体に付属している**組み込みスキル**と、プロジェクトや個人フォルダのスキルが含まれます。

   > 💡 **組み込みスキル**: Copilot CLI にはすぐに使えるスキルがプレインストールされています。たとえば、`customizing-copilot-cloud-agents-environment` スキルは Copilot クラウドエージェントの環境をカスタマイズするためのガイドを提供します。使用するために何も作成・インストールする必要はありません。`/skills list` を実行して何が利用可能かを確認してください。

2. **実際のスキルファイルを見てみましょう:** 提供されている [code-checklist SKILL.md](../../../.github/skills/code-checklist/SKILL.md) を確認してパターンを確認してください。YAML フロントマターと Markdown 指示だけです。

3. **コアコンセプトを理解する:** スキルはプロンプトがスキルの説明と一致するときに Copilot が*自動的に*読み込むタスク固有の指示です。有効化する必要はなく、自然に聞くだけです。


## スキルを理解する

エージェントスキルは、タスクに**関連するときに Copilot が自動的に読み込む**指示、スクリプト、リソースを含むフォルダです。Copilot はプロンプトを読み、スキルが一致するかどうかを確認し、関連する指示を自動的に適用します。

```bash
copilot

> Check books.py against our quality checklist
# Copilot はこれが "code-checklist" スキルと一致することを検出する
# そして自動的に Python 品質チェックリストを適用する

> Generate tests for the BookCollection class
# Copilot は "pytest-gen" スキルを読み込む
# そして好みのテスト構造を適用する

> What are the code quality issues in this file?
# Copilot は "code-checklist" スキルを読み込む
# そしてチームの標準に対してチェックする
```

> 💡 **重要なポイント**: スキルはプロンプトがスキルの説明と一致することに基づいて**自動的にトリガー**されます。自然に聞くだけで Copilot が関連するスキルをバックグラウンドで適用します。スキルを直接呼び出すこともできます。次で学びます。

> 🧰 **すぐに使えるテンプレート**: 試せるシンプルなコピー&ペーストスキルは [.github/skills](../../../.github/skills/) フォルダを確認してください。

### 直接スラッシュコマンドで呼び出す

自動トリガーがスキルの主な使い方ですが、名前をスラッシュコマンドとして使って**スキルを直接呼び出す**こともできます。

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

これにより、特定のスキルが使用されることを確認したいときに明示的な制御ができます。

#### 1 つのメッセージで複数のスキルを組み合わせる

1 つのメッセージで**複数のスキルを呼び出す**ことができ、スキルのスラッシュコマンドはプロンプトのどこにでも置けます（最初だけではありません）。これは 2 種類のチェックを一度に行いたいときに便利です。

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot は同じレスポンスで各指定スキルを適用し、複数の別々のメッセージを送る手間を省きます。

> 💡 **ヒント**: スキルのスラッシュコマンドを文章の中で最も自然な場所に置いてください。メッセージの先頭、中間、末尾に置けます。

> 📝 **スキル対エージェントの呼び出し**: スキルの呼び出しとエージェントの呼び出しを混同しないでください。
> - **スキル**: `/skill-name <prompt>`、例: `/code-checklist Check this file`
> - **エージェント**: `/agent`（リストから選択）または `copilot --agent <name>`（コマンドライン）
>
> 同じ名前のスキルとエージェントがある場合（例: "code-reviewer"）、`/code-reviewer` と入力すると**スキル**が呼び出され、エージェントではありません。

### スキルが使われたかどうかを確認する方法

Copilot に直接聞くことができます。

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### スキル対エージェント対 MCP

スキルは GitHub Copilot の拡張モデルの一部に過ぎません。エージェントと MCP サーバーとの比較です。

> *MCP についてはまだ心配しないでください。[第 06 章](../06-mcp-servers/README.md)でカバーします。スキルが全体像にどう合うかがわかるようにここに含まれています。*

<img src="../../../images/skills-agents-mcp-comparison.png" alt="エージェント、スキル、MCP サーバーの違いとワークフローへの組み合わせ方を示す比較図" width="800"/>

| 機能 | 何をするか | いつ使うか |
|---------|--------------|-------------|
| **エージェント** | AI の思考方法を変える | 多くのタスクで特化した専門知識が必要なとき |
| **スキル** | タスク固有の指示を提供する | 詳細なステップを持つ特定の繰り返しタスク |
| **MCP** | 外部サービスに接続する | API からリアルタイムデータが必要なとき |

幅広い専門知識にはエージェントを、特定のタスク指示にはスキルを、外部データには MCP を使います。エージェントは会話中に 1 つ以上のスキルを使用できます。たとえば、エージェントにコードチェックを頼むと、自動的に `security-audit` スキルと `code-checklist` スキルの両方を適用することがあります。

> 📚 **さらに学ぶ**: スキルフォーマットとベストプラクティスの完全なリファレンスは公式の [エージェントスキルについて](https://docs.github.com/copilot/concepts/agents/about-agent-skills)ドキュメントをご覧ください。

---

## 手動プロンプトから自動専門知識へ

スキルの作成方法に入る前に、なぜ学ぶ価値があるかを見てみましょう。一貫性の向上がわかれば、「どうやるか」がより理解しやすくなります。

### スキル導入前: 一貫しないレビュー

コードレビューのたびに何かを忘れることがあります。

```bash
copilot

> Review this code for issues
# 汎用レビュー - チーム固有の懸念事項を見落とすかもしれない
```

または毎回長いプロンプトを書きます。

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

時間: 入力に **30 秒以上**。一貫性: **記憶次第**。

### スキル導入後: 自動ベストプラクティス

`code-checklist` スキルをインストールして、自然に聞くだけです。

```bash
copilot

> Check the book collection code for quality issues
```

**舞台裏で何が起こるか**:
1. Copilot がプロンプトに「code quality」と「issues」を検出する
2. スキルの説明を確認し、`code-checklist` スキルが一致することを確認する
3. チームの品質チェックリストを自動的に読み込む
4. リストアップしなくてもすべてのチェックを適用する

<img src="../../../images/skill-auto-discovery-flow.png" alt="スキルの自動トリガー方法 - Copilot がプロンプトを正しいスキルと自動的に一致させる 4 ステップのフロー" width="800"/>

*自然に聞くだけ。Copilot がプロンプトを正しいスキルと一致させ、自動的に適用します。*

**出力**:
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

**違い**: チームの標準が毎回自動的に適用され、入力する必要がありません。

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![スキルトリガーデモ](../../../images/skill-trigger-demo.gif)

*デモの出力は異なります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

## 大規模な一貫性: チーム PR レビュースキル

チームに 10 点の PR チェックリストがあるとします。スキルなしでは、すべての開発者がすべての 10 点を覚える必要があり、誰かが必ず 1 点を忘れます。`pr-review` スキルで、チーム全体が一貫したレビューを受けられます。

```bash
copilot

> Can you review this PR?
```

Copilot は自動的にチームの `pr-review` スキルを読み込み、10 点すべてをチェックします。

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

**力の源**: すべてのチームメンバーが同じ標準を自動的に適用します。新入社員はチェックリストを覚える必要がありません。スキルが処理するからです。

---

# カスタムスキルを作成する

<img src="../../../images/creating-managing-skills.png" alt="スキルの作成と管理を表す輝く LEGO のようなブロックの壁を構築する人間とロボットの手" width="800"/>

SKILL.md ファイルから独自のスキルを構築しましょう。

---

## スキルの場所

スキルは `.github/skills/`（プロジェクト固有）または `~/.copilot/skills/`（ユーザーレベル）に保存されます。

### Copilot がスキルを見つける方法

Copilot はスキルを見つけるためにこれらの場所を自動的にスキャンします。

| 場所 | スコープ |
|----------|-------|
| `.github/skills/` | プロジェクト固有（git を通じてチームと共有） |
| `~/.copilot/skills/` | ユーザー固有（個人スキル） |

### スキル構造

各スキルは `SKILL.md` ファイルを含む独自のフォルダに格納されます。オプションでスクリプト、例、その他のリソースを含めることができます。

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # 必須: スキルの定義と指示
    ├── examples/          # オプション: Copilot が参照できる例ファイル
    │   └── sample.py
    └── scripts/           # オプション: スキルが使えるスクリプト
        └── validate.sh
```

> 💡 **ヒント**: ディレクトリ名は SKILL.md のフロントマターの `name`（小文字とハイフン）と一致させてください。

### SKILL.md フォーマット

スキルは YAML フロントマターを持つシンプルな Markdown フォーマットを使います。

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

**YAML プロパティ:**

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | **はい** | 一意の識別子（小文字、スペースにはハイフン） |
| `description` | **はい** | スキルが何をするか、Copilot がいつ使うべきか |
| `license` | いいえ | このスキルに適用されるライセンス |

> 📖 **公式ドキュメント**: [エージェントスキルについて](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### 最初のスキルを作成する

OWASP Top 10 の脆弱性をチェックするセキュリティ監査スキルを構築してみましょう。

```bash
# スキルディレクトリを作成する
mkdir -p .github/skills/security-audit

# SKILL.md ファイルを作成する
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

# スキルをテストする（スキルはプロンプトに基づいて自動的に読み込まれる）
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot は "security vulnerabilities" がスキルと一致することを検出する
# そして自動的に OWASP チェックリストを適用する
```

**期待される出力**（実際の結果は異なります）:

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

## 良いスキルの説明を書く

SKILL.md の `description` フィールドは重要です！Copilot がスキルを読み込むかどうかを決める方法です。

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **ヒント**: 自然に質問する方法と一致するキーワードを含めてください。「security review」と言う場合、説明に「security review」を含めます。

### スキルとエージェントを組み合わせる

スキルとエージェントは連携します。エージェントが専門知識を提供し、スキルが特定の指示を提供します。

```bash
# コードレビュアーエージェントで始める
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer エージェントの専門知識と
# code-checklist スキルのチェックリストが組み合わさる
```

---

# スキルの管理と共有

インストール済みスキルを見つけ、コミュニティスキルを探し、自分のスキルを共有しましょう。

<img src="../../../images/managing-sharing-skills.png" alt="CLI スキルの発見、使用、作成、共有サイクルを示すスキルの管理と共有" width="800" />

---

## `/skills` コマンドでスキルを管理する

`/skills` コマンドを使ってインストール済みスキルを管理します。

| コマンド | 機能 |
|---------|--------------|
| `/skills list` | インストール済みすべてのスキルを表示する |
| `/skills info <name>` | 特定のスキルの詳細を取得する |
| `/skills add <name>` | スキルを有効にする（リポジトリまたはマーケットプレイスから） |
| `/skills remove <name>` | スキルを無効化またはアンインストールする |
| `/skills reload` | SKILL.md ファイルを編集した後にスキルを再読み込みする |

> 💡 **覚えておいて**: 各プロンプトのためにスキルを「有効化」する必要はありません。インストールされると、スキルはプロンプトが説明と一致するときに**自動的にトリガー**されます。これらのコマンドは利用可能なスキルを管理するためのものであり、使用するためではありません。

### 例: スキルを確認する

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
<summary>実際の動作を見てみましょう！</summary>

![スキルリストデモ](../../../images/list-skills-demo.gif)

*デモの出力は異なります。モデル、ツール、レスポンスはここに表示されているものと異なります。*

</details>

---

### `/skills reload` を使うタイミング

スキルの SKILL.md ファイルを作成または編集した後、Copilot を再起動せずに変更を取得するために `/skills reload` を実行します。

```bash
# スキルファイルを編集する
# 次に Copilot 内で:
> /skills reload
Skills reloaded successfully.
```

> 💡 **知っておくと便利**: スキルは会話履歴を要約するために `/compact` を使った後も有効です。コンパクト後に再読み込みする必要はありません。

---

## コミュニティスキルを見つけて使う

### プラグインを使ってスキルをインストールする

> 💡 **プラグインとは何ですか？** プラグインはスキル、エージェント、MCP サーバー設定をまとめてバンドルできるインストール可能なパッケージです。Copilot CLI の「アプリストア」拡張のようなものと考えてください。

`/plugin` コマンドを使って、これらのパッケージを参照してインストールできます。

```bash
copilot

> /plugin list
# インストール済みプラグインを表示する

> /plugin marketplace
# 利用可能なプラグインを参照する

> /plugin install <plugin-name>
# マーケットプレイスからプラグインをインストールする
```

ローカルプラグインカタログを最新に保つには、以下で更新します。

```bash
copilot plugin marketplace update
```

プラグインは複数の機能をまとめてバンドルできます。単一のプラグインに関連するスキル、エージェント、連携して機能する MCP サーバー設定が含まれることがあります。

### コミュニティスキルリポジトリ

プリメイドスキルはコミュニティリポジトリからも入手できます。

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - スキルのドキュメントと例を含む公式 GitHub Copilot リソース

### GitHub CLI でコミュニティスキルをインストールする

GitHub リポジトリからスキルをインストールする最も簡単な方法は `gh skill install` コマンドを使用することです（[GitHub CLI v2.90.0 以上](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)が必要）:

```bash
# awesome-copilot からスキルを参照してインタラクティブに選択する
gh skill install github/awesome-copilot

# または特定のスキルを直接インストールする
gh skill install github/awesome-copilot code-checklist

# すべてのプロジェクトで個人使用のためにインストールする（ユーザースコープ）
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **インストール前に確認する**: スキルをインストールする前に必ずその `SKILL.md` を読んでください。スキルは Copilot の動作を制御するため、悪意のあるスキルが有害なコマンドを実行させたり、予期しない方法でコードを修正させたりする可能性があります。

---

# 練習

<img src="../../../images/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた居心地の良いデスク" width="800"/>

学んだことを実践して、独自のスキルを構築・テストしましょう。

---

## ▶️ 自分で試してみよう

### さらにスキルを構築する

異なるパターンを示す 2 つのスキルを以下に示します。上記「最初のスキルを作成する」と同じ `mkdir` + `cat` ワークフローに従うか、スキルを適切な場所にコピー&ペーストしてください。さらに例は [.github/skills](../../../.github/skills) にあります。

### pytest テスト生成スキル

コードベース全体で一貫した pytest 構造を確保するスキルです。

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

### チーム PR レビュースキル

チーム全体で一貫した PR レビュー基準を強制するスキルです。

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

### さらに進む

1. **スキル作成チャレンジ**: 3 点チェックリストを行う `quick-review` スキルを作成します:
   - 裸の except 句
   - 欠落している型ヒント
   - 不明確な変数名

   テストするには: 「Do a quick review of books.py」と聞きます

2. **スキル比較**: 詳細なセキュリティレビュープロンプトを手動で書く時間を計ります。次に「Check for security issues in this file」と聞いて、セキュリティ監査スキルが自動的に読み込まれるようにします。スキルはどれだけ時間を節約しましたか？

3. **チームスキルチャレンジ**: チームのコードレビューチェックリストについて考えてください。スキルとしてコード化できますか？スキルが常にチェックすべき 3 つのことを書き留めてください。

**自己確認**: `description` フィールドが重要な理由を説明できれば（Copilot がスキルを読み込むかどうかを決める方法）、スキルを理解しています。

---

## 📝 課題

### メインチャレンジ: ブックサマリースキルを構築する

上記の例は `pytest-gen` と `pr-review` スキルを作成しました。今度は全く異なる種類のスキルを作成する練習をしましょう: データからフォーマットされた出力を生成するスキルです。

1. 現在のスキルをリストアップする: Copilot を実行して `/skills list` を渡します。プロジェクトスキルを見るために `ls .github/skills/` または個人スキルのために `ls ~/.copilot/skills/` を使うこともできます。
2. ブックコレクションのフォーマットされた Markdown サマリーを生成する `book-summary` スキルを `.github/skills/book-summary/SKILL.md` に作成する
3. スキルには以下が必要:
   - 明確な名前と説明（説明は一致のために重要！）
   - 具体的なフォーマットルール（例: タイトル、著者、年、読了状況を含む Markdown テーブル）
   - 出力規約（例: 読了状況に ✅/❌ を使い、年でソートする）
4. スキルをテストする: `@samples/book-app-project/data.json Summarize the books in this collection`
5. `/skills list` を確認してスキルが自動トリガーされることを検証する
6. `/book-summary Summarize the books in this collection` で直接呼び出してみる

**成功基準**: ブックコレクションについて聞いたときに Copilot が自動的に適用する動作する `book-summary` スキルがあります。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**: `.github/skills/book-summary/SKILL.md` を作成します:

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

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**テスト:**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# スキルは説明の一致に基づいて自動トリガーされるはず
```

**トリガーされない場合:** `/skills reload` を試してから再度聞いてください。

</details>

### ボーナスチャレンジ: コミットメッセージスキル

1. 一貫したフォーマットで規約的なコミットメッセージを生成する `commit-message` スキルを作成する
2. 変更をステージしてテストする: 「Generate a commit message for my staged changes」と聞く
3. スキルをドキュメント化して、`copilot-skill` トピックで GitHub に共有する

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| ファイル名を `SKILL.md` 以外にする | スキルが認識されない | ファイルは正確に `SKILL.md` と名付けなければならない |
| 曖昧な `description` フィールド | スキルが自動的に読み込まれない | 説明は主要な発見メカニズム。特定のトリガーワードを使う |
| フロントマターに `name` または `description` がない | スキルが読み込まれない | YAML フロントマターに両方のフィールドを追加する |
| フォルダ場所が間違っている | スキルが見つからない | `.github/skills/skill-name/`（プロジェクト）または `~/.copilot/skills/skill-name/`（個人）を使う |

### トラブルシューティング

**スキルが使われない** - 期待通りに Copilot がスキルを使っていない場合:

1. **説明を確認する**: 聞き方と一致していますか？
   ```markdown
   # 悪い例: 曖昧すぎる
   description: Reviews code

   # 良い例: トリガーワードを含む
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **ファイルの場所を確認する**:
   ```bash
   # プロジェクトスキル
   ls .github/skills/

   # ユーザースキル
   ls ~/.copilot/skills/
   ```

3. **SKILL.md フォーマットを確認する**: フロントマターは必須:
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**スキルが表示されない** - フォルダ構造を確認する:
```
.github/skills/
└── my-skill/           # フォルダ名
    └── SKILL.md        # 正確に SKILL.md でなければならない（大文字小文字を区別）
```

変更を確実に取得するために、スキルを作成または編集した後 `/skills reload` を実行してください。

**スキルが読み込まれるかテストする** - Copilot に直接聞く:
```bash
> What skills do you have available for checking code quality?
# Copilot は見つけた関連スキルを説明する
```

**スキルが実際に機能しているかどうかを確認する方法**

1. **出力フォーマットを確認する**: スキルが出力フォーマット（`[CRITICAL]` タグなど）を指定している場合、レスポンスでそれを探す
2. **直接聞く**: レスポンスを得た後、「Did you use any skills for that?」と聞く
3. **あり/なしで比較する**: `--no-custom-instructions` で同じプロンプトを試して違いを確認する:
   ```bash
   # スキルあり
   copilot --allow-all -p "Review @file.py for security issues"

   # スキルなし（ベースライン比較）
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **特定のチェックを探す**: スキルに特定のチェック（「50 行を超える関数」など）が含まれている場合、それらが出力に表示されるか確認する

</details>

---

# まとめ

## 🔑 重要なポイント

1. **スキルは自動**: プロンプトがスキルの説明と一致するときに Copilot が読み込む
2. **直接呼び出し**: スラッシュコマンドとして `/skill-name` でスキルを直接呼び出すこともできる
3. **SKILL.md フォーマット**: YAML フロントマター（name、description、オプションの license）と Markdown 指示
4. **場所が重要**: プロジェクト/チーム共有には `.github/skills/`、個人使用には `~/.copilot/skills/`
5. **説明が鍵**: 自然に質問する方法と一致する説明を書く

> 📋 **クイックリファレンス**: コマンドとキーボードショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次のステップ

スキルは自動読み込みの指示で Copilot ができることを拡張します。しかし外部サービスへの接続はどうでしょうか？そこで MCP の出番です。

**[第 06 章: MCP サーバー](../06-mcp-servers/README.md)**では以下を学びます。

- MCP（Model Context Protocol）とは何か
- GitHub、ファイルシステム、ドキュメントサービスへの接続
- MCP サーバーの設定
- マルチサーバーワークフロー

---

**[← 第 04 章に戻る](../04-agents-custom-instructions/README.md)** | **[第 06 章に進む →](../06-mcp-servers/README.md)**
