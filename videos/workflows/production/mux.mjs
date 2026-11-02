import fs from "node:fs/promises";
import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { resolve } from "node:path";
import { root } from "./tools.mjs";

const timeline = JSON.parse(await fs.readFile(resolve(root, "production/timeline.json"), "utf8"));
const manifest = JSON.parse(await fs.readFile(resolve(root, "assets/narration/manifest.json"), "utf8"));
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const duration = timeline.scenes.reduce((sum, scene) => sum + scene.duration, 0);
assert(manifest.fitsPicture && manifest.timedFile && manifest.editorialPictureDuration === duration,
  "Generate a synchronized narration track matching the current picture before finalizing.");
assert(manifest.segments.length === timeline.scenes.length
  && timeline.scenes.every((scene, index) => manifest.segments[index].id === scene.id
    && manifest.segments[index].text === scene.narration),
  "Narration does not match the current script.");
const audio = resolve(root, manifest.timedFile);
assert(sha256(await fs.readFile(audio)) === manifest.timedSha256, "The synchronized narration audio has changed.");
const source = resolve(root, "renders/workflows-demo-console-1080p.mp4");
const output = resolve(root, "renders/workflows-demo-narrated-1080p.mp4");
const captions = resolve(root, "narration-captions.srt");
await fs.access(captions);
const child = spawn("ffmpeg", [
  "-hide_banner", "-loglevel", "error", "-y", "-i", source, "-i", audio, "-i", captions,
  "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
  "-ar", "48000", "-metadata:s:a:0", "language=eng", "-map_metadata", "-1",
  "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-metadata:s:s:0", "title=English",
  "-disposition:s:0", "0",
  "-movflags", "+faststart", output,
], { stdio: ["ignore", "ignore", "pipe"] });
let stderr = "";
child.stderr.on("data", (chunk) => { stderr += chunk; });
const [code] = await once(child, "close");
assert(code === 0, `Narration mux failed (${code}): ${stderr}`);
await fs.writeFile(resolve(root, "review/narrated-build.json"), JSON.stringify({
  output, duration, videoSource: source, audioSource: audio, captionsSource: captions,
  voiceId: manifest.voiceId, modelId: manifest.modelId,
  sha256: sha256(await fs.readFile(output)), videoReencoded: false,
}, null, 2) + "\n");
console.log(`Narrated export: ${output}`);
