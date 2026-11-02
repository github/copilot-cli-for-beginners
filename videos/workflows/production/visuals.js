const timeline = await (await fetch("/production/timeline.json")).json();
const purposeSync = await (await fetch("/assets/production/purpose-sync.json")).json();
const focusSync = await (await fetch("/assets/production/focus-sync.json")).json();
const hookSync = await (await fetch("/assets/production/hook-sync.json")).json();
const calloutSync = await (await fetch("/assets/production/callout-sync.json")).json();
gsap.config({ force3D: false });
const stage = document.getElementById("stage");
const escape = (value) => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll('"', "&quot;");
const mark = '<img class="brand-mark" src="/assets/production/GitHub_Invertocat_White.svg" alt="GitHub">';
const background = '<div class="background"></div>';
const stepIcons = [
  '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="m7 12 3 3 7-7"/>',
  '<circle cx="12" cy="8" r="4"/><path d="M4 22v-3a8 8 0 0 1 16 0v3"/>',
  '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
  '<path d="M6 2h9l4 4v16H6zM14 2v5h5M9 12h7M9 16h7"/>',
];
const header = (scene) => `<header class="titlebar"><p class="persistent-title">GitHub Copilot CLI <span>/ Dynamic Workflows</span></p><p class="step-label">${escape(scene.cue || "Official feature guide")}</p></header>`;
let active;
let animation;

window.renderScene = async (id, at, overlay = false) => {
  if (active !== id) {
    animation?.kill();
    const scene = timeline.scenes.find((candidate) => candidate.id === id);
    if (!scene) throw new Error(`Unknown scene ${id}`);
    if (scene.kind === "intro") {
      stage.innerHTML = `${background}<section class="intro-copy"><h1 class="intro-title"><span class="intro-product">GitHub Copilot CLI</span><span class="intro-subject">${escape(scene.headline)}</span></h1><div class="intro-rule"></div><div class="intro-mark">${mark}</div></section>`;
    } else if (scene.kind === "hook") {
      let wordIndex = 0;
      stage.innerHTML = `${background}${header(scene)}<section class="hook-copy">
        ${scene.wordLines.map((line) => `<p class="hook-line">${line.split(/\s+/).map((word) =>
          `<span class="hook-word" data-word-index="${wordIndex++}">${escape(word)}</span>`).join("")}</p>`).join("")}
        <p class="hook-definition">${escape(scene.definition)}</p></section>`;
    } else if (scene.kind === "purpose") {
      stage.innerHTML = `${background}${header(scene)}<section class="purpose-copy">
        <h1 class="purpose-heading">${escape(scene.headline)}</h1>
        <p class="purpose-definition">${escape(scene.definition)}</p>
        <div class="purpose-points">
          ${scene.points.map((point) => `<div class="purpose-point"><p class="scenario-title">${escape(point.text)}</p><p class="scenario-detail">${escape(point.detail)}</p></div>`).join("")}
        </div>
        <p class="purpose-example">${escape(scene.example.text)}</p>
      </section>`;
    } else if (scene.kind === "focus") {
      stage.innerHTML = `${background}${header(scene)}<section class="focus-copy">
        <h1>${escape(scene.headline)}</h1><p class="focus-definition">${escape(scene.definition)}</p>
        <div class="focus-steps">${scene.steps.map((step, index) => `<div class="focus-step">
          <div class="focus-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${stepIcons[index]}</svg><p class="focus-number">0${index + 1}</p></div><h2>${escape(step.title)}</h2><p>${escape(step.detail)}</p>
        </div>`).join("")}</div><p class="focus-registered">${escape(scene.registered)}</p>
        <p class="focus-outcome">${escape(scene.outcome)}</p></section>`;
    } else if (scene.kind === "closing") {
      stage.innerHTML = `${background}${header(scene)}<div class="closing-mark">${mark}</div>
        <h1 class="closing-heading">${escape(scene.headline).replaceAll("\n", "<br>")}</h1>
        <p class="closing-action">${escape(scene.definition)}</p>
        <div class="closing-command">/workflows</div>
        <div class="qr-group"><img class="qr-code" src="/assets/production/resource-qr.png" alt="Official dynamic workflows guide"><div class="qr-label">Scan to learn more</div></div>`;
    } else {
      const sync = calloutSync.find((candidate) => candidate.sceneId === scene.id);
      stage.innerHTML = `${overlay ? "" : background}${header(scene)}${sync ? `<svg class="console-callouts" viewBox="0 0 1920 1080" aria-hidden="true">${sync.reveals.map((event) =>
        `<g id="callout-${event.id}" class="console-callout" style="color:${event.color}"><rect x="${event.rect[0]}" y="${event.rect[1]}" width="${event.rect[2]}" height="${event.rect[3]}" rx="6" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></g>`).join("")}</svg>` : ""}`;
    }
    await document.fonts.ready;
    await Promise.all([...stage.querySelectorAll("img")].map((image) => image.decode()));
    animation = gsap.timeline({ paused: true });
    if (scene.kind === "intro") {
      animation.to(".intro-title", { opacity: 1, duration: 0.75, ease: "power2.out" }, 0.3);
      animation.fromTo(".intro-mark", { opacity: 0, scale: 0.72 }, { opacity: 1, scale: 1, duration: 1.2, ease: "expo.out", immediateRender: false }, 0.45);
      animation.fromTo(".intro-rule", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.8, ease: "power3.out", immediateRender: false }, 0.85);
    } else if (scene.kind === "hook") {
      hookSync.reveals.forEach((event) => {
        animation.fromTo(event.selector, { opacity: 0 }, {
          opacity: 1, duration: event.settledAt - event.revealStart, ease: "power2.out", immediateRender: false,
        }, event.revealStart);
      });
    } else if (scene.kind === "purpose") {
      animation.to(".purpose-heading,.purpose-definition", { opacity: 1, duration: 0.45 }, 0.2);
      purposeSync.reveals.forEach((event, index) => {
        animation.fromTo(event.selector, { opacity: 0, y: 10 }, {
          opacity: 1, y: 0, duration: event.settledAt - event.revealStart,
          ease: "power2.out", immediateRender: false,
        }, event.revealStart);
        if (index > 0) {
          animation.to(purposeSync.reveals[index - 1].selector, {
            opacity: 0.66, duration: 0.24,
          }, event.revealStart);
        }
      });
    } else if (scene.kind === "focus") {
      animation.to(".focus-copy", { opacity: 1, duration: 0.45, ease: "power2.out" }, 0.2);
      focusSync.reveals.forEach((event, index) => {
        const isCard = index < scene.steps.length;
        animation.fromTo(event.selector, { opacity: 0, y: isCard ? 14 : 8, scale: isCard ? 0.985 : 1 }, {
          opacity: 1, y: 0, scale: 1, duration: event.settledAt - event.revealStart,
          ease: "power2.out", immediateRender: false,
        }, event.revealStart);
        if (index > 0 && isCard) animation.to(focusSync.reveals[index - 1].selector, {
          opacity: 0.86, duration: 0.24,
        }, event.revealStart);
      });
    } else if (scene.kind === "closing") {
      animation.to(".closing-heading,.closing-mark", { opacity: 1, duration: 0.65 }, 0.25);
      animation.to(".closing-action,.closing-command", { opacity: 1, duration: 0.6 }, 0.7);
      animation.to(".qr-group", { opacity: 1, duration: 0.7 }, 1.2);
    } else if (scene.callouts) {
      const sync = calloutSync.find((candidate) => candidate.sceneId === scene.id);
      sync.reveals.forEach((event) => {
        animation.to(event.selector, { opacity: 1, duration: 0.1 }, event.revealStart);
        animation.fromTo(`${event.selector} rect`, { attr: { "stroke-dashoffset": 1 } }, {
          attr: { "stroke-dashoffset": 0 }, duration: event.settledAt - event.revealStart,
          ease: "power1.inOut", immediateRender: false,
        }, event.revealStart);
        if (event.endAt < scene.duration) animation.to(event.selector, { opacity: 0, duration: 0.25 }, event.endAt - 0.25);
      });
    }
    active = id;
  }
  animation.seek(at, true);
};
window.visualsReady = true;
