#!/usr/bin/env node
/**
 * Generate .tape files from demos.json configuration
 *
 * Supports single-prompt and multi-prompt demos:
 *   - "prompt": "text"              → single prompt
 *   - "prompts": ["a", "b"]         → multi-prompt (default responseWait each)
 *   - "prompts": [{ "text": "a", "responseWait": 10 }, "b"]  → mixed with overrides
 *   - "setup": ["cmd", "cmd"]       → shell commands that run before copilot
 *                                     starts. The recording hides them. They
 *                                     can use $DEMO_SCRATCH_DIR for temporary
 *                                     files (generate-demos.js sets it).
 *
 * Usage: npm run create:tapes
 */

const { writeFileSync, mkdirSync, existsSync } = require('fs');
const { join } = require('path');

const rootDir = join(__dirname, '..', '..');
const config = require('./demos.json');

function generatePromptBlock(entry, defaultWait, index) {
  const text = typeof entry === 'string' ? entry : entry.text;
  const wait = (typeof entry === 'object' && entry.responseWait) || defaultWait;
  const agentSelect = typeof entry === 'object' && entry.agentSelect;
  const label = index != null ? `Prompt ${index + 1}` : 'Execute the prompt';

  // Agent selection: type /agent, wait for picker, arrow down to agent, select
  if (agentSelect) {
    const arrowDown = (typeof entry === 'object' && entry.arrowDown) || 0;
    const arrowBlock = arrowDown > 0 ? `Down ${arrowDown}\nSleep 1s\n` : '';
    return `# ${label} - Select ${agentSelect} agent
Type "${text}"
Sleep 1s
Enter

# Wait for agent picker
Sleep 3s
${arrowBlock}Enter

# Wait for agent to load
Sleep ${wait}s`;
  }

  // If prompt ends with a file reference (@path), the file picker will be open.
  // Need an extra Enter to select the file before submitting the prompt.
  const endsWithFileRef = /@\S+$/.test(text);
  const enterBlock = endsWithFileRef
    ? 'Enter\nSleep 1s\nEnter'
    : 'Enter';

  // VHS Type command must be single-line; split multi-line prompts
  const lines = text.split('\n');
  let typeBlock;
  if (lines.length > 1) {
    typeBlock = lines
      .map((line, i) => i < lines.length - 1 ? `Type "${line}"\nEnter` : `Type "${line}"`)
      .join('\n');
  } else {
    typeBlock = `Type "${text}"`;
  }

  // Break response wait into chunks with periodic hidden nudges.
  // A hidden space+backspace forces copilot's TUI to scroll to the input area.
  const nudgeInterval = 3;
  let waitBlock = '';
  let remaining = wait;
  while (remaining > nudgeInterval) {
    waitBlock += `Sleep ${nudgeInterval}s\nHide\nType " "\nBackspace\nShow\n`;
    remaining -= nudgeInterval;
  }
  if (remaining > 0) {
    waitBlock += `Sleep ${remaining}s`;
  }

  return `# ${label}
${typeBlock}
Sleep 2s
${enterBlock}

# Wait for response (with periodic nudges to keep input visible)
${waitBlock}`;
}

// Setup commands run in the tape's shell before copilot starts. The commands
// join with "&&", so a failed command skips the final "clear" and leaves its
// error on screen.
function generateSetupBlock(setup) {
  if (!Array.isArray(setup) || setup.length === 0) {
    return '';
  }

  const command = [...setup, 'clear'].join(' && ');
  // VHS strings have no escape character, so a single quote would end the string.
  if (command.includes("'")) {
    throw new Error(`Setup commands cannot contain single quotes: ${command}`);
  }

  return `# Setup (hidden from the recording)
Hide
Type@5ms '${command}'
Enter
Sleep 2s
Show

`;
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
Set Framerate ${s.framerate}

# Human typing speed
Set TypingSpeed ${s.typingSpeed}

${generateSetupBlock(demo.setup)}# Launch copilot
Type "copilot"
Enter

# Wait for copilot to start
Sleep ${s.startupWait}s

${promptBlocks}

# Nudge TUI to scroll to input area
Type " "
Backspace
Sleep ${s.exitWait}s

# Exit cleanly
Ctrl+C
Sleep 1s
`;
}

// Main
console.log('📝 Creating tape files from demos.json...\n');

let created = 0;

for (const demo of config.demos) {
  const assetsDir = join(rootDir, demo.chapter, 'assets');
  const tapePath = join(assetsDir, `${demo.name}.tape`);

  // Ensure assets directory exists
  if (!existsSync(assetsDir)) {
    mkdirSync(assetsDir, { recursive: true });
    console.log(`  Created: ${demo.chapter}/assets/`);
  }

  // Generate tape content
  const content = generateTapeContent(demo, config.settings);

  // Write tape file
  writeFileSync(tapePath, content);
  console.log(`  ✓ ${demo.chapter}/assets/${demo.name}.tape`);
  created++;
}

console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`✓ Created ${created} tape file(s)`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`\nNext: npm run generate:vhs`);
