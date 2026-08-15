---
title: "Les Enfants Terribles — Integrated Development Roadmap and Experimental Program"
project: "Les Enfants Terribles"
project_code: "LET"
status: "proposed_roadmap_update"
version: "0.2-draft"
source_commit: "550422eaac46ed244fa73c8e68911612c9fb35f8"
prepared: "2026-08-15"
---

# Les Enfants Terribles — Integrated Development Roadmap and Experimental Program

## 0. Purpose of this document

This document is a synthesis and proposed update to the existing LET planning baseline after the first period of actual use and development.

It is intentionally broader than a sprint plan.

It should be used to:

1. correct the remaining integrity problems in the current implementation;
2. formalize the next major product abstractions now suggested by real use;
3. preserve a large development and experiment backlog without pretending everything should be active at once;
4. provide concrete reflection structures for movies, piano, Call of Duty, research, programming, and retrospective life capture;
5. create a path from today's useful capture tool toward the longer-term Solid / Liquid / Solidus cognitive-twin program;
6. keep the stable capture substrate boring while allowing the cognitive protocol layer to evolve rapidly.

This roadmap does **not** impose an artificial speed limit on development.

The project may implement or prototype ideas faster than expected. The constraint should instead be:

> **Development inventory may be large; active experimental conditions should remain limited enough that observed effects are interpretable.**

The existing "no more than three active experiments" rule should therefore be interpreted as an **experimental-concurrency rule**, not a prohibition on implementing future-capability scaffolds, branches, fixtures, or dormant protocols.

---

# 1. Current state at source commit `550422e`

The project has moved beyond a planning-only baseline.

The current implementation reports the following completed vertical slices:

- **Slice 0 — Foundation Capture Substrate**
  - local Flask application;
  - browser microphone recording;
  - raw immutable audio storage;
  - episode/artifact/event persistence;
  - replayable media;
  - system doctor.

- **Slice 1 — Asynchronous Transcription**
  - SQLite-backed queue;
  - leased worker behavior;
  - faster-whisper transcription;
  - raw-to-transcript provenance;
  - replay/retranscription.

- **Slice 2A — Mission Brief Bridge**
  - external strong-model workflow without recurring API spend;
  - source/provenance headers;
  - polished synthesis plus Liquid perturbation output;
  - import of external model output.

- **Slice 2B — Interactive Liquid Follow-Up**
  - structured perturbation items;
  - voice/text responses;
  - source-linked follow-up artifacts;
  - multi-turn episode trails.

- **Slice 2C — Lightweight Calibration and Local Heuristics**
  - local deterministic probes;
  - `Sharp / Known / Irrelevant` feedback;
  - question brevity;
  - domain/mode-specific heuristics.

- **Slice 2D — Pre-Session Prediction and Vocabulary Scaffolding**
  - prediction capture;
  - spoken prediction support;
  - prediction-to-reflection comparison;
  - domain concept palettes;
  - glossaries;
  - draft persistence through browser reloads.

The current head commit reports **55/55 automated tests passing**. That should be recorded as implementation evidence, but not confused with field validation.

## 1.1 The most important observed user signal

The strongest field signal so far is not a benchmark.

It is:

> **The capture loop is easy enough to use naturally, and the user likes using it.**

That moves the primary bottleneck.

The project no longer needs to spend all of its attention proving that a voice-capture diary can exist.

The next problem is:

> **How should LET structure attention and reflection so that the captured material becomes increasingly useful for learning, comparison, metacognition, vocabulary acquisition, and longitudinal self-understanding without turning enjoyable activities into obligatory optimization?**

---

# 2. New architectural stance

The stable substrate should remain:

```text
raw evidence
    ↓
episode
    ↓
derived artifacts
    ↓
provenance
    ↓
replay
```

The rapidly evolving research layer should become:

```text
THREAD
  │
  ├── EPISODES through time
  │
  ├── PROTOCOLS that structure reflection
  │
  ├── LENSES that introduce concepts/vocabulary
  │
  ├── PREDICTIONS and self-models
  │
  ├── EVIDENCE and external research
  │
  ├── LIQUID INTERVENTIONS
  │
  └── COMPARISONS / TRAJECTORIES
```

The project should avoid adding cognitive complexity directly into the capture substrate.

Instead:

> **Make the substrate stable; make protocols cheap to create, change, compare, disable, and replay.**

---

# 3. Immediate current-system corrections

These are not conceptual redesigns. They are integrity fixes or near-term hardening that should occur before the relevant data is treated as high-quality longitudinal evidence.

## FIX-01 — Make pre-session predictions truly append-only

### Current issue

The current user-facing API prevents changing a prediction after a primary raw capture exists, which is useful.

However, the underlying representation remains a mutable `prediction_json` field on the Episode, and `Episode.set_prediction()` replaces that JSON. The test suite also verifies replacing one prediction with another.

This creates an experimental integrity gap during the interval:

```text
prediction submitted
      ↓
practice / play / work occurs
      ↓
post-session capture begins
```

Until primary capture occurs, the prediction can still be rewritten.

### Required direction

Prediction history should be append-only.

Preferred long-term structure:

```text
predictions
-----------
id
episode_id
prediction_type
target_concept_id
statement_artifact_id / statement_text
confidence
created_at
supersedes_prediction_id nullable
locked_at
```

A correction should produce:

```text
Prediction A
    ↓ superseded-by
Prediction B
```

not mutation of Prediction A.

### Why

The value of prediction is precisely that it freezes the earlier model before hindsight can reconstruct it.

---

## FIX-02 — Do not mutate prediction content when voice transcription finishes

### Current issue

A spoken prediction begins as raw prediction audio, but the asynchronous worker later writes the Whisper transcription into `prediction_text`.

That makes a derived machine transcript appear to be the original prediction representation.

### Required direction

Preserve:

```text
raw prediction audio
      ↓
prediction transcript artifact
```

Prediction metadata should reference both.

A transcript can be corrected later without changing the historical prediction artifact.

---

## FIX-03 — Make prediction-audio registration part of the same durable capture bundle

### Current issue

Prediction audio can be written to disk before the main capture, while its Artifact row is currently registered separately after the episode/main-artifact transaction.

Possible failure modes include:

- orphan prediction media;
- an Episode whose `prediction_artifact_id` points at a row that was never created;
- a successful main capture with a partially registered pre-session prediction.

### Required direction

Expand `create_capture_bundle()` or introduce a generalized transaction API capable of committing:

- Episode;
- primary raw Artifact;
- prediction raw Artifact(s);
- prediction record;
- events;
- transcription jobs;

in a coherent transaction after all irreplaceable files have been safely written.

Recovery receipts should include all raw files involved in the bundle.

---

## FIX-04 — Separate stable concept identity from UI labels

### Current issue

Concept selections currently contain display strings such as:

- `⏱️ Tempo / Rushing`
- `⚔️ Ego-Challenging`
- `🦾 Tension / Posture`

while glossary entries use different terminology and no stable concept IDs.

### Required direction

Create stable identifiers:

```yaml
id: cod.centering
display_name: Centering
aliases:
  - crosshair placement
domain: cod
```

UI decorations and emojis should never become canonical identity.

---

## FIX-05 — Treat the current glossary as hypotheses, not canonical expertise

### Current issue

The vocabulary scaffolding is valuable as a prototype, but the present hard-coded definitions are uncited and may contain:

- local jargon;
- game-specific jargon;
- title/version-specific concepts;
- oversimplified piano pedagogy;
- project-specific invented concepts;
- concepts that are useful but not standard expert vocabulary.

### Required direction

Develop a source-backed **Concept Library**.

A concept should eventually contain:

```yaml
id:
term:
plain_language_definition:
aliases:
domain:
scope:
source_type:
sources:
confidence:
examples:
counterexamples:
user_examples:
first_seen_at:
accepted_state: proposed | useful | rejected | established-for-user
version:
```

The system must be allowed to say:

> "Possible term: centering. This appears to describe what you reported, but LET has not yet established that the concept is the best fit."

---

## FIX-06 — Record concept exposure to prevent hidden priming

Vocabulary changes what a person can attend to and how experience is categorized.

Therefore LET should record:

```text
Was a concept/lens shown before the experience?
Was it shown after blind reflection?
Was it introduced by Liquid?
Was it requested by the user?
```

This is necessary for later comparisons.

---

## FIX-07 — Add explicit Blind vs Lens operation

Do not automatically expose domain concept chips in every reflective workflow.

### Blind

```text
experience
   ↓
natural reflection
   ↓
freeze
   ↓
concepts / expert language revealed
```

Purpose: observe what the user notices without LET priming the categories.

### Lens

```text
choose concept
   ↓
experience
   ↓
reflect through that lens
```

Purpose: intentionally train attention or discrimination.

Both are useful.

They answer different questions.

---

## FIX-08 — Reduce leading certainty in local heuristics

Some current heuristic prompts name plausible mechanisms before evidence exists, e.g. physical tension, motor trajectory, positioning, spawn behavior, or tactical cause.

The existing Mission Brief has an epistemic guardrail; local heuristic questions need the same philosophy.

Prefer:

> "Could this have been a centering issue, or did it feel more like something else?"

over:

> "Was your centering compromised three seconds earlier?"

when no gameplay evidence exists.

Every local probe should know whether it is:

- clarification;
- candidate vocabulary;
- hypothesis;
- contradiction;
- evidence-backed observation.

---

## FIX-09 — Split implementation status from experimental status

The current field document uses labels such as:

> Slice 2D — Completed

That is technically correct as a software statement, but can be misread as:

> E003 is validated.

Introduce explicit dual status:

```yaml
implementation_status: implemented
field_status: collecting
gate_status: not_passed
```

A feature can be finished while the research question remains unresolved.

---

## FIX-10 — Prepare temporal fields for retrospective capture

Past-event reflection is becoming a first-class use case sooner than originally expected.

The data model should distinguish:

```text
occurred_at
recorded_at
recalled_at
estimated_date
date_precision
source_mode
```

Possible `source_mode` values:

- `immediate`
- `delayed_reflection`
- `retrospective_reconstruction`
- `rewatch`
- `external_historical_artifact`

Do not fake historical timestamp precision.

---

## FIX-11 — Keep compiled planning artifacts generated, not manually duplicated

As the project changes quickly, the large compiled planning packet can drift from the source documents.

If retained, generate it from canonical docs and optionally validate it in CI.

Otherwise remove it from the authoritative documentation path.

---

# 4. Core new abstractions

## 4.1 Episode

Retain **Episode**.

Definition:

> A bounded slice of lived experience, reflection, practice, performance, play, work, or recall.

Episode remains the primary storage/replay unit.

Examples:

- post-movie reaction;
- one piano practice block;
- a COD session reflection;
- a research insight;
- a retrospective memory;
- one programming breakpoint.

---

# 4.2 Thread

## Definition

A **Thread** is a meaningful thing whose relationship to the user persists across multiple Episodes.

Episode answers:

> What happened at this moment?

Thread answers:

> How is my relationship with this thing changing?

### Examples

```text
Thread: Film — Alien
├── first-watch immediate reaction
├── one-week Blind Echo
├── pre-rewatch memory
├── rewatch reaction
└── later essay
```

```text
Thread: Piano Piece — Chopin Nocturne Op. 9 No. 2
├── practice 1
├── practice 2
├── performance
├── practice after research pull
└── six-month revisit
```

```text
Thread: COD Concept — Centering
├── concept discovery
├── Lens session
├── blind session
├── gameplay review
└── later calibration
```

```text
Thread: Research Question — Recurrent latent state
├── spontaneous hypothesis
├── literature pull
├── experiment
├── contradiction
└── revised model
```

## Thread types

Initial candidate types:

- `subject`
- `movie`
- `book`
- `game`
- `piano_piece`
- `skill`
- `concept`
- `research_question`
- `project`
- `creative_work`
- `practice_goal`
- `open_question`
- `life_event`

Do not make the enum rigid prematurely.

## Relationship model

An Episode may eventually belong to multiple Threads.

Example:

```text
Piano Practice Episode
├── Thread: Chopin Nocturne
├── Thread: Rubato
└── Thread: Wrist Tension
```

Recommended representation:

```text
threads
episode_threads
```

with a role such as:

- primary;
- related;
- generated;
- evidence-for.

For the first implementation, allowing one primary Thread plus optional secondary links is sufficient.

---

# 4.3 Protocol

## Definition

A **Protocol** is a cognitive procedure applied to an Episode or Thread.

Mode answers:

> How should Liquid interact?

Protocol answers:

> What thinking process are we performing?

These should remain orthogonal.

Example:

```text
Domain: movie
Thread: Alien
Protocol: Blind Echo
Mode: Explore
```

## Initial protocol library

### Free Capture

Purpose: preserve whatever naturally comes to mind.

Steps:

1. record;
2. preserve;
3. optional Liquid;
4. stop.

No forced analysis.

### After-Action Review

Purpose: learn from performance or practice.

Core structure:

1. What did I expect?
2. What happened?
3. What differed?
4. What might explain the difference?
5. What, if anything, should change next time?

Best fit:

- piano;
- COD;
- programming;
- real-world work.

### Calibration

Purpose: compare self-prediction to later evidence.

Steps:

1. freeze prediction;
2. act/practice/play;
3. collect blind post-assessment;
4. reveal evidence;
5. compare;
6. record discrepancy and confidence update.

### Concept Lens

Purpose: intentionally use expert vocabulary to improve noticing.

Steps:

1. choose one concept;
2. review definition/examples;
3. perform/watch/play;
4. reflect specifically through that lens;
5. determine whether the concept actually fit.

### Blind Echo

Purpose: capture current reconstruction of an earlier event before seeing prior evidence.

Steps:

1. hide earlier Episode;
2. record current memory/interpretation;
3. freeze;
4. reveal original;
5. compare what persisted, vanished, emerged, or changed.

### Compare

Purpose: directly contrast two or more Episodes.

Comparison targets may include:

- transcript;
- self-rating;
- prediction;
- vocabulary;
- stated causal explanation;
- emotional residue;
- judgment;
- confidence;
- objective evidence.

### Research Pull

Purpose: convert a practical uncertainty into outside expertise.

Steps:

1. capture the user's current language/model;
2. define what is unknown;
3. retrieve source-backed concepts/research;
4. propose a small concept set;
5. distinguish established findings from candidate interpretations;
6. attach the research artifact to the Thread;
7. optionally run Teach-Back or Concept Lens next.

### Teach-Back

Purpose: test whether new language has become usable knowledge.

Steps:

1. hide definition;
2. user explains concept in own words;
3. provide an example from their own experience;
4. distinguish it from neighboring concepts;
5. compare to source.

### Creative Expansion

Purpose: let a captured reaction become writing rather than merely analysis.

Examples:

- film essay;
- short review;
- research note;
- project argument;
- personal reflection.

Important: this should preserve the pre-polish source.

### Reflection Ladder

Purpose: run a constrained multi-turn Liquid conversation rather than independent questions.

Possible sequence:

```text
SPECIFY
   ↓
EXPLAIN
   ↓
CONTRAST
   ↓
PREDICT
```

One question at a time.

Stop when marginal cognitive novelty falls off.

### Legacy Reconstruction

Purpose: capture memories or views of events that occurred before LET existed.

Requirements:

- mark as retrospective;
- allow approximate dates;
- never present reconstruction as contemporaneous evidence;
- later external artifacts can be attached without overwriting the reconstruction.

### Rewatch / Re-experience

Purpose: compare:

```text
original reaction
      ↓
later memory
      ↓
pre-rewatch expectation
      ↓
post-rewatch reaction
```

This is especially valuable for movies, games, music, books, and places.

---

# 4.4 Lens

A **Lens** is a temporary conceptual frame deliberately introduced to alter or sharpen attention.

Examples:

- COD: centering;
- COD: spawn rotation;
- piano: rubato;
- piano: pedaling;
- movie: blocking;
- movie: diegetic sound;
- research: falsification;
- programming: state invariant.

Lens exposure must be logged because the lens can alter the observation.

A Lens is not the same thing as a Protocol.

`Concept Lens` is a Protocol that explicitly uses one or more Lenses.

Other Protocols may also introduce Lenses later.

---

# 4.5 Concept Library

The Concept Library should become LET's interface to **expert representations**.

The goal is not trivia.

The goal is:

```text
experience
    ↓
user language
    ↓
candidate expert representation
    ↓
discrimination
    ↓
user-owned concept
```

Core actions:

- `suggest concept`
- `define`
- `show neighboring concept`
- `show example`
- `show counterexample`
- `source`
- `accept as useful`
- `reject`
- `teach back`
- `use as lens`
- `search user episodes for examples`

Later, Solid can learn which concepts the user truly uses rather than merely which ones LET displayed.

---

# 4.6 Reflection

Reflection should become an explicit object rather than being inferred only from raw artifacts.

Important dimensions:

```text
phase:
  pre
  immediate
  prompted
  delayed
  blind_recall
  post_evidence
  post_research
  rewatch

authorship:
  user
  model
  joint

visibility_condition:
  blind
  prior_episode_seen
  concepts_seen
  evidence_seen
```

This will become essential for longitudinal interpretation.

---

# 4.7 Protocol Run

Do not only store which Protocol an Episode "used."

Store each execution:

```yaml
protocol_run_id:
protocol_id:
protocol_version:
episode_id:
thread_id:
started_at:
completed_at:
steps_completed:
lenses_exposed:
prior_evidence_visible:
interventions:
outputs:
abandoned_at:
```

This makes protocols replayable and scientifically legible.

---

# 5. Protocol engine as a development multiplier

The next high-leverage developer tool may be a configuration-driven Protocol Registry.

Candidate structure:

```text
protocols/
├── free_capture.yaml
├── after_action.yaml
├── calibration.yaml
├── concept_lens.yaml
├── blind_echo.yaml
├── compare.yaml
├── research_pull.yaml
├── teach_back.yaml
├── creative_expansion.yaml
└── reflection_ladder.yaml
```

A protocol might specify:

```yaml
id: blind_echo
version: 1
title: Blind Echo

applies_to:
  - thread_with_prior_episode

visibility:
  hide_prior_episode_until_step: reveal

steps:
  - id: reconstruct
    type: capture
    prompt: >
      Without looking at your previous reflection, what do you now
      remember, think, and feel about this?

  - id: freeze
    type: commit_artifact

  - id: reveal
    type: reveal_prior_episode

  - id: compare
    type: liquid_question
    prompt_class: temporal_compare

outputs:
  - reflection
  - comparison
```

This keeps the application from becoming a collection of hard-coded domain workflows.

The UI can execute Protocols while the storage layer stays unchanged.

---

# 6. Domain-specific collection scaffolds

These are menus, not mandatory forms.

The user should always retain **Free Capture**.

## 6.1 Movies

### Natural immediate capture

Possible openings:

- What stayed with me?
- What specifically did I like/dislike?
- What exact scenes am I referring to?
- What changed in the back half?
- What performance or formal choice mattered?
- What did I expect versus receive?
- What am I uncertain about?

### Productive Liquid probes

When language is vague:

> "You said several scenes stood out. Which exact scene is most vivid, and what was it doing?"

When causal mechanism is missing:

> "You liked the back half more. What changed: pacing, stakes, character dynamics, style, or something else?"

When conclusion is strong:

> "What in the film is the strongest evidence for that reading?"

### Longitudinal movie Thread

Candidate episode sequence:

```text
Immediate reaction
        ↓
Blind Echo after delay
        ↓
Optional criticism/research
        ↓
post-research reflection
        ↓
pre-rewatch memory/prediction
        ↓
rewatch reaction
        ↓
creative synthesis
```

### Candidate vocabulary classes

- cinematography;
- editing;
- blocking;
- production design;
- diegetic/non-diegetic sound;
- pacing;
- narrative structure;
- performance;
- genre convention;
- motif;
- tone;
- theme;
- ambiguity;
- emotional residue.

Vocabulary should be source-backed and introduced carefully.

---

# 6.2 Piano

The most useful framework is likely a cyclical practice model:

```text
FORETHOUGHT
goal / prediction / strategy
        ↓
PERFORMANCE
play / monitor / mark
        ↓
SELF-REFLECTION
evaluate / explain / adapt
        ↺
```

### Before practice

Optional:

- What am I focusing on?
- What do I predict will break down?
- What strategy am I trying?
- What would count as improvement?

### During practice

Minimal interruption.

Possible MARK only.

### After practice

- What improved?
- What failed?
- Was the expected problem actually the main problem?
- Where did attention shift?
- What strategy changed the result?
- What should I try next?

### Potential conceptual families

- pulse/tempo;
- subdivision;
- articulation;
- fingering;
- hand/arm coordination;
- tension/release;
- pedaling;
- voicing;
- balance;
- dynamics;
- phrasing;
- rubato;
- memory;
- anticipation/visual targeting;
- practice strategy.

Do not diagnose physical mechanics from self-report alone.

---

# 6.3 Call of Duty

A useful decomposition is:

```text
MECHANICS
Can I execute?

PERCEPTION
Did I notice the signal?

GAME KNOWLEDGE
Did I understand the state?

DECISION
Did I choose well?

TEMPO / INITIATIVE
Did I act at the right time?

PSYCHOLOGICAL STATE
Did tilt, confidence, impatience, or flow alter behavior?
```

This is substantially richer than aim/KD.

### Possible capture rhythms

- pre-session curiosity;
- one between-match thought;
- end-of-session AAR;
- occasional gameplay-video review;
- targeted Lens session.

### Candidate concepts to research/source properly

- centering;
- pre-aim;
- sprint-to-fire;
- chall/re-chall/ego-chall;
- trading;
- baiting;
- anchoring;
- spawn influence/control;
- rotation;
- route timing;
- power position;
- head glitch;
- off-angle;
- information advantage;
- pacing/tempo;
- map control;
- objective timing;
- spawn read;
- audio cue usage.

Terminology may vary by title, mode, community, and competitive ruleset.

The Concept Library must store scope.

---

# 6.4 Research and spontaneous thought

Possible protocol:

```text
capture intuition
   ↓
state claim
   ↓
what would falsify?
   ↓
mechanism
   ↓
unknown
   ↓
Research Pull
   ↓
revised claim
```

Useful vocabulary:

- hypothesis;
- mechanism;
- confound;
- causal direction;
- falsifier;
- boundary condition;
- measurement artifact;
- alternative explanation;
- evidence strength;
- uncertainty;
- discriminating experiment.

---

# 6.5 Programming / agentic development

Potential capture structure:

- What problem am I actually solving?
- What invariant matters?
- What do I predict is risky?
- What am I delegating to the agent?
- What must I personally understand?
- What changed in my mental model?
- What evidence would make me trust the change?
- What is the clean resumption point?

Long-term Thread possibilities:

- feature;
- architectural decision;
- recurring bug class;
- development technique;
- agent-use strategy.

LET should not duplicate the canonical external project knowledge base.

It should model the human cognitive relationship to that work.

---

# 6.6 General / spontaneous life capture

Default should remain:

> Press record. Speak. Stop.

Do not require every thought to become a Protocol.

The system should preserve unstructured evidence.

A Protocol can be attached later if a Thread emerges.

---

# 7. Longitudinal and retrospective memory program

## 7.1 Resonance Drift

Working term:

> Change in the salience, meaning, confidence, or emotional residue of an experience across time.

Potential measurements are qualitative first.

Ask:

- What persisted?
- What disappeared?
- What grew?
- What became more certain?
- What became ambiguous?
- What details appeared only later?
- What judgments reversed?

Do not collapse this into a single numeric score.

## 7.2 Blind Echo

Blind Echo should become a first-class Protocol because showing the original reflection before current recall contaminates the comparison.

Rule:

> **Current reconstruction must be frozen before prior evidence is revealed.**

## 7.3 Retrospective reconstruction

LET should allow records of events that predate LET.

Example:

> "My current memory of the first time I saw Jurassic Park."

This is valuable evidence of the **current autobiographical model**, not necessarily a reliable contemporaneous reconstruction.

It should be labeled honestly.

## 7.4 Re-experience triads

High-value pattern:

```text
original experience
        ↓
delayed memory
        ↓
re-experience / rewatch
        ↓
new reflection
```

This can apply to:

- movies;
- games;
- books;
- music;
- places;
- old code/projects;
- ideas;
- life events.

---

# 8. Experiment portfolio

## Governing distinction

The backlog below is intentionally large.

It is not the same as the set of active experiments.

Maintain:

```text
DEVELOPMENT BACKLOG: unlimited
PROTOCOL LIBRARY: unlimited/dormant
ACTIVE EXPERIMENTS: ideally ≤ 3
```

An experiment becomes "active" when the project is deliberately changing what the user sees/does and evaluating the consequences.

## Existing experiments

### E001 — Capture and Episode Viability

Question:

> Does LET make valuable intentional capture natural enough to keep using?

Current state: field evidence is positive, continue observing rather than endlessly rebuilding.

### E002 — Liquid Specificity

Question:

> Can targeted questions increase the resolution of reflection?

Continue collecting:

- Sharp;
- Known;
- Irrelevant;
- answered/not answered;
- whether follow-up produced new thought.

### E003 — Self-Prediction and Evidence

Question:

> Does freezing a prediction and comparing it with later reflection/evidence improve calibration?

Required correction before strong interpretation:

- append-only prediction lineage;
- derived voice transcript;
- concept-exposure logging.

### E004 — Receptivity and Mode

Question:

> Does explicit mode selection improve fit?

Possible later comparison:

- user-selected mode;
- default;
- Liquid-selected mode.

### E005 — Replay

Question:

> Does processing the same source through multiple processors/models improve trust or insight enough to justify first-class comparison?

### E006 — Manual Subscription Bridge

Question:

> Is human-mediated use of strong subscription models sufficiently valuable relative to transport friction?

### E007 — Blind Solid

Question:

> Can Solid infer a bounded active state from observable evidence without seeing the user's private ground-truth card?

Later gate.

## New candidate experiments

### E008 — Concept Lens / Professional Vision

Question: Does source-backed expert vocabulary merely rename what the user already notices, create new useful distinctions, improve later perception, or constrain attention around LET's labels?

Conditions:

- Blind reflection → concept reveal;
- Concept Lens before activity → reflection;
- ordinary Free Capture.

Good first domains: piano, COD, movies.

### E009 — Blind Echo / Resonance Drift

Question: How does current memory/interpretation differ from an earlier contemporaneous reflection?

Protocol:

1. hide original;
2. record delayed reflection;
3. freeze;
4. reveal original;
5. compare;
6. Liquid asks one temporal-change question.

Best first domain: movies.

### E010 — Liquid Question Ladder

Question: Is one coherent sequence of differently functioning questions better than independent perturbations?

Candidate sequence:

```text
SPECIFY → EXPLAIN → CONTRAST → PREDICT
```

Stop at any point.

Measure marginal novelty and annoyance.

### E011 — Research Pull

Question: Can external research convert an intuitive but poorly named problem into useful expert knowledge?

Output:

- candidate concepts;
- distinctions;
- primary sources;
- uncertainty;
- one next observation or experiment.

### E012 — Piano Practice Microanalysis

Question: Does a lightweight forethought → performance → reflection protocol make practice more intentional without interrupting flow?

Compare:

- Free Capture;
- Prediction + AAR;
- Concept Lens.

### E013 — COD Game-Intelligence Decomposition

Question: When a strong mechanical player reflects on deaths/wins, does separating mechanics, perception, knowledge, decision, tempo, and psychological state reveal useful non-mechanical bottlenecks?

Important: do not assume poor performance. The point is richer representation.

### E014 — Retrospective Legacy Capture

Question: Is it useful to intentionally capture current reconstructions of important pre-LET experiences?

Examples:

- old movies;
- past projects;
- major learning experiences;
- memories of becoming good at a skill.

Evaluate value, not historical accuracy alone.

### E015 — Rewatch Triad

Question: What changes across original reaction, pre-rewatch memory, and post-rewatch reaction?

Potential value:

- taste development;
- memory reconstruction;
- changes in interpretive vocabulary.

### E016 — Objective-Media Debrief

Question: Does reviewing objective media after self-assessment produce useful discrepancies?

Possible media:

- piano recording;
- gameplay clip;
- code diff/test;
- screen recording when justified.

Do not show objective media before self-assessment when calibration is the target.

### E017 — Cross-Domain Concept Transfer

Question: Do concepts learned in one domain legitimately improve reasoning in another?

Examples:

- tempo;
- initiative;
- positioning;
- feedback;
- invariant;
- attention;
- information advantage.

Important: distinguish productive analogy from forced metaphor.

### E018 — Joy-Preserving Intervention

Question: Can LET learn when **not** to intervene?

Compare:

- question;
- optional question notice;
- silence.

Primary outcome:

- desire to continue activity;
- subjective fit;
- whether silence was retrospectively preferred.

### E019 — Reflection Timing

Question: What differs between immediate, 20-minute, next-day, and one-week reflection?

Best first domain: movies.

This is not only about accuracy; it is about different cognitive products.

### E020 — Protocol Personalization

Question: Which Protocols naturally fit which domain, context, and receptivity state?

Later aim:

```text
P(desired protocol | scene, thread, prior behavior)
```

### E021 — Concept Teach-Back

Question: Does being able to explain a concept in one's own words and generate a personal example predict whether the concept actually becomes useful?

### E022 — Vocabulary Priming Contamination

Question: How strongly does showing a concept palette before reflection alter what the user reports noticing?

This is the experimental reason to maintain Blind and Lens conditions.

### E023 — Thread Trajectory Summary

Question: Can LET summarize change across a Thread without flattening conflicting episodes into a false stable identity?

Required output:

- changed;
- stable;
- unknown;
- conflicting;
- new vocabulary;
- intervention history.

### E024 — Incremental Sensor Value

Question: For a specific unanswered question, how much new useful inference does a passive/automatic sensor add beyond intentional reflection?

Sensors should enter only under a declared hypothesis.

### E025 — Solid State Fidelity

Question: Can Solid accurately estimate current goal, mode, uncertainty, likely next action, and relevant context?

Use blind ground-truth comparison.

### E026 — S3 Contamination Detection

Question: Can LET identify patterns that may have been caused by its own interventions rather than treating them as independent observations?

### E027 — Venom / Self-Fulfilling Model Test

Question: Does showing the user an inferred trait or preference cause later behavior to align with that label?

Strong guardrails required.

### E028 — Solidus Commitment Drift

Question: Can a ratified commitment remain contextual and revisable rather than hardening into doctrine?

Very late-stage experiment.

---

# 9. Research and evidence principles

## 9.1 Labels can aid category/expertise learning

Research supports the idea that labels can make categories easier to learn and can help train perceptual discrimination.

Relevant sources:

- Lupyan, Rakison, & McClelland (2007), *Language is not just for talking: redundant labels facilitate learning of novel categories*. Psychological Science. DOI: `10.1111/j.1467-9280.2007.02028.x`. PMID: `18031415`.
- Scott et al. (2008), *The role of category learning in the acquisition and retention of perceptual expertise*. Brain Research. DOI: `10.1016/j.brainres.2008.02.054`. PMID: `18417106`.
- Searston & Tangen (2017), *Training perceptual experts: Feedback, labels, and contrasts*. Canadian Journal of Experimental Psychology. DOI: `10.1037/cep0000124`. PMID: `28252995`.

### LET implication

Vocabulary is not merely metadata.

It may alter what becomes perceptually/cognitively salient.

Therefore:

> **Record when the label was introduced.**

## 9.2 Structured debriefing is a credible model for post-performance reflection

Relevant sources:

- Tannenbaum & Cerasoli (2013), *Do team and individual debriefs enhance performance? A meta-analysis.* Human Factors. DOI: `10.1177/0018720812448394`. PMID: `23516804`.
- Keiser & Arthur (2021), *A meta-analysis of the effectiveness of the after-action review (or debrief) and factors that influence its effectiveness.* Journal of Applied Psychology. DOI: `10.1037/apl0000821`. PMID: `32852990`.

The later meta-analysis highlights alignment to the individual/task and objective review media as important moderators.

### LET implication

After-Action Review and objective-media comparison are good protocol families, but should be aligned to the actual activity.

## 9.3 Autobiographical memory is reconstructive and can change through retrieval

Relevant sources:

- *Memory Reconsolidation* review. PMID: `27885549`.
- *Does reactivation trigger episodic memory change? A meta-analysis.* DOI: `10.1016/j.nlm.2016.12.012`. PMID: `28025069`.
- Fivush & Grysman (2022), *Accuracy and reconstruction in autobiographical memory*. DOI: `10.1002/wcs.1620`. PMID: `36125799`.
- Elsey, Van Ast, & Kindt (2018), *Human memory reconsolidation: A guiding framework and critical review of the evidence.* DOI: `10.1037/bul0000152`. PMID: `29792441`.

### LET implication

Do not treat repeated reflections as repeated measurements of a fixed object.

They are new cognitive events.

Blind Echo should freeze current reconstruction before showing prior evidence.

Use cautious language around neurobiological "reconsolidation"; LET can safely study **change in reported memory/meaning** without claiming a specific neural mechanism.

## 9.4 Music practice has a strong self-regulation/metacognition tradition

Relevant sources:

- Biasutti & Concina (2019), *The Role of Metacognitive Skills in Music Learning and Performing*. DOI: `10.3389/fpsyg.2019.01583`. PMID: `31354586`.
- de Araújo et al. (2024), *Metacognition in musical practices: two studies with beginner and expert Brazilian musicians.* DOI: `10.3389/fpsyg.2024.1331988`. PMID: `38455117`.
- *Using a music microanalysis protocol to enhance instrumental practice* (2024). DOI: `10.3389/fpsyg.2024.1368074`. PMID: `38629042`.
- *Focus of attention in musical learning and music performance: a systematic review* (2024). DOI: `10.3389/fpsyg.2024.1290596`. PMID: `38650905`.

### LET implication

Piano is an excellent domain for structured forethought → performance → reflection cycles.

Do not assume one attentional focus strategy is universally superior.

---

# 10. Development inventory — near-term

The following may be developed quickly, potentially in parallel branches. They do not all need to become active field experiments immediately.

## Data/model

- append-only Prediction model;
- temporal source-mode fields;
- Thread entity and episode-thread links;
- Reflection entity;
- Protocol definition and ProtocolRun;
- Concept entity with stable IDs/provenance;
- Lens exposure log;
- comparison artifact;
- research-source artifact;
- explicit `implementation_status` vs `field_status`.

## Product/UI

- create/link Thread from Episode;
- Thread detail timeline;
- select Protocol at capture or after capture;
- Free Capture remains one-click default;
- Blind visibility gate;
- Concept Lens selection;
- "Teach me the language for this" action;
- "Compare with earlier reflection" action;
- "Reflect again without showing me the old one" action;
- "Research this" export/bridge action;
- protocol progress UI that is optional and dismissible;
- compare two Episodes side-by-side;
- show concept definition + source + examples;
- convert a Liquid question into a Thread.

## Developer multiplier

- configuration-driven protocol registry;
- protocol test harness;
- synthetic Thread fixtures;
- experiment-condition fixtures;
- source-backed Concept Library format;
- import/export for protocol definitions;
- deterministic protocol runner;
- one command to replay a Protocol over historical fixtures;
- documentation generator for protocol catalog.

---

# 11. Medium-term development inventory

- Thread trajectory summaries;
- side-by-side audio/transcript playback;
- transcript/interpretation diff;
- comparison of old vs current language;
- delayed-reflection scheduling (manual trigger first; automation later);
- approximate-date UX for legacy memories;
- external evidence attachment to retrospective memories;
- research artifact browser;
- concept-neighbor explorer;
- concept acceptance/rejection history;
- cross-domain concept aliases;
- per-Thread unknown/question register;
- "what changed?" longitudinal view;
- "what have I stopped mentioning?" view;
- model/prompt replay comparison;
- Protocol authoring interface;
- experiment assignment/condition logging;
- optional randomization support;
- structured human feedback on Protocol utility;
- export Thread as Markdown packet;
- import old notes/reviews/transcripts as historical Episodes.

---

# 12. Sensor and integration inventory

Sensors are **candidate capabilities**, not automatic roadmap commitments.

Each should be pulled in by a question.

## Plex

Potential value:

- movie start/end;
- first watch vs rewatch;
- title metadata;
- exact viewing date;
- historical watch records.

Potential experiment:

> Does automatically knowing rewatch/history make Blind Echo and Resonance Drift materially better?

## Git

Potential value:

- programming episode boundaries;
- objective code changes;
- compare self-assessment to actual diff;
- agent/human contribution context.

Do not duplicate the professional knowledge base.

## ActivityWatch

Potential value:

- interruption patterns;
- active app/window context;
- resumption experiments.

Only integrate if an actual cognitive question needs it.

## screenpipe

Potential value:

- bounded screen-context evidence;
- reconstruct what was visible;
- programming/gaming workflow analysis.

Avoid total-life capture merely because it is available.

## Piano media

Candidate inputs:

- audio;
- video;
- MIDI.

Use only when a question requires objective performance evidence.

## Gameplay

Candidate inputs:

- existing recorded clips;
- MARK timestamps;
- match metadata;
- later structured telemetry when accessible.

Import video before building custom capture.

## Phone

Future use:

- mobile capture;
- photo/image episodes;
- in-the-world thoughts;
- location/event context when explicitly useful.

Browser-first remains reasonable until phone friction becomes real.

---

# 13. Long-term systems

These should be documented now so the architecture does not make them impossible, but they should not be treated as current deliverables.

## 13.1 Mammal Pod

The shared evolving cognitive model/evidence substrate.

Contains:

- evidence;
- state estimates;
- Thread trajectories;
- concept familiarity;
- uncertainty;
- intervention history;
- contradictions.

Not a claim of identity.

## 13.2 Solid

Role:

> Descriptive/predictive mirror.

Questions:

- What is the user doing?
- What appears salient?
- What is the current mental model?
- What is uncertain?
- What is likely next?
- What support is likely wanted?

Requirements:

- evidence;
- scope;
- confidence;
- conflicting evidence;
- contestability.

## 13.3 Liquid

Role:

> Productive perturbation.

Future capabilities:

- select cognitive stance;
- choose whether to ask;
- generate alternatives;
- introduce vocabulary;
- challenge evidence;
- run question ladders;
- surface research;
- know when silence is superior.

Liquid should learn a **policy of intervention**, not merely become a larger chatbot.

## 13.4 Solidus

Role:

> Ratified commitment / chosen-policy perspective.

Questions:

- What has the user deliberately committed to?
- Does the current behavior support that commitment?
- Has the commitment changed?
- Is the old interpretation still valid?

Never turn values into doctrine.

## 13.5 Sleep / Offline Consolidation

A future "subconscious" pass can process recent Episodes without interrupting the user.

Possible outputs:

- repeated pattern;
- contradiction;
- forgotten open loop;
- unexpected cross-domain connection;
- concept that now has several user examples;
- Thread worth revisiting;
- stale assumption.

Surface only a small candidate set.

## 13.6 Cross-domain transfer model

Study whether representations transfer:

```text
tempo
initiative
positioning
feedback
invariant
attention
information advantage
prediction
```

Do not assume metaphor is equivalence.

## 13.7 Memory buoyancy / active forgetting

As the archive becomes large, LET should not treat everything as equally salient.

Future retrieval priority can depend on:

- current Thread relevance;
- recency;
- unresolved status;
- contradiction;
- user revisit;
- predicted usefulness.

Reduce retrieval priority rather than deleting history.

## 13.8 Counterfactual Twin

Later, ask:

> What might happen if I change this practice strategy / decision / attention pattern?

This requires much more evidence than ordinary Liquid questioning.

Do not build early.

## 13.9 Bounded agency

Very late-stage.

Possible actions:

- prepare a note;
- prepare a comparison;
- create a practice plan draft;
- surface a relevant source;
- prepare a project resumption packet.

Actions affecting external systems require separate authorization.

---

# 14. Suggested long-term data relationships

Conceptual model:

```text
Person
 │
 ├── Threads
 │    └── EpisodeThread links
 │
 ├── Episodes
 │    ├── Artifacts
 │    ├── Events
 │    ├── Reflections
 │    ├── Predictions
 │    ├── ProtocolRuns
 │    ├── LensExposures
 │    ├── Interventions
 │    └── Feedback
 │
 ├── Concepts
 │    ├── Sources
 │    ├── UserExamples
 │    └── ConceptExposure
 │
 ├── ResearchArtifacts
 │
 ├── Comparisons
 │
 └── TwinSnapshots
```

Do not implement the full schema at once.

This is a compatibility target.

---

# 15. Status taxonomy

Every future feature or research object should carry distinct status concepts.

## Software

- proposed
- implementing
- implemented
- retired

## Field

- unused
- collecting
- promising
- mixed
- not_useful
- harmful_or_intrusive

## Evidence/gate

- not_tested
- baseline_only
- preliminary
- replicated_within_person
- gate_passed
- gate_failed

This prevents:

> "code exists"

from silently becoming:

> "system works."

---

# 16. Development sequencing philosophy

A reasonable next sequence is:

## Phase A — Correct experimental integrity

- append-only predictions;
- prediction transcript lineage;
- prediction capture atomicity;
- concept IDs/provenance;
- exposure logging;
- temporal source modes.

## Phase B — Build the improvement layer

- Threads;
- Protocol registry;
- ProtocolRuns;
- Blind vs Lens;
- Concept Library;
- comparisons;
- Research Pull.

## Phase C — Run richer field experiments

Prioritize:

- Concept Lens;
- Blind Echo;
- Question Ladder;
- Research Pull;
- domain microanalysis.

Again:

> This sequence is a dependency map, not a speed limit.

If multiple pieces are cheap to build correctly, prototype them behind inactive Protocols or feature flags.

---

# 17. Branch/worktree strategy

Candidate parallel branches:

```text
fix/prediction-lineage
feat/thread-model
feat/protocol-registry
feat/concept-library
feat/longitudinal-compare
experiment/concept-lens
experiment/blind-echo
experiment/question-ladder
experiment/research-pull
```

Parallelize:

- isolated schema/design exploration;
- protocol fixtures;
- UI prototypes;
- research;
- concept sourcing;
- tests.

Serialize:

- live database migrations;
- canonical Episode semantics;
- intervention policy changes;
- merges touching the same provenance model.

---

# 18. Required documentation updates in the existing repository

When adopting this roadmap, reconcile rather than merely append.

## `README.md`

Update current status from planning baseline to active field/research instrument.

Add:

- stable substrate;
- new improvement layer;
- Thread/Protocol direction;
- implementation vs validation distinction.

## `docs/02_PRODUCT_EXPERIENCE_AND_USER_FLOWS.md`

Add:

- Protocol selection;
- Blind vs Lens;
- Thread revisit flows;
- retrospective/rewatch flows;
- Research Pull.

## `docs/03_TECHNICAL_ARCHITECTURE.md`

Add conceptual future interfaces for:

- Thread;
- Protocol;
- ProtocolRun;
- Concept Library;
- Lens exposure;
- comparisons.

Do not claim implementation before it exists.

## `docs/04_DATA_AND_EPISTEMIC_MODEL.md`

Add:

- append-only Prediction;
- Reflection;
- Thread;
- ProtocolRun;
- Concept;
- LensExposure;
- retrospective temporal fields;
- visibility condition.

## `docs/05_EXPERIMENT_PROGRAM_AND_GATES.md`

Add:

- backlog vs active experiment distinction;
- E008+ candidate experiment catalog;
- priming contamination;
- Blind Echo;
- Protocol experiments.

## `docs/06_INITIAL_TWO_WEEK_FIELD_PROGRAM.md`

Keep as historical field-program record or rename status accordingly.

Do not continuously rewrite it into the entire future roadmap.

A new ongoing field/research program doc should take over.

## `docs/09_DECISIONS_AND_OPEN_QUESTIONS.md`

Record new proposed decisions after implementation/review:

- append-only prediction lineage;
- Thread;
- Protocol separate from Mode;
- concept provenance;
- Blind/Lens exposure;
- development backlog vs experimental concurrency.

## `AGENTS.md`

Add rules:

- never expose a Lens before a Blind step unless Protocol says so;
- concept definitions require provenance before being treated as expert knowledge;
- historical reconstruction is not contemporaneous evidence;
- prediction revisions append rather than overwrite;
- implemented is not validated;
- development may be broad, but experiments must remain distinguishable.

## compiled packet

Generate from source or explicitly mark non-authoritative.

---

# 19. Proposed new decisions

These are candidates for the project's formal decision register.

## LET-D-025 — Prediction History Is Append-Only

A pre-session prediction may be corrected only by appending a superseding record. Original content remains recoverable.

## LET-D-026 — Thread Is the Longitudinal Organizing Unit

Episodes remain bounded events; Threads connect meaningful subjects/skills/questions across time.

## LET-D-027 — Protocol and Mode Are Orthogonal

Protocol defines the cognitive procedure; Mode defines Liquid's stance.

## LET-D-028 — Vocabulary Exposure Is an Intervention

Showing a concept or expert label must be recordable because it may alter subsequent attention/categorization.

## LET-D-029 — Concept Knowledge Requires Provenance

Hard-coded or model-generated vocabulary begins as proposed knowledge, not canonical expertise.

## LET-D-030 — Blind Reflection Is a First-Class Condition

When an experiment concerns natural noticing, memory drift, or calibration, prior evidence/concepts remain hidden until the blind artifact is frozen.

## LET-D-031 — Development Breadth Is Not Experimental Concurrency

The project may maintain or prototype a broad backlog while restricting simultaneous active interventions for causal clarity.

## LET-D-032 — Retrospective Reconstruction Is Valuable but Epistemically Distinct

Current memories of older events may be stored, linked, compared, and studied without being represented as contemporaneous records.

---

# 20. The core project question after this update

The early LET question was:

> Can we capture lived evidence cheaply enough to build a cognitive twin?

The emerging question is richer:

> **Can LET create a durable longitudinal environment in which a person can preserve experience, acquire better representations for what they notice, compare themselves across time, encounter carefully chosen cognitive perturbations, and learn when artificial support deepens cognition versus when it should remain silent?**

If this succeeds, the future Twin is not built from a pile of diary entries.

It is built from:

```text
experience
+ memory
+ change through time
+ predictions
+ vocabulary acquisition
+ evidence comparisons
+ interventions
+ corrections
+ chosen commitments
+ explicit uncertainty
```

That is a substantially stronger foundation for Solid, Liquid, Solidus, and the Mammal Pod.

---

# 21. Immediate practical recommendation

Continue using LET normally.

Do not wait for this roadmap to be fully implemented before capturing.

In parallel:

1. fix prediction lineage/integrity;
2. implement Thread;
3. implement a small Protocol Registry;
4. build Blind Echo and Concept Lens as the first new configurable Protocols;
5. begin source-backed concept work for piano and COD;
6. add Research Pull;
7. run only a small subset as deliberate experiments at any given time;
8. let actual Episodes determine which parts deserve deeper engineering.

> **Use provides the evidence. Development creates cheaper ways to ask the next question.**
