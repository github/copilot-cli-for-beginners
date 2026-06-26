![第 04 章：智能体与自定义指令](../../../04-agents-custom-instructions/images/chapter-header.png)

> **如果你能一次性"雇佣"一位 Python 代码审查员、一位测试专家和一位安全审查员……而且全都集成在同一个工具里，会怎么样？**

在第 03 章中，你掌握了几项核心工作流：代码审查、重构、调试、测试生成和 Git 集成。这些工作流让你能够借助 GitHub Copilot CLI 极大地提升生产力。现在，我们再往前走一步。

到目前为止，你一直把 Copilot CLI 当作一个通用助手来使用。智能体（Agent）则可以赋予它一个具体的"身份"，并自带一套既定标准——比如一位强制要求类型注解和 PEP 8 的代码审查员，或者一位专门编写 pytest 用例的测试助手。你将会看到：同样的提示词，交给一个有针对性指令的智能体来处理时，输出质量会有明显的提升。

## 🎯 学习目标

学完本章之后，你将能够：

- 使用内置智能体：Plan（`/plan`）、Code-review（`/review`），并理解自动智能体（Explore、Task）
- 使用智能体文件（`.agent.md`）创建专门化的智能体
- 利用智能体处理特定领域的任务
- 通过 `/agent` 与 `--agent` 在不同智能体之间切换
- 编写自定义指令文件，沉淀项目专属的标准

> ⏱️ **预计时长**：约 55 分钟（20 分钟阅读 + 35 分钟动手实践）

---

## 🧩 现实类比：聘请专业人士

当家里需要修缮时，你不会只打一个"万能帮手"的电话，而是会找对应的专业人员：

| 问题 | 专业人员 | 原因 |
|---------|------------|-----|
| 水管漏水 | 水管工 | 熟悉管道规范，拥有专用工具 |
| 重新布线 | 电工 | 了解安全要求，符合法规 |
| 更换屋顶 | 屋顶工 | 熟悉材料，了解当地天气情况 |

智能体的工作方式与此完全相同。与其使用一个通用 AI，不如使用专注于特定任务、并且了解正确流程的智能体。指令只需配置一次，之后每当你需要那种"专长"时——代码审查、测试、安全、文档——都可以直接复用。

<img src="../../../04-agents-custom-instructions/images/hiring-specialists-analogy.png" alt="聘请专业人士的类比——就像家庭维修要找专门的工种一样，AI 智能体也专门用于代码审查、测试、安全、文档等特定任务" width="800" />

---

# 使用智能体

立即上手内置智能体和自定义智能体。

---

## *第一次接触智能体？* 从这里开始！
从未使用或创建过智能体？以下是开启本课程所需的全部知识点。

1. **马上试用一个 *内置* 智能体：**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   这会调用 Plan 智能体，为你生成一份分步实现计划。

2. **看看我们准备的自定义智能体示例：** 定义一个智能体的指令非常简单，看一下我们提供的 [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) 文件就能掌握其模式。

3. **理解核心理念：** 使用智能体就像咨询某个领域的专家，而不是一个万能的通才。一个"前端智能体"会自动关注无障碍特性和组件模式，你不需要每次都提醒它，因为这些已经写在智能体的指令里了。


## 内置智能体

**在第 03 章"开发工作流"中你已经使用过一些内置智能体了！**
<br>`/plan` 和 `/review` 实际上就是内置智能体。现在你也明白了它们背后的运作机制。下面是完整列表：

| 智能体 | 调用方式 | 作用 |
|-------|---------------|--------------|
| **Plan** | `/plan` 或 `Shift+Tab`（在多种模式间切换） | 在编码之前生成分步实现计划 |
| **Code-review** | `/review` | 针对已暂存／未暂存的更改给出聚焦、可执行的反馈 |
| **Init** | `/init` | 生成项目配置文件（指令、智能体） |
| **Explore** | *自动调用* | 当你让 Copilot 探索或分析代码库时在内部使用 |
| **Task** | *自动调用* | 执行测试、构建、Lint、依赖安装等命令 |

<br>

**内置智能体实战** —— 调用 Plan、Code-review、Explore 与 Task 的示例

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

那么 Task 智能体呢？它会在幕后管理与跟踪正在发生的事情，并以清晰、整洁的格式向你汇报：

| 结果 | 你会看到什么 |
|---------|--------------|
| ✅ **成功** | 简短摘要（例如："All 247 tests passed"、"Build succeeded"） |
| ❌ **失败** | 完整输出，包括堆栈跟踪、编译器错误和详细日志 |


> 📚 **官方文档**：[GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# 为 Copilot CLI 添加智能体

你完全可以定义自己的智能体，把它们融入到日常工作流中！一次定义，随时调用！

<img src="../../../04-agents-custom-instructions/images/using-agents.png" alt="四个色彩缤纷的 AI 机器人并肩而立，每个都拿着不同的工具，象征着各自专长的智能体能力" width="800"/>

## 🗂️ 添加你的智能体 

智能体文件就是后缀为 `.agent.md` 的 Markdown 文件。它由两部分组成：YAML 前置信息（元数据）和 Markdown 指令。

> 💡 **第一次接触 YAML frontmatter？** 它是位于文件顶部、被 `---` 包裹的一小段配置。YAML 就是 `key: value` 形式的键值对。文件的其余部分仍然是普通的 Markdown。

下面是一个最简化的智能体：

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

> 💡 **必填项与可选项**：`description` 字段是必填的。其他字段如 `name`、`tools` 和 `model` 都是可选的。

## 智能体文件应当放在哪里

| 位置 | 作用范围 | 适用场景 |
|----------|-------|----------|
| `.github/agents/` | 项目级 | 团队共享、带有项目约定的智能体 |
| `~/.copilot/agents/` | 全局（所有项目） | 在任何地方都能用的个人智能体 |

**本项目在 [.github/agents/](../../../.github/agents/) 目录中提供了一些示例智能体文件**。你可以自己写，也可以基于这些已有的文件做定制。

<details>
<summary>📂 查看本课程提供的示例智能体</summary>

| 文件 | 说明 |
|------|-------------|
| `hello-world.agent.md` | 极简示例——从这里开始 |
| `python-reviewer.agent.md` | Python 代码质量审查员 |
| `pytest-helper.agent.md` | Pytest 测试专家 |

```bash
# Or copy one to your personal agents folder (available in every project)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

更多社区提供的智能体，请参见 [github/awesome-copilot](https://github.com/github/awesome-copilot)

</details>


## 🚀 使用自定义智能体的两种方式

### 交互模式
在交互模式下，使用 `/agent` 列出所有智能体并选择要使用的智能体。
选中后，对话将由该智能体接管并继续。

```bash
copilot
> /agent
```

要切换到另一个智能体，或回到默认模式，再次使用 `/agent` 命令即可。

### 编程模式

直接以指定智能体的身份启动一个新会话。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **切换智能体**：你可以随时通过再次使用 `/agent` 或 `--agent` 切换到其他智能体。要返回标准的 Copilot CLI 体验，使用 `/agent` 并选择 **no agent** 即可。

---

# 深入使用智能体

<img src="../../../04-agents-custom-instructions/images/creating-custom-agents.png" alt="工作台上正在被组装的机器人，周围环绕着各种零件与工具，象征着自定义智能体的创建过程" width="800"/>

> 💡 **本节为可选阅读。** 内置智能体（`/plan`、`/review`）已经足以应对大多数工作流。当你需要在工作中始终如一地应用某种专长时，再去创建自定义智能体即可。

下面的每个主题都是自包含的。**挑选你感兴趣的内容看就行——不必一次性全部读完。**

| 我想要…… | 跳转到 |
|---|---|
| 看看为什么智能体比通用提示更胜一筹 | [专家 vs 通才](#专家-vs-通才-直观对比) |
| 在一个功能上组合多个智能体 | [使用多个智能体协作](#使用多个智能体协作) |
| 组织、命名并分享智能体 | [组织与分享智能体](#organizing--sharing-agents) |
| 配置始终生效的项目上下文 | [为 Copilot 配置你的项目](#为-copilot-配置你的项目) |
| 查阅 YAML 属性和工具 | [智能体文件参考](#智能体文件参考) |

点击下方任一场景即可展开。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>专家 vs 通才：直观对比</strong> —— 为什么智能体的输出比通用提示更优</summary>

## 专家 vs 通才：直观对比

这正是智能体体现价值的地方。看看二者的差距：

### 不使用智能体（通用 Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
```

**通用输出**：
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基础、能跑，但缺失了很多细节。

---

### 使用 Python Reviewer 智能体

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
```

**专家输出**：
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

**python-reviewer 智能体自动包含了哪些内容**：
- ✅ 所有参数和返回值都带有类型注解
- ✅ 完整的 docstring，包含 Args/Returns/Raises
- ✅ 输入校验，并配套合适的错误处理
- ✅ 使用列表推导式以获得更好的性能
- ✅ 处理了边界情况（缺失或无效的 year 值）
- ✅ 符合 PEP 8 的格式规范
- ✅ 防御式编程实践

**差异之处**：同一个提示，输出却好得多。智能体会自动带上那些你可能忘了要求的专业实践。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>使用多个智能体协作</strong> —— 组合专家、会话中切换、把智能体当作工具</summary>

## 使用多个智能体协作

当多个专家围绕同一个功能协同工作时，真正的威力才会显现。

### 示例：构建一个简单功能

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

**关键洞察**：你是指挥专家的架构师。他们负责具体细节，你负责整体愿景。

<details>
<summary>🎬 看看实际效果！</summary>

![Python Reviewer 演示](../../../04-agents-custom-instructions/images/python-reviewer-demo.gif)

*演示输出会有所不同——你的模型、工具和响应都会与图中所示有所差异。*

</details>

### 把智能体当作工具

当你配置好智能体后，Copilot 在处理复杂任务时也可以把它们作为工具来调用。比如你请求一个全栈功能时，Copilot 可能会自动把其中的某些部分委派给合适的专家智能体。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>组织与分享智能体</strong> —— 命名、文件位置、指令文件以及团队共享</summary>

## 组织与分享智能体

### 给智能体起名

创建智能体文件时，名字很重要。你需要在 `/agent` 或 `--agent` 后输入它，团队成员也会在智能体列表中看到它。

| ✅ 推荐的名字 | ❌ 应避免 |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名约定：**
- 使用小写字母加连字符：`my-agent-name.agent.md`
- 包含领域信息：`frontend`、`backend`、`devops`、`security`
- 必要时更具体：`react-typescript` 优于笼统的 `frontend`

---

### 与团队共享

将智能体文件放在 `.github/agents/` 中，它们就会被纳入版本控制。推送到仓库后，每位团队成员都能自动获取。但智能体只是 Copilot 从你的项目中读取的文件类型之一，它还支持 **指令文件**——这些文件会自动应用到每一次会话，无需任何人执行 `/agent`。

可以这样理解：智能体是你按需调用的专家，而指令文件则是团队中始终生效的规则。

### 文件应放在哪里

你已经了解了两个主要位置（参见上文 [智能体文件应当放在哪里](#智能体文件应当放在哪里)）。可以使用下面这棵决策树来决定：

<img src="../../../04-agents-custom-instructions/images/agent-file-placement-decision-tree.png" alt="智能体文件位置决策树：试验阶段 → 当前文件夹；团队使用 → .github/agents/；到处使用 → ~/.copilot/agents/" width="800"/>

**从简单开始：** 先在你的项目目录里创建一个 `*.agent.md` 文件。等你对它满意了，再把它移到一个长期位置。

除了智能体文件，Copilot 还会自动读取 **项目级别的指令文件**，无需 `/agent`。详情见下文的 [为 Copilot 配置你的项目](#为-copilot-配置你的项目)，其中介绍了 `AGENTS.md`、`.instructions.md` 以及 `/init`。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>为 Copilot 配置你的项目</strong> —— AGENTS.md、指令文件以及 /init 设置</summary>

## 为 Copilot 配置你的项目

智能体是你按需调用的专家。**项目配置文件** 则不同：Copilot 会在每一次会话中自动读取它们，以了解项目的约定、技术栈和规则。无需任何人执行 `/agent`，仓库中所有协作者都自动共享同一份上下文。

### 使用 /init 快速搭建

最快的入门方式，是让 Copilot 帮你生成配置文件：

```bash
copilot
> /init
```

Copilot 会扫描你的项目，并创建量身定制的指令文件。生成之后你还可以自行修改。

### 指令文件格式

| 文件 | 作用范围 | 备注 |
|------|-------|-------|
| `AGENTS.md` | 项目根目录或子目录 | **跨平台标准** —— 同时适用于 Copilot 和其他 AI 助手 |
| `.github/copilot-instructions.md` | 项目级 | 专属于 GitHub Copilot |
| `.github/instructions/*.instructions.md` | 项目级 | 颗粒度更细、按主题分文件的指令 |
| `CLAUDE.md`、`GEMINI.md` | 项目根目录 | 出于兼容性考虑同样支持 |

> 🎯 **刚刚入门？** 项目指令直接使用 `AGENTS.md`。其他格式可以等到有需要时再去探索。

### AGENTS.md

`AGENTS.md` 是推荐的格式。它是一个 [开放标准](https://agents.md/)，可在 Copilot 和其他 AI 编码工具之间通用。把它放在仓库根目录，Copilot 就会自动读取。本项目自身的 [AGENTS.md](../../../AGENTS.md) 就是一个可参考的实例。

一份典型的 `AGENTS.md` 通常会描述项目背景、代码风格、安全要求和测试标准。你可以参照我们的示例文件来编写自己的版本。

### 自定义指令文件（.instructions.md）

如果团队希望进行更细粒度的控制，可以把指令拆分成按主题分类的文件。每个文件聚焦一个关注点，并自动生效：

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **提示**：指令文件适用于任何语言。这里使用 Python 是为了与本课程项目保持一致，但你也可以为 TypeScript、Go、Rust 或团队使用的任何技术创建类似的文件。

**寻找社区提供的指令文件**：到 [github/awesome-copilot](https://github.com/github/awesome-copilot) 浏览，那里有现成的指令文件，覆盖 .NET、Angular、Azure、Python、Docker 以及更多技术栈。

### 禁用自定义指令

如果你需要让 Copilot 忽略所有项目特定配置（在调试或对比行为时很有用）：

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>智能体文件参考</strong> —— YAML 属性、工具别名和完整示例</summary>

## 智能体文件参考

### 一个更完整的示例

你已经在前面看过 [最简智能体格式](#-添加你的智能体)。下面是一个更完整、并且使用了 `tools` 属性的智能体。请创建 `~/.copilot/agents/python-reviewer.agent.md`：

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

### YAML 属性

| 属性 | 是否必填 | 说明 |
|----------|----------|-------------|
| `name` | 否 | 显示名称（默认使用文件名） |
| `description` | **是** | 描述智能体的作用——帮助 Copilot 了解何时建议使用它 |
| `tools` | 否 | 允许使用的工具列表（不写则全部可用）。参见下方的工具别名。 |
| `target` | 否 | 限定为仅 `vscode` 或仅 `github-copilot` |

### 工具别名

在 `tools` 列表中可使用以下名称：
- `read` —— 读取文件内容
- `edit` —— 编辑文件
- `search` —— 搜索文件（grep/glob）
- `execute` —— 执行 shell 命令（亦可写作 `shell`、`Bash`）
- `agent` —— 调用其他自定义智能体

> 📖 **官方文档**：[Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **仅 VS Code**：`model` 属性（用于选择 AI 模型）在 VS Code 中可用，但 GitHub Copilot CLI 并不支持。为了跨平台共享智能体文件，你可以放心地包含它，GitHub Copilot CLI 会忽略这个字段。

### 更多智能体模板

> 💡 **写给初学者**：下面这些示例只是模板。**请把其中提到的具体技术替换成你项目实际使用的技术。** 重要的是智能体的*结构*，而不是它提到的某项具体技术。

本项目在 [.github/agents/](../../../.github/agents/) 目录中提供了可直接运行的示例：
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) —— 极简示例，从这里开始
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) —— Python 代码质量审查员
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) —— Pytest 测试专家

更多社区智能体，请参见 [github/awesome-copilot](https://github.com/github/awesome-copilot)。

</details>

---

# 实战练习

<img src="../../../images/practice.png" alt="温馨的桌面布置：显示着代码的显示器、台灯、咖啡杯和耳机，一切都已就绪，准备开始动手实践" width="800"/>

亲手创建你自己的智能体，并看看它们的实际效果。

---

## ▶️ 自己动手试一试

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

## 📝 作业

### 主挑战：组建一支专门化的智能体团队

在前面的动手示例中，你创建了 `reviewer` 和 `documentor` 两个智能体。现在我们换一个任务来练习创建并使用智能体——改进 book app 中的数据校验：

1. 在 `.github/agents/` 中创建 3 个针对 book app 的智能体文件（`.agent.md`），每个智能体一个文件
2. 你的智能体：
   - **data-validator**：检查 `data.json` 中是否存在缺失或畸形的数据（空作者、year=0、字段缺失）
   - **error-handler**：审查 Python 代码中错误处理是否一致，并给出统一方案的建议
   - **doc-writer**：生成或更新 docstring 与 README 内容
3. 在 book app 上分别使用每个智能体：
   - `data-validator` → 审计 `@samples/book-app-project/data.json`
   - `error-handler` → 审查 `@samples/book-app-project/books.py` 与 `@samples/book-app-project/utils.py`
   - `doc-writer` → 给 `@samples/book-app-project/books.py` 添加 docstring
4. 让它们协作：先用 `error-handler` 找出错误处理上的不足，再用 `doc-writer` 把改进后的方案文档化

**完成标准**：你拥有 3 个可用的智能体，它们能够稳定地给出高质量的输出，并且你可以通过 `/agent` 在它们之间切换。

<details>
<summary>💡 提示（点击展开）</summary>

**起步模板**：在 `.github/agents/` 中为每个智能体创建一个文件：

`data-validator.agent.md`：
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

`error-handler.agent.md`：
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

`doc-writer.agent.md`：
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

**测试你的智能体：**

> 💡 **提示：** 你本地的仓库副本中应该已经包含 `samples/book-app-project/data.json`。如果该文件缺失，请从源仓库下载原始版本：
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Select "data-validator" from the list
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**小贴士：** YAML 前置信息中的 `description` 字段是智能体能正常工作的必填项。

</details>

### 加分挑战：指令库

你已经构建了按需调用的智能体。现在试试另一面：**指令文件**——Copilot 会在每次会话中自动读取它们，无需 `/agent`。

创建一个 `.github/instructions/` 文件夹，并在其中放入至少 3 个指令文件：
- `python-style.instructions.md`，用于强制执行 PEP 8 与类型注解约定
- `test-standards.instructions.md`，用于在测试文件中强制执行 pytest 约定
- `data-quality.instructions.md`，用于校验 JSON 数据条目

针对 book app 的代码，分别测试每个指令文件。

---

<details>
<summary>🔧 <strong>常见错误与故障排查</strong>（点击展开）</summary>

### 常见错误

| 错误 | 现象 | 修复方式 |
|---------|--------------|-----|
| 智能体前置信息中缺少 `description` | 智能体无法加载或无法被发现 | 始终在 YAML 前置信息中包含 `description:` |
| 智能体文件位置不正确 | 调用时找不到对应的智能体 | 放置到 `~/.copilot/agents/`（个人）或 `.github/agents/`（项目） |
| 使用 `.md` 而不是 `.agent.md` | 文件可能不会被识别为智能体 | 文件名按 `python-reviewer.agent.md` 这种方式命名 |
| 智能体提示词过长 | 可能超出 30,000 个字符的上限 | 智能体定义保持聚焦；详尽的指令交给 skill 来承载 |

### 故障排查

**找不到智能体** —— 检查智能体文件是否存在于以下位置之一：
- `~/.copilot/agents/`
- `.github/agents/`

列出可用的智能体：

```bash
copilot
> /agent
# Shows all available agents
```

**智能体不按指令执行** —— 在你的提示词中要更明确，并在智能体定义中补充更多细节：
- 指明具体的框架／库以及版本
- 团队约定
- 示例代码模式

**自定义指令未加载** —— 在你的项目中执行 `/init` 来设置项目级指令：

```bash
copilot
> /init
```

也可以检查它们是否被禁用：
```bash
# Don't use --no-custom-instructions if you want them loaded
copilot  # This loads custom instructions by default
```

</details>

---

# 小结

## 🔑 关键要点

1. **内置智能体**：`/plan` 和 `/review` 直接调用即可；Explore 和 Task 会自动工作
2. **自定义智能体** 是定义在 `.agent.md` 文件中的专家
3. **优秀的智能体** 拥有清晰的专长、标准与输出格式
4. **多智能体协作** 通过组合不同专长来解决复杂问题
5. **指令文件**（`.instructions.md`）将团队标准编码下来，自动生效
6. **稳定一致的输出** 来自定义良好的智能体指令

> 📋 **快速参考**：完整的命令与快捷键列表，请参阅 [GitHub Copilot CLI 命令参考](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## ➡️ 下一步

智能体改变的是 *Copilot 在你的代码中如何思考问题、采取有针对性的行动* 的方式。接下来，你将了解 **技能（skills）**——它们改变的是 Copilot 遵循的 *步骤*。想知道智能体和技能到底有什么不同？第 05 章会正面回答这个问题。

在 [**第 05 章：Skills 系统**](../05-skills/README.md) 中，你将学到：

- 技能如何根据你的提示自动触发（无需斜杠命令）
- 安装社区提供的技能
- 通过 SKILL.md 文件创建自定义技能
- 智能体、技能与 MCP 之间的区别
- 何时使用哪一种

---

[**← 返回第 03 章**](../03-development-workflows/README.md) | [**继续学习第 05 章 →**](../05-skills/README.md)
