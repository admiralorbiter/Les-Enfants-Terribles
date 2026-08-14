---
title: "Agent Rules for Les Enfants Terribles"
project: "Les Enfants Terribles"
project_code: "LET"
status: "active_rules"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


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
