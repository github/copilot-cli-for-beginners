#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const repoRoot = process.cwd();
const languages = process.argv
  .slice(2)
  .flatMap((value) => value.split(/\s+/))
  .map((value) => value.trim())
  .filter(Boolean);

if (languages.length === 0) {
  console.error("Usage: node .github/scripts/fix-translated-markdown.js <language-codes>");
  process.exit(1);
}

const tableHeadersByLanguage = {
  es: "| Capítulo | Título | Lo que construirás |",
  ko: "| 장 | 제목 | 만들 내용 |",
  ja: "| 章 | タイトル | 作成するもの |",
  "zh-CN": "| 章节 | 标题 | 你将构建的内容 |",
};

const allFiles = new Set(walkFiles(repoRoot).map(toPosixRelative));
const errors = [];
let changedFiles = 0;

for (const language of languages) {
  const translationRoot = path.join(repoRoot, "translations", language);

  if (!fs.existsSync(translationRoot)) {
    console.log(`No translations found for ${language}; skipping.`);
    continue;
  }

  const markdownFiles = walkFiles(translationRoot).filter((file) => file.endsWith(".md"));

  for (const filePath of markdownFiles) {
    const original = fs.readFileSync(filePath, "utf8");
    const fixed = fixMarkdown(original, filePath, language);

    if (fixed !== original) {
      fs.writeFileSync(filePath, fixed);
      changedFiles += 1;
      console.log(`Fixed translated Markdown: ${toPosixRelative(filePath)}`);
    }

    validateMarkdown(fixed, filePath, language);
  }
}

if (errors.length > 0) {
  console.error("\nTranslated Markdown validation failed:");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Translated Markdown cleanup complete. Files changed: ${changedFiles}`);

function fixMarkdown(content, filePath, language) {
  let fixed = fixKnownTableHeaders(content, language);
  const headingSlugs = getHeadingSlugs(fixed);
  const headingSlugList = getHeadingSlugList(fixed);
  const sourceFile = getSourceFileForTranslation(filePath, language);

  fixed = fixed.replace(/\[([^\]\n]+)\]\((#[^)]+)\)/g, (match, label, destination) => {
    const currentSlug = destination.slice(1);

    if (headingSlugs.has(currentSlug)) {
      return match;
    }

    const labelSlug = slugifyHeading(label);

    if (headingSlugs.has(labelSlug)) {
      return `[${label}](#${labelSlug})`;
    }

    const candidates = [...headingSlugs].filter(
      (slug) => slug.startsWith(`${labelSlug}-`) || labelSlug.startsWith(`${slug}-`),
    );

    if (candidates.length === 1) {
      return `[${label}](#${candidates[0]})`;
    }

    const sourceHeadingIndex = getSourceHeadingIndex(sourceFile, currentSlug);

    if (sourceHeadingIndex !== -1 && sourceHeadingIndex < headingSlugList.length) {
      return `[${label}](#${headingSlugList[sourceHeadingIndex]})`;
    }

    return match;
  });

  return fixed.replace(/(\]\()([^)]+)(\))/g, (_match, prefix, destination, suffix) => {
    return `${prefix}${fixDestination(destination, filePath, language)}${suffix}`;
  });
}

function fixKnownTableHeaders(content, language) {
  const translatedHeader = tableHeadersByLanguage[language];

  if (!translatedHeader) {
    return content;
  }

  return content.replace(
    /^\|\s*Chapter\s*\|\s*Title\s*\|\s*What You'll Build\s*\|$/gm,
    translatedHeader,
  );
}

function fixDestination(destination, filePath, language) {
  if (isExternal(destination) || destination.startsWith("#") || destination.startsWith("<")) {
    return destination;
  }

  const { target, fragment } = splitDestination(destination);

  if (!target || target.startsWith("#")) {
    return destination;
  }

  const translatedDir = path.posix.dirname(toPosixRelative(filePath));
  const currentTarget = normalizePosix(path.posix.join(translatedDir, target));
  const translatedRoot = `translations/${language}`;
  const sourceRelativeFile = path.posix.relative(translatedRoot, toPosixRelative(filePath));
  const sourceDir = path.posix.dirname(sourceRelativeFile);
  const sourceTarget = normalizePosix(path.posix.join(sourceDir, target));

  if (pathExists(currentTarget)) {
    return `${target}${fixCrossFileFragment(fragment, sourceTarget, currentTarget)}`;
  }

  if (!pathExists(sourceTarget)) {
    return destination;
  }

  const translatedTarget = normalizePosix(path.posix.join(translatedRoot, sourceTarget));
  const preferredTarget = pathExists(translatedTarget) ? translatedTarget : sourceTarget;
  const relativeTarget = path.posix.relative(translatedDir, preferredTarget) || ".";
  const normalizedTarget = relativeTarget.startsWith(".") ? relativeTarget : `./${relativeTarget}`;

  return `${normalizedTarget}${fixCrossFileFragment(fragment, sourceTarget, preferredTarget)}`;
}

function validateMarkdown(content, filePath, language) {
  const fileRelative = toPosixRelative(filePath);
  const fileDir = path.posix.dirname(fileRelative);
  const headingSlugs = getHeadingSlugs(content);
  const sourceFile = getSourceFileForTranslation(filePath, language);

  for (const destination of getDestinations(content)) {
    if (isExternal(destination) || destination.startsWith("<")) {
      continue;
    }

    const { target, fragment } = splitDestination(destination);

    if (!target) {
      const slug = fragment.slice(1);

      if (
        slug &&
        !headingSlugs.has(slug) &&
        getSourceHeadingIndex(sourceFile, slug) !== -1
      ) {
        errors.push(`${fileRelative} links to missing heading #${slug}`);
      }

      continue;
    }

    const resolvedTarget = normalizePosix(path.posix.join(fileDir, target));

    if (!pathExists(resolvedTarget)) {
      const sourceTarget = getSourceTargetForDestination(filePath, language, target);

      if (sourceTarget && !pathExists(sourceTarget)) {
        continue;
      }

      errors.push(`${fileRelative} links to missing file ${destination}`);
      continue;
    }

    // Cross-file heading anchors are best-effort fixed above by mapping source
    // heading order to translated heading order. Avoid failing on anchors that
    // come from generated HTML IDs or pre-existing source content.
  }
}

function getDestinations(content) {
  const destinations = [];
  const pattern = /\]\(([^)]+)\)/g;
  let match;

  while ((match = pattern.exec(content)) !== null) {
    destinations.push(match[1]);
  }

  return destinations;
}

function getHeadingSlugs(content) {
  return new Set(getHeadingSlugList(content));
}

function getHeadingSlugList(content) {
  return getHeadingSlugListWith(content, slugifyHeading);
}

function getSourceHeadingIndex(sourceFile, slug) {
  if (!sourceFile || !pathExists(sourceFile)) {
    return -1;
  }

  const sourceContent = fs.readFileSync(path.join(repoRoot, sourceFile), "utf8");
  const slugLists = [
    getHeadingSlugListWith(sourceContent, slugifyHeading),
    getHeadingSlugListWith(sourceContent, slugifyGitHubHeading),
  ];

  for (const slugs of slugLists) {
    const index = slugs.indexOf(slug);

    if (index !== -1) {
      return index;
    }
  }

  return -1;
}

function getHeadingSlugListWith(content, slugifier) {
  const slugs = new Map();
  const result = [];

  for (const line of content.split(/\r?\n/)) {
    const match = /^(#{1,6})\s+(.+?)\s*$/.exec(line);

    if (!match) {
      continue;
    }

    const baseSlug = slugifier(match[2]);
    const count = slugs.get(baseSlug) || 0;
    const slug = count === 0 ? baseSlug : `${baseSlug}-${count}`;
    slugs.set(baseSlug, count + 1);
    result.push(slug);
  }

  return result;
}

function fixCrossFileFragment(fragment, sourceTarget, translatedTarget) {
  if (!fragment || !sourceTarget.endsWith(".md") || !translatedTarget.endsWith(".md")) {
    return fragment;
  }

  if (!pathExists(sourceTarget) || !pathExists(translatedTarget)) {
    return fragment;
  }

  const currentSlug = fragment.slice(1);
  const translatedContent = fs.readFileSync(path.join(repoRoot, translatedTarget), "utf8");
  const translatedSlugs = getHeadingSlugList(translatedContent);

  if (translatedSlugs.includes(currentSlug)) {
    return fragment;
  }

  const sourceContent = fs.readFileSync(path.join(repoRoot, sourceTarget), "utf8");
  const sourceSlugs = getHeadingSlugList(sourceContent);
  const sourceIndex = sourceSlugs.indexOf(currentSlug);

  if (sourceIndex === -1 || sourceIndex >= translatedSlugs.length) {
    return fragment;
  }

  return `#${translatedSlugs[sourceIndex]}`;
}

function getSourceFileForTranslation(filePath, language) {
  const translatedRoot = `translations/${language}`;
  const sourceFile = path.posix.relative(translatedRoot, toPosixRelative(filePath));

  if (sourceFile.startsWith("..")) {
    return "";
  }

  return sourceFile;
}

function getSourceTargetForDestination(filePath, language, target) {
  const sourceFile = getSourceFileForTranslation(filePath, language);

  if (!sourceFile) {
    return "";
  }

  const sourceDir = path.posix.dirname(sourceFile);
  return normalizePosix(path.posix.join(sourceDir, target));
}

function slugifyHeading(value) {
  return value
    .replace(/<[^>]+>/g, "")
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[`*_~]/g, "")
    .trim()
    .toLocaleLowerCase()
    .replace(/[^\p{Letter}\p{Number}\p{Mark}\s-]/gu, "")
    .trim()
    .replace(/\s+/g, "-");
}

function slugifyGitHubHeading(value) {
  return value
    .replace(/<[^>]+>/g, "")
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[`*_~]/g, "")
    .trim()
    .toLocaleLowerCase()
    .replace(/[^\p{Letter}\p{Number}\p{Mark}\s-]/gu, "")
    .replace(/\s/g, "-");
}

function splitDestination(destination) {
  const hashIndex = destination.indexOf("#");

  if (hashIndex === -1) {
    return { target: destination, fragment: "" };
  }

  return {
    target: destination.slice(0, hashIndex),
    fragment: destination.slice(hashIndex),
  };
}

function isExternal(destination) {
  return /^(https?:|mailto:|tel:)/i.test(destination);
}

function pathExists(relativePath) {
  if (allFiles.has(relativePath)) {
    return true;
  }

  if (fs.existsSync(path.join(repoRoot, relativePath))) {
    return true;
  }

  const indexPath = normalizePosix(path.posix.join(relativePath, "README.md"));
  return allFiles.has(indexPath);
}

function walkFiles(directory) {
  if (!fs.existsSync(directory)) {
    return [];
  }

  const entries = fs.readdirSync(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (entry.name === ".git" || entry.name === "node_modules") {
      continue;
    }

    const entryPath = path.join(directory, entry.name);

    if (entry.isDirectory()) {
      files.push(...walkFiles(entryPath));
    } else if (entry.isFile()) {
      files.push(entryPath);
    }
  }

  return files;
}

function toPosixRelative(filePath) {
  return normalizePosix(path.relative(repoRoot, filePath));
}

function normalizePosix(value) {
  return value.split(path.sep).join(path.posix.sep).replace(/\\/g, "/");
}
