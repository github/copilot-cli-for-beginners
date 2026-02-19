# Buggy Code Samples

This folder contains intentionally buggy code for practicing code review and debugging with GitHub Copilot CLI.

## Folder Structure

```
buggy-code/
├── js/                    # JavaScript examples
│   ├── userService.js     # User management with 8 bugs
│   └── paymentProcessor.js # Payment handling with 8 bugs
└── python/                # Python examples
    ├── user_service.py    # User management with 10 bugs
    └── payment_processor.py # Payment handling with 12 bugs
```

## Quick Start

### JavaScript

```bash
copilot

# Security audit
> Review @samples/buggy-code/js/userService.js for security issues

# Find all bugs
> Find all bugs in @samples/buggy-code/js/paymentProcessor.js
```

### Python

```bash
copilot

# Security audit
> Review @samples/buggy-code/python/user_service.py for security issues

# Find all bugs
> Find all bugs in @samples/buggy-code/python/payment_processor.py
```

## Bug Categories

### Common to Both Languages

| Bug Type | Description |
|----------|-------------|
| SQL Injection | User input directly in SQL queries |
| Hardcoded Secrets | API keys and passwords in source code |
| Race Conditions | Shared state without proper synchronization |
| Sensitive Data Logging | Passwords and card numbers in logs |
| Missing Input Validation | No checks on user-provided data |
| No Error Handling | Missing try/catch or try/except blocks |
| Weak Password Comparison | Plain text or timing-vulnerable comparisons |
| Missing Auth Checks | Operations without authorization verification |

### Python-Specific Bugs

| Bug Type | Description |
|----------|-------------|
| Pickle Deserialization | `pickle.loads()` on untrusted data |
| eval() Injection | User input passed to `eval()` |
| Unsafe YAML Loading | `yaml.load()` without safe loader |
| Shell Injection | User input in `os.system()` calls |
| Weak Hashing | MD5 for password hashing |
| Insecure Random | `random` module for security purposes |

## Practice Exercises

1. **Security Audit**: Run a comprehensive security review and list all vulnerabilities by severity
2. **Fix One Bug**: Pick a critical bug, get the fix from Copilot, understand why it works
3. **Generate Tests**: Create tests that would catch these bugs before deployment
4. **Refactor Safely**: Fix the SQL injection bugs while maintaining functionality
