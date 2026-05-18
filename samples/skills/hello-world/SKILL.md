---
name: hello-world
description: "Verify skills setup and demonstrate SKILL.md format - use when testing skills configuration, validating skill loading, creating a new skill template, or asking how skills work"
---

# Hello World Skill

Confirm that the skills system is loaded and working by producing a structured diagnostic response.

## Instructions

When the user asks to test skills, verify their setup, or mentions "hello world skill":

1. Confirm the skill loaded successfully
2. Show which skill file was matched
3. Provide a quick next-step suggestion

## Response Format

```
✅ Skills are working!

Skill loaded: hello-world
Source: .github/skills/hello-world/SKILL.md

Your skills setup is configured correctly. Try creating your own
skill by adding a new folder under .github/skills/ with a SKILL.md file.
```

## Example Prompts

- "Test my skills setup"
- "Use the hello world skill"
- "Are my skills working?"
- "Show me the skill file format"
