![第 06 章：MCP 服务器](../../../06-mcp-servers/images/chapter-header.png)

> **如果 Copilot 能读取你的 GitHub issue、查询数据库，并创建 PR……而这一切都在终端里完成，会是怎样的体验？**

到目前为止，Copilot 只能处理你直接提供给它的内容：你用 `@` 引用的文件、对话历史，以及它自身的训练数据。但如果它能主动访问你的 GitHub 仓库、浏览项目文件，或查阅某个库的最新文档，又会怎样呢？

这正是 MCP（Model Context Protocol，模型上下文协议）所做的事。它是一种将 Copilot 连接到外部服务的方式，让它能够访问实时的真实数据。Copilot 连接的每一项服务都被称为一个"MCP 服务器"。在本章中，你将设置几个这样的连接，并看到它们如何让 Copilot 变得更加强大。

> 💡 **已经熟悉 MCP？** [跳转到快速开始](#-use-the-built-in-github-mcp)，确认它正在工作并开始配置服务器。

## 🎯 学习目标

完成本章后，你将能够：

- 理解 MCP 是什么以及它为什么重要
- 使用 `/mcp` 命令管理 MCP 服务器
- 为 GitHub、文件系统和文档配置 MCP 服务器
- 在 book app 项目中使用基于 MCP 的工作流
- 知道何时以及如何构建自定义 MCP 服务器（可选）

> ⏱️ **预计用时**：约 50 分钟（15 分钟阅读 + 35 分钟动手实践）

---

## 🧩 现实类比：浏览器扩展

<img src="../../../06-mcp-servers/images/browser-extensions-analogy.png" alt="MCP 服务器就像浏览器扩展" width="800"/>

把 MCP 服务器想象成浏览器扩展。浏览器本身可以显示网页，但扩展能将它连接到额外的服务：

| 浏览器扩展 | 它连接的对象 | 对应的 MCP |
|-------------------|---------------------|----------------|
| 密码管理器 | 你的密码库 | **GitHub MCP** → 你的仓库、issue、PR |
| Grammarly | 写作分析服务 | **Context7 MCP** → 库的文档 |
| 文件管理器 | 云存储 | **Filesystem MCP** → 本地项目文件 |

没有扩展的浏览器仍然有用，但有了扩展，它就成了一个强大的工具。MCP 服务器对 Copilot 来说也是如此。它们将 Copilot 连接到真实、实时的数据源，让它可以读取你的 GitHub issue、浏览你的文件系统、获取最新文档等等。

***MCP 服务器将 Copilot 连接到外部世界：GitHub、代码仓库、文档以及更多内容***

> 💡 **关键洞察**：没有 MCP 时，Copilot 只能看到你用 `@` 显式分享的文件。有了 MCP，它可以主动探索你的项目、查看你的 GitHub 仓库、查找文档，所有这些都自动完成。

---

<img src="../../../06-mcp-servers/images/quick-start-mcp.png" alt="电源线与明亮的电火花相连，周围环绕着代表 MCP 服务器连接的科技图标" width="800"/>

# 快速开始：30 秒上手 MCP

## 从内置的 GitHub MCP 服务器开始
让我们立刻看看 MCP 的实际效果，无需任何配置。
GitHub MCP 服务器默认已经包含。试试这个：

```bash
copilot
> List the recent commits in this repository
```

如果 Copilot 返回了真实的提交数据，你就刚刚见识了 MCP 的实际作用。这就是 GitHub MCP 服务器代你访问 GitHub 的过程。但 GitHub 只是 *其中一个* 服务器。本章将向你展示如何添加更多服务器（文件系统访问、最新文档等等），让 Copilot 能做更多事情。

---

## `/mcp show` 命令

使用 `/mcp show` 查看已配置了哪些 MCP 服务器以及它们是否已启用：

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **只看到 GitHub 服务器？** 这是正常的！如果你还没添加任何额外的 MCP 服务器，那么 GitHub 就是列表中唯一的服务器。你将在下一节中添加更多。

> 📚 **想查看所有 MCP 管理命令？** 你可以在聊天中通过 `/mcp` 斜杠命令管理服务器，或直接在终端中使用 `copilot mcp`。请参阅本章末尾的[完整命令参考](#-additional-mcp-commands)。

<details>
<summary>🎬 看看实际效果！</summary>

![MCP 状态演示](../../../06-mcp-servers/images/mcp-status-demo.gif)

*演示输出会有所不同。你的模型、工具和响应会与此处展示的不同。*

</details>

---

## MCP 带来了哪些变化？

下面是 MCP 在实际使用中带来的差异：

**没有 MCP 时：**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**有了 MCP 后：**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP 让 Copilot 能够感知你真实的开发环境。

> 📚 **官方文档**：[关于 MCP](https://docs.github.com/copilot/concepts/context/mcp)，深入了解 MCP 如何与 GitHub Copilot 协同工作。

---

# 配置 MCP 服务器

<img src="../../../06-mcp-servers/images/configuring-mcp-servers.png" alt="双手在专业音频调音台上调节旋钮和滑块，代表 MCP 服务器的配置过程" width="800"/>

既然你已经看到了 MCP 的实际效果，那就让我们设置更多服务器吧。你可以通过两种方式添加服务器：**从内置注册表添加**（最简单——CLI 中提供引导式设置）或**手动编辑配置文件**（更灵活）。如果你不确定选哪种，请从注册表选项开始。

---

## 从注册表安装 MCP 服务器

CLI 内置了一个 MCP 服务器注册表，让你可以通过引导式设置发现并安装常用服务器——无需编辑 JSON。

```bash
copilot

> /mcp search
```

Copilot 会打开一个交互式选择器，显示可用的服务器。选择一个，CLI 就会引导你完成所需的配置（API 密钥、路径等），并自动将其添加到你的配置中。

> 💡 **为什么使用注册表？** 这是最容易上手的方式——你不需要知道 npm 包名、命令参数或 JSON 结构。CLI 会为你处理所有这些。

---

## MCP 配置文件

MCP 服务器配置在 `~/.copilot/mcp-config.json`（用户级，适用于所有项目）或 `.mcp.json`（项目级，放在项目根目录）中。如果你使用了上面的 `/mcp search`，CLI 已经为你创建或更新了此文件，但理解其格式有助于自定义。

> ⚠️ **注意**：`.vscode/mcp.json` 不再作为 MCP 配置源支持。如果你有现有的 `.vscode/mcp.json`，请将其迁移到项目根目录下的 `.mcp.json`。CLI 在检测到旧配置文件时会显示迁移提示。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*大多数 MCP 服务器以 npm 包的形式分发，并通过 `npx` 命令运行。*

<details>
<summary>💡 <strong>初次接触 JSON？</strong> 点击这里了解每个字段的含义</summary>

| 字段 | 含义 |
|-------|---------------|
| `"mcpServers"` | 所有 MCP 服务器配置的容器 |
| `"server-name"` | 你自己起的名字（例如 "github"、"filesystem"） |
| `"type": "local"` | 服务器在你的机器上运行 |
| `"command": "npx"` | 要运行的程序（npx 用于运行 npm 包） |
| `"args": [...]` | 传递给命令的参数 |
| `"tools": ["*"]` | 允许此服务器的所有工具 |

**重要的 JSON 规则：**
- 字符串使用双引号 `"`（不要使用单引号）
- 最后一项后面不能有逗号
- 文件必须是有效的 JSON（如果不确定，请使用 [JSON 验证器](https://jsonlint.com/)）

</details>

---

## 添加 MCP 服务器

GitHub MCP 服务器是内置的，无需任何设置。下面是你可以添加的其他服务器。**挑选你感兴趣的，或按顺序逐个学习。**

| 我想要…… | 跳转到 |
|---|---|
| 让 Copilot 浏览我的项目文件 | [Filesystem 服务器](#filesystem-服务器) |
| 获取最新的库文档 | [Context7 服务器](#context7-服务器-文档) |
| 探索可选的进阶功能（自定义服务器、web_fetch） | [进阶内容](#进阶内容) |

<details>
<summary><strong>Filesystem 服务器</strong> - 让 Copilot 探索你的项目文件</summary>
<a id="filesystem-server"></a>

### Filesystem 服务器

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` 路径的含义**：`.` 表示"当前目录"。Copilot 可以访问相对于你启动它的位置的文件。在 Codespace 中，这就是你的工作区根目录。如果你愿意，也可以使用绝对路径，例如 `/workspaces/copilot-cli-for-beginners`。

将其添加到你的 `~/.copilot/mcp-config.json` 中，然后重启 Copilot。

</details>

<details>
<summary><strong>Context7 服务器</strong> - 获取最新的库文档</summary>
<a id="context7-server-documentation"></a>

### Context7 服务器（文档）

Context7 让 Copilot 能够访问常用框架和库的最新文档。Copilot 不再依赖可能过时的训练数据，而是获取实际的当前文档。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **无需 API 密钥**
- ✅ **无需账号**
- ✅ **你的代码保留在本地**

将其添加到你的 `~/.copilot/mcp-config.json` 中，然后重启 Copilot。

</details>

<details>
<summary><strong>进阶内容</strong> - 自定义服务器与网络访问（可选）</summary>
<a id="beyond-the-basics"></a>

这些是可选的进阶内容，等你熟悉了上面的核心服务器后再来探索。

### Microsoft Learn MCP 服务器

到目前为止你看到的每个 MCP 服务器（filesystem、Context7）都在你的本地机器上运行。但 MCP 服务器也可以远程运行，这意味着你只需让 Copilot CLI 指向一个 URL，剩下的它都会处理。无需 `npx` 或 `python`，无需本地进程，也无需安装依赖。

[Microsoft Learn MCP 服务器](https://github.com/microsoftdocs/mcp)就是一个很好的例子。它让 Copilot CLI 可以直接访问 Microsoft 的官方文档（Azure、Microsoft Foundry 和其他 AI 主题、.NET、Microsoft 365 等等），从而能够搜索文档、获取完整页面，并查找官方代码示例，而不是依赖模型的训练数据。

- ✅ **无需 API 密钥**
- ✅ **无需账号**
- ✅ **无需本地安装**

**使用 `/plugin install` 快速安装：**

无需手动编辑 JSON 配置文件，你可以一条命令完成安装：

```bash
copilot

> /plugin install microsoftdocs/mcp
```

这会自动添加该服务器及其相关的 agent skill。安装的 skill 包括：

- **microsoft-docs**：概念、教程和事实查询
- **microsoft-code-reference**：API 查询、代码示例和故障排查
- **microsoft-skill-creator**：用于生成关于 Microsoft 技术的自定义 skill 的元 skill

**使用方法：**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 了解更多：[Microsoft Learn MCP 服务器概览](https://learn.microsoft.com/training/support/mcp-get-started)

### 使用 `web_fetch` 进行网络访问

Copilot CLI 内置了一个 `web_fetch` 工具，可以从任何 URL 获取内容。这在不离开终端的情况下拉取 README、API 文档或发布说明时非常有用。无需 MCP 服务器。

你可以通过 `~/.copilot/config.json`（Copilot 的常规设置）控制哪些 URL 可以访问，这与 `~/.copilot/mcp-config.json`（MCP 服务器定义）是分开的。

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**使用方法：**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### 构建自定义 MCP 服务器

想把 Copilot 连接到你自己的 API、数据库或内部工具？你可以用 Python 构建一个自定义的 MCP 服务器。这完全是可选的，因为预构建的服务器（GitHub、filesystem、Context7）已经覆盖了大多数使用场景。

📖 请参阅[自定义 MCP 服务器指南](mcp-custom-server.md)，其中以 book app 为例提供了完整的演练。

📚 想了解更多背景，请参阅 [MCP for Beginners 课程](https://github.com/microsoft/mcp-for-beginners)。

</details>

<a id="complete-configuration-file"></a>

### 完整的配置文件

下面是一个包含 filesystem 和 Context7 服务器的完整 `mcp-config.json`：

> 💡 **注意：** GitHub MCP 是内置的。你不需要将它添加到配置文件中。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

将其保存为 `~/.copilot/mcp-config.json` 以全局使用，或保存为项目根目录下的 `.mcp.json` 以进行项目级配置。

---

# 使用 MCP 服务器

现在你已经配置了 MCP 服务器，让我们看看它们能做什么。

<img src="../../../06-mcp-servers/images/using-mcp-servers.png" alt="使用 MCP 服务器 - 一个中心辐射式示意图，显示开发者的 CLI 与 GitHub、Filesystem、Context7 以及自定义/Web Fetch 服务器相连" width="800" />

---

## 服务器使用示例

**挑选一个服务器来探索，或按顺序逐个学习。**

| 我想试试…… | 跳转到 |
|---|---|
| GitHub 仓库、issue 与 PR | [GitHub 服务器](#github-服务器-内置) |
| 浏览项目文件 | [Filesystem 服务器使用](#filesystem-server-usage) |
| 查询库文档 | [Context7 服务器使用](#context7-server-usage) |
| 自定义服务器、Microsoft Learn MCP 与 web_fetch 用法 | [进阶内容用法](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub 服务器（内置）</strong> - 访问仓库、issue、PR 等等</summary>
<a id="github-server-built-in"></a>

### GitHub 服务器（内置）

GitHub MCP 服务器是**内置**的。如果你已登录 Copilot（在初次设置时已完成），它就已经可以工作了。无需任何配置！

> 💡 **不工作？** 运行 `/login` 以重新通过 GitHub 进行身份验证。

<details>
<summary><strong>开发容器中的身份验证</strong></summary>

- **GitHub Codespaces**（推荐）：身份验证是自动的。`gh` CLI 会继承你的 Codespace 令牌。无需任何操作。
- **本地开发容器（Docker）**：在容器启动后运行 `gh auth login`，然后重启 Copilot。

**身份验证故障排查：**
```bash
# Check if you're authenticated
gh auth status

# If not, log in
gh auth login

# Verify GitHub MCP is connected
copilot
> /mcp show
```

</details>

| 功能 | 示例 |
|---------|----------|
| **仓库信息** | 查看提交、分支、贡献者 |
| **Issue** | 列出、创建、搜索和评论 issue |
| **Pull Request** | 查看 PR、diff，创建 PR，检查状态 |
| **代码搜索** | 跨仓库搜索代码 |
| **Actions** | 查询工作流运行情况和状态 |

```bash
copilot

# See recent activity in this repo
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# Explore the repo structure
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# Search for code patterns across the repo
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **在使用自己的 fork？** 如果你 fork 了本课程仓库，你也可以试试写操作，例如创建 issue 和 pull request。我们会在下面的练习中实际操作一下。

> ⚠️ **看不到结果？** GitHub MCP 操作的是仓库的远程仓库（在 github.com 上），而不仅仅是本地文件。请确保你的仓库有远程地址：运行 `git remote -v` 进行检查。

</details>

<details>
<summary><strong>Filesystem 服务器</strong> - 浏览并分析项目文件</summary>
<a id="filesystem-server-usage"></a>

### Filesystem 服务器

配置完成后，filesystem MCP 会提供 Copilot 可以自动使用的工具：

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7 服务器</strong> - 查询库文档</summary>
<a id="context7-server-usage"></a>

### Context7 服务器

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot now knows the official pytest patterns
# and can apply them to samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>进阶内容</strong> - 自定义服务器与 web_fetch 用法</summary>
<a id="beyond-the-basics-usage"></a>

### 进阶内容

**自定义 MCP 服务器**：如果你按照[自定义 MCP 服务器指南](mcp-custom-server.md)构建了 book-lookup 服务器，你可以直接查询你的图书集合：

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**：如果你安装了 [Microsoft Learn MCP 服务器](#microsoft-learn-mcp-服务器)，你可以直接查询 Microsoft 的官方文档：

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**：使用内置的 `web_fetch` 工具从任何 URL 拉取内容：

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## 多服务器工作流

这些工作流展示了为什么开发者会说"再也不想没有它来工作了"。每个示例都在单个会话中组合了多个 MCP 服务器。

<img src="../../../06-mcp-servers/images/issue-to-pr-workflow.png" alt="使用 MCP 的 Issue 到 PR 工作流 - 展示了从获取 GitHub issue 到创建 pull request 的完整流程" width="800"/>

*完整的 MCP 工作流：GitHub MCP 检索仓库数据，Filesystem MCP 查找代码，Context7 MCP 提供最佳实践，Copilot 负责分析*

下面的每个示例都是自包含的。**挑选一个你感兴趣的，或者全部读完。**

| 我想看到…… | 跳转到 |
|---|---|
| 多个服务器协同工作 | [多服务器探索](#multi-server-exploration) |
| 在一个会话中从 issue 走到 PR | [Issue 到 PR 工作流](#issue-to-pr-workflow) |
| 快速进行项目健康检查 | [健康仪表板](#health-dashboard) |

<details>
<summary><strong>多服务器探索</strong> - 在一个会话中组合 filesystem、GitHub 和 Context7</summary>
<a id="multi-server-exploration"></a>

#### 用多个 MCP 服务器探索 Book App

```bash
copilot

# Step 1: Use filesystem MCP to explore the book app
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Step 2: Use GitHub MCP to check recent changes
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Step 3: Use Context7 MCP for best practices
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Step 4: Synthesize a recommendation
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 看看 MCP 工作流的实际效果！</summary>

![MCP 工作流演示](../../../06-mcp-servers/images/mcp-workflow-demo.gif)

*演示输出会有所不同。你的模型、工具和响应会与此处展示的不同。*

</details>

**结果**：代码探索 → 历史回顾 → 最佳实践查询 → 改进计划。**全部在一个终端会话中完成，同时使用三个 MCP 服务器。**

</details>

<details>
<summary><strong>Issue 到 PR 工作流</strong> - 不离开终端，从 GitHub issue 走到 pull request</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue 到 PR 工作流（在你自己的仓库中）

这在你拥有写权限的 fork 或仓库中效果最佳：

> 💡 **如果你现在不能尝试，不必担心。** 如果你处于只读克隆的状态，你将在作业中实际操作这一点。现在，先读完以理解整个流程。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**零复制粘贴。零上下文切换。一个终端会话。**

</details>

<details>
<summary><strong>健康仪表板</strong> - 使用多个服务器快速进行项目健康检查</summary>
<a id="health-dashboard"></a>

#### Book App 健康仪表板

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**结果**：多个数据源在几秒内被聚合在一起。手动完成的话，意味着要运行 grep、统计行数、检查 git log 并浏览测试文件。轻轻松松就要花 15 分钟以上的工作。

</details>

---

# 实践

<img src="../../../images/practice.png" alt="温馨的桌面布置：显示器上有代码，台灯、咖啡杯和耳机，准备好开始动手实践" width="800"/>

**🎉 你现在已经掌握了核心要点！** 你理解了 MCP，看到了如何配置服务器，也看到了真实工作流的实际效果。现在该轮到你自己试一试了。

---

## ▶️ 自己动手试试

现在轮到你了！完成这些练习，在 book app 项目上练习使用 MCP 服务器。

### 练习 1：检查你的 MCP 状态

先看看有哪些 MCP 服务器可用：

```bash
copilot

> /mcp show
```

你应该会看到 GitHub 服务器被列为已启用。如果没有，请运行 `/login` 进行身份验证。

---

### 练习 2：用 Filesystem MCP 探索 Book App

如果你已配置好 filesystem 服务器，用它来探索 book app：

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**预期结果**：Copilot 列出 `book_app.py`、`books.py` 和 `utils.py` 及其包含的函数。

> 💡 **还没配置 filesystem MCP？** 使用上面[完整配置](#完整的配置文件)章节中的 JSON 创建配置文件。然后重启 Copilot。

---

### 练习 3：用 GitHub MCP 查询仓库历史

使用内置的 GitHub MCP 探索本课程仓库：

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**预期结果**：Copilot 显示来自 GitHub 远程的最近提交信息和分支名。

> ⚠️ **在 Codespace 中？** 这会自动工作。身份验证是继承来的。如果你在本地克隆中，确保 `gh auth status` 显示你已登录。

---

### 练习 4：组合多个 MCP 服务器

现在在一个会话中组合 filesystem 和 GitHub MCP：

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**预期结果**：Copilot 读取该 JSON 文件（filesystem MCP），列出 5 本书，包括 "The Hobbit"、"1984"、"Dune"、"To Kill a Mockingbird" 和 "Mysterious Book"，然后查询 GitHub 获取提交历史。

**自我检查**：当你能够解释为什么"检查我的仓库提交历史"比手动运行 `git log` 并把输出粘贴到提示中更好时，你就理解了 MCP。

---

## 📝 作业

### 主要挑战：Book App MCP 探索

练习在 book app 项目上同时使用多个 MCP 服务器。在单个 Copilot 会话中完成以下步骤：

1. **验证 MCP 正在工作**：运行 `/mcp show` 并确认至少 GitHub 服务器已启用
2. **设置 filesystem MCP**（如果尚未完成）：创建 `~/.copilot/mcp-config.json` 并加入 filesystem 服务器配置
3. **探索代码**：要求 Copilot 使用 filesystem 服务器：
   - 列出 `samples/book-app-project/books.py` 中的所有函数
   - 检查 `samples/book-app-project/utils.py` 中哪些函数缺少类型提示
   - 读取 `samples/book-app-project/data.json` 并指出任何数据质量问题（提示：看看最后一项）
4. **检查仓库活动**：要求 Copilot 使用 GitHub MCP：
   - 列出最近修改了 `samples/book-app-project/` 中文件的提交
   - 检查是否有任何打开的 issue 或 pull request
5. **组合服务器**：在一个提示中，要求 Copilot：
   - 读取 `samples/book-app-project/tests/test_books.py` 中的测试文件
   - 将被测试的函数与 `books.py` 中的所有函数进行比较
   - 总结缺少哪些测试覆盖率

**成功标准**：你可以在单个 Copilot 会话中无缝地组合 filesystem 和 GitHub MCP 数据，并且可以解释每个 MCP 服务器对响应所做的贡献。

<details>
<summary>💡 提示（点击展开）</summary>

**第 1 步：验证 MCP**
```bash
copilot
> /mcp show
# Should show "github" as enabled
# If not, run: /login
```

**第 2 步：创建配置文件**

使用上面[完整配置](#完整的配置文件)章节中的 JSON，并将其保存为 `~/.copilot/mcp-config.json`。

**第 3 步：要查找的数据质量问题**

`data.json` 中的最后一本书是：
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
作者为空，年份为 0。这就是数据质量问题！

**第 5 步：测试覆盖率比较**

`test_books.py` 中的测试覆盖了：`add_book`、`mark_as_read`、`remove_book`、`get_unread_books` 和 `find_book_by_title`。像 `load_books`、`save_books` 和 `list_books` 这样的函数没有直接的测试。`book_app.py` 中的 CLI 函数和 `utils.py` 中的辅助函数完全没有测试。

**如果 MCP 不工作：** 在编辑配置文件后重启 Copilot。

</details>

### 进阶挑战：构建自定义 MCP 服务器

准备深入了？请按照[自定义 MCP 服务器指南](mcp-custom-server.md)用 Python 构建你自己的 MCP 服务器，连接到任何 API。

---

<details>
<summary>🔧 <strong>常见错误与故障排查</strong>（点击展开）</summary>

### 常见错误

| 错误 | 会发生什么 | 修复方法 |
|---------|--------------|-----|
| 不知道 GitHub MCP 是内置的 | 试图手动安装/配置它 | GitHub MCP 默认包含。直接试试："List the recent commits in this repo" |
| 在错误的位置查找配置 | 找不到或无法编辑 MCP 设置 | 用户级配置在 `~/.copilot/mcp-config.json` 中，项目级配置在项目根目录的 `.mcp.json` 中 |
| 配置文件中的 JSON 无效 | MCP 服务器无法加载 | 使用 `/mcp show` 检查配置；验证 JSON 语法 |
| 忘记对 MCP 服务器进行身份验证 | 出现"Authentication failed"错误 | 有些 MCP 需要单独的身份验证。检查每个服务器的要求 |

### 故障排查

**"MCP server not found"** - 检查：
1. npm 包是否存在：`npm view @modelcontextprotocol/server-github`
2. 你的配置是否为有效的 JSON
3. 服务器名称是否与配置匹配

使用 `/mcp show` 查看当前配置。

**"GitHub authentication failed"** - 内置的 GitHub MCP 使用你的 `/login` 凭据。试试：

```bash
copilot
> /login
```

这将通过 GitHub 重新对你进行身份验证。如果问题仍然存在，请检查你的 GitHub 账号是否对你访问的仓库具有必要的权限。

**"MCP server failed to start"** - 检查服务器日志：
```bash
# Run the server command manually to see errors
npx -y @modelcontextprotocol/server-github
```

**MCP 工具不可用** - 确保服务器已启用：
```bash
copilot

> /mcp show
# Check if server is listed and enabled
```

如果服务器被禁用，请参阅下面[其他 `/mcp` 命令](#-additional-mcp-commands)了解如何重新启用它。

</details>

---

<details>
<summary>📚 <strong>其他 MCP 命令</strong>（点击展开）</summary>
<a id="-additional-mcp-commands"></a>

你可以通过两种方式管理 MCP 服务器：在**聊天会话内使用斜杠命令**，或**直接在终端中使用 `copilot mcp` 命令**（不需要进入聊天会话）。

### 选项 1：斜杠命令（在聊天会话内）

这些命令在你已经在 `copilot` 中时可用：

| 命令 | 作用 |
|---------|--------------|
| `/mcp show` | 显示所有已配置的 MCP 服务器及其状态 |
| `/mcp add` | 交互式地设置以添加新服务器 |
| `/mcp edit <server-name>` | 编辑现有服务器配置 |
| `/mcp enable <server-name>` | 启用已禁用的服务器（跨会话保留） |
| `/mcp disable <server-name>` | 禁用服务器（跨会话保留） |
| `/mcp delete <server-name>` | 永久移除服务器 |
| `/mcp auth <server-name>` | 重新对使用 OAuth 的 MCP 服务器进行身份验证（例如，在切换账号后） |

### 选项 2：`copilot mcp` 命令（在终端中）

你也可以无需先开启聊天会话，直接从终端管理 MCP 服务器：

```bash
# List all configured MCP servers
copilot mcp list

# Enable a server
copilot mcp enable filesystem

# Disable a server
copilot mcp disable context7
```

> 💡 **何时使用哪种？** 当你已经在聊天会话中时，使用 `/mcp` 斜杠命令。当你想在开始会话之前快速检查或更改服务器设置时，从终端使用 `copilot mcp`。

在本课程的大部分内容中，`/mcp show` 就是你所需的全部。其他命令会随着你管理更多服务器而逐渐变得有用。

</details>

---

# 总结

## 🔑 核心要点

1. **MCP** 将 Copilot 连接到外部服务（GitHub、文件系统、文档）
2. **GitHub MCP 是内置的** —— 无需配置，只需 `/login`
3. **Filesystem 与 Context7** 通过 `~/.copilot/mcp-config.json` 配置
4. **多服务器工作流** 在单个会话中组合来自多个数据源的数据
5. **管理服务器有两种方式**：在聊天中使用 `/mcp` 斜杠命令，或在终端中使用 `copilot mcp`
6. **自定义服务器** 让你可以连接任何 API（可选，附录指南中已介绍）

> 📋 **快速参考**：完整的命令和快捷键列表请参阅 [GitHub Copilot CLI 命令参考](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## ➡️ 下一步

你现在已经具备了所有的构建块：模式、上下文、工作流、agent、skill 和 MCP。是时候将它们全部整合起来了。

在 [**第 07 章：融会贯通**](../07-putting-it-together/README.md) 中，你将学习：

- 在统一工作流中组合 agent、skill 和 MCP
- 从想法到合并的 PR 的完整功能开发
- 使用 hook 进行自动化
- 团队环境中的最佳实践

---

[**← 返回第 05 章**](../05-skills/README.md) | [**继续到第 07 章 →**](../07-putting-it-together/README.md)
