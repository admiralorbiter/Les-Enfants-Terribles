---
title: "Experiment Program and Decision Gates"
project: "Les Enfants Terribles"
project_code: "LET"
status: "active_research_instrument"
version: "0.2"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-15"
---


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

## 3. Development backlog freedom vs. experimental concurrency

A crucial distinction governs LET's evolution:

- **Development breadth is unconstrained:** The system may build, prototype, and scaffold dormant protocols, concept libraries, comparison tools, fixtures, and branches as quickly as engineering velocity allows.
- **Field experimental concurrency is strictly constrained:** No more than approximately **three active field manipulations/interventions** should run simultaneously in Jonathan's daily use.

This rule ensures that when changes in thinking, vocabulary, or recall occur, we can reliably attribute the cause to a specific intervention rather than confounding multiple overlapping probes.

### Experiment lifecycle

1. **Observe:** preserve a real friction, opportunity, or surprise.
2. **Frame:** turn it into a question without assuming the answer.
3. **Baseline:** identify the simplest current method.
4. **Probe:** create the smallest discriminating intervention or Protocol.
5. **Use:** run it in real or faithfully simulated work.
6. **Evaluate:** record outcome, burden, confounders, and surprise.
7. **Decide:** keep, revise, defer, or remove.
8. **Propagate:** update architecture and open questions.

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

### E008 — Concept Lens Priming vs. Spontaneous Noticing

**Question:** Does surfacing a specific domain concept (e.g. *rubato*, *centering*) before an experience improve discrimination and perceptual resolution, or does it narrow spontaneous noticing?

**Probe:** Compare Concept Lens sessions with unprompted Free Capture sessions across the same Thread.

### E009 — Blind Echo & Resonance Drift

**Question:** How does unprompted memory of a film or concept change across 7, 30, and 90 days?

**Probe:** Hide initial capture $\rightarrow$ record blind recall $\rightarrow$ reveal and generate comparison artifact.

### E010 — Retrospective Memory vs. Contemporaneous Capture

**Question:** How do retrospective reconstructions of older life events differ in detail and certainty from contemporaneous captures?

**Probe:** Use `source_mode: retrospective_reconstruction` with approximate dates.

### E011 — Research Pull Value vs. Manual AI Exploration

**Question:** Does structured Research Pull (packaging context + question + candidate concept extraction) yield more actionable domain knowledge than ad-hoc search?

### E012 — Teach-Back Verification vs. Passive Reading

**Question:** Does requiring a 30-second teach-back note improve retention and appropriate transfer of a newly acquired domain concept?

### E013 — Re-Experience Triad Comparison

**Question:** What does comparing pre-prediction, original reaction, and post-rewatch reflection reveal about personal taste and perceptual stability?

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
