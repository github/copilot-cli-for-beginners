# Additional Context Features

> 📖 **Prerequisite**: Complete [Chapter 02: Context and Conversations](../02-context-conversations/README.md) before reading this appendix.

This appendix covers two additional context features: working with images and managing permissions across multiple directories.

---

## Working with Images

You can include images in your conversations using the `@` syntax. Copilot can analyze screenshots, mockups, diagrams, and other visual content.

### Basic Image Reference

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analyzes the image and responds

> @mockup.png @current-design.png Compare these two designs

# You can also drag and drop images or paste from clipboard
```

### Supported Image Formats

| Format | Best For |
|--------|----------|
| PNG | Screenshots, UI mockups, diagrams |
| JPG/JPEG | Photos, complex images |
| GIF | Simple diagrams (first frame only) |
| WebP | Web screenshots |

### Practical Image Use Cases

**1. UI Debugging**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. Design Implementation**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. Error Analysis**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. Architecture Review**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. Before/After Comparison**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### Combining Images with Code

Images become even more powerful when combined with code context:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### Image Tips

- **Crop screenshots** to show only relevant portions (saves context tokens)
- **Use high contrast** for UI elements you want analyzed
- **Annotate if needed** - circle or highlight problem areas before uploading
- **One image per concept** - multiple images work, but be focused

---

## Permission Patterns

By default, Copilot can access files in your current directory. For files elsewhere, you need to grant access.

### Add Directories

```bash
# Add a directory to the allowed list
copilot --add-dir /path/to/other/project

# Add multiple directories
copilot --add-dir ~/workspace --add-dir /tmp
```

### Allow All Paths

```bash
# Disable path restrictions entirely (use with caution)
copilot --allow-all-paths
```

### Inside a Session

```bash
copilot

> /add-dir /path/to/other/project
# Now you can reference files from that directory

> /list-dirs
# See all allowed directories
```

### For Automation

```bash
# Allow all permissions for non-interactive scripts
copilot -p "Review @src/" --allow-all

# Or use the memorable alias
copilot -p "Review @src/" --yolo
```

### When You Need Multi-Directory Access

Common scenarios where you'll need these permissions:

1. **Monorepo work** - Comparing code across packages
2. **Cross-project refactoring** - Updating shared libraries
3. **Documentation projects** - Referencing multiple codebases
4. **Migration work** - Comparing old and new implementations

---

**[← Back to Chapter 02](../02-context-conversations/README.md)** | **[Return to Appendices](README.md)**
