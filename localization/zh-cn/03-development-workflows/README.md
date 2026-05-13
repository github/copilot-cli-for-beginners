![第 03 章：开发工作流](../../../03-development-workflows/images/chapter-header.png)

> **如果 AI 能找出你都不知道该问的 Bug，会是什么体验？**

在本章中，GitHub Copilot CLI 将成为你日常工作的得力助手。你将在每天都依赖的工作流中使用它：测试、重构、调试以及 Git 操作。

## 🎯 学习目标

学完本章后，你将能够：

- 使用 Copilot CLI 进行全面的代码评审
- 安全地重构遗留代码
- 借助 AI 协助调试问题
- 自动生成测试
- 把 Copilot CLI 集成到你的 git 工作流中

> ⏱️ **预计用时**：约 60 分钟（15 分钟阅读 + 45 分钟动手实践）

---

## 🧩 现实类比：木匠的工作流

木匠不仅会使用工具，他们还有针对不同任务的*工作流*：

<img src="../../../03-development-workflows/images/carpenter-workflow-steps.png" alt="工匠工作坊展示三条工作流泳道：制作家具（测量、切割、组装、修饰）、修复损伤（评估、拆除、修补、匹配）、质量检查（检视、测试接缝、检查对齐）" width="800"/>

类似地，开发者针对不同任务也有各自的工作流。GitHub Copilot CLI 能强化每一个工作流，让你在日常编程中更高效、更出色。

---

# 五大工作流

<img src="../../../03-development-workflows/images/five-workflows.png" alt="五个发光的霓虹图标，分别代表代码评审、测试、调试、重构和 git 集成工作流" width="800"/>

下面的每个工作流都是相对独立的。你可以挑选与当前需求最匹配的来学习，也可以全部走一遍。

---

## 自由选择你的冒险路线

本章涵盖开发者常用的五种工作流。**不过你不必一次全部读完！** 每个工作流都被收纳在下方一个可折叠的小节中。挑选你需要的、与当前项目最契合的来学习即可。其他的随时可以回来再探索。

<img src="../../../03-development-workflows/images/five-workflows-swimlane.png" alt="五种开发工作流：代码评审、重构、调试、测试生成、Git 集成，以横向泳道形式展示" width="800"/>

| 我想要…… | 跳转到 |
|---|---|
| 在合并前评审代码 | [工作流 1：代码评审](#workflow-1-code-review) |
| 清理混乱或遗留代码 | [工作流 2：重构](#workflow-2-refactoring) |
| 追踪并修复 Bug | [工作流 3：调试](#workflow-3-debugging) |
| 为代码生成测试 | [工作流 4：测试生成](#workflow-4-test-generation) |
| 写出更好的提交和 PR | [工作流 5：Git 集成](#workflow-5-git-integration) |
| 编码前进行调研 | [小贴士：在规划或编码前先调研](#quick-tip-research-before-you-plan-or-code) |
| 看一个端到端的修 Bug 完整流程 | [全部串起来](#putting-it-all-together-bug-fix-workflow) |

**点击下方任一工作流将其展开**，看看 GitHub Copilot CLI 如何在该领域强化你的开发流程。

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>工作流 1：代码评审</strong> —— 评审文件、使用 /review 智能体、生成严重程度清单</summary>

<img src="../../../03-development-workflows/images/code-review-swimlane-single.png" alt="代码评审工作流：评审、识别问题、排序、生成清单。" width="800"/>

### 基础评审

下例使用 `@` 符号引用一个文件，让 Copilot CLI 直接获取文件内容来进行评审。

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![代码评审演示](../../../03-development-workflows/images/code-review-demo.gif)

*演示输出会有所不同。你的模型、工具和回复会与此处展示的不一样。*

</details>

---

### 输入校验评审

让 Copilot CLI 把评审重点放在某一具体方面（这里是输入校验），只需在提示词中列出你关心的类别。

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### 跨文件项目评审

用 `@` 引用整个目录，让 Copilot CLI 一次性扫描项目里的每一个文件。

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### 交互式代码评审

通过多轮对话深入挖掘。先发起一次宽泛的评审，然后无需重新开始即可追加问题。

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI provides detailed review

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI shows potential issues with empty strings, special characters

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI generates prioritized action items
```

### 评审清单模板

让 Copilot CLI 按特定格式输出（这里是按严重程度分类的 markdown 清单，可以直接粘贴到 issue 中）。

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### 理解 Git 变更（使用 /review 前的重要知识）

在使用 `/review` 命令之前，你需要了解 git 中的两类变更：

| 变更类型 | 含义 | 如何查看 |
|-------------|---------------|------------|
| **已暂存的变更** | 你已用 `git add` 标记到下次提交的文件 | `git diff --staged` |
| **未暂存的变更** | 你已修改但尚未添加的文件 | `git diff` |

```bash
# Quick reference
git status           # Shows both staged and unstaged
git add file.py      # Stage a file for commit
git diff             # Shows unstaged changes
git diff --staged    # Shows staged changes
```

### 使用 /review 命令

`/review` 命令会调用内置的 **code-review 智能体**，它专为分析已暂存和未暂存的变更而优化，输出信噪比很高。使用斜杠命令可以触发一个专门的内置智能体，而不必自己写自由形式的提示词。

```bash
copilot

> /review
# Invokes the code-review agent on staged/unstaged changes
# Provides focused, actionable feedback

> /review Check for security issues in authentication
# Run review with specific focus area
```

> 💡 **小贴士**：code-review 智能体在你有待处理变更时效果最好。先用 `git add` 暂存你的文件，可获得更聚焦的评审。

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>工作流 2：重构</strong> —— 重组代码、分离关注点、改善错误处理</summary>

<img src="../../../03-development-workflows/images/refactoring-swimlane-single.png" alt="重构工作流：评估代码、规划改动、实施、验证行为。" width="800"/>

### 简单重构

> **先试试这个：** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

从直截了当的小改进开始。下面这些都可以在 book app 上试一试。每条提示都把 `@` 文件引用与一条具体的重构指令配对，这样 Copilot CLI 就清楚要改什么。

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **第一次接触重构？** 在挑战复杂转换之前，先从简单的请求入手，例如添加类型提示或改进变量名。

---

<details>
<summary>🎬 看看实际效果！</summary>

![重构演示](../../../03-development-workflows/images/refactor-demo.gif)

*演示输出会有所不同。你的模型、工具和回复会与此处展示的不一样。*

</details>

---

### 分离关注点

在一条提示中用 `@` 引用多个文件，让 Copilot CLI 在重构过程中跨文件移动代码。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### 改善错误处理

提供两个相关文件并描述其中的横切关注点，Copilot CLI 就能给出在两者间一致的修复建议。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### 添加文档

用一个详细的项目符号列表，明确指定每个 docstring 应包含的内容。

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### 用测试保驾护航的安全重构

在多轮对话中串联两个相关请求。先生成测试，然后在测试这张安全网下进行重构。

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Get tests first

> Now refactor the BookCollection class to use a context manager for file operations

# Refactor with confidence - tests verify behavior is preserved
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>工作流 3：调试</strong> —— 追踪 Bug、安全审计、跨文件追溯问题</summary>

<img src="../../../03-development-workflows/images/debugging-swimlane-single.png" alt="调试工作流：理解错误、定位根因、修复、测试。" width="800"/>

### 简单调试

> **先试试这个：** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

从描述哪里出错开始。下面是一些你可以在带 Bug 的 book app 上尝试的常见调试模式。每条提示都把 `@` 文件引用与清晰的症状描述配对，让 Copilot CLI 能定位并诊断 Bug。

```bash
copilot

# Pattern: "Expected X but got Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Pattern: "Unexpected behavior"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Pattern: "Wrong results"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **调试小贴士**：描述*症状*（你看到了什么）和*预期*（应该发生什么）。其余的交给 Copilot CLI。

---

<details>
<summary>🎬 看看实际效果！</summary>

![修复 Bug 演示](../../../03-development-workflows/images/fix-bug-demo.gif)

*演示输出会有所不同。你的模型、工具和回复会与此处展示的不一样。*

</details>

---

### "Bug 侦探" —— AI 找出相关的 Bug

这正是上下文感知调试的闪光点。在带 Bug 的 book app 上尝试这个场景：用 `@` 提供整个文件，只描述用户报告的症状。Copilot CLI 会追踪根因，并可能顺手发现附近其他的 Bug。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI 会做什么**：
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**这一点为什么重要**：Copilot CLI 会读取整个文件，理解你 Bug 报告的上下文，并给出带清晰解释的具体修复方案。

> 💡 **额外收获**：因为 Copilot CLI 分析的是整个文件，它经常会发现*你没问起的*其他问题。例如，在修复作者搜索的同时，Copilot CLI 可能还会注意到 `find_book_by_title` 中的大小写敏感 Bug！

### 真实世界的安全旁白

调试自己的代码固然重要，但理解生产应用中的安全漏洞同样关键。试试这个例子：把 Copilot CLI 指向一个不熟悉的文件，让它做一次安全审计。

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

这个文件展示的是你在生产应用中会遇到的真实安全模式。

> 💡 **你将遇到的常见安全术语：**
> - **SQL 注入**：当用户输入被直接拼入数据库查询时，攻击者可以借此执行恶意命令
> - **参数化查询**：更安全的替代方案 —— 用占位符（`?`）将用户数据与 SQL 命令分离开
> - **竞态条件**：当两个操作同时发生并互相干扰时
> - **XSS（跨站脚本）**：当攻击者把恶意脚本注入到网页中时

---

### 理解错误

把堆栈跟踪直接粘贴到提示词里，再配上 `@` 文件引用，Copilot CLI 就能把错误对应到源代码。

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### 用测试用例调试

描述确切的输入和观察到的输出，给 Copilot CLI 一个具体、可复现的测试用例去推理。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### 跨代码追踪问题

引用多个文件，让 Copilot CLI 跨文件追随数据流，定位问题源头。

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### 理解数据问题

把数据文件和读取它的代码一起提供，Copilot CLI 在建议错误处理改进时就能看到完整画面。

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>工作流 4：测试生成</strong> —— 自动生成全面的测试和边界用例</summary>

<img src="../../../03-development-workflows/images/test-gen-swimlane-single.png" alt="测试生成工作流：分析函数、生成测试、覆盖边界用例、运行。" width="800"/>

> **先试试这个：** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### "测试爆炸" —— 2 个测试 vs 15+ 个测试

手动写测试时，开发者通常只会写 2-3 个基础测试：
- 测试有效输入
- 测试无效输入
- 测试一个边界情况

来看看让 Copilot CLI 生成全面测试时会发生什么！下面这条提示用结构化的项目符号列表搭配 `@` 文件引用，引导 Copilot CLI 给出充分的测试覆盖：

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![测试生成演示](../../../03-development-workflows/images/test-gen-demo.gif)

*演示输出会有所不同。你的模型、工具和回复会与此处展示的不一样。*

</details>

---

**你会得到**：15+ 个全面的测试，包括：

```python
class TestBookCollection:
    # Happy path
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # Find operations
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # Edge cases
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # Data persistence
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # Special characters
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**结果**：30 秒之内，你就拿到了那些原本要花上一个小时去思考和编写的边界用例测试。

---

### 单元测试

针对单个函数，并列出你想覆盖的输入类别，让 Copilot CLI 生成聚焦而周全的单元测试。

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### 运行测试

用大白话向 Copilot CLI 询问你的工具链。它能为你生成正确的 shell 命令。

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI responds:
# cd samples/book-app-project && python -m pytest tests/
# Or for verbose output: python -m pytest tests/ -v
# To see print statements: python -m pytest tests/ -s
```

### 针对特定场景的测试

列出你想覆盖的进阶或棘手场景，让 Copilot CLI 跳出"幸福路径"。

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 在已有文件上追加测试

针对单个函数请求*额外的*测试，让 Copilot CLI 生成对现有测试的补充用例。

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>工作流 5：Git 集成</strong> —— 提交信息、PR 描述、/pr、/delegate 与 /diff</summary>

<img src="../../../03-development-workflows/images/git-integration-swimlane-single.png" alt="Git 集成工作流：暂存变更、生成信息、提交、创建 PR。" width="800"/>

> 💡 **本工作流假设你具备基本的 git 知识**（暂存、提交、分支）。如果你刚接触 git，建议先尝试另外四个工作流。

### 生成提交信息

> **先试试这个：** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` —— 暂存一些变更，然后运行这条命令，看 Copilot CLI 帮你写提交信息。

下例使用 `-p` 行内提示词标志，配合 shell 命令替换，把 `git diff` 的输出直接喂给 Copilot CLI，一次性生成提交信息。`$(...)` 语法会执行括号中的命令，并把它的输出插入到外层命令里。

```bash

# See what changed
git diff --staged

# Generate commit message using [Conventional Commit](../../../GLOSSARY.md#conventional-commit) format
# (structured messages like "feat(books): add search" or "fix(data): handle empty input")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Output: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![Git 集成演示](../../../03-development-workflows/images/git-integration-demo.gif)

*演示输出会有所不同。你的模型、工具和回复会与此处展示的不一样。*

</details>

---

### 解释变更

把 `git show` 的输出通过管道喂给 `-p` 提示词，得到对上一次提交的大白话总结。

```bash
# What did this commit change?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR 描述

把 `git log` 输出与一个结构化提示词模板结合，自动生成完整的 pull request 描述。

```bash
# Generate PR description from branch changes
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### 在交互模式下对当前分支使用 /pr

如果你正在 Copilot CLI 的交互模式下处理一个分支，可以使用 `/pr` 命令操作 pull request。用 `/pr` 来查看 PR、创建新 PR、修复现有 PR，或者让 Copilot CLI 根据分支状态自动判断。

```bash
copilot

> /pr [view|create|fix|auto]
```

### 推送前评审

在 `-p` 提示词中使用 `git diff main..HEAD`，可以对分支的全部变更进行一次推送前的快速复核。

```bash
# Last check before pushing
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### 使用 /delegate 处理后台任务

`/delegate` 命令会把工作交给 GitHub Copilot 云端智能体处理。使用 `/delegate` 斜杠命令（或 `&` 快捷写法），把一个定义清晰的任务交给后台智能体去做。

```bash
copilot

> /delegate Add input validation to the login form

# Or use the & prefix shortcut:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Commits your changes to a new branch
# 2. Opens a draft pull request
# 3. Works in the background on GitHub
# 4. Requests your review when done
```

对于那些定义清晰、希望在你专注于其他事情时被完成的任务，这非常合适。

### 使用 /diff 评审会话变更

`/diff` 命令展示当前会话期间所做的全部变更。在提交之前，用这个斜杠命令以可视化的 diff 形式查看 Copilot CLI 修改过的所有内容。

```bash
copilot

# After making some changes...
> /diff

# Shows a visual diff of all files modified in this session
# Great for reviewing before committing
```

</details>

---

## 小贴士：在规划或编码前先调研

当你需要调研某个库、了解最佳实践或探索一个不熟悉的话题时，可以在写任何代码之前用 `/research` 进行一次深度调研：

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot 会搜索 GitHub 仓库和网页资源，然后返回一份带参考资料的总结。当你即将开始一个新功能、想先做出明智的决策时，这一招特别有用。你可以使用 `/share` 把结果分享出去。

> 💡 **小贴士**：`/research` 与 `/plan` 配合很好，先调研后规划。先调研方案，再规划如何实现。

---

## 全部串起来：修 Bug 工作流

下面是修复一个上报 Bug 的完整工作流：

```bash

# 1. Understand the bug report
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. Debug the issue and fix (continuing in same session)
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. Generate tests for the fix
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# Exit the interactive session

> /exit

# 4. Run git add

# Stage the changes so git diff --staged has something to work with
git add .

# 5. Generate commit message
copilot -p "Generate commit message for: $(git diff --staged)"

# Example Output: "fix(books): support partial author name search"

# 6. Commit changes (optional)

git commit -m "<paste generated message>"
```

### 修 Bug 工作流总结

| 步骤 | 操作 | Copilot 命令 |
|------|--------|-----------------|
| 1 | 理解 Bug | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | 分析并修复 | `> Show me the function and fix the issue` |
| 3 | 生成测试 | `> Generate tests for [specific scenarios]` |
| 4 | 暂存变更 | `git add .` |
| 5 | 生成提交信息 | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | 提交变更 | `git commit -m "<paste generated message>"` |

---

# 实战练习

<img src="../../../images/practice.png" alt="温馨的桌面布置：显示器上展示着代码，台灯、咖啡杯和耳机一应俱全，准备开始动手实践" width="800"/>

现在轮到你应用这些工作流了。

---

## ▶️ 自己来试试

完成这些演示后，再尝试以下变体：

1. **Bug 侦探挑战**：让 Copilot CLI 调试 `samples/book-app-buggy/books_buggy.py` 中的 `mark_as_read` 函数。它有没有解释为什么这个函数会把*所有*书都标为已读，而不是只标记一本？

2. **测试挑战**：为 book app 里的 `add_book` 函数生成测试。数一数 Copilot CLI 包含了多少个你自己想不到的边界用例。

3. **提交信息挑战**：在 book app 的某个文件里做一点小改动，暂存它（`git add .`），然后运行：
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   生成的信息是不是比你随手写的更好？

**自检**：如果你能解释为什么"调试这个 Bug"比"找 Bug"更强大（上下文很重要！），那就说明你理解了开发工作流。

---

## 📝 作业

### 主挑战：重构、测试与发布

动手示例聚焦在 `find_book_by_title` 和代码评审上。现在请把同样的工作流技能应用到 `book-app-project` 中其他函数上：

1. **评审**：让 Copilot CLI 评审 `books.py` 中的 `remove_book()`，关注边界用例和潜在问题：
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **重构**：让 Copilot CLI 改进 `remove_book()`，处理诸如大小写不敏感匹配，并在书未找到时返回有用的反馈
3. **测试**：专门为改进后的 `remove_book()` 函数生成 pytest 测试，覆盖：
   - 移除一本存在的书
   - 大小写不敏感的标题匹配
   - 不存在的书返回合适的反馈
   - 从空集合中移除
4. **评审**：暂存你的变更，运行 `/review` 检查是否还有遗留问题
5. **提交**：生成符合 Conventional Commit 规范的提交信息：
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 提示（点击展开）</summary>

**每一步的示例提示词：**

```bash
copilot

# Step 1: Review
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# Step 2: Refactor
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# Step 3: Test
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# Step 4: Review
> /review

# Step 5: Commit
> Generate a conventional commit message for this refactor
```

**小贴士：** 改进 `remove_book()` 之后，可以试着问 Copilot CLI："这个文件里还有哪些函数可以做类似的改进？"它可能会建议对 `find_book_by_title()` 或 `find_by_author()` 做类似的改动。

</details>

### 加分挑战：用 Copilot CLI 创建一个应用

> 💡 **注意**：这个 GitHub Skills 练习使用的是 **Node.js**，而非 Python。但你将练到的 GitHub Copilot CLI 技巧 —— 创建 issue、生成代码、在终端中协作 —— 适用于任何语言。

该练习展示开发者如何使用 GitHub Copilot CLI 创建 issue、生成代码，并在终端中协作完成一个 Node.js 计算器应用。你将安装 CLI、使用模板和智能体，并实践迭代式、命令行驱动的开发。

##### <img src="../../../images/github-skills-logo.png" width="28" align="center" /> [开始 "Create applications with the Copilot CLI" Skills 练习](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>常见错误与故障排查</strong>（点击展开）</summary>

### 常见错误

| 错误 | 会发生什么 | 怎么解决 |
|---------|--------------|-----|
| 使用模糊的提示词，例如 "Review this code" | 只能得到泛泛的反馈，错过具体问题 | 写具体一点："Review for SQL injection, XSS, and auth issues" |
| 代码评审时没有使用 `/review` | 错过了优化过的 code-review 智能体 | 使用 `/review`，它专为高信噪比输出而调校 |
| 没有上下文就让其 "find bugs" | Copilot CLI 不知道你遇到的是哪个 Bug | 描述症状："Users report X happens when Y" |
| 生成测试时没有指定框架 | 测试可能用错语法或断言库 | 指定："Generate tests using Jest" 或 "using pytest" |

### 故障排查

**评审显得不完整** —— 把要找的内容写得更具体：

```bash
copilot

# Instead of:
> Review @samples/book-app-project/book_app.py

# Try:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**测试与我的框架不匹配** —— 指定框架：

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**重构改变了行为** —— 让 Copilot CLI 保持原有行为：

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# 总结

## 🔑 关键要点

<img src="../../../03-development-workflows/images/specialized-workflows.png" alt="为每项任务定制的专属工作流：代码评审、重构、调试、测试和 Git 集成" width="800"/>

1. **代码评审**在用上具体提示词后会变得全面
2. **重构**在先生成测试时更安全
3. **调试**得益于把错误信息和代码同时展示给 Copilot CLI
4. **测试生成**应包含边界用例和错误场景
5. **Git 集成**自动化了提交信息和 PR 描述

> 📋 **快速参考**：完整的命令与快捷方式列表见 [GitHub Copilot CLI 命令参考](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## ✅ 检查点：你已掌握核心要点

**恭喜你！** 现在你已具备使用 GitHub Copilot CLI 高效工作的全部核心技能：

| 技能 | 章节 | 你现在可以…… |
|-------|---------|----------------|
| 基础命令 | 第 01 章 | 使用交互模式、规划模式、编程式模式（-p）以及斜杠命令 |
| 上下文 | 第 02 章 | 使用 `@` 引用文件、管理会话、理解上下文窗口 |
| 工作流 | 第 03 章 | 评审代码、重构、调试、生成测试、与 git 集成 |

第 04-06 章涵盖更多功能，能让你的能力进一步增强，值得学习。

---

## 🛠️ 打造属于你自己的工作流

使用 GitHub Copilot CLI 没有唯一"正确"的方式。在你形成自己的模式时，这里有几条建议：

> 📚 **官方文档**：[Copilot CLI 最佳实践](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices)，来自 GitHub 推荐的工作流和提示。

- **任何不简单的任务都从 `/plan` 开始**。在执行前先打磨好计划 —— 好计划带来更好结果。
- **保存那些有效的提示词。** 当 Copilot CLI 出错时，记录哪里出了问题。久而久之，这就成了你个人的"行动手册"。
- **大胆尝试。** 有的开发者偏爱长而详细的提示词，有的喜欢短提示加追问。多试几种方式，留意哪种最自然。

> 💡 **预告**：在第 04 和 05 章中，你将学习如何把自己的最佳实践编成 Copilot CLI 自动加载的自定义指令和技能。

---

## ➡️ 下一步

剩下的章节会介绍扩展 Copilot CLI 能力的更多功能：

| 章节 | 涵盖内容 | 何时会想用 |
|---------|----------------|---------------------|
| 第 04 章：智能体 | 创建专门的 AI 角色 | 当你需要领域专家（前端、安全）时 |
| 第 05 章：技能 | 为任务自动加载指令 | 当你经常重复同样的提示词时 |
| 第 06 章：MCP | 接入外部服务 | 当你需要来自 GitHub、数据库的实时数据时 |

**建议**：先把这些核心工作流用上一周，再回头根据具体需求阅读第 04-06 章。

---

## 继续学习更多主题

在 **[第 04 章：智能体与自定义指令](../04-agents-custom-instructions/README.md)** 中，你将学到：

- 使用内置智能体（`/plan`、`/review`）
- 用 `.agent.md` 文件创建专门的智能体（前端专家、安全审计员）
- 多智能体协作模式
- 用于项目规范的自定义指令文件

---

**[← 返回第 02 章](../02-context-conversations/README.md)** | **[继续到第 04 章 →](../04-agents-custom-instructions/README.md)**
