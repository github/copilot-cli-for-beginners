# 附加上下文功能

> 📖 **前置要求**: 阅读本附录前，请先完成 [第 02 章: 上下文与会话](../02-context-conversations/README.md)。

本附录介绍两个附加上下文能力: 使用图片，以及管理跨多个目录的权限。

---

## 使用图片

你可以通过 `@` 语法在会话中引入图片。Copilot 可以分析截图、设计稿、图表以及其他可视化内容。

### 基础图片引用

```bash
copilot

> @screenshot.png 这个 UI 里发生了什么？

# Copilot 会分析图片并回复

> @mockup.png @current-design.png 对比这两个设计

# 你也可以拖拽图片或从剪贴板粘贴
```

### 支持的图片格式

| 格式 | 最适用场景 |
|--------|----------|
| PNG | 截图、UI 设计稿、示意图 |
| JPG/JPEG | 照片、复杂图像 |
| GIF | 简单图示（仅第一帧） |
| WebP | 网页截图 |

### 图片实战场景

**1. UI 调试**
```bash
> @bug-screenshot.png 按钮没有正确对齐。可能是什么 CSS 导致的？
```

**2. 设计落地实现**
```bash
> @figma-export.png 按这个设计写出对应的 HTML 和 Tailwind CSS
```

**3. 报错分析**
```bash
> @error-screenshot.png 这个报错是什么意思？我该怎么修复？
```

**4. 架构评审**
```bash
> @whiteboard-diagram.png 把这个架构图转换成可放进文档的 Mermaid 图
```

**5. 前后版本对比**
```bash
> @before.png @after.png 这两个 UI 版本之间有什么变化？
```

### 图片与代码结合

当图片与代码上下文一起使用时，效果会更强:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> 截图里的 header 看起来不对。代码里是什么原因导致的？
```

### 图片使用建议

- **裁剪截图**: 仅保留相关区域（可节省上下文 token）
- **提高对比度**: 让你希望分析的 UI 元素更清晰
- **必要时标注**: 上传前可圈出或高亮问题区域
- **一图一概念**: 多图可用，但尽量保持聚焦

---

## 权限模式

默认情况下，Copilot 只能访问当前目录下的文件。若需访问其他位置的文件，你需要显式授权。

### 添加目录

```bash
# 将一个目录加入允许列表
copilot --add-dir /path/to/other/project

# 添加多个目录
copilot --add-dir ~/workspace --add-dir /tmp
```

### 允许所有路径

```bash
# 完全关闭路径限制（谨慎使用）
copilot --allow-all-paths
```

### 在会话内授权

```bash
copilot

> /add-dir /path/to/other/project
# 现在你可以引用该目录中的文件

> /list-dirs
# 查看所有已允许目录
```

### 用于自动化

```bash
# 为非交互脚本启用全部权限
copilot -p "Review @src/" --allow-all

# 或者使用更易记的别名
copilot -p "Review @src/" --yolo
```

### 何时需要多目录访问

以下是常见场景:

1. **Monorepo 开发** - 跨 package 对比代码
2. **跨项目重构** - 更新共享库
3. **文档工程** - 引用多个代码库
4. **迁移工作** - 对比旧实现与新实现

---

**[← 返回第 02 章](../02-context-conversations/README.md)** | **[返回附录](README.zh-CN.md)**
