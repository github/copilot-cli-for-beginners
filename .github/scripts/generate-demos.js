#!/usr/bin/env node
/**
 * Generate course demo GIFs from .tape files
 *
 * This script finds all .tape files in [chapter]/assets/ folders and runs VHS
 * to generate GIFs. VHS is run from the project root so that @file references
 * in prompts resolve correctly. Each recording uses a clean, temporary
 * COPILOT_HOME, so your personal skills, agents, plugins, hooks, MCP servers,
 * Copilot Connectors, and saved memories do not appear in the GIFs.
 *
 * The script also checks every GIF after recording:
 *   - A GIF that shows the promo banner of Copilot CLI ("Discover <model> ...
 *     50% off right now") is recorded again, up to 3 attempts in total.
 *   - Every stretch of unchanged screen is shortened to 4 seconds, so a fixed
 *     response wait does not leave a frozen screen at the end of the GIF.
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
 *   - ffmpeg, tesseract, gifsicle: brew install ffmpeg tesseract gifsicle
 *   - Copilot CLI signed in (copilot login, or GH_TOKEN set)
 */

const { execFile, execSync } = require('child_process');
const { promisify } = require('util');
const { readdirSync, statSync, existsSync, readFileSync, copyFileSync, writeFileSync, chmodSync, mkdirSync, mkdtempSync, realpathSync, rmSync } = require('fs');
const { homedir, tmpdir } = require('os');
const { join, relative, dirname, basename } = require('path');
const { findPromoBanner, trimStaticFrames, MAX_STATIC_SECONDS } = require('./gif-utils');

const execFileAsync = promisify(execFile);

const rootDir = join(__dirname, '..', '..');
const realCopilotHome = process.env.COPILOT_HOME || join(homedir(), '.copilot');

// Total attempts for a demo whose GIF shows the promo banner
const MAX_ATTEMPTS = 3;

// Reads a JSON file that Copilot CLI writes. These files start with "//" comment
// lines, so the comments are removed before parsing.
function readCommentedJson(file) {
  const lines = readFileSync(file, 'utf8').split('\n');
  return {
    comments: lines.filter(line => line.trim().startsWith('//')),
    data: JSON.parse(lines.filter(line => !line.trim().startsWith('//')).join('\n'))
  };
}

// Read only the sign-in state (no tokens) from the real Copilot config, so a
// recording stays signed in when you used `copilot login`. Without it, copilot
// reads GH_TOKEN, GITHUB_TOKEN, or COPILOT_GITHUB_TOKEN.
function readLoginState() {
  try {
    const { loggedInUsers, lastLoggedInUser } = readCommentedJson(join(realCopilotHome, 'config.json')).data;
    return { loggedInUsers, lastLoggedInUser };
  } catch (e) {
    return {};
  }
}

// Every recording runs in its own throwaway COPILOT_HOME, so it starts like a
// new learner's install: no personal skills, agents, plugins, hooks, or MCP
// servers, and no leftover state from earlier recordings or sessions.
function createRecordingHome(loginState) {
  const dir = mkdtempSync(join(tmpdir(), 'copilot-recording-'));
  // Streamer mode hides quota details. Auto-update off keeps the CLI version
  // the same for the whole batch. Connectors and memory off keep account-level
  // data (such as a Slack connector or saved memories) out of the recordings,
  // and stop the recordings from saving new memories.
  const settings = { streamerMode: true, autoUpdate: false, connectors: false, memory: false };
  writeFileSync(join(dir, 'settings.json'), JSON.stringify(settings, null, 2) + '\n');
  writeFileSync(join(dir, 'config.json'), JSON.stringify({
    ...loginState,
    // Skips the "Confirm folder trust" prompt (--yolo does not skip it)
    trustedFolders: [realpathSync(rootDir)],
    // Uses the default model and features that learners get
    staff: false
  }, null, 2) + '\n');
  return dir;
}

// Copilot CLI turns on its promo banner (the "Discover <model> ... 50% off right
// now" text in the start screen) with an experiment flag from the GitHub servers.
// The CLI saves its flags in a cache folder (COPILOT_CACHE_HOME), and no setting
// turns this one off. The recordings share one temporary cache folder. A start-up
// of the CLI fills it, and then the script turns the flag off in it. The banner is
// a promotion, not course content.
const PROMO_FLAG = 'copilot_cli_changeboarding_model_nudge';

// Turns the promo flag off in the cache. Returns the number of cache entries that
// changed, or null if the cache cannot be read or has no experiment data.
function disablePromoFlag(cacheDir) {
  const file = join(cacheDir, 'exp-cache.json');
  try {
    const { comments, data } = readCommentedJson(file);
    if (!data.expAssignmentsCache) return null;
    let changed = 0;
    for (const entry of Object.values(data.expAssignmentsCache || {})) {
      for (const config of (entry.response && entry.response.Configs) || []) {
        if (config.Parameters && config.Parameters[PROMO_FLAG] === true) {
          config.Parameters[PROMO_FLAG] = false;
          changed++;
        }
      }
    }
    if (changed > 0) {
      writeFileSync(file, [...comments, JSON.stringify(data, null, 2)].join('\n') + '\n');
    }
    return changed;
  } catch (e) {
    return null;
  }
}

// Runs VHS once on a tape file, in a fresh COPILOT_HOME and the shared cache folder.
// A tape can store temporary files in $DEMO_SCRATCH_DIR. This folder is the fresh
// COPILOT_HOME, so it is deleted after the recording.
// Rejects when VHS fails, but the GIF can still exist.
async function runVhsOnce(tapeFile, gifPath, { wrappedPath, loginState, cacheDir }) {
  const recordingHome = createRecordingHome(loginState);
  try {
    await execFileAsync('vhs', [tapeFile, '--output', gifPath, '--quiet'], {
      cwd: rootDir,
      timeout: 600000,
      env: {
        ...process.env,
        PATH: wrappedPath,
        COPILOT_HOME: recordingHome,
        COPILOT_CACHE_HOME: cacheDir,
        DEMO_SCRATCH_DIR: recordingHome
      }
    });
  } finally {
    rmSync(recordingHome, { recursive: true, force: true });
  }
}

// Starts Copilot CLI once with the recording setup, so it saves its experiment
// flags in the cache folder, and then turns the promo flag off.
async function prepareExperimentCache(context) {
  const tapeFile = join(context.cacheDir, 'prepare.tape');
  writeFileSync(tapeFile, [
    'Output prepare.gif',
    'Set FontSize 18',
    'Set Width 1000',
    'Set Height 600',
    'Type "copilot"',
    'Enter',
    'Sleep 9s',
    'Ctrl+C',
    'Sleep 1s',
    'Ctrl+C',
    'Sleep 1s'
  ].join('\n') + '\n');

  try {
    await runVhsOnce(tapeFile, join(context.cacheDir, 'prepare.gif'), context);
  } catch (e) {
    console.log(`  ⚠ The start-up run failed: ${String(e.message).split('\n')[0]}`);
  }

  const changed = disablePromoFlag(context.cacheDir);
  if (changed === null) {
    console.log('  ⚠ Could not turn off the promo banner. A GIF that shows it is recorded again.');
  } else {
    console.log(changed > 0 ? '  ✓ Promo banner turned off' : '  ✓ The promo banner is not enabled');
  }
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

// Find all .tape files in [chapter]/assets/ folders
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

      const assetsDir = join(fullPath, 'assets');
      if (existsSync(assetsDir)) {
        try {
          const assetsEntries = readdirSync(assetsDir);
          for (const file of assetsEntries) {
            if (file.endsWith('.tape')) {
              tapeFiles.push(join(assetsDir, file));
            }
          }
        } catch (e) {
          // Can't read assets folder, skip
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

// Looks for the promo banner in the GIF. A failed check is reported but does not stop the batch.
async function checkForPromo(relativePath, gifPath) {
  try {
    return await findPromoBanner(gifPath);
  } catch (e) {
    console.log(`  ⚠ ${relativePath}: could not check for the promo banner - ${String(e.message).split('\n')[0]}`);
    return null;
  }
}

// Record a single demo. A GIF that shows the promo banner is recorded again, and
// the finished GIF gets its static ending shortened.
async function runVhs(tapeFile, context) {
  const relativePath = relative(rootDir, tapeFile);
  const outputFilename = getOutputFilename(tapeFile) || `${basename(tapeFile, '.tape')}.gif`;
  const targetPath = join(dirname(tapeFile), outputFilename);
  // Two chapters can use the same Output name, so every attempt records to a
  // temporary folder first
  const workDir = mkdtempSync(join(tmpdir(), 'copilot-recording-gif-'));
  const startTime = Date.now();

  try {
    let attempts = 0;
    let gifPath = null;
    let error = null;
    let promo = null;

    while (attempts < MAX_ATTEMPTS) {
      attempts++;
      const attemptPath = join(workDir, `attempt-${attempts}.gif`);
      error = null;
      try {
        await runVhsOnce(relativePath, attemptPath, context);
      } catch (e) {
        error = e;
      }

      // A GIF counts as recorded even if VHS exited non-zero. If VHS made no GIF,
      // the script keeps the GIF of an earlier attempt, if there is one.
      if (!existsSync(attemptPath)) break;
      gifPath = attemptPath;
      promo = await checkForPromo(relativePath, attemptPath);
      if (!promo) break;
      disablePromoFlag(context.cacheDir);
    }

    if (!gifPath) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);
      console.log(`  ✗ ${relativePath} (${elapsed}s) - ${error ? error.message : 'VHS did not create a GIF'}`);
      return { success: false, path: relativePath };
    }

    let trimmed = 0;
    try {
      trimmed = await trimStaticFrames(gifPath);
    } catch (e) {
      console.log(`  ⚠ ${relativePath}: could not shorten the static ending - ${String(e.message).split('\n')[0]}`);
    }
    copyFileSync(gifPath, targetPath);

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);
    const notes = [];
    if (attempts > 1) notes.push(`${attempts} attempts`);
    if (trimmed > 0) notes.push(`${trimmed.toFixed(0)}s of static screen removed`);
    console.log(`  ✓ ${relativePath} (${elapsed}s${notes.map(note => `, ${note}`).join('')})`);
    if (promo) {
      console.log(`  ⚠ ${relativePath}: the promo banner is still in the GIF after ${attempts} attempts ("${promo}")`);
    }
    return { success: true, path: relativePath, promo: Boolean(promo) };
  } finally {
    rmSync(workDir, { recursive: true, force: true });
  }
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

// VHS records the demos. The other tools read and shorten the finished GIFs.
function checkRequiredTools() {
  const missing = ['vhs', 'ffmpeg', 'tesseract', 'gifsicle'].filter(tool => {
    try {
      execSync(`which ${tool}`, { stdio: 'ignore' });
      return false;
    } catch (e) {
      return true;
    }
  });
  if (missing.length > 0) {
    console.error(`Missing tools: ${missing.join(', ')}\nInstall them with: brew install ${missing.join(' ')}`);
    process.exit(1);
  }
}

// Main
async function main() {
  console.log('🎬 Generating course demos...\n');
  checkRequiredTools();

  if (files.length > 0) {
    console.log(`Files: ${files.join(', ')}`);
  } else if (chapters.length > 0) {
    console.log(`Chapters: ${chapters.join(', ')}`);
  }
  console.log(`Concurrency: ${concurrency}`);
  console.log('🔒 Each recording runs in a clean COPILOT_HOME (streamer mode on; no personal skills, agents, plugins, hooks, MCP servers, connectors, or memories)');
  console.log(`🧹 Each GIF is checked for the promo banner (up to ${MAX_ATTEMPTS} attempts), and its static ending is shortened to ${MAX_STATIC_SECONDS}s`);
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

  const startTime = Date.now();
  const cacheDir = mkdtempSync(join(tmpdir(), 'copilot-recording-cache-'));
  const context = { wrappedPath, loginState: readLoginState(), cacheDir };

  let results;
  try {
    console.log('Preparing the experiment cache of Copilot CLI...');
    await prepareExperimentCache(context);
    console.log(`\nRecording ${tapeFiles.length} demos (${concurrency} at a time)...\n`);

    // Run with concurrency limit
    const tasks = tapeFiles.map(tapeFile => () => runVhs(tapeFile, context));
    results = await runWithConcurrency(tasks, concurrency);
  } finally {
    rmSync(cacheDir, { recursive: true, force: true });
    cleanupCopilotWrapper();
  }

  const succeeded = results.filter(r => r.success).length;
  const promoResults = results.filter(r => r.promo);
  const failedResults = results.filter(r => !r.success);
  const totalTime = ((Date.now() - startTime) / 1000).toFixed(0);

  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`✓ Success: ${succeeded}`);
  if (promoResults.length > 0) {
    console.log(`⚠ Promo banner still shown: ${promoResults.length}`);
    promoResults.forEach(r => console.log(`  - ${r.path}`));
  }
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
