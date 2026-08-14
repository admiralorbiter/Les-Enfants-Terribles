---
title: "Metal Gear Cognitive Model"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


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

