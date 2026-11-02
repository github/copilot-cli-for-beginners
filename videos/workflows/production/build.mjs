import fs from "node:fs/promises";
import http from "node:http";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { root, requireTool } from "./tools.mjs";

const { chromium } = requireTool("playwright");
const QRCode = requireTool("qrcode");
const config = JSON.parse(await fs.readFile(resolve(root, "production/timeline.json"), "utf8"));
const assets = resolve(root, "assets/production");
const review = resolve(root, "review");
const stillsOnly = process.argv.includes("--stills");
const output = resolve(root, "renders/workflows-demo-console-1080p.mp4");
await fs.mkdir(resolve(assets, "fonts"), { recursive: true });
await fs.mkdir(review, { recursive: true });
await fs.mkdir(resolve(root, "renders"), { recursive: true });

function assert(condition, message) {
  if (!condition) throw new Error(message);
}
assert(config.width === 1920 && config.height === 1080 && config.fps === 30,
  "This production recipe requires a 1920x1080, 30 fps timeline.");
assert(config.console.width === 1920 && config.console.height + config.console.top === 1080,
  "The full-width console and reserved title strip must exactly fill the output.");

async function run(command, args) {
  const child = spawn(command, args, { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const [code] = await once(child, "close");
  assert(code === 0, `${command} failed (${code}): ${stderr}`);
  return stdout;
}

for (const file of ["MonaSansVF.woff2", "MonaSansMonoVF.woff2", "OFL.txt"]) {
  const destination = resolve(assets, "fonts", file);
  const source = process.env.VIDEO_FONTS ? resolve(process.env.VIDEO_FONTS, file) : destination;
  if (source !== destination) await fs.copyFile(source, destination);
  await fs.access(destination);
}
const mark = process.env.VIDEO_MARK;
if (mark) await fs.copyFile(resolve(mark), resolve(assets, "GitHub_Invertocat_White.svg"));
await fs.access(resolve(assets, "GitHub_Invertocat_White.svg"));
await QRCode.toFile(resolve(assets, "resource-qr.png"), config.resourceUrl, {
  width: 360, margin: config.qr.quietZoneModules, errorCorrectionLevel: "M",
  color: { dark: "#000000", light: "#ffffff" },
});

const workflowOrigin = JSON.parse(await fs.readFile(resolve(root, config.evidence.origin), "utf8"));
const generatedExtension = await fs.readFile(resolve(root, workflowOrigin.extensionFile));
assert(createHash("sha256").update(generatedExtension).digest("hex") === workflowOrigin.extensionSha256
  && workflowOrigin.extensionSha256 === workflowOrigin.executedExtensionSha256,
  "The workflow shown being created must be the unchanged artifact used in the recorded run.");
const creationTranscript = await fs.readFile(resolve(root, workflowOrigin.creationTranscript), "utf8");
assert(creationTranscript.includes("Created and registered book-release-check")
  && creationTranscript.includes("Not run. Application code is unchanged."),
  "The authoring recording must show real creation and registration, not a preloaded workflow.");
const reportText = await fs.readFile(resolve(root, config.evidence.report), "utf8");
const summary = reportText.split("\n").find((line) => line.startsWith("Checks: "));
const gaps = reportText.split("## Two untested behaviors\n")[1]?.trim().split(/\n\n+/)
  .map((line) => line.replace(/^\d+\.\s*/, ""));
assert(reportText.includes("Checks: PASS") && summary && gaps?.length === 2, "The real report is missing or has changed shape. Review its contents before editing the video.");
assert(gaps[0].includes("Corrupted-data recovery") && gaps[0].includes("malformed JSON")
  && gaps[1].includes("Case-insensitive author matching") && gaps[1].includes("find_by_author"),
  "The report's findings changed. Revise the narration and evidence ledger before rebuilding this example.");
await fs.writeFile(resolve(assets, "report.json"), JSON.stringify({ summary, gaps }, null, 2));
const transcript = await fs.readFile(resolve(root, config.evidence.transcript), "utf8");
assert(reportText.includes("5 passed") && transcript.includes("All 5 tests passed")
  && transcript.includes("paused") && transcript.includes("completed"),
  "The source transcript does not contain the expected test, checkpoint, and completion evidence.");

const timecode = (seconds) => {
  const frame = Math.round(seconds * config.fps);
  return [Math.floor(frame / 108000), Math.floor(frame / 1800) % 60, Math.floor(frame / 30) % 60, frame % 30]
    .map((part) => String(part).padStart(2, "0")).join(":");
};
let cursor = 0;
for (const scene of config.scenes) {
  scene.start = cursor;
  scene.end = cursor + scene.duration;
  cursor = scene.end;
  if (scene.shots) {
    const seconds = scene.shots.reduce((sum, shot) => sum + shot.to - shot.from + shot.hold, 0);
    assert(Math.abs(seconds - scene.duration) < 0.001, `${scene.id}: shots do not fit the scene.`);
  }
}
assert(cursor <= config.maximumSeconds, "The edit exceeds the requested duration limit.");
let audioManifest;
try {
  audioManifest = JSON.parse(await fs.readFile(resolve(root, "assets/narration/manifest.json"), "utf8"));
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
const audioGenerated = audioManifest?.segments?.length === config.scenes.length
  && config.scenes.every((scene, index) => audioManifest.segments[index].id === scene.id
    && audioManifest.segments[index].text === scene.narration);
const purpose = config.scenes.find((scene) => scene.kind === "purpose");
assert(purpose?.points?.length === 3 && purpose.example, "The explanation needs three points and a demo sentence.");
const wordKey = (text) => text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
async function makeWordSync(scene, revealItems) {
  let record;
  if (audioGenerated) {
    const segment = audioManifest.segments.find((candidate) => candidate.id === scene.id);
    record = JSON.parse(await fs.readFile(resolve(root, segment.alignmentFile), "utf8"));
    assert(record.text === scene.narration, `${scene.id}: the alignment is stale.`);
    const hash = createHash("sha256").update(await fs.readFile(resolve(root, record.audioFile))).digest("hex");
    assert(hash === record.audioSha256, `${scene.id}: the audio changed after alignment.`);
  }
  const sync = {
    timingSource: audioGenerated ? "elevenlabs-word-alignment" : "editorial-without-audio",
    sceneId: scene.id, sceneStart: scene.start, fps: config.fps,
    ...(record ? { audioSha256: record.audioSha256, alignmentFile: `assets/narration/segments/${scene.id}.json` } : {}),
    reveals: revealItems.map((item) => {
      let spokenStart = null;
      let spokenEnd = null;
      let wordIndex = null;
      if (record) {
        const phrase = item.phrase.split(/\s+/).map(wordKey);
        const words = record.words;
        const matches = words.flatMap((_, index) =>
          phrase.every((word, offset) => wordKey(words[index + offset]?.word || "") === word) ? [index] : []);
        assert(matches.length === 1, `The narration must say "${item.phrase}" exactly once.`);
        wordIndex = matches[0];
        spokenStart = scene.speech[0] + words[wordIndex].start;
        spokenEnd = scene.speech[0] + words[wordIndex + phrase.length - 1].end;
      }
      const leadSeconds = scene.kind === "hook" ? 0.06 : 0.08;
      const revealSeconds = scene.kind === "hook" ? 0.12 : scene.callouts ? 0.5 : 0.24;
      const revealStart = spokenStart === null ? item.editorialStart : spokenStart - leadSeconds;
      const settledAt = revealStart + revealSeconds;
      assert(revealStart >= 0 && settledAt < scene.duration, `The reveal for "${item.text}" does not fit.`);
      return { selector: item.selector, text: item.text, phrase: item.phrase, wordIndex, spokenStart, spokenEnd,
        revealStart, settledAt, leadSeconds, settleSeconds: revealSeconds - leadSeconds,
        ...(item.rect ? { id: item.id, rect: item.rect, color: item.color,
          endAt: item.untilEnd ? scene.duration : Math.min(scene.duration - 0.6, (spokenEnd ?? settledAt) + item.holdSeconds) } : {}) };
    }),
  };
  assert(sync.reveals.every((event, index, all) =>
    index === 0 || event.revealStart > (scene.kind === "hook" ? all[index - 1].revealStart : all[index - 1].settledAt)),
  "Reveals must follow the spoken order.");
  scene.motion ||= [];
  scene.motion.push(...sync.reveals.map((event) => [event.revealStart, event.settledAt]));
  scene.motion.push(...sync.reveals.filter((event) => event.endAt).map((event) => [event.endAt - 0.25, event.endAt]));
  await fs.writeFile(resolve(assets, `${scene.id}-sync.json`), JSON.stringify(sync, null, 2) + "\n");
  return sync;
}
const purposeSync = await makeWordSync(purpose, [
  ...purpose.points.map((point, index) => ({
    ...point, phrase: point.text, selector: `.purpose-point:nth-child(${index + 1})`,
  })),
  { ...purpose.example, selector: ".purpose-example" },
]);
const focus = config.scenes.find((scene) => scene.kind === "focus");
assert(focus?.steps?.length === 4, "The selected scenario needs four steps.");
const focusSync = await makeWordSync(focus, [
  ...focus.steps.map((step, index) => ({
    text: step.title, phrase: step.title, editorialStart: step.editorialStart,
    selector: `.focus-step:nth-child(${index + 1})`,
  })),
  { text: focus.outcome, phrase: focus.outcomePhrase, selector: ".focus-outcome", editorialStart: 13 },
  { text: focus.registered, phrase: focus.registeredPhrase, selector: ".focus-registered", editorialStart: 14 },
]);
const hook = config.scenes.find((scene) => scene.kind === "hook");
assert(hook && hook.narration.startsWith(hook.wordLines.join(" ")), "The hook's visible words must match its speech.");
const hookSync = await makeWordSync(hook, [
  ...hook.wordLines.join(" ").split(/\s+/).map((text, index) => ({
    text, phrase: text, selector: `.hook-word[data-word-index="${index}"]`, editorialStart: 0.6 + index * 0.35,
  })),
  { text: hook.definition, phrase: hook.definitionPhrase, selector: ".hook-definition", editorialStart: 6 },
]);
const calloutSync = [];
for (const scene of config.scenes.filter((candidate) => candidate.callouts?.length)) {
  for (const callout of scene.callouts) {
    const [left, top, width, height] = callout.rect;
    assert(scene.kind === "footage" && left >= 4 && top >= config.console.top + 4 && width > 0 && height > 0
      && left + width < config.width - 4 && top + height < config.height - 4 && /^#[\da-f]{6}$/i.test(callout.color),
    `${scene.id}: the callout must fit the native console.`);
  }
  calloutSync.push(await makeWordSync(scene, scene.callouts.map((callout, index) => ({
    ...callout, text: callout.id, selector: `#callout-${callout.id}`, editorialStart: 0.6 + index * 2,
  }))));
}
await fs.writeFile(resolve(assets, "callout-sync.json"), JSON.stringify(calloutSync, null, 2) + "\n");
const narration = {
  timingStatus: config.timingStatus, fps: config.fps, durationSeconds: cursor,
  audioGenerated,
  hookSync, purposeSync, focusSync, calloutSync,
  synthesisNotes: [
    "Synthesize one cue at a time; timestamps and visual directions are not spoken.",
    "Speech windows are editorial targets, not provider word alignment.",
    "Measure the actual ElevenLabs character alignment before assembling final audio.",
    "Do not speed speech unnaturally to fill a window; use the reserved reading holds.",
    "Pronounce CLI as C L I, QR as Q R, and R as the letter R. Say /workflows as slash workflows.",
  ],
  cues: config.scenes.map((scene) => {
    const words = scene.narration.split(/\s+/).length;
    const speechStart = scene.start + scene.speech[0];
    const speechEnd = scene.start + scene.speech[1];
    const maximumWpm = words / (speechEnd - speechStart) * 60;
    assert(maximumWpm <= config.maximumNarrationWpm, `${scene.id}: speech window is too short (${maximumWpm.toFixed(1)} WPM).`);
    let shotCursor = scene.start;
    const pictureTiming = (scene.shots || []).map((shot) => {
      const playbackStart = shotCursor;
      const playbackEnd = shotCursor + shot.to - shot.from;
      const holdEnd = playbackEnd + shot.hold;
      shotCursor = holdEnd;
      return {
        playbackStart, playbackEnd, holdEnd, source: scene.source,
        sourceStart: shot.from, sourceEnd: shot.to,
      };
    });
    const generated = audioGenerated ? audioManifest.segments.find((segment) => segment.id === scene.id) : undefined;
    return {
      id: scene.id, sceneStart: scene.start, sceneEnd: scene.end, speechStart, speechEnd,
      inTimecode: timecode(speechStart), outTimecode: timecode(speechEnd),
      text: scene.narration, words, budgetSeconds: speechEnd - speechStart,
      requiredWpm: Math.round(maximumWpm), silentTailSeconds: scene.duration - scene.speech[1],
      visualCue: scene.headline || scene.kind,
      pictureTiming,
      ...(generated ? {
        audioFile: generated.audioFile,
        audioAlignmentFile: generated.alignmentFile,
        measuredSpeechStart: speechStart + generated.previewWords[0].start - generated.previewStart,
        measuredSpeechEnd: speechStart + generated.previewWords.at(-1).end - generated.previewStart,
        audioEnd: speechStart + generated.duration,
      } : {}),
    };
  }),
};
await fs.writeFile(resolve(root, "narration-timing.json"), JSON.stringify(narration, null, 2) + "\n");
const script = [
  "# Dynamic Workflows - timed narration script", "",
  `Picture length: **${cursor} seconds** at **30 fps**.`,
  audioGenerated
    ? "ElevenLabs audio has been generated. Actual speech alignment and listening-preview timing are in assets/narration/manifest.json."
    : "Audio for the current script has not yet been generated.",
  "These are editorial recording windows, not measured word-level alignment.",
  "Record only the quoted speech. Timecodes, directions, and reading holds are not spoken.",
  "Timecodes are HH:MM:SS:FF at 30 fps. The JSON sidecar also contains seconds.", "",
  "## ElevenLabs handoff", "",
  ...narration.synthesisNotes.map((note) => `- ${note}`), "",
  "Keep the voice natural. The end of each speech window leaves a deliberate reading hold.",
  "If measured speech overruns, revise the text or use an available hold; do not silently truncate it.", "",
  ...narration.cues.flatMap((cue) => [
    `## ${cue.id} - ${timecode(cue.sceneStart)} to ${timecode(cue.sceneEnd)}`, "",
    `**Speak:** ${cue.inTimecode} to ${cue.outTimecode} (${cue.budgetSeconds.toFixed(1)} s available; about ${cue.requiredWpm} words/minute if the whole window is used).`, "",
    `> ${cue.text}`, "",
    ...(cue.audioFile ? [
      `**Measured speech:** ${timecode(cue.measuredSpeechStart)} to ${timecode(cue.measuredSpeechEnd)}. Audio clip ends at ${timecode(cue.audioEnd)}; character alignment: \`${cue.audioAlignmentFile}\`.`, "",
    ] : []),
    `**Picture:** ${cue.visualCue}. **Then hold:** ${cue.silentTailSeconds.toFixed(1)} s with no speech.`, "",
    ...cue.pictureTiming.map((shot) => `- Picture movement: ${timecode(shot.playbackStart)}-${timecode(shot.playbackEnd)}; reading freeze: ${timecode(shot.playbackEnd)}-${timecode(shot.holdEnd)}.`),
    ...(cue.pictureTiming.length ? [""] : []),
  ]),
  "## Explanation reveal timing", "",
  ...[hookSync, purposeSync, focusSync, ...calloutSync].flatMap((sync) => sync.reveals.map((event) =>
    `- "${event.text}": reveal ${timecode(sync.sceneStart + event.revealStart)}; `
    + (event.spokenStart === null ? "editorial target; no synthesized word timing."
      : `spoken phrase ${timecode(sync.sceneStart + event.spokenStart)}; settled ${timecode(sync.sceneStart + event.settledAt)}.`))),
  "",
  "## Accuracy boundaries", "",
  "- The authoring recording starts without a workflow extension. Copilot creates and registers the project extension from the visible request.",
  "- The subsequent run uses that unchanged generated extension; its source hashes are recorded in the origin evidence.",
  "- `/workflows` manages runs; the natural-language request starts this workflow.",
  "- The checkpoint is defined in this example, not automatically added to every workflow.",
  "- This example journals its checks; not every unsaved operation is skipped on resume.",
  "- The report's two gaps come from the actual saved assessment.",
  "- Automatic tool approval applies only to the isolated demo fixture.",
  "- The lower-right QR links to the official usage guide and stays visible through the end.", "",
  "- The complete console is shown at native size, below a separate 64px title strip.",
  `- Console text is ${config.console.fontSize}px; the title and brief step labels are 28px and 26px.`, "",
].join("\n");
await fs.writeFile(resolve(root, "narration-script.md"), script);
if (audioGenerated) {
  const captions = [];
  for (const cue of narration.cues) {
    const segment = audioManifest.segments.find((candidate) => candidate.id === cue.id);
    let chunk = [];
    const flush = (nextWord) => {
      if (!chunk.length) return;
      const lines = [""];
      for (const word of chunk) {
        const text = word.text || word.word;
        if (lines.at(-1).length + text.length + 1 > 43) lines.push("");
        lines[lines.length - 1] += (lines.at(-1) ? " " : "") + text;
      }
      assert(lines.length <= 2, `${cue.id}: caption exceeds two lines.`);
      const start = cue.speechStart + chunk[0].start - segment.previewStart;
      const end = Math.min(cue.sceneEnd, cue.speechStart + chunk.at(-1).end - segment.previewStart + 0.15,
        nextWord ? cue.speechStart + nextWord.start - segment.previewStart : Infinity);
      assert(end > start && (!captions.length || start >= captions.at(-1).end - 0.001), "Captions overlap or have invalid timing.");
      captions.push({ start, end, text: lines.join("\n") });
      chunk = [];
    };
    for (const word of segment.previewWords) {
      if (chunk.length && (chunk.map((part) => part.text || part.word).join(" ").length + (word.text || word.word).length + 1 > 78
        || word.end - chunk[0].start > 4)) flush(word);
      chunk.push(word);
    }
    flush();
  }
  const canonical = config.scenes.map((scene) => scene.narration).join(" ").replace(/\s+/g, " ");
  assert(captions.map((caption) => caption.text).join(" ").replace(/\s+/g, " ") === canonical,
    "Authored captions must exactly reproduce the approved narration.");
  const subtitleTime = (seconds) => {
    const milliseconds = Math.round(seconds * 1000);
    return `${String(Math.floor(milliseconds / 3600000)).padStart(2, "0")}:${String(Math.floor(milliseconds / 60000) % 60).padStart(2, "0")}:${String(Math.floor(milliseconds / 1000) % 60).padStart(2, "0")},${String(milliseconds % 1000).padStart(3, "0")}`;
  };
  await fs.writeFile(resolve(root, "narration-captions.srt"), captions.map((caption, index) =>
    `${index + 1}\n${subtitleTime(caption.start)} --> ${subtitleTime(caption.end)}\n${caption.text}\n`).join("\n"));
}

const routes = new Map([
  ["/", ["production/visuals.html", "text/html"]],
  ["/production/styles.css", ["production/styles.css", "text/css"]],
  ["/production/visuals.js", ["production/visuals.js", "text/javascript"]],
  ["/production/timeline.json", ["production/timeline.json", "application/json"]],
  ["/assets/production/report.json", ["assets/production/report.json", "application/json"]],
  ["/assets/production/purpose-sync.json", ["assets/production/purpose-sync.json", "application/json"]],
  ["/assets/production/focus-sync.json", ["assets/production/focus-sync.json", "application/json"]],
  ["/assets/production/hook-sync.json", ["assets/production/hook-sync.json", "application/json"]],
  ["/assets/production/callout-sync.json", ["assets/production/callout-sync.json", "application/json"]],
  ["/assets/production/resource-qr.png", ["assets/production/resource-qr.png", "image/png"]],
  ["/assets/production/GitHub_Invertocat_White.svg", ["assets/production/GitHub_Invertocat_White.svg", "image/svg+xml"]],
  ["/assets/production/fonts/MonaSansVF.woff2", ["assets/production/fonts/MonaSansVF.woff2", "font/woff2"]],
  ["/assets/production/fonts/MonaSansMonoVF.woff2", ["assets/production/fonts/MonaSansMonoVF.woff2", "font/woff2"]],
]);
const server = http.createServer(async (request, response) => {
  const pathname = new URL(request.url, "http://localhost").pathname;
  const entry = routes.get(pathname);
  if (pathname === "/vendor/gsap.js") {
    response.writeHead(200, { "content-type": "text/javascript" });
    response.end(await fs.readFile(requireTool.resolve("gsap/dist/gsap.js")));
  } else if (entry) {
    response.writeHead(200, { "content-type": entry[1] });
    response.end(await fs.readFile(resolve(root, entry[0])));
  } else {
    response.writeHead(404); response.end("Not found");
  }
});
server.listen(0, "127.0.0.1");
await once(server, "listening");
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ headless: true, args: ["--disable-background-networking"] });
const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await context.route("**/*", (route) => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
const page = await context.newPage();
page.on("pageerror", (error) => { throw error; });

async function setScene(scene, at, overlay = false) {
  await page.evaluate(([id, seconds, transparent]) => window.renderScene(id, seconds, transparent), [scene.id, at, overlay]);
}

async function checkLayout(scene) {
  const problems = await page.evaluate(() => [...document.querySelectorAll("h1,h2,p,.intro-product,.intro-subject,.closing-command,.qr-label")].flatMap((element) => {
    let ancestor = element;
    while (ancestor && ancestor !== document.body) {
      if (Number(getComputedStyle(ancestor).opacity) < 0.05) return [];
      ancestor = ancestor.parentElement;
    }
    const rect = element.getBoundingClientRect();
    const fontSize = Number.parseFloat(getComputedStyle(element).fontSize);
    const text = element.textContent.trim();
    const issues = [];
    const hasDirectText = [...element.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
    if (hasDirectText && fontSize < 26) issues.push(`Text smaller than 26px: ${text}`);
    const bottomLimit = element.matches(".qr-label") ? 1048 : 884;
    if (rect.left < -1 || rect.right > 1921 || rect.top < -1 || rect.bottom > bottomLimit) issues.push(`Text outside the content zone: ${text} (${JSON.stringify(rect.toJSON())})`);
    if (element.scrollWidth > element.clientWidth + 2) issues.push(`Horizontal text overflow: ${text}`);
    return issues;
  }));
  assert(!problems.length, `${scene.id}: ${problems.join("\n")}`);
}

async function checkWordSync(scene, sync) {
  for (const event of sync.reveals) {
    await setScene(scene, event.revealStart - 0.05);
    const before = await page.$eval(event.selector, (element) => Number(getComputedStyle(element).opacity));
    assert(before < 0.01, `"${event.text}" appears before its reveal.`);
    if (event.spokenStart !== null) {
      await setScene(scene, event.spokenStart);
      const during = await page.$eval(event.selector, (element) => Number(getComputedStyle(element).opacity));
      assert(during >= 0.65, `"${event.text}" is not legible when its phrase begins.`);
      event.opacityAtWord = during;
    }
    await setScene(scene, event.settledAt + 0.001);
    if (scene.kind === "focus" && event.selector.startsWith(".focus-step")) {
      const footerHidden = await page.$$eval(".focus-outcome,.focus-registered", (elements) =>
        elements.every((element) => Number(getComputedStyle(element).opacity) < 0.01));
      assert(footerHidden, "The focus footer must stay hidden while the four cards are introduced.");
    }
    event.bounds = await page.$eval(event.selector, (element) => {
      const rect = element.getBoundingClientRect();
      return { left: Math.floor(rect.left), top: Math.floor(rect.top), width: Math.ceil(rect.width), height: Math.ceil(rect.height) };
    });
    await page.screenshot({ path: resolve(review, `${scene.id}-beat-${sync.reveals.indexOf(event) + 1}.png`) });
  }
  await fs.writeFile(resolve(assets, `${scene.id}-sync.json`), JSON.stringify(sync, null, 2) + "\n");
}

async function animatedClip(scene, file, transparent = false) {
  const child = spawn("ffmpeg", [
    "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", "30", "-i", "-",
    "-an", ...(transparent ? ["-c:v", "qtrle", "-pix_fmt", "argb"] : ["-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p"]),
    "-r", "30", "-video_track_timescale", "15360", "-movflags", "+faststart", file,
  ], { stdio: ["pipe", "ignore", "pipe"] });
  let errorText = "";
  child.stderr.on("data", (chunk) => { errorText += chunk; });
  const closed = once(child, "close");
  let buffer;
  let wasMoving = false;
  for (let frame = 0; frame < Math.round(scene.duration * 30); frame++) {
    const seconds = frame / 30;
    const moving = scene.motion.some(([from, to]) => seconds >= from && seconds <= to);
    if (!buffer || moving || wasMoving) {
      await setScene(scene, seconds, transparent);
      buffer = await page.screenshot({ type: "png", animations: "allow", omitBackground: transparent });
    }
    wasMoving = moving;
    if (!child.stdin.write(buffer)) await once(child.stdin, "drain");
  }
  child.stdin.end();
  const [code] = await closed;
  assert(code === 0, `${scene.id} encoder failed: ${errorText}`);
}

async function footageClip(scene, overlay, file) {
  const args = ["-hide_banner", "-loglevel", "error", "-y"];
  for (const shot of scene.shots) args.push("-ss", String(shot.from), "-t", String(shot.to - shot.from), "-i", resolve(root, scene.source));
  args.push(...(scene.callouts ? [] : ["-loop", "1"]), "-i", overlay);
  const filters = scene.shots.map((shot, index) => {
    return `[${index}:v]setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=${shot.hold},trim=duration=${shot.to - shot.from + shot.hold},setpts=PTS-STARTPTS[s${index}]`;
  });
  filters.push(scene.shots.map((_, index) => `[s${index}]`).join("") + `concat=n=${scene.shots.length}:v=1:a=0[proof]`);
  filters.push(`[proof]pad=1920:1080:0:${config.console.top}:color=0x0e1116[placed]`);
  filters.push(`[placed][${scene.shots.length}:v]overlay=0:0:shortest=1[out]`);
  args.push("-filter_complex", filters.join(";"), "-map", "[out]", "-t", String(scene.duration),
    "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
    "-r", "30", "-video_track_timescale", "15360", "-movflags", "+faststart", file);
  await run("ffmpeg", args);
}

try {
  const response = await page.goto(origin);
  assert(response?.ok(), "The local composition server did not respond.");
  await page.waitForFunction(() => window.visualsReady);
  const sceneFiles = [];
  const sourceInfo = new Map();
  for (const scene of config.scenes) {
    console.log(`${stillsOnly ? "Inspecting" : "Rendering"} ${scene.id} (${scene.start}-${scene.end}s)`);
    if (scene.kind === "purpose") await checkWordSync(scene, purposeSync);
    if (scene.kind === "focus") await checkWordSync(scene, focusSync);
    if (scene.kind === "hook") await checkWordSync(scene, hookSync);
    if (scene.callouts) {
      const sync = calloutSync.find((candidate) => candidate.sceneId === scene.id);
      for (const event of sync.reveals) {
        await setScene(scene, event.revealStart - 0.05, true);
        assert(await page.$eval(event.selector, (element) => Number(getComputedStyle(element).opacity)) < 0.01,
          `${event.id}: callout appears before its spoken anchor.`);
        await setScene(scene, event.settledAt + 0.01, true);
        assert(await page.$eval(`${event.selector} rect`, (element) => Number(element.getAttribute("stroke-dashoffset"))) < 0.01,
          `${event.id}: callout did not finish drawing.`);
        const overlay = resolve(review, `${scene.id}-${event.id}-overlay.png`);
        await page.screenshot({ path: overlay, omitBackground: true });
        let remaining = event.settledAt + 0.01;
        let sourceAt;
        for (const shot of scene.shots) {
          const play = shot.to - shot.from;
          if (remaining < play + shot.hold) { sourceAt = shot.from + Math.min(remaining, play - 0.04); break; }
          remaining -= play + shot.hold;
        }
        assert(Number.isFinite(sourceAt), `${event.id}: no corresponding source frame.`);
        await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-ss", String(sourceAt),
          "-i", resolve(root, scene.source), "-i", overlay, "-filter_complex",
          `[0:v]pad=1920:1080:0:${config.console.top}:color=0x0e1116[bg];[bg][1:v]overlay=0:0[out]`,
          "-map", "[out]", "-frames:v", "1", resolve(review, `${scene.id}-${event.id}-proof.png`)]);
      }
    }
    await setScene(scene, scene.duration - 0.1, scene.kind === "footage");
    await checkLayout(scene);
    if (scene.kind === "closing") {
      const qr = await page.$eval(".qr-code", (element) => {
        const rect = element.getBoundingClientRect();
        return { x: rect.x, y: rect.y, size: rect.width };
      });
      assert(qr.x === config.qr.x && qr.y === config.qr.y && qr.size === config.qr.size,
        "The visible QR must match its verified lower-right bounds.");
    }
    const still = resolve(review, `${scene.id}.png`);
    await page.screenshot({ path: still, omitBackground: scene.kind === "footage" });
    if (scene.kind === "footage") {
      if (!sourceInfo.has(scene.source)) {
        sourceInfo.set(scene.source, JSON.parse(await run("ffprobe", ["-v", "error", "-select_streams", "v:0",
          "-show_entries", "stream=width,height", "-show_entries", "format=duration", "-of", "json", resolve(root, scene.source)])));
      }
      const source = sourceInfo.get(scene.source);
      assert(source.streams[0].width === config.console.width && source.streams[0].height === config.console.height,
        `${scene.id}: record a native 1920x1016 console; do not crop or stretch old footage.`);
      for (const shot of scene.shots) {
        assert(shot.from >= 0 && shot.to > shot.from && shot.to <= Number(source.format.duration) && shot.hold >= 0 && !shot.crop,
          `${scene.id}: source range is invalid or introduces a crop.`);
      }
      const overlay = resolve(assets, `${scene.id}-overlay.png`);
      await fs.copyFile(still, overlay);
      const shot = scene.shots[0];
      await run("ffmpeg", [
        "-hide_banner", "-loglevel", "error", "-y", "-ss", String(shot.to - 0.1), "-i", resolve(root, scene.source),
        "-i", overlay, "-filter_complex",
        `[0:v]pad=1920:1080:0:${config.console.top}:color=0x0e1116[bg];[bg][1:v]overlay=0:0[out]`,
        "-map", "[out]", "-frames:v", "1", resolve(review, `${scene.id}-proof.png`),
      ]);
    }
    if (stillsOnly) continue;
    const file = resolve(assets, `${scene.id}.mp4`);
    if (scene.kind === "footage") {
      let overlay = resolve(assets, `${scene.id}-overlay.png`);
      if (scene.callouts) {
        overlay = resolve(assets, `${scene.id}-overlay.mov`);
        await animatedClip(scene, overlay, true);
      }
      await footageClip(scene, overlay, file);
    }
    else await animatedClip(scene, file);
    sceneFiles.push(file);
  }
  if (!stillsOnly) {
    const concat = resolve(assets, "concat.txt");
    await fs.writeFile(concat, sceneFiles.map((file) => `file '${file.replaceAll("'", "'\\''")}'`).join("\n"));
    await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat,
      "-map", "0:v:0", "-an", "-c:v", "copy", "-movflags", "+faststart", "-map_metadata", "-1", output]);
    const hash = createHash("sha256").update(await fs.readFile(output)).digest("hex");
    await fs.writeFile(resolve(review, "build.json"), JSON.stringify({
      output, duration: cursor, fps: 30, audioIncluded: false, narrationGenerated: audioGenerated, sha256: hash,
      edits: `Full-width native ${config.console.fontSize}px console, a reserved 64px title strip, cuts, and reading holds; no crop, scaling, or simulated AI output.`,
      scenes: config.scenes.map(({ id, start, end }) => ({ id, start, end })),
    }, null, 2));
    console.log(`Built ${output} (${cursor}s). Picture master is silent; narration is delivered separately.`);
  }
} finally {
  await context.close();
  await browser.close();
  await new Promise((done) => server.close(done));
}
