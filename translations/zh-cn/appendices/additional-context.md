# 更多上下文功能

> 📖 **前置要求**：阅读本附录前请先完成[第 02 章：上下文与对话](../02-context-conversations/README.md)。

本附录介绍两个额外的上下文功能：处理图片，以及在多个目录之间管理权限。

---

## 处理图片

你可以使用 `@` 语法在对话中包含图片。Copilot 能分析截图、设计稿、示意图以及其他视觉内容。

### 基本图片引用

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analyzes the image and responds

> @mockup.png @current-design.png Compare these two designs

# You can also drag and drop images or paste from clipboard
```

### 支持的图片格式

| 格式 | 适合场景 |
|--------|----------|
| PNG | 截图、UI 设计稿、示意图 |
| JPG/JPEG | 照片、复杂图片 |
| GIF | 简单示意图（仅识别第一帧） |
| WebP | 网页截图 |

### 图片的实际用例

**1. UI 调试**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. 设计稿落地**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. 错误分析**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. 架构评审**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. 前后对比**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### 把图片和代码结合起来

把图片和代码上下文结合起来，会更加强大：

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### 图片使用小贴士

- **裁剪截图**，只保留相关部分（节省上下文 token）
- **使用高对比度**，让你想分析的 UI 元素更清晰
- **必要时加注释** —— 上传前圈出或高亮问题区域
- **一张图聚焦一个概念** —— 多张图也行，但要有重点

---

## 权限模式

默认情况下，Copilot 可以访问你当前目录中的文件。要访问其他位置的文件，需要授予权限。

### 添加目录

```bash
# Add a directory to the allowed list
copilot --add-dir /path/to/other/project

# Add multiple directories
copilot --add-dir ~/workspace --add-dir /tmp
```

### 允许所有路径

```bash
# Disable path restrictions entirely (use with caution)
copilot --allow-all-paths
```

### 在会话内部

```bash
copilot

> /add-dir /path/to/other/project
# Now you can reference files from that directory

> /list-dirs
# See all allowed directories

> /yolo
# Quick alias for /allow-all on — auto-approves all permission prompts
```

### 用于自动化

```bash
# Allow all permissions for non-interactive scripts
copilot -p "Review @src/" --allow-all

# Or use the memorable alias
copilot -p "Review @src/" --yolo
```

### 何时需要多目录访问

下面这些场景中你通常会需要这些权限：

1. **Monorepo 工作** —— 跨多个包对比代码
2. **跨项目重构** —— 更新共享库
3. **文档项目** —— 引用多个代码库
4. **迁移工作** —— 对比新旧实现

---

[**← 返回第 02 章**](../02-context-conversations/README.md) | [**返回附录目录**](README.md)
