# Sample Source Code

This folder contains sample source files used in the course examples, particularly in Chapter 02 (Context and Conversations). These are only samples and not intended to be a full running application.

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
└── index.js       # App entry point
```

## Usage

These files are referenced in course examples using the `@` syntax:

```bash
copilot

> Explain what @samples/src/utils/helpers.js does
> Review @samples/src/api/ for security issues
> Compare @samples/src/auth/login.js and @samples/src/auth/register.js
```

## Notes

- Files contain intentional TODOs and minor issues for Copilot to find during reviews
- This is demo code that's not designed to actually run. NOT production-ready
- Used for learning the `@` file reference syntax
