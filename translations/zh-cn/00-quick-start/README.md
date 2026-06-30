![第 00 章：快速开始](../../../00-quick-start/images/chapter-header.png)

欢迎！在本章中，你将完成 GitHub Copilot CLI（命令行界面）的安装、使用 GitHub 账号登录，并验证一切是否正常工作。这是一个快速安装章节。一旦你准备就绪，真正的演示将从第 01 章开始！

## 🎯 学习目标

学完本章后，你将完成：

- 安装 GitHub Copilot CLI
- 使用 GitHub 账号登录
- 通过一个简单的测试验证它可以正常工作

> ⏱️ **预计耗时**：约 10 分钟（5 分钟阅读 + 5 分钟实操）

---

## ✅ 先决条件

- **GitHub 账号** 并具有 Copilot 访问权限。[查看订阅选项](https://github.com/features/copilot/plans)。学生/教师可通过 [GitHub Education 免费访问 Copilot Pro](https://education.github.com/pack)。
- **终端基础**：能够熟练使用 `cd`、`ls` 等命令

### 什么是“Copilot 访问权限”

GitHub Copilot CLI 需要一份有效的 Copilot 订阅。你可以在 [github.com/settings/copilot](https://github.com/settings/copilot) 查看你的状态。你应当看到以下其中之一：

- **Copilot Individual** —— 个人订阅
- **Copilot Business** —— 通过你所在的组织订阅
- **Copilot Enterprise** —— 通过你所在的企业订阅
- **GitHub Education** —— 面向通过验证的学生/教师免费

如果你看到“You don't have access to GitHub Copilot”，则需要使用免费方案、订阅一个套餐，或者加入一个为你提供访问权限的组织。

---

## 安装

> ⏱️ **预计耗时**：安装大约需要 2-5 分钟，认证再额外花费 1-2 分钟。

### GitHub Codespaces（无需任何配置）

如果你不想在本机安装任何先决条件，可以使用 GitHub Codespaces，其中已经为你准备好了 GitHub Copilot CLI（仍需登录），并预装了 Python 和 pytest。

1. [Fork 本仓库](https://github.com/github/copilot-cli-for-beginners/fork) 到你的 GitHub 账号
2. 选择 **Code** > **Codespaces** > **Create codespace on main**
3. 等待几分钟让容器构建完成
4. 万事俱备！终端会在 Codespace 环境中自动打开。

> 💡 **在 Codespace 中验证**：运行 `cd samples/book-app-project && python book_app.py help`，确认 Python 与示例应用都能正常工作。

### 本地安装

如果你想在本机运行 Copilot CLI 并使用课程示例，请按以下步骤操作。

1. 克隆仓库以获取课程示例：

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 选择以下任一方式安装 Copilot CLI。

    > 💡 **不知道选哪个？** 如果你已经安装了 Node.js，使用 `npm` 是最快的方式。否则，请选择适合你系统的安装方式。

    ### 全平台（npm）

    ```bash
    # If you have Node.js installed, this is a quick way to get the CLI
    npm install -g @github/copilot
    ```

    ### macOS/Linux（Homebrew）

    ```bash
    brew install copilot-cli
    ```

    ### Windows（WinGet）

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux（安装脚本）

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>可选：启用 shell tab 自动补全</summary>

Shell tab 自动补全可以让你按下 **Tab** 键来补全 `copilot` 子命令、命令选项以及部分选项的取值。这是可选项，但当你熟悉 CLI 后会非常方便。

Copilot CLI 目前支持 Bash、Zsh 和 Fish 的补全脚本：

```shell
# Bash, current session only
source <(copilot completion bash)

# Bash, persistent on Linux
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

添加持久化补全后，请重启你的 shell。在 Windows 上可以使用 PowerShell 来运行 Copilot CLI，但 `copilot completion` 目前仅支持 Bash、Zsh 和 Fish。

</details>

---

## 认证

在 `copilot-cli-for-beginners` 仓库根目录下打开一个终端窗口，启动 CLI 并允许它访问该文件夹。

```bash
copilot
```

如果你尚未授信，系统会询问你是否信任包含该仓库的文件夹。你可以选择仅本次信任，或者对今后所有会话都信任。

<img src="../../../00-quick-start/images/copilot-trust.png" alt="在 Copilot CLI 中信任文件夹中的文件" width="800"/>

信任文件夹后，你就可以使用 GitHub 账号登录。

```
> /login
```

**接下来会发生什么：**

1. Copilot CLI 会显示一个一次性验证码（如 `ABCD-1234`）
2. 浏览器会打开 GitHub 的设备授权页面。如果你尚未登录 GitHub，请先登录。
3. 在提示时输入该验证码
4. 选择 “Authorize” 以授予 GitHub Copilot CLI 访问权限
5. 返回终端——你已经成功登录！

<img src="../../../00-quick-start/images/auth-device-flow.png" alt="设备授权流程——展示从终端登录到完成登录确认的 5 个步骤" width="800"/>

*设备授权流程：终端生成验证码，你在浏览器中验证，Copilot CLI 即完成认证。*

**提示**：登录状态会跨会话保留。除非令牌过期或你显式登出，否则你只需要登录一次。

---

## 验证它是否可用

### 步骤 1：测试 Copilot CLI

既然你已经登录，让我们来验证 Copilot CLI 是否正常工作。在终端中，如果你尚未启动 CLI，请先启动它：

```bash
> Say hello and tell me what you can help with
```

收到响应后，你可以退出 CLI：

```bash
> /exit
```

---

<details>
<summary>🎬 看看实际效果！</summary>

![Hello 演示](../../../00-quick-start/images/hello-demo.gif)

*演示输出会有所不同。你的模型、工具和响应可能会与此处展示的内容不一样。*

</details>

---

**预期输出**：一个友好的回复，列出 Copilot CLI 的能力。

### 步骤 2：运行示例图书应用

本课程提供了一个示例应用，你将在整个课程中通过 CLI 不断探索并改进它（你可以在 /samples/book-app-project 中查看代码）。在开始之前，先确认这个 *Python 图书收藏终端应用* 能正常运行。请根据你的系统使用 `python` 或 `python3`。

> **注意：** 课程中展示的主要示例使用的是 Python（`samples/book-app-project`），因此如果你选择本地方式，需要确保本机已安装 [Python 3.10+](https://www.python.org/downloads/)（Codespace 已经预装好了）。如果你更习惯使用其他语言，也可以使用 JavaScript（`samples/book-app-project-js`）和 C#（`samples/book-app-project-cs`）版本。每个示例都附带一个 README，说明如何在对应语言中运行该应用。

```bash
cd samples/book-app-project
python book_app.py list
```

**预期输出**：列出 5 本书，包括 “The Hobbit”、“1984” 和 “Dune”。

### 步骤 3：在图书应用上试用 Copilot CLI

如果你刚执行完步骤 2，先回到仓库根目录：

```bash
cd ../..   # Back to the repository root if needed
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**预期输出**：一段对该图书应用主要函数与命令的总结。

如果出现错误，请查看下方的 [故障排查部分](#故障排查)。

完成后，你可以退出 Copilot CLI：

```bash
> /exit
```

---

## ✅ 你已准备就绪！

安装部分到此结束。真正的乐趣从第 01 章开始，在那里你将：

- 看着 AI 审查图书应用，瞬间发现代码质量问题
- 学习使用 Copilot CLI 的三种不同方式
- 用普通英语生成可运行的代码

[**继续学习第 01 章：初步上手 →**](../01-setup-and-first-steps/README.md)

---

## 故障排查

### “copilot: command not found”

CLI 尚未安装。换一种安装方式试试：

```bash
# If brew failed, try npm:
npm install -g @github/copilot

# Or the install script:
curl -fsSL https://gh.io/copilot-install | bash
```

### “You don't have access to GitHub Copilot”

1. 在 [github.com/settings/copilot](https://github.com/settings/copilot) 确认你拥有 Copilot 订阅
2. 如果使用工作账号，确认你所在的组织允许 CLI 访问

### “Authentication failed”

重新认证：

```bash
copilot
> /login
```

### 浏览器没有自动打开

手动访问 [github.com/login/device](https://github.com/login/device)，并输入终端中显示的验证码。

### 令牌过期

只需再次运行 `/login`：

```bash
copilot
> /login
```

### 仍然卡住？

- 查阅 [GitHub Copilot CLI 文档](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- 在 [GitHub Issues](https://github.com/github/copilot-cli/issues) 中搜索

---

## 🔑 关键要点

1. **GitHub Codespace 是快速上手的好方式** —— Python、pytest 和 GitHub Copilot CLI 都已预装好，你可以直接进入演示
2. **多种安装方式** —— 选择适合你系统的方式（Homebrew、WinGet、npm 或安装脚本）
3. **一次性认证** —— 登录会一直保留，直到令牌过期
4. **图书应用可以正常运行** —— 你将在整个课程中使用 `samples/book-app-project`

> 📚 **官方文档**：[安装 Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)，了解安装选项和系统要求。

> 📋 **快速参考**：参见 [GitHub Copilot CLI 命令参考文档](https://docs.github.com/en/copilot/reference/cli-command-reference)，获取完整的命令与快捷键列表。

---

[**继续学习第 01 章：初步上手 →**](../01-setup-and-first-steps/README.md)
