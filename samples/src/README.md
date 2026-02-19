# Sample Source Code (Legacy - Optional Reference)

> **Note**: The primary sample for this course is the **Python book collection app** in `../book-app-project/`. These JS/React files are from an earlier version of the course and are kept as optional extra reference material for learners who want JS examples.

This folder contains sample source files. These are only samples and not intended to be a full running application.

## Structure

```
src/
├── api/           # API route handlers
│   ├── auth.js    # Authentication endpoints
│   └── users.js   # User CRUD endpoints
├── auth/          # Client-side auth handlers
│   ├── login.js   # Login form logic
│   └── register.js # Registration form logic
├── components/    # React components
│   ├── Button.jsx # Reusable button
│   └── Header.jsx # App header with nav
├── models/        # Data models
│   └── User.js    # User model
├── services/      # Business logic
│   ├── productService.js
│   └── userService.js
├── utils/         # Helper functions
│   └── helpers.js
├── index.js       # App entry point
└── refactor-me.js # Beginner refactoring practice (Chapter 03)
```

## Usage

These files are referenced in course examples using the `@` syntax:

```bash
copilot

> Explain what @samples/src/utils/helpers.js does
> Review @samples/src/api/ for security issues
> Compare @samples/src/auth/login.js and @samples/src/auth/register.js
```

## Refactoring Practice

The `refactor-me.js` file is specifically designed for Chapter 03's refactoring exercises:

```bash
copilot

> @samples/src/refactor-me.js Rename the variable 'x' to something more descriptive
> @samples/src/refactor-me.js This function is too long. Split it into smaller functions.
> @samples/src/refactor-me.js Remove any unused variables
```

## Notes

- Files contain intentional TODOs and minor issues for Copilot to find during reviews
- This is demo code that's not designed to actually run. NOT production-ready
- Used for learning the `@` file reference syntax
