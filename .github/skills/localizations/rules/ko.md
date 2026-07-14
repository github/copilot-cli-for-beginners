# ko-kr

These rules apply to **both roles**: the `translator` agent uses them as generation directives (how to write the Korean text), and the `evaluator` agent uses them as review criteria (what to check and flag). Wherever a rule says "flag" or "look for", the translator should read it as "produce text that satisfies this".

In general, producing and evaluating translation quality requires both the accuracy of the meaning and the natural flow of the language. To do this, verify that the text passes core tests for accuracy, fluency, consistency, and cultural appropriateness.

Here are the 4 core pillars:

- **Accuracy:** Ensure the meaning matches the source text exactly, with no information added, distorted, or omitted.
- **Fluency:** Check that grammar, punctuation, and spelling adhere to the conventions of the target language so that the text reads naturally.
- **Terminology & Consistency:** Verify that specialized terms, names, and key phrases are used uniformly throughout the document.
- **Cultural Appropriateness:** Confirm that idioms, metaphors, and the overall tone are culturally sensitive and suited to the target audience.

## English to Korean Localization Scenario

English-to-Korean translation quality is best evaluated by checking for natural sentence structures, correct honorific levels, and accurate transformation of English idioms into natural Korean expressions. Korean has a drastically different grammar structure (Subject-Object-Verb) and deep cultural nuances that automated tools often miss.

### Key Evaluation Pillars for Korean

- **Honorifics and Tone:** Verify that the speech level—formal-polite (존댓말/jondaenmal) versus casual (반말/banmal)—is uniform and fits the target audience. For documentation, this means consistent 존댓말 throughout.
- **Natural Word Order:** Ensure the text does not read like a literal word-for-word translation (번역투/beonyeoktu), which results in long, awkward modifiers.
- **Subject Pronoun Omission:** Check that unnecessary pronouns like "그녀" (she) or "그들" (they) are removed, as natural Korean drops subjects when context is clear.
- **Terminology Adaptation:** Confirm whether technical words are accurately translated into localized Korean terms or appropriately transliterated into Hangul phonetic equivalents.

### Common Translation Mistakes to Flag

- **Passive Voice Overuse:** English frequently uses passive voice, but natural Korean heavily favors active verbs; overusing passive forms makes Korean text feel robotic.
- **Literal Phrase Translations:** Watch out for expressions like "in terms of" translated literally to "~의 관점에서" instead of natural Korean particles.
- **Plural Marker Overuse:** English strictly tracks plurals, but adding the Korean plural marker "~들" to every noun sounds highly unnatural.

### Practical Evaluation Framework

| Evaluation Metric | What to Look For (English to Korean Context) |
| :--- | :--- |
| **Accuracy (정확성)** | Are critical numbers, names, and core English meanings preserved without distortion? |
| **Fluency (유창성)** | Does a native Korean speaker understand the text instantly without re-reading sentences? |
| **Style Guide (스타일)** | Does the text follow Korean spelling, spacing (띄어쓰기), and punctuation rules? |

## Localization for Technical Documents for Developers

When evaluating English-to-Korean technical documentation for developers, standard linguistic rules change. Korean developers heavily favor industry-standard English terminology over clunky, forced Korean translations. If a translation forces purely native Korean words for established coding concepts, it will look amateurish and confuse the reader.

Evaluate your developer documentation by looking for specific markers across structural, lexical, and formatting levels.

### The Developer-Specific Evaluation Rubric

#### Terminology & Loanwords (가장 중요함)

- **Avoid "Over-Translation":** Some terms have well-established Korean equivalents and should use them (e.g., *String* → **문자열**, *Array* → **배열**, *Dependency* → **종속성/의존성**). Others have no natural Korean equivalent and must be transliterated into Hangul or kept in English—forcing a literal native translation is unacceptable (e.g., *Instance* → "실체" or *Thread* → "실" is wrong; use **인스턴스**, **스레드**). When unsure, prefer the form Korean developers actually use over a literal dictionary translation, and keep the chosen term consistent throughout (see Terminology & Consistency).
- **The First-Mention Rule:** For critical or unfamiliar technical jargon, the **first occurrence within a single file** should use the Hangul transliteration followed by the original English in parentheses—for example, **인스턴스(Instance)**. This follows the standardized [Microsoft Korean Localization Style Guide](https://learn.microsoft.com/globalization/reference/microsoft-style-guides) for technical acronyms and core definitions. Subsequent mentions in the same file can just use the Hangul. Apply this selectively to terms a reader may want to look up in English, not to every loanword.
- **Code Elements Untouched:** Ensure variables, function names, APIs, CLI commands (`npm install`), and code itself are kept exactly as in the source. However, **human-language comments inside code blocks** (e.g., `// fetch the user`) *should* be localized, since they are explanatory prose for the reader.

#### Tone and Politeness Level (합니다체)

- **The "합니다체" (Hamnida-che) Standard:** Developer docs should use the standard formal-polite register, **합니다체** (the 하십시오체 family, with endings like *~합니다 / ~습니다*). This is the conventional register for Korean technical documentation and is what the Microsoft Korean Localization Style Guide prescribes. Do **not** drop into the more casual **해요체** (endings like *~해요 / ~예요*), which reads too informal for documentation. Keep the register uniform throughout a file.
- **Direct Imperatives:** English documentation loves direct commands like *"Click here"* or *"Run the following script."* Render these as polite guiding instructions—use either the 합니다체 declarative (**"~를 실행합니다"**) or the polite imperative (**"~를 실행하십시오"**) consistently, rather than blunt commands. Avoid casual forms like "~하세요" when the rest of the document is in 합니다체.

#### Syntactic Readability for Code Logic

- **Conditional Mapping ("If" statements):** In English, conditional outcomes often come first (*"An error will occur if the key is missing"*). Korean reads more naturally with the condition first, so prefer reordering the logic so the prerequisite precedes the result (*"키가 누락되면 오류가 발생합니다"*). The leading *만약* is optional and can be omitted when *~면* already signals the condition.
- **Variables as Nouns:** Technical English often weaves variables into sentences (*"where x is the user ID"*). Ensure the Korean translation cleanly isolates the variable marker, using phrases like **"여기서 x는 사용자 ID를 나타냅니다."**

### Quick Quality Checklist for Developer Docs

| What to Flag (Bad ❌) | What to Approve (Good ⭕) | Why it Matters |
| :--- | :--- | :--- |
| **"git 커밋을 저장하십시오"** | **"git commit을 수행합니다"** | Keeps the exact CLI keyword `git commit` in English instead of translating it to "커밋 저장". |
| **"그녀의 토큰"** (Using "Her/Its token") | **"해당 토큰"** or omit the pronoun | Korean drops pronouns; "그녀" (she) or "그것" (it) breaks technical flow. |
| **"라이브러리들"** (Plural "Libraries") | **"라이브러리"** | Plural markers (`~들`) are repetitive in technical specs. |
| **"콜백 함수"** (No English reference) | **"콜백 함수(Callback function)"** | Allows developers to easily look up the original English error/API docs. |

## Evaluator Scoring Rubric

This is the **definitive pass/fail gate** for the `evaluator` role. Criteria are split into two tiers:

- **Tier A — Hard-fail criteria:** any material defect makes the document unusable, so these **must score 5 to pass**. A single broken command, altered number, corrupted link, or distorted fact fails the document outright.
- **Tier B — Graded criteria:** scored on the 1–5 scale below; these **pass at 4 or 5**.

A document **PASSES only when every applicable Tier A criterion scores 5 and every applicable Tier B criterion scores 4 or 5.** Otherwise it FAILS and is returned to the translator with specific notes (cite the offending source/target snippet and the failed criterion), then re-scored. If a document still fails the same subjective criterion after **3 iterations**, escalate to a human rather than looping further.

Tier B scale (applies to every Tier B criterion):

- **5 — Excellent:** Fully meets the criterion; no issues.
- **4 — Good (pass):** Meets the criterion; at most 1–2 trivial, non-blocking nits per ~1,000 words.
- **3 — Borderline (fail):** Several noticeable issues, or any issue that changes how a sentence reads; revision required.
- **2 — Poor (fail):** Frequent or significant violations throughout.
- **1 — Unacceptable (fail):** Criterion is largely unmet.

### Determining content type

Before scoring, classify the document so the right criteria apply:

- **Technical documentation** = content written for developers/operators (API docs, READMEs, tutorials, CLI guides, reference) **or any document that contains code, commands, or API identifiers**. Criteria 7–8 apply.
- **Non-technical content** = UI strings, marketing, narrative, or conversational copy with no code. Criteria 7–8 do **not** apply, and the register target in Criterion 4 is the audience-appropriate one rather than 합니다체.

If a non-technical document still contains occasional code or links, Tier A Criterion 2 (and Criterion 7, for those code spans) still apply to those spans.

### Tier A — Hard-fail criteria (must score 5)

| # | Criterion | Passes (5) when… | Fails (<5) when… |
| :-- | :--- | :--- | :--- |
| 1 | **Accuracy (정확성)** | Meaning matches the source exactly; every number, name, and fact is preserved; nothing is added, distorted, or omitted. | **Any** mistranslation, negation flip, fabricated/dropped fact, or altered number/name — even a single isolated one. |
| 2 | **Markdown & Structural Integrity** | Frontmatter keys, Markdown structure, tables, and external URLs are preserved exactly; heading order is stable. Heading anchors follow the localized headings, and every same-document anchor link resolves to its (now-localized) target. Image/asset paths resolve to a real asset—the original asset (relative path rewritten as needed) unless a localized asset exists. | **Any** broken link (including a same-document anchor that points at the original English slug after its heading was translated), unresolved image path, translated frontmatter key, or corrupted Markdown/table. |

### Tier B — Graded criteria (must score ≥4)

These are **always scored** unless marked technical-only.

| # | Criterion | Scores 5 when… | Pass floor — Score 4 | Fail ceiling — Score 3 | Scores 1 when… |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 3 | **Fluency (유창성)** | Reads naturally on first pass; grammar, spelling, spacing (띄어쓰기), and punctuation all correct; no 번역투 or passive-voice overuse. | ≤2 minor spacing/punctuation slips that don't impede reading. | Any awkward 번역투 sentence requiring re-reading, or 3+ grammar/spacing/punctuation errors. | Pervasive awkwardness; frequent grammar/spacing errors. |
| 4 | **Honorifics & Tone** | Register is uniform and matches the content type (합니다체 for documentation; audience-appropriate register otherwise); no unintended slips. | A single isolated ending slip that doesn't shift the perceived register. | 2+ register slips, or a tone that doesn't fit the audience. | Register is mixed or clearly inappropriate throughout. |
| 5 | **Terminology & Consistency** | Terms follow the locale rules and are used uniformly; correct accepted-equivalent vs. transliteration choices; first-mention English reference applied where useful. | 1 minor terminology inconsistency a reader can still follow. | 2+ inconsistent renderings of the same term, or one over-translation (e.g., *Instance* → "실체"). | Terminology is inconsistent or over-translated throughout. |
| 6 | **Cultural & Linguistic Naturalness** | Idioms adapted naturally; subjects/pronouns dropped where Korean would; no redundant plural `~들`. | 1–2 redundant pronouns/plurals that don't distort meaning. | Several literal idioms or redundant pronoun/`~들` patterns that read unnaturally. | Literal idiom calques and redundant pronouns/plurals throughout. |
| 7 | **Code & Command Integrity** *(technical only — Tier A severity: any violation caps this at ≤2)* | Variables, function names, APIs, and CLI commands are untouched and in English; only explanatory prose and human-language code comments are translated. | — (no "trivial" tolerance; treat as hard-fail) | A single translated/altered identifier or command. | Code, identifiers, or commands are translated or altered. |
| 8 | **Developer Terminology Convention** *(technical only)* | Industry-standard English/Hangul terms used as developers expect; native over-translations avoided for established coding concepts. | 1 borderline term choice that developers would still recognize. | A forced native translation of an established term, or terms developers wouldn't recognize. | Established concepts consistently forced into unnatural native Korean. |

> Criterion 7 carries Tier A severity in practice: a broken command or identifier is never a "non-blocking nit", so any violation fails the document. It is listed in Tier B only because it is conditional on technical content.

**Overall result:** PASS only if every applicable **Tier A** criterion = 5 **and** every applicable **Tier B** criterion ≥ 4 (criteria 7–8 apply to technical documentation only). Otherwise FAIL and iterate, up to the 3-iteration escalation cap. Score each criterion independently; if one defect could fall under two criteria, record it under the most specific one and do not double-penalize.
