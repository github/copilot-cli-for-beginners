import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { root } from "./tools.mjs";

const tools = process.env.NARRATION_TOOLS || process.env.VIDEO_TOOLS;
if (!tools) throw new Error("Set NARRATION_TOOLS or VIDEO_TOOLS to the existing content-to-video template directory.");
const {
  validateAlignment, wordsFromAlignment, rateFactor, spokenNarration, displayAlignment,
  pauseCuts, removePauses, shiftAlignment, tailNoise, silence,
} = await import(pathToFileURL(resolve(tools, "scripts/alignment.mjs")).href);
const timeline = JSON.parse(await fs.readFile(resolve(root, "production/timeline.json"), "utf8"));
const settings = JSON.parse(await fs.readFile(resolve(root, "production/narration-config.json"), "utf8"));
const audioRoot = resolve(root, "assets/narration");
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const hash = (value) => createHash("sha256").update(value).digest("hex");
const tempo = rateFactor(settings.prosodyRate);
assert(typeof settings.modelId === "string" && settings.modelId.length > 0
  && typeof settings.voiceId === "string" && settings.voiceId.length > 0,
  "Configure the explicitly approved voice and model before synthesis.");

async function run(command, args, input) {
  const child = spawn(command, args, { stdio: ["pipe", "pipe", "pipe"], timeout: 240000 });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const closed = once(child, "close");
  child.stdin.end(input);
  const [code] = await closed;
  assert(code === 0, command === "elevenlabs"
    ? `ElevenLabs ${args[0]} failed (${code}); provider output was not printed. Authentication or service access may need attention.`
    : `${command} failed (${code}): ${stderr}`);
  return stdout;
}

function addSectionPauses(pcm, alignment, normalizedAlignment, plan) {
  const words = wordsFromAlignment(alignment);
  const key = (text) => text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
  const insertions = plan.before.map((phrase) => {
    const target = phrase.split(/\s+/).map(key);
    const matches = words.flatMap((_, index) =>
      target.every((word, offset) => key(words[index + offset]?.word || "") === word) ? [index] : []);
    assert(matches.length === 1 && matches[0] > 0, `Cannot place a section pause before "${phrase}".`);
    const index = matches[0];
    const from = words[index - 1].end;
    const to = words[index].start;
    // Provider word gaps can contain speech; insert the full pause plus tempo-processing margin.
    const extraSamples = Math.ceil((plan.minimumSeconds + plan.tempoPaddingSeconds) * tempo * 24000);
    if (!extraSamples) return { phrase, samples: 0 };
    const frame = 120;
    let quietAt = -1;
    let quietRms = Infinity;
    for (let sample = Math.ceil(from * 24000); sample + frame <= Math.floor(to * 24000); sample += frame / 4) {
      let power = 0;
      for (let offset = 0; offset < frame; offset++) power += (pcm.readInt16LE((sample + offset) * 2) / 32768) ** 2;
      const rms = Math.sqrt(power / frame);
      if (rms < quietRms) { quietRms = rms; quietAt = sample + frame / 2; }
    }
    assert(quietAt >= 0 && quietRms < 0.01, `No safe silent interval before "${phrase}"; speech was not cut.`);
    let boundaryLevel = Infinity;
    const center = quietAt;
    for (let sample = center - frame / 4; sample <= center + frame / 4; sample++) {
      const level = Math.abs(pcm.readInt16LE((sample - 1) * 2)) + Math.abs(pcm.readInt16LE(sample * 2));
      if (level < boundaryLevel) { boundaryLevel = level; quietAt = sample; }
    }
    return { phrase, sample: quietAt, samples: extraSamples, at: quietAt / 24000, seconds: extraSamples / 24000 };
  }).filter((insertion) => insertion.samples > 0).sort((a, b) => a.sample - b.sample);
  const parts = [];
  let previous = 0;
  for (const insertion of insertions) {
    parts.push(pcm.subarray(previous * 2, insertion.sample * 2), Buffer.alloc(insertion.samples * 2));
    previous = insertion.sample;
  }
  parts.push(pcm.subarray(previous * 2));
  const shift = (value) => value + insertions.reduce((sum, insertion) => sum + (value >= insertion.at ? insertion.seconds : 0), 0);
  const shifted = (value) => value ? {
    ...value,
    character_start_times_seconds: value.character_start_times_seconds.map(shift),
    character_end_times_seconds: value.character_end_times_seconds.map(shift),
  } : null;
  return { pcm: Buffer.concat(parts), alignment: shifted(alignment),
    normalizedAlignment: shifted(normalizedAlignment), insertions };
}

const auth = JSON.parse(await run("elevenlabs", ["auth", "status"]));
assert(auth.schemes?.some((scheme) => scheme.logged_in && scheme.scheme === "OAuth"),
  "ElevenLabs OAuth is not active. Run elevenlabs auth login.");
await fs.mkdir(resolve(audioRoot, "segments"), { recursive: true });
await fs.mkdir(resolve(audioRoot, "provider"), { recursive: true });
let previousManifest;
try {
  previousManifest = JSON.parse(await fs.readFile(resolve(audioRoot, "manifest.json"), "utf8"));
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
const segments = [];
let pictureCursor = 0;
let previewCursor = 0;
for (let index = 0; index < timeline.scenes.length; index++) {
  const scene = timeline.scenes[index];
  const sceneStart = pictureCursor;
  pictureCursor += scene.duration;
  if (index > 0) previewCursor += timeline.audioPacing.previewGapSeconds;
  const pronunciations = [
    { text: "CLI", say: "C L I" }, { text: "QR", say: "Q R" },
  ].filter((entry) => new RegExp(`\\b${entry.text}\\b`).test(scene.narration));
  const spoken = spokenNarration(scene.narration, pronunciations);
  const input = {
    text: scene.narration, spokenText: spoken.text, ...settings,
    pronunciations: spoken.replacements,
    previousText: timeline.scenes[index - 1]?.narration || "",
    nextText: timeline.scenes[index + 1]?.narration || "",
    outputFormat: "pcm_24000",
    ...(scene.pausesBefore ? { sectionPauses: {
      before: scene.pausesBefore, minimumSeconds: scene.minimumPauseSeconds, tempoPaddingSeconds: 0.08,
    } } : {}),
  };
  const inputHash = hash(JSON.stringify(input));
  const requestHash = hash(JSON.stringify({
    text: input.spokenText, voiceId: input.voiceId, modelId: input.modelId,
    voiceSettings: input.voiceSettings, previousText: input.previousText, nextText: input.nextText,
    outputFormat: input.outputFormat,
  }));
  const clipHash = hash(JSON.stringify({ ...input, previousText: "", nextText: "" }));
  const file = resolve(audioRoot, "segments", `${scene.id}.wav`);
  const recordFile = resolve(audioRoot, "segments", `${scene.id}.json`);
  let record;
  try {
    record = JSON.parse(await fs.readFile(recordFile, "utf8"));
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  let cached = false;
  // Preserve verified speech when only a neighboring cue changes, retaining its original request hash.
  const oldIndex = previousManifest?.segments?.findIndex((segment) => segment.id === scene.id) ?? -1;
  const oldContextHash = oldIndex >= 0 && previousManifest.segments[oldIndex].text === scene.narration
    ? hash(JSON.stringify({
      ...input,
      previousText: previousManifest.segments[oldIndex - 1]?.text || "",
      nextText: previousManifest.segments[oldIndex + 1]?.text || "",
    })) : null;
  if (record && (record.inputHash === inputHash || record.clipHash === clipHash || record.inputHash === oldContextHash)) {
    try {
      cached = record.audioSha256 === hash(await fs.readFile(file));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    if (cached && record.clipHash !== clipHash) {
      record.clipHash = clipHash;
      await fs.writeFile(recordFile, JSON.stringify(record, null, 2));
    }
  }
  if (!cached) {
    const providerFile = resolve(audioRoot, "provider", `${scene.id}.json`);
    let provider;
    try {
      provider = JSON.parse(await fs.readFile(providerFile, "utf8"));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    if (provider?.requestHash !== requestHash && provider?.inputHash !== inputHash) {
      console.log(`Synthesizing ${scene.id} with the existing Ignite voice...`);
      const request = {
        text: spoken.text, model_id: settings.modelId, voice_settings: settings.voiceSettings,
        ...(input.previousText ? { previous_text: input.previousText } : {}),
        ...(input.nextText ? { next_text: input.nextText } : {}),
      };
      const response = JSON.parse(await run("elevenlabs", [
        "text-to-speech", "convert_with_timestamps", "--voice-id", settings.voiceId,
        "--output-format", "pcm_24000", "--json", "-", "--format", "json",
        "--via", "ghcp-cli-to-video", "--no-retry", "--no-pager",
      ], JSON.stringify(request)));
      assert(typeof response.audio_base64 === "string" && response.audio_base64.length,
        `${scene.id}: no audio was returned.`);
      validateAlignment(response.alignment, spoken.text);
      provider = {
        inputHash, requestHash, audio_base64: response.audio_base64, alignment: response.alignment,
        normalized_alignment: response.normalized_alignment || null,
      };
      await fs.writeFile(providerFile, JSON.stringify(provider));
    }
    let pcm = Buffer.from(provider.audio_base64, "base64");
    assert(pcm.length > 0 && pcm.length % 2 === 0, `${scene.id}: invalid PCM audio.`);
    validateAlignment(provider.alignment, spoken.text);
    const cuts = pauseCuts(pcm, 24000, provider.alignment, settings.maxPauseSeconds);
    pcm = removePauses(pcm, 24000, cuts);
    let providerAlignment = shiftAlignment(provider.alignment, cuts);
    let providerNormalizedAlignment = shiftAlignment(provider.normalized_alignment, cuts);
    let sectionPauses = [];
    if (input.sectionPauses) {
      const paused = addSectionPauses(pcm, providerAlignment, providerNormalizedAlignment, input.sectionPauses);
      pcm = paused.pcm;
      providerAlignment = paused.alignment;
      providerNormalizedAlignment = paused.normalizedAlignment;
      sectionPauses = paused.insertions;
    }
    const alignment = validateAlignment(displayAlignment(providerAlignment, spoken.replacements), scene.narration);
    const words = wordsFromAlignment(alignment, tempo);
    const finalCharacter = Math.max(
      providerAlignment.character_end_times_seconds.at(-1),
      providerNormalizedAlignment?.character_end_times_seconds.at(-1) || 0,
    );
    assert(finalCharacter <= pcm.length / 48000 + 0.12, `${scene.id}: alignment exceeds the returned audio.`);
    const needed = Math.ceil((finalCharacter + settings.tailSeconds) * 24000) * 2;
    if (pcm.length < needed) pcm = Buffer.concat([pcm, Buffer.alloc(needed - pcm.length)]);
    const keep = Math.min(pcm.length / 48000 / tempo, finalCharacter / tempo + settings.tailSeconds);
    assert(keep >= words.at(-1).end, `${scene.id}: trimming would cut speech.`);
    const temporary = resolve(audioRoot, "segments", `${scene.id}.pcm`);
    await fs.writeFile(temporary, pcm);
    try {
      await run("ffmpeg", [
        "-hide_banner", "-loglevel", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", temporary, "-af",
        `atempo=${tempo},atrim=end=${keep.toFixed(6)},afade=t=out:st=${Math.max(finalCharacter / tempo, keep - 0.08).toFixed(6)}:d=0.08`,
        "-ar", "48000", "-c:a", "pcm_s16le", "-map_metadata", "-1", file,
      ]);
    } finally {
      await fs.unlink(temporary);
    }
    const wav = await fs.readFile(file);
    const data = wav.indexOf("data", 12) + 8;
    assert(data >= 20, `${scene.id}: missing WAV data chunk.`);
    const noise = tailNoise(wav.subarray(data), 48000, words.at(-1).start);
    if (noise) await fs.writeFile(file, Buffer.concat([wav.subarray(0, data), silence(wav.subarray(data), 48000, noise)]));
    const info = JSON.parse(await run("ffprobe", ["-v", "error", "-show_format", "-show_streams", "-of", "json", file]));
    const duration = Number(info.format.duration);
    assert(duration >= words.at(-1).end && duration > 0, `${scene.id}: speech was cut off.`);
    record = {
      id: scene.id, text: scene.narration, spokenText: spoken.text, inputHash, clipHash,
      voiceId: settings.voiceId, modelId: settings.modelId, voiceSettings: settings.voiceSettings,
      prosodyRate: settings.prosodyRate, tempo, duration, rawDuration: Buffer.from(provider.audio_base64, "base64").length / 48000,
      audioFile: `assets/narration/segments/${scene.id}.wav`, audioSha256: hash(await fs.readFile(file)),
      alignment, providerAlignment, providerNormalizedAlignment, words, pauseCuts: cuts, sectionPauses,
      ...(noise ? { tailNoise: noise } : {}),
    };
    await fs.writeFile(recordFile, JSON.stringify(record, null, 2));
  }
  validateAlignment(record.alignment, scene.narration);
  assert(record.words.at(-1).end <= record.duration, `${scene.id}: invalid cached speech timing.`);
  const editorialStart = sceneStart + scene.speech[0];
  assert(index === 0 || scene.speech[0] >= timeline.audioPacing.minimumSceneLeadSeconds,
    `${scene.id}: narration starts before the incoming picture has settled.`);
  const previousSegment = segments.at(-1);
  const measuredStart = editorialStart + record.words[0].start;
  const measuredEnd = editorialStart + record.words.at(-1).end;
  const transitionPause = previousSegment ? measuredStart - previousSegment.measuredSpeechEnd : null;
  assert(transitionPause === null || transitionPause >= timeline.audioPacing.minimumTransitionSeconds,
    `${scene.id}: insufficient breathing room after the preceding section.`);
  const fitsPicture = editorialStart + record.duration <= pictureCursor;
  segments.push({
    id: scene.id, text: scene.narration, audioFile: record.audioFile, duration: record.duration,
    previewStart: previewCursor, previewEnd: previewCursor + record.duration,
    editorialStart, editorialSceneEnd: pictureCursor, fitsPicture,
    measuredSpeechStart: measuredStart, measuredSpeechEnd: measuredEnd, transitionPause,
    alignmentFile: `assets/narration/segments/${scene.id}.json`,
    previewWords: record.words.map((word) => ({ ...word, start: word.start + previewCursor, end: word.end + previewCursor })),
  });
  previewCursor += record.duration;
  console.log(`${scene.id}: ${record.duration.toFixed(2)}s${cached ? " (cached)" : ""}${fitsPicture ? "" : " (picture timing needs review)"}`);
}

const concat = resolve(audioRoot, "concat.txt");
await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
  "-i", "anullsrc=r=48000:cl=mono", "-t", String(timeline.audioPacing.previewGapSeconds),
  "-c:a", "pcm_s16le", resolve(audioRoot, "section-gap.wav")]);
await fs.writeFile(concat, segments.flatMap((segment, index) => [
  ...(index > 0 ? ["file 'section-gap.wav'"] : []),
  `file 'segments/${segment.id}.wav'`,
]).join("\n"));
const wavFile = resolve(audioRoot, "narration-preview.wav");
const mp3File = resolve(audioRoot, "narration-preview.mp3");
await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
  "-i", concat, "-c:a", "pcm_s16le", "-map_metadata", "-1", wavFile]);
await run("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", wavFile,
  "-c:a", "libmp3lame", "-b:a", "192k", "-map_metadata", "-1", mp3File]);
const info = JSON.parse(await run("ffprobe", ["-v", "error", "-show_format", "-of", "json", wavFile]));
const duration = Number(info.format.duration);
assert(Math.abs(duration - previewCursor) < 0.02, "The listening preview lost or duplicated speech.");
await run("ffmpeg", ["-hide_banner", "-v", "error", "-xerror", "-i", mp3File, "-f", "null", "-"]);
const fitsPicture = segments.every((segment) => segment.fitsPicture);
let timedFile;
if (fitsPicture) {
  timedFile = "assets/narration/narration-timed.wav";
  const inputs = segments.flatMap((segment) => ["-i", resolve(root, segment.audioFile)]);
  const delays = segments.map((segment, index) =>
    `[${index + 1}:a]adelay=${Math.round(segment.editorialStart * 1000)}:all=1[s${index}]`);
  const filters = [...delays,
    `[0:a]${segments.map((_, index) => `[s${index}]`).join("")}amix=inputs=${segments.length + 1}:normalize=0:duration=first[out]`,
  ].join(";");
  await run("ffmpeg", [
    "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-t", String(pictureCursor),
    "-i", "anullsrc=r=48000:cl=mono", ...inputs, "-filter_complex", filters, "-map", "[out]",
    "-t", String(pictureCursor), "-c:a", "pcm_s16le", "-map_metadata", "-1", resolve(root, timedFile),
  ]);
  const timed = JSON.parse(await run("ffprobe", [
    "-v", "error", "-show_format", "-of", "json", resolve(root, timedFile),
  ]));
  assert(Math.abs(Number(timed.format.duration) - pictureCursor) < 0.001,
    "The synchronized narration track does not match the picture duration.");
} else {
  console.warn("The listening preview is ready, but the picture needs retiming before synchronized audio can be assembled.");
}
const manifest = {
  provider: "elevenlabs-cli", ...settings,
  kind: "Listening preview with deliberate section pauses; longer picture reading holds are omitted.",
  audioPacing: timeline.audioPacing,
  previewFile: "assets/narration/narration-preview.mp3",
  losslessFile: "assets/narration/narration-preview.wav",
  previewDuration: duration, editorialPictureDuration: pictureCursor,
  previewSha256: hash(await fs.readFile(mp3File)), fitsPicture,
  ...(timedFile ? { timedFile, timedSha256: hash(await fs.readFile(resolve(root, timedFile))) } : {}),
  segments,
};
await fs.writeFile(resolve(audioRoot, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
console.log(`Audio preview ready: ${duration.toFixed(2)}s, ${segments.length} segments, same Ignite voice and Eleven v4.`);
