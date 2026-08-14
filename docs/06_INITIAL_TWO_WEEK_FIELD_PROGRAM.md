---
title: "Initial Two-Week Field Program"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


# Initial Two-Week Field Program

## 1. Nature of the period

This is not a sprint to finish LET.

It is a **field program** in which a minimum substrate is developed, used across ordinary life, and revised only when use reveals a reason.

The period begins after repository creation and ends with an evidence review—not a feature-completion ceremony.

## 2. Desired outcome

By the end of the period, we should know:

- whether desktop voice capture is worth keeping;
- whether Episode is the right organizing unit;
- whether Liquid produces metacognitive novelty;
- whether self-prediction is useful in piano or COD;
- which operational friction matters;
- which domain naturally pulls the project forward;
- what should be built next, removed, or left manual.

## 3. Minimum meaningful build

The first vertical slice should support:

1. local app launch;
2. audio record/stop;
3. atomic raw save;
4. SQLite episode/artifact record;
5. recent-episode list;
6. audio playback;
7. background transcription;
8. transcript view;
9. follow-up voice capture attached to the same episode;
10. backup/doctor basics.

Strongly preferred within the field period:

11. mode selection;
12. manual Liquid question;
13. Mission Brief export;
14. external-response import;
15. simple feedback;
16. replay of one processor.

Not required:

- passive sensors;
- automatic clone model;
- mobile;
- polished dashboard;
- autonomous intervention;
- screen recording;
- embeddings;
- graph;
- provider API.

## 4. Foundation window

The first few development sessions should answer only:

> Can Jonathan capture and recover an episode confidently?

Recommended sequence:

```text
record
  ↓
save raw
  ↓
show recent episode
  ↓
play it
  ↓
restart application
  ↓
play it again
  ↓
backup and restore
```

Only after that:

```text
transcribe
  ↓
attach transcript
  ↓
fail/retry
```

## 5. Week-one emphasis: capture and one useful question

Use LET opportunistically in ordinary life.

### Movies

After a movie:

- record immediate reaction;
- preserve it before external reviews;
- optionally ask Liquid to find one opening;
- continue only if interesting.

### Piano

At one natural practice boundary:

- state what you expect went well/wrong;
- optionally record or import evidence;
- compare afterward.

### Call of Duty

Between matches or after a session:

- use a quick reflection;
- optionally state one question;
- do not interrupt play.

### Research/spontaneous thought

Capture the idea.

Liquid may:

- define;
- challenge;
- ask what would change the conclusion;
- suggest one adjacent connection.

### Programming

At a breakpoint:

- what problem am I solving?
- what do I currently think?
- what am I waiting on?
- what did an agent change in my model?

## 6. Week-two emphasis: refine the loop, not the breadth

Choose the most promising observed use and improve one piece.

Candidate directions:

- better one-question selection;
- a smoother voice follow-up;
- self-prediction/evidence comparison;
- Mission Brief export/import;
- replay;
- better episode view;
- MARK events.

Do not pursue all of them.

Run at most three active experiments:

1. E001 Capture and episode viability.
2. E002 Liquid specificity.
3. E003 Self-prediction and evidence.

E004–E006 may be used only if they directly reduce friction in those three.

## 7. Suggested natural rhythm

### Capture

- press Record;
- speak;
- stop;
- leave.

### Optional immediate debrief

- choose mode;
- answer one question or continue;
- stop when the thought is complete.

### Processing

- transcription and analysis happen later;
- no need to watch.

### Revisit

- only when desired or when an experiment calls for it.

## 8. Minimal feedback

After a Liquid interaction, one tap may be enough:

- useful;
- interesting;
- wrong;
- already knew;
- intrusive;
- keep going;
- stop.

Optional voice note:

> Why was this useful?

## 9. Expedite path

To test advanced cognition quickly without expensive integration:

1. record in LET;
2. transcribe locally;
3. export a structured Mission Brief;
4. open Antigravity or an existing AI subscription;
5. run the brief through a strong model;
6. import or paste the result;
7. answer inside LET by voice.

This is a valid first-class workflow.

Do not mistake manual transport for architectural failure. It buys learning before integration.

## 10. Synthetic corpus

Before experimental processors touch live data, maintain a small synthetic corpus:

- fake movie reaction with vague language;
- fake piano self-assessment contradicted by evidence;
- fake COD frustration hypothesis;
- fake research idea with an unsupported assumption;
- fake work episode;
- transcript error;
- conflicting model outputs;
- identity overreach case.

The corpus supports agent development and regression tests without risking the archive.

## 11. Friction log

Record only meaningful friction:

```markdown
Context:
What I was trying to do:
Friction:
Workaround:
Did it prevent use?
Possible smallest fix:
```

Do not quantify every interaction.

## 12. What to watch for

Positive signals:

- desire to capture;
- richer specificity;
- spontaneous follow-up;
- useful disagreement;
- revised belief;
- better self-calibration;
- increased enjoyment;
- wanting to revisit.

Warning signals:

- avoiding the app;
- generic questions;
- feeling judged;
- turning play into obligation;
- excessive setup;
- transcript cleanup becoming the project;
- accumulating unreviewed analysis;
- building more than using.

## 13. End-of-period review

Review a small set of episodes, not only aggregate counts.

Ask:

1. Which capture would otherwise not exist?
2. What did Liquid make Jonathan notice?
3. Which question was best and why?
4. Which question should never have been asked?
5. Did any self-prediction differ from evidence?
6. Did LET increase, preserve, or reduce joy?
7. What operation created the most friction?
8. What feature was unnecessary?
9. Which domain produced the strongest pull?
10. What is the next gate?

Possible decisions:

- continue foundation;
- deepen Liquid;
- deepen one domain;
- build replay;
- pause development and collect more;
- simplify;
- stop.

## 14. Definition of a good first two weeks

A good field period does not require a clone.

It requires enough lived evidence to make the next architectural decision less imaginary.
