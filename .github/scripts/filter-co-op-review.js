#!/usr/bin/env node

// Runs `co-op-review` and post-filters its findings so the workflow only fails
// on genuine errors.
//
// Why this exists: the `translate` command and the `co-op-review` command ship
// with *different* exclusion lists. `translate` skips `.github/**` (it is in
// Co-op Translator's EXCLUDED_DIRS), so those files are never translated. But
// `co-op-review` does NOT exclude `.github/**`, so it reports every one of those
// untranslated source files as a "Missing translated file" error and fails the
// build. Those errors are false positives for paths this repo intentionally
// leaves untranslated. The review CLI exposes no way to extend its exclusions,
// so we drop findings under the excluded paths here and fail only on the rest.

const { spawnSync } = require("child_process");

// Source paths that are intentionally excluded from translation. Keep this in
// sync with the excludes in .github/workflows/co-op-translator.yml and the
// guidance in .github/workflows/translation-polisher.md.
const EXCLUDED_PREFIXES = [".github/", "samples/"];

const languages = process.argv
  .slice(2)
  .flatMap((value) => value.split(/\s+/))
  .map((value) => value.trim())
  .filter(Boolean);

if (languages.length === 0) {
  console.error("Usage: node .github/scripts/filter-co-op-review.js <language-codes>");
  process.exit(1);
}

const result = spawnSync(
  "co-op-review",
  ["-l", languages.join(" "), "--format", "github"],
  { encoding: "utf8" }
);

if (result.error && result.error.code === "ENOENT") {
  console.log("co-op-review is not available in the installed Co-op Translator package; skipping.");
  process.exit(0);
}

const report = result.stdout || "";
const stderr = result.stderr || "";

// Always surface the full report in the job log (and summary when available).
if (report.trim()) {
  console.log(report.trimEnd());
}
if (process.env.GITHUB_STEP_SUMMARY && report.trim()) {
  try {
    require("fs").appendFileSync(process.env.GITHUB_STEP_SUMMARY, `${report.trimEnd()}\n`);
  } catch (err) {
    console.error(`Could not write review report to step summary: ${err.message}`);
  }
}

const isExcluded = (filePath) =>
  EXCLUDED_PREFIXES.some((prefix) => filePath.startsWith(prefix));

const genuineErrors = [];
const ignoredErrors = [];

for (const line of report.split("\n")) {
  if (!line.trimStart().startsWith("|")) {
    continue;
  }
  const cells = line.split("|").map((cell) => cell.trim());
  // cells[0] is the empty string before the leading pipe.
  const severity = (cells[1] || "").toLowerCase();
  if (severity !== "error" && severity !== "warning") {
    continue; // Skip the metrics table, header, and separator rows.
  }
  if (severity !== "error") {
    continue; // Only errors fail the build; warnings are informational.
  }
  const filePath = (cells[4] || "").replace(/`/g, "").trim();
  if (isExcluded(filePath)) {
    ignoredErrors.push(filePath);
  } else {
    genuineErrors.push({ filePath, message: cells[5] || "" });
  }
}

if (ignoredErrors.length > 0) {
  console.log(
    `\nIgnored ${ignoredErrors.length} expected finding(s) for intentionally untranslated paths ` +
      `(${EXCLUDED_PREFIXES.join(", ")}).`
  );
}

if (genuineErrors.length > 0) {
  console.error(`\nco-op-review found ${genuineErrors.length} genuine error(s):`);
  for (const { filePath, message } of genuineErrors) {
    console.error(`  - ${filePath}: ${message}`);
  }
  if (stderr.trim()) {
    console.error(stderr.trimEnd());
  }
  process.exit(1);
}

console.log("\nco-op-review passed (no genuine errors).");
process.exit(0);
