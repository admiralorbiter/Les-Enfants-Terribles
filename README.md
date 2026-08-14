---
title: "Les Enfants Terribles — Project Planning Kit"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


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
