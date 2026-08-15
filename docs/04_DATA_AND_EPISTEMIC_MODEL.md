---
title: "Data and Epistemic Model"
project: "Les Enfants Terribles"
project_code: "LET"
status: "active_research_instrument"
version: "0.2"
owner: "Jonathan Lane"
created: "2026-08-13"
last_reviewed: "2026-08-15"
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
- behavior produced after intervention;
- contemporaneous evidence versus retrospective reconstruction.

The system should make it easier to be wrong safely.

## 2. Episode and Thread structure

An **Episode** is a bounded slice of lived experience that can contain multiple modalities, artifacts, predictions, and reflection phases.

A **Thread** is a persistent object of attention, skill, or inquiry that connects multiple Episodes across time.

```text
THREAD: "The Shining / Kubrick Visual Structure"
├── Episode 1 (Free Capture — Immediate Reaction)
│   ├── raw audio artifact
│   ├── faster-whisper transcript
│   └── Mission Brief analysis + Liquid question
├── Episode 2 (Blind Echo — 30 Days Later)
│   ├── blind recall reflection (hidden prior transcript)
│   ├── reveal & compare artifact
│   └── drift observation
└── Episode 3 (Concept Lens — Rewatch)
    ├── exposed lens: "Centering & Symmetry"
    ├── pre-rewatch prediction
    └── post-rewatch reflection
```

## 3. Core entities

### Thread

A persistent subject or inquiry across time:

```yaml
Thread:
  id: str
  title: str
  thread_type: str # movie | piano_piece | skill_concept | research_topic | project
  description: str
  status: str # active | dormant | closed
  created_at: timestamp
  updated_at: timestamp
```

### EpisodeThread

Many-to-many relationship linking Episodes to Threads:

```yaml
EpisodeThread:
  episode_id: str
  thread_id: str
  role: str # primary | related | evidence_for | generated_from
  created_at: timestamp
```

### Episode

A bounded experiential container:

```yaml
Episode:
  id: str
  title: str
  domain: str # movie | piano | cod | research | programming | general
  started_at: timestamp
  ended_at: timestamp
  created_at: timestamp
  status: str
  declared_mode: str # capture | explore | challenge | understand | improve | surprise | decide
  activity: str
  purpose: str
  notes: str
```

### Protocol & ProtocolRun

A **Protocol** defines a reusable cognitive procedure; a **ProtocolRun** tracks its live execution:

```yaml
Protocol:
  id: str # free_capture | blind_echo | concept_lens | calibration | research_pull
  version: str
  title: str
  purpose: str
  eligible_domains: list[str]
  steps: list[dict]
  completion_policy: str

ProtocolRun:
  id: str
  protocol_id: str
  protocol_version: str
  episode_id: str
  thread_id: str (nullable)
  started_at: timestamp
  completed_at: timestamp (nullable)
  status: str # active | completed | abandoned
  current_step: int
  visibility_state: dict # information barriers
```

### Prediction (Append-Only)

Pre-session hypotheses frozen before evidence or play:

```yaml
Prediction:
  id: str
  episode_id: str
  thread_id: str (nullable)
  prediction_type: str
  target_concept_id: str (nullable)
  statement_text: str (nullable)
  statement_artifact_id: str (nullable) # raw audio
  transcript_artifact_id: str (nullable) # derived Whisper transcript
  confidence: float (nullable)
  supersedes_id: str (nullable) # append-only correction
  locked_at: timestamp
  created_at: timestamp
```

### Concept, ConceptSource & ConceptExposure

Domain vocabulary backed by provenance:

```yaml
Concept:
  id: str # e.g. "cod.centering", "piano.rubato"
  term: str
  domain: str
  definition: str
  aliases: list[str]
  scope: str
  confidence: float
  status: str # proposed | useful | rejected | established_for_user
  version: str

ConceptSource:
  concept_id: str
  source_type: str # paper | book | gameplay_guide | music_pedagogy
  citation: str
  excerpt_or_note: str
  accessed_at: timestamp

ConceptExposure:
  id: str
  concept_id: str
  episode_id: str
  protocol_run_id: str (nullable)
  exposed_at: timestamp
  phase: str # before_activity | before_reflection | after_blind_reflection | research_pull
  user_requested: bool
  presentation: str # chip | card | glossary_hover | prompt
```

### Reflection

Human-authored meaning categorized by temporal and procedural phase:

```yaml
Reflection:
  id: str
  episode_id: str
  thread_id: str (nullable)
  protocol_run_id: str (nullable)
  phase: str # pre_session | immediate | prompted | delayed | blind_recall | post_reveal | post_evidence | retrospective_reconstruction
  modality: str # voice | text
  content_artifact_id: str
  prompt_id: str (nullable)
  created_at: timestamp
```

### Comparison & ResearchArtifact

```yaml
Comparison:
  id: str
  thread_id: str (nullable)
  episode_ids: list[str]
  comparison_type: str # immediate_vs_delayed | prediction_vs_reflection | blind_vs_lens | pre_rewatch_vs_post_rewatch
  processor: str
  created_at: timestamp
  artifact_id: str

ResearchArtifact:
  question: str
  sources: list[dict]
  candidate_concepts: list[dict]
  findings: str
  disagreements: str
  confidence: float
  application_hypotheses: list[str]
  suggested_next_observation: str
```

### Event & Artifact

```yaml
Event:
  id: str
  event_type: str
  occurred_at: timestamp
  recorded_at: timestamp
  source: str
  episode_id: str
  payload: dict

Artifact:
  id: str
  artifact_kind: str
  raw_or_derived: str # raw | derived
  mime_type: str
  path: str
  sha256: str
  created_at: timestamp
  occurred_at: timestamp
  source: str
  episode_id: str
  retention_class: str
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

For retrospective memory captures, explicitly support:

- **estimated_occurred_at:** e.g. `1997-06-01` or `1997`;
- **date_precision:** `exact` | `day` | `month` | `year` | `decade`;
- **source_mode:**
  - `immediate` (captured right after the event);
  - `delayed_reflection` (captured days/weeks later);
  - `retrospective_reconstruction` (recalled from years ago);
  - `rewatch` / `revisit` (re-experiencing an older artifact);
  - `external_historical_artifact` (imported historical note/log).

Reprocessing must not rewrite occurred or recorded time. Never fake precision.

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
| **GENE** | raw artifact, stable ID, hash, event time, append-only predictions |
| **MEME** | transcript, reflection, idea, procedure, argument, concept definitions |
| **SCENE** | activity, mode, purpose, thread, protocol, lens exposures, intervention history |
| **SENSE** | first-person meaning, affect, authentic expression, ambiguity |

## 9. Observation, intervention, and information barriers

The system must be able to answer:

- What did Solid estimate before Liquid asked anything?
- What did Jonathan say before seeing evidence or concepts?
- What changed after the question or lens exposure?
- Was a later behavior observed in a no-intervention period?
- Is this pattern partly produced by LET?

### 9.1 Information barriers & visibility state

Protocols can mandate strict visibility states to preserve epistemic cleanliness:

- `hidden_until: reveal` (e.g., in Blind Echo, prior transcripts remain hidden until current recall is frozen);
- `concept_palette: hidden` (in Blind capture, domain concepts are not surfaced to prevent unprompted noticing contamination);
- `frozen` (records locked from mutation before subsequent steps proceed).

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
