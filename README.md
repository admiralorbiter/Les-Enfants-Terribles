---
title: "Les Enfants Terribles — Longitudinal Reflection and Cognitive Laboratory"
project: "Les Enfants Terribles"
project_code: "LET"
status: "active_research_instrument"
version: "0.2"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-15"
---


# Les Enfants Terribles

> *"Building the future and keeping the past alive are one and the same thing."*
> — **Solid Snake**, *Metal Gear Solid 2: Sons of Liberty*

**Les Enfants Terribles (LET)** is a personal research-and-development project for building an artificial cognitive environment around one living person.

The immediate product is not a clone, autonomous assistant, productivity score, or total-life surveillance system. The immediate product is a low-friction, replayable longitudinal environment that can:

1. preserve episodes of lived experience with cryptographic provenance;
2. structure reflection through configurable cognitive procedures (**Protocols**);
3. connect persistent objects of inquiry across time (**Threads**);
4. acquire domain-specific representations and conceptual frameworks (**Lenses**);
5. accumulate empirical evidence for an inspectable, revisable cognitive model;
6. protect enjoyment, autonomy, and the distinction between the person and the model.

> **Core question:** Can an AI learn when and how to augment this particular human’s cognition—while remaining explicitly uncertain, preserving the original evidence, and avoiding the replacement of life with optimization?

## Current status

The project has advanced from a planning baseline into an **active research instrument**. 

The foundation capture substrate (Slices 0 through 2D) is operational: desktop voice recording, immutable raw artifact storage, asynchronous local transcription (`faster-whisper`), manual Mission Brief AI bridges, interactive perturbation follow-ups, offline heuristics, pre-session predictions, and vocabulary scaffolding are functional with 55/55 automated tests passing. 

The project is now entering its longitudinal learning phase: hardening prediction integrity (Workstream A), implementing persistent Threads (Workstream B), building a configurable Protocol laboratory (Workstream C), and introducing source-backed Concept Libraries (Workstream D).

## The first principle

> **The raw experience is irreplaceable; every interpretation is replaceable.**

A voice recording, gameplay clip, piano recording, spontaneous thought, or first reaction to a film can only be captured once. Transcripts, summaries, inferences, questions, and twin models can be recomputed later.

## Architectural layers

```text
┌─────────────────────────────────────────────────────────────┐
│                       FUTURE TWIN LAYER                     │
│    Solid State Estimator · Liquid Policy · Solidus Values   │
│             Mammal Pod · Counterfactual Simulation          │
└──────────────────────────────▲──────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────┐
│                LONGITUDINAL SEMANTIC LAYER                  │
│       Threads (Persistent Attention) · Protocols (Runs)      │
│      Source-Backed Concept Library · Lens Exposure Logs     │
│        Append-Only Predictions · Longitudinal Compare       │
└──────────────────────────────▲──────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────┐
│                  STABLE CAPTURE SUBSTRATE                   │
│      Desktop Browser Audio / Media Capture · SQLite DB      │
│     Immutable Raw Files · Derivations · Replay Engine       │
└─────────────────────────────────────────────────────────────┘
```

## Documentation map

| Document | Purpose |
|---|---|
| [Project Charter](docs/00_PROJECT_CHARTER.md) | Mission, scope, success, anti-goals, and operating principles |
| [Metal Gear Cognitive Model](docs/01_METAL_GEAR_COGNITIVE_MODEL.md) | Conceptual framing, GENE/MEME/SCENE/SENSE, clones, and named failure modes |
| [Product Experience and User Flows](docs/02_PRODUCT_EXPERIENCE_AND_USER_FLOWS.md) | How LET feels across movies, piano, COD, research, and programming |
| [Technical Architecture](docs/03_TECHNICAL_ARCHITECTURE.md) | Desktop-first stack, storage, processors, replay, manual AI bridge, and reliability |
| [Data and Epistemic Model](docs/04_DATA_AND_EPISTEMIC_MODEL.md) | Episodes, Threads, Protocols, artifacts, claims, interventions, and provenance |
| [Experiment Program and Gates](docs/05_EXPERIMENT_PROGRAM_AND_GATES.md) | How evidence—not code completion—controls advancement |
| [Initial Two-Week Field Program](docs/06_INITIAL_TWO_WEEK_FIELD_PROGRAM.md) | Historical foundation record and initial field slices (Slices 0–2D) |
| [Risks, Governance, and Failure Modes](docs/07_RISKS_GOVERNANCE_AND_FAILURE_MODES.md) | Human, epistemic, technical, and Metal Gear-named risks |
| [Research Map and Related Systems](docs/08_RESEARCH_MAP_AND_RELATED_SYSTEMS.md) | Research basis, adjacent cognitive architectures, and what to borrow |
| [Decisions and Open Questions](docs/09_DECISIONS_AND_OPEN_QUESTIONS.md) | Formal decision register (LET-D-001 to LET-D-032) and open questions |
| [Integrated Development Roadmap](docs/10_INTEGRATED_DEVELOPMENT_ROADMAP.md) | 21-section comprehensive development roadmap and experimental program |
| [Threads, Protocols, and Lenses](docs/11_THREADS_PROTOCOLS_AND_LEARNING_ARCHITECTURE.md) | Deep technical specification of the longitudinal semantic architecture |
| [Agent Rules](AGENTS.md) | Scope, epistemic integrity, and development rules for coding and research agents |
| [Episode Template](templates/episode-record.md) | Inspectable episode record |
| [Experiment Template](templates/experiment-record.md) | Small experimental protocol and decision record |
| [Processor Template](templates/processor-card.md) | Versioned processor definition and evaluation card |

A single-file export packet is preserved as [`LES_ENFANTS_TERRIBLES_PLANNING_PACKET.md`](LES_ENFANTS_TERRIBLES_PLANNING_PACKET.md) (non-authoritative).

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
