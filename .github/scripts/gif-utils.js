/**
 * GIF helpers for generate-demos.js
 *
 * Requirements (brew install ffmpeg tesseract gifsicle):
 *   - ffmpeg: extracts frames to read
 *   - tesseract: reads the text in a frame
 *   - gifsicle: finds and removes frames that repeat the previous frame
 */

const { execFile } = require('child_process');
const { promisify } = require('util');
const { mkdtempSync, readdirSync, renameSync, rmSync } = require('fs');
const { tmpdir } = require('os');
const { join } = require('path');

const execFileAsync = promisify(execFile);

// No screen stays unchanged longer than this in a trimmed GIF
const MAX_STATIC_SECONDS = 4;

// Copilot CLI sometimes shows a server-side banner such as "Discover <model> ...
// 50% off right now ... enter /model <name> to switch". It is not course content.
const PROMO_PATTERNS = [
  /enter\s+\/model\s+\S+\s+to\s+switch/i,
  /\d+\s*%\s*off\b/i
];

// The banner shows from start-up until the first response begins
const PROMO_SCAN_SECONDS = 20;

// Returns the banner text found in the first seconds of the GIF, or null
async function findPromoBanner(gifPath) {
  const dir = mkdtempSync(join(tmpdir(), 'copilot-promo-scan-'));
  try {
    // One frame per second is enough because the banner stays for several seconds
    await execFileAsync('ffmpeg', [
      '-v', 'error', '-t', String(PROMO_SCAN_SECONDS), '-i', gifPath,
      '-vf', 'fps=1', join(dir, 'f%02d.png')
    ]);

    for (const file of readdirSync(dir).sort()) {
      // tesseract needs to run from the file's directory (macOS path issue)
      const { stdout } = await execFileAsync('tesseract', [file, 'stdout'], { cwd: dir });
      const pattern = PROMO_PATTERNS.find(p => p.test(stdout));
      if (pattern) return stdout.match(pattern)[0];
    }
    return null;
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// Reads the frames from `gifsicle --info`. ffmpeg stores a frame that repeats the
// previous one as a 1x1 transparent pixel, so such a frame changes nothing on screen.
function readFrames(info) {
  return info
    .split(/^\s*\+ image #/m)
    .slice(1)
    .map(block => {
      const header = block.match(/^(\d+) (\d+)x(\d+)([^\n]*)/);
      if (!header) return null;
      const [, index, width, height, rest] = header;
      const delay = block.match(/delay ([\d.]+)s/);
      return {
        index: Number(index),
        isRepeat: width === '1' && height === '1' && rest.includes('transparent'),
        centiseconds: delay ? Math.round(parseFloat(delay[1]) * 100) : 0
      };
    })
    .filter(Boolean);
}

// Shortens every stretch of repeated frames to maxStaticSeconds, so a fixed wait
// for a fast response does not leave a frozen screen. Frames that change the
// screen stay as they are. Returns the number of seconds removed.
async function trimStaticFrames(gifPath, maxStaticSeconds = MAX_STATIC_SECONDS) {
  const { stdout } = await execFileAsync('gifsicle', ['--info', gifPath], { maxBuffer: 64 * 1024 * 1024 });
  const maxCentiseconds = Math.round(maxStaticSeconds * 100);

  const ranges = []; // [first, last] indexes of the frames to delete
  let removed = 0;
  let kept = 0; // time kept so far in the current stretch of repeated frames

  for (const frame of readFrames(stdout)) {
    if (!frame.isRepeat) {
      kept = 0;
    } else if (kept + frame.centiseconds <= maxCentiseconds) {
      kept += frame.centiseconds;
    } else {
      const last = ranges[ranges.length - 1];
      if (last && last[1] === frame.index - 1) last[1] = frame.index;
      else ranges.push([frame.index, frame.index]);
      removed += frame.centiseconds;
    }
  }

  if (ranges.length === 0) return 0;

  const trimmedPath = `${gifPath}.trimmed`;
  try {
    await execFileAsync('gifsicle', [
      gifPath,
      '--delete', ...ranges.map(([first, last]) => (first === last ? `#${first}` : `#${first}-${last}`)),
      '-o', trimmedPath
    ]);
    renameSync(trimmedPath, gifPath);
  } catch (e) {
    rmSync(trimmedPath, { force: true });
    throw e;
  }
  return removed / 100;
}

module.exports = { findPromoBanner, trimStaticFrames, MAX_STATIC_SECONDS };
