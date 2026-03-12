![第 00 章：快速开始](images/chapter-header.png)

欢迎！在本章中，你将安装 GitHub Copilot CLI（命令行界面），用你的 GitHub 账号登录，并确认一切可以正常运行。这是一个快速配置章节。准备完成后，真正的演示会从第 01 章开始。

## 🎯 学习目标

完成本章后，你将能够：

- 安装 GitHub Copilot CLI
- 使用你的 GitHub 账号登录
- 通过一个简单测试确认它可以正常工作

> ⏱️ **预计用时**：约 10 分钟（阅读 5 分钟 + 动手 5 分钟）

---

## ✅ 前置条件

- **具备 Copilot 访问权限的 GitHub 账号**。[查看订阅选项](https://github.com/features/copilot/plans)。学生和教师可通过 [GitHub Education](https://education.github.com/pack) 免费使用 Copilot Pro。
- **终端基础**：熟悉 `cd` 和 `ls` 这类命令

### “Copilot 访问权限”是什么意思

GitHub Copilot CLI 需要有效的 Copilot 订阅。你可以在 [github.com/settings/copilot](https://github.com/settings/copilot) 查看自己的状态。你应该会看到以下其中一种：

- **Copilot Individual** - 个人订阅
- **Copilot Business** - 通过组织提供
- **Copilot Enterprise** - 通过企业提供
- **GitHub Education** - 面向已验证学生/教师的免费资格

如果你看到 “You don't have access to GitHub Copilot”，那就需要使用免费选项、订阅某个方案，或者加入一个提供访问权限的组织。

---

## Installation

> ⏱️ **Time estimate**: Installation takes 2-5 minutes. Authentication adds another 1-2 minutes.

### 推荐：GitHub Codespaces（零配置）

如果你不想安装任何前置依赖，可以使用 GitHub Codespaces。它已经准备好了 GitHub Copilot CLI（你仍然需要登录），并预装了 Python 3.13、pytest 和 GitHub CLI。

1. [Fork this repository](https://github.com/github/copilot-cli-for-beginners/fork) to your GitHub account
2. Select **Code** > **Codespaces** > **Create codespace on main**
3. Wait a few minutes for the container to build
4. You're ready to go! The terminal will open automatically in the Codespace environment.

> 💡 **Verify in Codespace**: Run `cd samples/book-app-project && python book_app.py help` to confirm Python and the sample app are working.

### 备选：本地安装

> 💡 **不确定该选哪个？** 如果你已经安装了 Node.js，就用 `npm`。否则选择最适合你系统的方式。

> 💡 **演示需要 Python**：课程使用了一个 Python 示例应用。如果你是在本地操作，请在开始演示前先安装 [Python 3.10+](https://www.python.org/downloads/)。

> **注意：** 虽然课程中的主要示例使用 Python（`samples/book-app-project`），但如果你更习惯 JavaScript（`samples/book-app-project-js`）或 C#（`samples/book-app-project-cs`），也提供了相应版本。每个示例都带有 README，说明如何在对应语言中运行应用。

选择适合你系统的方法：

### All Platforms (npm)

```bash
# If you have Node.js installed, this is a quick way to get the CLI
npm install -g @github/copilot
```

### macOS/Linux (Homebrew)

```bash
brew install copilot-cli
```

### Windows (WinGet)

```bash
winget install GitHub.Copilot
```

### macOS/Linux (Install Script)

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

---

## Authentication

在 `copilot-cli-for-beginners` 仓库根目录打开一个终端窗口，启动 CLI，并允许它访问当前文件夹。

```bash
copilot
```

系统会提示你信任包含该仓库的文件夹（如果之前还没有信任过）。你可以选择只信任这一次，或者让之后的所有会话都默认信任。

<img src="images/copilot-trust.png" alt="在 Copilot CLI 中信任文件夹内的文件" width="800"/>

信任文件夹后，就可以使用 GitHub 账号登录了。

```
> /login
```

**接下来会发生什么：**

1. Copilot CLI 会显示一个一次性代码（例如 `ABCD-1234`）
2. 浏览器会打开 GitHub 的设备授权页面。如果你还没有登录 GitHub，需要先登录。
3. 按提示输入该代码
4. 选择 “Authorize”，为 GitHub Copilot CLI 授权
5. 回到终端，此时你已经登录完成

<img src="images/auth-device-flow.png" alt="设备授权流程，展示从终端登录到确认登录的 5 个步骤" width="800"/>

*设备授权流程：终端生成代码，你在浏览器中完成验证，Copilot CLI 随后通过认证。*

**提示**：登录状态会在多个会话之间持续保留。除非令牌过期，或者你主动登出，否则通常只需要操作一次。

---

## Verify It Works

### Step 1: Test Copilot CLI

现在你已经登录了，接下来确认 Copilot CLI 是否真的可用。如果 CLI 还没启动，就在终端中启动它：

```bash
> Say hello and tell me what you can help with
```

收到响应后，你可以退出 CLI：

```bash
> /exit
```

---

<details>
<summary>🎬 See it in action!</summary>

![Hello Demo](images/hello-demo.gif)

*Demo output varies. Your model, tools, and responses will differ from what's shown here.*

</details>

---

**预期输出**：一段友好的响应，列出 Copilot CLI 能提供哪些帮助。

### Step 2: Run the Sample Book App

课程提供了一个示例应用，你会在整门课程中使用 CLI 去探索和改进它。*（对应代码位于 /samples/book-app-project）* 在开始之前，先确认这个 *Python 图书收藏终端应用* 能正常运行。根据你的系统使用 `python` 或 `python3`。

> **注意：** 虽然课程中的主要示例使用 Python（`samples/book-app-project`），但如果你更习惯 JavaScript（`samples/book-app-project-js`）或 C#（`samples/book-app-project-cs`），也提供了相应版本。每个示例都带有 README，说明如何在对应语言中运行应用。

```bash
cd samples/book-app-project
python book_app.py list
```

**预期输出**：列出 5 本书，其中包括 “The Hobbit”、“1984” 和 “Dune”。

### Step 3: Try Copilot CLI with the Book App

如果你执行了步骤 2，请先返回仓库根目录：

```bash
cd ../..   # Back to the repository root if needed
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**预期输出**：对这个图书应用主要功能和命令的简要总结。

如果看到错误，请查看下面的 [troubleshooting section](#troubleshooting)。

完成后，你可以退出 Copilot CLI：

```bash
> /exit
```

---

## ✅ 你已经准备好了！

安装部分到这里就完成了。真正有意思的内容会在第 01 章开始，在那里你会：

- 看到 AI 立即审查图书应用并找出代码质量问题
- 学会使用 Copilot CLI 的三种不同方式
- 从自然语言直接生成可运行的代码

**[继续阅读第 01 章：First Steps →](../01-setup-and-first-steps/README.zh-CN.md)**

---

## Troubleshooting

### "copilot: command not found"

说明 CLI 还没有安装成功。尝试其他安装方式：

```bash
# If brew failed, try npm:
npm install -g @github/copilot

# Or the install script:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. 在 [github.com/settings/copilot](https://github.com/settings/copilot) 确认你确实拥有 Copilot 订阅
2. 如果你使用的是工作账号，检查你的组织是否允许 CLI 访问

### "Authentication failed"

重新进行认证：

```bash
copilot
> /login
```

### 浏览器没有自动打开

手动访问 [github.com/login/device](https://github.com/login/device)，然后输入终端中显示的代码。

### Token expired

只需要再次运行 `/login`：

```bash
copilot
> /login
```

### 还是卡住了？

- 查看 [GitHub Copilot CLI documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- 搜索 [GitHub Issues](https://github.com/github/copilot-cli/issues)

---

## 🔑 关键要点

1. **GitHub Codespaces 是一种很快的起步方式**：Python、pytest 和 GitHub Copilot CLI 都已预装好，可以直接进入演示环节
2. **安装方式不止一种**：选择适合你系统的方式（Homebrew、WinGet、npm 或安装脚本）
3. **认证通常只需一次**：登录状态会一直保留到令牌过期
4. **图书应用可以正常运行**：整门课程都会围绕 `samples/book-app-project` 展开

> 📚 **官方文档**：[Install Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) 了解安装选项和要求。

> 📋 **快速参考**：参见 [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference)，查看完整命令和快捷方式列表。

---

**[继续阅读第 01 章：First Steps →](../01-setup-and-first-steps/README.zh-CN.md)**
