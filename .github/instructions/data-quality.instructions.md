---
description: JSON データエントリのバリデーション規約
applyTo: "samples/**/data.json"
---

# データ品質ガイドライン

`data.json` の書籍エントリは以下のバリデーション規約に従ってください。

## 必須フィールド

すべてのエントリに以下の4フィールドが必要です：

| フィールド | 型 | 制約 |
|---|---|---|
| `title` | string | 空文字・空白のみは不可 |
| `author` | string | 空文字・空白のみは不可 |
| `year` | number (整数) | `0 ≤ year ≤ 現在年 + 1` |
| `read` | boolean | `true` または `false` |

## 有効なエントリの例

```json
{
  "title": "1984",
  "author": "George Orwell",
  "year": 1949,
  "read": true
}
```

## 無効なエントリの例

```json
// ❌ 著者が空
{ "title": "Unknown Book", "author": "", "year": 2020, "read": false }

// ❌ 年が負数
{ "title": "Bad Year", "author": "Author", "year": -1, "read": false }

// ❌ 年が未来すぎる（現在年+1 を超える）
{ "title": "Future Book", "author": "Author", "year": 2099, "read": false }

// ❌ 必須フィールド（read）が欠落
{ "title": "No Status", "author": "Author", "year": 2020 }
```

## バリデーションチェックリスト

データファイルを編集・作成する際に確認すること：

- [ ] すべてのエントリに `title`, `author`, `year`, `read` の4フィールドがある
- [ ] `title` と `author` が空文字でない
- [ ] `year` が 0 以上かつ来年以下の整数である
- [ ] `read` が `true` または `false`（文字列ではなく boolean）である
- [ ] 同一タイトルの重複エントリがない
- [ ] ファイル全体が有効な JSON 配列 `[...]` である
