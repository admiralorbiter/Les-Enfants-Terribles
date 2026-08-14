---
title: "Decisions and Open Questions"
project: "Les Enfants Terribles"
project_code: "LET"
status: "working_register"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


# Decisions and Open Questions

## 1. Decision register

### LET-D-001 — Desktop-first

**Decision:** The first field period targets Windows desktop through a local browser application.

**Rationale:** Movies, piano, gaming, research, and programming already occur near the desktop. Mobile is not required to validate the first loop.

**Reconsider when:** Desktop access prevents natural capture.

---

### LET-D-002 — Capture and Liquid are parallel cores

**Decision:** The first product is not capture-only. Liquid support is developed alongside capture at a minimal level.

**Rationale:** Metacognitive novelty is the primary desired value; capture is the substrate.

**Reconsider when:** Liquid adds enough complexity to delay trustworthy capture.

---

### LET-D-003 — Intentional capture first

**Decision:** Begin with deliberate voice/text/upload/mark capture.

**Rationale:** Natural episode boundaries are already known; passive-stream value is not yet established.

**Reconsider when:** A specific unanswered question requires context that intentional capture cannot provide.

---

### LET-D-004 — Raw media retained

**Decision:** Original recordings are retained indefinitely by default.

**Rationale:** Raw experience cannot be recreated; derived processing can be replayed.

**Reconsider when:** Storage scale creates practical risk or cost.

---

### LET-D-005 — Local archive, flexible processing

**Decision:** Durable archive and metadata are local. Selected material may be processed by cloud models.

**Rationale:** Privacy is not the main constraint; cost, portability, and provenance are.

**Reconsider when:** A provider or collaboration workflow requires a different boundary.

---

### LET-D-006 — Zero recurring API cost by default

**Decision:** Do not require paid APIs in the initial architecture.

**Rationale:** Existing subscriptions and local tools provide abundant processing; early learning does not justify metered integration.

**Reconsider when:** Measured integration value exceeds cost and manual burden.

---

### LET-D-007 — Manual AI bridge is first-class

**Decision:** Export/import through Antigravity or subscription interfaces is an accepted processor path.

**Rationale:** It permits strong-model experiments before API integration.

**Reconsider when:** Manual transport becomes the dominant operational friction.

---

### LET-D-008 — Filesystem media + SQLite metadata

**Decision:** Raw/derived media stays in the filesystem; SQLite stores identity, metadata, lineage, jobs, and searchable text.

**Rationale:** This preserves portability and avoids unnecessary BLOB complexity.

**Reconsider when:** Atomicity, portability, or deployment evidence favors another design.

---

### LET-D-009 — Flask + Jinja/HTMX

**Decision:** Use the user’s familiar Python/Flask stack for the first local application.

**Rationale:** Development risk and setup cost are lower; the UI does not require a large frontend framework.

**Reconsider when:** browser-media behavior or real-time interaction becomes significantly harder than a native/Tauri design.

---

### LET-D-010 — Processing is asynchronous

**Decision:** Capture success does not depend on transcription or AI.

**Rationale:** The moment must be preserved even when compute fails.

**Reconsider when:** Never; this is a core reliability principle, though implementation may evolve.

---

### LET-D-011 — Episode is the organizing unit

**Decision:** Multiple artifacts and reflections are grouped around meaningful episodes.

**Rationale:** This matches natural use and supports cross-modal reasoning.

**Reconsider when:** real use repeatedly requires a different unit.

---

### LET-D-012 — Observation and intervention are distinct

**Decision:** The data model separately records what was observed before and after Liquid acts.

**Rationale:** Prevent S3 Contamination.

**Reconsider when:** never at the conceptual level.

---

### LET-D-013 — Explicit modes before inferred modes

**Decision:** Jonathan may choose the desired cognitive support stance.

**Rationale:** It improves control and creates labels for later personalization.

**Reconsider when:** inferred selection demonstrates clear value while preserving override.

---

### LET-D-014 — Raw, transcript, and polished writing remain separate

**Decision:** A generated or edited review never overwrites the original reaction.

**Rationale:** Preserve authentic historical state and derivation.

---

### LET-D-015 — Professional episodes permitted, canonical professional data separated

**Decision:** LET may hold professional reflections but does not replace or silently duplicate `modeling`.

**Rationale:** Work is cognitively important; data-governance boundaries should remain legible.

---

### LET-D-016 — No more than three active experiments

**Decision:** Limit simultaneous experimental changes.

**Rationale:** Preserve usability and causal interpretability.

---

### LET-D-017 — Metal Gear terminology is conceptual, not gimmick-only

**Decision:** Use the framing for architecture and failure modes; keep low-level code names understandable.

**Rationale:** The metaphor should clarify rather than obscure.

---

### LET-D-018 — Slice 2 Decomposition (2A, 2B, 2C)

**Decision:** Decompose Slice 2 (Liquid Core & AI Bridge) into three independent, testable micro-slices:
- **Slice 2A:** Mission Brief Export & Polished Synthesis/Response Import (pure prompt and bridge probe);
- **Slice 2B:** Flexible Follow-Up Dialogue (multi-modal voice and typed text note responses);
- **Slice 2C:** Lightweight Calibration & Built-in Heuristics (1-tap feedback and offline deterministic question templates).

**Rationale:** Avoids conflating prompt quality, bridge friction, and interaction modality. Allows rapid validation of external AI value before building complex conversational branching.

---

### LET-D-019 — Dual Output of Mission Brief (Polished Synthesis + Liquid Perturbation)

**Decision:** The Mission Brief protocol requests two distinct, versioned derived artifacts:
1. **Polished Synthesis / Review Note:** A clean, publication-ready restructuring of the spoken thought in Jonathan's authentic voice (for Letterboxd, notes, or professional docs);
2. **Liquid Perturbation:** 1–2 high-leverage cognitive questions or challenges tailored to the declared mode.

**Rationale:** Satisfies the practical need for clean written summaries from spoken rambles while preserving strict epistemic separation and providing metacognitive challenge.

---

### LET-D-020 — Single-Transaction Capture & Storage Relativity

**Decision:** Store all artifact file paths relative to `config.data_dir` in SQLite, write raw media to disk before database insertion, commit `Episode`, `Artifact`, `Event`, and `Job` in a single SQLite transaction, and emit local JSON crash recovery receipts if the database transaction fails.

**Rationale:** Prevents orphaned state across directories, guarantees database portability across machines and folders, and eliminates partial-save capture loss.

---

### LET-D-021 — Native SQLite Disaster Recovery & Verified Rehearsal

**Decision:** Implement backup and restore via SQLite's online backup API (`conn.backup`) alongside cryptographic `manifest.json` generation and trial rehearsal verification (`let backup`, `let restore --verify`).

**Rationale:** Plain file copies of active WAL databases risk corruption. Verified rehearsal in isolated scratch directories proves disaster recoverability before live mutation.

## 2. Open questions

### LET-Q-001 — Data root and backup [RESOLVED by LET-D-020 & LET-D-021]

Resolved: Dedicated local folder `~/.let_data` (overridable via `LET_DATA_DIR`) with native online SQLite backups, cryptographic `manifest.json` generation, and `let restore --verify` rehearsals.

### LET-Q-002 — Exact transcription configuration

Which local model/precision provides acceptable speed and quality on the RTX 3060/Windows setup?

### LET-Q-003 — Episode metadata burden

Should initial capture ask for:

- nothing;
- domain only;
- title and domain;
- activity/mode;
- classification after capture?

### LET-Q-004 — Liquid v0

Should Liquid initially use:

- fixed question primitives;
- one strong-model prompt;
- both as a comparison?

### LET-Q-005 — Response import

What is the smoothest first manual bridge?

- clipboard;
- Markdown export/import;
- JSON;
- browser extension;
- watched folder.

### LET-Q-006 — Long recordings

Should browser recording upload at Stop or stream chunks during capture?

Defer until ordinary recording length demonstrates the need.

### LET-Q-007 — MARK

What is the least disruptive marker mechanism?

- in-app button;
- global hotkey;
- keyboard shortcut while app focused;
- external device later.

### LET-Q-008 — Feedback vocabulary

Which minimal labels produce useful evidence without turning interaction into rating work?

### LET-Q-009 — Mode vocabulary

Are the initial modes distinct and understandable in actual use?

### LET-Q-010 — Movie metadata

When does Plex integration become worth it, and does the current Plex setup support the required webhooks?

### LET-Q-011 — Professional boundary

What professional reflections are safe/useful to export to external subscription models?

### LET-Q-012 — Replay UI

What comparison is useful:

- side-by-side outputs;
- diff;
- human preference;
- error taxonomy;
- later usefulness?

### LET-Q-013 — Joy representation

How can LET learn about joy without reducing it to a crude score?

### LET-Q-014 — Solid onset

What minimum evidence warrants the first bounded Solid prediction?

### LET-Q-015 — Voice beyond transcript

Which non-text vocal features, if any, are useful and responsibly interpretable?

### LET-Q-016 — Sensor trigger rule

What exact unmet question would justify ActivityWatch, screenpipe, Plex, Git, gameplay, MIDI, or wearable integration?

### LET-Q-017 — Code visibility

Should the code repository remain private initially and become public after data boundaries and setup stabilize?

### LET-Q-018 — Experiment statistics

At what point is repeated informal use enough, and when should LET use randomization or a formal within-person design?

### LET-Q-019 — Follow-up Modality & Multi-turn Thread Pulling in the Bridge

When Liquid generates a sharp perturbation, how should follow-up exploration and resolution be captured in LET?

- **Case 1 (Single-Shot Punch):** The question is immediately clear and Jonathan wants to record a direct voice or text answer attached to the episode in LET.
- **Case 2 (Thread Pulling):** The question opens a broader thread where Jonathan chats back and forth with external AI (Antigravity, ChatGPT, Claude) across 3–4 turns before the core insight crystallizes. At what point and in what format should that final crystallization be synthesized and imported into LET?
- **Evolutionary Path:** How does this manual third-party chat workflow transition to an internal/local Liquid engine over time without corrupting artifact lineage?

## 3. Deliberately undecided

The following should not be decided before evidence:

- final twin ontology;
- vector store;
- knowledge graph;
- passive screen capture;
- mobile framework;
- wearable;
- learned policy;
- Solidus implementation;
- provider abstraction breadth;
- public product;
- autonomous action.

## 4. Decision review rule

A decision changes when:

- real use contradicts it;
- a simpler approach performs as well;
- a new constraint appears;
- maintenance exceeds value;
- safety/joy evidence changes;
- the dependent experiment ends.

Changes should preserve the prior decision and explain the new basis.
