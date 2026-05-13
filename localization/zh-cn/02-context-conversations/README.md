![第 02 章：上下文与对话](../../../02-context-conversations/images/chapter-header.png)

> **如果 AI 能看到你的整个代码库，而不仅仅是一次只看一个文件，那会怎样？**

在本章中，你将解锁 GitHub Copilot CLI 的真正威力：上下文。你将学习使用 `@` 语法来引用文件和目录，让 Copilot CLI 深入理解你的代码库。你会发现如何在多次会话之间保持对话连续，几天之后还能从离开的地方精确地继续工作，并看到跨文件分析如何捕捉到单文件审查会完全错过的 bug。

## 🎯 学习目标

完成本章后，你将能够：

- 使用 `@` 语法引用文件、目录和图片
- 使用 `--resume` 和 `--continue` 恢复之前的会话
- 理解[上下文窗口](../../../GLOSSARY.md#context-window)的工作原理
- 编写有效的多轮对话
- 为多项目工作流管理目录权限

> ⏱️ **预计耗时**：约 50 分钟（20 分钟阅读 + 30 分钟动手实践）

---

## 🧩 现实类比：与同事一起工作

<img src="../../../02-context-conversations/images/colleague-context-analogy.png" alt="上下文带来差异 —— 没有上下文 vs 有上下文" width="800"/>

*就像你的同事一样，Copilot CLI 不会读心。提供更多信息能帮助人类和 Copilot 给出更有针对性的支持！*

想象你向同事描述一个 bug：

> **没有上下文**：“这个图书应用不工作。”

> **有上下文**：“看一下 `books.py`，特别是 `find_book_by_title` 函数。它没有做不区分大小写的匹配。”

要给 Copilot CLI 提供上下文，请使用 *`@` 语法* 把 Copilot CLI 指向具体的文件。

---

# 必备：基础上下文

<img src="../../../02-context-conversations/images/essential-basic-context.png" alt="发光的代码块由光带连接，象征着上下文如何在 Copilot CLI 对话中流动" width="800"/>

本节涵盖你高效使用上下文所需的全部内容。请先掌握这些基础。

---

## @ 语法

`@` 符号用于在你的提示词中引用文件和目录。这就是你告诉 Copilot CLI “看一下这个文件”的方式。

> 💡 **提示**：本课程的所有示例都使用本仓库中的 `samples/` 文件夹，所以你可以直接试用每一条命令。

### 立刻试一试（无需任何准备）

你可以使用电脑上的任意文件来尝试：

```bash
copilot

# 指向你拥有的任意文件
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **手边没有项目？** 快速创建一个测试文件：
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基础 @ 模式

| 模式 | 作用 | 用法示例 |
|---------|--------------|-------------|
| `@file.py` | 引用单个文件 | `Review @samples/book-app-project/books.py` |
| `@folder/` | 引用某个目录下的所有文件 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 引用多个文件 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 引用单个文件

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![文件上下文演示](../../../02-context-conversations/images/file-context-demo.gif)

*演示输出会有所不同。你的模型、工具和响应会与此处显示的不一样。*

</details>

---

### 引用多个文件

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### 引用整个目录

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## 跨文件智能

这就是上下文成为超能力的地方。单文件分析很有用，跨文件分析则具有变革性。

<img src="../../../02-context-conversations/images/cross-file-intelligence.png" alt="跨文件智能 —— 比较单文件分析与跨文件分析，展示一起分析多个文件如何揭示在孤立查看时不可见的 bug、数据流和模式" width="800"/>

### 演示：找出跨多个文件的 bug

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **进阶选项**：如果你想做以安全为重点的跨文件分析，可以试试 Python 安全示例：
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 看看实际效果！</summary>

![多文件演示](../../../02-context-conversations/images/multi-file-demo.gif)

*演示输出会有所不同。你的模型、工具和响应会与此处显示的不一样。*

</details>

---

**Copilot CLI 会发现什么**：

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

**为什么这很重要**：单文件审查会错失全局。只有跨文件分析才能揭示：
- 应当合并的**重复代码**
- 展示组件如何交互的**数据流模式**
- 影响可维护性的**架构问题**

---

### 演示：60 秒理解一个代码库

<img src="../../../02-context-conversations/images/codebase-understanding.png" alt="分屏对比展示手动代码审查耗时 1 小时 vs AI 辅助分析仅耗时 10 秒" width="800" />

刚接触一个项目？使用 Copilot CLI 快速了解它。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**你会得到**：
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**结果**：原本要花一个小时阅读代码的工作，被压缩到 10 秒钟。你能立刻知道该把注意力放在哪里。

---

## 实用示例

### 示例 1：带上下文的代码审查

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI 现在拥有完整的文件内容，可以给出具体反馈：
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# 现在审查 book_app.py，但仍然了解 books.py 的上下文
```

### 示例 2：理解一个代码库

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI 阅读 books.py 并理解 BookCollection 类

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI 扫描该目录并进行汇总

> How does the app save and load books?

# Copilot CLI 可以基于已经读过的代码进行追踪
```

<details>
<summary>🎬 看看多轮对话的实际效果！</summary>

![多轮对话演示](../../../02-context-conversations/images/multi-turn-demo.gif)

*演示输出会有所不同。你的模型、工具和响应会与此处显示的不一样。*

</details>

### 示例 3：多文件重构

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI 同时看到这两个文件，可以建议如何合并重复代码
```

---

## 会话管理

会话会在你工作时自动保存。你可以恢复之前的会话，从离开的地方继续。

### 会话自动保存

每一次对话都会被自动保存。只要正常退出即可：

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... 进行一些工作 ...]

> /exit
```

### 恢复最近一次的会话

```bash
# 从离开的地方继续
copilot --continue
```

### 恢复指定的会话

```bash
# 在会话列表中以交互方式选择
copilot --resume

# 或按 ID 恢复指定会话
copilot --resume=abc123

# 或按你给会话起的名字来恢复
copilot --resume="my book app review"
```

> 💡 **怎么找到会话 ID？** 你不必记住它们。运行 `copilot --resume` 而不带 ID 时，会显示一个交互式列表，列出你之前的会话、它们的名字、ID 以及最近活跃时间。挑一个就行了。
>
> **多个终端怎么办？** 每个终端窗口都是独立的会话，拥有自己的上下文。如果你在三个终端里打开了 Copilot CLI，那就是三个独立的会话。从任意一个终端运行 `--resume` 都可以浏览全部会话。`--continue` 标志会先抓取当前工作目录下的会话；如果当前目录没有，则选取最近活跃的那个会话。
>
> **能在不重启的情况下切换会话吗？** 可以。在已激活的会话内使用 `/resume` 斜杠命令：
> ```
> > /resume
> # 显示可切换到的会话列表
> ```

### 整理你的会话

给会话起一个有意义的名字，方便你之后查找。你可以在启动时给会话命名，也可以在会话内随时重命名：

```bash
# 启动时直接给会话命名
copilot --name book-app-review

# 或者在会话内部重命名当前会话
copilot

> /rename book-app-review
# 会话已重命名，便于识别
```

会话被命名后，你就可以直接按名字恢复，而无需在列表中翻找：

```bash
copilot --resume=book-app-review
```

要清理你不再需要的会话，请在会话内使用 `/session delete`：

```bash
copilot

> /session delete            # 删除当前会话
> /session delete abc123     # 按 ID 删除指定会话
> /session delete-all        # 删除所有会话（请谨慎使用！）
```

### 检查并管理上下文

随着你不断添加文件和对话，Copilot CLI 的[上下文窗口](../../../GLOSSARY.md#context-window)会逐渐被占满。有几个命令可以帮助你保持掌控：

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 放弃当前会话（不保存历史）并开始一个全新的对话

> /new
# 结束当前会话（保存到历史中以便搜索/恢复）并开始一个全新的对话

> /rewind
# 打开时间线选择器，让你回滚到对话中的更早某个节点
```

> 💡 **何时使用 `/clear` 或 `/new`**：如果你一直在审查 books.py，想切换到讨论 utils.py，请先运行 /new（如果不需要保留会话历史就用 /clear）。否则旧话题留下的过时上下文可能干扰回答。

> 💡 **走错路或想换种方式？** 使用 `/rewind`（或按两次 Esc）打开 **时间线选择器**，让你回滚到对话中的任意更早节点，而不仅仅是最近一次。当你顺着错误的思路走了很远，又不想完全从头开始时，这非常有用。

---

### 从离开的地方继续

<img src="../../../02-context-conversations/images/session-persistence-timeline.png" alt="时间线展示 GitHub Copilot CLI 会话如何跨天保留 —— 周一开始，周三恢复，全部上下文都已还原" width="800"/>

*会话在你退出时会自动保存。几天之后恢复时，文件、问题和进度都会被记住。*

想象一下跨多天的工作流：

```bash
# 周一：开启一次图书应用审查，并从一开始就给会话命名
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# 着手修复...

> /exit
```

```bash
# 周三：按名字精确恢复到离开的位置
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**这之所以强大**：几天之后，Copilot CLI 仍然记得：
- 你正在处理的具体文件
- 编号过的问题列表
- 你已经处理过哪些问题
- 你们对话的上下文

无需重新解释。无需重新读取文件。直接接着干就行。

---

**🎉 你已经掌握了精华内容！** `@` 语法、会话管理（`--name`/`--continue`/`--resume`/`/rename`）以及上下文命令（`/context`/`/clear`），就足以让你高效地工作。下面的内容都是可选的。等你准备好时再回来看也不迟。

---

# 可选：深入了解

<img src="../../../02-context-conversations/images/optional-going-deeper.png" alt="蓝紫色调的抽象水晶洞窟，象征对上下文概念的更深入探索" width="800"/>

这些主题建立在上文的基础知识之上。**挑你感兴趣的看，或者直接跳到 [实践](#practice)。**

| 我想了解…… | 跳转到 |
|---|---|
| 通配符模式与高级会话命令 | [更多 @ 模式与会话命令](#additional-patterns) |
| 在多个提示词之间叠加上下文 | [上下文感知对话](#context-aware-conversations) |
| Token 限制与 `/compact` | [理解上下文窗口](#understanding-context-windows) |
| 如何挑选要引用的文件 | [选择要引用的内容](#choosing-what-to-reference) |
| 分析截图和原型图 | [处理图片](#working-with-images) |

<details>
<summary><strong>更多 @ 模式与会话命令</strong></summary>
<a id="additional-patterns"></a>

### 更多 @ 模式

对进阶用户，Copilot CLI 支持通配符模式和图片引用：

| 模式 | 作用 |
|---------|--------------|
| `@folder/*.py` | folder 中所有的 .py 文件 |
| `@**/test_*.py` | 递归通配：找出任何位置的所有测试文件 |
| `@image.png` | 用于 UI 审查的图片文件 |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### 查看会话信息

```bash
copilot

> /session
# 显示当前会话的详情和工作区摘要

> /usage
# 显示会话的指标和统计信息
```

### 分享你的会话

```bash
copilot

> /share file ./my-session.md
# 将会话导出为 markdown 文件

> /share gist
# 创建一个包含会话内容的 GitHub gist

> /share html
# 将会话导出为自包含的交互式 HTML 文件
# 适合把精修过的会话报告分享给同事，或留作日后参考
```

</details>

<details>
<summary><strong>上下文感知对话</strong></summary>
<a id="context-aware-conversations"></a>

### 上下文感知对话

当你进行层层叠加的多轮对话时，魔法才真正发生。

#### 示例：渐进式增强

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[Shows typed version]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[Adds validation and proper exceptions]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[Generates comprehensive tests]
```

注意每个提示词是如何在前一步工作的基础上构建的。这就是上下文的力量。

</details>

<details>
<summary><strong>理解上下文窗口</strong></summary>
<a id="understanding-context-windows"></a>

### 理解上下文窗口

你已经从基础部分了解了 `/context` 和 `/clear`。这里来看看上下文窗口工作原理的更深层次画面。

每个 AI 都有一个“上下文窗口”，也就是它一次能考虑的文本数量。

<img src="../../../02-context-conversations/images/context-window-visualization.png" alt="上下文窗口可视化" width="800"/>

*上下文窗口就像一张办公桌：一次只能容纳那么多东西。文件、对话历史和系统提示都会占用空间。*

#### 达到上限时会发生什么

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# 随着你添加更多文件和对话，这个数字会增长

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 警告：接近上下文上限

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` 命令

当你的上下文快满了，但又不想丢掉对话内容时，`/compact` 会汇总你的历史以释放 token：

```bash
copilot

> /compact
# 汇总对话历史，释放上下文空间
# 你的关键发现和决策会被保留
```

#### 上下文效率小贴士

| 场景 | 操作 | 原因 |
|-----------|--------|-----|
| 开启新话题 | `/clear` | 清除无关上下文 |
| 走错了路 | `/rewind` | 回滚到任意更早节点 |
| 长对话 | `/compact` | 汇总历史，释放 token |
| 需要特定文件 | `@file.py` 而非 `@folder/` | 仅加载所需内容 |
| 即将达到上限 | `/new` 或 `/clear` | 全新上下文 |
| 多个话题 | 每个话题用 `/rename` 命名 | 易于恢复到正确的会话 |

#### 大型代码库的最佳实践

1. **要具体**：用 `@samples/book-app-project/books.py` 而不是 `@samples/book-app-project/`
2. **在话题之间清理上下文**：切换关注点时使用 `/new` 或 `/clear`
3. **使用 `/compact`**：汇总对话以释放上下文
4. **使用多个会话**：每个功能或话题一个会话

</details>

<details>
<summary><strong>选择要引用的内容</strong></summary>
<a id="choosing-what-to-reference"></a>

### 选择要引用的内容

谈到上下文时，并非所有文件都同等重要。这里教你如何明智地选择：

#### 文件大小的考量

| 文件大小 | 大致 [Token](../../../GLOSSARY.md#token) 数 | 策略 |
|-----------|-------------------|----------|
| 小（少于 100 行） | 约 500-1,500 个 token | 可以随意引用 |
| 中（100-500 行） | 约 1,500-7,500 个 token | 引用具体文件 |
| 大（500 行以上） | 7,500+ 个 token | 有所取舍，引用特定文件 |
| 非常大（1000 行以上） | 15,000+ 个 token | 考虑拆分或只针对其中某些段落 |

**具体示例：**
- 图书应用的 4 个 Python 文件加起来约 2,000-3,000 个 token
- 一个典型的 Python 模块（200 行）约 3,000 个 token
- 一个 Flask API 文件（400 行）约 6,000 个 token
- 你的 package.json 约 200-500 个 token
- 一次简短的提示词 + 响应约 500-1,500 个 token

> 💡 **代码 token 数的快速估算法：** 把代码行数乘以约 15，就能得到大致的 token 数。请记住这只是一个估算。

#### 该包含什么 vs 该排除什么

**高价值**（建议包含）：
- 入口文件（`book_app.py`、`main.py`、`app.py`）
- 你正在询问的具体文件
- 被目标文件直接 import 的文件
- 配置文件（`requirements.txt`、`pyproject.toml`）
- 数据模型或 dataclass

**低价值**（可考虑排除）：
- 生成的文件（编译输出、打包后的资源）
- node modules 或 vendor 目录
- 大型数据文件或测试夹具
- 与你的问题无关的文件

#### 具体程度光谱

```
Less specific ────────────────────────► More specific
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ Scans everything                     └─ Just what you need
        (uses more context)                      (preserves context)
```

**何时放宽范围**（`@samples/book-app-project/`）：
- 初次探索代码库
- 跨多个文件查找模式
- 架构审查

**何时聚焦具体**（`@samples/book-app-project/books.py`）：
- 调试某个具体问题
- 对某个具体文件做代码审查
- 询问某一个函数

#### 实战示例：分阶段加载上下文

```bash
copilot

# 第 1 步：从结构开始
> @package.json What frameworks does this project use?

# 第 2 步：根据回答缩小范围
> @samples/book-app-project/ Show me the project structure

# 第 3 步：聚焦于关键内容
> @samples/book-app-project/books.py Review the BookCollection class

# 第 4 步：仅在需要时再加入相关文件
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

这种分阶段方法能让上下文保持聚焦且高效。

</details>

<details>
<summary><strong>处理图片</strong></summary>
<a id="working-with-images"></a>

### 处理图片

你可以通过 `@` 语法把图片加入对话，或者直接 **从剪贴板粘贴**（Cmd+V / Ctrl+V）。Copilot CLI 可以分析截图、原型图和示意图，帮助你进行 UI 调试、设计实现和错误分析。

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **了解更多**：参见 [更多上下文功能](../appendices/additional-context.md#working-with-images)，了解支持的格式、实用场景，以及把图片与代码结合使用的小技巧。

</details>

---

# 实践

<img src="../../../images/practice.png" alt="温馨的桌面：显示器上有代码、台灯、咖啡杯和耳机，准备开始动手实践" width="800"/>

是时候运用你在上下文和会话管理方面学到的技能了。

---

## ▶️ 自己动手试试

### 完整项目审查

本课程包含可直接审查的示例文件。启动 copilot 并运行下面的提示词：

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI 会指出诸如以下的问题：
# - 重复的展示函数
# - 缺失的输入校验
# - 不一致的错误处理
```

> 💡 **想用自己的文件试试？** 创建一个小型 Python 项目（`mkdir -p my-project/src`），添加一些 .py 文件，然后用 `@my-project/src/` 来审查它们。如果愿意，你也可以让 copilot 帮你生成示例代码！

### 会话工作流

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI 会建议一种校验方式]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 之后 —— 从离开的地方继续
copilot --continue

> Generate tests for the changes we made
```

---

完成上述演示之后，再尝试这些变体：

1. **跨文件挑战**：分析 book_app.py 和 books.py 是如何协同工作的：
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **会话挑战**：开启一个会话，用 `/rename my-first-session` 给它命名，做点事情，用 `/exit` 退出，然后运行 `copilot --continue`。它还记得你之前在做什么吗？

3. **上下文挑战**：在会话进行中运行 `/context`。你用了多少 token？再尝试 `/compact`，然后再次检查。（关于 `/compact` 的更多内容，请参见“深入了解”中的 [理解上下文窗口](#understanding-context-windows)。）

**自我检查**：当你能解释为什么 `@folder/` 比逐个打开每个文件更强大时，就说明你真正理解了上下文。

---

## 📝 作业

### 主挑战：追踪数据流

动手示例聚焦在代码质量审查和输入校验。现在用同样的上下文技巧来完成一个不同的任务 —— 追踪数据如何在应用中流动：

1. 启动一个交互式会话：`copilot`
2. 同时引用 `books.py` 和 `book_app.py`：
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. 把数据文件也纳入，作为额外上下文：
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. 请求一个跨文件的改进建议：
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. 重命名会话：`/rename data-flow-analysis`
6. 用 `/exit` 退出，然后用 `copilot --continue` 恢复，并就数据流再问一个后续问题

**成功标准**：你能跨多个文件追踪数据，能恢复一个命名过的会话，并能获得跨文件的建议。

<details>
<summary>💡 提示（点击展开）</summary>

**入门方法：**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

之后用 `copilot --continue` 恢复。

**有用的命令：**
- `@file.py` —— 引用单个文件
- `@folder/` —— 引用某个文件夹下的所有文件（注意结尾的 `/`）
- `/context` —— 查看当前用了多少上下文
- `/rename <name>` —— 给会话命名，方便日后恢复

</details>

### 加分挑战：上下文上限

1. 用 `@samples/book-app-project/` 一次性引用所有图书应用文件
2. 针对不同文件（`books.py`、`utils.py`、`book_app.py`、`data.json`）问几个详细问题
3. 运行 `/context` 查看用量。它有多快被填满？
4. 练习用 `/compact` 收回空间，然后继续对话
5. 试着让文件引用更具体（例如 `@samples/book-app-project/books.py` 而不是整个文件夹），观察上下文用量的变化

---

<details>
<summary>🔧 <strong>常见错误与故障排查</strong>（点击展开）</summary>

### 常见错误

| 错误 | 后果 | 解决方案 |
|---------|--------------|-----|
| 文件名前忘了写 `@` | Copilot CLI 把 “books.py” 当成普通文本 | 使用 `@samples/book-app-project/books.py` 来引用文件 |
| 期待会话自动持久化到下一次 | 重新启动 `copilot` 会丢失之前所有的上下文 | 使用 `--continue`（最近一次会话）或 `--resume`（从中挑选会话） |
| 引用当前目录之外的文件 | 出现 “Permission denied” 或 “File not found” 错误 | 使用 `/add-dir /path/to/directory` 授予访问权限 |
| 切换话题时不用 `/clear` | 旧的上下文会让对新话题的回答变得混乱 | 在开始另一项任务前先运行 `/clear` |

### 故障排查

**“File not found” 错误** —— 确认你处于正确的目录：

```bash
pwd  # 检查当前目录
ls   # 列出文件

# 然后启动 copilot 并使用相对路径
copilot

> Review @samples/book-app-project/books.py
```

**“Permission denied”** —— 把目录加入允许列表：

```bash
copilot --add-dir /path/to/directory

# 或者在会话内：
> /add-dir /path/to/directory
```

**上下文填充得太快**：
- 让文件引用更具体
- 在不同话题之间用 `/clear`
- 把工作拆分到多个会话中

</details>

---

# 小结

## 🔑 关键要点

1. **`@` 语法** 让 Copilot CLI 获得关于文件、目录和图片的上下文
2. **多轮对话** 会随着上下文的累积而互相叠加
3. **会话自动保存**：用 `--name` 在启动时命名，用 `--resume=<name>` 按名字恢复，或用 `--continue` 接着最近一次会话继续
4. **上下文窗口** 是有上限的：用 `/clear`、`/compact`、`/context`、`/new` 和 `/rewind` 来管理它们
5. **权限标志**（`--add-dir`、`--allow-all`）控制对多个目录的访问。请明智使用！
6. **图片引用**（`@screenshot.png`）有助于以可视方式调试 UI 问题

> 📚 **官方文档**：完整的上下文、会话与文件操作参考，请参见 [Use Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli)。

> 📋 **快速参考**：完整的命令和快捷键列表，请参见 [GitHub Copilot CLI 命令参考](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## ➡️ 下一步

既然你已经能给 Copilot CLI 提供上下文了，就让它真正在实际开发任务中派上用场吧。你刚刚学到的上下文技巧（文件引用、跨文件分析和会话管理）正是下一章中那些强大工作流的基础。

在 [**第 03 章：开发工作流**](../03-development-workflows/README.md) 中，你将学习：

- 代码审查工作流
- 重构模式
- 调试辅助
- 测试生成
- Git 集成

---

[**← 返回第 01 章**](../01-setup-and-first-steps/README.md) | [**继续到第 03 章 →**](../03-development-workflows/README.md)
