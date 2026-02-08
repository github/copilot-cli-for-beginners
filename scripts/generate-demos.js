#!/usr/bin/env node
/**
 * Generate course demo GIFs from .tape files
 *
 * This script finds all .tape files in [chapter]/images/ folders and runs VHS
 * to generate GIFs. VHS is run from the project root so that @file references
 * in prompts resolve correctly.
 *
 * Usage: npm run generate:vhs
 *
 * Requirements:
 *   - VHS: brew install vhs
 */

const { execSync } = require('child_process');
const { readdirSync, statSync, existsSync, readFileSync, renameSync, writeFileSync, chmodSync, mkdirSync, rmSync } = require('fs');
const { join, basename, relative, dirname } = require('path');

const rootDir = join(__dirname, '..');

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
function findTapeFiles(dir) {
  const tapeFiles = [];

  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);

    if (stat.isDirectory() && !entry.startsWith('.') && entry !== 'node_modules' && entry !== 'scripts') {
      // Check for images subfolder
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

// Main
console.log('🎬 Generating course demos...\n');
console.log('Working directory:', rootDir);
console.log('');

const tapeFiles = findTapeFiles(rootDir);

if (tapeFiles.length === 0) {
  console.log('No .tape files found in [chapter]/images/ folders');
  process.exit(0);
}

console.log(`Found ${tapeFiles.length} tape file(s):\n`);
tapeFiles.forEach(f => console.log('  - ' + relative(rootDir, f)));
console.log('');

// Set up copilot wrapper so --yolo is injected transparently
const wrappedPath = setupCopilotWrapper();
console.log('Copilot wrapper: --yolo injected via PATH\n');

let success = 0;
let failed = 0;

for (const tapeFile of tapeFiles) {
  const relativePath = relative(rootDir, tapeFile);
  const imagesDir = dirname(tapeFile);
  const outputFilename = getOutputFilename(tapeFile);

  console.log(`Processing: ${relativePath}`);

  try {
    // Run VHS from project root so @file references resolve correctly.
    // PATH is modified so "copilot" resolves to the wrapper (adds --yolo).
    execSync(`vhs ${relativePath}`, {
      cwd: rootDir,
      stdio: 'inherit',
      timeout: 180000, // 3 minute timeout per demo (real copilot takes longer)
      env: { ...process.env, PATH: wrappedPath }
    });

    // Move generated GIF to the images folder if it was created in root
    if (outputFilename) {
      const generatedPath = join(rootDir, outputFilename);
      const targetPath = join(imagesDir, outputFilename);
      if (existsSync(generatedPath) && generatedPath !== targetPath) {
        renameSync(generatedPath, targetPath);
        console.log(`   → Moved to: ${relative(rootDir, targetPath)}`);
      }
    }

    success++;
    console.log('');
  } catch (e) {
    console.log(`   ✗ Failed: ${e.message}\n`);
    failed++;
  }
}

cleanupCopilotWrapper();

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`✓ Success: ${success}`);
if (failed > 0) {
  console.log(`✗ Failed:  ${failed}`);
}
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
