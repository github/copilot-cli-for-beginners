#!/usr/bin/env node
/**
 * Post-process course demo GIFs
 *
 * Crops the bottom of each GIF to remove the "Remaining requests" status bar.
 *
 * Usage: npm run crop:gifs
 * Usage: npm run crop:gifs -- --height 540
 *
 * Requirements:
 *   - gifsicle: brew install gifsicle
 */

const { execSync } = require('child_process');
const { readdirSync, statSync, existsSync } = require('fs');
const { join, relative } = require('path');

const rootDir = join(__dirname, '..');

// Parse --height flag (default 520)
const args = process.argv.slice(2);
const heightIdx = args.indexOf('--height');
const cropHeight = heightIdx !== -1 && args[heightIdx + 1]
  ? parseInt(args[heightIdx + 1], 10)
  : 520;

// Find all GIFs in [chapter]/images/ folders
function findGifFiles(dir) {
  const gifFiles = [];

  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);

    if (stat.isDirectory() && !entry.startsWith('.') && entry !== 'node_modules' && entry !== 'scripts') {
      const imagesDir = join(fullPath, 'images');
      if (existsSync(imagesDir)) {
        try {
          const imagesEntries = readdirSync(imagesDir);
          for (const file of imagesEntries) {
            if (file.endsWith('.gif')) {
              gifFiles.push(join(imagesDir, file));
            }
          }
        } catch (e) {
          // Can't read images folder, skip
        }
      }
    }
  }

  return gifFiles;
}

// Main
console.log(`\nCropping GIFs to 1000x${cropHeight} (looping)...\n`);

const gifFiles = findGifFiles(rootDir);

if (gifFiles.length === 0) {
  console.log('No GIF files found in [chapter]/images/ folders');
  process.exit(0);
}

let success = 0;
let failed = 0;

for (const gifPath of gifFiles) {
  const relPath = relative(rootDir, gifPath);
  try {
    execSync(`gifsicle --crop "0,0+1000x${cropHeight}" --loopcount=forever "${gifPath}" -o "${gifPath}"`, { stdio: 'pipe' });
    console.log(`  ✓ ${relPath}`);
    success++;
  } catch (e) {
    console.log(`  ✗ ${relPath}: ${e.message}`);
    failed++;
  }
}

console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`✓ Cropped: ${success}`);
if (failed > 0) {
  console.log(`✗ Failed:  ${failed}`);
}
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
