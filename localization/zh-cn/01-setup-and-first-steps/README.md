![第 01 章：第一步](../../../01-setup-and-first-steps/images/chapter-header.png)

> **看看 AI 如何瞬间发现 bug、解释令人困惑的代码、生成可用的脚本。然后学习使用 GitHub Copilot CLI 的三种不同方式。**

本章是魔法开始的地方！你将亲身体验为什么开发者把 GitHub Copilot CLI 形容为「随时能拨通的资深工程师」。你将看到 AI 在几秒钟内找出安全漏洞，用通俗的语言解释复杂的代码，并即时生成可用的脚本。然后你将掌握三种交互模式（Interactive、Plan 和 Programmatic），让你清楚地知道任何任务该使用哪一种。

> ⚠️ **前置条件**：请确保你已经完成了 **[第 00 章：快速入门](../00-quick-start/README.md)**。在运行下面的演示之前，你需要先安装并完成 GitHub Copilot CLI 的身份认证。

## 🎯 学习目标

学完本章后，你将能够：

- 通过实操演示亲身感受 GitHub Copilot CLI 带来的生产力提升
- 为任何任务选择正确的模式（Interactive、Plan 或 Programmatic）
- 使用斜杠命令来控制你的会话

> ⏱️ **预计时间**：约 45 分钟（阅读 15 分钟 + 实操 30 分钟）

---

# 你的第一次 Copilot CLI 体验

<img src="../../../01-setup-and-first-steps/images/first-copilot-experience.png" alt="开发者坐在桌前，显示器上是代码，发光的粒子代表 AI 辅助" width="800"/>

直接上手，看看 Copilot CLI 能做什么。

---

## 轻松上手：你的第一组提示词

在进入令人惊艳的演示之前，我们先来尝试一些你现在就可以用的简单提示词。**不需要任何代码仓库**！只需打开一个终端并启动 Copilot CLI：

```bash
copilot
```

试试这些适合新手的提示词：

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

不用 Python？没问题！只需就你选择的语言提问即可。

注意它感觉有多自然。就像问同事问题一样直接提问。当你探索完毕后，输入 `/exit` 退出会话。

**关键洞察**：GitHub Copilot CLI 是对话式的。你不需要特殊的语法就能开始。只需用通俗的语言提问。

## 实战演示

现在让我们看看为什么开发者会说这就像「随时能拨通的资深工程师」。

> 📖 **阅读示例**：以 `>` 开头的行是你在 Copilot CLI 交互式会话中输入的提示词。没有 `>` 前缀的行是你在终端中运行的 shell 命令。

> 💡 **关于示例输出**：本课程中展示的示例输出仅供参考。由于 Copilot CLI 的回复每次都不一样，你的结果在措辞、格式和细节上都会有所不同。请关注返回信息的*类型*，而不是确切的文字。

### 演示 1：几秒钟完成代码评审

本课程包含了一些有意保留代码质量问题的示例文件。如果你在本地机器上工作并且尚未克隆仓库，请运行下面的 `git clone` 命令，进入 `copilot-cli-for-beginners` 文件夹，然后运行 `copilot` 命令。

```bash
# Clone the course repository if you're working locally and haven't already
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Start Copilot
copilot
```

进入 Copilot CLI 交互式会话后，运行以下命令：

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 符号是干什么用的？** `@` 符号告诉 Copilot CLI 去读取一个文件。你将在第 02 章详细学习它。现在，只需完全照抄上面的命令即可。

---

<details>
<summary>🎬 看看实际效果！</summary>

![代码评审演示](../../../01-setup-and-first-steps/images/code-review-demo.gif)

*演示输出会有所不同。你的模型、工具和回复都会与此处展示的不同。*

</details>

---

**收获**：几秒钟就完成了一次专业的代码评审。手动评审会花费……嗯……远比这多得多的时间！

---

### 演示 2：解释令人困惑的代码

有没有盯着代码搞不懂它到底在做什么的经历？在你的 Copilot CLI 会话中试试这个：

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![解释代码演示](../../../01-setup-and-first-steps/images/explain-code-demo.gif)

*演示输出会有所不同。你的模型、工具和回复都会与此处展示的不同。*

</details>

---

**会发生什么**：（你的输出会有所不同）Copilot CLI 读取文件、理解代码，并用通俗的语言解释它。

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**收获**：复杂的代码就像一位有耐心的导师那样被解释清楚了。

---

### 演示 3：生成可用的代码

需要一个原本要花 15 分钟去 Google 的函数？继续在你的会话中：

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![生成代码演示](../../../01-setup-and-first-steps/images/generate-code-demo.gif)

*演示输出会有所不同。你的模型、工具和回复都会与此处展示的不同。*

</details>

---

**会发生什么**：几秒钟内就得到一个完整、可用的函数，可以直接复制粘贴运行。

探索完毕后，退出会话：

```
> /exit
```

**收获**：即时获得满足感，而且整个过程你都在同一个连续的会话中。

---

# 模式与命令

<img src="../../../01-setup-and-first-steps/images/modes-and-commands.png" alt="未来感十足的控制面板，有发光的屏幕、旋钮和均衡器，代表 Copilot CLI 的模式和命令" width="800"/>

你已经看到了 Copilot CLI 能做什么。现在让我们了解*如何*高效地使用这些能力。关键是要知道在不同情境下应该使用三种交互模式中的哪一种。

> 💡 **注意**：Copilot CLI 还有一个 **Autopilot** 模式，它会自动完成任务而无需等待你的输入。它很强大，但需要授予完整的权限，并会自动消耗 premium 请求额度。本课程聚焦于下面的三种模式。等你熟悉了基础知识后，我们会指引你了解 Autopilot。

---

## 🧩 现实类比：外出就餐

把使用 GitHub Copilot CLI 想象成一次外出就餐。从规划行程到点单，不同的情境需要不同的方式：

| 模式 | 就餐类比 | 何时使用 |
|------|----------------|-------------|
| **Plan** | 去餐厅的 GPS 路线 | 复杂任务——先规划路线、检查每一站、达成共识，然后再开车 |
| **Interactive** | 与服务员交谈 | 探索和迭代——提问、定制、获得实时反馈 |
| **Programmatic** | 得来速点单 | 快速、明确的任务——留在你的环境里，快速拿到结果 |

就像外出就餐一样，你会自然而然地学会什么时候用哪种方式最合适。

<img src="../../../01-setup-and-first-steps/images/ordering-food-analogy.png" alt="使用 GitHub Copilot CLI 的三种方式 - Plan 模式（去餐厅的 GPS 路线）、Interactive 模式（与服务员交谈）、Programmatic 模式（得来速）" width="800"/>

*根据任务选择你的模式：Plan 用于先规划，Interactive 用于来回协作，Programmatic 用于快速一次性结果*

### 我应该从哪种模式开始？

**从 Interactive 模式开始。**
- 你可以做实验、提出后续问题
- 上下文通过对话自然地积累
- 出错时使用 `/clear` 就能轻松纠正

熟悉之后，再尝试：
- **Programmatic 模式**（`copilot -p "<your prompt>"`）用于快速的一次性问题
- **Plan 模式**（`/plan`）当你在编码前需要更详细地规划事情时

---

## 三种模式

### 模式 1：Interactive 模式（从这里开始）

<img src="../../../01-setup-and-first-steps/images/interactive-mode.png" alt="Interactive 模式 - 就像和能回答问题、调整订单的服务员交谈" width="250"/>

**最适合**：探索、迭代、多轮对话。就像和一个能回答问题、接受反馈、随时调整订单的服务员交谈。

启动一个交互式会话：

```bash
copilot
```

正如你目前所看到的，你会看到一个提示符，可以在那里自然地输入。要查看可用命令的帮助，只需输入：

```
> /help
```

**关键洞察**：Interactive 模式会保持上下文。每条消息都建立在前面的内容之上，就像真实的对话一样。

#### Interactive 模式示例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

注意每个提示词是如何建立在前一个回答之上的。你正在进行对话，而不是每次都从头开始。

---

### 模式 2：Plan 模式

<img src="../../../01-setup-and-first-steps/images/plan-mode.png" alt="Plan 模式 - 就像出行前用 GPS 规划路线" width="250"/>

**最适合**：复杂任务，你希望在执行前先审视一下方案。类似于出行前用 GPS 规划路线。

Plan 模式帮助你在编写任何代码之前先制定一个分步计划。使用 `/plan` 命令，按 **Shift+Tab** 切换进入 Plan 模式：

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **小技巧**：**Shift+Tab** 在以下模式之间循环切换：Interactive → Plan → Autopilot。在交互式会话中按下它即可切换模式，无需输入命令。

你也可以使用 `--plan` 标志直接以 Plan 模式启动 Copilot CLI：

```bash
copilot --plan
```

**Plan 模式输出：**（你的输出可能会有所不同）

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**关键洞察**：Plan 模式让你在编写任何代码之前都能审阅并修改方案。计划完成后，你甚至可以让 Copilot CLI 把它保存到一个文件中以备后用。例如，「Save this plan to `mark_as_read_plan.md`」会创建一个包含计划详情的 markdown 文件。

> 💡 **想试更复杂的？** 试试：`/plan Add search and filter capabilities to the book app`。Plan 模式可以从简单功能扩展到完整应用。

> 📚 **Autopilot 模式**：你可能已经注意到 Shift+Tab 会切换到第三种模式 **Autopilot**。在 autopilot 模式下，Copilot 会自动完成整个计划，每一步之后都不需要等待你的输入——就像把一个任务交给同事说「完成后告诉我」。典型的工作流是 plan → 接受 → autopilot，这意味着你需要先擅长写计划。你也可以用 `copilot --autopilot` 直接启动到 autopilot。先熟悉 Interactive 和 Plan 模式，准备好后再查看[官方文档](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)。

---

### 模式 3：Programmatic 模式

<img src="../../../01-setup-and-first-steps/images/programmatic-mode.png" alt="Programmatic 模式 - 就像使用得来速进行快速点单" width="250"/>

**最适合**：自动化、脚本、CI/CD、单次执行的命令。就像使用得来速进行快速点单，无需与服务员交谈。

使用 `-p` 标志执行不需要交互的一次性命令：

```bash
# Generate code
copilot -p "Write a function that checks if a number is even or odd"

# Get quick help
copilot -p "How do I read a JSON file in Python?"
```

**关键洞察**：Programmatic 模式给你一个快速的答案然后退出。没有对话，只有输入 → 输出。

<details>
<summary>📚 <strong>更进一步：在脚本中使用 Programmatic 模式</strong>（点击展开）</summary>

熟悉后，你可以在 shell 脚本中使用 `-p`：

```bash
#!/bin/bash

# Generate commit messages automatically
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Review a file
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **关于 `--allow-all`**：这个标志会跳过所有权限提示，让 Copilot CLI 在不询问的情况下读取文件、运行命令并访问 URL。这对 programmatic 模式（`-p`）是必需的，因为没有交互式会话来批准操作。只在你自己编写的提示词、并且在你信任的目录下使用 `--allow-all`。绝不要将其用于不可信的输入或敏感目录。

</details>

---

## 必备的斜杠命令

这些命令很适合在你刚开始使用 Copilot CLI 时学习：

| 命令 | 作用 | 何时使用 |
|---------|--------------|-------------|
| `/ask` | 提一个不影响对话历史的快速问题 | 当你想要一个快速答案而不打断当前任务时 |
| `/clear` | 清除对话并重新开始 | 切换话题时 |
| `/help` | 显示所有可用的命令 | 当你忘记某个命令时 |
| `/model` | 显示或切换 AI 模型 | 当你想更换 AI 模型时 |
| `/plan` | 在编码之前规划你的工作 | 用于更复杂的功能 |
| `/research` | 使用 GitHub 和网络资源进行深入研究 | 当你在编码前需要调研某个主题时 |
| `/exit` | 结束会话 | 当你完成时 |

> 💡 **`/ask` 与常规聊天的区别**：通常你发送的每条消息都会成为正在进行的对话的一部分，并影响后续的回复。`/ask` 是一个「不记录」的快捷方式——非常适合像 `/ask What does YAML mean?` 这样的快速一次性问题，不会污染你的会话上下文。

> 💡 **Tab 自动补全**：输入斜杠命令时，按 **Tab** 可以自动补全命令名，或在可用的子命令和参数之间循环。当你记不住命令的确切名称时尤其方便。

入门的部分就到这里！等你熟悉之后，可以再探索其他命令。

> 📚 **官方文档**：完整的命令和标志列表请见 [CLI command reference](https://docs.github.com/copilot/reference/cli-command-reference)。

<details>
<summary>📚 <strong>更多命令</strong>（点击展开）</summary>

> 💡 上面的必备命令涵盖了你日常使用的大部分场景。这份参考是供你准备好探索更多内容时使用的。

### Agent 环境

| 命令 | 作用 |
|---------|--------------|
| `/agent` | 浏览并从可用的 agent 中选择 |
| `/env` | 显示已加载的环境详情——哪些指令、MCP 服务器、skills、agents 和插件处于活动状态 |
| `/init` | 为你的仓库初始化 Copilot 指令 |
| `/mcp` | 管理 MCP 服务器配置 |
| `/skills` | 管理用于增强能力的 skills |

> 💡 Agents 在[第 04 章](../04-agents-custom-instructions/README.md)中介绍，skills 在[第 05 章](../05-skills/README.md)中介绍，MCP 服务器在[第 06 章](../06-mcp-servers/README.md)中介绍。

### 模型与子 agent

| 命令 | 作用 |
|---------|--------------|
| `/delegate` | 把任务交给 GitHub Copilot 云端 agent |
| `/fleet` | 把一个复杂任务拆分为并行子任务以更快完成 |
| `/model` | 显示或切换 AI 模型 |
| `/tasks` | 查看后台子 agent 和分离的 shell 会话 |

### 代码

| 命令 | 作用 |
|---------|--------------|
| `/diff` | 查看当前目录中所做的更改 |
| `/pr` | 对当前分支的 pull request 进行操作 |
| `/research` | 使用 GitHub 和网络资源进行深度研究调查 |
| `/review` | 运行 code-review agent 来分析改动 |
| `/terminal-setup` | 启用多行输入支持（shift+enter 和 ctrl+enter） |

### 权限

| 命令 | 作用 |
|---------|--------------|
| `/add-dir <directory>` | 把一个目录添加到允许列表 |
| `/allow-all [on\|off\|show]` | 自动批准所有权限提示；用 `on` 启用，`off` 禁用，`show` 查看当前状态 |
| `/yolo` | `/allow-all on` 的快捷别名——自动批准所有权限提示。 |
| `/cwd`, `/cd [directory]` | 查看或更改工作目录 |
| `/list-dirs` | 显示所有允许的目录 |

> ⚠️ **谨慎使用**：`/allow-all` 和 `/yolo` 会跳过确认提示。对受信任的项目很方便，但对不可信的代码要小心。

### 会话

| 命令 | 作用 |
|---------|--------------|
| `/clear` | 放弃当前会话（不保存历史）并开始一个新对话 |
| `/compact` | 总结对话以减少上下文占用 |
| `/context` | 显示上下文窗口的 token 使用情况和可视化 |
| `/keep-alive` | 在 Copilot CLI 处于活动状态时阻止系统进入睡眠——对在笔记本上运行长时间任务很方便 |
| `/new` | 结束当前会话（保存到历史以供搜索/恢复）并开始一个新对话。 |
| `/resume` | 切换到另一个会话（可选地指定会话 ID 或名称） |
| `/rename` | 重命名当前会话（省略名称即可自动生成一个） |
| `/rewind` | 打开时间线选择器以回滚到对话中较早的任意一个时间点 |
| `/usage` | 显示会话使用指标和统计信息 |
| `/session` | 显示会话信息和工作区摘要；使用 `/session delete`、`/session delete <id>` 或 `/session delete-all` 来移除会话 |
| `/share` | 把会话导出为 markdown 文件、GitHub gist 或自包含的 HTML 文件 |

### 显示

| 命令 | 作用 |
|---------|--------------|
| `/statusline`（或 `/footer`） | 自定义会话底部状态栏中显示的项目（目录、分支、effort、上下文窗口、配额） |
| `/theme` | 查看或设置终端主题 |

### 帮助与反馈

| 命令 | 作用 |
|---------|--------------|
| `/changelog` | 显示 CLI 版本的更新日志 |
| `/feedback` | 向 GitHub 提交反馈 |
| `/help` | 显示所有可用的命令 |

### 快速 shell 命令

通过以 `!` 为前缀，可以直接运行 shell 命令而不经过 AI：

```bash
copilot

> !git status
# Runs git status directly, bypassing the AI

> !python -m pytest tests/
# Runs pytest directly
```

### 切换模型

Copilot CLI 支持来自 OpenAI、Anthropic、Google 等的多个 AI 模型。你可以使用的模型取决于你的订阅级别和所在地区。使用 `/model` 查看你的选择并在它们之间切换：

```bash
copilot
> /model

# Shows available models and lets you pick one. Select Sonnet 4.5.
```

> 💡 **小技巧**：有些模型比其他模型消耗更多的「premium 请求」。标记为 **1x** 的模型（如 Claude Sonnet 4.5）是非常好的默认选择。它们既能干又高效。倍率更高的模型会更快地消耗你的 premium 请求配额，所以请把它们留给真正需要的时候。

> 💡 **不知道该选哪个模型？** 在模型选择器中选择 **`Auto`**，让 Copilot 为每个会话自动选择最佳的可用模型。如果你刚刚开始且不想费心选择模型，这是一个很好的默认选项。

</details>

---

# 实践

<img src="../../../images/practice.png" alt="温馨的工作桌面，显示器上是代码，台灯、咖啡杯和耳机已就位，准备开始动手实践" width="800"/>

是时候把你学到的内容付诸行动了。

---

## ▶️ 自己动手试试

### 交互式探索

启动 Copilot 并使用后续提示词来迭代地改进 book app：

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 规划一个功能

使用 `/plan` 让 Copilot CLI 在编写任何代码之前先规划好实现方式：

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Review the plan
# Approve or modify
# Watch it implement step by step
```

### 用 Programmatic 模式实现自动化

`-p` 标志让你可以直接从终端运行 Copilot CLI，而不必进入交互模式。从仓库根目录将下面的脚本复制粘贴到你的终端（不要在 Copilot 内部执行），以评审 book app 中的所有 Python 文件。

```bash
# Review all Python files in the book app
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell（Windows）：**

```powershell
# Review all Python files in the book app
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

完成演示后，再尝试这些变体：

1. **交互式挑战**：启动 `copilot` 并探索 book app。围绕 `@samples/book-app-project/books.py` 提问，并连续 3 次请求改进。

2. **Plan 模式挑战**：运行 `/plan Add rating and review features to the book app`。仔细阅读这个计划。它合理吗？

3. **Programmatic 挑战**：运行 `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`。它第一次运行就成功了吗？

---

## 💡 小技巧：从 Web 或手机控制你的 CLI 会话

GitHub Copilot CLI 支持**远程会话**，让你可以从 Web 浏览器（桌面或手机）或 GitHub Mobile app 监控并与正在运行的 CLI 会话交互，而无需亲自坐在终端前。

使用 `--remote` 标志启动一个远程会话：

```bash
copilot --remote
```

Copilot CLI 会显示一个链接并提供一个 QR 码。在你的手机上或桌面浏览器标签页中打开该链接，即可实时观看会话、发送后续提示词、审阅计划并远程引导 agent。会话是用户专属的，所以你只能访问自己的 Copilot CLI 会话。

你也可以在活动会话内随时启用远程访问：

```
> /remote
```

关于远程会话的更多详情可在 [Copilot CLI docs](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely) 中找到。

---

## 📝 作业

### 主挑战：改进 Book App 工具函数

实操示例聚焦于评审和重构 `book_app.py`。现在在另一个文件 `utils.py` 上练习相同的技能：

1. 启动一个交互式会话：`copilot`
2. 让 Copilot CLI 对该文件做摘要：「Summarize @samples/book-app-project/utils.py and explain what each function in this file does」
3. 让它添加输入校验：「Add validation to `get_user_choice()` so it handles empty input and non-numeric entries」
4. 让它改进错误处理：「What happens if `get_book_details()` receives an empty string for the title? Add guards for that.」
5. 请求添加 docstring：「Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values」
6. 观察上下文如何在提示词之间延续。每一次改进都建立在上一次的基础之上
7. 用 `/exit` 退出

**成功标准**：你应该得到一个改进后的 `utils.py`，包含输入校验、错误处理和一个 docstring，且全部通过多轮对话构建完成。

<details>
<summary>💡 提示（点击展开）</summary>

**可以尝试的示例提示词：**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**常见问题：**
- 如果 Copilot CLI 提出澄清性问题，自然地回答它们即可
- 上下文会向前延续，所以每个提示词都建立在前一个之上
- 想重新开始时使用 `/clear`

</details>

### 加分挑战：比较三种模式

示例中使用 `/plan` 处理搜索功能、使用 `-p` 进行批量评审。现在在同一个新任务上尝试全部三种模式：为 `BookCollection` 类添加一个 `list_by_year()` 方法：

1. **Interactive**：`copilot` → 让它一步步设计和实现该方法
2. **Plan**：`/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**：`copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**反思**：哪种模式感觉最自然？你会在什么时候使用每一种？

---

<details>
<summary>🔧 <strong>常见错误与故障排查</strong>（点击展开）</summary>

### 常见错误

| 错误 | 会发生什么 | 修复方法 |
|---------|--------------|-----|
| 输入 `exit` 而不是 `/exit` | Copilot CLI 会把「exit」当作一个提示词，而不是命令 | 斜杠命令始终以 `/` 开头 |
| 用 `-p` 进行多轮对话 | 每次 `-p` 调用都是孤立的，没有对前一次调用的记忆 | 对于建立在上下文之上的对话，使用交互模式（`copilot`） |
| 忘记给包含 `$` 或 `!` 的提示词加引号 | Shell 会在 Copilot CLI 看到之前先解释这些特殊字符 | 用引号包裹提示词：`copilot -p "What does $HOME mean?"` |
| 按一次 Esc 来取消正在运行的任务 | 单次 Esc 不再取消正在进行的工作（为防止误操作） | 在 Copilot CLI 处理时按 **两次 Esc** 来取消 |

### 故障排查

**「Model not available」** —— 你的订阅可能不包含所有模型。使用 `/model` 查看可用的模型。

**「Context too long」** —— 你的对话已经用满了上下文窗口。使用 `/clear` 重置，或开始一个新会话。

**「Rate limit exceeded」** —— 等几分钟后重试。可以考虑使用 programmatic 模式进行带延迟的批量操作。

</details>

---

# 总结

## 🔑 核心要点

1. **Interactive 模式**用于探索和迭代——上下文会向前延续。它就像和一个能记住你之前说过什么的人对话。
2. **Plan 模式**通常用于更复杂的任务。在实现之前先审阅。
3. **Programmatic 模式**用于自动化。无需交互。
4. **必备命令**（`/ask`、`/help`、`/clear`、`/plan`、`/research`、`/model`、`/exit`）涵盖了日常使用的大部分场景。

> 📋 **快速参考**：完整的命令和快捷键列表请见 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)。

---

## ➡️ 下一步

现在你已经理解了三种模式，让我们来学习如何向 Copilot CLI 提供关于你代码的上下文。

在 **[第 02 章：上下文与对话](../02-context-conversations/README.md)** 中，你将学习：

- 用于引用文件和目录的 `@` 语法
- 使用 `--resume` 和 `--continue` 进行会话管理
- 上下文管理如何让 Copilot CLI 真正变得强大

---

**[← 返回课程主页](../README.md)** | **[继续到第 02 章 →](../02-context-conversations/README.md)**
