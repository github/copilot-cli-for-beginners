#!/usr/bin/env node
/**
 * Generate course demo GIFs from .tape files
 *
 * This script finds all .tape files in [chapter]/images/ folders and runs VHS
 * to generate GIFs. VHS is run from the project root so that @file references
 * in prompts resolve correctly.
 *
 * Usage:
 *   npm run generate:vhs                          # all chapters, 5 concurrent
 *   npm run generate:vhs -- --chapter 03          # only chapter 03
 *   npm run generate:vhs -- --chapter 03 --chapter 05
 *   npm run generate:vhs -- --file path/to/demo.tape  # single tape file
 *   npm run generate:vhs -- --concurrency 3       # limit to 3 at a time
 *
 * Requirements:
 *   - VHS: brew install vhs
 */

const { exec, execSync } = require('child_process');
const { readdirSync, statSync, existsSync, readFileSync, renameSync, writeFileSync, chmodSync, mkdirSync, rmSync } = require('fs');
const { join, relative, dirname } = require('path');

const rootDir = join(__dirname, '..', '..');
const homeDir = require('os').homedir();
const copilotConfigPath = join(homeDir, '.copilot', 'config.json');
// Personal agents live in both ~/.copilot/agents and ~/.claude/agents
const personalAgentsDirs = [
  { dir: join(homeDir, '.copilot', 'agents'), backup: join(homeDir, '.copilot', 'agents.recording-bak') },
  { dir: join(homeDir, '.claude', 'agents'), backup: join(homeDir, '.claude', 'agents.recording-bak') }
];

// Ensure streamer mode is enabled so recordings don't show model names or quota
function enableStreamerMode() {
  try {
    const config = JSON.parse(readFileSync(copilotConfigPath, 'utf8'));
    const wasOn = config.streamer_mode || false;
    config.streamer_mode = true;
    delete config.on_air_mode;
    writeFileSync(copilotConfigPath, JSON.stringify(config, null, 2) + '\n');
    console.log(`🔴 Streamer mode: ${wasOn ? 'already enabled' : 'enabled'}`);
    return { wasOn };
  } catch (e) {
    console.warn('⚠ Could not read copilot config, streamer mode not verified');
    return null;
  }
}

// Restore streamer mode to its original state
function restoreStreamerMode(state) {
  if (state && !state.wasOn) {
    try {
      const config = JSON.parse(readFileSync(copilotConfigPath, 'utf8'));
      config.streamer_mode = false;
      writeFileSync(copilotConfigPath, JSON.stringify(config, null, 2) + '\n');
      console.log('🔴 Streamer mode: restored to off');
    } catch (e) { /* ignore */ }
  }
}

// Hide personal agents so only course agents appear in /agent picker
function hidePersonalAgents() {
  const hidden = [];
  for (const { dir, backup } of personalAgentsDirs) {
    try {
      // Restore stale backup from a previous interrupted run
      if (!existsSync(dir) && existsSync(backup)) {
        renameSync(backup, dir);
        console.log(`👤 Restored stale backup: ${backup}`);
      }
      if (existsSync(dir)) {
        renameSync(dir, backup);
        hidden.push({ dir, backup });
      }
    } catch (e) {
      console.warn(`⚠ Could not hide ${dir}:`, e.message);
    }
  }
  if (hidden.length > 0) {
    console.log(`👤 Personal agents: hidden (${hidden.length} location(s))`);
  }
  return hidden;
}

// Restore personal agents to their original locations
function restorePersonalAgents(hidden) {
  if (!hidden || hidden.length === 0) return;
  for (const { dir, backup } of hidden) {
    try {
      if (existsSync(backup)) {
        // Copilot may recreate the agents dir during recording - remove it first
        if (existsSync(dir)) {
          rmSync(dir, { recursive: true });
        }
        renameSync(backup, dir);
      }
    } catch (e) {
      console.warn(`⚠ Could not restore ${dir}:`, e.message);
      console.warn(`  Manual fix: mv "${backup}" "${dir}"`);
    }
  }
  console.log(`👤 Personal agents: restored (${hidden.length} location(s))`);
}

// Parse CLI args
const args = process.argv.slice(2);
const chapters = [];
const files = [];
let concurrency = 5;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--chapter' && args[i + 1]) {
    chapters.push(args[++i]);
  } else if (args[i] === '--file' && args[i + 1]) {
    files.push(args[++i]);
  } else if (args[i] === '--concurrency' && args[i + 1]) {
    concurrency = parseInt(args[++i], 10);
  }
}

// Create a wrapper script that injects --yolo and --allow-all-paths so copilot
// runs non-interactively. The tape just types "copilot" which looks clean in
// the recording, but the wrapper adds flags behind the scenes.
const wrapperDir = join(rootDir, '.vhs-wrapper');
function setupCopilotWrapper() {
  const realCopilot = execSync('which copilot', { encoding: 'utf8' }).trim();
  mkdirSync(wrapperDir, { recursive: true });
  const wrapperPath = join(wrapperDir, 'copilot');
  writeFileSync(wrapperPath, `#!/bin/bash\nexec "${realCopilot}" --yolo --allow-all-paths "$@"\n`);
  chmodSync(wrapperPath, '755');
  return `${wrapperDir}:${process.env.PATH}`;
}

function cleanupCopilotWrapper() {
  try { rmSync(wrapperDir, { recursive: true }); } catch (e) { /* ignore */ }
}

// Find all .tape files in [chapter]/images/ folders
function findTapeFiles(dir, chapterFilter) {
  const tapeFiles = [];

  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);

    if (stat.isDirectory() && !entry.startsWith('.') && entry !== 'node_modules') {
      // Apply chapter filter if specified
      if (chapterFilter.length > 0) {
        const matches = chapterFilter.some(ch => entry.startsWith(ch) || entry.includes(ch));
        if (!matches) continue;
      }

      const imagesDir = join(fullPath, 'images');
      if (existsSync(imagesDir)) {
        try {
          const imagesEntries = readdirSync(imagesDir);
          for (const file of imagesEntries) {
            if (file.endsWith('.tape')) {
              tapeFiles.push(join(imagesDir, file));
            }
          }
        } catch (e) {
          // Can't read images folder, skip
        }
      }
    }
  }

  return tapeFiles;
}

// Extract output filename from tape file
function getOutputFilename(tapeFilePath) {
  const content = readFileSync(tapeFilePath, 'utf8');
  const match = content.match(/^Output\s+(\S+)/m);
  return match ? match[1] : null;
}

// Run a single VHS recording and return a promise
function runVhs(tapeFile, wrappedPath) {
  const relativePath = relative(rootDir, tapeFile);
  const imagesDir = dirname(tapeFile);
  const outputFilename = getOutputFilename(tapeFile);

  return new Promise((resolve) => {
    const startTime = Date.now();

    exec(`vhs ${relativePath}`, {
      cwd: rootDir,
      timeout: 600000,
      env: { ...process.env, PATH: wrappedPath }
    }, (error) => {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);

      // Always move GIF if it was created, even if VHS exited non-zero
      let gifCreated = false;
      if (outputFilename) {
        const generatedPath = join(rootDir, outputFilename);
        const targetPath = join(imagesDir, outputFilename);
        if (existsSync(generatedPath) && generatedPath !== targetPath) {
          renameSync(generatedPath, targetPath);
          gifCreated = true;
        }
      }

      if (error && !gifCreated) {
        console.log(`  ✗ ${relativePath} (${elapsed}s) - ${error.message}`);
        resolve({ success: false, path: relativePath });
        return;
      }

      console.log(`  ✓ ${relativePath} (${elapsed}s)`);
      resolve({ success: true, path: relativePath });
    });
  });
}

// Run tasks with concurrency limit
async function runWithConcurrency(tasks, limit) {
  const results = [];
  const executing = new Set();

  for (const task of tasks) {
    const promise = task().then(result => {
      executing.delete(promise);
      return result;
    });
    executing.add(promise);
    results.push(promise);

    if (executing.size >= limit) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}

// Main
async function main() {
  console.log('🎬 Generating course demos...\n');

  if (files.length > 0) {
    console.log(`Files: ${files.join(', ')}`);
  } else if (chapters.length > 0) {
    console.log(`Chapters: ${chapters.join(', ')}`);
  }
  console.log(`Concurrency: ${concurrency}`);
  console.log('');

  // Enable streamer mode and hide personal agents before recording
  const streamerState = enableStreamerMode();
  const agentsWereHidden = hidePersonalAgents();
  console.log('');

  // Resolve tape files: explicit --file paths take priority over chapter scan
  let tapeFiles;
  if (files.length > 0) {
    const { resolve } = require('path');
    tapeFiles = files.map(f => resolve(rootDir, f)).filter(f => {
      if (!existsSync(f)) {
        console.log(`  ⚠ File not found: ${f}`);
        return false;
      }
      return true;
    });
  } else {
    tapeFiles = findTapeFiles(rootDir, chapters);
  }

  if (tapeFiles.length === 0) {
    console.log('No .tape files found');
    process.exit(0);
  }

  console.log(`Found ${tapeFiles.length} tape file(s):\n`);
  tapeFiles.forEach(f => console.log('  - ' + relative(rootDir, f)));
  console.log('');

  // Set up copilot wrapper so --yolo is injected transparently
  const wrappedPath = setupCopilotWrapper();
  console.log('Copilot wrapper: --yolo injected via PATH');
  console.log(`Recording ${tapeFiles.length} demos (${concurrency} at a time)...\n`);

  const startTime = Date.now();

  // Build task functions
  const tasks = tapeFiles.map(tapeFile => () => runVhs(tapeFile, wrappedPath));

  // Run with concurrency limit
  const results = await runWithConcurrency(tasks, concurrency);

  cleanupCopilotWrapper();
  restorePersonalAgents(agentsWereHidden);
  restoreStreamerMode(streamerState);

  const succeeded = results.filter(r => r.success).length;
  const failedResults = results.filter(r => !r.success);
  const totalTime = ((Date.now() - startTime) / 1000).toFixed(0);

  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`✓ Success: ${succeeded}`);
  if (failedResults.length > 0) {
    console.log(`✗ Failed:  ${failedResults.length}`);
    failedResults.forEach(r => console.log(`  - ${r.path}`));
  }
  console.log(`⏱ Total:   ${totalTime}s`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
}

main().catch(e => {
  console.error(e);
  cleanupCopilotWrapper();
  restorePersonalAgents(personalAgentsDirs); // always try to restore on error
  restoreStreamerMode({ wasOn: false });
  process.exit(1);
});
