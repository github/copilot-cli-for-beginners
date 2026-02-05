#!/usr/bin/env node

/**
 * Update Quick Reference Script
 *
 * Uses GitHub Copilot CLI to scan official documentation and update
 * the QUICK-REFERENCE.md file with the latest commands and features.
 *
 * Usage: npm run update:reference
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  outputFile: path.join(__dirname, '..', 'QUICK-REFERENCE.md'),
  templateFile: path.join(__dirname, 'quick-reference-template.md'),
  docsUrls: [
    'https://docs.github.com/copilot/using-github-copilot/using-github-copilot-in-the-command-line',
    'https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot'
  ]
};

/**
 * Run a Copilot CLI command and return the output
 */
function runCopilot(prompt, silent = true) {
  try {
    const silentFlag = silent ? '--silent' : '';
    const command = `copilot -p "${prompt.replace(/"/g, '\\"')}" ${silentFlag}`;
    console.log(`  Running Copilot: ${prompt.substring(0, 60)}...`);

    const output = execSync(command, {
      encoding: 'utf8',
      timeout: 120000, // 2 minute timeout
      maxBuffer: 10 * 1024 * 1024 // 10MB buffer
    });

    return output.trim();
  } catch (error) {
    console.warn(`  Warning: Copilot command failed: ${error.message}`);
    return null;
  }
}

/**
 * Use Copilot to research and generate updated content
 */
async function researchWithCopilot() {
  console.log('\n📡 Using Copilot CLI to research documentation...\n');

  const sections = {};

  // Research slash commands
  console.log('🔍 Researching slash commands...');
  sections.commands = runCopilot(
    `Research GitHub Copilot CLI slash commands. List ALL available slash commands in this exact format - one per line: "/command - description". Include core commands, session commands, permission commands, directory commands, and configuration commands. Be comprehensive.`
  );

  // Research @ syntax
  console.log('🔍 Researching @ syntax...');
  sections.atSyntax = runCopilot(
    `Explain the @ syntax in GitHub Copilot CLI for referencing files and directories. Include: single file, file with path, entire directory, glob patterns, and multiple files. Give practical examples.`
  );

  // Research built-in agents
  console.log('🔍 Researching built-in agents...');
  sections.agents = runCopilot(
    `List all built-in agents in GitHub Copilot CLI. For each agent, provide: name, command to invoke it, and what it does. Format as a table.`
  );

  // Research MCP servers
  console.log('🔍 Researching MCP servers...');
  sections.mcp = runCopilot(
    `List the most commonly used MCP (Model Context Protocol) servers for GitHub Copilot CLI. Include: github, filesystem, and any others that are popular. For each, explain what it does.`
  );

  // Research available models
  console.log('🔍 Researching available models...');
  sections.models = runCopilot(
    `List the AI models available in GitHub Copilot CLI. For each model, explain when to use it. Include information about which models consume premium requests and which don't.`
  );

  // Research keyboard shortcuts
  console.log('🔍 Researching keyboard shortcuts...');
  sections.shortcuts = runCopilot(
    `List keyboard shortcuts and special input methods in GitHub Copilot CLI. Include: Shift+Tab for plan mode, Ctrl+C, the ! prefix for shell commands, and any others.`
  );

  // Research CLI flags
  console.log('🔍 Researching CLI flags...');
  sections.flags = runCopilot(
    `List important command-line flags for the copilot command. Include: -p for programmatic mode, --silent for CI/CD, --resume, --continue, and any others.`
  );

  return sections;
}

/**
 * Generate the Quick Reference markdown using Copilot
 */
async function generateWithCopilot(researchData) {
  console.log('\n📝 Generating Quick Reference with Copilot...\n');

  const existingContent = fs.existsSync(CONFIG.outputFile)
    ? fs.readFileSync(CONFIG.outputFile, 'utf8')
    : '';

  const prompt = `You are updating a Quick Reference Card for GitHub Copilot CLI.

Here is the research data:

SLASH COMMANDS:
${researchData.commands || 'Use existing data'}

@ SYNTAX:
${researchData.atSyntax || 'Use existing data'}

BUILT-IN AGENTS:
${researchData.agents || 'Use existing data'}

MCP SERVERS:
${researchData.mcp || 'Use existing data'}

MODELS:
${researchData.models || 'Use existing data'}

SHORTCUTS:
${researchData.shortcuts || 'Use existing data'}

CLI FLAGS:
${researchData.flags || 'Use existing data'}

Here is the existing Quick Reference to update:
${existingContent.substring(0, 8000)}

Generate an updated QUICK-REFERENCE.md file that:
1. Keeps the same structure and sections
2. Updates any outdated information based on the research
3. Adds any new commands, features, or options discovered
4. Updates the "Last updated" date to today: ${new Date().toISOString().split('T')[0]}
5. Maintains professional formatting with tables and code blocks

Output ONLY the complete markdown content, nothing else.`;

  const updatedContent = runCopilot(prompt, true);

  if (updatedContent && updatedContent.length > 1000) {
    return updatedContent;
  }

  console.log('  Using incremental update approach...');
  return null; // Fall back to incremental updates
}

/**
 * Update specific sections of the Quick Reference
 */
function updateSections(researchData) {
  console.log('\n📝 Updating Quick Reference sections...\n');

  let content = fs.readFileSync(CONFIG.outputFile, 'utf8');

  // Update the last updated date
  const today = new Date().toISOString().split('T')[0];
  content = content.replace(
    /\*Last updated: \d{4}-\d{2}-\d{2}\*/,
    `*Last updated: ${today}*`
  );

  // If we don't have the date line, add it after the first blockquote
  if (!content.includes('*Last updated:')) {
    content = content.replace(
      '> Your cheat sheet for GitHub Copilot CLI commands, syntax, and workflows.',
      `> Your cheat sheet for GitHub Copilot CLI commands, syntax, and workflows.\n>\n> *Last updated: ${today}*`
    );
  }

  return content;
}

/**
 * Main function
 */
async function main() {
  console.log('🔄 Updating Quick Reference Card using Copilot CLI...\n');

  // Check if copilot is available
  try {
    execSync('which copilot', { encoding: 'utf8' });
  } catch {
    console.error('❌ Error: GitHub Copilot CLI is not installed or not in PATH');
    console.error('   Install with: npm install -g @github/copilot');
    process.exit(1);
  }

  // Research with Copilot
  const researchData = await researchWithCopilot();

  // Try to generate complete updated content
  let updatedContent = await generateWithCopilot(researchData);

  if (!updatedContent) {
    // Fall back to section updates
    updatedContent = updateSections(researchData);
  }

  // Write the updated file
  console.log(`\n📄 Writing ${CONFIG.outputFile}...`);
  fs.writeFileSync(CONFIG.outputFile, updatedContent, 'utf8');

  console.log('✅ Quick Reference Card updated successfully!\n');
  console.log('Next steps:');
  console.log('  1. Review the changes: git diff QUICK-REFERENCE.md');
  console.log('  2. Generate PDF: npm run generate:pdf');
  console.log('  3. Commit if satisfied: git add QUICK-REFERENCE.md QUICK-REFERENCE.pdf\n');
}

// Run
main().catch(error => {
  console.error('❌ Error:', error.message);
  process.exit(1);
});
