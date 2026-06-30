#!/usr/bin/env node
/**
 * Watch docs/content.yaml and rebuild the visual quickstart site on every save.
 *
 * Usage:
 *   npm run watch:visual-quickstart
 *
 * Leave this running while you edit content.yaml. Each save regenerates the
 * visual quickstart HTML/CSS (and re-optimizes images) automatically. Ctrl+C to stop.
 *
 * The watch loop, like the rest of the rendering/optimization engine, lives in the
 * reusable visual-quickstart-generator skill; this is a thin launcher that points
 * that engine at this repo's content file and output dir.
 *
 * Optional env overrides:
 *   VISUAL_QUICKSTART_SKILL_DIR  path to the visual-quickstart-generator skill folder
 */

const { spawnSync } = require('child_process');
const { existsSync } = require('fs');
const { join } = require('path');
const os = require('os');

const repoRoot = join(__dirname, '..', '..'); // .github/scripts -> repo root
const docsDir = join(repoRoot, 'docs');
const contentFile = join(docsDir, 'content.yaml');

const skillDir =
  process.env.VISUAL_QUICKSTART_SKILL_DIR ||
  join(os.homedir(), '.copilot', 'skills', 'visual-quickstart-generator');
const watchScript = join(skillDir, 'scripts', 'watch.js');

if (!existsSync(watchScript)) {
  console.error(
    `\u2716 Visual quickstart engine not found at:\n  ${watchScript}\n` +
      'Set VISUAL_QUICKSTART_SKILL_DIR to the visual-quickstart-generator skill folder, or install the skill.',
  );
  process.exit(1);
}
if (!existsSync(contentFile)) {
  console.error(`\u2716 Content file not found:\n  ${contentFile}`);
  process.exit(1);
}

const result = spawnSync(process.execPath, [watchScript], {
  stdio: 'inherit',
  env: { ...process.env, VISUAL_QUICKSTART_DOCS: docsDir, VISUAL_QUICKSTART_CONTENT: contentFile },
});

if (result.error) {
  console.error(`\u2716 Failed to run the engine: ${result.error.message}`);
  process.exit(1);
}
process.exit(result.status ?? 0);
