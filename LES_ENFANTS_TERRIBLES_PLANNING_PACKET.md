---
title: "Les Enfants Terribles — Compiled Planning Packet"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---

# Les Enfants Terribles — Compiled Planning Packet

> This file compiles the project planning dossier. Individual source files remain the maintainable version.


---

## Source: `README.md`

# Les Enfants Terribles

> *"Building the future and keeping the past alive are one and the same thing."*
> — **Solid Snake**, *Metal Gear Solid 2: Sons of Liberty*

**Les Enfants Terribles (LET)** is a personal research-and-development project for building an artificial cognitive environment around one living person.

The immediate product is not a clone, autonomous assistant, productivity score, or total-life surveillance system. The immediate product is a low-friction, replayable environment that can:

1. preserve episodes of lived experience;
2. support richer reflection and metacognition;
3. test when different forms of artificial assistance help or harm;
4. accumulate evidence for an inspectable, revisable cognitive model;
5. protect enjoyment, autonomy, and the distinction between the person and the model.

> **Core question:** Can an AI learn when and how to augment this particular human’s cognition—while remaining explicitly uncertain, preserving the original evidence, and avoiding the replacement of life with optimization?

## Current status

This repository packet is a **planning baseline**, not a frozen implementation contract.

The project is ready to begin a small first build and a two-week field period. The first implementation should remain narrow enough that real use can rewrite the roadmap.

## The first principle

> **The raw experience is irreplaceable; every interpretation is replaceable.**

A voice recording, gameplay clip, piano recording, spontaneous thought, or first reaction to a film can only be captured once. Transcripts, summaries, inferences, questions, and twin models can be recomputed later.

## What the project begins with

LET begins with two parallel cores:

```text
LIVED EXPERIENCE
       │
       ├──────────────► CAPTURE
       │                preserve what happened
       │
       └──────────────► LIQUID
                        create productive cognitive perturbation
```

Capture supplies evidence. Liquid asks questions, presents alternatives, requests predictions, points out missing specificity, or chooses silence. Both create richer longitudinal material for later Solid, Liquid, and Solidus models.

## Planning packet

| Document | Purpose |
|---|---|
| [Project Charter](docs/00_PROJECT_CHARTER.md) | Mission, scope, success, anti-goals, and operating principles |
| [Metal Gear Cognitive Model](docs/01_METAL_GEAR_COGNITIVE_MODEL.md) | Conceptual framing, GENE/MEME/SCENE/SENSE, clones, and named failure modes |
| [Product Experience and User Flows](docs/02_PRODUCT_EXPERIENCE_AND_USER_FLOWS.md) | How LET should feel across movies, piano, Call of Duty, research, and programming |
| [Technical Architecture](docs/03_TECHNICAL_ARCHITECTURE.md) | Desktop-first stack, storage, processors, replay, manual AI bridge, and reliability |
| [Data and Epistemic Model](docs/04_DATA_AND_EPISTEMIC_MODEL.md) | Episodes, artifacts, derivations, claims, interventions, and provenance |
| [Experiment Program and Gates](docs/05_EXPERIMENT_PROGRAM_AND_GATES.md) | How evidence—not code completion—controls advancement |
| [Initial Two-Week Field Program](docs/06_INITIAL_TWO_WEEK_FIELD_PROGRAM.md) | Flexible first use period, minimum build, and decision review |
| [Risks, Governance, and Failure Modes](docs/07_RISKS_GOVERNANCE_AND_FAILURE_MODES.md) | Human, epistemic, technical, and Metal Gear-named risks |
| [Research Map and Related Systems](docs/08_RESEARCH_MAP_AND_RELATED_SYSTEMS.md) | Research basis, adjacent projects, and what to borrow |
| [Decisions and Open Questions](docs/09_DECISIONS_AND_OPEN_QUESTIONS.md) | Current decisions, deferred choices, and reconsideration triggers |
| [Agent Rules](AGENTS.md) | Scope and safety rules for coding and research agents |
| [Episode Template](templates/episode-record.md) | Inspectable episode record |
| [Experiment Template](templates/experiment-record.md) | Small experimental protocol and decision record |
| [Processor Template](templates/processor-card.md) | Versioned processor definition and evaluation card |

A compiled single-file copy is also provided as [`LES_ENFANTS_TERRIBLES_PLANNING_PACKET.md`](LES_ENFANTS_TERRIBLES_PLANNING_PACKET.md).

## Intended first-use domains

The first field period deliberately spans different cognitive regimes:

- **Movies:** experience, interpretation, taste, memory, and writing.
- **Piano:** practice, performance, self-evaluation, and motor learning.
- **Call of Duty:** rapid decisions, strategy, flow, adaptation, and fun.
- **Research and spontaneous thought:** hypothesis generation, synthesis, curiosity, and belief revision.
- **Programming:** problem framing, agent delegation, review, architecture, and resumption.

The point is not to optimize all five. The point is to discover whether one underlying architecture can assist them differently.

## Status language

- **Locked for the first field period:** stable enough to build around temporarily.
- **Provisional:** current best option; expected to change.
- **Open:** intentionally unresolved until use provides evidence.
- **Deferred:** explicitly not part of the current build.

## Repository boundary

The code and planning documents may eventually be public. Raw personal media and the live data store should remain outside Git by default, regardless of the user’s broad comfort with cloud processing. This is primarily to prevent accidental repository bloat, duplicated storage, and unintended commits—not to impose a privacy ideology.

## Relationship to other systems

- **PREP-KC `modeling`:** models the external professional world and remains its own canonical knowledge system.
- **Big Brain Time:** supplies prior mechanisms and lessons, but LET is not required to preserve its architecture.
- **LET:** models the human–environment interaction and experiments with context-sensitive cognitive support.

Work episodes may enter LET, but professional ground truth should remain in the professional knowledge base unless a future experiment justifies a governed bridge.

## Governing rule

> Observed human–system behavior is allowed to rewrite this plan.


---

## Source: `AGENTS.md`

# AGENTS.md

These rules apply to any human or AI agent planning, implementing, reviewing, or researching Les Enfants Terribles.

## 1. Primary behavior

Build the smallest reliable instrument that can answer the current experimental question.

Do not treat rapid code generation as evidence that a feature should exist. Development speed is not the bottleneck. The bottleneck is learning what improves the joint system:

```text
Jonathan + AI + artifacts + models + environment + routines
```

## 2. Read before acting

Before substantive work, read:

1. `README.md`;
2. `docs/00_PROJECT_CHARTER.md`;
3. `docs/03_TECHNICAL_ARCHITECTURE.md`;
4. `docs/05_EXPERIMENT_PROGRAM_AND_GATES.md`;
5. `docs/09_DECISIONS_AND_OPEN_QUESTIONS.md`.

Then state:

- the design or research question;
- the smallest proposed change;
- the evidence that would justify keeping it;
- what is explicitly out of scope.

## 3. Scope discipline

- Implement one meaningful vertical slice at a time.
- Do not add adjacent features merely because they are easy.
- Do not convert a probe into a platform before the probe produces evidence.
- Do not build passive capture before a declared question requires that sensor.
- Do not implement Solidus, autonomous interventions, wearables, screen recording, embeddings, a knowledge graph, or agent swarms merely because the architecture permits them.
- Prefer removal and simplification when a feature does not improve real use.

When a task expands, stop and record the additional idea in the open-question or candidate-experiment list.

## 4. Raw evidence is immutable

- A successful capture means the raw artifact is durably saved.
- Never edit, rewrite, or normalize a raw artifact in place.
- Every derived artifact must point back to its source.
- Use content hashes for raw and derived artifacts.
- A failed transcription, model call, or worker must never invalidate a successful capture.
- Deletion and purge require an explicit user action and an impact report.
- Raw media never belongs in Git.

## 5. Epistemic separation

Keep these distinct:

- what happened;
- what Jonathan said;
- what a transcript says;
- what a model observed;
- what a model inferred;
- what Jonathan later accepted;
- what an intervention may have caused.

Model outputs are derived, revisable, and untrusted by default.

Do not write identity-level conclusions such as “Jonathan is…” from sparse episodes. Use bounded language:

> “Across these three episodes, Solid currently estimates…”

Every inference must carry evidence, time, scope, processor version, and uncertainty.

## 6. Observation and intervention

An observation generated before Liquid acts must not be silently mixed with behavior produced after Liquid’s intervention.

Log:

- decision point;
- context available;
- intervention candidates;
- option selected;
- whether no intervention was chosen;
- user response;
- subsequent evidence.

This separation is required to detect **S3 Contamination**: the system changing behavior and then misclassifying that change as independent evidence about the user.

## 7. Cost rule

Default recurring external API cost is **zero**.

Permitted early processing paths:

- local deterministic processing;
- local speech-to-text;
- local models;
- human-mediated use of existing subscription products;
- explicit, one-off paid experiments approved by Jonathan.

Do not introduce a paid dependency, hosted database, mandatory account, or metered API without a written decision.

## 8. User experience rule

Remove operational friction; preserve productive cognitive friction.

Operational friction includes setup, file management, forms, configuration, and remembering workflows.

Productive cognitive friction includes explaining, predicting, comparing, challenging, specifying, and reflecting when Jonathan is receptive.

Never add:

- streaks;
- guilt notifications;
- productivity scores;
- mandatory daily check-ins;
- a growing “reflection debt” badge;
- automatic optimization of leisure.

The system must be able to conclude:

> “Nothing needs improvement here. Enjoy it.”

## 9. Development method

For each feature:

1. frame the question;
2. identify the simplest baseline;
3. create a synthetic or historical fixture;
4. implement the smallest vertical slice;
5. test capture failure, processing failure, retry, and replay;
6. use it in a real episode when safe;
7. record the result;
8. keep, revise, defer, or remove.

Automated tests demonstrate technical behavior. They do not pass a human-value gate.

## 10. Agentic development

Parallelize:

- research;
- read-only inspection;
- test generation;
- independent critique;
- fixture creation.

Serialize:

- architectural commitments;
- live data migrations;
- integration into the canonical branch;
- changes to experiment rules.

Use branches or worktrees for isolated experiments. Do not let multiple agents concurrently rewrite the same subsystem without explicit ownership.

## 11. Required evidence envelope

Every substantial agent result should include:

```markdown
## Result
What changed or was learned?

## Evidence
Tests, fixture results, screenshots, recordings, citations, or observed use.

## Changed state
Files, schema, data, configuration, or external systems touched.

## Assumptions
What was treated as true?

## Risks and uncertainty
What remains unresolved?

## Human decision required
What specifically requires Jonathan?

## Suggested next action
One bounded action.
```

## 12. Documentation propagation

A meaningful change must update the relevant:

- architecture document;
- experiment record;
- decision/open-question register;
- agent rules when policy changes;
- migration notes when data structures change.

Do not create documentation volume merely to appear rigorous. Preserve only decisions, evidence, and context that future work needs.

## 13. Stop conditions

Stop rather than expanding when:

- the feature is not tied to an active experiment;
- its value depends on several untested assumptions;
- the user cannot inspect why it acted;
- it introduces mandatory cost;
- it risks raw-data loss;
- it makes joy or ordinary use feel like a performance review;
- the requested capability belongs beyond the current gate.

## 14. Final authority

Jonathan is **Big Boss**: the living original.

No model, policy, historical statement, or inferred value outranks his current ability to inspect, contest, reinterpret, suspend, or retire the system.


---

## Source: `docs/00_PROJECT_CHARTER.md`

# Project Charter

> *"Building the future and keeping the past alive are one and the same thing."*
> — **Solid Snake**, *Metal Gear Solid 2: Sons of Liberty*

## 1. Mission

Les Enfants Terribles is a personal research instrument and cognitive environment for learning how artificial systems can complement one person across work, learning, creativity, leisure, skilled practice, and reflection.

The project will preserve high-value episodes, create carefully chosen metacognitive interventions, build inspectable longitudinal models, and test whether those models produce useful novelty without eroding joy or autonomy.

## 2. Core research question

> Can an AI learn when and how to augment this particular human’s cognition?

This decomposes into several questions:

1. What evidence about a human is worth capturing?
2. What cognitive mode is the human currently in?
3. What support—if any—is appropriate in that mode?
4. Which interventions improve understanding, learning, calibration, or experience?
5. Which interventions create fatigue, self-consciousness, dependence, or loss of joy?
6. Can a model improve longitudinally without turning its prior interpretation into identity or fate?
7. Can the system remain useful when models, providers, and interfaces change?

## 3. Working thesis

A useful cognitive twin will not emerge from feeding a language model an undifferentiated lifetime archive.

It requires:

- preserved source evidence;
- meaningful episode boundaries;
- explicit context;
- separate observation and intervention;
- versioned and replayable processing;
- evidence-linked uncertainty;
- user correction and ratification;
- context-sensitive assistance;
- the valid option of silence.

## 4. Primary user

The first user is Jonathan.

Relevant traits for the initial design:

- Windows desktop is the primary capture environment.
- Voice interaction is welcome and does not count as meaningful friction.
- Operational setup and clerical maintenance do count as friction.
- Raw media should be retained.
- Cloud AI processing is acceptable; recurring cost is the stronger constraint.
- Existing subscription products may be used through a human-mediated bridge.
- The first-use domains are movies, piano, Call of Duty, research/spontaneous thought, and programming.
- Professional episodes are permitted, but professional canonical data remains separately governed.
- The strongest desired outcome is metacognitive novelty without loss of enjoyment.

## 5. Initial product proposition

LET should let Jonathan:

1. open a local browser application;
2. press Record;
3. speak naturally;
4. stop and know the raw recording is safe;
5. receive a transcript later;
6. optionally choose how he wants to think:
   - just capture;
   - explore;
   - challenge;
   - understand;
   - improve;
   - surprise me;
   - let Liquid decide;
7. answer follow-up questions by voice;
8. revisit the complete episode and its derivation history;
9. replay the episode through future processors.

## 6. Parallel cores

### Capture

Capture preserves an experience without forcing immediate interpretation.

Early modalities:

- voice;
- text;
- uploaded audio/video;
- manual markers;
- imported artifacts.

### Liquid

Liquid creates carefully chosen perturbations:

- specificity;
- mechanism;
- evidence;
- alternative explanations;
- prediction;
- calibration;
- transfer;
- pattern recognition;
- creative provocation;
- silence.

Liquid is useful before a mature twin exists. Its questions and Jonathan’s responses also generate evidence for later models.

## 7. Initial scope

### In scope

- desktop browser capture;
- raw media preservation;
- episode creation;
- local transcription;
- text and media attachment;
- optional cognitive mode selection;
- manual or model-assisted Liquid questions;
- voice responses;
- processor versioning;
- replay;
- lightweight feedback;
- a manual bridge to subscription AI tools;
- backup and restoration.

### Later, if earned

- Solid state estimation;
- intervention selection learned from history;
- Solidus and ratified value models;
- passive computer sensors;
- screen capture;
- Plex events;
- ActivityWatch;
- gameplay/piano analysis;
- phone capture;
- wearables;
- micro-randomized intervention experiments;
- bounded action.

### Explicitly out of initial scope

- continuous life recording;
- an autonomous personal proxy;
- fine-tuning a model on personal data;
- a universal ontology of the self;
- a public SaaS product;
- a social network;
- a productivity scoring system;
- automatic psychological diagnosis;
- medical, legal, or employment decision authority.

## 8. Two-week success condition

The first field period succeeds when several of these occur:

- LET preserves something Jonathan would otherwise have lost.
- Liquid causes at least one meaningful “I had not noticed that” moment.
- A question produces a more specific, surprising, or revised interpretation.
- A self-prediction differs usefully from later evidence.
- The system supports deeper engagement without making the activity feel like work.
- Jonathan naturally wants to use it again.
- Capture and recovery feel trustworthy.
- A failed or unnecessary feature is confidently removed.

Counts of recordings, model calls, tokens, or features are not primary success metrics.

## 9. Anti-goals

LET must not:

- equate more data with more understanding;
- convert leisure into mandatory improvement;
- make the twin an authority on identity;
- rewrite raw experience into a clean retrospective story;
- hide evidence that conflicts with its model;
- create notifications merely because it can;
- make reflection feel like debt;
- require ongoing API expenditure;
- lock the archive to one model or vendor;
- claim that a user change was independently predicted when the system helped cause it.

## 10. Operating principles

1. **Capture first, interpret later.**
2. **Raw evidence is more durable than derived meaning.**
3. **The archive is the genome, not the person.**
4. **Intentional capture precedes passive surveillance.**
5. **Use natural episode boundaries.**
6. **Remove operational friction; preserve productive cognitive friction.**
7. **Ask the highest-value question, not the largest number of questions.**
8. **Silence is a valid intervention.**
9. **Observation and intervention remain distinguishable.**
10. **Every processor is versioned and replayable.**
11. **Higher-level identity inference requires stronger evidence and human ratification.**
12. **A simpler baseline must be included before complexity is earned.**
13. **Real use can rewrite the plan.**
14. **Joy is an outcome, not an obstacle.**
15. **Failure should still leave a useful private multimodal journal.**

## 11. Relationship to professional work

LET may capture reflections about professional work, cognitive state, agent delegation, uncertainty, and resumption.

It should not silently copy confidential professional source material into a personal archive.

The PREP-KC `modeling` repository remains the authoritative model of that external professional domain. A future bridge may exchange bounded summaries or references, but the first field period keeps the systems distinct.

## 12. Governance posture

LET is not neutral simply because it is personal.

A system that represents a person can influence how that person understands and performs the self. Therefore Jonathan retains:

- inspection;
- contestation;
- correction;
- suppression;
- deletion;
- replay;
- export;
- provider choice;
- intervention control;
- model retirement.

## 13. North-star sentence

> Build a shadow that helps the living original see more clearly—without allowing the shadow to become the script.


---

## Source: `docs/01_METAL_GEAR_COGNITIVE_MODEL.md`

# Metal Gear Cognitive Model

> *"You mustn't allow yourself to be chained to fate, to be ruled by your genes. Humans can choose the kind of life they want to live."*
> — **Solid Snake**, *Metal Gear Solid*

## 1. Why the metaphor belongs in the architecture

Metal Gear repeatedly asks what persists when a person is reconstructed through genes, transmitted ideas, historical context, memory, artificial intelligence, role performance, and legacy.

LET asks a related design question:

> If we preserve a person’s experiences, expressions, patterns, decisions, contexts, and values, what kind of artificial shadow begins to emerge—and where does that shadow stop being the person?

The framing is not decorative. It supplies:

- a memorable layered model;
- distinct clone roles;
- warnings about inherited identity;
- names for failure modes;
- a philosophical limit on model authority.

This document intentionally adapts the themes rather than claiming every software role is a literal mapping of game canon.

## 2. The living original

### Big Boss

**Big Boss is Jonathan, the living original.**

The system contains evidence, representations, and simulations. It does not contain the living person.

Big Boss retains:

- current perspective;
- embodied experience;
- authority to reinterpret the past;
- authority to reject the twin;
- the ability to change without requesting model permission.

## 3. The four inheritance layers

Konami’s own retrospective describes the series through **GENE, MEME, and SCENE**, with later material associated with **SENSE**. LET uses these as a layered cognitive model.

### GENE — durable substrate

In LET:

- raw audio;
- raw video;
- original text;
- timestamps;
- source identity;
- content hashes;
- stable artifact relationships.

GENE is what can be copied most faithfully.

> **The archive is the genome, not the person.**

### MEME — transmitted content

In LET:

- transcript;
- expressed idea;
- review;
- explanation;
- procedure;
- belief;
- argument;
- learned pattern;
- generated synthesis.

MEME is what can be passed forward, recombined, challenged, and misunderstood.

### SCENE — context

In LET:

- activity;
- purpose;
- cognitive mode;
- timing;
- environment;
- preceding events;
- skill level;
- receptivity;
- fatigue;
- social or professional setting;
- whether Liquid has already intervened.

A statement about Jonathan without its Scene is often misleading.

```text
Jonathan likes challenge
```

is weaker than:

```text
After finishing a research session,
while explicitly requesting pushback,
Jonathan preferred aggressive challenge.
```

### SENSE — lived meaning

In LET:

- what the experience felt like;
- affect;
- embodied quality;
- personal significance;
- authentic voice;
- ambiguity;
- meaning that resists formalization.

SENSE is the layer LET should treat with the greatest humility. Audio may preserve cadence and affect better than a transcript, but neither recreates the original experience.

## 4. Mother Base

**Mother Base** is the local LET environment:

- browser application;
- archive;
- job worker;
- episode store;
- processor registry;
- experiment instruments;
- backups;
- review interfaces.

Mother Base is infrastructure, not the twin.

## 5. Mammal Pod

**Mammal Pod** is the evolving evidence-backed cognitive model shared by the clone perspectives.

It contains:

- episode history;
- current state estimates;
- uncertainty;
- evidence links;
- model versions;
- intervention history;
- accepted corrections;
- unresolved conflicts;
- ratified commitments.

It should never collapse into one opaque embedding that claims to represent Jonathan.

## 6. Codec

**Codec** is the interaction layer:

- one-button recording;
- voice questions;
- text conversation;
- mode selection;
- episode debrief;
- explanation of why a prompt surfaced;
- correction and feedback.

Codec is where assistance must remain legible and interruptible.

## 7. The clones

### Solid — descriptive mirror

Solid asks:

> What does the available evidence suggest Jonathan currently thinks, notices, does, expects, or prefers?

Solid is:

- conservative;
- evidence-linked;
- scope-bounded;
- uncertain;
- descriptive rather than prescriptive.

Solid must resist genetic determinism. Historical patterns do not dictate future identity.

Preferred wording:

> “Across four recent piano episodes, Solid estimates…”

Prohibited wording:

> “Jonathan is the kind of person who…”

### Liquid — cognitive perturbation

Liquid asks:

> What carefully chosen disturbance could reveal, deepen, or improve the current cognition?

Liquid can:

- request specifics;
- ask for mechanism;
- challenge an assumption;
- provide contrary evidence;
- generate alternatives;
- request a prediction;
- compare self-perception with observed evidence;
- create a creative tangent;
- choose silence.

Liquid is not a permanent Devil’s advocate. It is **liquid**: its stance changes with Scene and user receptivity.

### Solidus — constitutional or committed self

Solidus asks:

> Given Jonathan’s explicitly ratified goals, values, and protected commitments, what deserves attention or protection?

Solidus is not “perfect Jonathan.” It is a policy perspective constrained by:

- exact source language;
- date and context;
- scope;
- current ratification;
- known conflicts;
- reconsideration triggers.

Solidus belongs beyond the initial field period.

## 8. System map

```text
                         BIG BOSS
                    living Jonathan
                          │
                          ▼
                       EXPERIENCE
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
          GENE/MEME                SCENE/SENSE
        evidence/content          context/meaning
             │                         │
             └────────────┬────────────┘
                          ▼
                    ┌────────────┐
                    │ MAMMAL POD │
                    │ evidence   │
                    │ state      │
                    │ conflicts  │
                    │ uncertainty│
                    └─────┬──────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
          SOLID         LIQUID        SOLIDUS
          mirror       perturb       commitments
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                        CODEC
                          │
                          ▼
                      BIG BOSS
```

## 9. Named failure modes

### Patriots Problem — hidden editorial control

The system quietly curates what Jonathan sees until it shapes the informational environment from which future cognition is constructed.

Controls:

- inspectable suppression;
- reversible filters;
- “what did you not show me?”;
- source diversity;
- raw archive access;
- no invisible ranking as authority.

### S3 Contamination — intervention mistaken for observation

Liquid changes Jonathan’s behavior. Solid later treats the changed behavior as independent proof of a pre-existing trait.

Controls:

- observation/intervention separation;
- intervention timestamps;
- pre-intervention baselines;
- no-intervention comparisons;
- causal humility.

### Venom Problem — the original performs the model

The twin’s descriptions become persuasive scripts. Jonathan begins enacting the model, and the model treats the enactment as validation.

Controls:

- tentative language;
- counter-models;
- identity-level inference gates;
- regular “does this still fit?” review;
- explicit right to reject the model.

### Phantom Memory — reconstruction becomes history

A transcript error, generated summary, or plausible inference later appears as something that actually happened.

Controls:

- immutable raw evidence;
- derivation chains;
- source labels;
- quoted transcript spans;
- uncertainty;
- no silent promotion.

### The Boss’s Will Problem — values become doctrine

A contextual human aspiration becomes a timeless rule interpreted by the system.

Controls:

- preserve exact wording;
- preserve date and Scene;
- require ratification;
- include scope and exceptions;
- expiration/review;
- never let Solidus outrank Big Boss.

### Les Enfants Determinism — inheritance becomes fate

The clone treats repeated behavior, preferences, or skills as fixed identity.

Controls:

- time-bounded claims;
- alternatives;
- change detection;
- historical perspectives;
- language that separates tendency from essence.

## 10. Confidence gradient

The farther a claim moves from source evidence toward identity, the greater the required evidence and human authority.

```text
raw audio                         strongest source evidence
literal transcript                derived, correctable
episode-level observation         bounded inference
cross-episode pattern             stronger inference
cognitive routine                 longitudinal hypothesis
metacognitive tendency            high-risk abstraction
value or identity claim           requires explicit ratification
```

## 11. The philosophical boundary

LET is successful when the shadow helps Jonathan notice, remember, compare, and choose.

LET fails when it becomes the hidden author of what Jonathan is allowed to notice, how he is expected to behave, or who he believes himself to be.

## 12. Metal Gear source notes

The project framing draws on official Konami retrospective and timeline material:

- Konami’s 25th-anniversary retrospective describes the saga through **GENE**, **MEME**, and **SCENE**:
  https://www.konami.com/mg/archive/mg25th/truth/
- Konami’s series timeline describes the Peace Walker AI as based on the psychology of The Boss:
  https://eu-support.konami.com/hc/en-gb/articles/9822379926423-Backstory-What-is-the-timeline-of-the-events-that-precede-Metal-Gear-Solid-V-Ground-Zeroes-and-Metal-Gear-Solid-V-The-Phantom-Pain
- Peace Walker official archive:
  https://www.konami.com/mg/archive/mgs_pw/us/

The software roles and failure-mode names are LET’s design interpretations, not claims that the game canon defines these technical concepts.

*Metal Gear, its characters, and related names are the property of their respective rights holders. LET uses the references as an internal thematic and conceptual framework.*


---

## Source: `docs/02_PRODUCT_EXPERIENCE_AND_USER_FLOWS.md`

# Product Experience and User Flows

> *"Life isn't just about passing on your genes. We can leave behind much more than just DNA. Through speech, music, literature and movies... what we've seen, heard, felt... anger, joy and sorrow... these are the things I will pass on. That's what I live for."*
> — **Solid Snake**, *Metal Gear Solid 2: Sons of Liberty*

## 1. Experience goal

LET should feel like an available cognitive instrument, not an obligation.

The basic interaction should be:

```text
open → record → stop → raw saved
```

Everything after that is optional:

```text
transcribe → debrief → challenge → answer → revisit → replay
```

## 2. Friction model

### Operational friction to remove

- finding the right file;
- creating a note;
- naming and moving media;
- filling metadata;
- remembering a workflow;
- configuring models;
- waiting for transcription;
- manually reconstructing provenance;
- copying the same context repeatedly.

### Productive cognitive friction to preserve

- specifying what was vague;
- explaining mechanism;
- comparing interpretations;
- predicting before feedback;
- noticing uncertainty;
- challenging assumptions;
- transferring learning;
- making meaning.

For Jonathan, thinking is often the reward. Clerical setup is the friction.

## 3. Cognitive support modes

At capture or debrief, Jonathan may choose:

| Mode | System behavior |
|---|---|
| **Just capture** | Preserve the episode; no questioning |
| **Help me explore** | Curious, expansive, association-friendly questions |
| **Challenge me** | Counterexamples, assumptions, alternatives, evidence |
| **Help me understand** | Mechanism, definitions, causal structure |
| **Help me improve** | Diagnosis, strategy, prediction, transfer |
| **Surprise me** | High-variance but evidence-aware provocation |
| **You decide** | Liquid selects a stance and explains why |

The initial system should let Jonathan choose explicitly. Later Solid may predict the likely mode, but explicit choice remains available.

## 4. Timing model

### Before

Useful for:

- intention;
- prediction;
- goal;
- anticipated difficulty;
- confidence;
- what would count as success.

### During

Default behavior is silence.

Permitted during-flow interactions should be:

- explicitly requested;
- extremely short;
- marker-only;
- safe at a natural breakpoint.

### After

Useful for:

- immediate reflection;
- reconstruction;
- self-evaluation;
- evidence comparison;
- Liquid questioning;
- revision;
- next experiment.

### Offline

Useful for:

- transcription;
- clustering;
- replay;
- contradiction detection;
- candidate questions;
- cross-episode patterns.

Offline processing does not make canonical identity claims.

## 5. Core screens

These are conceptual surfaces, not mandatory v1 pages.

### Mother Base

- one prominent Capture button;
- recent episodes;
- processing status;
- current experiments;
- no guilt indicators.

### Codec

- record/stop;
- waveform/timer;
- optional domain and mode;
- voice or text follow-up;
- clear “raw saved” state.

### Mission Log

- chronological episode timeline;
- filters by domain;
- raw and derived artifacts;
- interventions and responses;
- replay history.

### Debrief

- self-prediction first when relevant;
- one or more candidate Liquid questions;
- “ask,” “later,” “ignore,” “push harder”;
- evidence and rationale.

### Mammal Pod

Later:

- current model;
- confidence;
- evidence;
- conflicting evidence;
- changes over time;
- user corrections.

## 6. Movie flow

### Immediate flow

1. Movie ends.
2. Open LET.
3. Press Record.
4. Speak freely.
5. Stop.
6. Raw audio is saved immediately.
7. Transcript appears later.
8. Choose:
   - done;
   - explore;
   - challenge;
   - help me write;
   - surprise me.

### Liquid examples

If Jonathan says:

> “The back half really worked, and several scenes stood out.”

Liquid might ask:

- Which scene is most present in your mind right now?
- What specifically changed in the back half?
- Was the effect visual, narrative, performative, musical, or something else?
- What evidence in the film supports your interpretation?
- Did the ending work because of what it resolved or because of what it left unresolved?
- What might someone who disliked the same scene be responding to?

### Writing branch

A strong episode may become:

```text
raw reaction
    ↓
follow-up reflection
    ↓
argument or theme
    ↓
outline
    ↓
draft
```

The polished piece remains derived from, not a replacement for, the original reaction.

## 7. Piano flow

### Practice

Before:

- What are you practicing?
- What do you expect to be difficult?
- How will you know if it improved?

During:

- silence;
- optional MARK hotkey;
- optional audio/video recording.

After, before analysis:

- What do you think happened?
- What improved?
- Where did attention go?
- Confidence?

Then compare with recording or other evidence.

### Performance

The default instruction is:

> Play the piece.

Metacognitive analysis belongs before or after, not inside fluent performance unless explicitly requested.

### Liquid examples

- You expected the transition to fail, but the recording suggests tempo drift appeared later. What were you monitoring?
- You repeated the passage six times without changing strategy. Was that deliberate?
- What would transfer from this practice to a different piece?
- Do you want improvement here, or do you want to enjoy playing it?

## 8. Call of Duty flow

### Play mode

Goal: have fun.

- Liquid remains silent.
- Passive observation is optional and not required.
- No performance score is generated.

### Lab mode

Jonathan may declare a question:

- Do I re-challenge too often?
- Am I using the same weapons because they fit me or because I avoid learning?
- Do I rotate late?
- Does frustration change decision quality?
- What is my self-assessment accuracy?

During play:

- optional MARK between safe moments;
- no unsolicited coaching.

After a match or session:

- quick self-evaluation;
- optional clip review;
- one high-value Liquid question.

### Liquid examples

- You described aim as the main problem. The marked clips may also show repeated disadvantaged re-peeks. Which explanation fits better?
- You used the same loadout across all matches. Was that a preference, a habit, or avoidance?
- Did your goal tonight shift from enjoyment to proving something after the losing streak?
- Nothing here needs optimizing. Did you enjoy the session?

## 9. Research and spontaneous thought flow

1. Press Record.
2. State the idea without forcing structure.
3. Optional transcript.
4. Liquid identifies:
   - ambiguous terms;
   - assumptions;
   - missing evidence;
   - alternative mechanisms;
   - adjacent domains;
   - predictions;
   - what would falsify the idea.
5. Jonathan answers by voice or chooses no follow-up.
6. A later processor may convert the episode into a research note.

Liquid may be more aggressive in this domain when requested.

## 10. Programming flow

LET is not the professional project-management system.

It may help Jonathan notice:

- what problem he is actually solving;
- why he delegated to an agent;
- what he believes before an agent responds;
- where review effort accumulates;
- which tasks teach versus merely complete;
- when a model response changes his architecture;
- whether he is waiting, exploring, reviewing, or integrating.

Natural episode boundaries include:

- before starting a feature;
- after dispatching agents;
- when stuck;
- before switching projects;
- after reviewing a result;
- after a merge or failure.

## 11. Liquid intervention vocabulary

| Type | Purpose | Example |
|---|---|---|
| **Specify** | Replace vague reference with an object | “Which scene?” |
| **Mechanism** | Explain how or why | “What made it work?” |
| **Evidence** | Ground interpretation | “What in the film supports that?” |
| **Alternative** | Generate competing explanations | “What else could explain it?” |
| **Counterexample** | Test boundaries | “When does that not hold?” |
| **Prediction** | Preserve pre-feedback belief | “What do you expect next?” |
| **Calibration** | Compare confidence and evidence | “How sure are you?” |
| **Pattern** | Surface recurrence | “This happened three times. Intentional?” |
| **Transfer** | Apply learning elsewhere | “What changes next time?” |
| **Values** | Test alignment without doctrine | “Do you actually want to improve this?” |
| **Creative provocation** | Open a new path | “What would this become as an essay?” |
| **Silence** | Protect flow or joy | No question |

## 12. Question selection

Liquid should rank candidate questions by:

```text
expected cognitive value
× novelty
× relevance to declared mode
× likelihood Jonathan is receptive
÷ interruption and interaction cost
```

This is a design heuristic, not a claim of precise measurement.

The interface should support:

- ask me;
- later;
- ignore;
- different question;
- push harder;
- stop here.

## 13. Joy protection

LET must not assume improvement is always desired.

A valid debrief may conclude:

- the activity was enjoyable;
- no analysis is needed;
- deliberate practice would reduce enjoyment;
- the best intervention is more play;
- the interesting pattern concerns joy rather than skill.

The system should help Jonathan understand flourishing, not only output.


---

## Source: `docs/03_TECHNICAL_ARCHITECTURE.md`

# Technical Architecture

## 1. Architecture objective

Build a local-first, desktop-first experimental substrate that preserves raw episodes, supports replaceable processors, and makes new hypotheses cheap to test.

The architecture should remain useful even if:

- no generative model is available;
- a transcription engine changes;
- subscription workflows remain manual;
- the twin concept fails;
- the user stops active experimentation.

## 2. Current stack decision

### Locked for the first field period

- **Platform:** Windows desktop.
- **Application:** local browser application.
- **Backend:** Python + Flask.
- **Frontend:** Jinja templates + HTMX; Alpine.js only where local state is helpful.
- **Capture:** browser `getUserMedia()` + `MediaRecorder`.
- **Metadata:** SQLite.
- **Search:** SQLite FTS5 for transcripts and text.
- **Raw media:** filesystem, outside Git.
- **Derived media/text:** filesystem plus SQLite metadata.
- **Processing:** asynchronous local worker.
- **Speech-to-text:** replaceable transcriber interface; local `faster-whisper` is the provisional default.
- **Media normalization:** FFmpeg or PyAV behind a small adapter.
- **Version control:** Git for code, schemas, prompts, fixtures, and planning—not raw media.
- **Recurring external API cost:** zero by default.

### Provisional

- SQLAlchemy 2 for persistence.
- Pydantic or JSON Schema for processor and event contracts.
- A database-backed job queue rather than Redis/Celery.
- A CLI entry point such as `let`.
- Localhost-only networking for the first field period.

### Deferred

- mobile-native application;
- multi-device sync;
- cloud backend;
- graph database;
- vector database;
- fine-tuning;
- continuous screen capture;
- wearable ingestion;
- multi-user collaboration.

## 3. High-level system

```text
BROWSER / IMPORT / SENSOR
          │
          ▼
    CAPTURE SERVICE
          │
          ├── save raw artifact atomically
          ├── compute hash
          ├── create event
          └── attach/create episode
          │
          ▼
      LOCAL STORE
   files + SQLite metadata
          │
          ▼
      JOB QUEUE
          │
    ┌─────┼─────────────┐
    ▼     ▼             ▼
normalize transcribe  processors
    │     │             │
    └─────┼─────────────┘
          ▼
   DERIVED ARTIFACTS
          │
          ▼
      REPLAY ENGINE
          │
    ┌─────┼───────────────┐
    ▼     ▼               ▼
  local manual bridge  future API
  model  subscription   provider
          │
          ▼
      DEBRIEF / FEEDBACK
```

## 4. Core components

### Capture service

Responsibilities:

- request browser microphone access;
- record audio;
- receive uploads;
- accept text;
- accept MARK events;
- save raw bytes before any processor runs;
- generate stable IDs;
- return an unambiguous success state.

Invariant:

> If Stop reports success, the raw artifact exists durably and can be recovered independently of all downstream processing.

### Episode service

Responsibilities:

- create and update meaningful episode containers;
- attach multiple artifacts and events;
- preserve natural boundaries;
- allow later merge/split without changing raw artifact identity;
- store domain and declared cognitive mode.

### Artifact store

Responsibilities:

- filesystem path management;
- content hashes;
- MIME/type metadata;
- immutable raw namespace;
- derived namespace;
- export and backup manifests.

Suggested local layout:

```text
LET_DATA/
├── let.sqlite
├── raw/
│   ├── audio/
│   ├── video/
│   ├── image/
│   └── text/
├── derived/
│   ├── normalized/
│   ├── transcripts/
│   ├── thumbnails/
│   ├── analyses/
│   └── exports/
├── backups/
└── temp/
```

### Job worker

Responsibilities:

- claim queued work;
- record processor/version/configuration;
- retry safely;
- avoid duplicate outputs;
- expose failure without blocking capture;
- support replay.

The initial queue can be a SQLite table with leases and statuses:

```text
queued → running → succeeded
                 ↘ failed → retry/dead
```

Do not introduce Redis or Celery before local concurrency requires them.

### Processor registry

A processor is any versioned transformation:

- audio normalization;
- transcription;
- transcript cleanup;
- episode segmentation;
- Liquid candidate generation;
- manual external model result;
- Solid state estimate;
- evidence comparison.

Initial implementation may use ordinary Python classes registered in code. A dynamic plug-in marketplace is unnecessary.

Conceptual interface:

```python
class Processor:
    name: str
    version: str

    def supports(self, inputs) -> bool: ...
    def run(self, context) -> list[DerivedArtifact]: ...
```

### Replay engine

Replay is a core multiplier.

It should be possible to:

- select an existing episode;
- choose a processor and version;
- run it again;
- preserve prior output;
- compare results;
- mark one result as preferred without erasing others.

### Manual AI bridge

Because subscription access is abundant and API spending is undesirable, human-mediated processing is a first-class path.

#### Export

Generate a bounded **Mission Brief** containing:

- episode purpose and domain;
- selected transcript/media references;
- declared cognitive mode (*Explore, Challenge, Understand, Improve, Surprise, Decide*);
- requested dual output specifications:
  1. **Polished Synthesis / Review Note:** clean, structured restructuring of spoken thoughts in authentic voice;
  2. **Liquid Perturbations:** 1–2 high-leverage questions or challenges;
- provenance and content hashes;
- exact return markdown schema.

Copy it to clipboard with one click or save Markdown/JSON.

#### External run

Jonathan uses Antigravity, ChatGPT, Claude, Gemini, or another subscribed interface.

#### Import

Paste the response back into LET.

LET records:

- provider/model if known;
- prompt packet hash;
- derived analysis artifact with SHA-256 hash;
- link to source transcript (`source_artifact_id`);
- time and parser version;
- rendered Polished Summary with 1-click copy and prominent Liquid Question card.

Manual transport does not weaken provenance if it is recorded explicitly.

### Feedback and experiment service

Store:

- whether an intervention was shown;
- the selected stance;
- user response;
- right/wrong/partly;
- useful/irrelevant/intrusive;
- novelty;
- joy effect;
- follow-up action;
- experiment condition.

## 5. Browser recording

The browser MediaStream Recording API is sufficient for the first capture experience.

Design requirements:

- large record/stop control;
- timer;
- visible microphone status;
- browser-supported MIME negotiation;
- safe cancellation;
- chunk handling for longer recordings if necessary;
- confirmation only after server persistence;
- local playback.

The application should not require real-time transcription.

## 6. Transcription

Use a provider interface:

```text
Transcriber
├── FasterWhisperTranscriber
├── WhisperCppTranscriber
├── CloudTranscriber
└── ManualTranscriptImporter
```

Initial decision:

- local transcription;
- timestamps;
- preserve raw unedited transcript;
- optional human-corrected transcript as another version;
- never overwrite.

Do not analyze acoustic features as psychological truth. Voice-prosody analysis is experimental and requires separate validation.

## 7. SQLite use

SQLite stores:

- episodes;
- artifacts;
- events;
- derivations;
- jobs;
- transcript segments;
- processor runs;
- interventions;
- feedback;
- experiments;
- model snapshots.

Use:

- WAL mode if concurrent browser/worker access requires it;
- foreign keys;
- transactions;
- schema versioning;
- FTS5 for searchable text;
- integrity checks.

Binaries remain on disk unless a later experiment demonstrates a compelling reason to use BLOBs.

## 8. Reliability invariants

1. Raw save precedes processing.
2. Raw artifacts are immutable.
3. Every artifact has a content hash.
4. Derived artifacts declare processor version and source.
5. Jobs are idempotent or produce distinct versioned results.
6. Retries never duplicate canonical identity.
7. A database rebuild does not alter event times.
8. Backup manifests can be verified.
9. Restore is rehearsed.
10. Temporary files are never mistaken for durable capture.
11. External model outputs are imports, not facts.
12. No recurring paid call happens without an explicit policy.

## 9. Sensor adapter model

Future sources should enter as adapters, not core rewrites.

Conceptual event API:

```python
let.observe(...)
let.capture(...)
let.mark(...)
let.attach(...)
```

Candidate sensors:

- Git;
- Plex webhooks;
- ActivityWatch;
- screenpipe;
- Omi;
- MIDI;
- game recordings;
- browser extensions;
- phone capture.

Rule:

> A hypothesis pulls in a sensor. A sensor does not invent its own justification.

Example:

- Question: “Do interruptions change programming review quality?”
- Sensor candidate: ActivityWatch window/AFK events.
- Only then integrate.

## 10. Fast experimental path

The fastest useful system is:

```text
browser audio capture
        ↓
raw file + SQLite episode
        ↓
local transcription
        ↓
Mission Brief export
        ↓
subscription model via Antigravity
        ↓
response import
        ↓
voice follow-up
```

This path can test sophisticated Liquid ideas before provider APIs, passive sensors, or autonomous agents exist.

## 11. Suggested repository shape

```text
les-enfants-terribles/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── .gitignore
├── docs/
├── schemas/
├── templates/
├── src/
│   └── let/
│       ├── capture/
│       ├── episodes/
│       ├── artifacts/
│       ├── jobs/
│       ├── processors/
│       ├── replay/
│       ├── feedback/
│       ├── experiments/
│       ├── web/
│       └── cli.py
├── tests/
│   ├── fixtures/
│   └── synthetic_corpus/
└── instance/
    └── local configuration only
```

The actual data root should be separately configured and ignored.

## 12. Developer multipliers to build early

These are more valuable than early feature breadth:

- stable capture/artifact API;
- episode abstraction;
- processor interface;
- replay;
- derivation/provenance;
- durable job queue;
- synthetic corpus;
- manual AI bridge;
- feedback primitive;
- doctor;
- backup/restore;
- export.

## 13. What not to decide yet

- final database schema;
- final transcript model;
- final UI design;
- embeddings;
- graph representation;
- learned intervention policy;
- clone ontology;
- long-term storage provider;
- passive capture platform;
- phone implementation.

The first-use evidence should shape these decisions.


---

## Source: `docs/04_DATA_AND_EPISTEMIC_MODEL.md`

# Data and Epistemic Model

> *"There is no such thing as an absolute timeless enemy. Our enemies are always relative, depending on the times and the politics."*
> — **The Boss**, *Metal Gear Solid 3: Snake Eater*

## 1. Design objective

LET must preserve the difference between:

- experience;
- record;
- transcription;
- interpretation;
- inference;
- accepted belief;
- intervention;
- behavior produced after intervention.

The system should make it easier to be wrong safely.

## 2. Episode as the central unit

An **Episode** is a bounded slice of lived experience that can contain multiple modalities and stages.

Examples:

```text
Movie: Alien
├── Plex playback event
├── immediate voice reaction
├── transcript
├── Liquid question
├── voice follow-up
├── later review
└── changed interpretation
```

```text
Piano practice
├── pre-practice prediction
├── audio/video recording
├── MARK events
├── post-practice self-assessment
├── objective comparison
└── next-practice decision
```

Episodes are human-meaningful containers. Raw artifact identity does not depend on episode organization.

## 3. Core entities

### Episode

Suggested fields:

```yaml
id:
title:
domain:
started_at:
ended_at:
created_at:
status:
declared_mode:
activity:
purpose:
notes:
```

### Event

A timestamped occurrence:

```yaml
id:
event_type:
occurred_at:
recorded_at:
source:
episode_id:
payload:
```

Examples:

- capture.started;
- capture.completed;
- marker.created;
- movie.scrobbled;
- processor.started;
- intervention.shown;
- feedback.recorded.

### Artifact

A file or text object:

```yaml
id:
artifact_kind:
raw_or_derived:
mime_type:
path:
sha256:
created_at:
occurred_at:
source:
episode_id:
retention_class:
```

### Processor run

```yaml
id:
processor_name:
processor_version:
configuration:
started_at:
completed_at:
status:
input_artifact_ids:
output_artifact_ids:
prompt_hash:
model_provider:
model_name:
```

### Derivation

```yaml
source_artifact_id:
derived_artifact_id:
activity:
processor_run_id:
source_span:
created_at:
```

### Transcript segment

```yaml
artifact_id:
segment_index:
start_seconds:
end_seconds:
text:
speaker:
confidence:
```

### Reflection

Human-authored meaning:

```yaml
id:
episode_id:
phase: spontaneous | prompted | later
modality:
content_artifact_id:
prompt_id:
created_at:
```

### Observation

A bounded description:

```yaml
claim:
observer:
scope:
evidence:
confidence:
time:
```

Example:

> In three marked COD clips, Jonathan re-entered the same lane within ten seconds after death.

### Interpretation

Meaning assigned to observations:

> The re-entry may reflect impatience after death.

This is not equivalent to the observation.

### Hypothesis

A testable explanation:

> If the issue is frustration rather than map strategy, re-challenge frequency should increase after consecutive deaths.

### Twin snapshot

```yaml
clone: solid
estimated_mode:
state:
confidence:
evidence:
conflicting_evidence:
processor_run_id:
valid_at:
```

### Intervention candidate

```yaml
stance:
question_or_action:
rationale:
evidence:
expected_cognitive_value:
estimated_burden:
availability_requirements:
```

### Intervention

```yaml
candidate_id:
decision_point:
selected_option:
shown_at:
response_artifact_id:
dismissed:
experiment_condition:
```

### Feedback

```yaml
correctness:
usefulness:
novelty:
intrusiveness:
joy_effect:
would_use_again:
notes:
```

## 4. Epistemic classes

LET should use a compact, comprehensible set:

- **Source:** raw artifact or external record.
- **Observation:** directly described/measured pattern.
- **Interpretation:** assigned meaning.
- **Hypothesis:** testable explanation.
- **Prediction:** expected future result.
- **Decision:** user-authorized choice.
- **Commitment:** ratified ongoing intention.
- **Unknown:** materially missing.
- **Conflict:** incompatible evidence or perspectives.
- **Retraction:** item should no longer support current conclusions.
- **Historical:** true as a record of an earlier perspective.

These classes may become fields rather than visible labels in every interface.

## 5. Provenance chain

Example:

```text
audio-001.webm
   │ transcribed by faster-whisper vX
   ▼
transcript-003
   │ interpreted by Liquid prompt v2 via Claude
   ▼
interpretation-009
   │ accepted in part by Jonathan
   ▼
reflection-011
   │ contributes to Solid model v4
   ▼
snapshot-018
```

Every step remains inspectable.

## 6. Temporal model

At minimum distinguish:

- **occurred_at:** when the underlying episode/event happened;
- **recorded_at:** when LET received it;
- **created_at:** when a derived object was created;
- **valid_from / valid_to:** optional interval during which a claim applies;
- **superseded_at:** when a later item replaced its current authority.

Reprocessing must not rewrite occurred or recorded time.

## 7. Source strength and abstraction

A simple authority ladder:

```text
raw media
direct user statement
external system event
human-corrected transcript
automatic transcript
bounded observation
interpretation
cross-episode pattern
cognitive routine
identity/value inference
```

The ladder is not absolute. A raw recording can be ambiguous; a corrected transcript may be more usable. The purpose is to prevent high-level inference from masquerading as direct evidence.

## 8. GENE / MEME / SCENE / SENSE mapping

| Layer | Stored objects |
|---|---|
| **GENE** | raw artifact, stable ID, hash, event time |
| **MEME** | transcript, reflection, idea, procedure, argument |
| **SCENE** | activity, mode, purpose, environment, intervention history |
| **SENSE** | first-person meaning, affect, authentic expression, ambiguity |

## 9. Observation versus intervention

The system must be able to answer:

- What did Solid estimate before Liquid asked anything?
- What did Jonathan say before seeing evidence?
- What changed after the question?
- Was a later behavior observed in a no-intervention period?
- Is this pattern partly produced by LET?

This is a data-model requirement, not only an analysis concern.

## 10. Identity inference gate

Identity-level claims require:

1. multiple episodes;
2. temporal diversity;
3. context diversity;
4. contradictory evidence search;
5. explicit uncertainty;
6. human review;
7. limited use;
8. reconsideration date.

Example:

Poor:

> Jonathan dislikes sentimental endings.

Better:

> In three 2026 film reflections, Jonathan criticized endings he described as sentimental. In two other films, he positively described emotional closure. The current evidence supports a contextual hypothesis rather than a stable preference.

## 11. Raw and corrected transcript policy

Preserve:

- raw model transcript;
- corrected transcript;
- correction diff;
- model/version;
- timestamps.

A corrected transcript does not replace the recording.

## 12. Model-response policy

A response imported from a subscription interface should preserve:

- exported Mission Brief;
- brief hash;
- stated provider/model when known;
- raw response;
- parsed objects;
- human acceptance/rejection;
- subsequent use.

## 13. Retention

Initial policy:

- retain raw media indefinitely;
- retain all processor outputs during experimentation;
- permit later suppression from default views;
- never equate suppression with deletion;
- create backup and storage lifecycle tools before large video ingestion.

## 14. Minimal initial schema

The first implementation does not need every entity above.

Minimum:

- episodes;
- events;
- artifacts;
- processor_runs;
- derivations;
- jobs;
- interventions;
- feedback.

Add higher-order cognitive objects only after real episodes demonstrate their value.


---

## Source: `docs/05_EXPERIMENT_PROGRAM_AND_GATES.md`

# Experiment Program and Decision Gates

## 1. Purpose

The experiment program prevents fast development from hardening untested assumptions.

The governing rule is:

> Run the cheapest experiment that can change an important decision before building the architecture that assumes the answer.

## 2. Unit of evaluation

The unit is not the model, prompt, or interface alone.

It is:

```text
Jonathan + LET + models + artifacts + context + time
```

A technically accurate feature can still fail if it:

- creates too much setup;
- interrupts flow;
- reduces enjoyment;
- produces reflection debt;
- creates false certainty;
- shifts work from creation to correction.

## 3. Experiment lifecycle

1. **Observe:** preserve a real friction, opportunity, or surprise.
2. **Frame:** turn it into a question without assuming the answer.
3. **Baseline:** identify the simplest current method.
4. **Probe:** create the smallest discriminating intervention.
5. **Use:** run it in real or faithfully simulated work.
6. **Evaluate:** record outcome, burden, confounders, and surprise.
7. **Decide:** keep, revise, defer, or remove.
8. **Propagate:** update architecture and open questions.

No more than three experiments should be active simultaneously.

## 4. Primary outcome concepts

### Metacognitive novelty

Did LET produce a useful realization, distinction, correction, or question that Jonathan would probably not have reached at that moment without it?

Examples:

- “I never noticed I describe scenes without specifying them.”
- “I thought aim was the issue, but the clips suggest re-challenging.”
- “I expected the piano transition to fail, but tempo drift happened elsewhere.”
- “I keep converting research uncertainty into implementation.”

### Joy effect

Did LET:

- increase engagement;
- preserve enjoyment;
- have no effect;
- make the activity feel evaluated or optimized;
- reduce desire to continue?

### Operational friction

How much effort was spent operating the system rather than thinking?

### Intervention utility

Was the question or evidence:

- useful;
- interesting but non-actionable;
- already known;
- irrelevant;
- intrusive;
- wrong.

### Correction burden

How much effort was required to repair the system’s model or output?

### Fidelity

Later: how well did Solid represent the current state, within declared scope?

## 5. Gate model

Passing a gate means demonstrated human-system value, not only green tests.

### G0 — Trustworthy capture

Question:

> Can LET reliably preserve and replay an intentional episode?

Required evidence:

- raw save succeeds;
- failure is visible;
- transcript failure does not lose capture;
- backup/restore works;
- Jonathan trusts Stop.

### G1 — Useful episode

Question:

> Does the episode representation make captured material meaningfully easier to revisit and extend?

Required evidence:

- at least one multi-artifact episode;
- raw/derived distinction is understandable;
- follow-up attaches naturally;
- no burdensome categorization.

### G2 — Productive Liquid

Question:

> Can a question or challenge create useful metacognitive novelty?

Required evidence:

- at least one meaningful example;
- examples of rejected/irrelevant prompts retained;
- burden acceptable;
- no claim that more questioning is always better.

### G3 — Calibration

Question:

> Can LET compare self-prediction with later evidence in a way that improves self-understanding?

Required evidence:

- pre-feedback prediction preserved;
- independent evidence available;
- discrepancy understood;
- no overclaim from one case.

### G4 — Context-sensitive support

Question:

> Can LET choose or recommend an intervention stance better than a static default?

Required evidence:

- mode/receptivity data;
- baseline comparison;
- correct uses of silence;
- no unacceptable intervention fatigue.

### G5 — Solid

Question:

> Can an inspectable model predict useful state or preferences across episodes?

Required evidence:

- evidence-linked state;
- uncertainty;
- contradiction handling;
- user contestation;
- acceptable correction burden.

### G6 — Solidus / bounded agency

Question:

> Can ratified commitments safely guide attention or prepared action?

Required evidence:

- values represented with context and review;
- user predicts system behavior;
- rollback;
- no doctrine;
- no high-consequence action without authorization.

## 6. Initial experiment portfolio

### E001 — Capture and episode viability

**Question:** Will one-button voice capture produce episodes Jonathan naturally wants to keep and revisit?

**Baseline:** existing ad hoc notes or no capture.

**Probe:** browser record/stop, raw save, optional title/domain, episode list.

**Primary observable:** Did the episode preserve something valuable with acceptable operational friction?

**Keep if:** capture is trusted and used naturally.

**Revise/remove if:** opening and managing the app outweighs value.

### E002 — Liquid specificity

**Question:** Can a small set of question primitives increase the resolution of film/research reflection?

**Baseline:** preserve original reaction without follow-up.

**Probe:** detect vague references, unsupported conclusions, or undeveloped mechanisms; surface one question or user-selected deeper conversation.

**Primary observable:** Did the response contain meaningful new information or revision?

**Important comparison:** fixed template versus model-generated question.

### E003 — Self-prediction and evidence

**Question:** Does predicting one’s own piano/COD performance before reviewing evidence improve calibration or reveal useful discrepancy?

**Baseline:** ordinary retrospective impression.

**Probe:** one pre-feedback question, optional confidence, then recording/clip comparison.

**Primary observable:** Was the discrepancy useful?

### E004 — Receptivity and mode

**Question:** Do explicit modes improve the fit of Liquid’s support?

**Probe:** just capture / explore / challenge / understand / improve / surprise / decide.

**Primary observable:** Would Jonathan choose the same mode again in a similar Scene?

### E005 — Replay

**Question:** Does rerunning one episode through a different processor reveal enough value to justify first-class replay?

**Probe:** two prompts, models, or processor versions on the same raw episode.

**Primary observable:** Did comparison improve trust, result quality, or design understanding?

### E006 — Manual subscription bridge

**Question:** Can a human-mediated external model workflow support rich experiments without API cost or unacceptable friction?

**Probe:** export Mission Brief, run in Antigravity/subscription app, import result.

**Primary observable:** setup and import burden versus cognitive value.

### E007 — Blind Solid

Later:

**Question:** Can Solid infer a bounded cognitive state from observable episode evidence without seeing Jonathan’s private ground-truth card?

## 7. Observation versus intervention periods

An experiment may operate in:

- **observation mode:** LET predicts but does not act;
- **intervention mode:** LET asks, challenges, or presents evidence;
- **control/baseline:** ordinary behavior or fixed template.

Do not infer natural preference from behavior generated immediately after repeated system prompting.

## 8. Future JITAI-style representation

LET can borrow a structural vocabulary from just-in-time adaptive intervention research without claiming to be a health intervention:

```text
decision point
tailoring/context variables
available intervention options
decision rule
selected option or no intervention
proximal outcome
longer-term outcome
```

Store these fields early enough that later within-person experiments remain possible.

## 9. Lightweight measurement

Avoid making Jonathan fill out research forms after every episode.

Default feedback can be:

- useful;
- not useful;
- wrong;
- already knew;
- intrusive;
- surprising;
- continue;
- stop.

Use richer notes only when the episode warrants them.

## 10. Stop rules

Stop or narrow an experiment when:

- capture or reflection becomes a chore;
- joy declines repeatedly;
- the question produces generic verbosity;
- correction burden exceeds value;
- a simple template performs as well;
- no decision depends on more evidence;
- the effect is caused by prompting rather than the proposed mechanism;
- the system creates identity certainty from sparse data.

## 11. Negative results

A negative result is useful when it tells us:

- a feature is unnecessary;
- a sensor adds noise;
- the right intervention is silence;
- a manual workflow is sufficient;
- a domain should remain unoptimized;
- a model is less useful than a fixed question;
- the concept is interesting but not worth maintaining.

## 12. Advancement review

At each gate review ask:

1. What can Jonathan + LET now do that neither could reliably do alone?
2. What new maintenance or coordination work appeared?
3. What became easier?
4. What became less joyful?
5. Which result came from actual evidence versus narrative enthusiasm?
6. What is the next smallest uncertainty worth reducing?


---

## Source: `docs/06_INITIAL_TWO_WEEK_FIELD_PROGRAM.md`

# Initial Two-Week Field Program

## 1. Nature of the period

This is not a sprint to finish LET.

It is a **field program** in which a minimum substrate is developed, used across ordinary life, and revised only when use reveals a reason.

The period begins after repository creation and ends with an evidence review—not a feature-completion ceremony.

## 2. Desired outcome

By the end of the period, we should know:

- whether desktop voice capture is worth keeping;
- whether Episode is the right organizing unit;
- whether Liquid produces metacognitive novelty;
- whether self-prediction is useful in piano or COD;
- which operational friction matters;
- which domain naturally pulls the project forward;
- what should be built next, removed, or left manual.

## 3. Minimum meaningful build

The implementation progresses through explicit vertical slices:

### Slice 0 — Foundation Capture Substrate (Completed)
- Local app launch (`python app.py` or `let run`);
- Browser microphone record/stop;
- Atomic raw audio persistence with SHA-256 hash calculation;
- SQLite metadata (episodes, artifacts, events);
- Recent episode feed and immediate in-browser audio playback;
- Diagnostic doctor and integrity verification (`let doctor`).

### Slice 1 — Asynchronous Worker & Speech-to-Text (Completed)
- SQLite-backed asynchronous job queue with atomic leasing and retry limits;
- Local `faster-whisper` transcription (`small.en` default with resilient CPU fallback);
- Derived transcript artifacts linked to raw audio with cryptographic hashes;
- Interactive timestamp seeking in web UI (clicking `[00:03]` seeks audio);
- Replay and CLI transcription triggers.

### Slice 2A — Mission Brief Bridge & Polished Synthesis (Active)
- 1-click **Mission Brief** Markdown export tailored by domain and declared mode;
- Dual output protocol: (1) **Polished Synthesis / Review Note** and (2) **Liquid Perturbations**;
- External model response import back into LET;
- Derived analysis persistence with SHA-256 lineage tracking;
- 1-click copy for clean synthesis and prominent Liquid question display.

### Slice 2B — Flexible Follow-Up Dialogue (Planned)
- Multi-modal response capture (voice recording and typed text notes attached directly to Liquid questions);
- Multi-turn conversation trail (*Capture → Question → Answer → Follow-up*).

### Slice 2C — Lightweight Calibration & Built-in Heuristics (Planned)
- 1-tap feedback reactions (`Useful`, `Surprising`, `Already Knew`, `Intrusive`);
- Deterministic/offline question primitives.

Not required:

- passive sensors;
- automatic clone model;
- mobile;
- polished dashboard;
- autonomous intervention;
- screen recording;
- embeddings;
- graph;
- provider API.

## 4. Foundation window

The first few development sessions should answer only:

> Can Jonathan capture and recover an episode confidently?

Recommended sequence:

```text
record
  ↓
save raw
  ↓
show recent episode
  ↓
play it
  ↓
restart application
  ↓
play it again
  ↓
backup and restore
```

Only after that:

```text
transcribe
  ↓
attach transcript
  ↓
fail/retry
```

## 5. Week-one emphasis: capture and one useful question

Use LET opportunistically in ordinary life.

### Movies

After a movie:

- record immediate reaction;
- preserve it before external reviews;
- optionally ask Liquid to find one opening;
- continue only if interesting.

### Piano

At one natural practice boundary:

- state what you expect went well/wrong;
- optionally record or import evidence;
- compare afterward.

### Call of Duty

Between matches or after a session:

- use a quick reflection;
- optionally state one question;
- do not interrupt play.

### Research/spontaneous thought

Capture the idea.

Liquid may:

- define;
- challenge;
- ask what would change the conclusion;
- suggest one adjacent connection.

### Programming

At a breakpoint:

- what problem am I solving?
- what do I currently think?
- what am I waiting on?
- what did an agent change in my model?

## 6. Week-two emphasis: refine the loop, not the breadth

Choose the most promising observed use and improve one piece.

Candidate directions:

- better one-question selection;
- a smoother voice follow-up;
- self-prediction/evidence comparison;
- Mission Brief export/import;
- replay;
- better episode view;
- MARK events.

Do not pursue all of them.

Run at most three active experiments:

1. E001 Capture and episode viability.
2. E002 Liquid specificity.
3. E003 Self-prediction and evidence.

E004–E006 may be used only if they directly reduce friction in those three.

## 7. Suggested natural rhythm

### Capture

- press Record;
- speak;
- stop;
- leave.

### Optional immediate debrief

- choose mode;
- answer one question or continue;
- stop when the thought is complete.

### Processing

- transcription and analysis happen later;
- no need to watch.

### Revisit

- only when desired or when an experiment calls for it.

## 8. Minimal feedback

After a Liquid interaction, one tap may be enough:

- useful;
- interesting;
- wrong;
- already knew;
- intrusive;
- keep going;
- stop.

Optional voice note:

> Why was this useful?

## 9. Expedite path

To test advanced cognition quickly without expensive integration:

1. record in LET;
2. transcribe locally;
3. export a structured Mission Brief;
4. open Antigravity or an existing AI subscription;
5. run the brief through a strong model;
6. import or paste the result;
7. answer inside LET by voice.

This is a valid first-class workflow.

Do not mistake manual transport for architectural failure. It buys learning before integration.

## 10. Synthetic corpus

Before experimental processors touch live data, maintain a small synthetic corpus:

- fake movie reaction with vague language;
- fake piano self-assessment contradicted by evidence;
- fake COD frustration hypothesis;
- fake research idea with an unsupported assumption;
- fake work episode;
- transcript error;
- conflicting model outputs;
- identity overreach case.

The corpus supports agent development and regression tests without risking the archive.

## 11. Friction log

Record only meaningful friction:

```markdown
Context:
What I was trying to do:
Friction:
Workaround:
Did it prevent use?
Possible smallest fix:
```

Do not quantify every interaction.

## 12. What to watch for

Positive signals:

- desire to capture;
- richer specificity;
- spontaneous follow-up;
- useful disagreement;
- revised belief;
- better self-calibration;
- increased enjoyment;
- wanting to revisit.

Warning signals:

- avoiding the app;
- generic questions;
- feeling judged;
- turning play into obligation;
- excessive setup;
- transcript cleanup becoming the project;
- accumulating unreviewed analysis;
- building more than using.

## 13. End-of-period review

Review a small set of episodes, not only aggregate counts.

Ask:

1. Which capture would otherwise not exist?
2. What did Liquid make Jonathan notice?
3. Which question was best and why?
4. Which question should never have been asked?
5. Did any self-prediction differ from evidence?
6. Did LET increase, preserve, or reduce joy?
7. What operation created the most friction?
8. What feature was unnecessary?
9. Which domain produced the strongest pull?
10. What is the next gate?

Possible decisions:

- continue foundation;
- deepen Liquid;
- deepen one domain;
- build replay;
- pause development and collect more;
- simplify;
- stop.

## 14. Definition of a good first two weeks

A good field period does not require a clone.

It requires enough lived evidence to make the next architectural decision less imaginary.


---

## Source: `docs/07_RISKS_GOVERNANCE_AND_FAILURE_MODES.md`

# Risks, Governance, and Failure Modes

## 1. Governance objective

LET is a personal system, but it can still become coercive, misleading, intrusive, expensive, or difficult to escape.

Governance begins before autonomous action because the system can influence identity and cognition through representation alone.

## 2. Human authority

Jonathan retains authority to:

- inspect source evidence;
- see why a model made a claim;
- correct or contest;
- mark historical rather than current;
- suppress from active use;
- delete or purge;
- disable a processor;
- require silence;
- switch providers;
- export;
- retire a clone or the entire system.

## 3. Authority ladder

| Object | May act as source? | May update current self-model automatically? |
|---|---:|---:|
| Raw user recording | Yes | No |
| Direct explicit decision | Yes | Only within declared scope |
| External event | Yes | No |
| Transcript | Yes, with caveat | No |
| Model observation | Supporting evidence | No |
| Model interpretation | Hypothesis | No |
| Cross-episode inference | Hypothesis | No |
| Value/identity model | Only after ratification | No silent update |

## 4. Human and cognitive risks

### Joy erosion

The system turns movies, piano, games, and curiosity into performance-management projects.

Controls:

- play/experience modes;
- no-intervention option;
- joy feedback;
- no productivity score;
- explicit “nothing to improve” outcome;
- stop rules.

### Intervention fatigue

Repeated questions reduce receptivity and create avoidance.

Controls:

- user-selected modes;
- question ranking;
- optional continuation;
- shadow mode;
- no streaks or debt.

### Excessive self-consciousness

During skilled or immersive activity, metacognitive prompting degrades flow or performance.

Controls:

- silence during execution by default;
- pre/post support;
- MARK-only during flow;
- self-controlled feedback.

### Overoptimization

The system optimizes an easily measured proxy and narrows the broader activity.

Controls:

- declare purpose;
- preserve qualitative reflection;
- include joy and meaning;
- compare with no-analysis periods.

### Dependence and skill loss

LET answers before Jonathan predicts or reconstructs.

Controls:

- self-prediction before feedback;
- retrieval/reconstruction modes;
- epistemic ownership choices;
- occasional no-AI baseline.

## 5. Epistemic risks

### Phantom Memory

A generated reconstruction is later treated as fact.

### Identity ossification

Temporary behavior becomes a stable self-description.

### Confidence laundering

A confident model output makes weak evidence feel authoritative.

### Correlated clones

Solid, Liquid, and Solidus agree because they share the same faulty source or prompt.

### Historical overwrite

Later interpretation replaces the original voice.

### Context collapse

A pattern from one Scene is generalized across all domains.

Controls across these risks:

- provenance;
- confidence;
- contradiction search;
- independent framing;
- raw preservation;
- scope/time;
- user ratification;
- replay with alternative processors.

## 6. Metal Gear failure modes

### Patriots Problem

> *"What we propose to do is not to control content, but to create context."*
> — **GW / The Patriots AI**, *Metal Gear Solid 2: Sons of Liberty*

Invisible curation controls the information environment.

### S3 Contamination

Intervention-produced behavior is mistaken for natural observation.

### Venom Problem

> *"I am you, and you are me. Carry that with you wherever you go."*
> — **Big Boss**, *Metal Gear Solid V: The Phantom Pain*

Jonathan starts performing the twin’s description.

### The Boss’s Will Problem

> *"She wanted to make the world whole again. But Zero and I... we misunderstood her will."*
> — **Big Boss**, *Metal Gear Solid 4: Guns of the Patriots*

A contextual value becomes doctrine.

### Les Enfants Determinism

> *"You mustn't allow yourself to be chained to fate, to be ruled by your genes."*
> — **Solid Snake**, *Metal Gear Solid*

Inherited data is treated as destiny.

These names should appear in design reviews because they are memorable checks, not merely lore.

## 7. Technical risks

### Data loss

Controls:

- atomic capture;
- hash;
- local backups;
- restore rehearsal;
- no dependency on transcription success.

### Database/media divergence

Controls:

- artifact manifests;
- doctor command;
- orphan detection;
- repair tooling;
- stable IDs.

### Storage growth

Controls:

- monitoring;
- explicit data root;
- derived-artifact cleanup policy later;
- raw-retention policy;
- delayed video expansion.

### Job duplication or corruption

Controls:

- leases;
- idempotency;
- distinct processor-run IDs;
- retry state;
- no in-place output replacement.

### Model/provider drift

Controls:

- record version;
- preserve prompt;
- replay;
- compare;
- local fallback.

### Accidental Git commit

Controls:

- data outside repo;
- `.gitignore`;
- pre-commit checks;
- synthetic fixtures only.

## 8. Cost risks

The user is comfortable with cloud processing but does not want recurring API cost.

Controls:

- cost-zero default;
- manual subscription bridge;
- local ASR;
- explicit provider adapter;
- cost logging if an API is enabled;
- no mandatory hosted service.

## 9. Professional/personal boundary

Professional episodes may contain sensitive context even if privacy is not a personal concern.

Initial rule:

- reflections may enter LET;
- professional canonical evidence remains in its governed repository;
- secrets and credentials never enter;
- external model export is deliberate;
- future bridges expose bounded context.

## 10. Availability and graceful degradation

LET remains useful without:

- internet;
- generative AI;
- transcription;
- a particular model;
- a sensor;
- advanced retrieval.

Core capture, playback, episode browsing, export, and restore should still work.

## 11. Contestation and correction

Corrections should:

- preserve the original model output;
- record who corrected it;
- record why;
- update current status;
- identify dependent snapshots;
- not rewrite raw history.

## 12. Model retirement

A clone or processor may be:

- experimental;
- active;
- suspended;
- superseded;
- retired.

Retirement means it no longer influences current recommendations. Historical outputs remain available for audit unless purged.

## 13. Destructive actions

Before deletion/purge, show:

- raw files;
- derived files;
- database rows;
- transcripts;
- summaries;
- model snapshots;
- indexes;
- backups;
- exports;
- downstream conclusions.

No destructive feature belongs in the earliest build beyond safe removal of synthetic/test data.

## 14. Ethical posture

LET should not infer or diagnose psychological, medical, or neurocognitive conditions from voice, activity, or behavior.

Any future sensitive inference class requires:

- explicit purpose;
- evidence review;
- appropriate expertise;
- user consent;
- strong limits;
- independent validation;
- clear non-diagnostic language.

## 15. Final governance test

> *"It's not about changing the world. It's about doing our best to leave the world... the way it is. It's about respecting the will of others, and believing in your own."*
> — **Big Boss**, *Metal Gear Solid 4: Guns of the Patriots*

Before enabling a new capability, ask:

> Does this make the shadow more useful to Big Boss—or does it increase the shadow’s power over him?


---

## Source: `docs/08_RESEARCH_MAP_AND_RELATED_SYSTEMS.md`

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


---

## Source: `docs/09_DECISIONS_AND_OPEN_QUESTIONS.md`

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


---

## Source: `templates/episode-record.md`

# Episode: <title>

## Identity

- **Episode ID:**
- **Domain:** movie / piano / COD / research / programming / thought / other
- **Started:**
- **Ended:**
- **Declared mode:** just capture / explore / challenge / understand / improve / surprise / decide
- **Purpose:**

## Raw artifacts

| Artifact | Type | Time | SHA-256 | Notes |
|---|---|---|---|---|

## Immediate reflection

Preserve the spontaneous reflection or link to its raw recording/transcript.

## Pre-feedback prediction

- **What do I think happened?**
- **What do I expect?**
- **Confidence:**
- **What evidence would change my mind?**

## Liquid intervention

- **Decision point:**
- **Stance:**
- **Question or evidence:**
- **Why this was selected:**
- **Alternative options suppressed:**

## Response

Link the raw answer and transcript.

## Evidence comparison

What later evidence agreed, disagreed, or remained ambiguous?

## Feedback

- [ ] Useful
- [ ] Surprising
- [ ] Wrong
- [ ] Already known
- [ ] Intrusive
- [ ] Increased joy/engagement
- [ ] Reduced joy/engagement
- [ ] Continue
- [ ] Stop

## What changed?

Did the episode produce:

- more specificity;
- a revised explanation;
- a new question;
- a behavior change;
- a writing/research idea;
- no meaningful change?

## Provenance

List processor runs, prompts, model versions, and source spans.

## Follow-up

One optional next action. Leave empty when none is needed.


---

## Source: `templates/experiment-record.md`

# Experiment: <ID> — <title>

## Question

What uncertainty can this experiment reduce?

## Decision affected

What might we do differently based on the result?

## Current assumption

What do we presently believe, and how uncertain is it?

## Baseline

What is the simplest comparison?

## Intervention / probe

What is the smallest change being tested?

## Domain and Scene

Where and under what conditions will it run?

## Inputs

What evidence, sensors, episodes, or models are required?

## Outcomes

### Primary observable

One thing that most directly answers the question.

### Secondary observations

At most a small number.

## Burden and joy checks

- operational effort;
- interruption;
- correction burden;
- enjoyment/engagement.

## Observation/intervention status

- [ ] Observation only
- [ ] Intervention
- [ ] Includes no-intervention comparison
- [ ] Randomized decision point

## Procedure

1.
2.
3.

## Stop rule

When should we stop rather than collect more?

## Result

What happened?

## Confounders

What else could explain the result?

## Decision

- [ ] Keep
- [ ] Revise
- [ ] Defer
- [ ] Remove
- [ ] Run a sharper follow-up

## Rationale

Why?

## Artifacts

Episodes, processor runs, code, fixtures, and evidence.

## Reconsider when

What future evidence would reopen this decision?


---

## Source: `templates/processor-card.md`

# Processor: <name>

## Identity

- **Processor name:**
- **Version:**
- **Owner:**
- **Status:** experimental / active / suspended / superseded / retired

## Purpose

What transformation or cognitive operation does this processor perform?

## Supported inputs

- artifact types;
- episode requirements;
- context requirements.

## Outputs

What exact objects does it produce?

## Epistemic authority

What may this output support?

What must it never be treated as?

## Implementation

- local deterministic;
- local model;
- subscription/manual bridge;
- paid API;
- external sensor.

## Configuration

Record prompt, model, decoding/configuration, schema, and dependencies.

## Provenance

How are source artifacts and spans linked?

## Failure behavior

What happens if it fails, times out, or returns invalid content?

## Cost

Compute, storage, API, and human effort.

## Evaluation

- fixtures;
- real episodes;
- baseline;
- known failure modes;
- user feedback.

## Replay

Can prior episodes be processed with this version?

## Retirement

How is influence removed while preserving history?
