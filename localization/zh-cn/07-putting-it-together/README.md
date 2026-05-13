![第 07 章：融会贯通](../../../07-putting-it-together/images/chapter-header.png)

> **你所学的一切在此汇聚。在一次会话中，从想法走到合并的 PR。**

在本章中，你将把所学的一切整合到完整的工作流中。你将通过多智能体协作来构建功能、设置可在提交前发现安全问题的 pre-commit 钩子、把 Copilot 集成到 CI/CD 流水线中，并且在一个终端会话中从功能想法走到合并的 PR。这正是 GitHub Copilot CLI 真正成为效率倍增器的地方。

> 💡 **提示**：本章展示如何把你学到的所有内容组合起来。**你不一定需要 agents、skills 或 MCP 才能高效工作（虽然它们会非常有用）。** 核心工作流——描述、计划、实现、测试、审阅、发布——仅靠第 00–03 章中的内置功能就能完成。

## 🎯 学习目标

学完本章后，你将能够：

- 在统一的工作流中组合使用 agents、skills 和 MCP（Model Context Protocol，模型上下文协议）
- 用多工具方法构建完整功能
- 用 hooks 设置基础自动化
- 应用专业开发的最佳实践

> ⏱️ **预计时间**：约 75 分钟（阅读 15 分钟 + 动手实践 60 分钟）

---

## 🧩 现实类比：交响乐团

<img src="../../../07-putting-it-together/images/orchestra-analogy.png" alt="交响乐团类比 —— 统一的工作流" width="800"/>

一支交响乐团有许多声部：
- **弦乐**奠定基础（就像你的核心工作流）
- **铜管**带来力量（就像具备专长的 agents）
- **木管**增添色彩（就像扩展能力的 skills）
- **打击乐**保持节奏（就像连接外部系统的 MCP）

单独看，每个声部都很有限。合在一起、由出色的指挥统领，便能演奏出宏大的乐章。

**这就是本章要教你的！**<br>
*就像指挥家带领乐团一样，你也在把 agents、skills 和 MCP 编排成统一的工作流*

让我们先走一遍这样一个场景：在一次会话中修改代码、生成测试、进行审阅并创建 PR。

---

## 一次会话，从想法到合并的 PR

不必在编辑器、终端、测试运行器和 GitHub 网页之间来回切换、每次都丢失上下文，你可以在一个终端会话中把所有工具组合起来。我们将在下面的[集成模式](#the-integration-pattern-for-power-users)小节里拆解这一模式。

```bash
# Start Copilot in interactive mode
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot creates high-level plan...

# SWITCH TO PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# SWITCH TO PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# IMPLEMENT
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TEST
> Generate comprehensive tests for the new feature

# Multiple tests are generated similar to the following:
# - Happy path (3 tests) — filters correctly, excludes read, includes unread
# - Edge cases (4 tests) — empty collection, all read, none read, single book
# - Parametrized (5 cases) — varying read/unread ratios via @pytest.mark.parametrize
# - Integration (4 tests) — interplay with mark_as_read, remove_book, add_book, and data integrity

# Review the changes
> /review

# If review passes, use /pr to operate on the pull request for the current branch
> /pr [view|create|fix|auto]

# Or ask naturally if you want Copilot to draft it from the terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**传统做法**：在编辑器、终端、测试运行器、文档和 GitHub 网页之间来回切换。每次切换都会带来上下文损失和摩擦。

**关键洞察**：你像建筑师一样调度专家，他们处理细节，你掌控全局。

> 💡 **更进一步**：对于这种大型多步骤计划，可以试试 `/fleet`，让 Copilot 并行运行相互独立的子任务。详见[官方文档](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)。

---

# 更多工作流

<img src="../../../07-putting-it-together/images/combined-workflows.png" alt="一群人正在拼一幅由齿轮组成的彩色巨型拼图，象征 agents、skills 和 MCP 如何组合成统一的工作流" width="800"/>

对于已经学完第 04–06 章的高级用户，下面这些工作流展示了 agents、skills 和 MCP 如何成倍提升你的效率。

## 集成模式

下面是组合一切的思维模型：

<img src="../../../07-putting-it-together/images/integration-pattern.png" alt="集成模式 —— 一个 4 阶段的工作流：收集上下文（MCP）、分析与规划（Agents）、执行（Skills + 手动）、收尾（MCP）" width="800"/>

---

## 工作流 1：调查并修复 Bug

借助完整的工具集成进行真实世界的 Bug 修复：

```bash
copilot

# PHASE 1: Understand the bug from GitHub (MCP provides this)
> Get the details of issue #1

# Learn: "find_by_author doesn't work with partial names"

# PHASE 2: Research best practice (deep research with web + GitHub sources)
> /research Best practices for Python case-insensitive string matching

# PHASE 3: Find related code
> @samples/book-app-project/books.py Show me the find_by_author method

# PHASE 4: Get expert analysis
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching

# Agent identifies: Method uses exact equality instead of substring matching

# PHASE 5: Fix with agent guidance
> Implement the fix using lowercase comparison and 'in' operator

# PHASE 6: Generate tests
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# PHASE 7: Commit and PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## 工作流 2：自动化代码审阅（可选）

> 💡 **本节为可选内容。** Pre-commit 钩子对团队很有用，但并不是高效工作的必需品。如果你刚入门，可以跳过。
>
> ⚠️ **性能提醒**：该钩子会对每个暂存文件调用一次 `copilot -p`，每个文件需要数秒。对于大型提交，建议只检查关键文件，或者改为手动用 `/review` 进行审阅。

**git hook**（git 钩子）是 Git 在某些时刻自动运行的脚本，例如在每次提交之前。你可以用它来对代码运行自动化检查。下面演示如何在每次提交时自动让 Copilot 进行审阅：

```bash
# Create a pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    # --allow-all auto-approves file reads/writes so the hook can run unattended.
    # Only use this in automated scripts. In interactive sessions, let Copilot ask for permission.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOS 用户提示**：macOS 默认没有 `timeout` 命令。可以通过 `brew install coreutils` 安装，或者把 `timeout 60` 替换成不带超时保护的简单调用。

> 📚 **官方文档**：[Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) 和 [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) 提供完整的 hooks API。
>
> 💡 **内置替代方案**：Copilot CLI 还自带一套 hooks 系统（`copilot hooks`），可以在 pre-commit 等事件上自动运行。上面那种手写的 git hook 给了你完全的控制权，而内置系统配置更简单。请查阅以上文档来决定哪种方式更适合你的工作流。

这样，每次提交都会进行一次快速的安全审阅：

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Output:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## 工作流 3：上手新代码库

加入新项目时，把上下文、agents 和 MCP 组合起来，可以快速上手：

```bash
# Start Copilot in interactive mode
copilot

# PHASE 1: Get the big picture with context
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# PHASE 2: Understand a specific flow
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# PHASE 3: Get expert analysis with an agent
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# PHASE 4: Find something to work on (MCP provides GitHub access)
> List open issues labeled "good first issue"

# PHASE 5: Start contributing
> Pick the simplest open issue and outline a plan to fix it
```

这一工作流把 `@` 上下文、agents 和 MCP 组合到一次入门会话中，正是本章前面提到的集成模式。

---

# 最佳实践与自动化

那些能让你的工作流更高效的模式与习惯。

---

## 最佳实践

### 1. 先准备上下文，再让其分析

在请求分析之前，先收集好上下文：

```bash
# Good
> Get the details of issue #42
> /agent
# Select python-reviewer
> Analyze this issue

# Less effective
> /agent
# Select python-reviewer
> Fix login bug
# Agent doesn't have issue context
```

### 2. 区分清楚：Agents、Skills 与自定义指令

每种工具都有自己的最佳应用场景：

```bash
# Agents: Specialized personas you explicitly activate
> /agent
# Select python-reviewer
> Review this authentication code for security issues

# Skills: Modular capabilities that auto-activate when your prompt
# matches the skill's description (you must create them first — see Ch 05)
> Generate comprehensive tests for this code
# If you have a testing skill configured, it activates automatically

# Custom instructions (.github/copilot-instructions.md): Always-on
# guidance that applies to every session without switching or triggering
```

> 💡 **关键点**：Agents 和 skills 都既能分析、也能生成代码。真正的区别在于 **它们如何被激活** —— agents 需要显式触发（`/agent`），skills 是自动触发（按提示词匹配），而自定义指令则始终生效。

### 3. 让会话保持聚焦

用 `/rename` 给会话打标签（便于在历史中查找），用 `/exit` 干净地结束：

```bash
# Good: One feature per session
> /rename list-unread-feature
# Work on list unread
> /exit

copilot
> /rename export-csv-feature
# Work on CSV export
> /exit

# Less effective: Everything in one long session
```

### 4. 借助 Copilot 让工作流可复用

不要只把工作流写在 wiki 里，而是直接编码进你的仓库，让 Copilot 能用上：

- **自定义指令**（`.github/copilot-instructions.md`）：始终生效的指南，涵盖编码规范、架构规则以及构建/测试/部署步骤。每次会话都会自动遵循。
- **Prompt 文件**（`.github/prompts/`）：可复用、可参数化的提示词，团队可以共享 —— 例如代码评审、组件生成或 PR 描述的模板。
- **自定义 agents**（`.github/agents/`）：编码特定的角色（例如安全审阅员或文档撰写员），团队任何成员都可以通过 `/agent` 激活它们。
- **自定义 skills**（`.github/skills/`）：把分步骤的工作流说明打包起来，在相关场景自动激活。

> 💡 **收益**：新成员可以免费获得你的工作流 —— 它们已经融入仓库本身，而不是锁在某人的脑子里。

---

## 加分项：生产环境模式

下面这些模式是可选的，但在专业环境中很有价值。

### PR 描述生成器

```bash
# Generate comprehensive PR descriptions
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD 集成

对于已经拥有 CI/CD 流水线的团队，你可以借助 GitHub Actions 在每个 pull request 上自动进行 Copilot 审阅。这包括自动发布审阅评论以及筛选关键问题。

> 📖 **了解更多**：完整的 GitHub Actions 工作流、配置选项与排错技巧，请参见 [CI/CD 集成](../../../appendices/ci-cd-integration.md)。

---

# 实战练习

<img src="../../../images/practice.png" alt="温馨的桌面：显示器上有代码，旁边摆着台灯、咖啡杯和耳机，一切就绪，准备动手实践" width="800"/>

把完整的工作流付诸实践。

---

## ▶️ 自己动手试一试

完成示例后，可以尝试下面这些变体：

1. **端到端挑战**：选一个小功能（例如「列出未读书籍」或「导出为 CSV」）。走一遍完整的工作流：
   - 用 `/plan` 规划
   - 用 agents（python-reviewer、pytest-helper）做设计
   - 实现
   - 生成测试
   - 创建 PR

2. **自动化挑战**：按照「自动化代码审阅」工作流设置 pre-commit 钩子。故意在提交中引入一个文件路径漏洞，看看会不会被拦下来？

3. **你自己的生产工作流**：为一项你常做的任务设计一套属于自己的工作流。把它写成清单。哪些部分可以用 skills、agents 或 hooks 来自动化？

**自检**：当你能向同事解释 agents、skills 和 MCP 是如何协同工作的，以及什么时候该用哪种工具时，本课程就算学完了。

---

## 📝 作业

### 主挑战：端到端功能

动手示例带你走过了构建「列出未读书籍」功能的全过程。现在请用同样的完整工作流练习另一个功能：**按年份范围搜索书籍**：

1. 启动 Copilot 并收集上下文：`@samples/book-app-project/books.py`
2. 用 `/plan Add a "search by year" command that lets users find books published between two years` 进行规划
3. 在 `BookCollection` 中实现一个 `find_by_year_range(start_year, end_year)` 方法
4. 在 `book_app.py` 中添加一个 `handle_search_year()` 函数，提示用户输入起止年份
5. 生成测试：`@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. 用 `/review` 审阅
7. 更新 README：`@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. 生成提交消息

边做边把你的工作流记录下来。

**完成标准**：你已经使用 Copilot CLI 把这个功能从想法一路做到提交，包括规划、实现、测试、文档和审阅。

> 💡 **加分项**：如果你在第 04 章配置过 agents，可以尝试创建并使用自定义 agents。例如用一个 error-handler agent 来审阅实现，用一个 doc-writer agent 来更新 README。

<details>
<summary>💡 提示（点击展开）</summary>

**沿用本章开头[「一次会话，从想法到合并的 PR」](#idea-to-merged-pr-in-one-session)示例中的模式。** 关键步骤包括：

1. 用 `@samples/book-app-project/books.py` 收集上下文
2. 用 `/plan Add a "search by year" command` 进行规划
3. 实现方法和命令处理函数
4. 生成包含边界情况的测试（非法输入、空结果、范围反向）
5. 用 `/review` 审阅
6. 用 `@samples/book-app-project/README.md` 更新 README
7. 用 `-p` 生成提交消息

**需要考虑的边界情况：**
- 如果用户输入「2000」和「1990」（范围反向）该怎么办？
- 如果没有书籍匹配该范围呢？
- 如果用户输入了非数字内容呢？

**关键是要练习完整的工作流**：想法 → 上下文 → 规划 → 实现 → 测试 → 文档 → 提交。

</details>

---

<details>
<summary>🔧 <strong>常见错误</strong>（点击展开）</summary>

| 错误 | 会发生什么 | 修正方式 |
|---------|--------------|-----|
| 直接跳到实现阶段 | 错过设计层面的问题，后续修复成本高 | 先用 `/plan` 把思路理清楚 |
| 多个工具能配合时只用了一个 | 速度更慢、结果不够全面 | 组合使用：用 Agent 做分析 → 用 Skill 执行 → 用 MCP 集成 |
| 提交前没有审阅 | 安全问题或 Bug 被漏过 | 一定要运行 `/review`，或使用 [pre-commit 钩子](#workflow-2-code-review-automation-optional) |
| 忘记把工作流分享给团队 | 每个人都在重新发明轮子 | 把模式沉淀到共享的 agents、skills 和 instructions 中 |

</details>

---

# 总结

## 🔑 核心要点

1. **集成 > 隔离**：组合使用工具，效果最大化
2. **上下文优先**：在分析前总是先准备好必要的上下文
3. **Agents 用于分析，Skills 用于执行**：用对的工具做对的事
4. **把重复工作自动化**：Hooks 和脚本能让你的效率翻倍
5. **沉淀工作流文档**：可分享的模式让整个团队受益

> 📋 **快速参考**：完整命令和快捷键列表请参见 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## 🎓 课程完结！

恭喜你！你学到了：

| 章节 | 学到了什么 |
|---------|-------------------|
| 00 | Copilot CLI 安装与快速开始 |
| 01 | 三种交互模式 |
| 02 | 用 @ 语法管理上下文 |
| 03 | 开发工作流 |
| 04 | 专属 agents |
| 05 | 可扩展的 skills |
| 06 | 通过 MCP 连接外部系统 |
| 07 | 统一的生产工作流 |

现在你已经可以把 GitHub Copilot CLI 真正用作开发流程中的效率倍增器了。

## ➡️ 下一步

学习不会就此止步：

1. **每天练习**：用 Copilot CLI 处理真实工作
2. **打造定制工具**：为你的具体需求创建 agents 和 skills
3. **分享知识**：帮助团队采用这些工作流
4. **保持更新**：关注 GitHub Copilot 的新特性

### 资源

- [GitHub Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Community Skills](https://github.com/topics/copilot-skill)

---

**干得漂亮！现在去打造一些精彩的东西吧。**

**[← 返回第 06 章](../06-mcp-servers/README.md)** | **[返回课程主页 →](../README.md)**
