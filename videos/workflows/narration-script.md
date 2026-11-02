# Dynamic Workflows - timed narration script

Picture length: **156.03333333333336 seconds** at **30 fps**.
ElevenLabs audio has been generated. Actual speech alignment and listening-preview timing are in assets/narration/manifest.json.
These are editorial recording windows, not measured word-level alignment.
Record only the quoted speech. Timecodes, directions, and reading holds are not spoken.
Timecodes are HH:MM:SS:FF at 30 fps. The JSON sidecar also contains seconds.

## ElevenLabs handoff

- Synthesize one cue at a time; timestamps and visual directions are not spoken.
- Speech windows are editorial targets, not provider word alignment.
- Measure the actual ElevenLabs character alignment before assembling final audio.
- Do not speed speech unnaturally to fill a window; use the reserved reading holds.
- Pronounce CLI as C L I, QR as Q R, and R as the letter R. Say /workflows as slash workflows.

Keep the voice natural. The end of each speech window leaves a deliberate reading hold.
If measured speech overruns, revise the text or use an available hold; do not silently truncate it.

## intro - 00:00:00:00 to 00:00:04:15

**Speak:** 00:00:00:15 to 00:00:04:14 (4.0 s available; about 152 words/minute if the whole window is used).

> What are dynamic workflows, and why would you use them?

**Measured speech:** 00:00:00:15 to 00:00:03:19. Audio clip ends at 00:00:04:08; character alignment: `assets/narration/segments/intro.json`.

**Picture:** What are
Dynamic Workflows?. **Then hold:** 0.0 s with no speech.

## hook - 00:00:04:15 to 00:00:17:00

**Speak:** 00:00:05:02 to 00:00:16:29 (11.9 s available; about 121 words/minute if the whole window is used).

> The tests passed. That's a good start, but what's still untested? Dynamic workflows bring commands, AI agents, and review checkpoints into one reusable process.

**Measured speech:** 00:00:05:01 to 00:00:16:14. Audio clip ends at 00:00:16:29; character alignment: `assets/narration/segments/hook.json`.

**Picture:** hook. **Then hold:** 0.1 s with no speech.

## purpose - 00:00:17:00 to 00:00:37:24

**Speak:** 00:00:17:21 to 00:00:37:23 (20.1 s available; about 168 words/minute if the whole window is used).

> Here are a few examples of where dynamic workflows can help. Prepare a release with tests and a list of what's untested. Review a pull request with the checks and findings in one place. Investigate a failed build by gathering logs and possible next steps. Let's look at a simple example with a Python book app.

**Measured speech:** 00:00:17:21 to 00:00:37:07. Audio clip ends at 00:00:37:22; character alignment: `assets/narration/segments/purpose.json`.

**Picture:** A few places this helps. **Then hold:** 0.1 s with no speech.

## focus - 00:00:37:24 to 00:00:55:03

**Speak:** 00:00:38:10 to 00:00:55:02 (16.7 s available; about 165 words/minute if the whole window is used).

> Here's the plan. Run the tests first. Then, take a look at the results. Find the gaps with an AI agent. We'll save the report so we can decide what needs work. This is our own workflow, not a built-in command. Let's create book release check.

**Measured speech:** 00:00:38:10 to 00:00:54:02. Audio clip ends at 00:00:55:02; character alignment: `assets/narration/segments/focus.json`.

**Picture:** What haven't we tested yet?. **Then hold:** 0.1 s with no speech.

## create - 00:00:55:03 to 00:01:08:06

**Speak:** 00:00:55:17 to 00:01:08:04 (12.6 s available; about 157 words/minute if the whole window is used).

> First, tell Copilot what the workflow should do. We give it a name, describe the checks and review checkpoint, and ask it to save a reusable project extension. Creating it doesn't run it.

**Measured speech:** 00:00:55:17 to 00:01:07:17. Audio clip ends at 00:01:08:01; character alignment: `assets/narration/segments/create.json`.

**Picture:** Describe the workflow in plain language. **Then hold:** 0.0 s with no speech.

- Picture movement: 00:00:55:03-00:01:02:15; reading freeze: 00:01:02:15-00:01:06:06.
- Picture movement: 00:01:06:06-00:01:08:06; reading freeze: 00:01:08:06-00:01:08:06.

## created - 00:01:08:06 to 00:01:20:21

**Speak:** 00:01:08:19 to 00:01:20:19 (12.0 s available; about 145 words/minute if the whole window is used).

> Copilot turns that request into code and registers the workflow. The saved extension holds the steps, including our pause for review. Now book release check is ready to run.

**Measured speech:** 00:01:08:20 to 00:01:20:01. Audio clip ends at 00:01:20:16; character alignment: `assets/narration/segments/created.json`.

**Picture:** Inspect the workflow Copilot created. **Then hold:** 0.1 s with no speech.

- Picture movement: 00:01:08:06-00:01:09:06; reading freeze: 00:01:09:06-00:01:20:21.

## run - 00:01:20:21 to 00:01:29:12

**Speak:** 00:01:21:04 to 00:01:29:11 (8.2 s available; about 161 words/minute if the whole window is used).

> Let's ask Copilot to run book release check. This starts the workflow we just created, beginning with the tests and help check.

**Measured speech:** 00:01:21:04 to 00:01:28:22. Audio clip ends at 00:01:29:06; character alignment: `assets/narration/segments/run.json`.

**Picture:** Start the book app's release check. **Then hold:** 0.0 s with no speech.

- Picture movement: 00:01:20:21-00:01:24:06; reading freeze: 00:01:24:06-00:01:24:27.
- Picture movement: 00:01:24:27-00:01:27:27; reading freeze: 00:01:27:27-00:01:29:12.

## checkpoint - 00:01:29:12 to 00:01:36:12

**Speak:** 00:01:29:26 to 00:01:36:11 (6.5 s available; about 175 words/minute if the whole window is used).

> The checks are done. The workflow's paused here, so we can look at the results before going any further.

**Measured speech:** 00:01:29:26 to 00:01:35:22. Audio clip ends at 00:01:36:06; character alignment: `assets/narration/segments/checkpoint.json`.

**Picture:** Stop at a human-review checkpoint. **Then hold:** 0.0 s with no speech.

- Picture movement: 00:01:29:12-00:01:30:12; reading freeze: 00:01:30:12-00:01:36:12.

## checks - 00:01:36:12 to 00:01:48:10

**Speak:** 00:01:36:26 to 00:01:48:08 (11.4 s available; about 147 words/minute if the whole window is used).

> All five tests passed, and the help command works. But does it handle damaged data? And can we find authors regardless of capitalization? Let's have the agent check.

**Measured speech:** 00:01:36:26 to 00:01:47:20. Audio clip ends at 00:01:48:05; character alignment: `assets/narration/segments/checks.json`.

**Picture:** Review the evidence before continuing. **Then hold:** 0.1 s with no speech.

- Picture movement: 00:01:36:12-00:01:38:12; reading freeze: 00:01:38:12-00:01:48:10.

## monitor - 00:01:48:10 to 00:01:56:08

**Speak:** 00:01:48:24 to 00:01:56:06 (7.4 s available; about 153 words/minute if the whole window is used).

> Type slash workflows, pick our paused release check, and press Enter. Now we can see what's happened so far.

**Measured speech:** 00:01:48:24 to 00:01:55:18. Audio clip ends at 00:01:56:03; character alignment: `assets/narration/segments/monitor.json`.

**Picture:** Open /workflows. **Then hold:** 0.1 s with no speech.

- Picture movement: 00:01:48:10-00:01:50:10; reading freeze: 00:01:50:10-00:01:50:25.
- Picture movement: 00:01:50:25-00:01:54:25; reading freeze: 00:01:54:25-00:01:56:08.

## resume - 00:01:56:08 to 00:02:06:05

**Speak:** 00:01:56:22 to 00:02:06:04 (9.4 s available; about 172 words/minute if the whole window is used).

> Press R to keep going. We don't need to rerun those checks; their results are saved. The agent now looks through the code and tests for gaps.

**Measured speech:** 00:01:56:22 to 00:02:05:16. Audio clip ends at 00:02:06:00; character alignment: `assets/narration/segments/resume.json`.

**Picture:** Resume the saved run. **Then hold:** 0.1 s with no speech.

- Picture movement: 00:01:56:08-00:01:58:08; reading freeze: 00:01:58:08-00:01:59:14.
- Picture movement: 00:01:59:14-00:02:04:14; reading freeze: 00:02:04:14-00:02:06:05.

## completed - 00:02:06:05 to 00:02:11:05

**Speak:** 00:02:06:19 to 00:02:11:04 (4.5 s available; about 147 words/minute if the whole window is used).

> That's finished. Let's open the report and see what needs attention.

**Measured speech:** 00:02:06:19 to 00:02:10:15. Audio clip ends at 00:02:11:00; character alignment: `assets/narration/segments/completed.json`.

**Picture:** Find the completed run. **Then hold:** 0.0 s with no speech.

- Picture movement: 00:02:06:05-00:02:08:05; reading freeze: 00:02:08:05-00:02:11:05.

## report - 00:02:11:05 to 00:02:23:13

**Speak:** 00:02:11:19 to 00:02:23:12 (11.8 s available; about 158 words/minute if the whole window is used).

> The report gives us two things to test next: handling a damaged data file and finding authors regardless of capitalization. So, before we ship, we know where to spend our time.

**Measured speech:** 00:02:11:19 to 00:02:22:23. Audio clip ends at 00:02:23:08; character alignment: `assets/narration/segments/report.json`.

**Picture:** Use the report to choose the next fix. **Then hold:** 0.0 s with no speech.

- Picture movement: 00:02:11:05-00:02:22:14; reading freeze: 00:02:22:14-00:02:23:13.

## closing - 00:02:23:13 to 00:02:36:01

**Speak:** 00:02:23:27 to 00:02:36:00 (12.1 s available; about 169 words/minute if the whole window is used).

> If you keep doing the same checks by hand, this is worth trying. The QR code links to the guide. Use slash workflows to keep track of your runs. Give dynamic workflows a try.

**Measured speech:** 00:02:23:27 to 00:02:35:09. Audio clip ends at 00:02:35:24; character alignment: `assets/narration/segments/closing.json`.

**Picture:** Give dynamic
workflows a try.. **Then hold:** 0.0 s with no speech.

## Explanation reveal timing

- "The": reveal 00:00:05:00; spoken phrase 00:00:05:02; settled 00:00:05:03.
- "tests": reveal 00:00:05:10; spoken phrase 00:00:05:12; settled 00:00:05:14.
- "passed.": reveal 00:00:05:18; spoken phrase 00:00:05:20; settled 00:00:05:22.
- "That's": reveal 00:00:06:18; spoken phrase 00:00:06:20; settled 00:00:06:22.
- "a": reveal 00:00:06:22; spoken phrase 00:00:06:24; settled 00:00:06:26.
- "good": reveal 00:00:06:25; spoken phrase 00:00:06:26; settled 00:00:06:28.
- "start,": reveal 00:00:07:01; spoken phrase 00:00:07:03; settled 00:00:07:05.
- "but": reveal 00:00:07:27; spoken phrase 00:00:07:29; settled 00:00:08:01.
- "what's": reveal 00:00:08:03; spoken phrase 00:00:08:05; settled 00:00:08:07.
- "still": reveal 00:00:08:13; spoken phrase 00:00:08:14; settled 00:00:08:16.
- "untested?": reveal 00:00:08:19; spoken phrase 00:00:08:21; settled 00:00:08:23.
- "Commands, AI agents, and review checkpoints.
One reusable process.": reveal 00:00:10:03; spoken phrase 00:00:10:05; settled 00:00:10:06.
- "Prepare a release": reveal 00:00:21:24; spoken phrase 00:00:21:27; settled 00:00:22:01.
- "Review a pull request": reveal 00:00:25:21; spoken phrase 00:00:25:23; settled 00:00:25:28.
- "Investigate a failed build": reveal 00:00:29:21; spoken phrase 00:00:29:24; settled 00:00:29:29.
- "Demo: a simple Python book app.": reveal 00:00:33:29; spoken phrase 00:00:34:01; settled 00:00:34:06.
- "Run the tests": reveal 00:00:39:12; spoken phrase 00:00:39:15; settled 00:00:39:20.
- "Take a look": reveal 00:00:41:15; spoken phrase 00:00:41:18; settled 00:00:41:23.
- "Find the gaps": reveal 00:00:43:07; spoken phrase 00:00:43:10; settled 00:00:43:14.
- "Save the report": reveal 00:00:46:01; spoken phrase 00:00:46:03; settled 00:00:46:08.
- "We get a report. We still make the release decision.": reveal 00:00:46:24; spoken phrase 00:00:46:26; settled 00:00:47:01.
- "Custom workflow: book-release-check": reveal 00:00:48:28; spoken phrase 00:00:49:00; settled 00:00:49:05.
- "created-extension": reveal 00:01:10:22; spoken phrase 00:01:10:25; settled 00:01:11:07.
- "created-checkpoint": reveal 00:01:15:29; spoken phrase 00:01:16:01; settled 00:01:16:14.
- "paused-review": reveal 00:01:31:15; spoken phrase 00:01:31:17; settled 00:01:32:00.
- "five-tests": reveal 00:01:36:23; spoken phrase 00:01:36:26; settled 00:01:37:08.
- "help-check": reveal 00:01:38:23; spoken phrase 00:01:38:25; settled 00:01:39:08.
- "assessment-agent": reveal 00:02:02:06; spoken phrase 00:02:02:08; settled 00:02:02:21.
- "test-gaps": reveal 00:02:12:16; spoken phrase 00:02:12:18; settled 00:02:13:01.
- "damaged-file": reveal 00:02:14:13; spoken phrase 00:02:14:15; settled 00:02:14:28.
- "author-matching": reveal 00:02:16:17; spoken phrase 00:02:16:19; settled 00:02:17:02.

## Accuracy boundaries

- The authoring recording starts without a workflow extension. Copilot creates and registers the project extension from the visible request.
- The subsequent run uses that unchanged generated extension; its source hashes are recorded in the origin evidence.
- `/workflows` manages runs; the natural-language request starts this workflow.
- The checkpoint is defined in this example, not automatically added to every workflow.
- This example journals its checks; not every unsaved operation is skipped on resume.
- The report's two gaps come from the actual saved assessment.
- Automatic tool approval applies only to the isolated demo fixture.
- The lower-right QR links to the official usage guide and stays visible through the end.

- The complete console is shown at native size, below a separate 64px title strip.
- Console text is 26px; the title and brief step labels are 28px and 26px.
