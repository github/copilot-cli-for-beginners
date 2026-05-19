# PR Hygiene Notes

## Review Focus

- Confirm the change stays within the intended exercise scope.
- Verify the evidence section matches the commands actually run.
- Check rollback is simple and limited to the touched files.

## Verification Steps

- Run the primary local check for the Python sample:

```bash
cd samples/book-app-project
python run_tests.py
```

- If the change affects runtime behavior, include one concrete manual command and its expected outcome.

## Rollback Guidance

- Prefer reverting the single exercise commit.
- If the exercise introduced a non-code artifact only, rollback is just removing that file.
- Avoid mixing unrelated cleanup into the same PR so rollback stays small.

## Commit Message Improvements

Use short imperative messages that name the exercise outcome clearly.

Examples:

- `crawl: ex11 add pr hygiene note`
- `crawl: ex10 add local test script`
- `crawl: ex13 add book list display toggle`

## PR Body Checklist

- Summary explains what changed and why.
- Review focus calls out the highest-risk part of the exercise.
- Evidence lists exact commands and a short result summary.
- Risk and rollback stay concrete and low-friction.