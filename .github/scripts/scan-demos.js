#!/usr/bin/env node
/**
 * Scan chapter README files and extract copilot demo commands
 * Updates .github/scripts/demos.json with found commands
 *
 * Usage: npm run scan:demos
 *
 * To mark a command as the primary demo for a chapter, add a comment:
 *   <!-- demo: chapter-name-demo -->
 *   ```bash
 *   copilot -p "your command"
 *   ```
 *
 * Or it will use the first copilot -p command found in each chapter.
 */

const { readFileSync, writeFileSync, readdirSync, existsSync } = require('fs');
const { join } = require('path');

const rootDir = join(__dirname, '..', '..');
const demosJsonPath = join(__dirname, 'demos.json');

// Default settings for generated tapes
const defaultSettings = {
  fontSize: 18,
  width: 1000,
  height: 600,
  theme: "Dracula",
  typingSpeed: "60ms",
  startupWait: 5,
  responseWait: 25,
  exitWait: 2
};

// Find all chapter directories (XX-chapter-name pattern)
function findChapters() {
  return readdirSync(rootDir)
    .filter(name => /^\d{2}-/.test(name))
    .filter(name => existsSync(join(rootDir, name, 'README.md')))
    .sort();
}

// Extract copilot commands from markdown content
function extractCopilotCommands(content) {
  const commands = [];

  // Look for marked demos first: <!-- demo: name -->
  const markedDemoRegex = /<!--\s*demo:\s*([^\s]+)\s*-->\s*```(?:bash|shell)?\s*([\s\S]*?)```/gi;
  let match;
  while ((match = markedDemoRegex.exec(content)) !== null) {
    const name = match[1];
    const codeBlock = match[2].trim();
    const copilotMatch = codeBlock.match(/copilot(?:\s+-p\s+["'](.+?)["']|\s*$)/);
    if (copilotMatch) {
      commands.push({
        name,
        prompt: copilotMatch[1] || null,
        isInteractive: !copilotMatch[1],
        marked: true
      });
    }
  }

  // If no marked demos, find all copilot -p commands
  if (commands.length === 0) {
    // Match copilot -p "..." or copilot -p '...'
    const programmaticRegex = /copilot\s+-p\s+["']([^"']+)["']/g;
    while ((match = programmaticRegex.exec(content)) !== null) {
      commands.push({
        prompt: match[1],
        isInteractive: false,
        marked: false
      });
    }
  }

  return commands;
}

// Generate demo name from chapter name
function generateDemoName(chapter) {
  // 00-quick-start -> quick-start-demo
  return chapter.replace(/^\d+-/, '') + '-demo';
}

// Extract description from chapter title
function extractDescription(content) {
  const titleMatch = content.match(/^#\s+(.+)$/m);
  if (titleMatch) {
    // "Chapter 01: First Steps" -> "First Steps"
    return titleMatch[1].replace(/^Chapter\s+\d+:\s*/, '').trim();
  }
  return 'Demo';
}

// Main
console.log('🔍 Scanning chapters for copilot commands...\n');

const chapters = findChapters();
const demos = [];

for (const chapter of chapters) {
  const readmePath = join(rootDir, chapter, 'README.md');
  const content = readFileSync(readmePath, 'utf8');

  const commands = extractCopilotCommands(content);
  const description = extractDescription(content);

  if (commands.length > 0) {
    // Use the first (or marked) command
    const cmd = commands.find(c => c.marked) || commands[0];
    const demoName = cmd.name || generateDemoName(chapter);

    const demo = {
      chapter,
      name: demoName,
      description: description + ' demo'
    };

    if (cmd.prompt) {
      demo.prompt = cmd.prompt;
    } else {
      demo.prompt = "What can you help me with? Give a brief summary.";
      demo.note = "Interactive mode - customize this prompt";
    }

    demos.push(demo);
    console.log(`  ✓ ${chapter}`);
    console.log(`    └─ "${demo.prompt.substring(0, 60)}${demo.prompt.length > 60 ? '...' : ''}"`);
  } else {
    console.log(`  ⚠ ${chapter} - No copilot commands found`);
  }
}

// Write demos.json
const output = {
  settings: defaultSettings,
  demos
};

writeFileSync(demosJsonPath, JSON.stringify(output, null, 2) + '\n');

console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`✓ Found ${demos.length} demos`);
console.log(`✓ Updated .github/scripts/demos.json`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`\nNext steps:`);
console.log(`  1. Review/edit .github/scripts/demos.json`);
console.log(`  2. npm run create:tapes`);
console.log(`  3. npm run generate:vhs`);
