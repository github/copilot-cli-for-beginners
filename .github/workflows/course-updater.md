---
name: "Course Updater"
description: "Daily check for new GitHub Copilot CLI features and updates. Opens a PR if the course content needs updating."
on:
  schedule: daily
  workflow_dispatch:
tools:
  bash: ["curl", "gh"]
  edit:
  web-fetch:
  github:
    toolsets: [repos]
safe-outputs:
  allowed-domains:
    - github.com
  create-pull-request:
    labels: [automated-update, copilot-cli-updates]
    title-prefix: "[bot] "
    base-branch: main
---

# Check for Copilot CLI Updates

You are a documentation maintainer for the Copilot CLI for Beginners repository. Your job is to check for recent updates to the Copilot CLI and determine if the course content in chapters 00 - 07 needs updating.

## Step 1 — Gather recent Copilot CLI updates

Use `web-fetch` to read the following pages and extract the latest entries from the past 7 days:

- https://github.com/github/copilot-cli/blob/main/changelog.md — CLI changelog

Also use `gh` CLI to check the latest releases and commits in the `github/copilot-cli` repo.

Look for:

- New features or capabilities (e.g., new commands, tools, integrations)
- Significant changes to existing features (renames, deprecations)
- New customization options (e.g. instructions, agents, skills, MCP, plugins)

## Step 2 — Compare against the current course content and existing PRs

This course targets beginners so only include content changes that would cater to that audience. For example, if a new feature is advanced or doesn't qualify as a "beginner" level feature, it may not be necessary to include it in the course content since we don't want to overwhelm learners. Determine what is most relevant and helpful for beginners learning about the Copilot CLI.

Read all of the readme files in the repo and compare the features documented there against what you found in Step 1. Also check existing pull requests to see if any updates are already in progress. DO NOT duplicate efforts if an update has already been proposed in an open PR.
Identify:

- **Missing features** — new capabilities not yet documented
- **Outdated information** — features that have been renamed, deprecated, or significantly changed

If there is nothing new or everything is already up to date, stop here and report that no updates are needed. 

## Step 3 — Update the course content

If updates are needed, make a decision on which chapter(s) need to be updated.

If the new information can be added to existing chapter(s), edit those chapters to include refinements, new sections, or updated information as needed. Remember that this course targets beginners, so ensure that any new content is explained clearly and simply, with examples if possible.

## Step 4 — Open a pull request

Create a pull request with your changes, using the `main` branch as the base branch. The PR title should summarize what was updated (e.g., "Add /plan command documentation"). The PR body should list:

1. What new features or changes were found
2. What sections of the course were updated
3. Links to the source announcements

The PR should target the `main` branch and include the labels `automated-update` and `copilot-cli-updates`.