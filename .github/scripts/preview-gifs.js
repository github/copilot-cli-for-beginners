#!/usr/bin/env node
/**
 * Extract a preview frame from each demo GIF for quick visual inspection.
 * Saves individual PNG frames to demo-previews/ directory.
 *
 * Requires: ffmpeg, gifsicle (for frame delay info)
 *
 * Usage:
 *   node preview-gifs.js                  # default: 3s before end
 *   node preview-gifs.js --before 5       # 5s before end
 */

const { execSync } = require('child_process');
const { readdirSync, existsSync, mkdirSync, rmSync } = require('fs');
const { join, basename } = require('path');

const rootDir = join(__dirname, '..', '..');
const previewDir = join(rootDir, 'demo-previews');

// Parse CLI args
const args = process.argv.slice(2);
let beforeSeconds = 3;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--before' && args[i + 1]) {
    beforeSeconds = parseFloat(args[++i]);
  }
}

// Find all demo GIFs
function findGifs() {
  const gifs = [];
  for (const entry of readdirSync(rootDir)) {
    if (!/^\d{2}-/.test(entry)) continue;
    const imagesDir = join(rootDir, entry, 'images');
    if (!existsSync(imagesDir)) continue;
    for (const file of readdirSync(imagesDir)) {
      if (file.endsWith('-demo.gif')) {
        gifs.push({ path: join(imagesDir, file), chapter: entry });
      }
    }
  }
  return gifs.sort((a, b) => a.path.localeCompare(b.path));
}

// Get frame delays from a GIF
function getFrameDelays(gifPath) {
  const output = execSync(`gifsicle --info "${gifPath}"`, { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  const delays = [];
  const delayRegex = /delay (\d+(?:\.\d+)?)s/g;
  let match;
  while ((match = delayRegex.exec(output)) !== null) {
    delays.push(parseFloat(match[1]));
  }
  return delays;
}

// Find frame index at N seconds before the end
function frameAtSecondsBeforeEnd(delays, seconds) {
  const totalTime = delays.reduce((a, b) => a + b, 0);
  const targetTime = totalTime - seconds;
  if (targetTime <= 0) return 0;

  let cumulative = 0;
  for (let i = 0; i < delays.length; i++) {
    cumulative += delays[i];
    if (cumulative >= targetTime) return i;
  }
  return delays.length - 1;
}

// Main
if (existsSync(previewDir)) rmSync(previewDir, { recursive: true });
mkdirSync(previewDir, { recursive: true });

const gifs = findGifs();
if (gifs.length === 0) {
  console.log('No demo GIFs found');
  process.exit(0);
}

console.log(`\nExtracting frames (${beforeSeconds}s before end) from ${gifs.length} GIFs...\n`);

let count = 0;
for (const { path: gif, chapter } of gifs) {
  const name = basename(gif, '.gif');
  const delays = getFrameDelays(gif);
  const frameIndex = frameAtSecondsBeforeEnd(delays, beforeSeconds);
  const prefix = chapter.replace(/^(\d+)-.+/, '$1');
  const outName = `${prefix}-${name}.png`;
  const outPath = join(previewDir, outName);

  try {
    execSync(
      `ffmpeg -y -i "${gif}" -vf "select=eq(n\\,${frameIndex})" -vframes 1 -update 1 "${outPath}" 2>/dev/null`,
      { stdio: 'pipe' }
    );
    console.log(`  ✓ ${outName} (frame #${frameIndex}/${delays.length})`);
    count++;
  } catch (e) {
    console.log(`  ✗ ${name}: extraction failed`);
  }
}

console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`✓ ${count} preview frames saved to demo-previews/`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`\nOpen in Finder: open demo-previews/`);
