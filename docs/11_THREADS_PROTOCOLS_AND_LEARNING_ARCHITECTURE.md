---
title: "LET — Threads, Protocols, Lenses, and Longitudinal Learning Architecture"
project: "Les Enfants Terribles"
status: "proposed_design"
version: "0.1-draft"
source_commit: "550422eaac46ed244fa73c8e68911612c9fb35f8"
prepared: "2026-08-15"
---

# Threads, Protocols, Lenses, and Longitudinal Learning Architecture

## 1. Why this document exists

The first LET architecture was optimized around **Episodes**:

> capture one meaningful moment and preserve its provenance.

Actual use now exposes a second need:

> preserve the relationship among moments, and structure different ways of thinking about them.

This document defines a proposed semantic layer above the existing Episode/artifact substrate.

It is deliberately designed so that most cognitive experiments can be implemented as configuration and data rather than repeated Flask/database rewrites.

---

# 2. The orthogonal dimensions

Avoid collapsing several distinct concerns into one `mode` field.

A future LET encounter can be described by:

```text
DOMAIN
What kind of activity is this?
movie / piano / cod / research / programming / general

THREAD
What persistent thing is this about?
Alien / Chopin Nocturne / centering / latent recurrence

EPISODE
What bounded event happened now?
post-watch reflection / practice block / match session

PROTOCOL
What thinking procedure are we running?
Free Capture / Blind Echo / Calibration / Research Pull

MODE
How should Liquid behave?
capture / explore / challenge / understand / improve / surprise / decide

LENS
What conceptual frame has been deliberately exposed?
centering / rubato / diegetic sound / state invariant

EVIDENCE
What information is available?
raw voice / prior episode / video / paper / Git diff

INTERVENTION
What did LET introduce?
question / concept / contradiction / evidence / silence

REFLECTION
What did the user produce?
prediction / immediate account / delayed recall / post-evidence revision
```

Each dimension should be independently inspectable.

---

# 3. Thread specification

## 3.1 Minimal entity

```yaml
Thread:
  id:
  title:
  thread_type:
  description:
  status: active | dormant | closed
  created_at:
  updated_at:
```

## 3.2 Episode association

Prefer many-to-many compatibility:

```yaml
EpisodeThread:
  episode_id:
  thread_id:
  role: primary | related | evidence_for | generated_from
  created_at:
```

First UI may expose only one primary Thread to keep friction low.

## 3.3 Thread should not be an identity claim

Poor:

> Thread: Jonathan hates sentimental endings

Better:

> Thread: Sentimentality / emotional closure in film

The Thread is a question/object of attention.

Solid may later infer a pattern over it, but the container itself should not bake in the conclusion.

---

# 4. Protocol specification

## 4.1 Protocol definition

```yaml
Protocol:
  id:
  version:
  title:
  purpose:
  eligible_domains:
  eligibility:
  steps:
  completion_policy:
  outputs:
  experimental_notes:
```

## 4.2 Step types

Candidate primitives:

- `capture`
- `prompt`
- `prediction`
- `freeze`
- `reveal_artifact`
- `select_lens`
- `research_pull`
- `liquid_question`
- `compare`
- `rating`
- `teach_back`
- `mark`
- `branch`
- `stop`

The implementation should begin with a much smaller subset.

## 4.3 Visibility controls

Protocol design needs explicit information barriers.

Example:

```yaml
visibility:
  prior_episode: hidden_until: reveal
  concept_palette: hidden
  objective_evidence: hidden_until: self_assessment_frozen
```

This is not cosmetic.

Information visibility changes cognition.

---

# 5. ProtocolRun

A Protocol is reusable design.

A ProtocolRun is one actual execution.

```yaml
ProtocolRun:
  id:
  protocol_id:
  protocol_version:
  episode_id:
  thread_id:
  started_at:
  completed_at:
  status:
  current_step:
  condition:
  metadata:
```

Associated events should capture:

- which step was entered;
- what the user saw;
- what was hidden;
- what was skipped;
- what was abandoned;
- which Lens was shown;
- which intervention was answered.

A partially completed protocol is valid data.

Do not create "reflection debt."

---

# 6. Reflection model

Recommended conceptual entity:

```yaml
Reflection:
  id:
  episode_id:
  thread_id:
  protocol_run_id:
  phase:
  artifact_id:
  authored_by:
  visibility_state:
  created_at:
```

Candidate phases:

- `pre_session`
- `immediate`
- `prompted`
- `delayed`
- `blind_recall`
- `post_reveal`
- `post_evidence`
- `post_research`
- `rewatch`
- `retrospective_reconstruction`
- `creative_synthesis`

This makes temporal comparisons far easier than inferring phase from file order.

---

# 7. Prediction model

Predictions need stronger lineage than the current Episode JSON.

Proposed:

```yaml
Prediction:
  id:
  episode_id:
  thread_id:
  statement_text:
  statement_artifact_id:
  transcript_artifact_id:
  target_concept_id:
  confidence:
  created_at:
  supersedes_id:
  locked_at:
```

Rules:

1. append-only;
2. raw voice is source;
3. transcript is derived;
4. a correction is another Prediction;
5. post-session changes are not Predictions—they are Reflections.

---

# 8. Concept / Lens model

## Concept

```yaml
Concept:
  id: cod.centering
  term: Centering
  domain: cod
  definition:
  aliases:
  scope:
  confidence:
  status:
  version:
```

## ConceptSource

```yaml
ConceptSource:
  concept_id:
  source_type:
  citation:
  excerpt_or_note:
  accessed_at:
  confidence:
```

## ConceptExposure

```yaml
ConceptExposure:
  id:
  concept_id:
  episode_id:
  protocol_run_id:
  exposed_at:
  phase:
  user_requested:
  presentation:
```

Possible phases:

- `before_activity`
- `before_reflection`
- `after_blind_reflection`
- `after_evidence`
- `research_pull`

This is necessary to distinguish learning from priming.

---

# 9. Compare object

A Compare operation can create a derived comparison artifact.

```yaml
Comparison:
  id:
  thread_id:
  episode_ids:
  comparison_type:
  processor:
  created_at:
  artifact_id:
```

Candidate types:

- immediate_vs_delayed;
- prediction_vs_reflection;
- reflection_vs_objective_media;
- blind_vs_lens;
- pre_rewatch_vs_post_rewatch;
- before_research_vs_after_research;
- model_A_vs_model_B.

The generated comparison should preserve contradictions rather than produce a single "current truth."

---

# 10. Research Pull architecture

A Research Pull is a processor/protocol hybrid.

Input:

- Episode/Thread context;
- user's current terminology;
- explicit unknown/question.

Output:

```yaml
ResearchArtifact:
  question:
  sources:
  candidate_concepts:
  findings:
  disagreements:
  confidence:
  application_hypotheses:
  suggested_next_observation:
```

Rules:

- prefer primary sources;
- separate established findings from analogy;
- do not silently add source-backed concepts to the canonical Concept Library;
- allow user acceptance/rejection;
- record model/search provenance.

Manual ChatGPT/Claude/Antigravity workflow is acceptable.

API automation is optional later.

---

# 11. Blind vs Lens as a system-level distinction

## Blind

Use when the goal is to measure:

- natural noticing;
- unprompted vocabulary;
- current recall;
- spontaneous self-assessment.

Example:

```text
watch film
   ↓
free reflection
   ↓
FREEZE
   ↓
show concepts / old review / criticism
```

## Lens

Use when the goal is to train:

- attention;
- discrimination;
- domain vocabulary;
- intentional practice.

Example:

```text
review "centering"
   ↓
play match
   ↓
reflect specifically on centering
```

Neither is superior.

The project needs both.

---

# 12. Longitudinal temporal semantics

For every relevant object distinguish:

```text
occurred_at
recorded_at
created_at
```

For retrospective records add:

```text
estimated_occurred_at
date_precision
source_mode
```

Example:

```yaml
source_mode: retrospective_reconstruction
estimated_occurred_at: 1997
date_precision: year
recorded_at: 2026-08-15T...
```

Never manufacture a precise date merely to fit a database column.

---

# 13. Example end-to-end flows

## Movie — immediate → Blind Echo → rewatch

```text
THREAD: The Shining
│
├── EP1
│   protocol: Free Capture
│   phase: immediate
│
├── EP2 (one month later)
│   protocol: Blind Echo
│   old EP1 hidden
│   current recall frozen
│   EP1 revealed
│   compare artifact created
│
└── EP3
    pre-rewatch prediction
    rewatch
    post-rewatch reflection
    compare EP1 / EP2 / EP3
```

## Piano — concept acquisition

```text
THREAD: Chopin — left-hand transition
│
├── EP1 Blind practice reflection
│      "I miss the landing when I move across the keyboard."
│
├── Research Pull
│      candidate concepts:
│      anticipatory gaze
│      tactile landmark
│      lateral forearm transport
│
├── EP2 Concept Lens
│      lens exposed before practice
│
└── Teach-Back
       which concept actually matched?
```

## COD — mechanics vs game intelligence

```text
THREAD: Re-challenging fights
│
├── EP1 end-session blind reflection
│
├── Concept suggestion
│      ego-chall / information disadvantage / health disadvantage
│
├── EP2 Lens session
│
├── optional gameplay clip
│
└── Objective-Media AAR
```

---

# 14. UI principles

1. **Free Capture is always available.**
2. Protocols should never be mandatory.
3. Protocol step count should be visible but not guilt-inducing.
4. Abandoning a Protocol is legitimate.
5. Blind state must be trustworthy—do not leak hidden information.
6. The system should explain why it is hiding something.
7. Concept cards should show scope/source.
8. A Thread should make revisiting easy, not create categorization work.
9. Most links should be created after capture if classification would slow capture.
10. The user can always say "just let me ramble."

---

# 15. Migration philosophy

Do not force all historical Episodes into Threads.

Allow:

- unthreaded Episodes;
- automatic Thread suggestions;
- human linking;
- later merge/split of Threads.

Raw artifacts and Episode IDs must not change when Thread organization changes.

Protocol history should also survive Protocol definition updates through versioning.

---

# 16. What this architecture enables later

Without changing the meaning of old data, this model can later support:

- Solid state estimates;
- Thread trajectory modeling;
- concept familiarity modeling;
- preference drift;
- memory drift;
- Liquid policy learning;
- sensor-enriched comparison;
- cross-domain transfer;
- Solidus commitments;
- offline consolidation;
- bounded agency.

The reason to build Threads/Protocols/Lenses carefully is not because all future systems need to be implemented now.

It is because these objects preserve **which human experienced what information, under what cognitive procedure, at what point in time**.

That is the substrate a trustworthy cognitive twin eventually needs.
