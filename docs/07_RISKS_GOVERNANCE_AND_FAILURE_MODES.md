---
title: "Risks, Governance, and Failure Modes"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


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
