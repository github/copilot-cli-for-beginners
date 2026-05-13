![面向初学者的 GitHub Copilot CLI](../../images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [你将学到什么](#-你将学到什么) &ensp; ✅ [先决条件](#-先决条件) &ensp; 🤖 [Copilot 家族](#-了解-github-copilot-家族) &ensp; 📚 [课程结构](#-课程结构) &ensp; 📋 [命令参考](#-github-copilot-cli-命令参考)

# 面向初学者的 GitHub Copilot CLI

> **✨ 学习如何借助 AI 驱动的命令行助手，为你的开发工作流提速。**

GitHub Copilot CLI 把 AI 助手直接带到你的终端中。无需切换到浏览器或代码编辑器，你就可以提出问题、生成功能完整的应用、审查代码、生成测试，并在不离开命令行的情况下调试问题。

把它想象成一位 24/7 随时在线的资深同事——可以阅读你的代码、解释那些让人困惑的写法，并帮助你更高效地工作！

> 📘 **更喜欢网页体验？** 你可以直接在 GitHub 上学习这门课程，也可以在 [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) 上以更传统的浏览方式查看。

本课程适合：

- **软件开发者**：希望从命令行使用 AI 的人
- **终端用户**：相比 IDE 集成，更喜欢以键盘驱动的工作流
- **希望统一规范的团队**：希望在团队范围内标准化 AI 辅助代码审查与开发实践

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="../../images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - 参加或主办一场活动" width="100%" />
  </picture>
</a>

## 🎯 你将学到什么

这门动手实践课程会带你从零基础成长为可以高效使用 GitHub Copilot CLI 的开发者。在所有章节中，你都会围绕同一个 Python 图书收藏应用进行练习，并通过 AI 辅助的工作流逐步改进它。学完之后，你就能从容地用 AI 来审查代码、生成测试、调试问题以及自动化工作流——这一切都在你的终端里完成。

**无需任何 AI 经验。** 只要你会用终端，就能学会。

**适合人群：** 开发者、学生，以及任何具备软件开发经验的人。

## ✅ 先决条件

开始之前，请确保你已具备：

- **GitHub 账号**：[免费注册一个](https://github.com/signup)<br>
- **GitHub Copilot 访问权限**：[免费方案](https://github.com/features/copilot/plans)、[按月订阅](https://github.com/features/copilot/plans)，或 [面向学生/教师免费](https://education.github.com/pack)<br>
- **终端基础**：能够熟练使用 `cd`、`ls` 等命令

## 🤖 了解 GitHub Copilot 家族

GitHub Copilot 已经发展成为一系列 AI 驱动的工具。下面是各个产品的运行场景：

| 产品 | 运行环境 | 描述 |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（本课程） | 你的终端 | 原生于终端的 AI 编码助手 |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains 等 | Agent 模式、聊天、行内补全 |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | 围绕你的仓库进行沉浸式聊天，创建 agent 等 |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | 把 issue 分配给 agent，由它返回 PR |

本课程聚焦于 **GitHub Copilot CLI**，让 AI 助手直接进入你的终端。

## 📚 课程结构

![GitHub Copilot CLI 学习路径](../../images/learning-path.png)

| 章节 | 标题 | 你将构建什么 |
|:-------:|-------|-------------------|
| 00 | 🚀 [快速开始](./00-quick-start/README.md) | 安装与验证 |
| 01 | 👋 [初步上手](./01-setup-and-first-steps/README.md) | 现场演示 + 三种交互模式 |
| 02 | 🔍 [上下文与对话](./02-context-conversations/README.md) | 多文件项目分析 |
| 03 | ⚡ [开发工作流](./03-development-workflows/README.md) | 代码审查、调试、测试生成 |
| 04 | 🤖 [打造专属的 AI 助手](./04-agents-custom-instructions/README.md) | 适配你工作流的自定义 agent |
| 05 | 🛠️ [自动化重复性任务](./05-skills/README.md) | 自动加载的 skill |
| 06 | 🔌 [连接 GitHub、数据库与 API](./06-mcp-servers/README.md) | MCP 服务器集成 |
| 07 | 🎯 [融会贯通](./07-putting-it-together/README.md) | 完整的功能开发工作流 |

## 📖 课程的学习方式

每一章都遵循相同的结构：

1. **现实世界类比**：通过熟悉的事物理解概念
2. **核心概念**：掌握必要的基础知识
3. **动手实践**：运行实际命令并查看结果
4. **课后作业**：练习所学内容
5. **下一步**：预告下一章的内容

**所有代码示例都是可运行的。** 课程中每一个 copilot 文本块都可以直接复制到你的终端运行。

## 📋 GitHub Copilot CLI 命令参考

[**GitHub Copilot CLI 命令参考文档**](https://docs.github.com/en/copilot/reference/cli-command-reference) 可以帮你查找命令和键盘快捷键，从而更高效地使用 Copilot CLI。

## 🌐 使用你的首选语言

本教程提供以下语言版本。

[English](../../README.md) | [Español](../es-es/README.md) | [日本語](../ja-jp/README.md) | [한국어](../ko-kr/README.md) | [Português](../pt-br/README.md) | [中文(简体)](./README.md)

## 🙋 获取帮助

- 🐛 **发现 Bug？** [提交 Issue](https://github.com/github/copilot-cli-for-beginners/issues)
- 📚 **官方文档：** [GitHub Copilot CLI 文档](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## 参与贡献

> **注意**：课程中使用的代码经过精心设计，会在审查、解释和调试场景中产生特定类型的输出，因此我们无法接受修改现有代码的 PR。

**如何贡献：**

1. Fork 本仓库并克隆到本地
2. 创建一个特性分支（`git checkout -b my-improvement`）
3. 进行你的修改
4. 提交一个 pull request

## 许可证

本项目基于 MIT 开源许可证授权。完整条款请参阅 [LICENSE](../../LICENSE) 文件。
