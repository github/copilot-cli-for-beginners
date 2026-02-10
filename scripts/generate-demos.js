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
 *   npm run generate:vhs -- --concurrency 3       # limit to 3 at a time
 *
 * Requirements:
 *   - VHS: brew install vhs
 */

const { exec, execSync } = require('child_process');
const { readdirSync, statSync, existsSync, readFileSync, renameSync, writeFileSync, chmodSync, mkdirSync, rmSync } = require('fs');
const { join, relative, dirname } = require('path');

const rootDir = join(__dirname, '..');

// Parse CLI args
const args = process.argv.slice(2);
const chapters = [];
let concurrency = 5;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--chapter' && args[i + 1]) {
    chapters.push(args[++i]);
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

    if (stat.isDirectory() && !entry.startsWith('.') && entry !== 'node_modules' && entry !== 'scripts') {
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
      timeout: 180000,
      env: { ...process.env, PATH: wrappedPath }
    }, (error) => {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);

      if (error) {
        console.log(`  ✗ ${relativePath} (${elapsed}s) - ${error.message}`);
        resolve({ success: false, path: relativePath });
        return;
      }

      // Move generated GIF to the images folder if it was created in root
      if (outputFilename) {
        const generatedPath = join(rootDir, outputFilename);
        const targetPath = join(imagesDir, outputFilename);
        if (existsSync(generatedPath) && generatedPath !== targetPath) {
          renameSync(generatedPath, targetPath);
        }
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

  if (chapters.length > 0) {
    console.log(`Chapters: ${chapters.join(', ')}`);
  }
  console.log(`Concurrency: ${concurrency}`);
  console.log('');

  const tapeFiles = findTapeFiles(rootDir, chapters);

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
  process.exit(1);
});
