---
description: PEP 8 準拠と型ヒントの規約
applyTo: "samples/**/*.py"
---

# Python スタイルガイド

このプロジェクトの Python コードは以下の規約に従ってください。

## インポート

- ファイル先頭に `from __future__ import annotations` を記述する
- 標準ライブラリ → サードパーティ → ローカルの順でグループ化する
- 各グループ間は空行で区切る

```python
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
```

## 型ヒント

- すべての関数に引数の型と戻り値の型を注釈する
- モダンな構文を使用する: `list[Book]`（`List[Book]` ではなく）
- Union 型は `|` 演算子を使用する: `Book | None`（`Optional[Book]` ではなく）

```python
def find_by_title(self, title: str) -> Book | None:
```

## 命名規約

- 定数: `UPPER_SNAKE_CASE`（例: `DATA_FILE`）
- クラス: `PascalCase`（例: `BookCollection`）
- 関数・メソッド: `snake_case`（例: `add_book`）
- プライベートメソッド: `_` プレフィックス（例: `_read_json`）
- 例外クラス: `<Domain>Error` パターン（例: `BookValidationError`）

## ドキュメンテーション

- Google スタイルの docstring を使用する
- `Args:`, `Returns:`, `Raises:` セクションを含める
- パブリックメソッドには `Example:` セクション（doctest 形式）を含める

```python
def add_book(self, title: str, author: str, year: int) -> Book:
    """Add a new book to the collection and persist the change.

    Args:
        title: The book's title. Must not be empty.
        author: The author's name. Must not be empty.
        year: The publication year.

    Returns:
        The newly created Book instance.

    Raises:
        BookValidationError: If validation fails.

    Example:
        >>> collection.add_book("1984", "George Orwell", 1949)
    """
```

## データモデル

- データクラスには `@dataclass` デコレータを使用する
- 例外は専用の基底クラスから継承する階層にする
