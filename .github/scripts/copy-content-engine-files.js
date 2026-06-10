#!/usr/bin/env node
/**
 * Copy the course content subset required by the CSE content engine.
 *
 * Usage:
 *   npm run copy:content-engine
 */

const {
  cpSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} = require('fs');
const { dirname, join, relative, resolve } = require('path');

const sourceRoot = process.cwd();
const destinationRoot = '/Users/danwahlin/Desktop/projects/cse-content-engine/content/learning-pathways/copilot-cli-for-beginners';
const destinationParent = dirname(destinationRoot);
const contentEngineSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  type: 'object',
  properties: {
    aliases: {
      type: 'array',
      description: 'Relative paths to redirect to this item',
      items: {
        type: 'string',
        description: 'A relative path to redirect to this item',
      },
    },
    audience: {
      type: 'string',
      description: 'The intended audience for the guide',
    },
    description: {
      type: 'string',
      description: 'A brief description of the item',
    },
    icon: {
      type: 'string',
      description: 'An icon to represent the item',
    },
    id: {
      type: 'string',
      description: 'A unique identifier for the guide',
    },
    params: {
      type: 'object',
      description: "Flexible parameters that don't affect presentation",
    },
    slug: {
      type: 'string',
      description: 'A kebab-case identifier',
    },
    title: {
      type: 'string',
      description: 'The display name of the item',
    },
    weight: {
      type: 'integer',
      description: 'The order to display the item in',
    },
  },
  required: ['title', 'description', 'weight'],
  additionalProperties: true,
};

function log(message) {
  console.log(`  ${message}`);
}

function fail(message) {
  console.error(`\nError: ${message}`);
  process.exit(1);
}

function ensureSafeDestination() {
  if (!existsSync(destinationParent)) {
    fail(`Destination parent does not exist: ${destinationParent}`);
  }

  const resolvedSource = resolve(sourceRoot);
  const resolvedDestination = resolve(destinationRoot);

  if (resolvedSource === resolvedDestination) {
    fail('Destination cannot be the source repository root.');
  }

  if (resolvedDestination.startsWith(`${resolvedSource}/`)) {
    fail('Destination cannot be inside the source repository.');
  }
}

function copyFile(sourcePath, destinationPath) {
  mkdirSync(dirname(destinationPath), { recursive: true });

  if (sourcePath.endsWith('.md')) {
    writeFileSync(destinationPath, prepareMarkdownForContentEngine(sourcePath), 'utf8');
  } else {
    cpSync(sourcePath, destinationPath);
  }

  log(`Copied ${relative(sourceRoot, sourcePath)} -> ${relative(destinationRoot, destinationPath)}`);
}

function prepareMarkdownForContentEngine(sourcePath) {
  const markdown = readFileSync(sourcePath, 'utf8');
  const frontmatter = getMarkdownFrontmatter(markdown);

  if (!frontmatter) {
    return markdown;
  }

  return markdown.replace(/^<!--\r?\n---\r?\n[\s\S]*?\r?\n---\r?\n-->\r?\n*/, `---\n${frontmatter}\n---\n\n`);
}

function getMarkdownFrontmatter(markdown) {
  const hiddenFrontmatter = markdown.match(/^<!--\r?\n---\r?\n([\s\S]*?)\r?\n---\r?\n-->/)?.[1];
  const visibleFrontmatter = markdown.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1];

  return (hiddenFrontmatter ?? visibleFrontmatter)?.replace(/\r\n/g, '\n');
}

function getFrontmatterField(frontmatter, field) {
  return frontmatter.match(new RegExp(`^${field}:.*$`, 'm'))?.[0];
}

function writeIndexFromReadme(sourceReadmePath, destinationDirectory, extraFields = []) {
  const markdown = readFileSync(sourceReadmePath, 'utf8');
  const frontmatter = getMarkdownFrontmatter(markdown);

  if (!frontmatter) {
    fail(`Cannot create index.yml because ${relative(sourceRoot, sourceReadmePath)} has no frontmatter.`);
  }

  const indexFields = ['title', 'description', 'slug', 'weight', 'icon']
    .map((field) => getFrontmatterField(frontmatter, field))
    .filter(Boolean);
  indexFields.push(...extraFields);

  if (indexFields.length === 0) {
    fail(`Cannot create index.yml because ${relative(sourceRoot, sourceReadmePath)} has no index metadata.`);
  }

  mkdirSync(destinationDirectory, { recursive: true });
  writeFileSync(join(destinationDirectory, 'index.yml'), `${indexFields.join('\n')}\n`, 'utf8');
  log(`Generated ${relative(destinationRoot, join(destinationDirectory, 'index.yml'))}`);
}

function writeContentEngineSchema() {
  const destinationPath = join(destinationRoot, 'schema.json');
  writeFileSync(destinationPath, `${JSON.stringify(contentEngineSchema, null, 2)}\n`, 'utf8');
  log(`Generated ${relative(destinationRoot, destinationPath)}`);
}

function copyDirectory(sourcePath, destinationPath) {
  if (!existsSync(sourcePath)) {
    fail(`Required directory does not exist: ${relative(sourceRoot, sourcePath)}`);
  }

  cpSync(sourcePath, destinationPath, { recursive: true });
  log(`Copied ${relative(sourceRoot, sourcePath)}/ -> ${relative(destinationRoot, destinationPath)}/`);
}

function getChapterFolders() {
  return readdirSync(sourceRoot)
    .filter((entry) => /^0[0-7]-/.test(entry))
    .filter((entry) => statSync(join(sourceRoot, entry)).isDirectory())
    .sort();
}

function stripFragmentAndQuery(target) {
  return target.split('#')[0].split('?')[0];
}

function isExternalLink(target) {
  return /^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith('//') || target.startsWith('#');
}

function getChapterLocalMarkdownLinks(chapterPath) {
  const readmePath = join(chapterPath, 'README.md');
  const readme = readFileSync(readmePath, 'utf8');
  const links = new Set();
  const patterns = [
    /\[[^\]]+\]\(([^)\s]+\.md(?:#[^)]+)?)(?:\s+"[^"]*")?\)/gi,
    /<a\b[^>]*\bhref=["']([^"']+\.md(?:#[^"']+)?)["']/gi,
  ];

  for (const pattern of patterns) {
    for (const match of readme.matchAll(pattern)) {
      const target = stripFragmentAndQuery(match[1]);
      if (!target || isExternalLink(target)) {
        continue;
      }

      const resolvedTarget = resolve(chapterPath, target);
      if (dirname(resolvedTarget) === resolve(chapterPath) && resolvedTarget !== resolve(readmePath)) {
        links.add(resolvedTarget);
      }
    }
  }

  return [...links].sort();
}

function copyAppendices() {
  const sourceAppendices = join(sourceRoot, 'appendices');
  const destinationAppendices = join(destinationRoot, 'appendices');

  if (!existsSync(sourceAppendices)) {
    fail('Required appendices directory does not exist.');
  }

  writeIndexFromReadme(join(sourceAppendices, 'README.md'), destinationAppendices);

  for (const markdownFile of findMarkdownFiles(sourceAppendices)) {
    copyFile(markdownFile, join(destinationAppendices, relative(sourceAppendices, markdownFile)));
  }
}

function copyCourseContent() {
  console.log(`Overlaying course content into:\n${destinationRoot}\n`);

  mkdirSync(destinationRoot, { recursive: true });

  copyFile(join(sourceRoot, 'README.md'), join(destinationRoot, 'README.md'));
  writeContentEngineSchema();
  writeIndexFromReadme(join(sourceRoot, 'README.md'), destinationRoot, ['icon: CopilotIcon']);
  copyDirectory(join(sourceRoot, 'assets'), join(destinationRoot, 'assets'));

  for (const chapterFolder of getChapterFolders()) {
    const sourceChapter = join(sourceRoot, chapterFolder);
    const destinationChapter = join(destinationRoot, chapterFolder);

    mkdirSync(destinationChapter, { recursive: true });
    copyFile(join(sourceChapter, 'README.md'), join(destinationChapter, 'README.md'));
    writeIndexFromReadme(join(sourceChapter, 'README.md'), destinationChapter);
    copyDirectory(join(sourceChapter, 'assets'), join(destinationChapter, 'assets'));

    for (const linkedMarkdown of getChapterLocalMarkdownLinks(sourceChapter)) {
      copyFile(linkedMarkdown, join(destinationChapter, relative(sourceChapter, linkedMarkdown)));
    }
  }

  copyAppendices();
}

function findMarkdownFiles(directory) {
  const files = [];

  for (const entry of readdirSync(directory)) {
    const path = join(directory, entry);
    const stat = statSync(path);

    if (stat.isDirectory()) {
      files.push(...findMarkdownFiles(path));
    } else if (entry.endsWith('.md')) {
      files.push(path);
    }
  }

  return files;
}

function validateMarkdownImagePaths() {
  const imagePatterns = [
    /!\[[^\]]*]\(([^)\s]+)(?:\s+"[^"]*")?\)/g,
    /<img\b[^>]*\bsrc=["']([^"']+)["']/gi,
  ];
  const brokenLinks = [];

  for (const markdownFile of findMarkdownFiles(destinationRoot)) {
    const markdown = readFileSync(markdownFile, 'utf8');

    for (const pattern of imagePatterns) {
      for (const match of markdown.matchAll(pattern)) {
        const target = stripFragmentAndQuery(match[1]);
        if (!target || isExternalLink(target)) {
          continue;
        }

        const resolvedTarget = target.startsWith('/')
          ? join(destinationRoot, target.slice(1))
          : resolve(dirname(markdownFile), target);

        if (!existsSync(resolvedTarget)) {
          const line = markdown.slice(0, match.index).split('\n').length;
          brokenLinks.push(`${relative(destinationRoot, markdownFile)}:${line} -> ${target}`);
        }
      }
    }
  }

  if (brokenLinks.length > 0) {
    fail(`Broken copied Markdown image references:\n${brokenLinks.join('\n')}`);
  }

  console.log('\nValidation passed: all copied Markdown image references resolve.');
}

function validateMarkdownFrontmatter() {
  const requiredFields = contentEngineSchema.required ?? [];
  const missingFrontmatter = [];

  for (const markdownFile of findMarkdownFiles(destinationRoot)) {
    const markdown = readFileSync(markdownFile, 'utf8');
    const frontmatter = markdown.match(/^---\n([\s\S]*?)\n---\n/)?.[1];
    const relativePath = relative(destinationRoot, markdownFile);

    if (!frontmatter) {
      missingFrontmatter.push(`${relativePath}: missing frontmatter`);
      continue;
    }

    const missingFields = requiredFields.filter(
      (field) => !new RegExp(`^${field}:`, 'm').test(frontmatter),
    );

    if (missingFields.length > 0) {
      missingFrontmatter.push(`${relativePath}: missing ${missingFields.join(', ')}`);
    }
  }

  if (missingFrontmatter.length > 0) {
    fail(`Copied Markdown frontmatter does not match schema requirements:\n${missingFrontmatter.join('\n')}`);
  }

  console.log('Validation passed: copied Markdown frontmatter includes required schema fields.');
}

ensureSafeDestination();
copyCourseContent();
validateMarkdownFrontmatter();
validateMarkdownImagePaths();
console.log('\nDone.');
