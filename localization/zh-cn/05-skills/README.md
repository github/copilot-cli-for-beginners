![第 05 章：技能系统](../../../05-skills/images/chapter-header.png)

> **如果 Copilot 能自动应用你团队的最佳实践，而你不必每次都向它解释，那会怎样？**

在本章中，你将学习 Agent Skills（智能体技能）：当与你的任务相关时，Copilot 会自动加载这些指令文件夹。智能体改变的是 Copilot 的*思考方式*，而技能则教会 Copilot *完成任务的具体方法*。你将创建一个安全审计技能，每当你询问安全相关的问题时 Copilot 都会应用它；构建团队标准的代码审查准则，确保代码质量的一致性；并了解技能如何在 Copilot CLI、VS Code 以及 GitHub Copilot 云端智能体之间协同工作。


## 🎯 学习目标

学完本章后，你将能够：

- 理解 Agent Skills 的工作原理以及何时使用它们
- 通过 SKILL.md 文件创建自定义技能
- 使用来自共享仓库的社区技能
- 知道何时使用技能、智能体或者 MCP

> ⏱️ **预计用时**：约 55 分钟（20 分钟阅读 + 35 分钟动手实践）

---

## 🧩 现实类比：电动工具

通用电钻很有用，但搭配专用配件后会变得更强大。
<img src="../../../05-skills/images/power-tools-analogy.png" alt="电动工具——技能扩展 Copilot 的能力" width="800"/>


技能的工作方式与此类似。就像为不同的工作更换钻头一样，你可以为 Copilot 添加针对不同任务的技能：

| 技能配件 | 用途 |
|------------|---------|
| `commit` | 生成风格一致的提交信息 |
| `security-audit` | 检查 OWASP 漏洞 |
| `generate-tests` | 创建全面的 pytest 测试 |
| `code-checklist` | 应用团队代码质量标准 |



*技能就像专用配件，扩展了 Copilot 能做的事情*

---

# 技能的工作原理

<img src="../../../05-skills/images/how-skills-work.png" alt="星空背景上由光线串连起来的发光 RPG 风格技能图标，象征 Copilot 技能" width="800"/>

了解技能是什么、为什么重要，以及它们与智能体和 MCP 有何不同。

---

## *第一次接触技能？* 从这里开始！

1. **看看已经可用的技能：**
   ```bash
   copilot
   > /skills list
   ```
   这会列出 Copilot 能找到的所有技能，包括 CLI 自带的**内置技能**，以及来自项目和个人文件夹的技能。

   > 💡 **内置技能**：Copilot CLI 开箱即用就附带了一些技能。例如，`customizing-copilot-cloud-agents-environment` 技能就提供了一份关于如何自定义 Copilot 云端智能体环境的指南。你不需要创建或安装任何东西就能使用这些技能。运行 `/skills list` 看看都有哪些。

2. **查看一个真实的技能文件：** 看看我们提供的 [code-checklist SKILL.md](../../../.github/skills/code-checklist/SKILL.md)，了解一下它的格式。其实就是 YAML frontmatter 加上 Markdown 指令而已。

3. **理解核心概念：** 技能是任务专用的指令，当你的提示与某个技能的描述相匹配时，Copilot 会*自动*加载它。你不需要主动激活它们，只需自然地提问即可。


## 理解技能

Agent Skills 是包含指令、脚本和资源的文件夹，**当与你的任务相关时**，Copilot 会自动加载它们。Copilot 会读取你的提示，检查是否有匹配的技能，然后自动应用相关指令。

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

> 💡 **关键点**：技能会根据你的提示与技能描述的匹配情况**自动触发**。你只需自然地提问，Copilot 就会在幕后应用相关技能。你也可以直接调用技能，下面就会介绍这一点。

> 🧰 **开箱即用的模板**：查看 [.github/skills](../../../.github/skills/) 文件夹，里面有可以直接复制粘贴试用的简单技能。

### 直接通过斜杠命令调用

虽然自动触发是技能的主要工作方式，但你也可以使用技能名作为斜杠命令来**直接调用**：

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

这样可以让你显式控制，确保使用特定的技能。

#### 在一条消息中组合调用多个技能

你可以**在一条消息中调用多个技能**，并且技能斜杠命令可以出现在提示的任何位置——不一定要放在开头。当你想一次性完成两种不同的检查时，这非常方便：

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot 会在同一次回复中应用每一个被点名的技能，让你不必发送多条独立的消息。

> 💡 **小贴士**：把技能斜杠命令放在你句子中最自然的位置即可。可以放在消息的开头、中间或结尾。

> 📝 **技能调用 vs 智能体调用**：不要把技能调用和智能体调用搞混了：
> - **技能**：`/skill-name <prompt>`，例如 `/code-checklist Check this file`
> - **智能体**：`/agent`（从列表中选择）或 `copilot --agent <name>`（命令行）
>
> 如果你同时拥有同名的技能和智能体（例如都叫 "code-reviewer"），输入 `/code-reviewer` 会调用**技能**，而不是智能体。

### 我怎么知道某个技能被使用了？

你可以直接询问 Copilot：

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### 技能 vs 智能体 vs MCP

技能只是 GitHub Copilot 可扩展性体系中的一环。下面对比一下它与智能体和 MCP 服务器的差别。

> *现在还不用担心 MCP，我们会在[第 06 章](../06-mcp-servers/)中介绍它。这里提一下只是为了让你看清技能在整体图景中的位置。*

<img src="../../../05-skills/images/skills-agents-mcp-comparison.png" alt="对比图，展示智能体、技能与 MCP 服务器之间的差异，以及它们如何组合到你的工作流中" width="800"/>

| 特性 | 它做什么 | 何时使用 |
|---------|--------------|-------------|
| **智能体（Agents）** | 改变 AI 的思考方式 | 在多种任务中需要专门的专家能力时 |
| **技能（Skills）** | 提供任务专用的指令 | 用于具体、可重复的任务，并附带详细步骤时 |
| **MCP** | 连接外部服务 | 需要从 API 获取实时数据时 |

智能体用于广泛的专业知识，技能用于特定任务的指令，而 MCP 用于外部数据。一个智能体可以在一次对话中使用一个或多个技能。例如，当你让一个智能体检查代码时，它可能会同时自动应用 `security-audit` 技能和 `code-checklist` 技能。

> 📚 **进一步学习**：完整的技能格式和最佳实践请参考官方文档 [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)。

---

## 从手动提示到自动专家能力

在深入讲解如何创建技能之前，先看看*为什么*它们值得学习。一旦你看到一致性方面的提升，"如何做" 部分就会更容易理解。

### 没有技能时：审查不一致

每次代码审查，你都可能漏掉某些事情：

```bash
copilot

> Review this code for issues
# Generic review - might miss your team's specific concerns
```

或者每次都写一段冗长的提示：

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

耗时：**30 秒以上**才能打完。一致性：**取决于记性**。

### 有了技能后：自动应用最佳实践

只要安装了 `code-checklist` 技能，自然地提问即可：

```bash
copilot

> Check the book collection code for quality issues
```

**幕后发生的事情**：
1. Copilot 在你的提示里看到 "code quality" 和 "issues"
2. 检查技能描述，发现你的 `code-checklist` 技能匹配
3. 自动加载你团队的质量检查清单
4. 应用所有检查项，无需你逐项罗列

<img src="../../../05-skills/images/skill-auto-discovery-flow.png" alt="技能如何自动触发——展示 Copilot 如何将你的提示自动匹配到正确技能的 4 步流程" width="800"/>

*只要自然提问，Copilot 就会把你的提示匹配到合适的技能并自动应用。*

**输出**：
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

**差别在于**：你团队的标准每次都被自动应用，无需你再敲出来。

---

<details>
<summary>🎬 看看实际效果！</summary>

![技能触发演示](../../../05-skills/images/skill-trigger-demo.gif)

*演示输出会有所不同。你的模型、工具和回复都会与此处展示的内容有所差别。*

</details>

---

## 规模化的一致性：团队 PR 审查技能

设想你的团队有一份 10 项的 PR 检查清单。没有技能时，每位开发者都得记住全部 10 项，总有人会漏掉其中一项。有了 `pr-review` 技能后，整个团队就能获得一致的审查：

```bash
copilot

> Can you review this PR?
```

Copilot 会自动加载团队的 `pr-review` 技能，并检查所有 10 项：

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

**威力所在**：每个团队成员都自动应用相同的标准。新人不必背下检查清单，因为技能已经替他们做到了。

---

# 创建自定义技能

<img src="../../../05-skills/images/creating-managing-skills.png" alt="人类与机械手共同搭建一面发光的乐高积木墙，象征技能的创建与管理" width="800"/>

通过 SKILL.md 文件构建你自己的技能。

---

## 技能存放位置

技能存放在 `.github/skills/`（项目级）或 `~/.copilot/skills/`（用户级）。

### Copilot 如何查找技能

Copilot 会自动扫描以下位置：

| 位置 | 范围 |
|----------|-------|
| `.github/skills/` | 项目专属（通过 git 与团队共享） |
| `~/.copilot/skills/` | 用户专属（你的个人技能） |

### 技能结构

每个技能都放在自己的文件夹里，并包含一个 `SKILL.md` 文件。你也可以选择性地加入脚本、示例或其他资源：

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Required: Skill definition and instructions
    ├── examples/          # Optional: Example files Copilot can reference
    │   └── sample.py
    └── scripts/           # Optional: Scripts the skill can use
        └── validate.sh
```

> 💡 **小贴士**：目录名应当与 SKILL.md frontmatter 中的 `name` 一致（小写，使用连字符）。

### SKILL.md 格式

技能使用带 YAML frontmatter 的简单 Markdown 格式：

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

**YAML 属性：**

| 属性 | 是否必填 | 描述 |
|----------|----------|-------------|
| `name` | **是** | 唯一标识符（小写，空格用连字符代替） |
| `description` | **是** | 描述技能的功能以及 Copilot 何时应使用它 |
| `license` | 否 | 适用于该技能的许可证 |

> 📖 **官方文档**：[About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### 创建你的第一个技能

让我们构建一个安全审计技能，用来检查 OWASP Top 10 漏洞：

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

**预期输出**（你的结果会有所不同）：

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

## 写好技能描述

SKILL.md 中的 `description` 字段非常关键！它决定了 Copilot 是否会加载你的技能：

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **小贴士**：包含与你自然提问方式一致的关键词。如果你会说 "security review"，那就在描述里写上 "security review"。

### 把技能与智能体结合使用

技能与智能体是相辅相成的。智能体提供专家能力，技能提供具体指令：

```bash
# Start with a code-reviewer agent
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer agent's expertise combines
# with your code-checklist skill's checklist
```

---

# 管理与共享技能

发现已安装的技能、寻找社区技能，以及分享你自己的技能。

<img src="../../../05-skills/images/managing-sharing-skills.png" alt="管理和共享技能——展示 CLI 技能从发现、使用、创建到分享的循环" width="800" />

---

## 使用 `/skills` 命令管理技能

使用 `/skills` 命令来管理你已安装的技能：

| 命令 | 它做什么 |
|---------|--------------|
| `/skills list` | 显示所有已安装的技能 |
| `/skills info <name>` | 获取某个技能的详细信息 |
| `/skills add <name>` | 启用一个技能（来自仓库或市场） |
| `/skills remove <name>` | 禁用或卸载一个技能 |
| `/skills reload` | 在编辑 SKILL.md 文件后重新加载技能 |

> 💡 **请记住**：你不需要为每条提示去 "激活" 技能。一旦安装好，当你的提示与技能描述匹配时，技能就会**自动触发**。这些命令是用来管理哪些技能可用的，而不是用来使用它们的。

### 示例：查看你的技能

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
<summary>看看实际效果！</summary>

![列出技能演示](../../../05-skills/images/list-skills-demo.gif)

*演示输出会有所不同。你的模型、工具和回复都会与此处展示的内容有所差别。*

</details>

---

### 何时使用 `/skills reload`

在创建或编辑技能的 SKILL.md 文件后，运行 `/skills reload` 即可在不重启 Copilot 的情况下让改动生效：

```bash
# Edit your skill file
# Then in Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **小知识**：即使你使用 `/compact` 总结过对话历史，技能仍然有效。压缩后无需重新加载。

---

## 查找并使用社区技能

### 使用插件安装技能

> 💡 **什么是插件？** 插件是可安装的包，能够把技能、智能体和 MCP 服务器配置打包在一起。可以把它们看作 Copilot CLI 的 "应用商店" 扩展。

`/plugin` 命令可以让你浏览并安装这些包：

```bash
copilot

> /plugin list
# Shows installed plugins

> /plugin marketplace
# Browse available plugins

> /plugin install <plugin-name>
# Install a plugin from the marketplace
```

要保持本地插件目录的最新状态，可以用以下命令刷新：

```bash
copilot plugin marketplace update
```

插件可以打包多种能力。一个插件可能包含多个相关的技能、智能体和 MCP 服务器配置，它们协同工作。

### 社区技能仓库

预制好的技能也可以从社区仓库中获取：

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** —— GitHub 官方的 Copilot 资源，包含技能文档与示例

### 使用 GitHub CLI 安装社区技能

从 GitHub 仓库安装技能最简单的方式是使用 `gh skill install` 命令（需要 [GitHub CLI v2.90.0+](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)）：

```bash
# Browse and interactively select a skill from awesome-copilot
gh skill install github/awesome-copilot

# Or install a specific skill directly
gh skill install github/awesome-copilot code-checklist

# Install for personal use across all projects (user scope)
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **安装前务必审阅**：在安装某个技能之前，请先阅读它的 `SKILL.md`。技能控制着 Copilot 的行为，恶意的技能可能指示它执行有害命令或以意想不到的方式修改代码。

---

# 实践

<img src="../../../images/practice.png" alt="温馨的桌面布置：显示器上显示代码，台灯、咖啡杯和耳机已就绪，准备开始动手实践" width="800"/>

应用你所学到的知识，构建并测试你自己的技能。

---

## ▶️ 自己动手试试

### 构建更多技能

下面是另外两个展示不同模式的技能。按照上面 "创建你的第一个技能" 中相同的 `mkdir` + `cat` 流程操作，或者把这些技能复制粘贴到正确的位置即可。更多示例可在 [.github/skills](../../../.github/skills) 中找到。

### pytest 测试生成技能

一个确保整个代码库 pytest 结构一致的技能：

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

### 团队 PR 审查技能

一个在团队中强制执行一致 PR 审查标准的技能：

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

### 更进一步

1. **技能创建挑战**：创建一个 `quick-review` 技能，做 3 项检查：
   - 裸的 except 子句
   - 缺少类型提示
   - 变量名含义不清

   通过这样提问来测试它："Do a quick review of books.py"

2. **技能对比**：给自己计时，手动写一段详细的安全审查提示。然后只问 "Check for security issues in this file"，让你的 security-audit 技能自动加载。技能为你节省了多少时间？

3. **团队技能挑战**：想想你团队的代码审查清单。能否将其编码为一个技能？写下该技能应当始终检查的 3 项内容。

**自我检查**：当你能解释为什么 `description` 字段很重要时（它决定了 Copilot 是否会加载你的技能），就说明你理解技能了。

---

## 📝 作业

### 主挑战：构建一个图书摘要技能

上面的示例创建了 `pytest-gen` 和 `pr-review` 技能。现在练习创建一种完全不同类型的技能：根据数据生成格式化输出。

1. 列出当前的技能：运行 Copilot 并向它发送 `/skills list`。你也可以使用 `ls .github/skills/` 查看项目级技能，或 `ls ~/.copilot/skills/` 查看个人技能。
2. 在 `.github/skills/book-summary/SKILL.md` 创建一个 `book-summary` 技能，用于生成图书集合的格式化 Markdown 摘要
3. 你的技能应当具备：
   - 清晰的名称和描述（描述对于匹配至关重要！）
   - 具体的格式化规则（例如：包含书名、作者、年份、阅读状态的 Markdown 表格）
   - 输出约定（例如：用 ✅/❌ 表示阅读状态，按年份排序）
4. 测试该技能：`@samples/book-app-project/data.json Summarize the books in this collection`
5. 通过 `/skills list` 验证技能是否会自动触发
6. 尝试用 `/book-summary Summarize the books in this collection` 直接调用它

**成功标准**：你拥有一个可用的 `book-summary` 技能，当你询问图书集合时 Copilot 会自动应用它。

<details>
<summary>💡 提示（点击展开）</summary>

**起步模板**：创建 `.github/skills/book-summary/SKILL.md`：

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

**测试它：**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# The skill should auto-trigger based on the description match
```

**如果没有触发：** 试试 `/skills reload`，然后再问一次。

</details>

### 加分挑战：提交信息技能

1. 创建一个 `commit-message` 技能，用于以一致的格式生成 conventional commit 提交信息
2. 通过暂存一个改动并提问 "Generate a commit message for my staged changes" 来测试它
3. 为你的技能编写文档，并使用 `copilot-skill` 主题在 GitHub 上分享

---

<details>
<summary>🔧 <strong>常见错误与故障排查</strong>（点击展开）</summary>

### 常见错误

| 错误 | 会发生什么 | 修复方法 |
|---------|--------------|-----|
| 把文件命名为非 `SKILL.md` 的名称 | 技能不会被识别 | 文件必须严格命名为 `SKILL.md` |
| `description` 字段含糊 | 技能永远不会被自动加载 | 描述是首要的发现机制。使用具体的触发词 |
| frontmatter 缺少 `name` 或 `description` | 技能加载失败 | 在 YAML frontmatter 中同时添加这两个字段 |
| 文件夹位置错误 | 找不到技能 | 使用 `.github/skills/skill-name/`（项目级）或 `~/.copilot/skills/skill-name/`（个人级） |

### 故障排查

**技能没被使用** —— 如果 Copilot 没有按预期使用你的技能：

1. **检查描述**：它是否与你的提问方式相匹配？
   ```markdown
   # Bad: Too vague
   description: Reviews code

   # Good: Includes trigger words
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **核实文件位置**：
   ```bash
   # Project skills
   ls .github/skills/

   # User skills
   ls ~/.copilot/skills/
   ```

3. **检查 SKILL.md 格式**：frontmatter 是必需的：
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**技能没有出现** —— 检查文件夹结构：
```
.github/skills/
└── my-skill/           # Folder name
    └── SKILL.md        # Must be exactly SKILL.md (case-sensitive)
```

在创建或编辑技能后运行 `/skills reload`，确保改动被识别。

**测试技能是否加载** —— 直接询问 Copilot：
```bash
> What skills do you have available for checking code quality?
# Copilot will describe relevant skills it found
```

**我怎么知道我的技能确实在工作？**

1. **检查输出格式**：如果你的技能指定了输出格式（比如 `[CRITICAL]` 标签），看看回复中是否有这种标签
2. **直接询问**：得到回复后问一句 "Did you use any skills for that?"
3. **对比有/无技能**：用同一条提示加上 `--no-custom-instructions` 看看差异：
   ```bash
   # With skills
   copilot --allow-all -p "Review @file.py for security issues"

   # Without skills (baseline comparison)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **核对具体检查项**：如果你的技能包含具体检查项（例如 "functions over 50 lines"），看看这些是否出现在输出中

</details>

---

# 总结

## 🔑 核心要点

1. **技能是自动的**：当你的提示与技能描述匹配时，Copilot 会自动加载它们
2. **直接调用**：你也可以使用 `/skill-name` 作为斜杠命令直接调用技能
3. **SKILL.md 格式**：YAML frontmatter（name、description，license 可选）加上 Markdown 指令
4. **位置很重要**：`.github/skills/` 用于项目/团队共享，`~/.copilot/skills/` 用于个人使用
5. **描述是关键**：写出与你自然提问方式相匹配的描述

> 📋 **快速参考**：完整的命令和快捷键列表请参考 [GitHub Copilot CLI 命令参考](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## ➡️ 下一步

技能通过自动加载的指令扩展了 Copilot 能做的事情。但要连接外部服务怎么办？这就是 MCP 的用武之地。

在**[第 06 章：MCP 服务器](../06-mcp-servers/README.md)**中，你将学习：

- 什么是 MCP（Model Context Protocol，模型上下文协议）
- 连接到 GitHub、文件系统和文档服务
- 配置 MCP 服务器
- 多服务器工作流

---

**[← 返回第 04 章](../04-agents-custom-instructions/README.md)** | **[继续到第 06 章 →](../06-mcp-servers/README.md)**
