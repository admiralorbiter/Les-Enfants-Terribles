---
title: "Research Map and Related Systems"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


# Research Map and Related Systems

## 1. Research posture

Research informs options and tests. It does not automatically become product requirements.

For every external finding distinguish:

1. phenomenon;
2. supported finding;
3. population/task boundary;
4. design implication;
5. LET hypothesis;
6. local probe.

Evidence authority:

```text
systematic review / meta-analysis
primary replicated research
standards / official technical documentation
single primary study
recent preprint
analogy
local observation
```

Local evidence may be highly decision-relevant for Jonathan, but it supports only the scope actually tested.

## 2. Experience sampling and reactivity

### What it contributes

Experience-sampling methods collect reports close to lived experience, reducing some retrospective loss and exposing within-person dynamics.

Repeated measurement can also change thoughts or behavior, and compliance can decline under demanding protocols.

### LET implication

- prefer voluntary natural decision points;
- avoid constant random prompts initially;
- treat measurement as a possible intervention;
- keep observation and intervention distinct;
- operational burden matters.

### Local probe

Compare spontaneous post-episode capture with a structured prompt in one domain.

### Starting sources

- Eisele et al. (2023), measurement reactivity:
  https://pubmed.ncbi.nlm.nih.gov/36174163/
- Rintala et al. (2019), response compliance:
  https://pubmed.ncbi.nlm.nih.gov/30394762/

## 3. Event segmentation and episodic memory

### What it contributes

Continuous experience is cognitively organized around event boundaries. Event boundaries are disproportionately remembered, and event segmentation affects later reconstruction.

### LET implication

- Episode is a cognitive unit, not only a database folder;
- natural boundaries—movie end, match end, piece break, commit/merge—are valuable capture points;
- passive streams should later be segmented into meaningful episodes.

### Starting source

- Jeunehomme & D’Argembeau (2018), event segmentation and temporal compression:
  https://pubmed.ncbi.nlm.nih.gov/29982966/

## 4. After-action review and debriefing

### What it contributes

Meta-analytic evidence indicates structured after-action review can improve training outcomes, with stronger effects when aligned to the task/person and supported by objective performance media.

### LET implication

- post-episode reflection is plausible;
- piano/game recordings may be more valuable than introspection alone;
- facilitation should be domain-specific;
- debriefing should not become generic questioning.

### Starting source

- Keiser & Arthur (2021), AAR meta-analysis:
  https://pubmed.ncbi.nlm.nih.gov/32852990/

## 5. Self-regulated learning and music

### What it contributes

Music self-regulation research commonly uses cycles of forethought, performance/practice, and self-reflection. Reviews identify planning, self-monitoring, self-recording, strategy instruction, external feedback, and technology as useful mechanisms, with mixed effects depending on context and study quality.

### LET implication

- separate practice from performance;
- ask predictions before evidence;
- provide an external perspective after;
- preserve learner control;
- do not assume more reflection always improves performance.

### Starting sources

- Wang et al. (2025), metacognition/SRL in music:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12734040/
- Lubert & Gröpel (2025), self-regulated music-performance interventions:
  https://doi.org/10.1177/10298649241290448
- Silva & Marinho (2025), advanced musicians’ SRL:
  https://doi.org/10.1177/10298649241275614
- Queiroz et al. (2025), pedagogical SRL approaches:
  https://doi.org/10.1177/03057356251348414

## 6. Self-controlled feedback and motor learning

### What it contributes

A 2025 meta-analysis found learner-controlled feedback showed benefits for retention and transfer, though not a clear acquisition advantage.

### LET implication

- “ask me / later / ignore” is not merely UX;
- Jonathan should initially control when piano/game feedback arrives;
- later predictive timing should remain overrideable.

### Starting source

- Wang et al. (2025):
  https://pubmed.ncbi.nlm.nih.gov/41009321/

## 7. Just-in-time adaptive intervention structure

### What it contributes

JITAI research formalizes decision points, tailoring variables, intervention options, decision rules, proximal outcomes, availability, and intervention fatigue. Micro-randomized trials repeatedly compare intervention options, including no intervention.

### LET implication

Borrow the experimental structure, not the health claims:

```text
decision point
context
available options
selection
no-intervention possibility
proximal outcome
```

This is a strong model for later Liquid timing and stance selection.

### Starting sources

- Nahum-Shani et al., JITAI design principles:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5364076/
- Klasnja et al., micro-randomized trials:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9755932/
- MRT applied design overview:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8887814/

## 8. Voice diaries

### What it contributes

A 2026 scoping review found voice-diary computational analysis remains early, mostly transcript-centered, rarely multimodal, and inconsistently validated.

### LET implication

- raw voice preservation is more important than current analysis;
- transcript-only systems discard potentially useful signal;
- acoustic inference should remain experimental;
- transparent validation is required.

### Starting source

- Nemeti et al. (2026):
  https://pubmed.ncbi.nlm.nih.gov/42175039/

## 9. Cognitive twins

> *"Can a machine replicate the human heart? The Mammal Pod wasn't meant to make decisions—it was built to understand her thinking."*
> — *Adapted from Dr. Strangelove, Peace Walker*

### What it contributes

Recent preprints describe cognitive twins as longitudinal, personalized representations that may model or simulate cognition. One education study builds a hierarchy from behavioral instances through patterns, cognitive routines, metacognitive tendencies, and values. Governance work warns that cognitive representation itself creates authority and control risks before any autonomous action occurs.

### LET implication

- layered models are plausible;
- fidelity must be evaluated;
- higher abstraction requires lower default authority;
- representation, access, contestation, and retirement need governance;
- LET should not rush to proxy action.

### Starting sources

- Hwang et al. (2026), Cognitive Twins:
  https://arxiv.org/abs/2605.04761
- Bonagiri et al. (2026), cognitive-digital-twin governance:
  https://arxiv.org/abs/2606.23094

These are recent preprints and should not be treated as settled architecture.

## 10. External cognition and lifetime stores

### MyLifeBits

What it demonstrates:

- long-lived heterogeneous personal archives;
- search;
- annotations;
- links;
- saved queries;
- multiple representations over the same source material.

What LET should borrow:

- durable source substrate;
- replay/reuse;
- rich derived views.

What LET should not assume:

- total capture itself creates understanding.

Sources:

- https://www.microsoft.com/en-us/research/project/mylifebits/
- https://www.microsoft.com/en-us/research/publication/the-mylifebits-lifetime-store/

## 11. Related software systems

### ActivityWatch

Project:
https://github.com/ActivityWatch/activitywatch

Useful concepts:

- independent watchers;
- local event API;
- active-window and AFK events;
- extensibility;
- timeline/query model;
- user-owned data.

Potential LET use:

- later source of lightweight computer-context events;
- model for sensor adapters.

Do not copy:

- generic time-tracking as the core purpose.

### screenpipe

Project:
https://github.com/screenpipe/screenpipe

Useful concepts:

- event-driven screen capture;
- accessibility-tree-first extraction;
- audio transcription;
- local SQLite/FTS;
- REST/MCP access;
- per-agent data permissions;
- derived agents over captured context.

Potential LET use:

- experimental external sensor when screen history becomes relevant.

Caution:

- current product/licensing/pricing and branch behavior may change;
- its broad continuous-capture posture is not LET’s initial approach;
- integration must follow a concrete hypothesis.

### Omi

Project:
https://github.com/BasedHardware/omi

Useful concepts:

- desktop/mobile/wearable conversation capture;
- transcription pipeline;
- device SDKs;
- app ecosystem;
- multi-modal expansion.

Potential LET use:

- future phone/wearable sensor;
- reference for device protocol and capture infrastructure.

Do not copy initially:

- cloud-heavy backend complexity;
- always-on product scope.

### Plex

Official webhook documentation:
https://support.plex.tv/articles/115002267687-webhooks/

Potential LET use:

- media-play/stop/scrobble events;
- automatic episode metadata for home viewing.

Do not integrate until the manual movie flow is useful and webhook availability under the current Plex account is confirmed.

### Big Brain Time

Useful prior mechanisms:

- re-entry;
- context packs;
- audit;
- replayable derived stores;
- handoff;
- epistemic reconciliation.

Lesson:

- mechanisms should be pulled by observed use, not implemented as a predetermined feature sequence.

### PREP-KC modeling

Useful prior mechanism:

- Markdown + agent rules can produce real operational leverage.

Boundary:

- it models the external professional system;
- LET models human cognition and intervention;
- integration is a later governed bridge.

## 12. Browser and storage foundations

### Browser media capture

MDN:
https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API

Design implication:

- desktop one-button audio capture can begin in a browser without a native app.

### SQLite

Official documentation:

- WAL: https://sqlite.org/wal.html
- FTS5: https://sqlite.org/fts5.html

Design implication:

- one local database can support metadata, jobs, and transcript search while raw media remains on disk.

### Faster Whisper

Project:
https://github.com/SYSTRAN/faster-whisper

PyPI:
https://pypi.org/project/faster-whisper/

Design implication:

- local, replaceable transcription without mandatory API cost.

## 13. Research gaps LET can explore

- When does metacognitive questioning deepen experience versus weaken flow?
- Which question primitives produce useful novelty across different domains?
- How does self-assessment calibration vary across movies, piano, gaming, research, and programming?
- Can explicit mode selection provide training data for later intervention selection?
- Which parts of voice matter beyond transcript?
- How much personal history improves a model before it creates noise?
- Can a twin distinguish stable tendency from Scene?
- How does intervention change the behavior the twin is trying to model?
- What level of replayability produces practical value?
- Which experiences should remain unoptimized?

## 14. Research rule

A paper can justify a probe.

Only local evidence can justify making that probe part of Jonathan’s life.
