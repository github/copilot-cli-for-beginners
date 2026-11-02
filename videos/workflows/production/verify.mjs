import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { resolve } from "node:path";
import { root, requireTool } from "./tools.mjs";

const sharp = requireTool("sharp");
const jsQR = requireTool("jsqr");
const config = JSON.parse(await fs.readFile(resolve(root, "production/timeline.json"), "utf8"));
const narration = JSON.parse(await fs.readFile(resolve(root, "narration-timing.json"), "utf8"));
const narrated = process.argv.includes("--narrated");
const file = resolve(root, narrated ? "renders/workflows-demo-narrated-1080p.mp4" : "renders/workflows-demo-console-1080p.mp4");
const run = async (command, args) => {
  const child = spawn(command, args, { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const [code] = await once(child, "close");
  if (code !== 0) throw new Error(`${command} failed (${code}): ${stderr}`);
  return { stdout, stderr };
};
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const info = JSON.parse((await run("ffprobe", ["-v", "error", "-show_streams", "-show_format", "-of", "json", file])).stdout);
const [video] = info.streams;
const duration = Number(info.format.duration);
assert(video.codec_type === "video" && info.streams.length === (narrated ? 3 : 1),
  narrated ? "The narrated delivery must contain video, audio, and authored English captions." : "The picture master must contain video only.");
let audioCorrelation;
let pacingProof;
let captionsProof;
if (narrated) {
  const subtitles = info.streams.filter((stream) => stream.codec_type === "subtitle");
  assert(subtitles.length === 1 && subtitles[0].codec_name === "mov_text" && subtitles[0].tags.language === "eng",
    "The delivery needs a selectable English caption track.");
  const encodedCaptions = (await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-i", file,
    "-map", "0:s:0", "-f", "srt", "pipe:1"])).stdout;
  const captionText = encodedCaptions.split(/\r?\n/).filter((line) => line.trim() && !/^\d+$/.test(line.trim())
    && !line.includes("-->")).join(" ").replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim();
  assert(captionText === config.scenes.map((scene) => scene.narration).join(" ").replace(/\s+/g, " "),
    "The encoded captions do not match the approved narration.");
  assert(/\bpull request\b/.test(captionText) && !/\bpoll request\b/.test(captionText),
    "Captions must say pull request, not poll request.");
  captionsProof = { passed: true, source: "approved narration and measured word alignment", language: "eng", pullRequestCorrect: true };
  const audio = info.streams.find((stream) => stream.codec_type === "audio");
  assert(audio?.codec_name === "aac" && audio.sample_rate === "48000" && audio.channels === 1,
    "The narrated delivery needs a real 48 kHz mono AAC narration stream.");
  assert(Math.abs(Number(audio.duration) - duration) < 0.05, "Narration and picture lengths differ.");
  const manifest = JSON.parse(await fs.readFile(resolve(root, "assets/narration/manifest.json"), "utf8"));
  assert(manifest.fitsPicture && Math.abs(manifest.editorialPictureDuration - duration) < 1 / config.fps,
    "The audio manifest does not match the picture.");
  const decodedAudio = resolve(root, "review/narrated-audio-check.wav");
  const pcm = (wav) => {
    assert(wav.toString("ascii", 0, 4) === "RIFF", "Audio comparison requires PCM WAV.");
    for (let at = 12; at + 8 <= wav.length;) {
      const size = wav.readUInt32LE(at + 4);
      if (wav.toString("ascii", at, at + 4) === "data") return wav.subarray(at + 8, at + 8 + size);
      at += 8 + size + size % 2;
    }
    throw new Error("Missing PCM audio data.");
  };
  try {
    await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", file,
      "-map", "0:a:0", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", decodedAudio]);
    const actual = pcm(await fs.readFile(decodedAudio));
    const expected = pcm(await fs.readFile(resolve(root, manifest.timedFile)));
    assert(Math.abs(actual.length - expected.length) <= 4096, "Decoded narration length is incorrect.");
    let dot = 0;
    let a2 = 0;
    let b2 = 0;
    for (let at = 0; at + 1 < Math.min(actual.length, expected.length); at += 2) {
      const a = actual.readInt16LE(at);
      const b = expected.readInt16LE(at);
      dot += a * b;
      a2 += a * a;
      b2 += b * b;
    }
    audioCorrelation = dot / Math.sqrt(a2 * b2);
    assert(audioCorrelation >= 0.98, "The encoded audio is silent, shifted, or does not match the synchronized narration.");
    const quietRms = (from, to) => {
      const start = Math.ceil(from * 48000);
      const end = Math.floor(to * 48000);
      assert(end > start && start >= 0 && end * 2 <= actual.length, "Invalid pause-check interval.");
      let power = 0;
      for (let sample = start; sample < end; sample++) power += (actual.readInt16LE(sample * 2) / 32768) ** 2;
      return Math.sqrt(power / (end - start));
    };
    const longestQuietSeconds = (from, to) => {
      const frame = 480;
      let longest = 0;
      let streak = 0;
      for (let at = Math.ceil(from * 48000); at + frame <= Math.floor(to * 48000); at += frame) {
        let power = 0;
        for (let offset = 0; offset < frame; offset++) power += (actual.readInt16LE((at + offset) * 2) / 32768) ** 2;
        streak = Math.sqrt(power / frame) < 0.01 ? streak + 1 : 0;
        longest = Math.max(longest, streak);
      }
      return longest * frame / 48000;
    };
    const transitions = [];
    const explanation = [];
    const preview = pcm(await fs.readFile(resolve(root, manifest.losslessFile)));
    let previousEnd;
    for (const [index, segment] of manifest.segments.entries()) {
      const record = JSON.parse(await fs.readFile(resolve(root, segment.alignmentFile), "utf8"));
      const scene = config.scenes[index];
      const start = segment.editorialStart + record.words[0].start;
      const end = segment.editorialStart + record.words.at(-1).end;
      if (index > 0) {
        assert(segment.editorialStart - narration.cues[index].sceneStart >= config.audioPacing.minimumSceneLeadSeconds,
          `${segment.id}: speech begins before the incoming picture has settled.`);
        const gap = start - previousEnd;
        assert(gap >= config.audioPacing.minimumTransitionSeconds, `${segment.id}: the section transition is rushed.`);
        assert(gap <= config.audioPacing.maximumTransitionSeconds, `${segment.id}: the section transition drags.`);
        const middle = (start + previousEnd) / 2;
        const halfWindow = Math.min(0.18, gap / 4);
        const rms = quietRms(middle - halfWindow, middle + halfWindow);
        assert(rms < 0.01, `${segment.id}: the encoded transition pause contains unexpected sound.`);
        const quietSeconds = longestQuietSeconds(previousEnd, start);
        assert(quietSeconds >= config.audioPacing.minimumTransitionSeconds,
          `${segment.id}: insufficient measured silence between sections.`);
        const previous = manifest.segments[index - 1];
        const previewGap = segment.previewStart - previous.previewEnd;
        assert(Math.abs(previewGap - config.audioPacing.previewGapSeconds) < 0.0001,
          `${segment.id}: the listening preview lost its section pause.`);
        const quietPreview = preview.subarray(
          Math.ceil((previous.previewEnd + 0.005) * 48000) * 2,
          Math.floor((segment.previewStart - 0.005) * 48000) * 2);
        assert(quietPreview.length > 0 && quietPreview.every((value) => value === 0),
          `${segment.id}: the listening-preview separator is not silent.`);
        transitions.push({ next: segment.id, gapSeconds: gap, quietSeconds, quietRms: rms, previewGapSeconds: previewGap });
      }
      previousEnd = end;
      for (const phrase of scene.pausesBefore || []) {
        const key = (text) => text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
        const target = phrase.split(/\s+/).map(key);
        const matches = record.words.flatMap((_, at) =>
          target.every((word, offset) => key(record.words[at + offset]?.word || "") === word) ? [at] : []);
        assert(matches.length === 1 && matches[0] > 0, `Missing paced phrase "${phrase}".`);
        const at = matches[0];
        const from = segment.editorialStart + record.words[at - 1].end;
        const to = segment.editorialStart + record.words[at].start;
        const gap = to - from;
        assert(gap >= scene.minimumPauseSeconds - 0.0001, `"${phrase}" needs a longer pause.`);
        const quietSeconds = longestQuietSeconds(from, to);
        assert(quietSeconds >= scene.minimumPauseSeconds, `"${phrase}" has insufficient measured silence.`);
        explanation.push({ phrase, gapSeconds: gap, quietSeconds });
      }
    }
    assert(manifest.audioPacing.previewGapSeconds === config.audioPacing.previewGapSeconds,
      "The listening-preview spacing is stale.");
    const longestSilence = longestQuietSeconds(0, Math.min(duration, actual.length / 96000));
    assert(longestSilence <= config.audioPacing.maximumQuietSeconds,
      `The encoded video contains ${longestSilence.toFixed(2)} seconds of uninterrupted silence.`);
    pacingProof = { passed: true, transitions, explanation, longestQuietSeconds: longestSilence,
      previewGapSeconds: manifest.audioPacing.previewGapSeconds };
    await fs.writeFile(resolve(root, "review/narration-pacing.json"), JSON.stringify(pacingProof, null, 2) + "\n");
  } finally {
    await fs.unlink(decodedAudio).catch((error) => { if (error.code !== "ENOENT") throw error; });
  }
}
assert(video.width === 1920 && video.height === 1080 && video.codec_name === "h264" && video.pix_fmt === "yuv420p" && video.avg_frame_rate === "30/1", "Delivery format is incorrect.");
assert(duration <= 180 && Math.abs(duration - narration.durationSeconds) <= 2 / 30, "Picture and narration plan durations do not match.");
assert(typeof narration.audioGenerated === "boolean", "The narration handoff must report whether audio has been generated.");
for (let index = 0; index < narration.cues.length; index++) {
  const cue = narration.cues[index];
  assert(cue.speechStart >= cue.sceneStart && cue.speechEnd <= cue.sceneEnd && cue.speechEnd > cue.speechStart && cue.requiredWpm <= config.maximumNarrationWpm, `${cue.id}: invalid speech budget.`);
  assert(index === 0 || cue.sceneStart === narration.cues[index - 1].sceneEnd, "The timing plan has a gap or overlap.");
}
const decoded = await run("ffmpeg", ["-hide_banner", "-nostats", "-v", "info", "-xerror", "-i", file,
  "-vf", "blackdetect=d=0.1:pix_th=0.01:pic_th=0.995", "-f", "null", "-"]);
assert(!decoded.stderr.includes("black_start:"), "Unexpected black frames were detected.");

async function verifyWordSync(sceneId) {
  const sync = JSON.parse(await fs.readFile(resolve(root, `assets/production/${sceneId}-sync.json`), "utf8"));
  const cue = narration.cues.find((candidate) => candidate.id === sync.sceneId);
  const scene = config.scenes.find((candidate) => candidate.id === sceneId);
  const expectedReveals = sceneId === "hook" ? scene.wordLines.join(" ").split(/\s+/).length + 1
    : sceneId === "focus" ? scene.steps.length + 2 : 4;
  assert(sync.sceneStart === cue.sceneStart && sync.reveals.length === expectedReveals,
    "Explanation reveal timing does not match the picture.");
  if (sceneId === "focus") assert(sync.reveals.slice(scene.steps.length).every((event) =>
    event.revealStart > sync.reveals[scene.steps.length - 1].settledAt),
  "The footer lines must appear after all four workflow cards.");
  if (narrated) assert(sync.timingSource === "elevenlabs-word-alignment",
    "Narrated explanation reveals must use measured word timing, not editorial guesses.");
  const record = sync.alignmentFile
    ? JSON.parse(await fs.readFile(resolve(root, sync.alignmentFile), "utf8")) : null;
  if (record) assert(record.audioSha256 === sync.audioSha256,
    "Explanation reveal timing refers to a different voice clip.");
  const baselineFile = resolve(root, `review/${sceneId}-word-baseline.png`);
  await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-ss",
    String(cue.sceneStart + 1 / 30), "-i", file, "-frames:v", "1", baselineFile]);
  const baseline = await fs.readFile(baselineFile);
  const visualProof = [];
  for (const [index, event] of sync.reveals.entries()) {
    if (record) {
      const words = record.words.slice(event.wordIndex, event.wordIndex + event.phrase.split(/\s+/).length);
      const key = (text) => text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
      assert(words.map((word) => key(word.word)).join(" ") === event.phrase.split(/\s+/).map(key).join(" "),
        `The reveal for "${event.text}" is anchored to the wrong words.`);
      const expectedStart = cue.speechStart - cue.sceneStart + words[0].start;
      assert(Math.abs(expectedStart - event.spokenStart) < 0.000001
        && Math.abs(event.spokenStart - event.revealStart - event.leadSeconds) < 0.000001
        && Math.abs(event.settledAt - event.spokenStart - event.settleSeconds) < 0.000001,
      `The reveal for "${event.text}" is not synchronized to its spoken words.`);
    }
    assert(event.bounds, `Missing encoded-frame check region for "${event.text}".`);
    const reference = await sharp(baseline).extract(event.bounds).removeAlpha().raw().toBuffer();
    const times = {
      before: Math.floor((cue.sceneStart + event.revealStart) * 30 - 1) / 30,
      onWord: Math.ceil((cue.sceneStart + (event.spokenStart ?? event.settledAt)) * 30) / 30,
      settled: Math.ceil((cue.sceneStart + event.settledAt) * 30 + 1) / 30,
    };
    const scores = {};
    for (const [name, at] of Object.entries(times)) {
      const frame = resolve(root, `review/${sceneId}-word-${index + 1}-${name}.png`);
      await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-ss", String(at),
        "-i", file, "-frames:v", "1", frame]);
      const pixels = await sharp(frame).extract(event.bounds).removeAlpha().raw().toBuffer();
      let difference = 0;
      for (let pixel = 0; pixel < pixels.length; pixel++) difference += Math.abs(pixels[pixel] - reference[pixel]);
      scores[name] = difference / pixels.length;
    }
    assert(scores.settled > 1.5 && scores.before < scores.settled * 0.1
      && scores.onWord >= scores.settled * 0.6,
    `Encoded "${event.text}" is visible too early, missing, or not legible on its spoken phrase.`);
    visualProof.push({ text: event.text, spokenAt: event.spokenStart === null ? null : cue.sceneStart + event.spokenStart,
      frameTimes: times, contrast: scores, legibleOnWord: event.spokenStart === null ? null : true });
  }
  await fs.writeFile(resolve(root, `review/${sceneId}-word-sync.json`), JSON.stringify({
    timingSource: sync.timingSource, passed: true, reveals: visualProof,
  }, null, 2) + "\n");
  return { timingSource: sync.timingSource, checkedReveals: visualProof.length, passed: true };
}
const purposeWordSync = await verifyWordSync("purpose");
const focusWordSync = await verifyWordSync("focus");
const hookWordSync = await verifyWordSync("hook");
const calloutProof = [];
for (const scene of config.scenes.filter((candidate) => candidate.callouts)) {
  const sync = JSON.parse(await fs.readFile(resolve(root, `assets/production/${scene.id}-sync.json`), "utf8"));
  assert(sync.sceneStart === narration.cues.find((cue) => cue.id === scene.id).sceneStart
    && sync.reveals.length === scene.callouts.length, `${scene.id}: stale console callouts.`);
  if (narrated) assert(sync.timingSource === "elevenlabs-word-alignment", "Console callouts need real speech alignment.");
  const record = sync.alignmentFile ? JSON.parse(await fs.readFile(resolve(root, sync.alignmentFile), "utf8")) : null;
  if (record) assert(record.audioSha256 === sync.audioSha256, `${scene.id}: callouts refer to a different voice clip.`);
  for (const event of sync.reveals) {
    if (record) {
      const key = (text) => text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
      const words = record.words.slice(event.wordIndex, event.wordIndex + event.phrase.split(/\s+/).length);
      assert(words.map((word) => key(word.word)).join(" ") === event.phrase.split(/\s+/).map(key).join(" ")
        && Math.abs(event.spokenStart - scene.speech[0] - words[0].start) < 0.000001
        && Math.abs(event.spokenStart - event.revealStart - event.leadSeconds) < 0.000001,
      `${event.id}: callout is not anchored to its spoken phrase.`);
    }
    const [left, top, width, height] = event.rect;
    const color = [1, 3, 5].map((at) => Number.parseInt(event.color.slice(at, at + 2), 16));
    const scores = {};
    for (const [name, local] of Object.entries({
      before: event.revealStart - 0.06,
      midway: (event.revealStart + event.settledAt) / 2,
      settled: event.settledAt + 0.08,
    })) {
      const frame = resolve(root, `review/${scene.id}-${event.id}-${name}.png`);
      await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-ss", String(sync.sceneStart + local),
        "-i", file, "-frames:v", "1", frame]);
      const pixels = await sharp(frame).extract({ left: left - 2, top: top - 2, width: width + 4, height: height + 4 })
        .removeAlpha().raw().toBuffer();
      let matches = 0;
      for (let at = 0; at < pixels.length; at += 3) {
        if (color.every((channel, index) => Math.abs(pixels[at + index] - channel) < 40)) matches++;
      }
      scores[name] = matches;
    }
    assert(scores.settled >= 0.7 * (width + height) * 2 && scores.before < scores.settled * 0.15
      && scores.midway > scores.settled * 0.2 && scores.midway < scores.settled * 0.85,
    `${event.id}: the encoded outline is premature, incomplete, or not visibly drawn.`);
    calloutProof.push({ scene: scene.id, id: event.id, phrase: event.phrase, drawnAt: sync.sceneStart + event.settledAt,
      rect: event.rect, colorPixels: scores, passed: true });
  }
}
await fs.writeFile(resolve(root, "review/console-callouts.json"), JSON.stringify(calloutProof, null, 2) + "\n");
const purposeCue = narration.cues.find((cue) => cue.id === "purpose");

const scenarios = config.scenes.find((scene) => scene.kind === "purpose");
const focus = config.scenes.find((scene) => scene.kind === "focus");
const focusCue = narration.cues.find((cue) => cue.id === focus?.id);
const createCue = narration.cues.find((cue) => cue.id === "create");
const createdCue = narration.cues.find((cue) => cue.id === "created");
const runCue = narration.cues.find((cue) => cue.id === "run");
assert(scenarios.points.length >= 2 && scenarios.points.length <= 3
  && scenarios.points.every((point) => point.detail), "Each opening scenario needs a concrete outcome.");
assert(focusCue?.sceneStart === purposeCue.sceneEnd && focus.steps.length === 4
  && focus.registered.includes("book-release-check")
  && focus.steps.at(-1).detail === "release-report.md",
"The selected release story must bridge the scenarios and the real console with its four actual phases.");
assert(createCue?.sceneStart === focusCue.sceneEnd && createdCue?.sceneStart === createCue.sceneEnd
  && runCue?.sceneStart === createdCue.sceneEnd,
  "The story must show real creation and its saved result before running the custom workflow.");
const origin = JSON.parse(await fs.readFile(resolve(root, config.evidence.origin), "utf8"));
assert(origin.extensionSha256 === origin.executedExtensionSha256 && origin.preloaded === false,
  "The authored workflow and the executed workflow must be the same artifact, without preloading.");
const creationProof = [];
for (const cue of [createCue, createdCue]) {
  const scene = config.scenes.find((candidate) => candidate.id === cue.id);
  const shot = scene.shots.at(-1);
  const outputAt = cue.sceneEnd - 0.1;
  const sourceAt = shot.to - 1 / 25;
  const comparison = await run("ffmpeg", ["-hide_banner", "-nostats", "-loglevel", "info",
    "-ss", String(sourceAt), "-i", resolve(root, scene.source), "-ss", String(outputAt), "-i", file,
    "-filter_complex", `[1:v]crop=1920:1016:0:${config.console.top}[console];[0:v][console]ssim[out]`,
    "-map", "[out]", "-frames:v", "1", "-f", "null", "-"]);
  const ssim = Number(comparison.stderr.match(/All:([\d.]+)/)?.[1]);
  assert(ssim >= 0.99, `${cue.id}: the authoring console does not match its authentic source.`);
  creationProof.push({ scene: cue.id, source: scene.source, sourceAt, outputAt, ssim });
}
const focusComparison = await run("ffmpeg", ["-hide_banner", "-nostats", "-loglevel", "info",
  "-ss", String(focusCue.sceneEnd - 0.5), "-i", file, "-i", resolve(root, "review/focus.png"),
  "-filter_complex", "[0:v][1:v]ssim[out]", "-map", "[out]", "-frames:v", "1", "-f", "null", "-"]);
const focusSimilarity = Number(focusComparison.stderr.match(/All:([\d.]+)/)?.[1]);
assert(focusSimilarity >= 0.99, "The encoded release-story card does not match its inspected layout.");
const storyProof = {
  passed: true, scenarios: scenarios.points.map(({ text, detail }) => ({ scenario: text, outcome: detail })),
  demonstratedWorkflow: "book-release-check", question: focus.headline,
  phases: focus.steps, decisionBoundary: focus.outcome, encodedFocusSsim: focusSimilarity,
  origin: { ...origin, encodedCreation: creationProof },
};
await fs.writeFile(resolve(root, "review/story-verification.json"), JSON.stringify(storyProof, null, 2) + "\n");

const checks = config.scenes.find((scene) => scene.id === "checks");
const checkCue = narration.cues.find((cue) => cue.id === "checks");
const shot = checks.shots.at(-1);
assert(shot.hold >= 0.5, "Native-console verification needs a settled reading hold.");
const source = JSON.parse((await run("ffprobe", ["-v", "error", "-select_streams", "v:0",
  "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", resolve(root, checks.source)])).stdout).streams[0];
assert(source.width === config.console.width && source.height === config.console.height, "The source console dimensions changed.");
const [numerator, denominator] = source.r_frame_rate.split("/").map(Number);
const sourceAt = shot.to - denominator / numerator;
const outputAt = checkCue.sceneEnd - 0.5;
const comparison = await run("ffmpeg", ["-hide_banner", "-nostats", "-loglevel", "info",
  "-ss", String(sourceAt), "-i", resolve(root, checks.source), "-ss", String(outputAt), "-i", file,
  "-filter_complex", `[1:v]crop=1920:1016:0:${config.console.top}[console];[0:v][console]ssim[out]`,
  "-map", "[out]", "-frames:v", "1", "-f", "null", "-"]);
const nativeSimilarity = Number(comparison.stderr.match(/All:([\d.]+)/)?.[1]);
assert(nativeSimilarity >= 0.99, "The encoded console no longer matches the complete native source; check for cropping, scaling, or obstructing overlays.");

const closing = narration.cues.at(-1);
const qrProof = [];
const fullyVisibleAt = closing.sceneStart + 1.9;
assert(config.qr.x >= 1500 && config.qr.y + config.qr.size >= 980
  && config.qr.x + config.qr.size <= 1888 && config.qr.y + config.qr.size <= 1048,
  "The QR must sit safely in the lower-right corner.");
for (const at of [...Array.from({ length: Math.floor(duration - fullyVisibleAt) }, (_, index) => fullyVisibleAt + index), duration - 1 / 30]) {
  const frame = resolve(root, `review/qr-${at.toFixed(2)}.png`);
  await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-ss", String(at), "-i", file, "-frames:v", "1", frame]);
  const { data, info: pixels } = await sharp(frame).extract({
    left: config.qr.x, top: config.qr.y, width: config.qr.size, height: config.qr.size,
  }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const qr = jsQR(new Uint8ClampedArray(data), pixels.width, pixels.height);
  assert(qr?.data === config.resourceUrl, `The QR does not decode to the official URL at ${at}s.`);
  qrProof.push({ at, url: qr.data });
}
assert(duration - fullyVisibleAt >= config.qr.minimumHoldSeconds, "The QR hold is too short to scan.");
const verification = {
  passed: true, duration, width: video.width, height: video.height, fps: video.avg_frame_rate,
  audioIncluded: narrated, narrationGenerated: narration.audioGenerated, fullDecode: true, blackFrames: false, qrProof,
  ...(narrated ? { audioCorrelation, audioPacing: pacingProof, captions: captionsProof } : {}),
  hookWordSync, purposeWordSync, focusWordSync, callouts: calloutProof,
  qrFullyVisibleSeconds: duration - fullyVisibleAt,
  story: storyProof,
  narrationCues: narration.cues.length,
  nativeConsole: { width: source.width, height: source.height, sourceAt, outputAt, ssim: nativeSimilarity },
};
await fs.writeFile(resolve(root, narrated ? "review/narrated-verification.json" : "review/verification.json"), JSON.stringify(verification, null, 2) + "\n");
console.log(`Verified: ${duration.toFixed(2)}s, 1080p30, ${narrated ? "synchronized AAC narration" : "picture only"}, ${narration.cues.length} timed narration cues, final-frame QR decoded.`);
