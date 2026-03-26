# Book Collection App

蔵書を管理するPython CLIアプリです。
本の追加・削除・検索・既読管理ができます。

---

## 機能

* JSONファイルに書籍データを保存（タイトル、著者、出版年、既読状態）
* すべてのコマンドで入力バリデーション
* 著者名や出版年範囲での検索
* 既読マーク機能

---

## ファイル

* `book_app.py` - メインCLIエントリーポイント
* `books.py` - BookCollectionクラス（データロジック）
* `utils.py` - UI・入力用ヘルパー関数
* `data.json` - サンプル書籍データ
* `tests/test_books.py` - BookCollectionのユニットテスト
* `test_book_app.py` - CLIハンドラーのユニットテスト

---

## アプリの実行

```bash
python book_app.py list
python book_app.py add
python book_app.py remove
python book_app.py find
python book_app.py find-title
python book_app.py mark-read
python book_app.py search-year
python book_app.py help
```

## テストの実行

```bash
python -m pytest
```

---

## 注意

* GitHub Copilot CLIコースの教材用サンプルです
* 学習目的のためシンプルな構成にしています
