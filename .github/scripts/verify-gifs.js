#!/usr/bin/env node
/**
 * Verify demo GIFs completed successfully by checking their last frame.
 *
 * Extracts the last frame of each GIF, runs OCR via tesseract, and checks
 * for known failure/success patterns to determine if the demo completed.
 *
 * Usage:
 *   npm run verify:gifs              # check all GIFs
 *   npm run verify:gifs -- --save    # also save last-frame PNGs to /tmp/gif-last-frames/
 *
 * Requirements:
 *   - ffmpeg + ffprobe: brew install ffmpeg
 *   - tesseract: brew install tesseract
 */

const { execSync } = require('child_process');
const { readdirSync, statSync, existsSync, mkdirSync, rmSync } = require('fs');
const { join, basename, dirname } = require('path');

const rootDir = join(__dirname, '..', '..');
const tmpDir = '/tmp/gif-last-frames';
const saveFrames = process.argv.includes('--save');

// Patterns that indicate the response was cut off or incomplete
const FAILURE_PATTERNS = [
  'operation cancelled by user',
  'ctrl+c again to exit',
  'thinking (esc to cancel',
];

// Patterns that indicate a completed response (positive signals)
const SUCCESS_PATTERNS = [
  'type @ to mention files',
  'remaining requests',
];

function findGifs(dir) {
  const gifs = [];
  for (const entry of readdirSync(dir)) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);
    if (stat.isDirectory() && !entry.startsWith('.') && entry !== 'node_modules') {
      const imagesDir = join(fullPath, 'images');
      if (existsSync(imagesDir)) {
        for (const file of readdirSync(imagesDir)) {
          if (file.endsWith('-demo.gif')) {
            gifs.push(join(imagesDir, file));
          }
        }
      }
    }
  }
  return gifs.sort();
}

function getFrameCount(gifPath) {
  try {
    const result = execSync(
      `ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "${gifPath}"`,
      { encoding: 'utf8', timeout: 30000 }
    );
    return parseInt(result.trim(), 10);
  } catch {
    return -1;
  }
}

function extractLastFrame(gifPath, outputPath) {
  const frames = getFrameCount(gifPath);
  if (frames <= 0) return false;
  const lastFrame = frames - 1;
  try {
    execSync(
      `ffmpeg -y -i "${gifPath}" -vf "select=eq(n\\,${lastFrame})" -frames:v 1 "${outputPath}" 2>/dev/null`,
      { timeout: 30000 }
    );
    return existsSync(outputPath);
  } catch {
    return false;
  }
}

function extractTextFromFrame(pngPath) {
  const dir = dirname(pngPath);
  const file = basename(pngPath);
  try {
    // tesseract needs to run from the file's directory (macOS path issue)
    const text = execSync(`tesseract "${file}" stdout 2>/dev/null`, {
      encoding: 'utf8', timeout: 15000, cwd: dir
    });
    return text.toLowerCase();
  } catch {
    return '';
  }
}

function checkLastFrame(gifPath) {
  const name = basename(gifPath, '.gif');
  const chapter = basename(join(gifPath, '..', '..'));
  const chNum = chapter.substring(0, 2);
  const pngPath = join(tmpDir, `${chNum}-${name}.png`);

  if (!extractLastFrame(gifPath, pngPath)) {
    return { name: `${chNum}/${name}`, status: 'ERROR', reason: 'Could not extract last frame' };
  }

  const text = extractTextFromFrame(pngPath);

  if (!text.trim()) {
    return { name: `${chNum}/${name}`, status: 'UNKNOWN', reason: 'OCR returned no text' };
  }

  // Check for failure patterns
  for (const pattern of FAILURE_PATTERNS) {
    if (text.includes(pattern)) {
      return { name: `${chNum}/${name}`, status: 'INCOMPLETE', reason: `Found: "${pattern}"` };
    }
  }

  // Check for the copilot prompt (indicates it returned to prompt = completed)
  const hasPrompt = SUCCESS_PATTERNS.some(p => text.includes(p));
  if (hasPrompt) {
    return { name: `${chNum}/${name}`, status: 'OK', reason: 'Response completed' };
  }

  // Has text but no known patterns - likely OK but uncertain
  return { name: `${chNum}/${name}`, status: 'OK?', reason: 'Has text, no failure patterns detected' };
}

// Main
function main() {
  // Check dependencies
  try {
    execSync('which tesseract', { encoding: 'utf8' });
  } catch {
    console.error('Error: tesseract is required. Install with: brew install tesseract');
    process.exit(1);
  }
  try {
    execSync('which ffprobe', { encoding: 'utf8' });
  } catch {
    console.error('Error: ffmpeg/ffprobe is required. Install with: brew install ffmpeg');
    process.exit(1);
  }

  console.log('🔍 Verifying demo GIFs...\n');

  // Set up temp directory
  if (existsSync(tmpDir)) rmSync(tmpDir, { recursive: true });
  mkdirSync(tmpDir, { recursive: true });

  const gifs = findGifs(rootDir);

  if (gifs.length === 0) {
    console.log('No GIF files found');
    process.exit(0);
  }

  console.log(`Found ${gifs.length} GIF(s)\n`);

  const results = [];
  for (const gif of gifs) {
    const result = checkLastFrame(gif);
    results.push(result);
  }

  // Print results table
  const nameWidth = Math.max(32, ...results.map(r => r.name.length + 2));
  const statusWidth = 14;

  const header = 'GIF'.padEnd(nameWidth) + 'Status'.padEnd(statusWidth) + 'Details';
  const separator = '─'.repeat(header.length + 10);

  console.log(separator);
  console.log(header);
  console.log(separator);

  for (const r of results) {
    const icon = r.status === 'OK' ? '✓' :
                 r.status === 'OK?' ? '~' :
                 r.status === 'INCOMPLETE' ? '✗' : '?';
    const statusStr = `${icon} ${r.status}`.padEnd(statusWidth);
    console.log(`${r.name.padEnd(nameWidth)}${statusStr}${r.reason}`);
  }

  console.log(separator);

  const ok = results.filter(r => r.status === 'OK' || r.status === 'OK?').length;
  const incomplete = results.filter(r => r.status === 'INCOMPLETE').length;
  const unknown = results.filter(r => r.status === 'UNKNOWN' || r.status === 'ERROR').length;

  console.log(`\n✓ Complete: ${ok}  ✗ Incomplete: ${incomplete}  ? Unknown: ${unknown}`);

  if (incomplete > 0) {
    console.log('\nIncomplete GIFs need increased responseWait in .github/scripts/demos.json');
  }

  // Clean up unless --save
  if (!saveFrames) {
    rmSync(tmpDir, { recursive: true });
  } else {
    console.log(`\nLast-frame PNGs saved to: ${tmpDir}`);
  }

  process.exit(incomplete > 0 ? 1 : 0);
}

main();
