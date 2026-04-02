---
applyTo: "**/data.json"
---

# Data Quality Instructions

Apply these rules whenever reading, writing, or generating entries in `data.json`.

## Required Fields

Every entry must include all six fields:

| Field | Type | Rules |
|---|---|---|
| `title` | string | Non-empty, no leading/trailing whitespace |
| `author` | string | Non-empty, no leading/trailing whitespace |
| `year` | integer | 1000–2100, or `0` for unknown — never a string like `"1984"` |
| `read` | boolean | `true` or `false` — never a string, never `null` |
| `rating` | integer or null | `1`–`5` if `read` is `true`; must be `null` if `read` is `false` |
| `review` | string or null | Non-empty string if present; must be `null` if `read` is `false` |

## Valid Entry Example

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "year": 1965,
  "read": true,
  "rating": 4,
  "review": "Epic world-building and intricate politics. A dense but rewarding read."
}
```

## Common Mistakes to Avoid

- ❌ `"year": "1965"` — year must be a number, not a string
- ❌ `"read": "true"` — read must be a boolean, not a string
- ❌ `"rating": 0` or `"rating": 6` — rating must be 1–5
- ❌ `"rating": 4` when `"read": false` — unread books must have `null` rating
- ❌ `"author": ""` — author must be non-empty
- ❌ Missing any of the six fields — all fields are required, even if `null`

## When Generating New Entries

- Preserve the existing sort order or append to the end
- Use 2-space indentation (matches the existing file format)
- Keep the JSON array valid — no trailing commas

## When Validating Existing Entries

Flag any entry that:
1. Is missing one or more required fields
2. Has `author` or `title` as an empty string or whitespace-only
3. Has `year` outside 1–2100 (excluding `0`) or as a non-integer
4. Has `read` as anything other than `true` or `false`
5. Has a non-null `rating` when `read` is `false`
6. Has a `rating` outside the range 1–5
7. Has a non-null `review` when `read` is `false`
