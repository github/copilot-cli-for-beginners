# es-es

These rules apply to **both roles**: the `translator` agent uses them as generation directives (how to write the Spanish text), and the `evaluator` agent uses them as review criteria (what to check and flag). Wherever a rule says "flag" or "look for", the translator should read it as "produce text that satisfies this".

In general, producing and evaluating translation quality requires both the accuracy of the meaning and the natural flow of the language. To do this, verify that the text passes core tests for accuracy, fluency, consistency, and cultural appropriateness.

Here are the 4 core pillars:

- **Accuracy:** Ensure the meaning matches the source text exactly, with no information added, distorted, or omitted.
- **Fluency:** Check that grammar, punctuation, and spelling adhere to the conventions of the target language so that the text reads naturally.
- **Terminology & Consistency:** Verify that specialized terms, names, and key phrases are used uniformly throughout the document.
- **Cultural Appropriateness:** Confirm that idioms, metaphors, and the overall tone are culturally sensitive and suited to the target audience.

## English to Spanish Localization Scenario

English-to-Spanish translation quality is best evaluated by checking for natural sentence structures, correct register (formal versus informal address), grammatical gender and number agreement, and accurate transformation of English idioms into natural Spanish expressions. Spanish carries grammatical features—gender agreement, verb conjugation, and inverted punctuation marks—that automated tools often handle incorrectly, and it favors a flow that differs noticeably from literal English word order.

### Key Evaluation Pillars for Spanish

- **Register and Tone (formal vs. informal):** Verify that the form of address—formal (*usted*) versus informal (*tú*)—and, for documentation, the convention of the impersonal/infinitive register is uniform and fits the target audience. For documentation, this typically means addressing the reader with *usted* or avoiding direct address altogether, consistently throughout.
- **Gender and Number Agreement:** Ensure that articles, adjectives, and participles agree in gender and number with the nouns they modify (e.g., *la nueva función*, not *el nuevo función*).
- **Subject Pronoun Omission:** Check that unnecessary subject pronouns like "yo", "tú", "él", or "ellos" are dropped, since Spanish is a pro-drop language and the verb conjugation already conveys the subject when context is clear.
- **Inverted Punctuation:** Confirm that questions and exclamations open with the inverted marks (¿ … ? and ¡ … !), which English lacks and machine output frequently omits.
- **Terminology Adaptation:** Confirm whether technical words are accurately translated into established Spanish terms or appropriately kept as accepted English loanwords.

### Common Translation Mistakes to Flag

- **Anglicism Overuse (Calques):** Watch for English structures copied literally, such as "en orden de" for *in order to* (use *para*) or false friends like *actualmente* mistaken for "actually" (it means "currently").
- **Gerund Misuse:** English uses the *-ing* form liberally; Spanish does not. Flag literal gerund translations where Spanish prefers an infinitive or a relative clause (e.g., *"un archivo conteniendo datos"* → *"un archivo que contiene datos"*).
- **Passive Voice Overuse:** English frequently uses passive voice, but natural Spanish favors active constructions or the impersonal/reflexive *se* (e.g., *"se ejecuta el comando"* rather than *"el comando es ejecutado"*).
- **Capitalization Carryover:** English title-case and capitalized common nouns, days, months, and languages should follow Spanish rules (lowercase for *lunes*, *enero*, *español*; sentence case for headings).

### Practical Evaluation Framework

| Evaluation Metric | What to Look For (English to Spanish Context) |
| :--- | :--- |
| **Accuracy (Precisión)** | Are critical numbers, names, and core English meanings preserved without distortion? |
| **Fluency (Fluidez)** | Does a native Spanish speaker understand the text instantly without re-reading sentences? |
| **Style Guide (Estilo)** | Does the text follow Spanish spelling, accent marks (tildes), inverted punctuation, and capitalization rules? |

## Localization for Technical Documents for Developers

When evaluating English-to-Spanish technical documentation for developers, standard linguistic rules change. Spanish-speaking developers heavily favor industry-standard English terminology over forced Spanish translations for many concepts. If a translation forces purely native Spanish words for established coding concepts, it will look amateurish and confuse the reader.

Evaluate your developer documentation by looking for specific markers across structural, lexical, and formatting levels.

### The Developer-Specific Evaluation Rubric

#### Terminology & Loanwords (lo más importante)

- **Avoid "Over-Translation":** Some terms have well-established Spanish equivalents and should use them (e.g., *String* → **cadena**, *Array* → **arreglo/matriz**, *Dependency* → **dependencia**, *File* → **archivo**). Others are commonly kept in English by Spanish-speaking developers and should not be force-translated (e.g., *Thread*, *Commit*, *Deploy*, *Framework*, *Backend*). When unsure, prefer the form Spanish developers actually use over a literal dictionary translation, and keep the chosen term consistent throughout (see Terminology & Consistency).
- **The First-Mention Rule:** For critical or unfamiliar technical jargon, the **first occurrence within a single file** may give the Spanish term followed by the original English in parentheses—for example, **interfaz de programación de aplicaciones (API)**—or keep the English term followed by a brief Spanish gloss. This follows the standardized [Microsoft Spanish Localization Style Guide](https://learn.microsoft.com/globalization/reference/microsoft-style-guides) for technical acronyms and core definitions. Subsequent mentions in the same file can use the shorter form. Apply this selectively to terms a reader may want to look up in English, not to every loanword.
- **Code Elements Untouched:** Ensure variables, function names, APIs, CLI commands (`npm install`), and code itself are kept exactly as in the source. However, **human-language comments inside code blocks** (e.g., `// fetch the user`) *should* be localized, since they are explanatory prose for the reader.

#### Tone and Politeness Level (registro formal)

- **The Impersonal/Formal Standard:** Developer docs should use a neutral, formal register—either addressing the reader as **usted** or, more commonly, using impersonal constructions and the infinitive for instructions. This is the conventional register for Spanish technical documentation and is what the Microsoft Spanish Localization Style Guide prescribes. Do **not** drop into the informal **tú** ("haz clic", "ejecuta"), which reads too casual for documentation. Keep the register uniform throughout a file.
- **Direct Imperatives:** English documentation loves direct commands like *"Click here"* or *"Run the following script."* Render these with the formal imperative (**"Haga clic aquí"**, **"Ejecute el siguiente script"**) or the infinitive (**"Para ejecutar el script…"**) consistently, rather than the informal *tú* imperative. Avoid mixing *"haz"* and *"haga"* within the same document.

#### Syntactic Readability for Code Logic

- **Conditional Mapping ("If" statements):** In English, conditional outcomes often come first (*"An error will occur if the key is missing"*). Spanish reads naturally either way, but prefer placing the condition first for clarity (*"Si falta la clave, se produce un error"*). Keep the conditional connector *si* without a written accent (unlike *sí*, "yes").
- **Variables as Nouns:** Technical English often weaves variables into sentences (*"where x is the user ID"*). Ensure the Spanish translation cleanly isolates the variable, using phrases like **"donde x es el identificador de usuario (user ID)"**. For agreement, attach the variable to an explicit head noun rather than guessing its gender (*"el valor de x"*, *"la variable x"*).

### Quick Quality Checklist for Developer Docs

| What to Flag (Bad ❌) | What to Approve (Good ⭕) | Why it Matters |
| :--- | :--- | :--- |
| **"Guarde el commit de git"** | **"Ejecute `git commit`"** | Keeps the exact CLI keyword `git commit` in English instead of translating it to "guardar el commit". |
| **"Haz clic en el botón"** (informal *tú*) | **"Haga clic en el botón"** or **"Hacer clic en el botón"** | Documentation uses the formal/impersonal register, not the casual *tú* imperative. |
| **"el nuevo función"** (gender disagreement) | **"la nueva función"** | Articles and adjectives must agree in gender with the noun (*función* is feminine). |
| **"función de retorno de llamada"** (no English reference) | **"callback (función de retorno de llamada)"** | Leads with the term developers actually use in English, with a Spanish gloss, so they can look up the original API/error docs. |

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
- **Non-technical content** = UI strings, marketing, narrative, or conversational copy with no code. Criteria 7–8 do **not** apply, and the register target in Criterion 4 is the audience-appropriate one rather than the formal/impersonal documentation register.

If a non-technical document still contains occasional code or links, Tier A Criterion 2 (and Criterion 7, for those code spans) still apply to those spans.

### Tier A — Hard-fail criteria (must score 5)

| # | Criterion | Passes (5) when… | Fails (<5) when… |
| :-- | :--- | :--- | :--- |
| 1 | **Accuracy (Precisión)** | Meaning matches the source exactly; every number, name, and fact is preserved; nothing is added, distorted, or omitted. | **Any** mistranslation, negation flip, fabricated/dropped fact, or altered number/name — even a single isolated one. |
| 2 | **Markdown & Structural Integrity** | Frontmatter keys, Markdown structure, tables, URLs, link targets, image paths, and heading anchors/slugs are preserved exactly; heading order is stable. | **Any** broken link, altered anchor, translated frontmatter key, or corrupted Markdown/table. |

### Tier B — Graded criteria (must score ≥4)

These are **always scored** unless marked technical-only.

| # | Criterion | Scores 5 when… | Pass floor — Score 4 | Fail ceiling — Score 3 | Scores 1 when… |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 3 | **Fluency (Fluidez)** | Reads naturally on first pass; grammar, spelling, accent marks (tildes), and punctuation all correct; no anglicism calques or passive-voice overuse. | ≤2 minor accent/punctuation slips that don't impede reading. | Any awkward calque sentence requiring re-reading, or 3+ grammar/accent/punctuation errors. | Pervasive awkwardness; frequent grammar/accent errors. |
| 4 | **Register & Tone** | Register is uniform and matches the content type (formal/impersonal for documentation; audience-appropriate register otherwise); no unintended slips between *tú* and *usted*. | A single isolated address slip that doesn't shift the perceived register. | 2+ register slips, or a tone that doesn't fit the audience. | Register is mixed or clearly inappropriate throughout. |
| 5 | **Terminology & Consistency** | Terms follow the locale rules and are used uniformly; correct accepted-equivalent vs. English-loanword choices; first-mention English reference applied where useful. | 1 minor terminology inconsistency a reader can still follow. | 2+ inconsistent renderings of the same term, or one over-translation (e.g., *Thread* → "hilo de ejecución" where developers expect "thread"). | Terminology is inconsistent or over-translated throughout. |
| 6 | **Cultural & Linguistic Naturalness** | Idioms adapted naturally; subject pronouns dropped where Spanish would; correct gender/number agreement; inverted punctuation present. | 1–2 redundant pronouns or minor agreement slips that don't distort meaning. | Several literal idioms, redundant subject pronouns, missing inverted marks, or agreement errors that read unnaturally. | Literal idiom calques, redundant pronouns, and agreement errors throughout. |
| 7 | **Code & Command Integrity** *(technical only — Tier A severity: any violation caps this at ≤2)* | Variables, function names, APIs, and CLI commands are untouched and in English; only explanatory prose and human-language code comments are translated. | — (no "trivial" tolerance; treat as hard-fail) | A single translated/altered identifier or command. | Code, identifiers, or commands are translated or altered. |
| 8 | **Developer Terminology Convention** *(technical only)* | Industry-standard English/Spanish terms used as developers expect; native over-translations avoided for established coding concepts. | 1 borderline term choice that developers would still recognize. | A forced native translation of an established term, or terms developers wouldn't recognize. | Established concepts consistently forced into unnatural native Spanish. |

> Criterion 7 carries Tier A severity in practice: a broken command or identifier is never a "non-blocking nit", so any violation fails the document. It is listed in Tier B only because it is conditional on technical content.

**Overall result:** PASS only if every applicable **Tier A** criterion = 5 **and** every applicable **Tier B** criterion ≥ 4 (criteria 7–8 apply to technical documentation only). Otherwise FAIL and iterate, up to the 3-iteration escalation cap. Score each criterion independently; if one defect could fall under two criteria, record it under the most specific one and do not double-penalize.
