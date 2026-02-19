---
name: code-checklist
description: Team code quality checklist - use for checking Python code quality, bugs, security issues, and best practices
---

# Code Checklist Skill

Apply this checklist when checking Python code.

## Code Quality Checklist

- [ ] All functions have type hints
- [ ] No bare except clauses
- [ ] No mutable default arguments
- [ ] Context managers used for file I/O
- [ ] Functions are under 50 lines
- [ ] Variable and function names follow PEP 8 (snake_case)

## Input Validation Checklist

- [ ] User input is validated before processing
- [ ] Edge cases handled (empty strings, None, out-of-range values)
- [ ] Error messages are clear and helpful

## Testing Checklist

- [ ] New code has corresponding pytest tests
- [ ] Edge cases are covered
- [ ] Tests use descriptive names

## Output Format

Present findings as:

```
## Code Checklist: [filename]

### Code Quality
- [PASS/FAIL] Description of finding

### Input Validation
- [PASS/FAIL] Description of finding

### Testing
- [PASS/FAIL] Description of finding

### Summary
[X] items need attention before merge
```
