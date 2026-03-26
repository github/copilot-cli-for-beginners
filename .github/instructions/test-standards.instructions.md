---
description: テストファイルでの pytest 規約
applyTo: "samples/**/test_*.py,samples/**/tests/**/*.py"
---

# テスト規約（pytest）

このプロジェクトのテストコードは以下の pytest 規約に従ってください。

## ファイル・関数の命名

- テストファイル: `test_<module>.py`
- テスト関数: `test_<feature>_<scenario>`（例: `test_add_book_empty_title`）
- テストクラス: `Test<Feature><Scenario>`（関連シナリオのグループ化用）

```python
class TestFindByAuthorPartialMatch:
    """Substring of the author name should still find matching books."""
```

## フィクスチャ

- `@pytest.fixture()` を使用し、説明的な名前をつける
- テストファイルの分離には `tmp_path` を使用する
- フィクスチャの連鎖で複雑なセットアップを構築する

```python
@pytest.fixture()
def collection(tmp_path):
    """Create a BookCollection with temporary storage."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    return BookCollection(data_file=str(temp_file))

@pytest.fixture()
def orwell_collection(collection):
    """Collection pre-loaded with two George Orwell books."""
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    return collection
```

## アサーション

- シンプルな `assert` 文を使用する（`self.assertEqual` ではなく）
- 例外テストには `pytest.raises` を `match` パラメータ付きで使用する
- 出力キャプチャには `capsys` フィクスチャを使用する

```python
def test_add_book_empty_title(collection):
    with pytest.raises(BookValidationError, match="Title cannot be empty"):
        collection.add_book("", "Author", 2020)
```

```python
def test_handle_add_output(mock_input, mock_collection, capsys):
    book_app.handle_add()
    output = capsys.readouterr().out
    assert "Book added successfully" in output
```

## モック

- `@patch()` デコレータで外部依存をモックする
- `side_effect` でユーザー入力をシミュレーションする
- `assert_called_once_with` で呼び出しを検証する

```python
@patch("book_app.collection")
@patch("builtins.input", side_effect=["The Hobbit", "Tolkien", "1937"])
def test_handle_add_valid_input(mock_input, mock_collection, capsys):
    book_app.handle_add()
    mock_collection.add_book.assert_called_once_with("The Hobbit", "Tolkien", 1937)
```

## テスト構成

- 論理セクションをコメントで区切る: `# --- Adding Books ---`
- 1テスト1アサーション（関連する検証はまとめてよい）
- テスト間の状態汚染を防ぐため `tmp_path` で分離する
