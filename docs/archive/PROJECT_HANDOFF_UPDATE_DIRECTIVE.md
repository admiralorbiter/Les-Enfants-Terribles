---
title: "LET Project Handoff — Roadmap Reconciliation Directive"
project: "Les Enfants Terribles"
status: "agent_handoff"
source_commit: "550422eaac46ed244fa73c8e68911612c9fb35f8"
prepared: "2026-08-15"
---

# LET Project Handoff — Roadmap Reconciliation Directive

## Mission

Use the accompanying roadmap documents to update the Les Enfants Terribles project from the initial capture-first plan into its next phase:

> **a longitudinal reflection and learning laboratory built on top of the now-usable capture substrate.**

Do not treat this handoff as an instruction to implement every feature immediately.

Do treat it as an instruction to ensure the project's documentation, decision register, data model direction, and development backlog contain the full set of ideas.

---

# Source context

Current repository head used for this handoff:

```text
550422eaac46ed244fa73c8e68911612c9fb35f8
feat(liquid): implement pre-session prediction, vocabulary scaffolding,
and draft persistence (Slice 2D / E003)
```

The current implementation reports:

- reliable capture/hardening;
- transcription/replay;
- manual Mission Brief bridge;
- interactive Liquid follow-ups;
- ratings/local heuristics;
- pre-session prediction;
- vocabulary scaffolding;
- 55/55 tests passing in the commit record.

The user is actively using LET and reports:

- the capture experience is easy;
- the system is enjoyable to use;
- most real captures so far are movie reactions;
- piano and other domains have also been tested;
- the next need is more structure for what to notice, name, compare, research, and revisit.

---

# Required project changes

## 1. Preserve the stable philosophy

Do not discard:

- raw evidence is irreplaceable;
- derived interpretation is replaceable;
- operational friction should be minimized;
- productive cognitive friction may be valuable;
- joy should not automatically become an optimization target;
- observation and intervention must remain distinguishable;
- recurring API cost should remain zero by default;
- sensors need hypotheses;
- models remain contestable.

## 2. Correct current prediction integrity

Before E003 data is treated as strong calibration evidence:

- make predictions append-only;
- preserve prediction voice transcript as derived artifact rather than mutation;
- make prediction audio registration transactional with the capture bundle;
- preserve corrections as superseding records.

Add tests for:

- prediction cannot be overwritten;
- correction preserves original;
- prediction voice audio and transcript lineage;
- crash during prediction artifact registration;
- historical replay of original prediction.

## 3. Introduce the new semantic layer

Add design/backlog work for:

- `Thread`
- `EpisodeThread`
- `Protocol`
- `ProtocolRun`
- `Reflection`
- `Concept`
- `ConceptSource`
- `ConceptExposure`
- `Lens`
- `Comparison`
- `ResearchArtifact`

Do not implement the whole long-term schema in one migration.

Start with the minimum fields needed for the first Protocol experiments.

## 4. Record these proposed architectural decisions

Review and, if accepted, add:

- LET-D-025 — Prediction History Is Append-Only
- LET-D-026 — Thread Is the Longitudinal Organizing Unit
- LET-D-027 — Protocol and Mode Are Orthogonal
- LET-D-028 — Vocabulary Exposure Is an Intervention
- LET-D-029 — Concept Knowledge Requires Provenance
- LET-D-030 — Blind Reflection Is a First-Class Condition
- LET-D-031 — Development Breadth Is Not Experimental Concurrency
- LET-D-032 — Retrospective Reconstruction Is Valuable but Epistemically Distinct

Do not silently mark them accepted merely because they appear in the roadmap.

Use the project's normal decision procedure.

---

# Documentation reconciliation map

## README

Change the project status to reflect actual use.

The README should explain:

```text
stable capture substrate
      +
longitudinal Thread layer
      +
configurable Protocol layer
      +
future Twin layer
```

## Technical Architecture

Add proposed interfaces and dependencies, clearly marked not-yet-implemented.

## Data and Epistemic Model

Add:

- Prediction history;
- Thread;
- ProtocolRun;
- Reflection phase;
- Concept provenance;
- Lens/Concept exposure;
- retrospective temporal semantics.

## Experiment Program

Add the expanded experiment backlog from the integrated roadmap.

Preserve:

> no more than approximately three **active experiments**

but explicitly state this does not cap development backlog, dormant Protocols, or isolated prototypes.

## Initial Two-Week Field Program

Treat as a historical/initial field-program document.

Do not keep growing it forever.

Create an ongoing development/research roadmap instead.

## Decisions/Open Questions

Close or update questions superseded by real implementation.

Add new questions around:

- Thread UX;
- Protocol format;
- concept sourcing;
- Blind/Lens comparison;
- historical-memory capture;
- Research Pull;
- delayed revisit scheduling.

## AGENTS.md

Add:

1. **Implemented is not validated.**
2. Predictions append; they do not overwrite.
3. A Lens shown before reflection is an intervention and must be logged.
4. Do not reveal hidden prior evidence in Blind Protocols.
5. Hard-coded/model-generated domain vocabulary is proposed knowledge until sourced.
6. Retrospective memory is not contemporaneous evidence.
7. Protocol abandonment is not a failed obligation.
8. Broad development is permitted; simultaneous field manipulations must remain interpretable.

## Compiled planning packet

Either:

- regenerate from canonical sources automatically; or
- mark it non-authoritative.

Do not maintain divergent manual copies.

---

# Development workstreams

These can move in parallel when their schema ownership is clear.

## Workstream A — Current integrity

- prediction lineage;
- prediction artifact atomicity;
- concept IDs;
- concept exposure log;
- temporal source modes.

## Workstream B — Longitudinal substrate

- Thread model;
- Thread timeline;
- Episode linking;
- Compare.

## Workstream C — Protocol laboratory

- protocol configuration format;
- ProtocolRun;
- Free Capture;
- Blind Echo;
- Concept Lens;
- Calibration;
- Research Pull;
- Reflection Ladder.

## Workstream D — Concept / expertise layer

- source-backed concept library;
- domain scopes;
- aliases/examples/counterexamples;
- teach-back;
- user acceptance/rejection.

## Workstream E — Field experiments

Only a small set should be active at once.

Recommended first candidates after integrity fixes:

1. Concept Lens;
2. Blind Echo / Resonance Drift;
3. Liquid Question Ladder or Research Pull.

The exact three should be chosen from current natural use, not because this document lists them first.

---

# Do not block ordinary use

The user should continue capturing immediately.

No refactor should require pausing real-world use unless it risks data loss.

Backward compatibility with current Episodes is important.

Old Episodes may remain:

- unthreaded;
- protocol-less;
- concept-less.

That is acceptable.

---

# Definition of a successful roadmap update

The project has successfully absorbed this handoff when:

- current integrity fixes are captured as explicit work;
- Threads and Protocols are represented in design/docs;
- the large experiment backlog is preserved;
- only a small number of experiments are designated active;
- vocabulary is no longer treated as an unsourced static glossary;
- retrospective/longitudinal reflection is first-class;
- the user can keep using Free Capture with no added burden;
- future Solid/Liquid/Solidus development remains compatible with the new semantic model.

---

# Companion documents

Read in this order:

1. `10_INTEGRATED_DEVELOPMENT_ROADMAP.md`
2. `11_THREADS_PROTOCOLS_AND_LEARNING_ARCHITECTURE.md`
3. this handoff directive

The first document contains the full development/experiment inventory.

The second is the deeper specification of the new semantic layer.

This directive tells the project how to reconcile them with the existing canonical documentation.
