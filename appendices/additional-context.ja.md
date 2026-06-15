<!--
---
id: CopilotCLI-Appendix-Additional-Context
title: 追加のコンテキスト機能
description: GitHub Copilot CLI における画像コンテキストの使用方法と、複数ディレクトリにまたがる権限管理について学びます。
audience: Developers / Students / Terminal users
slug: additional-context-features
weight: 92
---
-->

# 追加のコンテキスト機能

> 📖 **前提条件**: この付録を読む前に、[第02章：コンテキストと対話](../02-context-conversations/README.ja.md) を完了してください。

この付録では、画像の扱いと複数ディレクトリにまたがるアクセス許可の管理という、2つの追加コンテキスト機能を解説します。

---

## 画像の扱い

`@` 構文を使って、会話に画像を含めることができます。Copilot はスクリーンショット、モックアップ、図表、その他の視覚的コンテンツを分析できます。

### 基本的な画像参照

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot が画像を分析して回答します

> @mockup.png @current-design.png Compare these two designs

# ドラッグ＆ドロップやクリップボードからの貼り付けも可能です
```

### サポートされる画像フォーマット

| フォーマット | 最適な用途 |
|--------|----------|
| PNG | スクリーンショット、UI モックアップ、図表 |
| JPG/JPEG | 写真、複雑な画像 |
| GIF | シンプルな図表（最初のフレームのみ） |
| WebP | Web スクリーンショット |

### 実用的な画像使用例

**1. UI デバッグ**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. デザイン実装**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. エラー分析**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. アーキテクチャレビュー**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. 変更前後の比較**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### 画像とコードの組み合わせ

画像はコードのコンテキストと組み合わせるとさらに強力になります：

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### 画像に関するヒント

- **スクリーンショットをトリミング**して、関連部分のみを表示してください（コンテキストトークンを節約します）
- **高コントラスト**を使用して、分析したい UI 要素を際立たせてください
- **必要に応じて注釈を追加** — アップロード前に問題のある領域を丸で囲んだり強調したりしてください
- **1つの概念につき1枚の画像** — 複数の画像も可能ですが、焦点を絞ってください

---

## アクセス許可のパターン

デフォルトでは、Copilot は現在のディレクトリ内のファイルにアクセスできます。他の場所にあるファイルについては、アクセス許可を付与する必要があります。

### ディレクトリの追加

```bash
# 許可リストにディレクトリを追加
copilot --add-dir /path/to/other/project

# 複数のディレクトリを追加
copilot --add-dir ~/workspace --add-dir /tmp
```

### すべてのパスを許可

```bash
# パス制限を完全に無効化（注意して使用）
copilot --allow-all-paths
```

### セッション内での操作

```bash
copilot

> /add-dir /path/to/other/project
# そのディレクトリ内のファイルを参照できるようになります

> /list-dirs
# 許可されているすべてのディレクトリを表示

> /yolo
# /allow-all on のクイックエイリアス — すべての権限確認を自動承認
```

### 自動化のための設定

```bash
# 非対話型スクリプトですべての権限を許可
copilot -p "Review @src/" --allow-all

# または覚えやすいエイリアスを使用
copilot -p "Review @src/" --yolo
```

### 複数ディレクトリへのアクセスが必要な場面

以下のような場面でこれらの権限が必要になります：

1. **モノレポ作業** - パッケージ間でのコード比較
2. **プロジェクト横断的なリファクタリング** - 共有ライブラリの更新
3. **ドキュメントプロジェクト** - 複数のコードベースを参照
4. **移行作業** - 旧実装と新実装の比較

---

**[← 第02章に戻る](../02-context-conversations/README.ja.md)** | **[付録一覧に戻る](README.md)**
