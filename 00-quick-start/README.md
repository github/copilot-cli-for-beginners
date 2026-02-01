# Chapter 00: Quick Start

Welcome! In this chapter, you'll get GitHub Copilot CLI (Command Line Interface) installed, authenticated with your GitHub account, and verified that everything works. This is a quick setup chapter. Once you're up and running, the real demos start in Chapter 01!

## Learning Objectives

By the end of this chapter, you'll have:

- Installed GitHub Copilot CLI
- Authenticated with your GitHub account
- Verified it works with a simple test

---

## Prerequisites

- **GitHub Account** with Copilot access
  - Students/Teachers: [Free via GitHub Education](https://education.github.com/pack)
  - Everyone else: [$10/month or $100/year](https://github.com/features/copilot)
- **Terminal/Command line** basics (cd, ls, etc.)
- **Node.js v18+** (only required if using npm installation method - not needed for Homebrew, WinGet, or install script)

### What "Copilot Access" Means

GitHub Copilot CLI requires an active Copilot subscription. You can check your status at [github.com/settings/copilot](https://github.com/settings/copilot). You should see one of:

- **Copilot Individual** - Personal subscription ($10/month)
- **Copilot Business** - Through your organization
- **Copilot Enterprise** - Through your enterprise
- **GitHub Education** - Free for verified students/teachers

If you see "You don't have access to GitHub Copilot," you'll need to subscribe or join an organization that provides access.

---

## Installation

> ⏱️ **Time estimate**: Installation takes 2-5 minutes. Authentication adds another 1-2 minutes.

> 🚀 **Want zero setup?** Use [GitHub Codespaces](https://github.com/codespaces) - Copilot CLI is pre-installed! Just open any repository in a Codespace and run `copilot` to start.

Choose the method that works for your system:

### All Platforms (npm)

```bash
npm install -g @github/copilot
```

### macOS/Linux (Homebrew)

```bash
brew install copilot-cli
```

### Windows (WinGet)

```bash
winget install GitHub.Copilot
```

### macOS/Linux (Install Script)

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

### GitHub Codespaces

If you're using GitHub Codespaces, **Copilot CLI is already installed** in the default image. Just run `copilot` to get started.

---

## Authentication

Start the CLI and log in:

```bash
copilot
> /login
```

**What happens next:**

1. Copilot displays a one-time code (like `ABCD-1234`)
2. Your browser opens to GitHub's device authorization page
3. Enter the code when prompted
4. Click "Authorize" to grant Copilot CLI access
5. Return to your terminal - you're now logged in!

**Tip**: The login persists across sessions. You only need to do this once unless your token expires or you explicitly log out.

---

## Verify It Works

Run this simple test:

```bash
copilot -p "Say hello and tell me what you can help with"
```

<details>
<summary>🎬 See it in action!</summary>

![Hello Demo](images/hello-demo.gif)

</details>

**Expected output**: A friendly response listing Copilot's capabilities.

If you see an error, check the [troubleshooting section](#troubleshooting) below.

---

## ✅ You're Ready!

That's it for installation. The real fun starts in Chapter 01, where you'll:

- Watch AI find 8 security bugs in 5 seconds
- Learn three different ways to use Copilot
- Generate working code from plain English

**[Continue to Chapter 01: First Steps →](../01-setup-and-first-steps/README.md)**

---

## Troubleshooting

### "copilot: command not found"

The CLI isn't installed. Try a different installation method:

```bash
# If brew failed, try npm:
npm install -g @github/copilot

# Or the install script:
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. Verify you have a Copilot subscription at [github.com/settings/copilot](https://github.com/settings/copilot)
2. Check that your organization permits CLI access (if using a work account)

### "Authentication failed"

Re-authenticate:

```bash
copilot
> /login
```

### Browser doesn't open automatically

Manually visit [github.com/login/device](https://github.com/login/device) and enter the code shown in your terminal.

### Token expired

Tokens typically last 8 hours. Simply run `/login` again:

```bash
copilot
> /login
```

### Still stuck?

- Check the [GitHub Copilot CLI documentation](https://docs.github.com/en/copilot)
- Search [GitHub Issues](https://github.com/github/copilot-cli/issues)

---

## Key Takeaways

1. **Multiple installation methods** - Choose what works for your system (Homebrew, WinGet, npm, or install script)
2. **One-time authentication** - Login persists until token expires
3. **Quick verification** - Use `-p` flag for instant testing

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

**[Continue to Chapter 01: First Steps →](../01-setup-and-first-steps/README.md)**
