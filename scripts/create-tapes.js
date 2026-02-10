#!/usr/bin/env node
/**
 * Generate .tape files from demos.json configuration
 *
 * Supports single-prompt and multi-prompt demos:
 *   - "prompt": "text"              → single prompt
 *   - "prompts": ["a", "b"]         → multi-prompt (default responseWait each)
 *   - "prompts": [{ "text": "a", "responseWait": 10 }, "b"]  → mixed with overrides
 *
 * Usage: npm run create:tapes
 */

const { writeFileSync, mkdirSync, existsSync } = require('fs');
const { join } = require('path');

const rootDir = join(__dirname, '..');
const config = require('./demos.json');

function generatePromptBlock(entry, defaultWait, index) {
  const text = typeof entry === 'string' ? entry : entry.text;
  const wait = (typeof entry === 'object' && entry.responseWait) || defaultWait;
  const label = index != null ? `Prompt ${index + 1}` : 'Execute the prompt';

  // If prompt ends with a file reference (@path), the file picker will be open.
  // Need an extra Enter to select the file before submitting the prompt.
  const endsWithFileRef = /@\S+$/.test(text);
  const enterBlock = endsWithFileRef
    ? 'Enter\nSleep 1s\nEnter'
    : 'Enter';

  return `# ${label}
Type "${text}"
Sleep 2s
${enterBlock}

# Wait for response
Sleep ${wait}s`;
}

function generateTapeContent(demo, settings) {
  const s = { ...settings, ...demo }; // Allow per-demo overrides

  // Build prompt blocks from either "prompt" (single) or "prompts" (array)
  let promptBlocks;
  if (demo.prompts && Array.isArray(demo.prompts)) {
    promptBlocks = demo.prompts
      .map((entry, i) => generatePromptBlock(entry, s.responseWait, i))
      .join('\n\n');
  } else {
    promptBlocks = generatePromptBlock(demo.prompt, s.responseWait);
  }

  return `# ${demo.chapter}: ${demo.description}
# Auto-generated from demos.json - Real copilot execution

Output ${demo.name}.gif

Set FontSize ${s.fontSize}
Set Width ${s.width}
Set Height ${s.height}
Set Theme "${s.theme}"
Set Padding 20
Set BorderRadius 8
Set Margin 10
Set MarginFill "#282a36"

# Human typing speed
Set TypingSpeed ${s.typingSpeed}

# Launch copilot
Type "copilot"
Enter

# Wait for copilot to start
Sleep ${s.startupWait}s

${promptBlocks}

# Exit cleanly
Ctrl+C
Sleep ${s.exitWait}s
`;
}

// Main
console.log('📝 Creating tape files from demos.json...\n');

let created = 0;

for (const demo of config.demos) {
  const imagesDir = join(rootDir, demo.chapter, 'images');
  const tapePath = join(imagesDir, `${demo.name}.tape`);

  // Ensure images directory exists
  if (!existsSync(imagesDir)) {
    mkdirSync(imagesDir, { recursive: true });
    console.log(`  Created: ${demo.chapter}/images/`);
  }

  // Generate tape content
  const content = generateTapeContent(demo, config.settings);

  // Write tape file
  writeFileSync(tapePath, content);
  console.log(`  ✓ ${demo.chapter}/images/${demo.name}.tape`);
  created++;
}

console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`✓ Created ${created} tape file(s)`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`\nNext: npm run generate:vhs`);
