# Copilot CLI: a useful `/workflows` demo

A narrated 1920x1080, 30 fps video lasting **2:36.0**, showing a real release-readiness
check on an isolated copy of `samples/book-app-project/`.

**Current narrated video:** `renders/workflows-demo-narrated-1080p.mp4`

**Fresh review copy:** `renders/workflows-demo-complete-story-1080p.mp4`

**Silent picture master:** `renders/workflows-demo-console-1080p.mp4`

**Audio handoff:** [timed narration script](narration-script.md) and
[machine-readable timing](narration-timing.json). These are editorial speech
windows; the script also lists measured speech boundaries from the generated audio.
The **audio-only listening preview** is
`assets/narration/narration-preview.mp3`. A lossless listening copy,
`narration-preview.wav`, and a **2:36.0 synchronized track**,
`narration-timed.wav`, are alongside it. The listening preview omits the picture's
reading holds. `assets/narration/manifest.json` and the per-cue JSON files retain
the actual ElevenLabs character/word alignment, voice, model, settings, and hashes.

The edit starts inside an already-open Copilot CLI with experimental features
enabled. It first asks Copilot to create the custom `book-release-check`
workflow from a plain-language request. It shows the actual saved and registered
extension, runs that unchanged workflow, reviews the checks, opens `/workflows`,
resumes a human-review checkpoint, and shows the report produced by the workflow.
Five existing tests and the CLI help check pass. The report identifies test gaps;
passing checks are not a production-readiness guarantee.

## Where does book-release-check come from?

`book-release-check` is a custom name chosen for this example, not a built-in
command. The creation recording starts with no workflow extension. The visible
request asks Copilot to write a reusable project extension, run tests and CLI
help, pause for review, ask an agent for two test gaps, and save a report.
Copilot creates `.github/extensions/book-release-check/extension.mjs`, reloads
extensions, and confirms registration without running it.

The exact generated code is retained in `creation/assets/generated-extension.mjs`.
Its SHA256 before and after the recorded run is identical; the hashes, run ID,
and source paths are in `creation/assets/workflow-origin.json`. The edit then
shows this workflow running, not the previous hand-authored implementation.
Application source files remain unchanged. The earlier prepared extension in
`capture/book-release-check/extension.mjs` is retained for the older run-only recipe.

The edit uses an animated Mona Sans title with GitHub's green/purple palette,
matching the supplied FinOps video's restrained title/underline/mark treatment.
The title reads **What are Dynamic Workflows?** and the narration asks why to
use them, without an
untested-code tagline. A separate hook reveals "The tests passed" and
"That's a good start, but what's still untested?" word by word using the real
voice alignment, then defines the reusable process. A spoken introduction
leads into the three examples rather than jumping directly into a list.
Three illustrative workflows show the
broader use cases: preparing a release, reviewing a pull request, and
investigating a failed build. These are examples users can define, not built-in
workflows or additional recorded demonstrations.

The story then selects the book app's release check and shows its four actual
phases: run tests, stop for your review, assess coverage gaps, and save a report.
It explains that this is our custom workflow, then shows how Copilot creates it
from the requested process and saves the steps as reusable code. Creation and
registration do not start a run. The same
question carries through the native console: what passed, and what still needs
testing? The fresh report answers it with corrupted-data recovery and
case-insensitive author-matching
coverage gaps. No release is performed or approved.

The three opening scenarios are spoken in the same order and wording as their
labels. Each reveal is derived from the actual ElevenLabs word alignment,
starting 80 ms before its phrase and settling 160 ms after it starts. Previous
points dim as the next one is discussed; the demo sentence has its own spoken
anchor. `assets/production/purpose-sync.json` records the measured anchors.
The selected scenario's four cards use the same word-driven timing, with
rounded corners, simple role icons, restrained green-to-purple accents, and a
small upward entrance. Each card appears as its step is introduced, rather
than presenting four static boxes before the narration reaches them.
Both supporting footer lines stay hidden while the four cards are introduced.
The release-decision line enters on "so we can decide"; the loaded-workflow
line follows on "This is our own workflow." Both use a short fade and upward entrance.
`assets/production/focus-sync.json` records the
four card anchors and these two later footer anchors.
`assets/production/hook-sync.json` records the eleven individual word entrances
and definition. The verifier checks encoded frames before, on, and after all
twenty-two explanatory reveals,
not merely whether the audio track and picture have matching lengths.

The narration uses plain, conversational instructions rather than presentation
slogans. Scene lengths follow measured speech, with roughly 1.1-second
transitions, a 0.65-second minimum, and a 1.6-second maximum. Incoming speech
waits at least 0.35 seconds for the new picture. A deliberate pause before
"Prepare a release" separates the examples lead-in from the first scenario;
it requires at least 0.6 seconds of actual quiet audio. The other examples
retain natural sentence breaks; no pause is forced into connected speech.
The audio-only preview adds 0.25-second separators in addition to clip tails.
Planning windows allow up to 180 words per minute; no additional speech or
footage speed-up is used to shorten the edit. Unneeded waiting frames and
reading freezes are cut instead.

Encoded-audio measurements must show no uninterrupted silence over 1.8 seconds
anywhere in the video, not just acceptable gaps between timestamped words.
Proof is saved in `review/narration-pacing.json`. The selected
scenario card is also checked against the encoded video, with the story
boundaries recorded in `review/story-verification.json`.

The console was recorded at **1920x1016 with native 26px text**, reduced from
32px by recording again rather than shrinking or framing the old footage. It fills the
screen below a **64px title strip**, with a consistent 28px product/feature
title at the top-left and a brief 26px step label at the top-right. There are
no enlarged crops, framed proof panels, stretched pixels, or large demo
headings. Native tabs, phases, output, and keyboard hints remain visible.
The actual report is shown in the terminal, not on a redesigned slide.
Cuts and reading freezes are used; playback is not sped up.

Nine thin, unfilled boxes draw around real text as it is discussed: the generated
extension, its review checkpoint, the paused
review checkpoint, five passing tests, CLI help, the assessment phase, and the
report's test-gaps section and two individual items. Source pixels are not
replaced, enlarged, or dimmed. Each console overlay is rendered with transparency
at native size, and the encoded verifier checks that the outlines progress from
absent to partially drawn to complete. Box positions are specific to this
recording, not inferred from arbitrary terminal output.

The closing QR is in the lower-right, links to the official usage guide,
and remains fully visible for **10.7 seconds** through the final frame.
Its actual bounds are x=1660, y=812, 180x180, with a four-module white quiet zone.
The verifier decodes it at one-second intervals and from the final frame.
The final video includes synchronized AAC narration using the existing Ignite
ElevenLabs voice and a selectable English caption track. Captions come from the
approved script and measured word alignment, not speech recognition; they say
**pull request**, not "poll request." `narration-captions.srt` is the matching
sidecar. Captions are not burned over the native console. The intermediate
picture master stays silent. No music or simulated AI responses are included. The
original 97-second edit and previous 146-second framed edit remain available as
`renders/workflows-demo-1080p.mp4` and
`renders/workflows-demo-polished-1080p.mp4`. The first recording's source clips
and report are archived in `assets/first-recording/`. The previous 32px footage,
report, and audio are preserved in `assets/recording-32px/`.

The closing headline and final spoken sentence are **Give dynamic workflows
a try.** Previous guided reviews, including
`renders/workflows-demo-guided-v3-1080p.mp4`, remain available.

## Recreate the video

Requirements: Copilot CLI with dynamic workflow support, VHS, ttyd, ffmpeg,
ffprobe, Node.js, a signed-in GitHub CLI, and Python 3.10+ with pytest.
The example was exercised with Copilot CLI 1.0.98 and VHS 0.12.1.
If the workflow feature is unavailable, update with `copilot update`, enable
experimental features, and check current account/plan eligibility.

From this directory:

```bash
# Choose a Python interpreter with pytest available under a clean HOME.
# python3.14 was available locally; another compatible interpreter is fine.
CAPTURE_PYTHON=python3.14 bash capture/record-creation.sh
# Inspect the generated extension before executing it.
bash capture/record-created-workflow.sh
```

This uses the reusable skill's recorder and the local console-specific tape
settings. Set `CLI_TO_VIDEO_SKILL=/absolute/path/to/cli-to-video` if the skill
is installed elsewhere. The recorder uses the skill's dynamic-workflows example
hooks for the fixture instructions, hash checks, and origin evidence. New recording artifacts are written to `creation/assets/`.
The second script uses the same temporary HOME and never replaces the generated
extension. It also records the focused report view and generates origin evidence
from the source hashes. Inspect the actual report before rebuilding; a new
assessment can change the findings. The supplied `creation/assets/` retains
the complete verified evidence; do not record again merely to rebuild the video.

Record only when new evidence is needed; rebuilding from the retained footage
does not consume Copilot credits. A new run can produce different timings or
findings. Inspect it and adapt `production/timeline.json` and the narration
before rebuilding; the supplied source ranges describe this recording.

The local renderer reuses the already installed reference-video dependencies:

```bash
VIDEO_TOOLS="$HOME/Desktop/test/ignite-2026/.github/skills/content-to-video/template" \
  bash capture/render.sh
```

For a standalone copy, run `npm install` and `npx playwright install chromium`
in this directory, then `bash capture/render.sh`. The renderer uses the local
font files, their OFL license, and official GitHub mark in `assets/production/`.
If restoring source assets, supply `VIDEO_FONTS=/path/to/fonts` and
`VIDEO_MARK=/path/to/GitHub_Invertocat_White.svg`; never redraw the brand mark.
`VIDEO_TOOLS` changes dependency resolution only, not where the output is written.

## Narration

The audio uses the reference FinOps video's existing ElevenLabs voice
`gwU7DXdLrTvWCiUTPZG8`, model `eleven_v4`, stability 0.5, similarity 0.75, and
the same +5% post-generation delivery rate, alignment-aware pause shortening,
and 0.45-second natural tail. Settings are in `production/narration-config.json`.
Ask before changing the voice or model. An explicit narration request authorizes
normal synthesis; do not request approval again.

```bash
elevenlabs auth status
NARRATION_TOOLS="$HOME/Desktop/test/ignite-2026/.github/skills/content-to-video/template" \
  npm run narrate
```

`NARRATION_TOOLS` supplies the existing pipeline's alignment helpers; `VIDEO_TOOLS`
can supply the same directory. OAuth stays in the CLI's credential store.
The generator reuses unchanged, hash-verified clips and retained provider
responses rather than paying for repeated speech. It never reads timecodes or
visual directions aloud. The synchronized track preserves the picture's reading
holds without truncating or further accelerating speech.

After rendering the picture master, make the requested narrated delivery:

```bash
VIDEO_TOOLS="$HOME/Desktop/test/ignite-2026/.github/skills/content-to-video/template" \
  npm run finalize
```

This copies the H.264 picture without another video encode, adds 192 kbps AAC
narration, and verifies `renders/workflows-demo-narrated-1080p.mp4`. Verification
compares decoded audio with the synchronized WAV, rejecting silent, incorrect,
or shifted narration; it also checks the native console and final-frame QR.

## Picture verification

For still previews without encoding, use `node production/build.mjs --stills`
with the same dependency environment. `npm run verify` checks the final MP4,
fully decodes it, checks the timing budgets, and decodes the QR from both the
closing hold and the encoded final frame. It also compares the complete encoded
console region with its native source using SSIM, rejecting cropped, scaled,
or obstructed output. Final delivery remains under three minutes.

The runner creates a new temporary HOME and copies the sample app into it.
It authenticates through an environment variable, warms up first-run notices,
and records creation, execution, and the report in the same environment. Tokens are not written to tapes
or files. Recording consumes real Copilot credits.

`--allow-all-tools` is used only for this disposable fixture to avoid unattended
approval dialogs. Do not copy that approval policy into a production project.
The extension executes its own known Python checks directly.

VHS renders a virtual terminal, so monitor scaling does not change the MP4
dimensions. A dedicated recording-control window was placed on the MacBook's
built-in display; existing windows were not moved.

## Source map

| Path | Purpose |
| --- | --- |
| `capture/setup-env.sh` | Build the isolated book app and CLI configuration |
| `capture/record-console.sh` | Record the native 32px console through the reusable skill |
| `capture/record-creation.sh` | Record real Copilot authoring in a fresh app with no preloaded workflow |
| `capture/record-created-workflow.sh` | Run the generated extension unchanged and record its actual report |
| `capture/tapes/workflow-create.tape` | Plain-language creation request and real registration output |
| `capture/tapes/workflow-created-run.tape` | Start, inspect, and resume the newly created workflow |
| `capture/tapes/workflow-created-report.tape` | Show the actual report header and findings with sed/fold |
| `capture/record.sh` | Original 28px full-frame recording recipe |
| `capture/tapes/console-settings.tape` | 1920x1016 native terminal below the 64px title |
| `capture/tapes/console-report.tape` | Show the real report with 112-column word wrapping at 26px |
| `capture/tapes/preflight.tape` | Exercise the live experimental `/workflows` UI |
| `capture/tapes/workflow-demo.tape` | Launch, run, inspect, and resume |
| `capture/tapes/report.tape` | Display the real report with word wrapping |
| `capture/render.sh` | Build and verify the polished edit |
| `production/timeline.json` | Scene lengths, full-console source ranges, reading holds, and speech windows |
| `production/visuals.*`, `production/styles.css` | Deterministic local animation and layout |
| `production/build.mjs`, `production/verify.mjs` | Local browser/ffmpeg build and final media checks |
| `production/evidence.json` | Official-source claims and sample-specific evidence |
| `production/narrate.mjs`, `production/narration-config.json` | Cached timestamped synthesis using the existing Ignite voice/settings |
| `production/mux.mjs` | Add synchronized AAC narration without re-encoding the picture |
| `assets/production/purpose-sync.json`, `review/purpose-word-sync.json` | Actual word-derived reveal anchors and encoded-frame synchronization proof |
| `assets/narration/` | Listening preview, synchronized track, and measured alignment/provenance |
| `narration-script.md`, `narration-timing.json` | Timestamped voice-production handoff |
| `creation/assets/release-report.md` | Actual report from the newly authored workflow |
| `creation/assets/workflow-origin.json` | Creation/run artifact hashes and source provenance |
| `assets/` | Real source recordings and local production assets |
| `review/` | Full-size scene previews, QR proof, and verification results |
| `renders/` | Final video |

Generated recordings and temporary capture metadata are ignored by Git.

## Related documentation

- [Dynamic workflows](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/dynamic-workflows)
- [Using dynamic workflows](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-dynamic-workflows)
- [VHS](https://github.com/charmbracelet/vhs)

The reusable, self-contained `cli-to-video` skill (formerly `ghcp-cli-to-video`)
is in `ignite-2026/.github/skills/cli-to-video/`. It works for any CLI scenario;
this video is its `examples/dynamic-workflows/` example.
