---
title: "Product Experience and User Flows"
project: "Les Enfants Terribles"
project_code: "LET"
status: "active_research_instrument"
version: "0.2"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-15"
---


# Product Experience and User Flows

> *"Life isn't just about passing on your genes. We can leave behind much more than just DNA. Through speech, music, literature and movies... what we've seen, heard, felt... anger, joy and sorrow... these are the things I will pass on. That's what I live for."*
> — **Solid Snake**, *Metal Gear Solid 2: Sons of Liberty*

## 1. Experience goal

LET should feel like an available cognitive instrument, not an obligation.

The basic interaction remains frictionless:

```text
open → record → stop → raw saved
```

Everything after that is configurable and optional:

```text
transcribe → select protocol / lens → debrief → challenge → answer → revisit → compare
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
- comparing interpretations across time;
- predicting before feedback;
- noticing uncertainty;
- challenging assumptions;
- transferring learning;
- making meaning.

For Jonathan, thinking is often the reward. Clerical setup is the friction.

## 3. Orthogonal cognitive dimensions

Avoid collapsing distinct cognitive concerns into a single mode. An encounter in LET combines:

- **Domain:** What kind of activity is this? (*Movies, Piano, COD, Research, Programming, Life*)
- **Thread:** What persistent line of inquiry does this belong to? (*The Shining, Chopin Nocturne, Re-challenging*)
- **Protocol:** What thinking procedure are we running? (*Free Capture, Blind Echo, Concept Lens, Research Pull*)
- **Mode:** How should Liquid behave? (*Explore, Challenge, Understand, Improve, Surprise, Decide, Capture*)
- **Lens:** What domain concept is deliberately primed or analyzed? (*Centering, Rubato, Diegetic Sound*)

### 3.1 Configurable thinking protocols

| Protocol | Purpose | Key Procedure |
|---|---|---|
| **Free Capture** | Low-friction unprompted thought | Speak naturally $\rightarrow$ save raw $\rightarrow$ transcript $\rightarrow$ done. |
| **Concept Lens** | Deliberately train attention/vocabulary | Select concept/lens $\rightarrow$ engage $\rightarrow$ reflect through that lens. |
| **Blind Echo** | Measure unprompted recall & drift | Prior episode hidden $\rightarrow$ unprompted recall frozen $\rightarrow$ reveal & compare. |
| **Calibration** | Test self-prediction against reality | Record pre-session prediction $\rightarrow$ session $\rightarrow$ compare prediction vs evidence. |
| **Research Pull** | Investigate unknown mechanisms | Frame unknown $\rightarrow$ run external/local literature pull $\rightarrow$ candidate concepts. |
| **Teach-Back** | Verify comprehension of candidate concept | System presents concept $\rightarrow$ user explains it in own words + provides example. |
| **After-Action Review** | Structured post-performance debrief | What was supposed to happen $\rightarrow$ what happened $\rightarrow$ why $\rightarrow$ next action. |
| **Reflection Ladder** | Deep multi-step progressive inquiry | Immediate impression $\rightarrow$ structural analysis $\rightarrow$ emotional/value synthesis. |

### 3.2 Blind vs. Lens UX distinction

- **Blind Protocol UX:** When measuring natural noticing, memory drift, or unprompted calibration, LET strictly hides previous episodes, past notes, and expert concept palettes. The user records freely, freezing their unprompted account before any reveal.
- **Lens Protocol UX:** When training perceptual acuity or adopting new vocabulary, LET surfaces the concept definition and examples *before* the session or reflection begins.

Neither is superior; both are first-class, and the UI makes the distinction transparent without information leaks.

## 4. Cognitive support modes

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

The initial system lets Jonathan choose explicitly. Later Solid may recommend the likely mode, but explicit choice remains available.

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

## 14. Longitudinal revisit & retrospective flows

### 14.1 Blind Echo & Resonance Drift

```text
Thread: "The Shining"
├── Episode 1 (Day 0): Immediate voice reaction (Free Capture)
└── Episode 2 (Day 30): Blind Echo
    ├── Old Episode 1 transcript strictly hidden
    ├── Spontaneous recall recorded: "What lingers? What scenes do I remember?"
    ├── Recall frozen
    ├── Episode 1 revealed
    └── Comparison artifact generated: What faded? What crystallized? What shifted in salience?
```

### 14.2 Rewatch / re-experience triads

```text
1. Pre-rewatch prediction / expectation (Append-only prediction record)
2. Rewatch experience
3. Post-rewatch reflection (Concept Lens or Free Capture)
4. Triad Compare: Prediction vs. Immediate Impression vs. Retrospective Memory
```

### 14.3 Retrospective memory capture

Capturing memories of past events from years ago:
- Distinct `source_mode = "retrospective_reconstruction"`
- Approximate timestamp `estimated_occurred_at` (e.g. `1998`, precision `year`)
- Contemporaneous recording timestamp `recorded_at`
- Never fakes timestamp precision; preserves memory as a current cognitive artifact about the past.
