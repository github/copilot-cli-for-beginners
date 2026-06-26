---
name: localizations
description: A skill that localizes contents into given locales.
---

# Localize contents into given locales

A skill that localizes contents into given locales.

## How it works

The skill takes input content and a list of target locales. It then translates the content into each specified locale, providing localized versions for each.

### Content structure

```text
.
├── README.md
├── 00-quick-start/
│   └── *.md
├── 01-setup-and-first-steps/
│   └── *.md
├── 02-context-conversations/
│   └── *.md
├── 03-development-workflows/
│   └── *.md
├── 04-agents-custom-instructions/
│   └── *.md
├── 05-skills/
│   └── *.md
├── 06-mcp-servers/
│   └── *.md
├── 07-putting-it-together/
│   └── *.md
└── appendices/
    └── *.md
```

### Input contents

Here are the list of contents for localization:

- `README.md`: The main documentation file for the project.
- All markdown files in the `00-*` directories and `appendices` directory **and its subdirectories** (`00-*/**/*.md`, `appendices/**/*.md`): The main content files for the project documentation.

Both `README.md`, the `00-*` directories, and the `appendices` directory are in scope. The **`00-*`** directories and `appendices` directory are the default locations for content files, but `README.md` at the project root is always included as well.

Files already under `translations/` are **outputs**, not inputs—never treat them as source content to be localized again.

### Target locales

Target locales are defined in the `rules` directory as markdown files in this skill (`rules/ko.md`, for example). **To determine which locales to process, list the files in `rules/`: each `<locale>.md` file corresponds to exactly one supported target locale.** Each locale has its own set of rules and guidelines for translation, ensuring that the localized content is appropriate for the target audience.

Locale identifiers use lowercase with a hyphen (for example, `ko` or `zh-cn`). This is the canonical casing for both the rules filename and the output directory in this skill; keep them consistent.

### Output contents

All the localized contents are stored in the `translations` directory, with each locale having its own subdirectory. For example, the localized content for Korean would be stored in `translations/ko/`.

It's assumed that the **`translations`** directory is the default location for all the localized content files.

## Localization process

There are three cases for localization. To detect which case applies, compare the **source tree** against the existing `translations/<locale>/` tree, and use the **git history of the source files** to detect changes:

- **Original exists, no localized version for the locale:** Create a new localized document.
- **Both original and localized versions exist:** Run `git diff` (or `git log`) on the **source** file to find what changed in the source since the localized version was last produced, then update only the affected sections of the localized document to match. Do not re-translate unchanged sections unnecessarily.
- **Localized version exists, but the original has been deleted:** Delete the orphaned localized document (and prune now-empty locale subdirectories).

The process runs in two passes. First, the content is analyzed to identify key phrases and context. Then the `translator` agent performs the initial localization, followed by a review-and-refinement pass by the `evaluator` agent to ensure quality and consistency.

> The `translator` and `evaluator` "agents" are **roles/personas**, not external tools. If no dedicated sub-agents are available, perform them as sequential personas: first adopt the translator role to produce the draft, then adopt the evaluator role to critique and refine that draft against the locale rules. Repeat the refinement loop until the evaluator's criteria pass.

### Markdown and formatting preservation

Regardless of locale, the following must be preserved exactly and **not** translated:

- YAML frontmatter **keys** (translate values only where appropriate, e.g. a `title`).
- Fenced and inline code, including variable, function, and command names.
- URLs, link targets, image paths, and heading anchors/slugs.
- HTML tags, Markdown structure, tables, and admonition markers.

Translate human-language prose, including comments inside code blocks where they are explanatory (per the locale rules). Keep heading structure and ordering stable so links and anchors continue to resolve.

### Translator agent

Use the `translator` agent to perform the localization. It should follow the rules and guidelines defined for each target locale document in the `rules` directory.

### Evaluator agent

Use the `evaluator` agent to assess the quality of the localized content. The evaluator checks for accuracy, cultural relevance, and overall quality, following the rules and guidelines defined for the target locale in the `rules` directory.

The evaluator scores the localized document against the locale's **Evaluator Scoring Rubric** (defined in the locale's `rules/<locale>.md`). The rubric uses two tiers: **Tier A** hard-fail criteria that must score 5, and **Tier B** graded criteria (1–5) that must score 4 or 5. A document passes only when **every applicable Tier A criterion scores 5 and every applicable Tier B criterion scores ≥ 4**. If anything falls short, return the document to the translator with specific notes and re-run the translate → evaluate loop until it passes, escalating to a human after the rubric's iteration cap.

## DOs and DON'Ts

- **Do** perform localization only for the target locales defined in the `rules` directory (one `<locale>.md` per supported locale). Do not localize into unsupported locales.
- **Do** preserve Markdown structure, code, links, image paths, heading anchors, and frontmatter keys exactly (see *Markdown and formatting preservation*).
- **Do** mirror the source directory layout under `translations/<locale>/`.
- **Don't** treat files under `translations/` as source input.
- **Don't** reorder or restructure content; keep headings and their order stable.
- **Don't** translate code, commands, or identifiers; translate explanatory prose and code comments only.

