import { spawn } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineWorkflow, joinSession } from "@github/copilot-sdk/extension";

const app = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");

function runPython(args, signal) {
  return new Promise((resolveRun, reject) => {
    const child = spawn("python3", args, {
      cwd: app,
      signal,
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    });
    let output = "";
    child.stdout.setEncoding("utf8").on("data", (chunk) => { output += chunk; });
    child.stderr.setEncoding("utf8").on("data", (chunk) => { output += chunk; });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === null) {
        reject(new Error(`Python was terminated: ${args.join(" ")}`));
      } else {
        resolveRun({ command: `python3 ${args.join(" ")}`, exitCode: code, output: output.trim() });
      }
    });
  });
}

const releaseCheck = defineWorkflow({
  meta: {
    name: "book-release-check",
    description: "Check the Python book app, pause for human review, then write release-report.md. No inputs.",
    phases: [
      { title: "Run project checks", detail: "Run pytest and the CLI help smoke check." },
      { title: "Human review checkpoint", detail: "Resume in /workflows when ready." },
      { title: "Assess release readiness", detail: "An agent evaluates the evidence and test coverage." },
      { title: "Save release report", detail: "Write release-report.md in the book app." },
    ],
  },
  run: async (ctx) => {
    ctx.phase("Run project checks");
    const checks = await ctx.step("book-checks-v1", async () => {
      const results = await Promise.all([
        runPython(["-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/"], ctx.signal),
        runPython(["book_app.py", "help"], ctx.signal),
      ]);
      for (const check of results) {
        ctx.log(`${check.exitCode === 0 ? "PASS" : "FAIL"}: ${check.command}\n${check.output}`);
      }
      return results;
    });

    ctx.phase("Human review checkpoint");
    ctx.log("Project checks are saved. Review the evidence, then resume this run in /workflows.");
    await ctx.pause("review-project-checks");

    ctx.phase("Assess release readiness");
    ctx.log("Resumed with saved check results; the test commands are not run again.");
    const sourceFiles = ["books.py", "tests/test_books.py", "README.md"];
    const sources = await Promise.all(sourceFiles.map(async (file) =>
      `${file}:\n${await readFile(resolve(app, file), "utf8")}`));
    const assessment = await ctx.agent(
      "Assess this small Python book collection app for a demo release, not production. " +
      "Use only the supplied evidence; do not run tools or edit files. " +
      "Passing tests do not prove production readiness. Identify exactly two concrete " +
      "untested behaviors from the supplied source. Keep each item under 18 words, " +
      "and the summary under 30 words.\n\n" +
      `Check evidence:\n${JSON.stringify(checks)}\n\n${sources.join("\n\n")}`,
      {
        label: "Release-readiness assessment",
        schema: {
          type: "object",
          required: ["summary", "untestedBehaviors"],
          properties: {
            summary: { type: "string" },
            untestedBehaviors: { type: "array", items: { type: "string" } },
          },
        },
      },
    );
    if (assessment === null) {
      throw new Error("The release-readiness agent did not return a valid assessment.");
    }

    ctx.phase("Save release report");
    const allPassed = checks.every((check) => check.exitCode === 0);
    const report = [
      "# Book app release readiness",
      "",
      `Checks: ${allPassed ? "PASS" : "FAIL"}`,
      ...checks.map((check) => `- ${check.command}: ${check.exitCode === 0 ? "PASS" : "FAIL"}`),
      "",
      "## Assessment",
      assessment.summary,
      "",
      "## Test gaps to address",
      ...assessment.untestedBehaviors.map((gap) => `- ${gap}`),
      "",
      "Passing checks are evidence, not a guarantee of production readiness.",
      "",
    ].join("\n");
    await ctx.step("save-release-report-v1", async () => {
      await writeFile(resolve(app, "release-report.md"), report, "utf8");
      return { file: "release-report.md" };
    });
    ctx.log("Saved release-report.md with check results and concrete test gaps.");
    return { checksPassed: allPassed, report: "release-report.md", assessment };
  },
});

await joinSession({ workflows: [releaseCheck] });
