---
name: "Traffic Updater"
description: "Weekly collection of repo traffic data (views and unique visitors). Appends the previous week's daily numbers to CSV files."
on:
  schedule: weekly on monday
  workflow_dispatch:
tools:
  bash: ["date"]
  edit:
  github:
    toolsets: [repos]
mcp-scripts:
  fetch-traffic:
    description: "Fetch the last 14 days of traffic views for this repository from the GitHub API. Returns JSON with a views array containing timestamp, count, and uniques per day."
    run: |
      gh api repos/$GITHUB_REPOSITORY/traffic/views
    env:
      GH_TOKEN: "${{ secrets.GH_AW_GITHUB_TOKEN }}"
      GITHUB_REPOSITORY: "${{ github.repository }}"
safe-outputs:
  allowed-domains:
    - github.com
  noop:
    report-as-issue: false
  create-pull-request:
    labels: [automated-update, traffic-data]
    title-prefix: "[bot] "
    base-branch: main
    fallback-as-issue: false
    protected-files: allowed
    allowed-files:
      - ".github/uvs.csv"
      - ".github/views.csv"
    github-token: ${{ secrets.GH_AW_GITHUB_TOKEN }}
---

# Collect Weekly Repo Traffic

You are a traffic collection bot for the **copilot-cli-for-beginners** repository. Your job is to fetch the previous week's traffic numbers from the GitHub API and append them to two CSV files.

## Definitions

- **Unique visitors** go in `.github/uvs.csv`
- **Total views** go in `.github/views.csv`
- Both files use the format `"MM/DD",count` — one line per day, no header row.
- The workflow can be triggered on any day. It always resumes from where the files left off.
- Every pull request must contain exactly seven consecutive, complete days of data.

## Step 1 — Determine the last recorded date

Read the last line of `.github/uvs.csv` (or `.github/views.csv` — they should be in sync). Parse the `"MM/DD"` date to determine the last day already recorded. Assume the current year for the date.

If both files are empty, treat the start date as 14 days ago (the maximum the GitHub API provides).

## Step 2 — Fetch traffic data

Call the `fetch-traffic` tool (no inputs needed). It returns JSON with a `views` array containing objects with `timestamp`, `count`, and `uniques` for each day in the last 14 days.

## Step 3 — Determine the next complete seven-day window

The next collection window starts on the calendar day immediately after the last recorded date and ends six days later.

Before editing either CSV file, verify all of the following:

1. The API response contains all seven dates in that window.
2. The seven dates are consecutive, with no missing or duplicate dates.
3. The final date in the window is before today's date, so every day is complete.

Do not substitute later dates for a missing date and do not create a partial-week pull request. GitHub's traffic API can occasionally lag by several days. If any validation fails, do not modify either file and stop with a no-op report that lists the dates still missing. A later scheduled or manual run will retry the same window.

Format the seven validated dates as `"MM/DD"` (zero-padded month and day, no year).

## Step 4 — Append the complete window

Append exactly seven new rows to the end of each file, keeping the existing data intact:

- **`.github/uvs.csv`** — append `"MM/DD",{uniques}` for each new day
- **`.github/views.csv`** — append `"MM/DD",{count}` for each new day

Rows must be in chronological order (earliest date first). Before creating the pull request, verify both files end with the same seven dates and that exactly seven rows were added to each file.

## Step 5 — Open a pull request

Create a pull request targeting the `main` branch. The PR title should summarize the date range, e.g.:

> Add traffic data for week of MM/DD – MM/DD

The PR body should include:

1. The date range collected
2. Total views and unique visitors for the week
3. A short table or list showing the daily breakdown
