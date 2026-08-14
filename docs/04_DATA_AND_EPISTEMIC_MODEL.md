---
title: "Data and Epistemic Model"
project: "Les Enfants Terribles"
project_code: "LET"
status: "planning_baseline"
version: "0.1"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-13"
---


# Data and Epistemic Model

> *"There is no such thing as an absolute timeless enemy. Our enemies are always relative, depending on the times and the politics."*
> — **The Boss**, *Metal Gear Solid 3: Snake Eater*

## 1. Design objective

LET must preserve the difference between:

- experience;
- record;
- transcription;
- interpretation;
- inference;
- accepted belief;
- intervention;
- behavior produced after intervention.

The system should make it easier to be wrong safely.

## 2. Episode as the central unit

An **Episode** is a bounded slice of lived experience that can contain multiple modalities and stages.

Examples:

```text
Movie: Alien
├── Plex playback event
├── immediate voice reaction
├── transcript
├── Liquid question
├── voice follow-up
├── later review
└── changed interpretation
```

```text
Piano practice
├── pre-practice prediction
├── audio/video recording
├── MARK events
├── post-practice self-assessment
├── objective comparison
└── next-practice decision
```

Episodes are human-meaningful containers. Raw artifact identity does not depend on episode organization.

## 3. Core entities

### Episode

Suggested fields:

```yaml
id:
title:
domain:
started_at:
ended_at:
created_at:
status:
declared_mode:
activity:
purpose:
notes:
```

### Event

A timestamped occurrence:

```yaml
id:
event_type:
occurred_at:
recorded_at:
source:
episode_id:
payload:
```

Examples:

- capture.started;
- capture.completed;
- marker.created;
- movie.scrobbled;
- processor.started;
- intervention.shown;
- feedback.recorded.

### Artifact

A file or text object:

```yaml
id:
artifact_kind:
raw_or_derived:
mime_type:
path:
sha256:
created_at:
occurred_at:
source:
episode_id:
retention_class:
```

### Processor run

```yaml
id:
processor_name:
processor_version:
configuration:
started_at:
completed_at:
status:
input_artifact_ids:
output_artifact_ids:
prompt_hash:
model_provider:
model_name:
```

### Derivation

```yaml
source_artifact_id:
derived_artifact_id:
activity:
processor_run_id:
source_span:
created_at:
```

### Transcript segment

```yaml
artifact_id:
segment_index:
start_seconds:
end_seconds:
text:
speaker:
confidence:
```

### Reflection

Human-authored meaning:

```yaml
id:
episode_id:
phase: spontaneous | prompted | later
modality:
content_artifact_id:
prompt_id:
created_at:
```

### Observation

A bounded description:

```yaml
claim:
observer:
scope:
evidence:
confidence:
time:
```

Example:

> In three marked COD clips, Jonathan re-entered the same lane within ten seconds after death.

### Interpretation

Meaning assigned to observations:

> The re-entry may reflect impatience after death.

This is not equivalent to the observation.

### Hypothesis

A testable explanation:

> If the issue is frustration rather than map strategy, re-challenge frequency should increase after consecutive deaths.

### Twin snapshot

```yaml
clone: solid
estimated_mode:
state:
confidence:
evidence:
conflicting_evidence:
processor_run_id:
valid_at:
```

### Intervention candidate

```yaml
stance:
question_or_action:
rationale:
evidence:
expected_cognitive_value:
estimated_burden:
availability_requirements:
```

### Intervention

```yaml
candidate_id:
decision_point:
selected_option:
shown_at:
response_artifact_id:
dismissed:
experiment_condition:
```

### Feedback

```yaml
correctness:
usefulness:
novelty:
intrusiveness:
joy_effect:
would_use_again:
notes:
```

## 4. Epistemic classes

LET should use a compact, comprehensible set:

- **Source:** raw artifact or external record.
- **Observation:** directly described/measured pattern.
- **Interpretation:** assigned meaning.
- **Hypothesis:** testable explanation.
- **Prediction:** expected future result.
- **Decision:** user-authorized choice.
- **Commitment:** ratified ongoing intention.
- **Unknown:** materially missing.
- **Conflict:** incompatible evidence or perspectives.
- **Retraction:** item should no longer support current conclusions.
- **Historical:** true as a record of an earlier perspective.

These classes may become fields rather than visible labels in every interface.

## 5. Provenance chain

Example:

```text
audio-001.webm
   │ transcribed by faster-whisper vX
   ▼
transcript-003
   │ interpreted by Liquid prompt v2 via Claude
   ▼
interpretation-009
   │ accepted in part by Jonathan
   ▼
reflection-011
   │ contributes to Solid model v4
   ▼
snapshot-018
```

Every step remains inspectable.

## 6. Temporal model

At minimum distinguish:

- **occurred_at:** when the underlying episode/event happened;
- **recorded_at:** when LET received it;
- **created_at:** when a derived object was created;
- **valid_from / valid_to:** optional interval during which a claim applies;
- **superseded_at:** when a later item replaced its current authority.

Reprocessing must not rewrite occurred or recorded time.

## 7. Source strength and abstraction

A simple authority ladder:

```text
raw media
direct user statement
external system event
human-corrected transcript
automatic transcript
bounded observation
interpretation
cross-episode pattern
cognitive routine
identity/value inference
```

The ladder is not absolute. A raw recording can be ambiguous; a corrected transcript may be more usable. The purpose is to prevent high-level inference from masquerading as direct evidence.

## 8. GENE / MEME / SCENE / SENSE mapping

| Layer | Stored objects |
|---|---|
| **GENE** | raw artifact, stable ID, hash, event time |
| **MEME** | transcript, reflection, idea, procedure, argument |
| **SCENE** | activity, mode, purpose, environment, intervention history |
| **SENSE** | first-person meaning, affect, authentic expression, ambiguity |

## 9. Observation versus intervention

The system must be able to answer:

- What did Solid estimate before Liquid asked anything?
- What did Jonathan say before seeing evidence?
- What changed after the question?
- Was a later behavior observed in a no-intervention period?
- Is this pattern partly produced by LET?

This is a data-model requirement, not only an analysis concern.

## 10. Identity inference gate

Identity-level claims require:

1. multiple episodes;
2. temporal diversity;
3. context diversity;
4. contradictory evidence search;
5. explicit uncertainty;
6. human review;
7. limited use;
8. reconsideration date.

Example:

Poor:

> Jonathan dislikes sentimental endings.

Better:

> In three 2026 film reflections, Jonathan criticized endings he described as sentimental. In two other films, he positively described emotional closure. The current evidence supports a contextual hypothesis rather than a stable preference.

## 11. Raw and corrected transcript policy

Preserve:

- raw model transcript;
- corrected transcript;
- correction diff;
- model/version;
- timestamps.

A corrected transcript does not replace the recording.

## 12. Model-response policy

A response imported from a subscription interface should preserve:

- exported Mission Brief;
- brief hash;
- stated provider/model when known;
- raw response;
- parsed objects;
- human acceptance/rejection;
- subsequent use.

## 13. Retention

Initial policy:

- retain raw media indefinitely;
- retain all processor outputs during experimentation;
- permit later suppression from default views;
- never equate suppression with deletion;
- create backup and storage lifecycle tools before large video ingestion.

## 14. Minimal initial schema

The first implementation does not need every entity above.

Minimum:

- episodes;
- events;
- artifacts;
- processor_runs;
- derivations;
- jobs;
- interventions;
- feedback.

Add higher-order cognitive objects only after real episodes demonstrate their value.
