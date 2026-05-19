# Toggle Notes

## Book Year Display Toggle

- Variable: `BOOK_APP_SHOW_YEAR`
- Scope: `samples/book-app-project/book_app.py`
- Default: enabled

## Behavior

- `BOOK_APP_SHOW_YEAR=1` keeps the year visible in `list` output.
- `BOOK_APP_SHOW_YEAR=0` hides the year from `list` output.
- Accepted false-like values: `0`, `false`, `off`, `no`

## Local Verification

Enabled:

```bash
cd samples/book-app-project
$env:BOOK_APP_SHOW_YEAR="1"
python book_app.py list
```

Disabled:

```bash
cd samples/book-app-project
$env:BOOK_APP_SHOW_YEAR="0"
python book_app.py list
```

This toggle only affects CLI display. It does not change stored book data.